#!/usr/bin/env python3
"""Focused PR 63 replay and one forced carry-exchange comparison."""
from __future__ import annotations

import collections
import gzip
import hashlib
import importlib.util
import json
import resource
import sys
import time
from pathlib import Path

FAST_SOURCE = "e2eb7063e5ca6788dd86b3c2affdc49b470efc3ba57ca89ef820e76e6843bb89"
WORD = "640696dd7cd893add9d6e12d0d587956fecf113b2eff8c29547b82e5a6f3c0ad"
WORD_GZIP = "1a57c143380a063211653f1f35e7cc9710539523b0b34c90f354a0425c34bd59"
DEFAULT_VALUE = 62984


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: dict) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def span_probe(g, slots, frames, retired, blocks, signal, contains,
               value, value_uses, uses, assign, order):
    target = signal[value]
    position = {group: i for i, group in enumerate(order)}
    demand_slots = {assign[u] for u in value_uses[value]
                    if uses[u][1] == g and uses[u][2] is None and u in assign}
    eligible = []
    for slot, form in enumerate(slots):
        if slot in demand_slots or not form or form == target:
            continue
        old_group = frames[slot]
        if not contains(blocks[old_group]["frame"], blocks[g]["frame"]):
            continue
        future = [u for u, other_slot in assign.items() if other_slot == slot
                  and position[uses[u][1]] > position[g]]
        if any(uses[u][2] is not None for u in future):
            continue
        if any(not contains(blocks[g]["frame"], blocks[uses[u][1]]["frame"])
               for u in future):
            continue
        eligible.append((slot, form))

    # Keep a literal support witness, not only a Boolean span result.
    pivots = {}
    for i, (slot, form) in enumerate(eligible):
        row, support = form, 1 << i
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
            break
        row, source_support = pivots[pivot]
        remaining ^= row
        support ^= source_support
    in_span = remaining == 0
    witness = [dict(slot=eligible[i][0], form_hex=hex(eligible[i][1]))
               for i in range(len(eligible)) if support >> i & 1] if in_span else []
    retired_rows = [(slot, form) for slot, form in eligible if slot in retired]
    small_witness = None
    retired_by_form = collections.defaultdict(list)
    for slot, form in retired_rows:
        retired_by_form[form].append(slot)
    for slot, form in retired_rows:
        for other in retired_by_form.get(target ^ form, ()):
            if other != slot:
                small_witness = dict(arity=2, slots=[slot, other])
                break
        if small_witness is not None:
            break
    if small_witness is None:
        pair_forms = collections.defaultdict(list)
        for i, (slot_a, form_a) in enumerate(retired_rows):
            if form_a == target:
                continue
            for slot_b, form_b in retired_rows[i+1:]:
                if form_b != target:
                    pair_forms[form_a ^ form_b].append((slot_a, slot_b))
        for slot, form in retired_rows:
            if form == target:
                continue
            for a, b in pair_forms.get(target ^ form, ()):
                if slot not in (a, b):
                    small_witness = dict(arity=3, slots=[a, b, slot])
                    break
            if small_witness is not None:
                break
    if small_witness is not None:
        witness_slots = small_witness["slots"]
        forms_by_slot = dict(eligible)
        assert len(witness_slots) == small_witness["arity"]
        assert len(set(witness_slots)) == len(witness_slots)
        reconstructed = 0
        for slot in witness_slots:
            reconstructed ^= forms_by_slot[slot]
        assert reconstructed == target
    return dict(value=value, target_group=g, target_frame=list(blocks[g]["frame"]),
        target_input_slots=sorted(demand_slots), eligible_other_roles=len(eligible),
        retired_eligible_roles=sum(slot in retired for slot, _ in eligible),
        target_in_available_other_role_span=in_span, witness=witness,
        retired_one_to_three_carrier_witness=small_witness,
        interpretation="A witness is only a control-span screen; writing, restoring, and endpoint costs remain due.")


def span_probe_batch(g, targets, slots, frames, retired, blocks, signal, contains,
                     value_uses, uses, assign, order, future_by_slot):
    """Screen many demanded values at one compiler point with shared role eligibility."""
    position = {group: i for i, group in enumerate(order)}
    eligible_base = []
    for slot, form in enumerate(slots):
        if not form or not contains(blocks[frames[slot]]["frame"], blocks[g]["frame"]):
            continue
        future = [u for u in future_by_slot.get(slot, ())
                  if position[uses[u][1]] > position[g]]
        if any(uses[u][2] is not None for u in future):
            continue
        if any(not contains(blocks[g]["frame"], blocks[uses[u][1]]["frame"])
               for u in future):
            continue
        eligible_base.append((slot, form, slot in retired))

    results = []
    for value in targets:
        target = signal[value]
        demand_slots = {assign[u] for u in value_uses[value]
                        if uses[u][1] == g and uses[u][2] is None and u in assign}
        eligible = [(slot, form, is_retired) for slot, form, is_retired in eligible_base
                    if slot not in demand_slots and form != target]
        pivots = {}
        for _, form, _ in eligible:
            row = form
            while row:
                pivot = row.bit_length() - 1
                if pivot not in pivots:
                    pivots[pivot] = row
                    break
                row ^= pivots[pivot]
        remaining = target
        while remaining:
            pivot = remaining.bit_length() - 1
            if pivot not in pivots:
                break
            remaining ^= pivots[pivot]
        results.append(dict(value=value, target_group=g,
            eligible_other_roles=len(eligible),
            retired_eligible_roles=sum(is_retired for _, _, is_retired in eligible),
            target_in_available_other_role_span=remaining == 0))
    return results


