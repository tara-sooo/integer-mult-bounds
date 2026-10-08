#!/usr/bin/env python3
"""One bounded h=23 PR 63 compile with trace-only observations."""
from __future__ import annotations

import copy
import gzip
import hashlib
import importlib.util
import io
import json
import resource
import sys
import time
from datetime import datetime, timezone
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
PINNED = HERE / 'pinned'
PR63 = 'aa7701b68540b7863d3b66a414e4319915d6282d'
ISSUE17 = '8d4fb37796f9eb2badeca1ef0dd1c810ae23245c'
AXIS = 23
USE = dict(producer=2039, consumer=2044, operand=0)
EXPECTED_WORD = '640696dd7cd893add9d6e12d0d587956fecf113b2eff8c29547b82e5a6f3c0ad'
EXPECTED_GZIP = '1a57c143380a063211653f1f35e7cc9710539523b0b34c90f354a0425c34bd59'
COMPILER_SOURCE = '9984aaccf880e4840402322d76678bfddb33ce7e494af78430a43429f51b85fd'
INSTRUMENTED_COMPILER = '6581da72be6f53246d1989c75ec36ca90960ebd6cbb3b4b1427a6343486fea53'
GRAPH_SOURCE = '3d47e89d2649c90800a276bdd0480131def50e0bdf92c122a19494b55bf17420'
MIN_AVAILABLE_KIB = 2621440


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_word(word: dict) -> bytes:
    return (json.dumps(word, separators=(',', ':')) + '\n').encode()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def verify_pins() -> tuple[dict, dict, bytes]:
    manifest = json.loads((PINNED / 'SOURCE_MANIFEST.json').read_text())
    assert manifest['source_commit'] == PR63
    for name, digest in manifest['files'].items():
        path = PINNED / name
        if name == 'scripts/experiments/rank_pair_compiler.py':
            path = path.with_name(path.name + '.original')
        assert sha(path.read_bytes()) == digest, f'pinned source drift: {name}'
    assert manifest['files']['scripts/experiments/rank_pair_compiler.py'] == COMPILER_SOURCE
    assert manifest['files']['research/pair-assembly/pair_graph.py'] == GRAPH_SOURCE
    compiler_path = PINNED / 'scripts/experiments/rank_pair_compiler.py'
    assert sha(compiler_path.with_name(compiler_path.name + '.original').read_bytes()) == COMPILER_SOURCE
    assert sha(compiler_path.read_bytes()) == INSTRUMENTED_COMPILER
    receipt = json.loads((PINNED / 'research/rank-pair/frame-compiler.json').read_text())
    expected = receipt['axes'][str(AXIS)]
    frozen_gzip = (PINNED / f'research/rank-pair/frame-word-{AXIS}.json.gz').read_bytes()
    assert sha(frozen_gzip) == EXPECTED_GZIP == expected['gzip_sha256']
    frozen_raw = gzip.decompress(frozen_gzip)
    frozen_word = json.loads(frozen_raw)
    frozen_canonical = canonical_word(frozen_word)
    assert frozen_canonical == frozen_raw
    assert sha(frozen_canonical) == EXPECTED_WORD == expected['word_sha256']
    return manifest, expected, frozen_canonical


def projector(h: int, frame: tuple[int, int]):
    """Exact projector formula from the pinned PR 63 pair-assembly audit."""
    core_bits, cover_bits = frame
    core = {i for i in range(h) if core_bits >> i & 1}
    outside = {i for i in range(h) if (cover_bits & ~core_bits) >> i & 1}
    c, n = len(core), len(outside)
    if c == 3 and cover_bits == core_bits:
        p = [Q(3 + int(i in core)) for i in range(h)]
        q = [Q(int(i in core), 2) - Q(5, 3 * (h + 1)) for i in range(h)]
        return [[p[i] * q[j] for j in range(h)] for i in range(h)]
    if c not in (1, 2):
        return None
    s = 3 - c
    d = s * s + (c - 1) * n
    w = [3 + int(i in core) for i in range(h)]
    z = [3 * (h + 1) * int(i in core) - 10 for i in range(h)]
    o = [int(i in outside) for i in range(h)]
    return [[Q(int(i == j and i in outside)) + Q(
        s * o[i] * z[j] + 3 * (h + 1) * s * w[i] * o[j] + n * w[i] * z[j]
        - 3 * (h + 1) * (c - 1) * o[i] * o[j], 3 * (h + 1) * d)
        for j in range(h)] for i in range(h)]


