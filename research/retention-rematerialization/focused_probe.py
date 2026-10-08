#!/usr/bin/env python3
"""FOCUSED h=23 replay and retired-span screen for the real Y2048 uses."""
import argparse
import collections
import datetime
import hashlib
import importlib.util
import json
import resource
import shutil
import sys
import time
from pathlib import Path

ISSUE19 = "eaa21e97209357575ef462d189c0950b6da85e7c"
PR63 = "aa7701b68540b7863d3b66a414e4319915d6282d"
WORD = "640696dd7cd893add9d6e12d0d587956fecf113b2eff8c29547b82e5a6f3c0ad"
WORD_GZIP = "1a57c143380a063211653f1f35e7cc9710539523b0b34c90f354a0425c34bd59"
GRAPH = "3d47e89d2649c90800a276bdd0480131def50e0bdf92c122a19494b55bf17420"
COMPILER = "9984aaccf880e4840402322d76678bfddb33ce7e494af78430a43429f51b85fd"
INSTRUMENTED_COMPILER = "e2eb7063e5ca6788dd86b3c2affdc49b470efc3ba57ca89ef820e76e6843bb89"
TARGETS = (1954, 1974, 2066, 2086)
Y2048_USES = (522, 571, 801, 851)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replace_once(source: str, old: str, new: str) -> str:
    assert source.count(old) == 1, f"instrumentation anchor count: {source.count(old)} for {old!r}"
    return source.replace(old, new, 1)


def span_probe(g: int, slots: list[int], frames: list[int], retired: set[int], blocks: list[dict],
               signal: dict[int, int], contains, value: int = 2048) -> dict:
    target = signal[value]
    target_frame = blocks[g]["frame"]
    eligible = [dict(slot=s, frame_group=frames[s], form=slots[s]) for s in sorted(retired)
                if contains(blocks[frames[s]]["frame"], target_frame)]
    by_form = {}
    for row in eligible:
        if row["form"]:
            by_form.setdefault(row["form"], row)
    forms = sorted(by_form)

    basis = {}
    for i, form in enumerate(forms):
        row, expression = form, 1 << i
        while row:
            pivot = row.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = (row, expression)
                break
            old_row, old_expression = basis[pivot]
            row ^= old_row
            expression ^= old_expression
    remaining, expression = target, 0
    while remaining:
        pivot = remaining.bit_length() - 1
        if pivot not in basis:
            break
        row, roles = basis[pivot]
        remaining ^= row
        expression ^= roles
    in_span = remaining == 0
    span_roles = [by_form[forms[i]] for i in range(len(forms)) if expression >> i & 1] if in_span else []

    def witness(form_values):
        return [dict(slot=by_form[f]["slot"], frame_group=by_form[f]["frame_group"], form=f)
                for f in form_values]

    selected = None
    if in_span and target in by_form:
        selected = witness([target])
    if in_span and selected is None:
        for form in forms:
            complement = target ^ form
            if complement in by_form and form < complement:
                selected = witness([form, complement])
                break
    if in_span and selected is None:
        form_set = set(forms)
        for i, left in enumerate(forms):
            for right in forms[i + 1:]:
                third = target ^ left ^ right
                if third in form_set and third != left and third != right:
                    selected = witness([left, right, third])
                    break
            if selected is not None:
                break
    return dict(target_group=g, target_frame=target_frame, target_frame_rank=blocks[g]["rank"],
                retired_eligible_roles=len(eligible), distinct_nonzero_forms=len(forms),
                retired_span_rank=len(basis), target_in_retired_span=in_span,
                smallest_witness_up_to_three=(selected if selected is not None else None),
                one_gaussian_span_witness=span_roles if in_span else None)