def replace_once(source: str, old: str, new: str) -> str:
    assert source.count(old) == 1, f"instrumentation anchor count: {source.count(old)} for {old!r}"
    return source.replace(old, new, 1)


def instrument(source: str) -> str:
    source = replace_once(source, "trace=dict(logical_use=",
        "trace=dict(focus_value=producer,probe_groups=list(trace_spec.get('probe_groups',())),all_span_targets_by_group=trace_spec.get('all_span_targets_by_group',{}),all_span_rows=[],logical_use=")
    source = replace_once(source, "for g in {pg,cg}:\n",
        "for g in ({pg,cg}|set(trace_spec.get('extra_trace_groups',()))):\n")
    source = replace_once(source,
        "for step,g in enumerate(order):\n  b=blocks[g];outuses=[u for u in b['uses']if u not in right];outvalues=sorted({uses[u][0]for u in outuses});assert outvalues==b['outvalues']\n",
        "for step,g in enumerate(order):\n  b=blocks[g];outuses=[u for u in b['uses']if u not in right];outvalues=sorted({uses[u][0]for u in outuses});assert outvalues==b['outvalues']\n  if trace is not None and g in trace['probe_groups']:\n   trace['groups'][g]['focus_span']=__issue21_span_probe__(g,slots,frames,retired,blocks,signal,contains,trace['focus_value'],value_uses,uses,assign,order)\n  if trace is not None and g in trace['all_span_targets_by_group']:\n   trace['all_span_rows'].extend(__issue21_batch_span_probe__(g,trace['all_span_targets_by_group'][g],slots,frames,retired,blocks,signal,contains,value_uses,uses,assign,order,issue21_future_by_slot))\n")
    source = replace_once(source,
        "slots=[];frames=[];ops=[];events=[];hist=Counter();assign={};sources={};retired=set();linear_forms={};target_open={};stats['regions']=len(blocks)",
        "slots=[];frames=[];ops=[];events=[];hist=Counter();assign={};sources={};retired=set();linear_forms={};target_open={};issue21_future_by_slot=defaultdict(list);stats['regions']=len(blocks)")
    source = replace_once(source, "assign[key]=s;assert slots[s]==signal[uses[key][0]]",
        "assign[key]=s;issue21_future_by_slot[s].append(key);assert slots[s]==signal[uses[key][0]]")
    source = replace_once(source, "assign[u]=s\n  if trace is not None and g in trace['groups']:",
        "assign[u]=s;issue21_future_by_slot[s].append(u)\n  if trace is not None and g in trace['groups']:")
    source = replace_once(source,
        "trace['groups'][g]['value_slots']={x:value_slots[x]for x in value_slots}\n",
        "trace['groups'][g]['value_slots']={x:value_slots[x]for x in value_slots}\n   trace['groups'][g]['assigned_uses']=[dict(compiler_use=u,value=uses[u][0],target_group=uses[u][1],terminal=uses[u][2],matched=u in right,slot=assign.get(u))for u in b['uses']]\n")
    source = replace_once(source,
        "idx=len(ops);op=(a,b,g);ops.append(op)\n",
        "idx=len(ops);op=(a,b,g);ops.append(op)\n  if trace is not None:trace.setdefault('global_operation_causes',Counter())[(g,cause)]+=1\n")
    source = replace_once(source,
        " if not enabled:return edges,chosen,right,stats\n # Greedy first, then exact augmenting paths in linear/partition matroid intersection.\n",
        " if not enabled:return edges,chosen,right,stats\n forced_edges=set()\n forced=globals().get('FORCE_MATCH')\n if forced is not None:\n  requests=[forced]if len(forced)==3 and isinstance(forced[0],int)else list(forced)\n  for y,carry_group,target_group in requests:\n   matches=[e for e,(g,u,i)in enumerate(edges)if g==carry_group and uses[u][0]==y and uses[u][1]==target_group]\n   assert len(matches)==1,matches\n   forced_edge=matches[0];g,u,i=edges[forced_edge];assert u not in right and can(forced_edge)\n   chosen.add(forced_edge);right[u]=forced_edge;blocks[g]['selected'].add(forced_edge);forced_edges.add(forced_edge)\n # Greedy first, then exact augmenting paths in linear/partition matroid intersection.\n")
    source = replace_once(source, "f=right[u];fg=edges[f][0]\n",
        "f=right[u]\n   if f in forced_edges:continue\n   fg=edges[f][0]\n")
    return source


