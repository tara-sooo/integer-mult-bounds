#!/usr/bin/env python3
"""FAST-only follow-up for first-round and final-round paid-clone choices."""
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('issue6_search', HERE/'search.py')
search = importlib.util.module_from_spec(spec)
spec.loader.exec_module(search)
cg = search.cg

FIRST_SEEDS = ('101', '102')
FINAL_SEEDS = ('9', '10')


def select(document, circuit, round_index, strategy, seed=None):
    round_doc = document['rounds'][round_index]
    choices = search.chain_options(circuit, round_doc)
    changes = 0
    for index, (job, options) in enumerate(zip(round_doc['jobs'], choices)):
        if strategy == 'shortest-chain':
            first, chain = min(options, key=lambda item: (len(item[1]), item[1], item[0]))
        else:
            key = f'issue6:round2:{round_index}:{seed}:{circuit.h}:{index}'.encode()
            choice_index = int.from_bytes(sha256(key).digest()[:8], 'big') % len(options)
            first, chain = options[choice_index]
        if first != job['first'] or list(chain) != job['chain']:
            changes += 1
        job['first'], job['chain'] = first, list(chain)
    return changes, [len(row) for row in choices]


def first_round_candidate(h, strategy, seed=None):
    document = search.baseline_jobs(h)
    circuit = cg.base_graph(h)
    round_doc = document['rounds'][0]
    changed, option_counts = select(document, circuit, 0, strategy, seed)
    # replay_round checks providers, partitions, chronology, envelopes, complete
    # continuation chains, source pins, and exact scalar outputs before profiling.
    candidate = search.replay_unpinned(circuit, round_doc)
    round_doc['output_graph_sha256'] = cg.digest(candidate)
    return candidate, changed, option_counts


def final_round_candidate(h, strategy, seed=None):
    document = search.baseline_jobs(h)
    circuit = cg.base_graph(h)
    for round_doc in document['rounds'][:-1]:
        circuit = cg.replay_round(circuit, round_doc)
    round_doc = document['rounds'][-1]
    changed, option_counts = select(document, circuit, len(document['rounds'])-1,
                                    strategy, seed)
    candidate = search.replay_unpinned(circuit, round_doc)
    round_doc['output_graph_sha256'] = cg.digest(candidate)
    return candidate, changed, option_counts


def record(binary, work, h, round_name, strategy, seed=None):
    try:
        if round_name == 'first':
            circuit, changed, option_counts = first_round_candidate(h, strategy, seed)
            scope = 'round-1 graph only; later round schedule must be regenerated'
        else:
            circuit, changed, option_counts = final_round_candidate(h, strategy, seed)
            scope = 'complete pinned clone schedule; exact profile and kappa not rerun'
    except ValueError as error:
        return dict(round=round_name, dimension=h, strategy=strategy, seed=seed,
                    status='rejected', rejection_reason=str(error))
    row = search.screen(binary, circuit, work, h,
                        f'{round_name}-{strategy}-{seed or "none"}')
    return dict(round=round_name, dimension=h, strategy=strategy, seed=seed,
                status='screened',
                changed_chains=changed, clones=circuit.clone_count,
                choice_count_min=min(option_counts), choice_count_max=max(option_counts),
                R=row['R'], matched=row['matched'],
                rank_sum=row['rank_sum'], graph_sha256=cg.digest(circuit), scope=scope)


