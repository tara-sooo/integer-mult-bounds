#!/usr/bin/env python3
"""One bounded h=23 PR 63 compile with trace-only observations."""
from __future__ import annotations

import copy
import gzip
import hashlib
import importlib.util
import io
import json
import os
import resource
import sys
import time
import traceback
import zlib
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
INSTRUMENTED_COMPILER = 'e2eb7063e5ca6788dd86b3c2affdc49b470efc3ba57ca89ef820e76e6843bb89'
GRAPH_SOURCE = '3d47e89d2649c90800a276bdd0480131def50e0bdf92c122a19494b55bf17420'
MIN_AVAILABLE_KIB = 2621440


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_word(word: dict) -> bytes:
    return (json.dumps(word, separators=(',', ':')) + '\n').encode()


def deterministic_gzip(data: bytes, filename: str | None = 'frame-word-23.json.gz') -> bytes:
    stream = io.BytesIO()
    with gzip.GzipFile(filename=filename, fileobj=stream, mode='wb', mtime=0, compresslevel=9) as archive:
        archive.write(data)
    return stream.getvalue()


def write_json(path: Path, payload: dict) -> None:
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n')
    temporary.replace(path)


def disk_available_kib(path: Path) -> int:
    stat = os.statvfs(path)
    return stat.f_bavail * stat.f_frsize // 1024


def gzip_sections(data: bytes) -> dict:
    assert data[:3] == b'\x1f\x8b\x08'
    flags = data[3]
    offset = 10
    extra = None
    filename = None
    comment = None
    if flags & 4:
        length = int.from_bytes(data[offset:offset + 2], 'little')
        extra = data[offset + 2:offset + 2 + length].hex()
        offset += 2 + length
    if flags & 8:
        end = data.index(b'\0', offset)
        filename = data[offset:end].decode('latin1')
        offset = end + 1
    if flags & 16:
        end = data.index(b'\0', offset)
        comment = data[offset:end].decode('latin1')
        offset = end + 1
    if flags & 2:
        offset += 2
    assert offset <= len(data) - 8
    return dict(header=data[:offset], deflate=data[offset:-8], trailer=data[-8:],
                metadata=dict(flags=flags, mtime=int.from_bytes(data[4:8], 'little'),
                              xfl=data[8], os=data[9], extra_hex=extra,
                              filename=filename, comment=comment))


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


def backward_cone(group: dict, output_support: int | None) -> tuple[list[int], int | None]:
    if output_support is None:
        return [], None
    live = output_support
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


def xor_selected(rows: list[int], support: int) -> int:
    value = 0
    for i, row in enumerate(rows):
        if support >> i & 1:
            value ^= row
    return value


def solve_linear_combination(rows: list[tuple[int, int]], target: int) -> list[int] | None:
    """Return physical labels whose exact GF(2) sum is target."""
    for slot, row in rows:
        if row == target:
            return [slot]
    pivots: dict[int, tuple[int, int]] = {}
    for position, (_, original) in enumerate(rows):
        row, support = original, 1 << position
        while row:
            pivot = row.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = (row, support)
                break
            old, old_support = pivots[pivot]
            row ^= old
            support ^= old_support
    remaining, support = target, 0
    while remaining:
        pivot = remaining.bit_length() - 1
        if pivot not in pivots:
            return None
        row, row_support = pivots[pivot]
        remaining ^= row
        support ^= row_support
    selected = [rows[i][0] for i in bit_positions(support)]
    check = 0
    for slot, row in rows:
        if slot in selected:
            check ^= row
    assert check == target
    return selected


def replay_group_linear_forms(group: dict, word: dict) -> dict[int, int]:
    """Rebuild the captured physical slot vectors in original input variables."""
    forms = {row['slot']: row['global_form_mask'] for row in group['linear_form_seed']}
    forms.update({row['slot']: row['global_form_mask'] for row in group.get('additional_linear_seeds', [])})
    operations = {row['op_index']: row for row in group['operations']}
    for record in group['timeline']:
        kind = record['record_kind']
        if kind == 'event' and record['cause'] == 'slot_allocation':
            forms[record['event'][0]] = 0
        elif kind == 'op':
            row = operations[record['op_index']]
            target, control, _ = row['op']
            assert tuple(row['op']) == tuple(word['ops'][row['op_index']])
            assert target in forms and control in forms
            assert forms[target] == row['physical_target_form_before_global']
            assert forms[control] == row['physical_control_form_before_global']
            forms[target] ^= forms[control]
            assert forms[target] == row['physical_target_form_after_global']
        elif kind == 'acquire' and record['kind'] == 'reclaimed':
            assert forms.get(record['slot']) == 0, 'reclaimed slot was not cleared'
    for row in group['linear_end_slot_forms']:
        assert forms[row['slot']] == row['global_form_mask']
    return forms