def load_compiler(path: Path, source: str, forced):
    namespace = {"__name__": "issue21_focused_compiler", "__file__": str(path),
                 "__issue21_span_probe__": span_probe,
                 "__issue21_batch_span_probe__": span_probe_batch,
                 "FORCE_MATCH": forced}
    exec(compile(source, str(path) + ".issue21-instrumented", "exec"), namespace)
    return namespace


def canonical_word(word: dict) -> bytes:
    return (json.dumps(word, separators=(",", ":")) + "\n").encode()


def deterministic_gzip(data: bytes) -> bytes:
    import io
    stream = io.BytesIO()
    with gzip.GzipFile(filename="frame-word-23.json.gz", fileobj=stream,
                       mode="wb", mtime=0, compresslevel=9) as archive:
        archive.write(data)
    return stream.getvalue()


def rank_profile(word: dict, frame_tools, h: int = 23) -> dict:
    """Rebuild the rank histogram from every literal event and endpoint."""
    profile = collections.Counter()
    role_frame = {}
    for slot, old, new in word["events"]:
        new_frame = tuple(word["frames"][new])
        new_rank = frame_tools.frame_dim(new_frame)
        if old == -1:
            assert slot not in role_frame
            profile[new_rank] += 1
        else:
            assert role_frame[slot] == old
            old_frame = tuple(word["frames"][old])
            assert not (new_frame[0] & ~old_frame[0])
            assert not (old_frame[1] & ~new_frame[1])
            profile[new_rank - frame_tools.frame_dim(old_frame)] += 1
        role_frame[slot] = new
    outputs = {row[0]: row for row in word["outputs"]}
    assert len(outputs) == len(word["outputs"])
    for slot, group in role_frame.items():
        rank = frame_tools.frame_dim(tuple(word["frames"][group]))
        if slot not in outputs:
            profile[h - rank] += 1
        else:
            _, output_group, _, triple = outputs[slot]
            assert output_group == group
            if len(triple) == 1:
                profile[rank] += 1
                profile[h - rank] += 1
            else:
                profile[h - 1 - rank] += 1
                profile[1] += 1
    assert len(role_frame) == word["R"]
    assert len(role_frame) == len(set(role_frame))
    assert set(outputs) <= set(role_frame)
    return {str(k): v for k, v in sorted(profile.items())}


def role_ledger(word: dict, frame_tools, slot: int, h: int = 23) -> dict:
    rows = [(i, tuple(event)) for i, event in enumerate(word["events"]) if event[0] == slot]
    assert rows and rows[0][1][1] == -1
    frame = None
    paid = []
    for index, event in rows:
        _, old, new = event
        new_frame = tuple(word["frames"][new])
        if old == -1:
            assert frame is None
            rank = frame_tools.frame_dim(new_frame)
            kind = "allocation"
        else:
            assert frame == old
            old_frame = tuple(word["frames"][old])
            assert not (new_frame[0] & ~old_frame[0])
            assert not (old_frame[1] & ~new_frame[1])
            rank = frame_tools.frame_edge_rank(23, old_frame, new_frame)
            kind = "frame_transition"
        paid.append(dict(event_index=index, event=list(event), kind=kind,
                         exact_Q23_rank=rank))
        frame = new
    output = next((row for row in word["outputs"] if row[0] == slot), None)
    final_rank = frame_tools.frame_dim(tuple(word["frames"][frame]))
    if output is None:
        endpoint = dict(kind="retired_cleanup", group=frame, exact_Q23_rank=h-final_rank)
        endpoint_mass = h - final_rank
    else:
        _, group, common, triple = output
        rank = frame_tools.frame_dim(tuple(word["frames"][group]))
        endpoint_ranks = [rank, h-rank] if len(triple) == 1 else [h-1-rank, 1]
        endpoint = dict(kind="terminal_output", output_record=output,
                        charged_rank_bins=endpoint_ranks)
        endpoint_mass = sum(endpoint_ranks)
    return dict(slot=slot, history=paid, final_group=frame, final_frame=list(word["frames"][frame]),
        endpoint=endpoint, role_rank_mass=sum(row["exact_Q23_rank"] for row in paid)+endpoint_mass,
        scope="complete slot lifetime in this word, including post-demand reuse and its terminal/retirement endpoint")


def local_inverse_check(operations: list[dict]) -> dict:
    gates = [tuple(row["op"][:2]) for row in operations]
    slots = sorted({slot for gate in gates for slot in gate})
    index = {slot: i for i, slot in enumerate(slots)}
    local = [(index[a], index[b]) for a, b in gates]

    def apply(state, sequence):
        state = state[:]
        for target, control in sequence:
            state[target] ^= state[control]
        return state

    inverse = list(reversed(local))
    checked = 0
    for bit in range(len(slots)):
        state = [int(i == bit) for i in range(len(slots))]
        assert apply(apply(state, local), inverse) == state
        checked += 1
    return dict(status="PASS", gate_count=len(gates), touched_role_slots=slots,
                arbitrary_dirty_role_basis_vectors=checked,
                scope="local group M followed by its exact inverse; not a full word replay")


