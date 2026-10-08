#!/usr/bin/env python3
"""Deterministic screening of alternate final-round clone chains on PR 53."""
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import shlex
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CLONES = ROOT / 'research/skip-clones'
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(CLONES))
from partial_swap.graph import export
import cloned_graph as cg

SEEDS = ('1', '2', '3', '4', '5', '6', '7', '8')
PROFILE = CLONES / 'profiles.cpp'
WEIGHTED_PROFILE = ROOT / 'references/copied-fixed/pr44/profiles.cpp'
MATCH_OPTIMIZER = ROOT / 'research/skip-strips/optimize_matching.py'
BASELINE_MANIFEST = HERE / 'baseline-SOURCE.json'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def baseline_jobs(h):
    return json.loads((HERE / f'baseline-clone-jobs-{h}.json').read_text())


def rank_times(c):
    ranks = [0] * len(c.args)
    for node in c.active:
        ranks[node] = 1 if c.args[node] is None else c.union[node].bit_count() - c.core[node].bit_count()
    order = sorted(c.active, key=lambda node: (ranks[node], node))
    return ranks, {node: i for i, node in enumerate(order)}, order


def chain_options(c, round_doc):
    _, times, order = rank_times(c)
    roots = list(c.outputs.values())
    users = [[] for _ in c.args]
    for node in order:
        if c.args[node] is not None:
            for pos, child in enumerate(c.args[node]):
                users[child].append(2 * node + pos)
    for j, root in enumerate(roots):
        users[root].append((1 << 31) | j)

    def use(edge):
        if edge >> 31:
            j = edge & 0x7fffffff
            return roots[j], roots[j], len(order) + j
        owner = edge // 2
        return c.args[owner][edge % 2], owner, times[owner]

    incoming, next_use = set(), {}
    for donor, edge in round_doc['matching_before']:
        value, _, _ = use(edge)
        pos = c.args[donor].index(value)
        next_use[2 * donor + pos] = edge
        incoming.add(edge)

    options = []
    for job in round_doc['jobs']:
        parent = job['parent']
        choices = {(job['first'], tuple(job['chain']))}
        for edge in users[parent]:
            if edge in incoming or use(edge)[0] != parent:
                continue
            _, _, first_time = use(edge)
            if any(times[provider] >= first_time for provider in job['providers']):
                continue
            moved, seen, current = [], set(), edge
            while True:
                if current in seen or use(current)[0] != parent:
                    moved = []
                    break
                seen.add(current)
                moved.append(current)
                if current not in next_use:
                    break
                current = next_use[current]
            if moved:
                choices.add((edge, tuple(moved)))
        options.append(sorted(choices))
    return options


def replay_unpinned(c, round_doc):
    original_require = cg.require
    cg.require = lambda ok, message: None if message == 'Clone output graph differs from pin' else original_require(ok, message)
    try:
        return cg.replay_round(c, round_doc)
    finally:
        cg.require = original_require


def select_chains(c, round_doc, seed, h):
    changes, selected = [], []
    for index, (job, choices) in enumerate(zip(round_doc['jobs'], chain_options(c, round_doc))):
        key = f'issue6:{seed}:{h}:{index}'.encode()
        choice_index = int.from_bytes(sha256(key).digest()[:8], 'big') % len(choices)
        first, moved = choices[choice_index]
        selected.append((first, list(moved)))
        if first != job['first'] or list(moved) != job['chain']:
            changes.append(dict(job=index, parent=job['parent'], old_first=job['first'],
                                old_chain=job['chain'], first=first, chain=list(moved)))
    for job, (first, moved) in zip(round_doc['jobs'], selected):
        job['first'], job['chain'] = first, moved
    return selected, changes


def candidate_document(h, seed):
    doc = baseline_jobs(h)
    c = cg.base_graph(h)
    for round_doc in doc['rounds'][:-1]:
        c = cg.replay_round(c, round_doc)
    rd = doc['rounds'][-1]
    selected, changes = select_chains(c, rd, seed, h)
    candidate = replay_unpinned(c, rd)
    rd['output_graph_sha256'] = cg.digest(candidate)
    candidate.verify()
    choice_hash = sha256(json.dumps(selected, separators=(',', ':')).encode()).hexdigest()
    return doc, candidate, changes, choice_hash


