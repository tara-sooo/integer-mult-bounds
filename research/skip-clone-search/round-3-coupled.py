#!/usr/bin/env python3
"""Small deterministic two-round paid-clone neighborhood search."""
from copy import deepcopy
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import shlex
import struct
import subprocess
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('issue6_search', HERE/'search.py')
search = importlib.util.module_from_spec(spec)
spec.loader.exec_module(search)
cg = search.cg

NEIGHBORHOODS = (
    dict(id='n1-single-first', count=1, positions='first', rule='shortest-chain', providers='preserve'),
    dict(id='n2-single-last', count=1, positions='last', rule='longest-chain', providers='last-alternative'),
    dict(id='n3-two-spread', count=2, positions='thirds', rule='sha256-choice', providers='sha256-choice'),
    dict(id='n4-three-spread', count=3, positions='quarters', rule='shortest-chain', providers='alternatives-first'),
)


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def canonical_edges(edges):
    payload = json.dumps(sorted([list(x) for x in edges]), separators=(',', ':')).encode()
    return sha256(payload).hexdigest()


def compile_reserved_screen(work):
    source = search.PROFILE.read_text()
    guard = 'assert(lin && "A pinned carrier matching is required");'
    donors = ('std::vector<U>donors;for(U x=1;x<n;x++)if(active[x]&&args[x][0]&&'
              'adjacency(x,[](U){return true;}))donors.push_back(x);')
    if guard not in source or donors not in source:
        raise RuntimeError('Pinned matching profiler changed')
    source = source.replace('#include <algorithm>', '#include <algorithm>\n#include <sstream>')
    source = source.replace(guard, '// Issue 6 FAST screen: output the matching before profiling.')
    replacement = (
        'std::vector<U>excluded(n);const char* ex=getenv("ISSUE6_EXCLUDED_DONORS");'
        'if(ex){std::istringstream es(ex);U x;while(es>>x)if(x<n)excluded[x]=1;}'
        'std::vector<U>donors;for(U x=1;x<n;x++)if(!excluded[x]&&active[x]&&args[x][0]&&'
        'adjacency(x,[](U){return true;}))donors.push_back(x);')
    source = source.replace(donors, replacement)
    if donors in source:
        raise RuntimeError('Provider reservation patch failed')
    screen_source = work/'profiles-coupled-screen.cpp'
    screen_source.write_text(source)
    binary = work/'profiles-coupled-screen'
    command = [*shlex.split(os.environ.get('CXX', 'c++')), '-O3', '-std=c++17',
               '-include', 'algorithm', '-I', str(ROOT/'scripts/partial_swap'),
               str(screen_source), '-o', str(binary)]
    subprocess.run(command, check=True)
    return binary, digest(screen_source)


def match_screen(binary, circuit, work, h, label, reserved=()):
    dag, links_path = work/f'{label}-{h}.bin', work/f'{label}-{h}.uses'
    search.export(circuit, dag)
    env = dict(os.environ)
    env.pop('LINKS_IN', None)
    env.pop('DUMP_EDGES', None)
    env['ISSUE6_EXCLUDED_DONORS'] = ' '.join(map(str, sorted(reserved)))
    proc = subprocess.Popen([str(binary), str(dag), str(links_path)], stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, text=True, env=env)
    try:
        line = proc.stdout.readline()
        if not line:
            raise RuntimeError(f'Matching screen returned no summary for {label}, h={h}')
        row = json.loads(line)
    finally:
        proc.terminate()
        proc.wait()
        proc.stdout.close()
    raw = links_path.read_bytes()
    n, count = struct.unpack_from('<2I', raw)
    if len(raw) != 8+8*count:
        raise RuntimeError('Matching output has an invalid binary length')
    edges = [list(struct.unpack_from('<2I', raw, 8+8*i)) for i in range(count)]
    if n != len(circuit.args) or count != row['matched']:
        raise RuntimeError('Matching output disagrees with screen summary')
    return row, edges, digest(links_path)