def compare_operations(baseline: dict, alternative: dict,
                       base_trace: dict, alt_trace: dict) -> dict:
    base_by_group = collections.defaultdict(list)
    alt_by_group = collections.defaultdict(list)
    for target, control, group in baseline["ops"]:
        base_by_group[group].append((target, control))
    for target, control, group in alternative["ops"]:
        alt_by_group[group].append((target, control))
    changes = []
    for group in sorted(set(base_by_group) | set(alt_by_group)):
        before, after = collections.Counter(base_by_group[group]), collections.Counter(alt_by_group[group])
        removed, added = before-after, after-before
        if removed or added:
            changes.append(dict(group=group, baseline_xors=sum(before.values()),
                alternative_xors=sum(after.values()), delta=sum(after.values())-sum(before.values()),
                removed_ops=[[a,b,n] for (a,b),n in sorted(removed.items())],
                added_ops=[[a,b,n] for (a,b),n in sorted(added.items())]))
    before_cause = base_trace["global_operation_causes"]
    after_cause = alt_trace["global_operation_causes"]
    cause_changes = []
    for group, cause in sorted(set(before_cause) | set(after_cause)):
        old, new = before_cause.get((group,cause),0), after_cause.get((group,cause),0)
        if old != new:
            cause_changes.append(dict(group=group,cause=cause,baseline=old,alternative=new,delta=new-old))
    assert sum(row["delta"] for row in changes) == len(alternative["ops"])-len(baseline["ops"])
    return dict(changed_groups=changes, changed_operation_causes=cause_changes)


def candidate_observation(trace: dict, word: dict, frame_tools, value: int,
                          source_group: int, consumer_groups: list[int], graph_uses: list[dict]) -> dict:
    source = trace["groups"][source_group]
    demand_rows = []
    for group in consumer_groups:
        target = trace["groups"][group]
        input_row = next(row for row in target["input_slots"] if row["value"] == value)
        event_row = next(row for row in target["events"]
                         if row["cause"] == "block_input" and row["event"][0] == input_row["slot"])
        slot = input_row["slot"]
        event = tuple(event_row["event"])
        exact_rank = frame_tools.frame_edge_rank(
            23, tuple(word["frames"][event[1]]), tuple(word["frames"][event[2]]))
        assert event_row["event_index"] >= 0
        demand_rows.append(dict(use_id=next(row["compiler_use"] for row in source["assigned_uses"]
                                           if row["value"] == value and row["target_group"] == group),
            consumer_group=group, input_slot=slot, block_input_event_index=event_row["event_index"],
            event=list(event), exact_Q23_rank=exact_rank,
            rank_method="exact rational projector difference"))
    copies = [row for row in source["operations"] if row["cause"] == "duplicate_use_copy"
              and row["op"][1] == source["value_slots"].get(value)]
    selected = []
    for group in consumer_groups:
        selected.extend(row for row in trace["groups"][group]["selected_edges"]
                        if row["value"] == value)
    return dict(value=value, producer_group=source_group, producer_frame=list(source["frame"]),
        producer_value_slot=source["value_slots"].get(value), graph_use_count=len(graph_uses),
        graph_uses=graph_uses,
        physical_demands=demand_rows,
        assigned_uses=[row for row in source["assigned_uses"] if row["value"] == value],
        producer_duplicate_use_copy_ops=[dict(op_index=row["op_index"], op=row["op"])
                                         for row in copies],
        outgoing_selected_carry_edges=selected,
        consumer_groups={str(g):dict(frame=trace["groups"][g]["frame"],
            rank=trace["groups"][g]["rank"], inputs=trace["groups"][g]["input_slots"],
            selected_edges=trace["groups"][g]["selected_edges"],
            focus_span=trace["groups"][g].get("focus_span")) for g in consumer_groups})