def validate_group_coverage(gid: int, group: dict, word: dict) -> None:
    expected_ops = [i for i, op in enumerate(word['ops']) if op[2] == gid]
    expected_events = [i for i, event in enumerate(word['events']) if event[2] == gid]
    assert group['operation_indices'] == expected_ops
    assert group['event_indices'] == expected_events
    timeline = group['emission_timeline']
    assert [entry['sequence'] for entry in timeline] == list(range(len(timeline)))
    assert [entry['op_index'] for entry in timeline if entry['record_kind'] == 'op'] == expected_ops
    assert [entry['event_index'] for entry in timeline if entry['record_kind'] == 'event'] == expected_events


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
    source_ops, source_live = backward_cone(groups[source_group], 1 << use_slot if use_slot is not None else None)
    consumer = groups[consumer_group]
    input_rows = consumer['linear_form_seed']
    input_values = [row['value'] for row in input_rows]
    input_forms = [row['global_form_mask'] for row in input_rows]
    target_coeff = consumer['coefficients'][USE['consumer']]
    target_signal = raw_trace['target_signal_global_mask']
    assert xor_selected(input_forms, target_coeff) == target_signal
    assert target_coeff == raw_trace['consumer_input_coefficient_mask']
    replayed_forms = replay_group_linear_forms(consumer, word)
    synthesis_basis = consumer['synthesis_basis']
    elimination = consumer['gaussian_elimination']
    eliminated_rows = [row['row_mask'] for row in synthesis_basis]
    for target, control in elimination:
        eliminated_rows[target] ^= eliminated_rows[control]
    assert eliminated_rows == [1 << i for i in range(len(input_rows))]
    slots_by_input = [row['slot'] for row in input_rows]
    expected_plan = [dict(target_input=a, control_input=b, target_slot=slots_by_input[a], control_slot=slots_by_input[b])
                     for a, b in reversed(consumer['gaussian_elimination'])]
    assert consumer['physical_xor_plan'] == expected_plan
    assert len(consumer['synthesis_op_indices']) == len(expected_plan)
    for index, plan in zip(consumer['synthesis_op_indices'], expected_plan):
        assert tuple(word['ops'][index]) == (plan['target_slot'], plan['control_slot'], consumer_group)
    end_rows = consumer['linear_end_slot_forms']
    end_by_slot = {row['slot']: row['global_form_mask'] for row in end_rows}
    for value, slot in consumer['value_slots'].items():
        assert replayed_forms[slot] == end_by_slot[slot]
        assert replayed_forms[slot] == xor_selected(input_forms, consumer['coefficients'][value])
    output_value_slots = consumer['value_slots']
    preferred = [output_value_slots[x] for x in consumer['output_values'] if x in output_value_slots]
    preferred += [row['slot'] for row in input_rows]
    preferred += [row['slot'] for row in end_rows]
    end_by_slot = {row['slot']: row['global_form_mask'] for row in end_rows}
    ordered_end_slots = list(dict.fromkeys(s for s in preferred if s in end_by_slot))
    target_support_slots = solve_linear_combination([(s, end_by_slot[s]) for s in ordered_end_slots], target_signal)
    target_support_mask = None if target_support_slots is None else sum(1 << s for s in target_support_slots)
    reconstructed_target = None
    if target_support_slots is not None:
        reconstructed_target = 0
        for slot in target_support_slots:
            reconstructed_target ^= end_by_slot[slot]
        assert reconstructed_target == target_signal
    target_ops, target_live = backward_cone(consumer, target_support_mask)
    expected_live = sum(1 << input_rows[i]['slot'] for i in bit_positions(target_coeff))
    if target_live is not None:
        assert target_live == expected_live
    direct_end_slots = [row['slot'] for row in end_rows if row['global_form_mask'] == target_signal]
    target_materializations = raw_trace['target_materializations']
    classification = ('MATERIALIZED' if direct_end_slots or target_materializations else
                      'VIRTUAL_LINEAR_FORM' if target_support_slots is not None else 'UNRESOLVED')
    current_uses = {row['index']: dict(index=row['index'], value=row['value'], target_group=row['consumer_group'],
                                       terminal=row['terminal'], role='block_output_use')
                    for row in consumer['compiler_uses']}
    for edge in consumer['selected_edges']:
        current_uses[edge['use']] = dict(index=edge['use'], value=edge['value'], role='matched_input_carry',
                                         input_index=edge['input_index'])
    end_role_rows = []
    for row in end_rows:
        end_role_rows.append(dict(slot=row['slot'], global_form_mask=row['global_form_mask'],
                                  values=row['values'],
                                  compiler_uses=[current_uses[u] for u in row['compiler_uses'] if u in current_uses],
                                  retired=(row['slot'] in consumer.get('retired_slots', []))))
    end_roles_by_slot = {row['slot']: row for row in end_role_rows}
    related_slots = {s for s in (source_value_slot, use_slot, input_slot, target_slot, *(target_support_slots or [])) if s is not None}
    for op_index in set(source_ops) | set(target_ops or []):
        related_slots.update(word['ops'][op_index][:2])
    input_coefficients = []
    consumer_inputs = groups[consumer_group]['input_slots']
    input_form_by_slot = {row['slot']: row['global_form_mask'] for row in input_rows}
    for row in consumer_inputs:
        input_coefficients.append(dict(input_index=row['input_index'], value=row['value'], slot=row['slot'],
                                       coefficient=bool(target_coeff >> row['input_index'] & 1),
                                       global_form_mask=input_form_by_slot[row['slot']],
                                       present_in_target_cone=(bool(target_live >> row['slot'] & 1) if target_live is not None else None)))
    assert all(x['coefficient'] == x['present_in_target_cone'] for x in input_coefficients)
    cross_block = source_group != consumer_group
    if cross_block:
        assert use_slot == input_slot
    source_reaches_target = bool(target_live >> input_slot & 1) if input_slot is not None and target_live is not None else None
    source_input_support = set(bit_positions(source_live)) if source_live is not None else set()
    target_input_support = set(bit_positions(target_live)) if target_live is not None else set()
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
                                    coefficient_rows=row['coefficients'], output_values=row['output_values'],
                                    output_basis=row['output_basis'], compiler_uses=row['compiler_uses'],
                                    selected_edges=row['selected_edges'],
                                    value_slots=row['value_slots'], operation_indices=expected_ops,
                                    event_indices=expected_events, emission_timeline=row['timeline'])
        for record in row['operations']:
            op_index = record['op_index']
            exact = tuple(word['ops'][op_index])
            assert exact == tuple(record['op'])
            relations = (['producer_value_to_selected_use'] if gid == source_group and op_index in source_ops else []) + (
                ['block_linear_form_for_Y2'] if gid == consumer_group and op_index in target_ops else [])
            if record['cause'].startswith(('retired_slot_clear', 'duplicate_use_copy')) and set(exact[:2]) & related_slots:
                relations.append('copy_or_clear_in_related_block')
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
            if record['cause'] == 'block_input':
                if gid == source_group and slot in source_input_support:
                    relation.append('FSa_producer_input_support_raise')
                if gid == consumer_group and slot in target_input_support:
                    relation.append('Y2_linear_input_support_raise')
                if slot == input_slot:
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
    direct_uses = raw_trace['target_direct_graph_uses']
    child_values = sorted({row['node'] for row in direct_uses if row['same_group']})
    output_absorption = []
    for child in child_values:
        child_coeff = consumer['coefficients'][child]
        output_absorption.append(dict(child_node=child, coefficient_mask=child_coeff,
                                      coefficient_input_values=[input_values[i] for i in bit_positions(child_coeff)],
                                      external_output=(child in consumer['output_values']),
                                      relation_to_Y2=dict(xor_input_values=[input_values[i] for i in bit_positions(child_coeff ^ target_coeff)],
                                                         coefficient_difference=child_coeff ^ target_coeff)))
    assert output_absorption and any(row['external_output'] for row in output_absorption)
    source_and_target_ops = sorted(set(source_ops) | set(target_ops or []))
    operation_map = {row['index']: row for row in operations_out}
    supporting_events = sorted({event_index for op_index in source_and_target_ops
                                for event_index in operation_map[op_index]['raise_event_indices']})
    for gid, slots_needed in ((source_group, source_input_support), (consumer_group, target_input_support)):
        supporting_events.extend(row['event_index'] for row in groups[gid]['events']
                                 if row['cause'] == 'block_input' and row['event'][0] in slots_needed)
    supporting_events = sorted(set(supporting_events))
    event_by_id = {row['index']: row for row in events_out}
    support_ranks = [dict(event_index=i, event=event_by_id[i]['event'], rank_Q_23=event_by_id[i]['rank_Q_23_factor'],
                          cause=event_by_id[i]['cause']) for i in supporting_events]
    all_support_ranks_known = all(row['rank_Q_23'] is not None for row in support_ranks)
    relation = 'VIRTUAL_LINEAR_FORM_CONE' if classification == 'VIRTUAL_LINEAR_FORM' else 'MATERIALIZED_PLUS_BLOCK_CONE'
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
                 linear_form=dict(status=classification, variables='the consumer block external input values in listed order',
                                  input_values=input_values, input_global_form_masks=[hex(x) for x in input_forms],
                                  target_coefficient_mask=target_coeff, target_input_values=[input_values[i] for i in bit_positions(target_coeff)],
                                  target_global_form_mask=hex(target_signal), coefficient_matches_graph_signal=True,
                                  dedicated_logical_value_slot=target_slot,
                                  materialized_end_slots=direct_end_slots,
                                  materialization_intervals=target_materializations,
                                  exit_slot_representation=dict(status=('MATERIALIZED' if direct_end_slots else 'VIRTUAL_LINEAR_FORM' if target_support_slots is not None else 'UNRESOLVED'),
                                      support_slots=target_support_slots,
                                      terms=[dict(slot=s, global_form_mask=hex(end_by_slot[s]),
                                                  logical_values=end_roles_by_slot[s]['values'],
                                                  compiler_uses=end_roles_by_slot[s]['compiler_uses'],
                                                  retired=end_roles_by_slot[s]['retired'])
                                             for s in (target_support_slots or [])],
                                      reconstructed_global_form=(hex(reconstructed_target) if reconstructed_target is not None else None)),
                                  all_exit_slot_forms=[dict(slot=row['slot'], global_form_mask=hex(row['global_form_mask']),
                                                            assigned_logical_values=row['values'], compiler_uses=row['compiler_uses'],
                                                            retired=row['retired']) for row in end_role_rows],
                                  input_seeds=consumer['linear_form_seed'],
                                  additional_physical_seeds=consumer.get('additional_linear_seeds', []),
                                  operation_form_records=consumer['operations'],
                                  emission_timeline=consumer['timeline'],
                                  end_slot_form_records=end_rows,
                                  retired_slots=consumer.get('retired_slots', []),
                                  physical_xor_form_replay='PASS',
                                  synthesis_basis=synthesis_basis,
                                  gaussian_elimination=elimination,
                                  physical_xor_plan=consumer['physical_xor_plan'],
                                  synthesis_op_indices=consumer['synthesis_op_indices'],
                                  physical_xor_plan_verified=True,
                                  target_linear_operation_indices=target_ops,
                                  source_to_target_input_support_slots=bit_positions(target_live) if target_live is not None else None,
                                  coalesced_output_absorption=output_absorption),
                 correspondence=dict(cardinality=relation, one_to_one_assumed=False,
                                     operation_relation='producer creation and consumer GF(2) output-form cones; shared block operations remain shared',
                                     source_to_target_input_coefficient=raw_trace['consumer_input_coefficient'],
                                     source_slot_in_Y2_emission_cone=source_reaches_target,
                                     producer_input_slot_support=(bit_positions(source_live) if source_live is not None else None),
                                     producer_to_use_op_indices=source_ops, consumer_to_Y2_op_indices=target_ops,
                                     consumer_input_coefficients=input_coefficients,
                                     target_supporting_event_indices=supporting_events,
                                     supporting_event_ranks_Q_23=support_ranks,
                                     supporting_event_rank_sum_if_complete=(sum(row['rank_Q_23'] for row in support_ranks)
                                                                           if all_support_ranks_known else None),
                                     supporting_known_rank_partial_sum=sum(row['rank_Q_23'] for row in support_ranks if row['rank_Q_23'] is not None),
                                     supporting_event_ranks_complete=all_support_ranks_known,
                                     target_group_auxiliary_operations=[row for row in operations_out
                                         if row['frame_group'] == consumer_group and row['index'] not in (target_ops or [])],
                                     standalone_use_cost='UNRESOLVED: shared block transformations, copy/clear preparation, wrapper multiplicity, and source-paper child assignment are not apportioned to this graph occurrence'),
                 groups=groups_out, operations=operations_out, events=events_out,
                 target_materialization_frame_events=[],
                 execution=dict(operation_indices='compiler ops[] and events[] entries in the frozen serialized word',
                                orientation='NOT_ENCODED_BY_ARRAY_ENTRY',
                                full_forward_or_reverse_word_replay='NOT_RUN'),
                 resources=dict(runtime_seconds=runtime, peak_rss_kib=peak_kib,
                                full_word_replay='NOT_RUN', h25='NOT_RUN', full_compile='NOT_RUN'))
    for interval in target_materializations:
        interval_events = {}
        for boundary in ('start', 'end'):
            for event_index in interval.get(boundary, {}).get('raise_event_indices', []):
                interval_events[event_index] = dict(event_index=event_index,
                    event=word['events'][event_index], cause=f'materialization_{boundary}')
        interval_events.update({item['event_index']: item for item in interval.get('frame_events', [])})
        for item in interval_events.values():
            event_index = item['event_index']
            exact = tuple(word['events'][event_index])
            assert exact == tuple(item['event'])
            slot, old, new = exact
            old_frame = tuple(word['frames'][old]) if old >= 0 else None
            new_frame = tuple(word['frames'][new])
            rank = frame_edge_rank(AXIS, old_frame, new_frame) if old_frame is not None and old != new else (0 if old_frame is not None else None)
            trace['target_materialization_frame_events'].append(dict(event_index=event_index, event=list(exact), slot=slot,
                old_frame=(dict(core_mask=old_frame[0], cover_mask=old_frame[1]) if old_frame is not None else None),
                new_frame=dict(core_mask=new_frame[0], cover_mask=new_frame[1]), rank_Q_23=rank))
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
    verification = trace['hash_verification']
    assert verification['checkpoint_written_before_trace_analysis']
    assert verification['canonical_json_sha256'] == expected_word
    assert verification['canonical_json_bytes_identical'] == (expected_word == EXPECTED_WORD)
    assert verification['canonical_json_matches_frozen'] == (expected_word == EXPECTED_WORD)
    assert verification['expected_canonical_json_sha256'] == EXPECTED_WORD
    assert verification['deterministic_gzip_sha256'] == expected_gzip
    assert verification['deterministic_gzip_matches_frozen'] == (expected_gzip == EXPECTED_GZIP)
    assert trace['status'] in ('MATERIALIZED', 'VIRTUAL_LINEAR_FORM', 'UNRESOLVED', 'WORD_DRIFT')
    linear = trace['linear_form']
    assert linear['status'] in ('MATERIALIZED', 'VIRTUAL_LINEAR_FORM', 'UNRESOLVED')
    input_forms = [int(mask, 16) for mask in linear['input_global_form_masks']]
    assert xor_selected(input_forms, linear['target_coefficient_mask']) == int(linear['target_global_form_mask'], 16)
    assert linear['target_input_values'] == [linear['input_values'][i] for i in bit_positions(linear['target_coefficient_mask'])]
    end_forms = {row['slot']: int(row['global_form_mask'], 16) for row in linear['all_exit_slot_forms']}
    support_slots = linear['exit_slot_representation']['support_slots']
    if support_slots is not None:
        target = 0
        for slot in support_slots:
            assert slot in end_forms
            target ^= end_forms[slot]
        assert target == int(linear['target_global_form_mask'], 16)
        assert linear['exit_slot_representation']['reconstructed_global_form'] == hex(target)
    if linear['status'] == 'VIRTUAL_LINEAR_FORM':
        assert not linear['materialized_end_slots']
        assert not linear['materialization_intervals']
        assert support_slots is not None
    if linear['status'] == 'MATERIALIZED':
        assert linear['materialized_end_slots'] or linear['materialization_intervals']
    assert trace['carriers']['target_value_slot'] == linear['dedicated_logical_value_slot']
    replay_group = dict(linear_form_seed=linear['input_seeds'],
                        additional_linear_seeds=linear['additional_physical_seeds'],
                        operations=linear['operation_form_records'],
                        timeline=linear['emission_timeline'],
                        linear_end_slot_forms=linear['end_slot_form_records'])
    replay_group_linear_forms(replay_group, word)
    basis_rows = [row['row_mask'] for row in linear['synthesis_basis']]
    for target, control in linear['gaussian_elimination']:
        basis_rows[target] ^= basis_rows[control]
    assert basis_rows == [1 << i for i in range(len(linear['input_values']))]
    input_slot_by_index = {row['input_index']: row['slot'] for row in linear['input_seeds']}
    expected_plan = [dict(target_input=a, control_input=b, target_slot=input_slot_by_index[a], control_slot=input_slot_by_index[b])
                     for a, b in reversed(linear['gaussian_elimination'])]
    assert linear['physical_xor_plan'] == expected_plan
    assert linear['physical_xor_plan_verified']
    assert len(linear['synthesis_op_indices']) == len(expected_plan)
    for index, step in zip(linear['synthesis_op_indices'], expected_plan):
        assert tuple(word['ops'][index]) == (step['target_slot'], step['control_slot'], trace['blocks']['consumer_group'])
    assert trace['carriers']['matched'] == (trace['carriers']['match_edge_index'] is not None)
    for gid, group in trace['groups'].items():
        g = int(gid)
        validate_group_coverage(g, group, word)
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
    target_timeline = linear['emission_timeline']
    cone_ops, cone_live = backward_cone(dict(timeline=target_timeline),
        sum(1 << slot for slot in (support_slots or [])) if support_slots is not None else None)
    assert cone_ops == trace['correspondence']['consumer_to_Y2_op_indices']
    if cone_live is None:
        assert trace['linear_form']['source_to_target_input_support_slots'] is None
    else:
        assert bit_positions(cone_live) == trace['linear_form']['source_to_target_input_support_slots']
    for interval in linear['materialization_intervals']:
        slot = interval['slot']
        assert 0 <= slot < len(word['frames'])
        for edge in ('start', 'end'):
            record = interval.get(edge, {})
            op = record.get('operation')
            if op is not None:
                assert tuple(op) == tuple(word['ops'][record['index']])
                assert op[0] == slot
            event_indices = record.get('raise_event_indices', [])
            if op is not None:
                assert [word['events'][event_index][0] for event_index in event_indices] == list(op[:2])
            else:
                assert all(tuple(word['events'][event_index])[0] == slot for event_index in event_indices)
        for row in interval.get('frame_events', []):
            assert tuple(row['event']) == tuple(word['events'][row['event_index']])
    for row in trace['target_materialization_frame_events']:
        assert tuple(row['event']) == tuple(word['events'][row['event_index']])
        if row['old_frame'] is not None and row['event'][1] != row['event'][2]:
            assert row['rank_Q_23'] == frame_edge_rank(AXIS,
                (row['old_frame']['core_mask'], row['old_frame']['cover_mask']),
                (row['new_frame']['core_mask'], row['new_frame']['cover_mask']))
    support_ranks = trace['correspondence']['supporting_event_ranks_Q_23']
    complete = all(row['rank_Q_23'] is not None for row in support_ranks)
    assert complete == trace['correspondence']['supporting_event_ranks_complete']
    expected_rank_sum = sum(row['rank_Q_23'] for row in support_ranks) if complete else None
    assert expected_rank_sum == trace['correspondence']['supporting_event_rank_sum_if_complete']
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
    rejected('wrong GF(2) input coefficient', lambda x: x['linear_form'].__setitem__('target_coefficient_mask', x['linear_form']['target_coefficient_mask'] ^ 1))
    def alter_linear_support(x):
        support = x['linear_form']['exit_slot_representation']['support_slots']
        assert support
        support[0] = support[0] + 1
    rejected('wrong physical slot in virtual linear form', alter_linear_support)
    rejected('wrong physical elimination slot', lambda x: x['linear_form']['physical_xor_plan'][0].__setitem__('target_slot', x['linear_form']['physical_xor_plan'][0]['target_slot'] + 1))
    rejected('wrong compiler op index', lambda x: x['operations'][0].__setitem__('index', len(word['ops'])))
    rejected('wrong op frame group', lambda x: x['operations'][0].__setitem__('frame_group', x['operations'][0]['frame_group'] + 1))
    def omit_copy_or_clear(x):
        i = next(i for i, op in enumerate(x['operations']) if 'copy' in op.get('cause', '') or 'clear' in op.get('cause', ''))
        x['operations'].pop(i)
    if any('copy' in op.get('cause', '') or 'clear' in op.get('cause', '') for op in trace['operations']):
        rejected('omitted copy/clear operation record', omit_copy_or_clear)
    else:
        rejected('omitted group operation record (copy/clear validator fixture)', lambda x: x['operations'].pop())
    rejected('omitted frame-raise event', lambda x: x['events'].pop())
    rejected('stale matching decision', lambda x: x['carriers'].__setitem__('matched', not x['carriers']['matched']))
    rejected('stale pinned compiler hash', lambda x: x['source'].__setitem__('frozen_compiler_sha256', '0' * 64))
    rejected('wrong frame-event group', lambda x: x['events'][0]['event'].__setitem__(2, x['events'][0]['event'][2] + 1))
    def swap_timeline(x):
        timeline = x['linear_form']['emission_timeline']
        if len(timeline) > 1:
            positions = [i for i, row in enumerate(timeline) if row['record_kind'] == 'op'][:2]
            timeline[positions[0]], timeline[positions[1]] = timeline[positions[1]], timeline[positions[0]]
        else:
            timeline[0]['sequence'] += 1
    rejected('swapped emission timeline', swap_timeline)
    rejected('stale frozen word hash', lambda x: x['source'].__setitem__('word_sha256', '0' * 64))
    if trace['carriers']['target_value_slot'] is None:
        rejected('lost hash checkpoint when dedicated Y2 slot is None', lambda x: x.__setitem__('hash_verification', {}))
    rejected('invented execution orientation', lambda x: x['execution'].__setitem__('orientation', 'REVERSE_COMPLEMENT'))
    rejected('forced one-XOR bijection', lambda x: x['correspondence'].__setitem__('one_to_one_assumed', True))
    return cases