def rational_rank(rows: list[list[Q]]) -> int:
    a = [row[:] for row in rows]
    rank = 0
    for col in range(len(a[0]) if a else 0):
        pivot = next((r for r in range(rank, len(a)) if a[r][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = a[rank][col]
        a[rank] = [x / scale for x in a[rank]]
        for r in range(len(a)):
            if r != rank and a[r][col]:
                factor = a[r][col]
                a[r] = [x - factor * y for x, y in zip(a[r], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank


def frame_dim(frame: tuple[int, int]) -> int:
    core, cover = frame
    if core == cover and core.bit_count() == 3:
        return 1
    return (cover & ~core).bit_count()


@lru_cache(maxsize=None)
def frame_edge_rank(h: int, old: tuple[int, int], new: tuple[int, int]) -> int | None:
    a, b = projector(h, old), projector(h, new)
    if a is None or b is None:
        return None
    rank = rational_rank([[b[i][j] - a[i][j] for j in range(h)] for i in range(h)])
    # The compiler's containment check supplies nesting; PR 63's common-metric
    # projectors then make the dimension difference the exact edge rank.
    assert not (new[0] & ~old[0]) and not (old[1] & ~new[1])
    assert rank == frame_dim(new) - frame_dim(old)
    return rank


def backward_cone(group: dict, output_slot: int | None) -> tuple[list[int], int | None]:
    if output_slot is None:
        return [], None
    live = 1 << output_slot
    relevant = []
    for record in reversed(group['timeline']):
        kind = record['record_kind']
        if kind == 'op':
            target, control, _ = record['op']
            if live >> target & 1:
                relevant.append(record['op_index'])
                live ^= 1 << control
        elif kind == 'acquire':
            live &= ~(1 << record['slot'])
        elif kind == 'event' and record['cause'] == 'slot_allocation':
            live &= ~(1 << record['event'][0])
    return sorted(relevant), live


def bit_positions(mask: int) -> list[int]:
    positions = []
    while mask:
        bit = mask & -mask
        positions.append(bit.bit_length() - 1)
        mask ^= bit
    return positions


def build_trace(raw_trace: dict, compiled: dict, word: dict, raw_hash: str,
                gzip_hash: str, expected: dict, manifest: dict, runtime: float,
                peak_kib: int) -> dict:
    source_group = raw_trace['producer_group']
    consumer_group = raw_trace['consumer_group']
    groups = raw_trace['groups']
    use_slot = raw_trace['source_use_slot']
    target_slot = raw_trace['target_value_slot']
    source_value_slot = raw_trace['source_value_slot']
    input_slot = raw_trace['consumer_input_slot']
    source_ops, source_live = backward_cone(groups[source_group], use_slot if use_slot is not None else source_value_slot)
    target_ops, target_live = backward_cone(groups[consumer_group], target_slot) if target_slot is not None else (None, None)
    related_slots = {s for s in (source_value_slot, use_slot, input_slot, target_slot) if s is not None}
    for op_index in set(source_ops) | set(target_ops or []):
        related_slots.update(word['ops'][op_index][:2])
    input_coefficients = []
    consumer_inputs = groups[consumer_group]['input_slots']
    for row in consumer_inputs:
        input_coefficients.append(dict(input_index=row['input_index'], value=row['value'], slot=row['slot'],
                                       coefficient=bool(raw_trace['consumer_input_coefficient_mask'] >> row['input_index'] & 1),
                                       present_in_target_cone=(bool(target_live >> row['slot'] & 1) if target_live is not None else None)))
    if target_live is not None:
        assert all(x['coefficient'] == x['present_in_target_cone'] for x in input_coefficients)
    cross_block = source_group != consumer_group
    if cross_block:
        assert use_slot == input_slot
    source_reaches_target = bool(target_live >> input_slot & 1) if input_slot is not None and target_live is not None else None
    groups_out = {}
    operations_out = []
    events_out = []
    event_relations = {}
    for gid in sorted(groups):
        row = groups[gid]
        frame = tuple(row['frame'])
        expected_ops = [i for i, op in enumerate(word['ops']) if op[2] == gid]
        expected_events = [i for i, event in enumerate(word['events']) if event[2] == gid]
        assert [x['op_index'] for x in row['operations']] == expected_ops
        assert [x['event_index'] for x in row['events']] == expected_events
        groups_out[str(gid)] = dict(frame=dict(core_mask=frame[0], cover_mask=frame[1]), rank=row['rank'],
                                    logical_nodes=row['nodes'], input_slots=row['input_slots'],
                                    value_slots=row['value_slots'], operation_indices=expected_ops,
                                    event_indices=expected_events, emission_timeline=row['timeline'])
        for record in row['operations']:
            op_index = record['op_index']
            exact = tuple(word['ops'][op_index])
            assert exact == tuple(record['op'])
            relations = (['producer_value_to_selected_use'] if gid == source_group and op_index in source_ops else []) + (
                ['selected_input_to_Y2'] if gid == consumer_group and target_ops is not None and op_index in target_ops else [])
            if record['cause'].startswith('retired_slot_clear') and exact[0] in related_slots:
                relations.append('slot_initialization_for_related_value')
            operations_out.append(dict(word_sha256=raw_hash, axis=AXIS, collection='ops', index=op_index,
                                       operation=list(exact), cause=record['cause'],
                                       trace_relation=relations or ['block_group_context_only'],
                                       frame_group=exact[2], raise_event_indices=list(record['event_indices'])))
            for event_index in record['event_indices']:
                event_relations[event_index] = operations_out[-1]['trace_relation']
        for record in row['events']:
            event_index = record['event_index']
            exact = tuple(word['events'][event_index])
            assert exact == tuple(record['event'])
            slot, old, new = exact
            if old < 0:
                rank23 = rank575 = None
                transition = 'ALLOCATION_WITHOUT_OLD_FRAME'
            elif old == new:
                rank23 = rank575 = 0
                transition = 'SAME_FRAME_NO_TRANSITION'
            else:
                old_frame = tuple(word['frames'][old])
                new_frame = tuple(word['frames'][new])
                rank23 = frame_edge_rank(AXIS, old_frame, new_frame)
                rank575 = rank23
                transition = 'NESTED_RATIONAL_FRAME_EDGE'
            relation = list(event_relations.get(event_index, []))
            if record['cause'] == 'block_input' and slot == input_slot:
                relation.append('selected_use_consumer_input_raise')
            if slot in (source_value_slot, use_slot, target_slot):
                relation.append('selected_value_or_carrier_slot')
            events_out.append(dict(word_sha256=raw_hash, axis=AXIS, collection='events', index=event_index,
                                   event=list(exact), cause=record['cause'], slot=slot,
                                   old_group=old, new_group=new,
                                   old_frame=(dict(core_mask=old_frame[0], cover_mask=old_frame[1]) if old >= 0 else None),
                                   new_frame=dict(core_mask=word['frames'][new][0], cover_mask=word['frames'][new][1]),
                                   transition=transition, trace_relation=relation or ['block_group_context_only'],
                                   rank_Q_23_factor=rank23,
                                   rank_Q_575_per_h25_triple_context=rank575,
                                   h25_triple_context='uniform over all 2300 source triple lines' if rank575 is not None else 'UNRESOLVED',
                                   section4_child='UNRESOLVED'))
    classification = ('REAL_PINNED_TRACE_CONFIRMED' if target_slot is not None and cross_block and raw_trace['compiler_use'] is not None
                      and use_slot == input_slot and source_reaches_target else 'PINNED_WORD_BUT_TRACE_AMBIGUOUS')
    relation = 'BLOCK_SYNTHESIS_CONES' if classification == 'REAL_PINNED_TRACE_CONFIRMED' else 'BLOCK_COALESCED_OR_UNRESOLVED'
    trace = dict(status=classification,
                 source=dict(pr63_commit=PR63, graph_sha256=manifest['files']['research/pair-assembly/pair_graph.py'],
                             frozen_compiler_sha256=COMPILER_SOURCE,
                             instrumented_compiler_sha256=sha((PINNED / 'scripts/experiments/rank_pair_compiler.py').read_bytes()),
                             global_frame_contract_commit=ISSUE17,
                             h25_triple_contexts=2300,
                             h23_product_frame='P_T(25) tensor P_hat_group(23)',
                             axis=AXIS, word_sha256=raw_hash, word_gzip_sha256=gzip_hash,
                             frozen_word_sha256=expected['word_sha256'], frozen_word_gzip_sha256=expected['gzip_sha256']),
                 logical_use=dict(stable_id=f'graph:h{AXIS}:producer{USE["producer"]}:consumer{USE["consumer"]}:operand{USE["operand"]}',
                                  producer_node=USE['producer'], consumer_node=USE['consumer'], operand=USE['operand'],
                                  coalesced_occurrences=raw_trace['coalesced_occurrences'],
                                  compiler_use_index=raw_trace['compiler_use']),
                 blocks=dict(producer_group=source_group, consumer_group=consumer_group,
                             producer_frame_group=raw_trace['source_value_frame_group'],
                             selected_use_frame_group=raw_trace['source_use_frame_group'],
                             consumer_input_frame_group=consumer_group,
                             target_frame_group=raw_trace['target_value_frame_group']),
                 carriers=dict(matched=raw_trace['matched'], match_edge_index=raw_trace['match_edge'],
                               match_input_index=raw_trace.get('match_input_index'),
                               source_value_slot=source_value_slot, selected_use_slot=use_slot,
                               consumer_input_slot=input_slot, target_value_slot=target_slot,
                               source_use_equals_consumer_input=(use_slot == input_slot if cross_block else None),
                               target_outgoing_uses=raw_trace['target_outgoing_uses']),
                 correspondence=dict(cardinality=relation, one_to_one_assumed=False,
                                     operation_relation='exact producer and consumer backward cones; shared block operations remain shared',
                                     source_to_target_input_coefficient=raw_trace['consumer_input_coefficient'],
                                     source_slot_in_Y2_emission_cone=source_reaches_target,
                                     producer_input_slot_support=(bit_positions(source_live) if source_live is not None else None),
                                     producer_to_use_op_indices=source_ops, consumer_to_Y2_op_indices=target_ops,
                                     consumer_input_coefficients=input_coefficients),
                 groups=groups_out, operations=operations_out, events=events_out,
                 execution=dict(operation_indices='compiler ops[] and events[] entries in the frozen serialized word',
                                orientation='NOT_ENCODED_BY_ARRAY_ENTRY',
                                full_forward_or_reverse_word_replay='NOT_RUN'),
                 resources=dict(runtime_seconds=runtime, peak_rss_kib=peak_kib,
                                full_word_replay='NOT_RUN', h25='NOT_RUN', full_compile='NOT_RUN'))
    return trace


def validate_trace(trace: dict, word: dict, expected_word: str, expected_gzip: str) -> None:
    assert trace['source']['word_sha256'] == expected_word
    assert trace['source']['word_gzip_sha256'] == expected_gzip
    assert trace['source']['frozen_compiler_sha256'] == COMPILER_SOURCE
    assert trace['source']['graph_sha256'] == GRAPH_SOURCE
    assert trace['logical_use']['producer_node'] == USE['producer']
    assert trace['logical_use']['consumer_node'] == USE['consumer']
    assert trace['logical_use']['operand'] == USE['operand']
    assert not trace['correspondence']['one_to_one_assumed']
    assert trace['correspondence']['cardinality'] != 'ONE_TO_ONE'
    assert trace['execution']['orientation'] == 'NOT_ENCODED_BY_ARRAY_ENTRY'
    assert trace['execution']['full_forward_or_reverse_word_replay'] == 'NOT_RUN'
    if trace['carriers']['target_value_slot'] is None:
        assert trace['correspondence']['consumer_to_Y2_op_indices'] is None
        assert trace['correspondence']['source_slot_in_Y2_emission_cone'] is None
    assert trace['carriers']['matched'] == (trace['carriers']['match_edge_index'] is not None)
    for gid, group in trace['groups'].items():
        g = int(gid)
        assert group['operation_indices'] == [i for i, op in enumerate(word['ops']) if op[2] == g]
        assert group['event_indices'] == [i for i, event in enumerate(word['events']) if event[2] == g]
        timeline = group['emission_timeline']
        assert [entry['sequence'] for entry in timeline] == list(range(len(timeline)))
        assert [entry['op_index'] for entry in timeline if entry['record_kind'] == 'op'] == group['operation_indices']
        assert [entry['event_index'] for entry in timeline if entry['record_kind'] == 'event'] == group['event_indices']
    expected_op_indices = sorted(i for group in trace['groups'].values() for i in group['operation_indices'])
    expected_event_indices = sorted(i for group in trace['groups'].values() for i in group['event_indices'])
    assert sorted(op['index'] for op in trace['operations']) == expected_op_indices
    assert sorted(event['index'] for event in trace['events']) == expected_event_indices
    event_map = {event['index']: tuple(event['event']) for event in trace['events']}
    for op in trace['operations']:
        idx = op['index']
        assert tuple(op['operation']) == tuple(word['ops'][idx])
        assert op['frame_group'] == word['ops'][idx][2]
        assert len(op['raise_event_indices']) == 2
        for event_index in op['raise_event_indices']:
            assert event_map[event_index] == tuple(word['events'][event_index])
    for event in trace['events']:
        assert tuple(event['event']) == tuple(word['events'][event['index']])
        if event.get('rank_Q_23_factor') is not None:
            if event['event'][1] == event['event'][2]:
                assert event['rank_Q_23_factor'] == event['rank_Q_575_per_h25_triple_context'] == 0
            elif event.get('old_frame') is not None:
                assert event['rank_Q_23_factor'] == frame_edge_rank(AXIS,
                    (event['old_frame']['core_mask'], event['old_frame']['cover_mask']),
                    (event['new_frame']['core_mask'], event['new_frame']['cover_mask']))
                assert event['rank_Q_575_per_h25_triple_context'] == event['rank_Q_23_factor']
    if trace['blocks']['producer_group'] != trace['blocks']['consumer_group']:
        assert trace['carriers']['selected_use_slot'] == trace['carriers']['consumer_input_slot']
    if trace.get('status') == 'REAL_PINNED_TRACE_CONFIRMED':
        assert trace['carriers']['target_value_slot'] is not None
        assert trace.get('hash_verification', {}).get('canonical_json_matches_frozen')
        assert trace['correspondence']['cardinality'] == 'BLOCK_SYNTHESIS_CONES'
        assert trace['correspondence']['source_slot_in_Y2_emission_cone']
    assert trace['resources']['full_word_replay'] == 'NOT_RUN'


def run_negative_controls(trace: dict, word: dict, expected_word: str, expected_gzip: str) -> list[str]:
    cases = []
    def rejected(name, mutate):
        broken = copy.deepcopy(trace)
        mutate(broken)
        try:
            validate_trace(broken, word, expected_word, expected_gzip)
        except (AssertionError, IndexError, KeyError, StopIteration, TypeError):
            cases.append(name)
        else:
            raise AssertionError(f'negative control was accepted: {name}')
    rejected('wrong producer/use operand identity', lambda x: x['logical_use'].__setitem__('operand', 1))
    if trace['blocks']['producer_group'] != trace['blocks']['consumer_group']:
        rejected('swapped physical slots', lambda x: x['carriers'].__setitem__('consumer_input_slot', x['carriers']['consumer_input_slot'] + 1))
    rejected('wrong compiler op index', lambda x: x['operations'][0].__setitem__('index', len(word['ops'])))
    rejected('wrong op frame group', lambda x: x['operations'][0].__setitem__('frame_group', x['operations'][0]['frame_group'] + 1))
    def omit_copy_or_clear(x):
        i = next((i for i, op in enumerate(x['operations']) if 'copy' in op.get('cause', '') or 'clear' in op.get('cause', '')), 0)
        x['operations'].pop(i)
    rejected('omitted copy/clear operation record', omit_copy_or_clear)
    rejected('omitted frame-raise event', lambda x: x['events'].pop())
    rejected('stale matching decision', lambda x: x['carriers'].__setitem__('matched', not x['carriers']['matched']))
    rejected('stale pinned compiler hash', lambda x: x['source'].__setitem__('frozen_compiler_sha256', '0' * 64))
    rejected('wrong frame-event group', lambda x: x['events'][0]['event'].__setitem__(2, x['events'][0]['event'][2] + 1))
    def swap_timeline(x):
        timeline = next(group['emission_timeline'] for group in x['groups'].values() if group['emission_timeline'])
        if len(timeline) > 1:
            timeline[0], timeline[1] = timeline[1], timeline[0]
        else:
            timeline[0]['sequence'] += 1
    rejected('swapped emission timeline', swap_timeline)
    rejected('stale frozen word hash', lambda x: x['source'].__setitem__('word_sha256', '0' * 64))
    rejected('invented execution orientation', lambda x: x['execution'].__setitem__('orientation', 'REVERSE_COMPLEMENT'))
    rejected('forced one-XOR bijection', lambda x: x['correspondence'].__setitem__('one_to_one_assumed', True))
    return cases


def self_check() -> None:
    source_frame = (0b111, 0b111)
    expanded_frame = (0b001, (1 << AXIS) - 1)
    assert rational_rank(projector(AXIS, source_frame)) == 1
    assert frame_edge_rank(AXIS, source_frame, expanded_frame) == AXIS - 2
    cone, inputs = backward_cone(dict(timeline=[
        dict(record_kind='op', op_index=0, op=(3, 1, 7)),
        dict(record_kind='acquire', slot=3),
        dict(record_kind='acquire', slot=4),
        dict(record_kind='op', op_index=1, op=(4, 3, 7))]), 4)
    assert cone == [1] and inputs == 0
    assert backward_cone(dict(timeline=[]), None) == ([], None)
    word = dict(ops=[[3, 1, 7], [4, 3, 7], [5, 4, 7]],
                events=[[3, 6, 7], [1, 6, 7], [4, 6, 7], [3, 6, 7], [5, 6, 7], [4, 6, 7]])
    digest = sha(canonical_word(word))
    trace = dict(source=dict(word_sha256=digest, word_gzip_sha256='fixture-gzip',
                             frozen_compiler_sha256=COMPILER_SOURCE, graph_sha256=GRAPH_SOURCE),
                 logical_use=dict(producer_node=2039, consumer_node=2044, operand=0),
                 correspondence=dict(cardinality='BLOCK_SYNTHESIS_CONES', one_to_one_assumed=False),
                 execution=dict(orientation='NOT_ENCODED_BY_ARRAY_ENTRY', full_forward_or_reverse_word_replay='NOT_RUN'),
                 groups={'7':dict(operation_indices=[0, 1, 2], event_indices=[0, 1, 2, 3, 4, 5],
                                  emission_timeline=[dict(sequence=0, record_kind='event', event_index=0),
                                                     dict(sequence=1, record_kind='event', event_index=1),
                                                     dict(sequence=2, record_kind='op', op_index=0),
                                                     dict(sequence=3, record_kind='event', event_index=2),
                                                     dict(sequence=4, record_kind='event', event_index=3),
                                                     dict(sequence=5, record_kind='op', op_index=1),
                                                     dict(sequence=6, record_kind='event', event_index=4),
                                                     dict(sequence=7, record_kind='event', event_index=5),
                                                     dict(sequence=8, record_kind='op', op_index=2)])},
                 operations=[dict(index=0, operation=[3, 1, 7], frame_group=7, cause='block_synthesis', raise_event_indices=[0, 1]),
                             dict(index=1, operation=[4, 3, 7], frame_group=7, cause='duplicate_use_copy', raise_event_indices=[2, 3]),
                             dict(index=2, operation=[5, 4, 7], frame_group=7, cause='retired_slot_clear', raise_event_indices=[4, 5])],
                 events=[dict(index=0, event=[3, 6, 7]), dict(index=1, event=[1, 6, 7]),
                         dict(index=2, event=[4, 6, 7]), dict(index=3, event=[3, 6, 7]),
                         dict(index=4, event=[5, 6, 7]), dict(index=5, event=[4, 6, 7])],
                 blocks=dict(producer_group=7, consumer_group=8),
                 carriers=dict(selected_use_slot=9, consumer_input_slot=9, target_value_slot=5, matched=False, match_edge_index=None),
                 resources=dict(full_word_replay='NOT_RUN'))
    trace['correspondence'].update(source_slot_in_Y2_emission_cone=True, consumer_to_Y2_op_indices=[1, 2])
    validate_trace(trace, word, digest, 'fixture-gzip')
    unresolved_target = copy.deepcopy(trace)
    unresolved_target['carriers']['target_value_slot'] = None
    unresolved_target['correspondence']['source_slot_in_Y2_emission_cone'] = None
    unresolved_target['correspondence']['consumer_to_Y2_op_indices'] = None
    validate_trace(unresolved_target, word, digest, 'fixture-gzip')
    passed = run_negative_controls(trace, word, digest, 'fixture-gzip')
    assert len(passed) == 13
    print('PASS isolated fixture and exact frame-rank self-check:', ', '.join(passed))


def run_focused() -> None:
    attempt = HERE / 'FOCUSED_STARTED.json'
    receipt_path = HERE / 'FOCUSED_RECEIPT.json'
    trace_path = HERE / 'TRACE.json'
    assert not attempt.exists() and not receipt_path.exists() and not trace_path.exists(), 'refusing a second FOCUSED run'
    manifest, expected, frozen_raw = verify_pins()
    available_kib = next(int(line.split()[1]) for line in Path('/proc/meminfo').read_text().splitlines()
                         if line.startswith('MemAvailable:'))
    assert available_kib >= MIN_AVAILABLE_KIB, f'RESOURCE_GATED: only {available_kib} KiB available'
    attempt.write_text(json.dumps(dict(status='STARTED', started_utc=datetime.now(timezone.utc).isoformat(),
                                       axis=AXIS, source_commit=PR63,
                                       resource_gate=dict(pre_compile_mem_available_kib=available_kib,
                                                          minimum_available_kib=MIN_AVAILABLE_KIB,
                                                          address_space_limit='NOT_APPLIED',
                                                          wall_timeout_seconds=1800)), indent=2) + '\n')
    sys.dont_write_bytecode = True
    compiler = load_module('instrumented_rank_pair_compiler', PINNED / 'scripts/experiments/rank_pair_compiler.py')
    # Load the graph's PR 63 helper modules from its own pinned tree, separate
    # from the PR 48 producer modules already imported by the compiler copy.
    for name in ('partial_swap', 'partial_swap.paired', 'partial_swap.shared', 'exclusion_circuit'):
        sys.modules.pop(name, None)
    sys.path.insert(0, str(PINNED / 'scripts'))
    graph_module = load_module('pinned_pair_graph', PINNED / 'research/pair-assembly/pair_graph.py')
    compiler.graph = graph_module.graph
    start = time.monotonic()
    try:
        compiled, word, raw_trace = compiler.compile_(AXIS, matching=True, reclaim=True, dirty=False, trace_spec=USE)
    except BaseException as exc:
        attempt.write_text(json.dumps(dict(status='FAILED_DURING_SINGLE_FOCUSED_ATTEMPT',
                                           started_utc=json.loads(attempt.read_text())['started_utc'],
                                           error=repr(exc)), indent=2) + '\n')
        raise
    runtime = time.monotonic() - start
    peak_kib = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    raw = canonical_word(word)
    word_hash = sha(raw)
    stream = io.BytesIO()
    with gzip.GzipFile(fileobj=stream, mode='wb', mtime=0) as archive:
        archive.write(raw)
    gzip_hash = sha(stream.getvalue())
    hash_verification = dict(canonical_json_sha256=word_hash, expected_canonical_json_sha256=EXPECTED_WORD,
                             canonical_json_matches_frozen=(raw == frozen_raw and word_hash == EXPECTED_WORD),
                             deterministic_gzip_sha256=gzip_hash, expected_gzip_sha256=EXPECTED_GZIP,
                             deterministic_gzip_matches_frozen=(gzip_hash == EXPECTED_GZIP))
    (HERE / 'WORD_HASH_RECEIPT.json').write_text(json.dumps(hash_verification, indent=2) + '\n')
    stable = expected['compiled']
    for key in ('roles', 'rank_mass', 'elementary_xors', 'stats'):
        assert compiled[key] == stable[key], f'compiled receipt drift in {key}'
    assert compiled['histogram'] == {int(k): v for k, v in stable['histogram'].items()}
    trace = build_trace(raw_trace, compiled, word, word_hash, gzip_hash, expected, manifest, runtime, peak_kib)
    status = 'WORD_DRIFT' if not hash_verification['canonical_json_matches_frozen'] else trace['status']
    trace['status'] = status
    trace['hash_verification'] = hash_verification
    validate_trace(trace, word, word_hash, gzip_hash)
    negative_controls = run_negative_controls(trace, word, word_hash, gzip_hash)
    trace['negative_controls'] = dict(status='PASS', cases=negative_controls, fixture_only=False)
    trace['compiled_summary'] = dict(roles=compiled['roles'], elementary_xors=compiled['elementary_xors'],
                                     rank_mass=compiled['rank_mass'], statistics=compiled['stats'],
                                     generated_word_operations=4 * len(word['ops']) + 2 * len(word['scatter']) + 2 * len(word['sources']),
                                     generated_events=len(word['events']), dirty_basis_replay='NOT RUN')
    trace_path.write_text(json.dumps(trace, indent=2, sort_keys=True) + '\n')
    receipt_path.write_text(json.dumps(dict(status=status, started_utc=json.loads(attempt.read_text())['started_utc'],
                                            completed_utc=datetime.now(timezone.utc).isoformat(), axis=AXIS,
                                            runtime_seconds=runtime, peak_rss_kib=peak_kib,
                                            canonical_word_sha256=word_hash, gzip_sha256=gzip_hash,
                                            pinned_word_match=(raw == frozen_raw and word_hash == EXPECTED_WORD),
                                            trace_file='TRACE.json'), indent=2) + '\n')
    attempt.write_text(json.dumps(dict(status='COMPLETED', started_utc=json.loads(attempt.read_text())['started_utc'],
                                       completed_utc=datetime.now(timezone.utc).isoformat()), indent=2) + '\n')
    print(json.dumps(dict(status=status, runtime_seconds=runtime, peak_rss_kib=peak_kib,
                          canonical_word_sha256=word_hash, gzip_sha256=gzip_hash,
                          source_group=raw_trace['producer_group'], consumer_group=raw_trace['consumer_group'],
                          source_slot=raw_trace['source_use_slot'], consumer_input_slot=raw_trace['consumer_input_slot'],
                          target_slot=raw_trace['target_value_slot'], op_count=len(word['ops']), event_count=len(word['events']))), flush=True)


if __name__ == '__main__':
    if '--self-check' in sys.argv[1:]:
        self_check()
    else:
        try:
            run_focused()
        except BaseException as exc:
            marker = HERE / 'FOCUSED_STARTED.json'
            if marker.exists():
                state = json.loads(marker.read_text())
                if state['status'] == 'STARTED':
                    marker.write_text(json.dumps(dict(status='FAILED_AFTER_SINGLE_FOCUSED_ATTEMPT',
                                                       started_utc=state['started_utc'], error=repr(exc)), indent=2) + '\n')
            raise