def dirty_wrapper_check(word: dict) -> dict:
    actual_slots = (21455, 1078, 17581, 22506, 22507, 22508)
    local = {slot: i for i, slot in enumerate(actual_slots)}
    inputs, outputs, roles = 3, 4, len(actual_slots)
    data_width = inputs + outputs
    total = data_width + roles
    m = [(data_width + local[a], data_width + local[b])
         for a, b, g in word["ops"][75969:75976]]
    assert all(g == 1929 for a, b, g in word["ops"][75969:75976])
    carriers = (21455, 22506, 22507, 22508)
    j = [(inputs + i, data_width + local[slot]) for i, slot in enumerate(carriers)]
    v = [(data_width + local[21455], 0), (data_width + local[1078], 1),
         (data_width + local[17581], 2)]
    circuit = m + j + m[::-1] + v + m + j + m[::-1] + v

    def apply(state, gates):
        state = state[:]
        for a, b in gates:
            state[a] ^= state[b]
        return state

    forward_ok = True
    reverse_ok = True
    for bit in range(total):
        initial = [int(i == bit) for i in range(total)]
        got = apply(initial, circuit)
        expected = initial[:]
        if bit < inputs:
            for out in range(outputs):
                expected[inputs + out] ^= initial[bit]
        assert got == expected, ("forward", bit, got, expected)
        inverse = [(b, a) for a, b in reversed(circuit)]
        got_inverse = apply(initial, inverse)
        expected_inverse = initial[:]
        if inputs <= bit < inputs + outputs:
            for inp in range(inputs):
                expected_inverse[inp] ^= initial[bit]
        assert got_inverse == expected_inverse, ("inverse", bit, got_inverse, expected_inverse)
    return dict(status="PASS", input_bits=inputs, output_bits=outputs, arbitrary_dirty_role_bits=roles,
                checked_basis_vectors=total, both_orientations=True,
                operation_list="actual ops[75969..75975] inside the reversible dirty wrapper",
                wrapper_scaffolding="V seeds the three exact source inputs; J exposes the four demanded carriers",
                measured_cost=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("issue19_worktree", type=Path)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("FOCUSED_RECEIPT.json"))
    args = parser.parse_args()
    started = time.monotonic()
    started_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    root = args.issue19_worktree.resolve()
    source_data = root / "research/real-word-provenance"
    helpers = load_module("issue20_issue19_helpers", source_data / "run_focused.py")
    manifest, expected, frozen_canonical = helpers.verify_pins()
    pinned_receipt = json.loads((source_data / "FOCUSED_RECEIPT.json").read_text())
    head = __import__("subprocess").run(["git", "-C", str(root), "rev-parse", "HEAD"], check=True,
                                        capture_output=True, text=True).stdout.strip()
    assert head == ISSUE19
    assert manifest["source_commit"] == PR63
    assert manifest["files"]["research/pair-assembly/pair_graph.py"] == GRAPH
    assert manifest["files"]["scripts/experiments/rank_pair_compiler.py"] == COMPILER

    pin = source_data / "pinned"
    for name in ("partial_swap", "partial_swap.paired", "partial_swap.shared", "exclusion_circuit"):
        sys.modules.pop(name, None)
    sys.path.insert(0, str(pin / "scripts"))
    compiler_path = pin / "scripts/experiments/rank_pair_compiler.py"
    original_source = compiler_path.read_text()
    assert sha(original_source.encode()) == INSTRUMENTED_COMPILER
    source = replace_once(
        original_source,
        "target_outgoing_uses=[])",
        "target_outgoing_uses=[])\n  trace['probe_groups']=list(trace_spec.get('probe_groups', ()))\n  trace['probe_snapshots']={}\n  trace['producer_use_slots']=[]")
    source = replace_once(source, "  for g in {pg,cg}:\n",
                          "  for g in ({pg,cg} | set(trace_spec.get('probe_groups', ()))):\n")
    source = replace_once(
        source,
        " for step,g in enumerate(order):\n  b=blocks[g];outuses=[u for u in b['uses']if u not in right];outvalues=sorted({uses[u][0]for u in outuses});assert outvalues==b['outvalues']\n",
        " for step,g in enumerate(order):\n  b=blocks[g];outuses=[u for u in b['uses']if u not in right];outvalues=sorted({uses[u][0]for u in outuses});assert outvalues==b['outvalues']\n  if trace is not None and g in trace['probe_groups']:\n   trace['probe_snapshots'][g]=__issue20_span_probe__(g,slots,frames,retired,blocks,signal,contains,2048)\n")
    source = replace_once(
        source,
        "   used.add(x);assert u not in assign;assign[u]=s\n  if trace is not None and g in trace['groups']:\n",
        "   used.add(x);assert u not in assign;assign[u]=s\n  if trace is not None and g==trace['producer_group']:\n   trace['producer_use_slots']=[dict(compiler_use=u,target_group=uses[u][1],slot=assign[u]) for u in value_uses[trace['logical_use']['producer']]]\n  if trace is not None and g in trace['groups']:\n")

    compiler_ns = {"__name__": "issue20_focused_compiler", "__file__": str(compiler_path),
                   "__issue20_span_probe__": span_probe}
    exec(compile(source, str(compiler_path) + ".issue20-probe", "exec"), compiler_ns)
    graph_module = load_module("issue20_pair_graph", pin / "research/pair-assembly/pair_graph.py")
    compiler_ns["graph"] = graph_module.graph
    c, blocks, uses, value_uses, owner, signal, order, contains = compiler_ns["build"](23)
    compile_started = time.monotonic()
    _, word, trace = compiler_ns["compile_"](
        23, matching=True, reclaim=True, dirty=False,
        trace_spec=dict(producer=2048, consumer=2349, operand=0,
                        probe_groups=list(TARGETS)))
    compile_seconds = time.monotonic() - compile_started

    canonical = helpers.canonical_word(word)
    generated_hash = sha(canonical)
    generated_gzip = helpers.deterministic_gzip(canonical)
    gzip_hash = sha(generated_gzip)
    assert canonical == frozen_canonical and generated_hash == WORD
    assert gzip_hash == WORD_GZIP
    checkpoint = dict(status="WORD_HASH_CHECKPOINT", source_commit=head, pr63_commit=PR63,
                      graph_sha256=GRAPH, compiler_sha256=COMPILER, word_sha256=generated_hash,
                      word_gzip_sha256=gzip_hash, compile_seconds=compile_seconds,
                      peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    args.output.with_name("FOCUSED_HASH_CHECKPOINT.json").write_text(
        json.dumps(checkpoint, indent=2, sort_keys=True) + "\n")
    assert trace["producer_group"] == 1929
    outgoing = trace["producer_use_slots"]
    assert [(r["compiler_use"], r["target_group"]) for r in outgoing] == list(zip(Y2048_USES, TARGETS))
    assert [r["slot"] for r in outgoing] == [21455, 22506, 22507, 22508]
    assert len({r["slot"] for r in outgoing}) == 4

    frame_edges = []
    source_frame = tuple(word["frames"][1929])
    source_rank = blocks[1929]["rank"]
    for row in outgoing:
        target = row["target_group"]
        target_frame = tuple(word["frames"][target])
        event = (row["slot"], 1929, target)
        matches = [i for i, item in enumerate(word["events"]) if tuple(item) == event]
        assert len(matches) == 1
        rank = helpers.frame_edge_rank(23, source_frame, target_frame)
        assert rank == blocks[target]["rank"] - source_rank == 2
        frame_edges.append(dict(compiler_use=row["compiler_use"], slot=row["slot"], target_group=target,
                                event_index=matches[0], event=list(event), exact_Q23_rank=rank,
                                target_frame=list(target_frame), target_rank=blocks[target]["rank"]))

    # Rebuild every paid rank bin from literal events plus output/retirement endpoints.
    role_frame = {}
    profile = collections.Counter()
    for event in word["events"]:
        slot, old, new = event
        if old == -1:
            assert slot not in role_frame
            profile[blocks[new]["rank"]] += 1
        else:
            assert role_frame[slot] == old
            rank = blocks[new]["rank"] - blocks[old]["rank"]
            assert rank == blocks[new]["rank"] - blocks[old]["rank"]
            profile[rank] += 1
        role_frame[slot] = new
    output_by_slot = {row[0]: row for row in word["outputs"]}
    assert len(output_by_slot) == len(word["outputs"])
    for slot, final_group in role_frame.items():
        if slot not in output_by_slot:
            profile[23 - blocks[final_group]["rank"]] += 1
        else:
            _, group, common, triple = output_by_slot[slot]
            rank = blocks[group]["rank"]
            if len(triple) == 1:
                profile[rank] += 1
                profile[23 - rank] += 1
            else:
                profile[22 - rank] += 1
                profile[1] += 1
    expected_profile = {int(k): v for k, v in expected["compiled"]["histogram"].items()}
    assert dict(profile) == expected_profile

    role_ledger = []
    for row in outgoing:
        slot = row["slot"]
        history = []
        for index, event in enumerate(word["events"]):
            if event[0] == slot:
                history.append(dict(event_index=index, event=event))
        final_group = role_frame[slot]
        endpoint = output_by_slot.get(slot)
        role_ledger.append(dict(slot=slot, carrier_history=history, final_group=final_group,
                                 final_rank=blocks[final_group]["rank"],
                                 endpoint=(dict(kind="terminal_output", record=endpoint) if endpoint else
                                           dict(kind="retired_cleanup", rank=23-blocks[final_group]["rank"]))))

    probe_rows = []
    for target in TARGETS:
        group = trace["groups"][target]
        snap = trace["probe_snapshots"][target]
        frame = tuple(word["frames"][target])
        direct_local = not compiler_ns["independent"](
            [signal[y] for y in blocks[target]["inputs"] if y != 2048], signal[2048])
        witness = snap["smallest_witness_up_to_three"]
        if witness:
            witness_with_ranks = []
            for control in witness:
                control_frame = tuple(word["frames"][control["frame_group"]])
                witness_with_ranks.append(dict(slot=control["slot"], frame_group=control["frame_group"],
                    exact_raise_rank=helpers.frame_edge_rank(23, control_frame, frame), form_hex=hex(control["form"])))
            witness = witness_with_ranks
        probe_rows.append(dict(target_group=target, input_slots=group["input_slots"],
                               target_input_slot=next(r["slot"] for r in group["input_slots"] if r["value"] == 2048),
                               direct_local_input_reconstruction=direct_local,
                               retired_span=dict(eligible_roles=snap["retired_eligible_roles"],
                                   span_rank=snap["retired_span_rank"], target_in_span=snap["target_in_retired_span"],
                                   witness_up_to_three=witness,
                                   gaussian_witness_size=(len(snap["one_gaussian_span_witness"])
                                                          if snap["one_gaussian_span_witness"] is not None else None))))

    frame_incomparable = all(
        not contains(blocks[a]["frame"], blocks[b]["frame"])
        for a in TARGETS for b in TARGETS if a != b)
    assert frame_incomparable
    events = {tuple(row) for row in word["events"]}
    illegal_merged_edges = [(21455, 1929, 1974), (22506, 1929, 2066), (22507, 1929, 2086)]
    assert all(edge not in events for edge in illegal_merged_edges)
    assert sum(row["exact_Q23_rank"] for row in frame_edges) == 8
    local_dirty = dirty_wrapper_check(word)

    # Per-role rank bins include allocation, every frame raise, and the exact final endpoint.
    copy_ops = [i for i, op in enumerate(word["ops"]) if op[2] == 1929 and i in (75973, 75974, 75975)]
    assert copy_ops == [75973, 75974, 75975]
    receipt = dict(status="PASS", started_utc=started_utc, source=dict(issue19_commit=head,
        pr63_commit=PR63, graph_sha256=GRAPH, frozen_compiler_sha256=COMPILER,
        instrumented_compiler_sha256=INSTRUMENTED_COMPILER, runtime_instrumentation_sha256=sha(source.encode()),
        word_sha256=generated_hash, word_gzip_sha256=gzip_hash),
        baseline=dict(axis=23, compiler_xors=expected["compiled"]["elementary_xors"],
            roles=expected["compiled"]["roles"], rank_mass=expected["compiled"]["rank_mass"],
            profile_rebuilt_from_events_and_endpoints=True,
            y2048_demand_slots=[r["slot"] for r in outgoing], peak_simultaneous_y2048_roles=4,
            duplicate_use_copy_ops=copy_ops, expanded_wrapper_copy_xors=4*len(copy_ops),
            outgoing_frame_edges=frame_edges, outgoing_role_endpoints=role_ledger,
            y2048_group_operations=[dict(index=i,op=word["ops"][i]) for i in range(75969,75976)],
            local_dirty_restoration=local_dirty),
        retired_span_probes=probe_rows,
        retention=dict(one_carrier_across_child_demands="INADMISSIBLE: equal-rank destination frames are pairwise incomparable",
                       separate_carriers="BASELINE: four distinct carriers and four exact rank-2 edges"),
        pr96_negative_control=dict(status="PASS", four_distinct_source_to_child_edges=True,
            exact_rank_sum=8, invented_merged_edges_rejected=illegal_merged_edges,
            free_transition_merge="REJECTED: no matching event or shared target frame"),
        resources=dict(compile_seconds=compile_seconds,
            pinned_issue19_compile_seconds=pinned_receipt["compile_seconds"],
            runtime_seconds=time.monotonic()-started, peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            free_disk_kib_after=shutil.disk_usage(root).free//1024,
            full_h23_dirty_word_replay="NOT_RUN; exact selected-block dirty wrapper checked"))
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