def run():
    previous = json.loads((HERE/'screening.json').read_text())
    baseline = previous['baseline']
    previous_seeds = set(previous['seeds'])
    if previous_seeds & (set(FIRST_SEEDS) | set(FINAL_SEEDS)):
        raise RuntimeError('Follow-up seed overlaps the previous final-round sample')
    pins = previous['source_sha256']
    if search.digest(search.BASELINE_MANIFEST) != pins['source_manifest_sha256']:
        raise RuntimeError('Baseline source manifest changed')
    for name, expected in pins['source_files'].items():
        if search.digest(ROOT/name) != expected:
            raise RuntimeError(f'Pinned source changed: {name}')
    for h in (23, 25):
        for label, path, expected in (
                ('clone jobs', HERE/f'baseline-clone-jobs-{h}.json', pins['clone_jobs'][str(h)]),
                ('original roles', HERE/f'baseline-original-{h}.json', pins['role_records'][str(h)])):
            if search.digest(path) != expected:
                raise RuntimeError(f'Pinned baseline {label} changed: h={h}')
    if search.digest(HERE/'baseline-parameters.json') != pins['parameters']:
        raise RuntimeError('Baseline exact parameters changed')
    if search.digest(HERE/'baseline-parameters.json') != pins['parameters']:
        raise RuntimeError('Baseline exact parameters changed')
    results = []
    first_baseline = {}
    with tempfile.TemporaryDirectory(prefix='issue6-round2-fast-') as directory:
        work = Path(directory)
        binary, screen_source_hash = search.compile_screen(work)
        for h in (23, 25):
            base = cg.base_graph(h)
            baseline_round1 = cg.replay_round(base, search.baseline_jobs(h)['rounds'][0])
            baseline_row = search.screen(binary, baseline_round1, work, h, 'baseline-round1')
            previous_round = dict(R=baseline_row['R'], matched=baseline_row['matched'],
                                  rank_sum=baseline_row['rank_sum'])
            previous_round['graph_sha256'] = cg.digest(baseline_round1)
            first_baseline[h] = previous_round
            for seed in FIRST_SEEDS:
                result = record(binary, work, h, 'first', 'sha256-choice', seed)
                result['compared_with_round_baseline'] = previous_round
                result['delta_R'] = result['R']-previous_round['R']
                results.append(result)
            result = record(binary, work, h, 'first', 'shortest-chain')
            result['compared_with_round_baseline'] = previous_round
            result['delta_R'] = result['R']-previous_round['R']
            results.append(result)
        for h in (23, 25):
            for seed in FINAL_SEEDS:
                result = record(binary, work, h, 'final', 'sha256-choice', seed)
                result['compared_with_final_baseline'] = dict(
                    R=baseline[f'R{h}'], W=baseline['W'])
                result['delta_R'] = result['R']-baseline[f'R{h}']
                results.append(result)
            result = record(binary, work, h, 'final', 'shortest-chain')
            result['compared_with_final_baseline'] = dict(
                R=baseline[f'R{h}'], W=baseline['W'])
            result['delta_R'] = result['R']-baseline[f'R{h}']
            results.append(result)
    for round_name, strategies in (
            ('first', [('sha256-choice', seed) for seed in FIRST_SEEDS] + [('shortest-chain', None)]),
            ('final', [('sha256-choice', seed) for seed in FINAL_SEEDS] + [('shortest-chain', None)])):
        for strategy, seed in strategies:
            pair = [row for row in results if row['round'] == round_name
                    and row['strategy'] == strategy and row['seed'] == seed
                    and row['status'] == 'screened']
            if len(pair) != 2:
                continue
            by_h = {row['dimension']: row for row in pair}
            W = search.width(by_h[23]['R'], by_h[25]['R'])
            if round_name == 'first':
                baseline_W = search.width(first_baseline[23]['R'], first_baseline[25]['R'])
            else:
                baseline_W = baseline['W']
            for row in pair:
                row['W'] = W
                row['delta_W'] = W-baseline_W
                row['compared_with_W'] = baseline_W
                if round_name == 'first':
                    row['decision'] = ('potential only; later round invalidated and not rebuilt'
                                       if W < baseline_W else
                                       'not promoted; no first-round FAST W gain')
                else:
                    row['decision'] = ('FOCUSED candidate; exact profile replay required'
                                       if W < baseline_W else
                                       'not promoted; no final-round FAST W gain')
    final_improved = any(row.get('round') == 'final' and row.get('delta_W', 0) < 0
                         for row in results)
    first_potential = any(row.get('round') == 'first' and row.get('delta_W', 0) < 0
                          for row in results)
    report = dict(schema_version=1, issue=6,
                  pinned_pr53_commit=previous['pinned_producer_commit'],
                  pinned_pr54_commit=previous['pinned_pr54_commit'],
                  baseline=dict(R23=baseline['R23'], R25=baseline['R25'],
                                W=baseline['W'], kappa=baseline['kappa']),
                  final_round_seeds=list(FINAL_SEEDS),
                  first_round_seeds=list(FIRST_SEEDS),
                  previous_final_seeds=previous['seeds'],
                  environment=previous['environment'],
                  method='First round: deterministic SHA-256 choices (seeds 101,102) and shortest complete chain; '
                         'final round: new SHA-256 seeds 9,10 and shortest complete chain. '
                         'Every screen follows strict clone replay; matching/profile values are discovery-only.',
                  screen_profiler_sha256=screen_source_hash,
                  source_sha256=dict(baseline_manifest=search.digest(search.BASELINE_MANIFEST),
                                     script=search.digest(Path(__file__).resolve()),
                                     previous_screening=search.digest(HERE/'screening.json'),
                                     source_files=pins['source_files'],
                                     baseline_clone_jobs={str(h): search.digest(
                                         HERE/f'baseline-clone-jobs-{h}.json') for h in (23, 25)},
                                     baseline_original_roles={str(h): search.digest(
                                         HERE/f'baseline-original-{h}.json') for h in (23, 25)},
                                     parameters=pins['parameters']),
                  candidates=results,
                  first_round_baseline=first_baseline,
                  rejected_candidates=[row for row in results if row['status'] == 'rejected'],
                  focused=False, full=False,
                  conclusion=('A final-round candidate improved FAST W; exact profile replay is required.'
                              if final_improved else
                              'A first-round candidate improved partial FAST W, but its later schedule needs rebuilding.'
                              if first_potential else
                              'No candidate improved its comparable FAST W screen; no exact kappa claim is made.'))
    target = HERE/'round-2-fast.json'
    target.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    for row in results:
        if row['status'] == 'rejected':
            print(f"REJECT {row['round']} h={row['dimension']} {row['strategy']} "
                  f"seed={row['seed']}: {row['rejection_reason']}", flush=True)
        else:
            print(f"{row['round']} h={row['dimension']} {row['strategy']} seed={row['seed']} "
                  f"R={row['R']} clones={row['clones']} rank_sum={row['rank_sum']} "
                  f"changed={row['changed_chains']}", flush=True)
    print(f'Wrote {target}')


if __name__ == '__main__':
    run()