def screen(binary, c, work, h, label):
    dag = work / f'{label}-{h}.bin'
    export(c, dag)
    env = dict(os.environ)
    env.pop('LINKS_IN', None)
    env.pop('DUMP_EDGES', None)
    proc = subprocess.Popen([str(binary), str(dag)], stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, text=True, env=env)
    try:
        line = proc.stdout.readline()
        if not line:
            raise RuntimeError(f'Profiler produced no matching summary for h={h}, {label}')
        row = json.loads(line)
    finally:
        proc.terminate()
        proc.wait()
        proc.stdout.close()
    return row


def compile_screen(work):
    source = PROFILE.read_text()
    guard = 'assert(lin && "A pinned carrier matching is required");'
    if guard not in source:
        raise RuntimeError('Pinned profiler matching guard changed')
    screen_source = work / 'profiles-screen.cpp'
    screen_source.write_text(source.replace(guard, '// Screening uses the built-in maximum-cardinality matcher.'))
    binary = work / 'profiles-screen'
    command = [*shlex.split(os.environ.get('CXX', 'c++')), '-O3', '-std=c++17', '-include', 'algorithm',
               '-I', str(ROOT / 'scripts/partial_swap'), str(screen_source), '-o', str(binary)]
    subprocess.run(command, check=True)
    return binary, digest(screen_source)


def compile_edge_dump(work):
    binary = work / 'profiles-dump'
    command = [*shlex.split(os.environ.get('CXX', 'c++')), '-O3', '-std=c++17', '-include', 'algorithm',
               '-I', str(ROOT / 'scripts/partial_swap'), str(WEIGHTED_PROFILE), '-o', str(binary)]
    subprocess.run(command, check=True)
    return binary