def layout_maps(circuit, round_doc, result):
    _, _, order = search.rank_times(circuit)
    before, terminal = {}, []
    for index, job in enumerate(round_doc['jobs']):
        if job['first'] >> 31:
            terminal.append(index)
        else:
            before.setdefault(job['first']//2, []).append(index)
    original, clones, next_node = {}, {}, 1
    for old in order:
        for index in before.get(old, []):
            clones[index] = next_node
            next_node += 1
        original[old] = next_node
        next_node += 1
    for index in terminal:
        clones[index] = next_node
        next_node += 1
    if next_node != len(result.args):
        raise RuntimeError('Node-layout reconstruction differs from strict replay')
    return original, clones


def intermediate_map(base, base_doc, base_result, candidate_doc, candidate_result):
    base_original, base_clones = layout_maps(base, base_doc, base_result)
    candidate_original, candidate_clones = layout_maps(base, candidate_doc, candidate_result)
    result = {base_original[node]: candidate_original[node] for node in base_original}
    result.update({base_clones[index]: candidate_clones[index] for index in base_clones})
    if set(result) != set(range(1, len(base_result.args))):
        raise RuntimeError('First-round node correspondence is incomplete')
    if len(set(result.values())) != len(result) or len(result) != len(candidate_result.args)-1:
        raise RuntimeError('First-round node correspondence is not bijective')
    return result


def map_use(edge, node_map):
    return edge if edge >> 31 else 2*node_map[edge//2]+(edge%2)


def neighborhood_jobs(round_doc, h, case):
    count, style = case['count'], case['positions']
    n = len(round_doc['jobs'])
    if style == 'first':
        indexes = [0]
    elif style == 'last':
        indexes = [n-1]
    elif style == 'thirds':
        indexes = [n//3, (2*n)//3]
    elif style == 'quarters':
        indexes = [n//4, n//2, (3*n)//4]
    else:
        indexes = sorted(range(n), key=lambda i: sha256(
            f'issue6-coupled-v1:{case["id"]}:{h}:{i}'.encode()).digest())[:count]
    return sorted(set(indexes))


def choose_first_round(base, doc, h, case):
    round_doc = doc['rounds'][0]
    choices = search.chain_options(base, round_doc)
    indexes = neighborhood_jobs(round_doc, h, case)
    edits = []
    for index in indexes:
        job, options = round_doc['jobs'][index], choices[index]
        alternatives = [x for x in options if x != (job['first'], tuple(job['chain']))]
        if not alternatives:
            raise ValueError(f'no alternate complete chain for first-round job {index}')
        if case['id'] == 'n1-single-first':
            selected = alternatives[0]
        else:
            key = f'issue6-coupled-v1:{case["id"]}:{h}:{index}'.encode()
            selected = alternatives[int.from_bytes(sha256(key).digest()[:8], 'big') % len(alternatives)]
        old_first, old_chain = job['first'], job['chain'][:]
        job['first'], job['chain'] = selected[0], list(selected[1])
        edits.append(dict(job=index, parent=job['parent'], old_first=old_first,
                          old_chain=old_chain, first=job['first'], chain=job['chain'][:]))
    return edits


def remap_second_round(template, node_map, source_digest):
    result = deepcopy(template)
    for job in result['jobs']:
        job['parent'] = node_map[job['parent']]
        job['providers'] = [node_map[x] for x in job['providers']]
        job['source_children'] = [node_map[x] for x in job['source_children']]
        job['first'] = map_use(job['first'], node_map)
        job['chain'] = [map_use(x, node_map) for x in job['chain']]
    result['source_graph_sha256'] = source_digest
    result['output_graph_sha256'] = '0'*64
    return result


def provider_pair_options(circuit, round_doc):
    _, times, order = search.rank_times(circuit)
    supports = cg.scalar_supports(circuit)
    consumers = {}
    for gate in order:
        args = circuit.args[gate]
        if args is not None:
            for child in args:
                consumers.setdefault(child, []).append(gate)
    result = []
    for job in round_doc['jobs']:
        parent = job['parent']
        first = use_info(circuit, order, times, job['first'])
        if first is None or first[0] != parent:
            raise ValueError('Mapped first use is not a use of its clone parent')
        children = job['source_children']
        if (supports[children[0]] & supports[children[1]] or
                supports[children[0]] | supports[children[1]] != supports[parent] or
                circuit.core[children[0]] & circuit.core[children[1]] != circuit.core[parent] or
                circuit.union[children[0]] | circuit.union[children[1]] != circuit.union[parent]):
            raise ValueError('Mapped source children do not partition the parent')
        sides = []
        for child in children:
            sides.append([gate for gate in consumers.get(child, ())
                          if times[gate] < first[2] and
                          not (circuit.core[parent] & ~circuit.core[gate] or
                               circuit.union[gate] & ~circuit.union[parent])])
        pairs = [(left, right) for left in sides[0] for right in sides[1] if left != right]
        original = tuple(job['providers'])
        pairs.sort(key=lambda pair: (pair != original, times[pair[0]]+times[pair[1]], pair))
        if not pairs:
            raise ValueError('No distinct, timely provider pair for mapped source partition')
        result.append(pairs)
    return result


def select_provider_pairs(round_doc, options, case, h):
    claimed, selected = set(), []
    for index, (job, choices) in enumerate(zip(round_doc['jobs'], options)):
        original = tuple(job['providers'])
        if case['providers'] == 'preserve':
            ordered = sorted(choices, key=lambda pair: (pair != original, pair))
        elif case['providers'] == 'last-alternative':
            ordered = sorted(choices, key=lambda pair: (pair == original if index == len(options)-1 else pair != original, pair))
        elif case['providers'] == 'alternatives-first':
            ordered = sorted(choices, key=lambda pair: (pair == original, pair))
        else:
            key = f'issue6-coupled-v1:providers:{case["id"]}:{h}:{index}'.encode()
            ordered = sorted(choices, key=lambda pair: sha256(key+struct.pack('<2I', *pair)).digest())
        available = [pair for pair in ordered if not set(pair) & claimed]
        if not available:
            raise ValueError(f'provider capacity collision at job {index}')
        pair = available[0]
        job['providers'] = list(pair)
        claimed.update(pair)
        selected.append(dict(job=index, mapped_original=list(original), candidate_pairs=len(choices),
                             selected=list(pair), changed=pair != original))
    if len(claimed) != 2*len(round_doc['jobs']):
        raise ValueError('Selected provider capacities are not globally distinct')
    return selected


def check_provider_selection(circuit, round_doc):
    _, times, order = search.rank_times(circuit)
    supports = cg.scalar_supports(circuit)
    providers, parents, formal = set(), set(), set()
    for job in round_doc['jobs']:
        parent, pair, children = job['parent'], job['providers'], job['source_children']
        first = use_info(circuit, order, times, job['first'])
        if first is None or first[0] != parent:
            return 'clone first use does not consume its parent'
        if parent in parents or parent in formal:
            return 'clone parent conflicts with another clone partition'
        if set(children) & parents:
            return 'source partition depends on another cloned parent'
        parents.add(parent)
        formal.update(children)
        if (len(pair) != 2 or pair[0] == pair[1] or set(pair) & providers):
            return 'provider capacities are not distinct'
        providers.update(pair)
        if (supports[children[0]] & supports[children[1]] or
                supports[children[0]] | supports[children[1]] != supports[parent] or
                circuit.core[children[0]] & circuit.core[children[1]] != circuit.core[parent] or
                circuit.union[children[0]] | circuit.union[children[1]] != circuit.union[parent]):
            return 'source children do not form the parent partition'
        for provider, child in zip(pair, children):
            if (provider not in circuit.active or circuit.args[provider] is None or
                    child not in circuit.args[provider]):
                return 'provider does not own its named source child'
            if times[provider] >= first[2]:
                return 'provider is not earlier than the first moved use'
            if (circuit.core[parent] & ~circuit.core[provider] or
                    circuit.union[provider] & ~circuit.union[parent]):
                return 'provider violates the parent core/cover'
    return None


def check_matching(circuit, edges, reserved):
    ranks, times, order = search.rank_times(circuit)
    donors, incoming = set(), set()
    for donor, edge in edges:
        info = use_info(circuit, order, times, edge)
        if info is None or donor not in circuit.active or circuit.args[donor] is None:
            return 'matching contains an invalid gate or use'
        target, event = info[1], info[3]
        if donor in donors or edge in incoming:
            return 'matching capacity collision'
        if donor in reserved:
            return 'matching consumes a reserved provider capacity'
        if info[0] not in circuit.args[donor]:
            return 'matching donor does not own the actual operand'
        if (ranks[donor], donor) >= (ranks[target], event):
            return 'matching carrier is noncausal'
        if circuit.core[target] & ~circuit.core[donor] or circuit.union[donor] & ~circuit.union[target]:
            return 'matching carrier violates core/cover nesting'
        donors.add(donor)
        incoming.add(edge)
    return None


def use_info(circuit, order, times, edge):
    if type(edge) is not int or edge < 0 or edge >= 1 << 32:
        return None
    roots = list(circuit.outputs.values())
    if edge >> 31:
        index = edge & 0x7fffffff
        if index >= len(roots):
            return None
        return roots[index], roots[index], len(order)+index, len(order)+index
    owner = edge//2
    if owner not in circuit.active or circuit.args[owner] is None:
        return None
    return circuit.args[owner][edge%2], owner, times[owner], owner


def legal_second_round_choices(circuit, round_doc):
    _, times, order = search.rank_times(circuit)
    incoming, next_use = set(), {}
    for donor, edge in round_doc['matching_before']:
        info = use_info(circuit, order, times, edge)
        if info is None:
            continue
        try:
            pos = circuit.args[donor].index(info[0])
        except (IndexError, AttributeError):
            continue
        incoming.add(edge)
        next_use[2*donor+pos] = edge
    all_options = search.chain_options(circuit, round_doc)
    chosen = []
    for job, options in zip(round_doc['jobs'], all_options):
        valid = []
        for first, chain in options:
            info = use_info(circuit, order, times, first)
            if info is None or info[0] != job['parent'] or first in incoming:
                continue
            if any(times[p] >= info[2] for p in job['providers']):
                continue
            expected, seen, current = [], set(), first
            while current not in seen:
                seen.add(current)
                item = use_info(circuit, order, times, current)
                if item is None or item[0] != job['parent']:
                    expected = []
                    break
                expected.append(current)
                if current not in next_use:
                    break
                current = next_use[current]
            if expected and tuple(expected) == tuple(chain):
                valid.append((first, tuple(chain)))
        if not valid:
            raise ValueError(f'no legal second-round continuation for parent {job["parent"]}')
        chosen.append(valid)
    return chosen


def select_second_round(round_doc, options, case, h):
    claimed = set()
    selected = []
    for index, (job, choices) in enumerate(zip(round_doc['jobs'], options)):
        free = [choice for choice in choices if not set(choice[1]) & claimed]
        if not free:
            raise ValueError(f'second-round chain collision at job {index}')
        rule = case['rule']
        if rule == 'shortest-chain':
            choice = min(free, key=lambda x: (len(x[1]), x[1], x[0]))
        elif rule == 'longest-chain':
            choice = max(free, key=lambda x: (len(x[1]), tuple(-e for e in x[1]), -x[0]))
        else:
            key = f'issue6-coupled-v1:round2:{case["id"]}:{h}:{index}'.encode()
            choice = free[int.from_bytes(sha256(key).digest()[:8], 'big') % len(free)]
        job['first'], job['chain'] = choice[0], list(choice[1])
        claimed.update(choice[1])
        selected.append(dict(job=index, parent=job['parent'], providers=job['providers'][:],
                             source_children=job['source_children'][:], first=job['first'],
                             chain=job['chain'][:]))
    return selected


def remap_edges(edges, node_map):
    return [[node_map[donor], map_use(edge, node_map)] for donor, edge in edges]


def provider_capacity_negative(circuit, round_doc):
    ranks, times, order = search.rank_times(circuit)
    donors = {donor for donor, _ in round_doc['matching_before']}
    for job in round_doc['jobs']:
        first = use_info(circuit, order, times, job['first'])
        for side, child in enumerate(job['source_children']):
            other = job['providers'][1-side]
            for donor in sorted(donors):
                if donor == other or circuit.args[donor] is None or child not in circuit.args[donor]:
                    continue
                if times[donor] >= first[2]:
                    continue
                nested = not (circuit.core[job['parent']] & ~circuit.core[donor] or
                              circuit.union[donor] & ~circuit.union[job['parent']])
                if not nested:
                    continue
                trial = deepcopy(round_doc)
                trial_job = trial['jobs'][round_doc['jobs'].index(job)]
                trial_job['providers'][side] = donor
                try:
                    cg.replay_round(circuit, trial)
                except ValueError as error:
                    if str(error) == 'Provider capacity already used':
                        return dict(status='rejected', reason=str(error),
                                    provider=donor, source_child=child)
    return dict(status='not_found', reason='no isolated admissible provider edge found')


def illegal_move_negative(circuit, round_doc):
    trial = deepcopy(round_doc)
    first_job, other = trial['jobs'][0], trial['jobs'][1]
    if other['parent'] == first_job['parent']:
        raise RuntimeError('Negative move control needs distinct parents')
    first_job['first'] = other['first']
    first_job['chain'] = [other['first']]
    try:
        cg.replay_round(circuit, trial)
    except ValueError as error:
        if 'Clone must start an actual parent chain' in str(error):
            return dict(status='rejected', reason=str(error))
        return dict(status='rejected', reason=str(error))
    raise RuntimeError('Illegal clone-move control unexpectedly passed')


def no_op_control(binary, work, h, baseline, expected):
    doc = search.baseline_jobs(h)
    base = cg.base_graph(h)
    mid = cg.replay_round(base, doc['rounds'][0])
    provider_options = provider_pair_options(mid, doc['rounds'][1])
    original_pairs_present = all(tuple(job['providers']) in choices
                                 for job, choices in zip(doc['rounds'][1]['jobs'], provider_options))
    if not original_pairs_present:
        raise RuntimeError(f'No-op provider enumeration lost a pinned pair h={h}')
    providers = {p for job in doc['rounds'][1]['jobs'] for p in job['providers']}
    row, edges, link_hash = match_screen(binary, mid, work, h, 'control-intermediate', providers)
    pinned_edges = doc['rounds'][1]['matching_before']
    if canonical_edges(edges) != canonical_edges(pinned_edges):
        raise RuntimeError(f'No-op intermediate matching differs from pinned h={h}')
    doc['rounds'][1]['matching_before'] = edges
    # Keep the verified pinned second-round jobs; only the matching was rebuilt.
    final = cg.replay_round(mid, doc['rounds'][1])
    if cg.digest(final) != doc['rounds'][1]['output_graph_sha256']:
        raise RuntimeError(f'No-op schedule did not reproduce pinned output h={h}')
    final_row, final_edges, final_link_hash = match_screen(binary, final, work, h, 'control-final')
    if final_row['R'] != expected[f'R{h}']:
        raise RuntimeError(f'No-op final R differs from saved baseline h={h}')
    control = dict(intermediate=dict(R=row['R'], matched=row['matched'], rank_sum=row['rank_sum'],
                                  matching_sha256=link_hash, matching_equal_pinned=True,
                                  graph_sha256=cg.digest(mid)),
                final=dict(R=final_row['R'], matched=final_row['matched'],
                           rank_sum=final_row['rank_sum'], clones=final.clone_count,
                           matching_sha256=final_link_hash, graph_sha256=cg.digest(final)),
                provider_pair_enumeration=dict(jobs=len(provider_options),
                                               options_per_job=[len(x) for x in provider_options],
                                               pinned_pairs_present=original_pairs_present),
                final_matching_edges_sha256=final_link_hash)
    return control, final_edges


def stale_matching_control(candidate_mid, baseline_second, node_map):
    stale = remap_second_round(baseline_second, node_map, cg.digest(candidate_mid))
    stale['matching_before'] = remap_edges(baseline_second['matching_before'], node_map)
    try:
        search.replay_unpinned(candidate_mid, stale)
    except ValueError as error:
        return dict(status='rejected', reason=str(error))
    return dict(status='still-valid', reason='remapped pinned edges remain admissible')


def evaluate_neighbor(binary, work, h, case, baseline, baseline_mid, baseline_final_edges):
    doc = search.baseline_jobs(h)
    base = cg.base_graph(h)
    first_doc = doc['rounds'][0]
    try:
        edits = choose_first_round(base, doc, h, case)
        first_doc['output_graph_sha256'] = '0'*64
        mid = search.replay_unpinned(base, first_doc)
    except ValueError as error:
        return dict(status='rejected', h=h, case=case['id'], phase='first-round',
                    reason=str(error))
    first_doc['output_graph_sha256'] = cg.digest(mid)
    node_map = intermediate_map(base, baseline['rounds'][0], baseline_mid,
                                first_doc, mid)
    second = remap_second_round(baseline['rounds'][1], node_map, cg.digest(mid))
    try:
        provider_options = provider_pair_options(mid, second)
        provider_selection = select_provider_pairs(second, provider_options, case, h)
        provider_error = check_provider_selection(mid, second)
        if provider_error:
            raise ValueError(provider_error)
    except ValueError as error:
        return dict(status='not-evaluated', h=h, case=case['id'], phase='provider-enumeration',
                    reason=str(error), edits=edits, intermediate=dict(graph_sha256=cg.digest(mid)))
    providers = [p for job in second['jobs'] for p in job['providers']]
    if len(providers) != len(set(providers)):
        return dict(status='not-evaluated', h=h, case=case['id'], phase='provider-reservation',
                    reason='mapped provider capacities collide', edits=edits,
                    intermediate=dict(graph_sha256=cg.digest(mid)))
    reserved = set(providers)
    match_row, edges, links_hash = match_screen(binary, mid, work, h,
                                                f'{case["id"]}-intermediate', reserved)
    if reserved & {donor for donor, _ in edges}:
        raise RuntimeError('Reserved provider was selected as an intermediate donor')
    matching_error = check_matching(mid, edges, reserved)
    if matching_error:
        return dict(status='not-evaluated', h=h, case=case['id'], phase='matching-validation',
                    reason=matching_error, edits=edits,
                    intermediate=dict(R=match_row['R'], matched=match_row['matched'],
                                     rank_sum=match_row['rank_sum'], graph_sha256=cg.digest(mid),
                                     matching_sha256=links_hash))
    second['matching_before'] = edges
    baseline_mapped = remap_edges(baseline['rounds'][1]['matching_before'], node_map)
    matching_delta = len(set(map(tuple, baseline_mapped)) ^ set(map(tuple, edges)))
    stale_check = (stale_matching_control(mid, baseline['rounds'][1], node_map)
                   if case['id'] == 'n1-single-first' else None)
    try:
        choices = legal_second_round_choices(mid, second)
        rebuilt_jobs = select_second_round(second, choices, case, h)
        final = search.replay_unpinned(mid, second)
    except ValueError as error:
        return dict(status='not-evaluated', h=h, case=case['id'], phase='second-round-rebuild',
                    reason=str(error), edits=edits,
                    intermediate=dict(R=match_row['R'], matched=match_row['matched'],
                                     rank_sum=match_row['rank_sum'], graph_sha256=cg.digest(mid),
                                     matching_sha256=links_hash, matching_changed_edges=matching_delta),
                    stale_matching_reuse=stale_check,
                    provider_selection=provider_selection)
    second['output_graph_sha256'] = cg.digest(final)
    final_row, final_edges, final_hash = match_screen(binary, final, work, h,
                                                       f'{case["id"]}-final')
    final_matching_delta = len(set(map(tuple, baseline_final_edges)) ^ set(map(tuple, final_edges)))
    return dict(status='screened', h=h, case=case['id'], edits=edits,
                intermediate=dict(R=match_row['R'], matched=match_row['matched'],
                                 rank_sum=match_row['rank_sum'], graph_sha256=cg.digest(mid),
                                 matching_sha256=links_hash, matching_changed_edges=matching_delta,
                                 reserved_provider_count=len(reserved)),
                second_round=dict(clones=len(second['jobs']), jobs=rebuilt_jobs,
                                  provider_selection=provider_selection,
                                  provider_pair_candidate_counts=[len(x) for x in provider_options],
                                  provider_pairs_changed=sum(x['changed'] for x in provider_selection),
                                  matching_before_sha256=links_hash),
                final=dict(R=final_row['R'], matched=final_row['matched'],
                           rank_sum=final_row['rank_sum'], clones=final.clone_count,
                           matching_sha256=final_hash, matching_changed_edges=final_matching_delta,
                           graph_sha256=cg.digest(final)),
                stale_matching_reuse=stale_check,
                invalid_move_control=illegal_move_negative(mid, second)
                if case['id'] == 'n1-single-first' else None)


def run():
    started = time.monotonic()
    previous_fast = json.loads((HERE/'round-2-fast.json').read_text())
    previous = json.loads((HERE/'screening.json').read_text())
    expected = previous['baseline']
    pins = previous['source_sha256']
    for name, digest_expected in pins['source_files'].items():
        if digest(ROOT/name) != digest_expected:
            raise RuntimeError(f'Pinned source changed: {name}')
    if digest(HERE/'baseline-SOURCE.json') != pins['source_manifest_sha256']:
        raise RuntimeError('Baseline source manifest changed')
    for h in (23, 25):
        if digest(HERE/f'baseline-clone-jobs-{h}.json') != pins['clone_jobs'][str(h)]:
            raise RuntimeError(f'Baseline clone schedule changed: h={h}')
        if digest(HERE/f'baseline-original-{h}.json') != pins['role_records'][str(h)]:
            raise RuntimeError(f'Baseline role record changed: h={h}')
    if digest(HERE/'baseline-parameters.json') != pins['parameters']:
        raise RuntimeError('Baseline exact parameters changed')
    controls, results, baseline_final_edges = {}, [], {}
    with tempfile.TemporaryDirectory(prefix='issue6-coupled-search-') as directory:
        work = Path(directory)
        binary, compiled_source_hash = compile_reserved_screen(work)
        baseline_docs, baseline_mids = {}, {}
        for h in (23, 25):
            baseline_docs[h] = search.baseline_jobs(h)
            base = cg.base_graph(h)
            baseline_mids[h] = cg.replay_round(base, baseline_docs[h]['rounds'][0])
            controls[str(h)], baseline_final_edges[h] = no_op_control(
                binary, work, h, baseline_docs[h], expected)
        for case in NEIGHBORHOODS:
            pair = []
            for h in (23, 25):
                pair.append(evaluate_neighbor(binary, work, h, case, baseline_docs[h],
                                              baseline_mids[h], baseline_final_edges[h]))
            by_h = {row['h']: row for row in pair if row['status'] == 'screened'}
            if len(by_h) == 2:
                first_w = search.width(by_h[23]['intermediate']['R'],
                                       by_h[25]['intermediate']['R'])
                final_w = search.width(by_h[23]['final']['R'], by_h[25]['final']['R'])
                for row in pair:
                    if row['status'] == 'screened':
                        row['intermediate']['W'] = first_w
                        row['final']['W'] = final_w
                        row['final']['delta_R23'] = by_h[23]['final']['R']-expected['R23']
                        row['final']['delta_R25'] = by_h[25]['final']['R']-expected['R25']
                        row['final']['delta_W'] = final_w-expected['W']
            results.extend(pair)
        # The stale-pair and provider-capacity controls are run on the unchanged graph.
        baseline_doc = baseline_docs[23]
        mid = baseline_mids[23]
        bad = deepcopy(baseline_doc['rounds'][1])
        bad['matching_before'].append(bad['matching_before'][0][:])
        try:
            cg.replay_round(mid, bad)
        except ValueError as error:
            controls['duplicate_matching_edge'] = dict(status='rejected', reason=str(error))
        else:
            raise RuntimeError('Duplicate matching edge control unexpectedly passed')
        controls['unpaid_provider'] = {
            '23': provider_capacity_negative(baseline_mids[23], baseline_docs[23]['rounds'][1])}
        if controls['unpaid_provider']['23']['status'] != 'rejected':
            raise RuntimeError('Unpaid-provider control did not reach the capacity rejection')
        controls['no_op_W'] = search.width(controls['23']['final']['R'],
                                           controls['25']['final']['R'])
    candidates = []
    for case in NEIGHBORHOODS:
        pair = [row for row in results if row['case'] == case['id']]
        by_h = {row['h']: row for row in pair if row['status'] == 'screened'}
        if len(by_h) == 2:
            candidates.append(dict(case=case['id'], first_round_change_count=case['count'],
                                  second_round_rule=case['rule'], status='complete',
                                  intermediate_W=by_h[23]['intermediate']['W'],
                                  final_W=by_h[23]['final']['W'],
                                  delta_W=by_h[23]['final']['delta_W'],
                                  dimensions={str(h): by_h[h] for h in (23,25)}))
        else:
            candidates.append(dict(case=case['id'], first_round_change_count=case['count'],
                                  second_round_rule=case['rule'], status='incomplete',
                                  dimensions={str(row['h']): row for row in pair}))
    complete = [row for row in candidates if row['status'] == 'complete']
    best = min(complete, key=lambda row: (row['final_W'], row['case'])) if complete else None
    if best:
        best['delta_R23'] = best['dimensions']['23']['final']['delta_R23']
        best['delta_R25'] = best['dimensions']['25']['final']['delta_R25']
    improved = best is not None and best['final_W'] < expected['W']
    input_hashes = dict(previous_screening=digest(HERE/'screening.json'),
                        previous_fast=digest(HERE/'round-2-fast.json'),
                        baseline_manifest=digest(HERE/'baseline-SOURCE.json'),
                        baseline_jobs={str(h): digest(HERE/f'baseline-clone-jobs-{h}.json')
                                       for h in (23,25)},
                        source_files=pins['source_files'])
    input_sha256 = sha256(json.dumps(input_hashes, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    report = dict(schema_version=1, issue=6, round='two-round-coupled-local-search',
                  pinned_pr53_commit=previous['pinned_producer_commit'],
                  pinned_pr54_commit=previous['pinned_pr54_commit'],
                  deterministic_seed='issue6-coupled-v1', candidate_order=[x['id'] for x in NEIGHBORHOODS],
                  dimension_order=[23,25], job_order='baseline JSON order', input_sha256=input_sha256,
                  baseline=dict(R23=expected['R23'], R25=expected['R25'], W=expected['W'],
                                kappa=expected['kappa']),
                  controls=controls, candidate_count=len(candidates), candidates=candidates,
                  candidate_rows=results, best=best, focused=False, full=False,
                  method='Four deterministic 1-3-job first-round neighborhoods. Rebuild intermediate '
                         'provider-pair choices from each mapped source partition, reserve their distinct '
                         'capacities, rebuild maximum carrier matching and regenerate complete chains, then '
                         'screen final maximum matching.',
                  matching_policy='Exact maximum-cardinality matching on admissible carriers after '
                                  'excluding the distinct provider gates reserved by the rebuilt second round.',
                  screen_source_sha256=compiled_source_hash,
                  source_sha256=dict(script=digest(Path(__file__).resolve()), **input_hashes),
                  environment=previous_fast['environment'],
                  elapsed_seconds=round(time.monotonic()-started, 3),
                  conclusion=('Final FAST improvement found; FOCUSED replay required.' if improved else
                              'No final FAST improvement among complete candidates; incomplete candidates are not scored.'))
    target = HERE/'round-3-coupled.json'
    target.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(f"wrote {target}; complete={len(complete)}/{len(candidates)}; "
          f"best W={best['final_W'] if best else 'unavailable'}; baseline W={expected['W']}", flush=True)


if __name__ == '__main__':
    run()