def self_check() -> None:
    started = time.monotonic()
    source_frame = (0b111, 0b111)
    expanded_frame = (0b001, (1 << AXIS) - 1)
    assert rational_rank(projector(AXIS, source_frame)) == 1
    assert frame_edge_rank(AXIS, source_frame, expanded_frame) == AXIS - 2
    cone, inputs = backward_cone(dict(timeline=[
        dict(record_kind='event', cause='slot_allocation', event=(4, -1, 7)),
        dict(record_kind='op', op_index=0, op=(3, 1, 7)),
        dict(record_kind='op', op_index=1, op=(4, 3, 7))]), 1 << 4)
    assert cone == [0, 1] and inputs == ((1 << 1) | (1 << 3))
    assert backward_cone(dict(timeline=[]), None) == ([], None)
    assert solve_linear_combination([(13, 0b111), (10, 0b001), (11, 0b010)], 0b110) == [13, 10]
    assert solve_linear_combination([(10, 0b001), (11, 0b010)], 0b100) is None
    word = dict(ops=[[3, 1, 7], [4, 3, 7], [5, 4, 7]],
                events=[[3, 6, 7], [1, 6, 7], [4, 6, 7], [3, 6, 7], [5, 6, 7], [4, 6, 7]])
    timeline = [dict(sequence=0, record_kind='event', event_index=0),
                dict(sequence=1, record_kind='event', event_index=1),
                dict(sequence=2, record_kind='op', op_index=0),
                dict(sequence=3, record_kind='event', event_index=2),
                dict(sequence=4, record_kind='event', event_index=3),
                dict(sequence=5, record_kind='op', op_index=1),
                dict(sequence=6, record_kind='event', event_index=4),
                dict(sequence=7, record_kind='event', event_index=5),
                dict(sequence=8, record_kind='op', op_index=2)]
    group = dict(operation_indices=[0, 1, 2], event_indices=[0, 1, 2, 3, 4, 5], emission_timeline=timeline)
    validate_group_coverage(7, group, word)
    bad = copy.deepcopy(group);bad['operation_indices'].remove(1)
    try: validate_group_coverage(7, bad, word)
    except AssertionError: pass
    else: raise AssertionError('omitted copy/clear operation was accepted')
    bad = copy.deepcopy(group);bad['event_indices'].pop()
    try: validate_group_coverage(7, bad, word)
    except AssertionError: pass
    else: raise AssertionError('omitted frame raise was accepted')
    bad = copy.deepcopy(group);bad['emission_timeline'][2],bad['emission_timeline'][5]=bad['emission_timeline'][5],bad['emission_timeline'][2]
    try: validate_group_coverage(7, bad, word)
    except AssertionError: pass
    else: raise AssertionError('reordered physical operations were accepted')
    forms = replay_group_linear_forms(dict(
        linear_form_seed=[dict(slot=1,global_form_mask=0b010)],
        additional_linear_seeds=[dict(slot=3,global_form_mask=0b001,first_op_index=0)],
        operations=[dict(op_index=0,op=[3,1,7],physical_target_form_before_global=1,physical_control_form_before_global=2,physical_target_form_after_global=3)],
        timeline=[dict(record_kind='op',op_index=0)],
        linear_end_slot_forms=[dict(slot=3,global_form_mask=3)]), dict(ops=[[3,1,7]],events=[]))
    assert forms == {1: 2, 3: 3}
    named_gzip = gzip_sections(deterministic_gzip(b'GF(2)'))
    unnamed_gzip = gzip_sections(deterministic_gzip(b'GF(2)', filename=None))
    assert named_gzip['metadata']['filename'] == 'frame-word-23.json'
    assert unnamed_gzip['metadata']['filename'] is None
    assert named_gzip['deflate'] == unnamed_gzip['deflate'] and named_gzip['trailer'] == unnamed_gzip['trailer']
    receipt = dict(status='PASS', tests=['exact rational frame edge', 'GF(2) combination solver',
        'virtual-form reconstruction', 'reverse operation cone', 'exact ops/events coverage',
        'wrong order rejection', 'missing copy/clear rejection', 'missing raise rejection',
        'gzip filename metadata comparison'],
        wall_seconds=time.monotonic() - started, peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    write_json(HERE / 'FAST_CHECK_RECEIPT.json', receipt)
    print(json.dumps(receipt), flush=True)


def normalize_raw_trace(raw_trace: dict) -> dict:
    raw_trace['groups'] = {int(gid): row for gid, row in raw_trace['groups'].items()}
    for row in raw_trace['groups'].values():
        for key in ('coefficients', 'value_slots'):
            row[key] = {int(k): v for k, v in row[key].items()}
    return raw_trace


def postprocess_saved_word() -> None:
    """Resume trace analysis from the hash checkpoint without recompiling."""
    manifest, expected, frozen_raw = verify_pins()
    hash_path = HERE / 'WORD_HASH_RECEIPT.json'
    raw_trace_path = HERE / 'FOCUSED_RAW_TRACE.json'
    assert hash_path.exists() and raw_trace_path.exists()
    hash_verification = json.loads(hash_path.read_text())
    raw_trace = normalize_raw_trace(json.loads(raw_trace_path.read_text()))
    if hash_verification['canonical_json_matches_frozen']:
        raw = frozen_raw
    else:
        generated_path = HERE / 'GENERATED_WORD_H23.json.gz'
        assert generated_path.exists(), 'generated word was not retained after canonical drift'
        raw = gzip.decompress(generated_path.read_bytes())
    word = json.loads(raw)
    assert canonical_word(word) == raw
    assert sha(raw) == hash_verification['canonical_json_sha256']
    initial_gzip = deterministic_gzip(raw, filename=None)
    initial_gzip_hash = sha(initial_gzip)
    initial_variant = hash_verification.get('initial_bytesio_gzip_variant')
    assert initial_gzip_hash == (initial_variant['sha256'] if initial_variant else hash_verification['deterministic_gzip_sha256'])
    generated_gzip = deterministic_gzip(raw)
    gzip_hash = sha(generated_gzip)
    frozen_gzip = (PINNED / f'research/rank-pair/frame-word-{AXIS}.json.gz').read_bytes()
    generated_sections, frozen_sections = gzip_sections(generated_gzip), gzip_sections(frozen_gzip)
    hash_verification['initial_bytesio_gzip_variant'] = dict(sha256=initial_gzip_hash, bytes=len(initial_gzip),
        filename=None, matches_frozen=(initial_gzip == frozen_gzip))
    hash_verification['word_stats']['gzip_bytes'] = len(generated_gzip)
    hash_verification.update(
        deterministic_gzip_sha256=gzip_hash, generated_gzip_bytes=len(generated_gzip),
        deterministic_gzip_matches_frozen=(generated_gzip == frozen_gzip and gzip_hash == EXPECTED_GZIP),
        gzip_writer=dict(format='gzip.GzipFile', filename='frame-word-23.json.gz', mtime=0, compresslevel=9,
                         python=sys.version.split()[0], zlib_compile=zlib.ZLIB_VERSION,
                         zlib_runtime=zlib.ZLIB_RUNTIME_VERSION),
        gzip_comparison=dict(header_bytes_equal=generated_sections['header'] == frozen_sections['header'],
            deflate_payload_equal=generated_sections['deflate'] == frozen_sections['deflate'],
            trailer_equal=generated_sections['trailer'] == frozen_sections['trailer'],
            generated_header=generated_sections['metadata'], frozen_header=frozen_sections['metadata'],
            outcome=('EXACT_MATCH' if generated_gzip == frozen_gzip else
                     'IDENTICAL_DEFLATE_DIFFERENT_GZIP_HEADER' if generated_sections['deflate'] == frozen_sections['deflate'] and generated_sections['trailer'] == frozen_sections['trailer'] else
                     'COMPRESSED_STREAM_DIFFERS')))
    write_json(hash_path, hash_verification)
    manifest, expected, _ = verify_pins()
    stats = hash_verification['word_stats']
    compiled = dict(roles=stats['roles'], rank_mass=stats['rank_mass'], elementary_xors=stats['elementary_xors'],
                    stats=stats['statistics'], histogram={int(k): v for k, v in stats['histogram'].items()})
    assert all(hash_verification['compiled_baseline_checks'].values())
    compile_runtime = hash_verification['compile_seconds']
    compile_peak_kib = hash_verification['compile_peak_rss_kib']
    post_start = time.monotonic()
    trace = build_trace(raw_trace, compiled, word, sha(raw), gzip_hash, expected, manifest,
                        compile_runtime, compile_peak_kib)
    status = 'WORD_DRIFT' if not hash_verification['canonical_json_matches_frozen'] else trace['status']
    trace['status'] = status
    trace['hash_verification'] = hash_verification
    validate_trace(trace, word, sha(raw), gzip_hash)
    negative_controls = run_negative_controls(trace, word, sha(raw), gzip_hash)
    trace['negative_controls'] = dict(status='PASS', cases=negative_controls, fixture_only=False)
    trace['compiled_summary'] = dict(roles=compiled['roles'], elementary_xors=compiled['elementary_xors'],
        rank_mass=compiled['rank_mass'], statistics=compiled['stats'],
        generated_word_operations=4 * len(word['ops']) + 2 * len(word['scatter']) + 2 * len(word['sources']),
        generated_events=len(word['events']), dirty_basis_replay='NOT RUN')
    post_seconds = time.monotonic() - post_start
    observed_peaks = [compile_peak_kib, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss]
    prior_receipt = HERE / 'FOCUSED_RECEIPT.json'
    if prior_receipt.exists():
        observed_peaks.append(json.loads(prior_receipt.read_text()).get('peak_rss_kib', 0))
    recovery_record = HERE / 'runs' / 'attempt-02' / 'POSTPROCESS_RECOVERY.json'
    if recovery_record.exists():
        observed_peaks.append(json.loads(recovery_record.read_text()).get('observed_peak_rss_kib', 0))
    peak_kib = max(observed_peaks)
    total_runtime = compile_runtime + post_seconds
    trace['resources'].update(runtime_seconds=total_runtime, total_runtime_seconds=total_runtime, peak_rss_kib=peak_kib,
        compile_seconds=compile_runtime, compile_peak_rss_kib=compile_peak_kib,
        postprocess_seconds=post_seconds, postprocess_only_recovery=True,
        free_disk_kib_after_run=disk_available_kib(HERE))
    write_json(HERE / 'TRACE.json', trace)
    completed_utc = datetime.now(timezone.utc).isoformat()
    receipt = dict(status=status, started_utc=json.loads((HERE / 'FOCUSED_STARTED.json').read_text())['started_utc'],
        completed_utc=completed_utc, axis=AXIS, source_commit=PR63, compile_count=1,
        compile_seconds=compile_runtime, postprocess_seconds=post_seconds, total_runtime_seconds=total_runtime,
        compile_peak_rss_kib=compile_peak_kib, peak_rss_kib=peak_kib,
        free_disk_kib_after_run=disk_available_kib(HERE), canonical_word_sha256=sha(raw), gzip_sha256=gzip_hash,
        pinned_word_match=hash_verification['canonical_json_matches_frozen'],
        gzip_matches_frozen=hash_verification['deterministic_gzip_matches_frozen'],
        compiled_baseline_checks=hash_verification['compiled_baseline_checks'], trace_file='TRACE.json',
        raw_trace_file='FOCUSED_RAW_TRACE.json', hash_checkpoint_file='WORD_HASH_RECEIPT.json',
        postprocess_only_recovery=True)
    write_json(HERE / 'FOCUSED_RECEIPT.json', receipt)
    marker_path = HERE / 'FOCUSED_STARTED.json'
    marker = json.loads(marker_path.read_text())
    marker.update(status='COMPLETED_FROM_SAVED_WORD_CHECKPOINT', completed_utc=completed_utc,
                  total_runtime_seconds=total_runtime, peak_rss_kib=peak_kib, word_hash=sha(raw))
    marker.pop('error', None);marker.pop('traceback', None)
    write_json(marker_path, marker)
    failure = HERE / 'TRACE_FAILURE.json'
    if failure.exists(): failure.unlink()
    print(json.dumps(dict(status=status, postprocess_only_recovery=True, runtime_seconds=total_runtime,
        peak_rss_kib=peak_kib, canonical_word_sha256=sha(raw), gzip_sha256=gzip_hash,
        source_group=raw_trace['producer_group'], consumer_group=raw_trace['consumer_group'],
        source_slot=raw_trace['source_use_slot'], consumer_input_slot=raw_trace['consumer_input_slot'],
        target_slot=raw_trace['target_value_slot'], op_count=len(word['ops']), event_count=len(word['events']))), flush=True)


def run_focused() -> None:
    attempt = HERE / 'FOCUSED_STARTED.json'
    receipt_path = HERE / 'FOCUSED_RECEIPT.json'
    trace_path = HERE / 'TRACE.json'
    assert not attempt.exists() and not receipt_path.exists() and not trace_path.exists(), 'refusing a second FOCUSED run'
    manifest, expected, frozen_raw = verify_pins()
    available_kib = next(int(line.split()[1]) for line in Path('/proc/meminfo').read_text().splitlines()
                         if line.startswith('MemAvailable:'))
    assert available_kib >= MIN_AVAILABLE_KIB, f'RESOURCE_GATED: only {available_kib} KiB available'
    started_utc = datetime.now(timezone.utc).isoformat()
    run_start = time.monotonic()
    started = dict(status='STARTED', started_utc=started_utc, axis=AXIS, source_commit=PR63,
                   compile_count=1,
                   resource_gate=dict(pre_compile_mem_available_kib=available_kib,
                                      minimum_available_kib=MIN_AVAILABLE_KIB,
                                      pre_compile_free_disk_kib=disk_available_kib(HERE),
                                      address_space_limit='NOT_APPLIED', wall_timeout_seconds=1800))
    write_json(attempt, started)
    sys.dont_write_bytecode = True
    compiler = load_module('instrumented_rank_pair_compiler', PINNED / 'scripts/experiments/rank_pair_compiler.py')
    # Load the graph's PR 63 helper modules from its own pinned tree, separate
    # from the PR 48 producer modules already imported by the compiler copy.
    for name in ('partial_swap', 'partial_swap.paired', 'partial_swap.shared', 'exclusion_circuit'):
        sys.modules.pop(name, None)
    sys.path.insert(0, str(PINNED / 'scripts'))
    graph_module = load_module('pinned_pair_graph', PINNED / 'research/pair-assembly/pair_graph.py')
    compiler.graph = graph_module.graph
    compile_start = time.monotonic()
    try:
        compiled, word, raw_trace = compiler.compile_(AXIS, matching=True, reclaim=True, dirty=False, trace_spec=USE)
    except BaseException as exc:
        state = json.loads(attempt.read_text())
        state.update(status='FAILED_DURING_COMPILE', error=repr(exc), traceback=traceback.format_exc())
        write_json(attempt, state)
        raise
    compile_runtime = time.monotonic() - compile_start
    compile_peak_kib = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    raw = canonical_word(word)
    word_hash = sha(raw)
    generated_gzip = deterministic_gzip(raw)
    gzip_hash = sha(generated_gzip)
    frozen_gzip = (PINNED / f'research/rank-pair/frame-word-{AXIS}.json.gz').read_bytes()
    generated_sections = gzip_sections(generated_gzip)
    frozen_sections = gzip_sections(frozen_gzip)
    check_fields = ('roles', 'rank_mass', 'elementary_xors', 'stats')
    receipt_checks = {key: compiled[key] == expected['compiled'][key] for key in check_fields}
    receipt_checks['histogram'] = compiled['histogram'] == {int(k): v for k, v in expected['compiled']['histogram'].items()}
    hash_verification = dict(checkpoint_written_before_trace_analysis=True,
        canonical_json_sha256=word_hash, expected_canonical_json_sha256=EXPECTED_WORD,
        canonical_json_bytes_identical=(raw == frozen_raw),
        canonical_json_matches_frozen=(raw == frozen_raw and word_hash == EXPECTED_WORD),
        generated_canonical_bytes=len(raw), expected_canonical_bytes=len(frozen_raw),
        deterministic_gzip_sha256=gzip_hash, expected_gzip_sha256=EXPECTED_GZIP,
        deterministic_gzip_matches_frozen=(gzip_hash == EXPECTED_GZIP),
        generated_gzip_bytes=len(generated_gzip), frozen_gzip_bytes=len(frozen_gzip),
        gzip_comparison=dict(header_bytes_equal=generated_sections['header'] == frozen_sections['header'],
                             deflate_payload_equal=generated_sections['deflate'] == frozen_sections['deflate'],
                             trailer_equal=generated_sections['trailer'] == frozen_sections['trailer'],
                             generated_header=generated_sections['metadata'], frozen_header=frozen_sections['metadata'],
                             outcome=('EXACT_MATCH' if generated_gzip == frozen_gzip else
                                      'IDENTICAL_DEFLATE_DIFFERENT_GZIP_HEADER' if generated_sections['deflate'] == frozen_sections['deflate'] and generated_sections['trailer'] == frozen_sections['trailer'] else
                                      'COMPRESSED_STREAM_DIFFERS')),
        gzip_writer=dict(format='gzip.GzipFile', filename='frame-word-23.json.gz', mtime=0, compresslevel=9,
                         python=sys.version.split()[0], zlib_compile=zlib.ZLIB_VERSION,
                         zlib_runtime=zlib.ZLIB_RUNTIME_VERSION),
        compiled_baseline_checks=receipt_checks,
        compile_seconds=compile_runtime, compile_peak_rss_kib=compile_peak_kib,
        post_compile_free_disk_kib=disk_available_kib(HERE),
        word_stats=dict(roles=compiled['roles'], elementary_xors=len(word['ops']), events=len(word['events']),
                        frames=len(word['frames']), scatter=len(word['scatter']), sources=len(word['sources']),
                        canonical_bytes=len(raw), gzip_bytes=len(generated_gzip), rank_mass=compiled['rank_mass'],
                        histogram=compiled['histogram'], statistics=compiled['stats']))
    write_json(HERE / 'WORD_HASH_RECEIPT.json', hash_verification)
    write_json(HERE / 'FOCUSED_RAW_TRACE.json', raw_trace)
    if not hash_verification['canonical_json_matches_frozen']:
        (HERE / 'GENERATED_WORD_H23.json.gz').write_bytes(generated_gzip)
    started.update(status='WORD_CHECKPOINT_SAVED_TRACE_PENDING', compile_seconds=compile_runtime,
                    compile_peak_rss_kib=compile_peak_kib)
    write_json(attempt, started)
    stable = expected['compiled']
    assert all(receipt_checks.values()), f'compiled receipt drift: {receipt_checks}'
    trace = build_trace(raw_trace, compiled, word, word_hash, gzip_hash, expected, manifest, compile_runtime, compile_peak_kib)
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
    total_runtime = time.monotonic() - run_start
    peak_kib = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    trace['resources'].update(runtime_seconds=total_runtime, total_runtime_seconds=total_runtime, peak_rss_kib=peak_kib,
                              compile_seconds=compile_runtime, compile_peak_rss_kib=compile_peak_kib,
                              postprocess_seconds=total_runtime - compile_runtime,
                              free_disk_kib_after_run=disk_available_kib(HERE))
    trace_path.write_text(json.dumps(trace, indent=2, sort_keys=True) + '\n')
    receipt = dict(status=status, started_utc=started_utc, completed_utc=datetime.now(timezone.utc).isoformat(),
                   axis=AXIS, source_commit=PR63, compile_count=1, compile_seconds=compile_runtime,
                   total_runtime_seconds=total_runtime, compile_peak_rss_kib=compile_peak_kib,
                   peak_rss_kib=peak_kib, free_disk_kib_after_run=disk_available_kib(HERE),
                   canonical_word_sha256=word_hash, gzip_sha256=gzip_hash,
                   pinned_word_match=hash_verification['canonical_json_matches_frozen'],
                   compiled_baseline_checks=receipt_checks, trace_file='TRACE.json',
                   raw_trace_file='FOCUSED_RAW_TRACE.json', hash_checkpoint_file='WORD_HASH_RECEIPT.json')
    write_json(receipt_path, receipt)
    started.update(status='COMPLETED', completed_utc=receipt['completed_utc'], total_runtime_seconds=total_runtime,
                   peak_rss_kib=peak_kib, word_hash=word_hash)
    write_json(attempt, started)
    print(json.dumps(dict(status=status, runtime_seconds=total_runtime, peak_rss_kib=peak_kib,
                          canonical_word_sha256=word_hash, gzip_sha256=gzip_hash,
                          source_group=raw_trace['producer_group'], consumer_group=raw_trace['consumer_group'],
                          source_slot=raw_trace['source_use_slot'], consumer_input_slot=raw_trace['consumer_input_slot'],
                          target_slot=raw_trace['target_value_slot'], op_count=len(word['ops']), event_count=len(word['events']))), flush=True)


if __name__ == '__main__':
    if '--self-check' in sys.argv[1:]:
        self_check()
    elif '--postprocess-saved-word' in sys.argv[1:]:
        postprocess_saved_word()
    else:
        try:
            run_focused()
        except BaseException as exc:
            marker = HERE / 'FOCUSED_STARTED.json'
            if marker.exists():
                state = json.loads(marker.read_text())
                if state['status'] in ('STARTED', 'WORD_CHECKPOINT_SAVED_TRACE_PENDING'):
                    state.update(status='FAILED_AFTER_WORD_CHECKPOINT' if (HERE / 'WORD_HASH_RECEIPT.json').exists() else 'FAILED',
                                 error=repr(exc), traceback=traceback.format_exc())
                    write_json(marker, state)
                    write_json(HERE / 'TRACE_FAILURE.json', dict(error=repr(exc), traceback=traceback.format_exc(),
                                hash_checkpoint_file=('WORD_HASH_RECEIPT.json' if (HERE / 'WORD_HASH_RECEIPT.json').exists() else None),
                                raw_trace_file=('FOCUSED_RAW_TRACE.json' if (HERE / 'FOCUSED_RAW_TRACE.json').exists() else None)))
            raise