def main() -> None:
    started = time.monotonic()
    worktree = Path(sys.argv[1]).resolve()
    out = Path(__file__).resolve().parent
    fast = json.loads((out / "FAST_RECEIPT.json").read_text())
    span_only = len(sys.argv) > 2 and sys.argv[2] == "--span-only"
    all_spans = len(sys.argv) > 2 and sys.argv[2] == "--all-spans"
    span_mode = span_only or all_spans
    value = (fast["copy_finalist_summaries"][0]["value"] if all_spans else
             int(sys.argv[3] if span_only else sys.argv[2])
             if len(sys.argv) > (3 if span_only else 2) else DEFAULT_VALUE)
    candidate_rows = (fast["finalist_summaries"] + fast["copy_finalist_summaries"]
                      + fast["serial_finalist_summaries"] if span_mode
                      else fast["finalist_summaries"])
    finalist = next(row for row in candidate_rows if row["value"] == value)
    consumer_groups = sorted({row["consumer_group"] for row in finalist["physical_demands"]})
    force_all_eligible = not span_mode and len(sys.argv) > 3 and sys.argv[3] == "--all-eligible"
    if span_mode:
        carry_group = target_group = None
        forced_requests = []
    elif force_all_eligible:
        by_use = {}
        for edge in finalist["carry_screen"]["eligible_carry_edges"]:
            if not edge["target_already_matched"]:
                by_use.setdefault(edge["use_id"], (value, edge["from_group"], edge["to_group"]))
        forced_requests = list(by_use.values())
        assert len(forced_requests) >= 2
        carry_group, target_group = forced_requests[0][1:]
    elif len(sys.argv) > 4:
        carry_group, target_group = map(int, sys.argv[3:5])
        forced_requests = [(value, carry_group, target_group)]
    else:
        edge = next(row for row in finalist["carry_screen"]["eligible_carry_edges"]
                    if not row["target_already_matched"])
        carry_group, target_group = edge["from_group"], edge["to_group"]
        forced_requests = [(value, carry_group, target_group)]
    target_use = (None if span_mode else next(row for row in finalist["physical_demands"]
                      if row["consumer_group"] == target_group))
    graph_use = next(row for row in finalist["graph_uses"]
                     if row["consumer_group"] == (consumer_groups[0] if span_mode else target_group))
    issue19 = load_module("issue21_fast_helpers", out / "fast_check.py")
    pin, manifest, frozen_word = issue19.verify_sources(worktree)
    compiler_path = pin / "scripts/experiments/rank_pair_compiler.py"
    instrumented = compiler_path.read_text()
    assert sha(instrumented.encode()) == FAST_SOURCE
    runtime_source = instrument(instrumented)
    runtime_hash = sha(runtime_source.encode())
    frame_tools = load_module("issue21_issue19_frame_tools",
                              worktree / "research/real-word-provenance/run_focused.py")
    graph = load_module("issue21_focused_pair_graph", pin / "research/pair-assembly/pair_graph.py")
    base = load_compiler(compiler_path, runtime_source, None)
    base["graph"] = graph.graph
    candidate_groups = consumer_groups
    extra_groups = sorted(set(candidate_groups + [g for g in (carry_group, target_group)
                                                   if g is not None]))
    trace_spec = dict(producer=value, consumer=graph_use["consumer"], operand=graph_use["operand"],
        extra_trace_groups=extra_groups, probe_groups=[] if all_spans else candidate_groups)
    if all_spans:
        targets_by_group = collections.defaultdict(set)
        inventory = json.loads((out / "inventory.json").read_text())["values"]
        for row in inventory:
            if len(row["u"]) < 2:
                continue
            demand_groups = {use[1] for use in row["u"] if use[4] != "T"}
            if not demand_groups:
                continue
            for group in demand_groups:
                targets_by_group[group].add(row["v"])
        trace_spec["all_span_targets_by_group"] = {
            group: sorted(values) for group, values in targets_by_group.items()}

    started_compile = time.monotonic()
    baseline_result, baseline_word, baseline_trace = base["compile_"](
        23, matching=True, reclaim=True, dirty=False, trace_spec=trace_spec)
    baseline_seconds = time.monotonic() - started_compile
    baseline_raw = canonical_word(baseline_word)
    baseline_hash = sha(baseline_raw)
    baseline_gzip_hash = sha(deterministic_gzip(baseline_raw))
    checkpoint = dict(status="BASELINE_WORD_HASH_CHECKPOINT", candidate_value=value,
        pr63_commit=issue19.PR63,
        baseline_word_sha256=baseline_hash, baseline_word_gzip_sha256=baseline_gzip_hash,
        baseline_elementary_xors=baseline_result["elementary_xors"],
        baseline_roles=baseline_result["roles"], baseline_rank_mass=baseline_result["rank_mass"],
        runtime_instrumentation_sha256=runtime_hash, baseline_compile_seconds=baseline_seconds,
        peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if not span_mode:
        write_json(out / f"FOCUSED_HASH_CHECKPOINT_{value}.json", checkpoint)
    assert baseline_hash == WORD and baseline_gzip_hash == WORD_GZIP, checkpoint

    if all_spans:
        baseline_profile = rank_profile(baseline_word, frame_tools)
        assert baseline_profile == {str(k): v for k, v in sorted(
            ((int(k), v) for k, v in baseline_result["histogram"].items()))}
        rows = baseline_trace["all_span_rows"]
        expected = sum(map(len, trace_spec["all_span_targets_by_group"].values()))
        assert len(rows) == expected, (len(rows), expected)
        by_value = collections.defaultdict(list)
        for row in rows:
            by_value[row["value"]].append(row)
        hit_demands = sum(row["target_in_available_other_role_span"] for row in rows)
        hit_values = sum(any(row["target_in_available_other_role_span"] for row in value_rows)
                         for value_rows in by_value.values())
        compact_rows = [[row["value"], row["target_group"],
                         int(row["target_in_available_other_role_span"]),
                         row["eligible_other_roles"], row["retired_eligible_roles"]]
                        for row in rows]
        receipt = dict(status="PASS", phase="FAST_REGENERATION_AVAILABILITY",
            source=dict(issue19_commit=issue19.ISSUE19, issue20_result_commit=issue19.ISSUE20,
                pr63_commit=issue19.PR63, graph_sha256=issue19.GRAPH,
                compiler_sha256=issue19.COMPILER, pinned_word_sha256=WORD,
                pinned_word_gzip_sha256=WORD_GZIP,
                pinned_instrumented_compiler_sha256=FAST_SOURCE,
                runtime_instrumentation_sha256=runtime_hash),
            coverage=dict(graph_multi_values_with_multiple_physical_demand_groups=len(by_value),
                graph_multi_values_with_multiple_physical_demands=sum(len(row["u"]) >= 2 for row in inventory),
                multiple_physical_values_without_an_external_block_input=sum(len(row["u"]) >= 2 for row in inventory)-len(by_value),
                separate_demand_points=len(rows),
                span_hit_demands=hit_demands, span_hit_values=hit_values,
                definition="For each demand, screen the candidate fresh-signal form against other currently frame/future-use-eligible physical role forms, excluding direct candidate carriers."),
            baseline=dict(word_sha256=baseline_hash, word_gzip_sha256=baseline_gzip_hash,
                elementary_xors=baseline_result["elementary_xors"], roles=baseline_result["roles"],
                rank_mass=baseline_result["rank_mass"], rank_histogram=baseline_profile),
            availability_schema="Rows are [logical_value, demand_group, in_span, eligible_other_roles, retired_eligible_roles]. A span hit is a fresh-form witness screen, not a complete dirty-state reconstruction or paid schedule.",
            resources=dict(baseline_compile_seconds=baseline_seconds,
                wall_seconds=time.monotonic()-started,
                peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                free_disk_kib=__import__("shutil").disk_usage(out).free//1024))
        (out / "regeneration_availability.json").write_text(
            json.dumps(compact_rows, separators=(",", ":")) + "\n")
        write_json(out / "REGENERATION_FAST_RECEIPT.json", receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return

    if span_only:
        baseline_profile = rank_profile(baseline_word, frame_tools)
        assert baseline_profile == {str(k): v for k, v in sorted(
            ((int(k), v) for k, v in baseline_result["histogram"].items()))}
        demand_rows = []
        for group in consumer_groups:
            trace_group = baseline_trace["groups"][group]
            input_row = next(row for row in trace_group["input_slots"] if row["value"] == value)
            event_row = next(row for row in trace_group["events"]
                             if row["cause"] == "block_input" and row["event"][0] == input_row["slot"])
            event = event_row["event"]
            rank = frame_tools.frame_edge_rank(23, tuple(baseline_word["frames"][event[1]]),
                                               tuple(baseline_word["frames"][event[2]]))
            demand_rows.append(dict(use_id=next(row["use_id"] for row in finalist["physical_demands"]
                                                if row["consumer_group"] == group),
                consumer_group=group, slot=input_row["slot"], event_index=event_row["event_index"],
                event=event, exact_Q23_rank=rank))
        source_trace = baseline_trace["groups"][finalist["producer_group"]]
        local_checks = {str(g):local_inverse_check(baseline_trace["groups"][g]["operations"])
                        for g in consumer_groups}
        spans = {str(g):baseline_trace["groups"][g]["focus_span"] for g in consumer_groups}
        regen_receipt = dict(status="PASS", phase="FOCUSED_REGENERATION_SCREEN",
            source=dict(issue19_commit=issue19.ISSUE19, issue20_result_commit=issue19.ISSUE20,
                pr63_commit=issue19.PR63, graph_sha256=issue19.GRAPH,
                compiler_sha256=issue19.COMPILER, pinned_word_sha256=WORD,
                pinned_word_gzip_sha256=WORD_GZIP,
                pinned_instrumented_compiler_sha256=FAST_SOURCE,
                runtime_instrumentation_sha256=runtime_hash),
            candidate=dict(value=value, producer_group=finalist["producer_group"],
                graph_use_count=finalist["graph_use_count"], graph_uses=finalist["graph_uses"],
                physical_demands=demand_rows,
                baseline_duplicate_use_copy_xors=finalist["baseline_duplicate_use_copy_xors"],
                producer_group_duplicate_use_copy_xors=sum(
                    row["cause"] == "duplicate_use_copy" for row in source_trace["operations"])),
            physical_value_span_screen=dict(scope="fresh-signal forms carried by currently frame-eligible roles; a hit is not a dirty-state reconstruction schedule",
                per_demand=spans,
                summary=dict(demand_count=len(demand_rows), span_hits=sum(row["target_in_available_other_role_span"] for row in spans.values()),
                    min_witness_roles=min((len(row["witness"]) for row in spans.values() if row["target_in_available_other_role_span"]), default=None),
                    witness_role_counts={g:len(row["witness"]) for g,row in spans.items()})),
            baseline=dict(word_sha256=baseline_hash, word_gzip_sha256=baseline_gzip_hash,
                elementary_xors=baseline_result["elementary_xors"], roles=baseline_result["roles"],
                rank_mass=baseline_result["rank_mass"], rank_histogram=baseline_profile),
            local_dirty_checks=local_checks,
            validation=dict(baseline_canonical_hash_matches_frozen=True,
                compiler_internal_all_block_input_signal_assertions=True,
                global_scatter_assertion=True, all_frame_inclusions_asserted=True,
                local_group_M_then_inverse_all_touched_dirty_role_basis=True,
                full_global_dirty_basis_replay="NOT_RUN"),
            resources=dict(baseline_compile_seconds=baseline_seconds,
                wall_seconds=time.monotonic()-started,
                peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                free_disk_kib=__import__("shutil").disk_usage(out).free//1024))
        write_json(out / f"REGENERATION_RECEIPT_{value}.json", regen_receipt)
        print(json.dumps(regen_receipt, indent=2, sort_keys=True))
        return

    alternative = load_compiler(compiler_path, runtime_source,
        forced_requests[0] if len(forced_requests) == 1 else forced_requests)
    alternative["graph"] = graph.graph
    started_alternative = time.monotonic()
    alt_result, alt_word, alt_trace = alternative["compile_"](
        23, matching=True, reclaim=True, dirty=False, trace_spec=trace_spec)
    alternative_seconds = time.monotonic() - started_alternative
    alt_raw = canonical_word(alt_word)
    alt_hash = sha(alt_raw)
    alt_gzip_hash = sha(deterministic_gzip(alt_raw))
    assert alt_hash != baseline_hash
    checkpoint.update(dict(status="BOTH_WORD_HASHES_CHECKED", alternative_word_sha256=alt_hash,
        alternative_word_gzip_sha256=alt_gzip_hash, alternative_compile_seconds=alternative_seconds,
        peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
    write_json(out / f"FOCUSED_HASH_CHECKPOINT_{value}.json", checkpoint)

    baseline_profile = rank_profile(baseline_word, frame_tools)
    alt_profile = rank_profile(alt_word, frame_tools)
    assert baseline_profile == {str(k): v for k, v in sorted(
        ((int(k), v) for k, v in baseline_result["histogram"].items()))}
    assert alt_profile == {str(k): v for k, v in sorted(
        ((int(k), v) for k, v in alt_result["histogram"].items()))}

    baseline_candidate = candidate_observation(baseline_trace, baseline_word, frame_tools,
        value, finalist["producer_group"], candidate_groups, finalist["graph_uses"])
    alt_candidate = candidate_observation(alt_trace, alt_word, frame_tools,
        value, finalist["producer_group"], candidate_groups, finalist["graph_uses"])
    producer_base = baseline_trace["groups"][finalist["producer_group"]]
    producer_alt = alt_trace["groups"][finalist["producer_group"]]
    first_group_base = baseline_trace["groups"][carry_group]
    first_group_alt = alt_trace["groups"][carry_group]
    baseline_target = next(row for row in producer_base["assigned_uses"]
                           if row["compiler_use"] == target_use["use_id"])
    alt_target = next(row for row in producer_alt["assigned_uses"]
                      if row["compiler_use"] == target_use["use_id"])
    assert not baseline_target["matched"] and alt_target["matched"]
    assert next(row for row in alt_trace["groups"][target_group]["input_slots"]
                if row["value"] == value)["slot"] == next(
                    row for row in first_group_alt["input_slots"]
                    if row["value"] == value)["slot"]
    forced_routes = []
    for _, source_group, destination_group in forced_requests:
        use = next(row for row in finalist["physical_demands"]
                   if row["consumer_group"] == destination_group)
        base_assignment = next(row for row in producer_base["assigned_uses"]
                               if row["compiler_use"] == use["use_id"])
        alt_assignment = next(row for row in producer_alt["assigned_uses"]
                              if row["compiler_use"] == use["use_id"])
        assert not base_assignment["matched"] and alt_assignment["matched"]
        source_slot = next(row for row in alt_trace["groups"][source_group]["input_slots"]
                           if row["value"] == value)["slot"]
        destination_slot = next(row for row in alt_trace["groups"][destination_group]["input_slots"]
                                if row["value"] == value)["slot"]
        assert source_slot == destination_slot
        forced_routes.append(dict(use_id=use["use_id"], source_group=source_group,
            destination_group=destination_group, slot=source_slot,
            baseline_matched=base_assignment["matched"], forced_matched=alt_assignment["matched"]))

    affected_groups = sorted(set([finalist["producer_group"], *candidate_groups,
                                  carry_group, target_group]))
    local_checks = {}
    for label, trace in (("baseline", baseline_trace), ("forced_carry", alt_trace)):
        local_checks[label] = {str(g):local_inverse_check(trace["groups"][g]["operations"])
                               for g in affected_groups}

    # Check the competitor's changed real demand edge and the focused candidate
    # transitions by direct rational-projector subtraction.
    competitor_demands = {}
    matching_exchange = {}
    for label, word, trace in (("baseline", baseline_word, baseline_trace),
                               ("forced_carry", alt_word, alt_trace)):
        matching_exchange[label] = {str(g):trace["groups"][g]["selected_edges"]
            for g in sorted({source for _,source,_ in forced_requests})}

    carrier_ledgers = {}
    for label, word, candidate in (("baseline", baseline_word, baseline_candidate),
                                   ("forced_carry", alt_word, alt_candidate)):
        candidate_slots = sorted({row["input_slot"] for row in candidate["physical_demands"]})
        carrier_ledgers[label] = dict(
            candidate_value_carriers=[role_ledger(word, frame_tools, slot)
                                      for slot in candidate_slots])

    delta_profile = {rank: alt_profile.get(str(rank), 0) - baseline_profile.get(str(rank), 0)
                     for rank in sorted({int(k) for k in baseline_profile} | {int(k) for k in alt_profile})
                     if alt_profile.get(str(rank), 0) != baseline_profile.get(str(rank), 0)}
    operation_diff = compare_operations(baseline_word, alt_word, baseline_trace, alt_trace)
    receipt = dict(status="PASS", phase="FOCUSED", source=dict(issue19_commit=issue19.ISSUE19,
        issue20_result_commit=issue19.ISSUE20, pr63_commit=issue19.PR63,
        graph_sha256=issue19.GRAPH, compiler_sha256=issue19.COMPILER,
        pinned_word_sha256=WORD, pinned_word_gzip_sha256=WORD_GZIP,
        pinned_instrumented_compiler_sha256=FAST_SOURCE,
        runtime_instrumentation_sha256=runtime_hash),
        candidate=baseline_candidate,
        frame_control_probe={str(g):baseline_trace["groups"][g]["focus_span"]
                             for g in candidate_groups},
        carrier_role_lifetimes=carrier_ledgers,
        matching_capacity=dict(group=carry_group, target_group=target_group,
            forced_routes=forced_routes,
            input_values=[row["value"] for row in first_group_base["input_slots"]],
            output_basis_rank=len(first_group_base["output_basis"]),
            baseline_target_use=baseline_target, forced_target_use=alt_target,
            baseline_selected_edges=first_group_base["selected_edges"],
            forced_selected_edges=first_group_alt["selected_edges"],
            explanation="The forced legal edge takes one row slot in the carry block; all matched rows are listed so any displaced use remains visible."),
        matching_exchange=matching_exchange,
        baseline=dict(word_sha256=baseline_hash, word_gzip_sha256=baseline_gzip_hash,
            elementary_xors=baseline_result["elementary_xors"], roles=baseline_result["roles"],
            rank_mass=baseline_result["rank_mass"], rank_histogram=baseline_profile,
            compiler_stats=dict(baseline_result["stats"]),
            producer_group_duplicate_use_copy_xors=sum(
                row["cause"] == "duplicate_use_copy"
                for row in baseline_trace["groups"][finalist["producer_group"]]["operations"])),
        forced_carry=dict(word_sha256=alt_hash, word_gzip_sha256=alt_gzip_hash,
            forced_edge=dict(value=value, carry_group=carry_group, target_group=target_group,
                             compiler_use=target_use["use_id"]),
            forced_edges=[dict(value=y,carry_group=g,target_group=t) for y,g,t in forced_requests],
            elementary_xors=alt_result["elementary_xors"], roles=alt_result["roles"],
            rank_mass=alt_result["rank_mass"], rank_histogram=alt_profile,
            compiler_stats=dict(alt_result["stats"]),
            producer_group_duplicate_use_copy_xors=sum(
                row["cause"] == "duplicate_use_copy"
                for row in alt_trace["groups"][finalist["producer_group"]]["operations"]),
            candidate=alt_candidate),
        delta=dict(xors=alt_result["elementary_xors"]-baseline_result["elementary_xors"],
            roles=alt_result["roles"]-baseline_result["roles"],
            rank_mass=alt_result["rank_mass"]-baseline_result["rank_mass"],
            rank_histogram=delta_profile,
            terminal_output_count=len(alt_word["outputs"])-len(baseline_word["outputs"]),
            complete_child_histogram="NOT_RECOMPUTED", recurrence_moment="NOT_RECOMPUTED",
            kappa="NOT_ESTABLISHED"),
        physical_xor_ledger=operation_diff,
        local_dirty_checks=local_checks,
        validation=dict(baseline_canonical_hash_matches_frozen=True,
            alternative_is_new_word=True, compiler_internal_all_block_input_signal_assertions=True,
            global_scatter_assertion=True, all_frame_inclusions_asserted=True,
            local_group_M_then_inverse_all_touched_dirty_role_basis=True,
            full_global_dirty_basis_replay="NOT_RUN; local wrapper checks are scoped to affected groups"),
        resources=dict(baseline_compile_seconds=baseline_seconds,
            forced_carry_compile_seconds=alternative_seconds,
            wall_seconds=time.monotonic()-started,
            peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            free_disk_kib=__import__("shutil").disk_usage(out).free//1024))
    write_json(out / f"FOCUSED_RECEIPT_{value}.json", receipt)
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