def regenerate_matching(binary, c, work, h):
    dag, edges = work / f'weighted-{h}.bin', work / f'weighted-edges-{h}.txt'
    export(c, dag)
    env = dict(os.environ, DUMP_EDGES=str(edges))
    env.pop('LINKS_IN', None)
    subprocess.run([str(binary), str(dag)], env=env, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    spec_name = f'issue6_matching_optimizer_{h}'
    import importlib.util
    spec = importlib.util.spec_from_file_location(spec_name, MATCH_OPTIMIZER)
    optimizer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(optimizer)
    selected = optimizer.solve(edges, h)
    import struct
    out = CLONES / f'links-{h}.uses'
    out.write_bytes(struct.pack('<2I', len(c.args), len(selected)) +
                     b''.join(struct.pack('<2I', donor, use) for donor, use in selected))
    return dict(matched=len(selected), edges_sha256=digest(edges), links_sha256=digest(out))


def width(r23, r25):
    from math import comb
    n = comb(23, 3) * comb(25, 3)
    return 2 * n + (n // comb(23, 3)) * r23 + (n // comb(25, 3)) * r25


def run():
    source = json.loads(BASELINE_MANIFEST.read_text())
    expected = source['files']
    pinned_code = ('research/skip-clones/cloned_graph.py', 'research/skip-clones/clone_io.py',
                   'research/skip-clones/profiles.cpp', 'research/skip-strips/skip_graph.py',
                   'scripts/partial_swap/graph.py', 'scripts/partial_swap/binary_io.hpp',
                   'references/copied-fixed/pr44/profiles.cpp', 'research/skip-strips/optimize_matching.py')
    for name in pinned_code:
        if digest(ROOT / name) != expected[name]:
            raise RuntimeError(f'Pinned search source changed: {name}')
    for h in (23, 25):
        name = f'research/skip-clones/clone-jobs-{h}.json'
        if digest(HERE / f'baseline-clone-jobs-{h}.json') != expected[name]:
            raise RuntimeError(f'Baseline clone schedule changed: h={h}')
        name = f'research/skip-clones/original-{h}.json'
        if digest(HERE / f'baseline-original-{h}.json') != expected[name]:
            raise RuntimeError(f'Baseline role record changed: h={h}')
    if digest(HERE / 'baseline-parameters.json') != expected['research/skip-clones/parameters.json']:
        raise RuntimeError('Baseline exact parameters changed')
    baseline = dict(source_manifest_sha256=digest(BASELINE_MANIFEST),
                    source_files={name: expected[name] for name in pinned_code},
                    clone_jobs={str(h): digest(HERE / f'baseline-clone-jobs-{h}.json') for h in (23, 25)},
                    links={str(h): expected[f'research/skip-clones/links-{h}.uses'] for h in (23, 25)},
                    role_records={str(h): digest(HERE / f'baseline-original-{h}.json') for h in (23, 25)},
                    parameters=digest(HERE / 'baseline-parameters.json'),
                    search_script=digest(Path(__file__).resolve()))
    report = dict(schema_version=1, pinned_producer_commit='3ffd4021995c959ac02d12920e0279ae97dd03c7',
                  pinned_pr54_commit='7210de7d0f9ccaeb64c3f60f188419e02be08d95',
                  method='Choose a deterministic SHA-256-indexed final-round continuation chain for each clone; '
                         'replay every invariant, then screen exact maximum matching cardinality. '
                         'Matching and profile scores are discovery only.',
                  seeds=list(SEEDS), source_sha256=baseline,
                  environment=dict(python=platform.python_version(), platform=platform.platform()), candidates=[])
    with tempfile.TemporaryDirectory(prefix='issue6-clone-search-') as directory:
        work = Path(directory)
        binary, screen_source_hash = compile_screen(work)
        report['screen_profiler_sha256'] = screen_source_hash
        base_rows = {}
        for h in (23, 25):
            base = cg.base_graph(h)
            for rd in baseline_jobs(h)['rounds']:
                base = cg.replay_round(base, rd)
            row = screen(binary, base, work, h, 'baseline')
            saved = json.loads((HERE / f'baseline-original-{h}.json').read_text())
            if row['R'] != saved['R']:
                raise RuntimeError(f'Maximum matching screen disagrees with pinned R{h}')
            base_rows[h] = row
        base_w = width(base_rows[23]['R'], base_rows[25]['R'])
        report['baseline'] = dict(R23=base_rows[23]['R'], R25=base_rows[25]['R'], W=base_w,
                                  kappa=json.loads((HERE / 'baseline-parameters.json').read_text())['kappa'])
        for seed in SEEDS:
            rows, changes, graph_hashes, schedule_hashes = {}, {}, {}, {}
            for h in (23, 25):
                doc, c, edits, choice_hash = candidate_document(h, seed)
                row = screen(binary, c, work, h, f'seed-{seed}')
                rows[h], changes[h], graph_hashes[h], schedule_hashes[h] = row, edits, cg.digest(c), choice_hash
            item = dict(seed=seed, R23=rows[23]['R'], R25=rows[25]['R'],
                        W=width(rows[23]['R'], rows[25]['R']),
                        schedule_sha256=sha256((schedule_hashes[23] + schedule_hashes[25]).encode()).hexdigest(),
                        graph_sha256=graph_hashes,
                        changed_chains={str(h): changes[h] for h in (23, 25)})
            report['candidates'].append(item)
            print(f"seed={seed} R23={item['R23']} R25={item['R25']} W={item['W']} "
                  f"changed={len(changes[23])}+{len(changes[25])}", flush=True)
        best = min(report['candidates'], key=lambda row: (row['W'], row['seed']))
        report['best_screened_seed'] = best['seed']
        report['best_screened_improves_W'] = best['W'] < base_w
        report['selection_rule'] = 'Minimum W, then lexicographically smallest seed; exact full replay is required before any claim.'
        dump_binary = compile_edge_dump(work)
        matching = {}
        for h in (23, 25):
            doc, c, _, _ = candidate_document(h, best['seed'])
            (CLONES / f'clone-jobs-{h}.json').write_text(json.dumps(doc, indent=2) + '\n')
            match = regenerate_matching(dump_binary, c, work, h)
            if match['matched'] != base_rows[h]['matched']:
                raise RuntimeError(f'Weighted matching cardinality differs from screened maximum: h={h}')
            matching[str(h)] = match
        report['selected_matching'] = matching
    target = HERE / 'screening.json'
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(f"best seed={best['seed']} W={best['W']} baseline W={base_w}; wrote {target}")


if __name__ == '__main__':
    run()
