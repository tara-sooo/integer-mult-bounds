#!/usr/bin/env python3
"""FAST source and frame checks for the pinned h=23 retention candidate."""
import argparse
import gzip
import hashlib
import importlib.util
import json
import resource
import subprocess
import sys
import time
from pathlib import Path

ISSUE19 = "eaa21e97209357575ef462d189c0950b6da85e7c"
PR63 = "aa7701b68540b7863d3b66a414e4319915d6282d"
WORD = "640696dd7cd893add9d6e12d0d587956fecf113b2eff8c29547b82e5a6f3c0ad"
WORD_GZIP = "1a57c143380a063211653f1f35e7cc9710539523b0b34c90f354a0425c34bd59"
GRAPH = "3d47e89d2649c90800a276bdd0480131def50e0bdf92c122a19494b55bf17420"
COMPILER = "9984aaccf880e4840402322d76678bfddb33ce7e494af78430a43429f51b85fd"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    started = time.monotonic()
    parser = argparse.ArgumentParser()
    parser.add_argument("issue19_worktree", type=Path)
    args = parser.parse_args()
    root = args.issue19_worktree.resolve()
    head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], check=True,
                          capture_output=True, text=True).stdout.strip()
    assert head == ISSUE19, f"Issue 19 source must be pinned at {ISSUE19}, found {head}"

    data = root / "research/real-word-provenance"
    trace = json.loads((data / "TRACE.json").read_text())
    raw_trace = json.loads((data / "FOCUSED_RAW_TRACE.json").read_text())
    receipt = json.loads((data / "WORD_HASH_RECEIPT.json").read_text())
    assert trace["source"]["pr63_commit"] == PR63
    assert trace["source"]["graph_sha256"] == GRAPH
    assert trace["source"]["frozen_compiler_sha256"] == COMPILER
    assert trace["source"]["word_sha256"] == WORD
    assert trace["source"]["word_gzip_sha256"] == WORD_GZIP
    frozen_gzip = (data / "pinned/research/rank-pair/frame-word-23.json.gz").read_bytes()
    frozen_raw = gzip.decompress(frozen_gzip)
    assert sha(frozen_gzip) == WORD_GZIP
    assert sha(frozen_raw) == WORD
    assert receipt["canonical_json_bytes_identical"] is True
    assert receipt["deterministic_gzip_matches_frozen"] is True

    pin = data / "pinned"
    for name in ("partial_swap", "partial_swap.paired", "partial_swap.shared", "exclusion_circuit"):
        sys.modules.pop(name, None)
    sys.path.insert(0, str(pin / "scripts"))
    compiler_path = pin / "scripts/experiments/rank_pair_compiler.py.original"
    compiler_ns = {"__name__": "issue20_pinned_compiler", "__file__": str(compiler_path)}
    exec(compile(compiler_path.read_text(), str(compiler_path), "exec"), compiler_ns)
    graph_path = pin / "research/pair-assembly/pair_graph.py"
    graph = load_module("issue20_pinned_pair_graph", graph_path).graph
    compiler_ns["graph"] = graph
    c, blocks, uses, value_uses, owner, signal, order, contained = compiler_ns["build"](23)
    focused = load_module("issue19_focused_helpers", data / "run_focused.py")

    def graph_uses(node: int) -> list[dict]:
        return [dict(consumer=y, operand=i, consumer_group=owner[y], same_group=owner[y] == owner[node])
                for y in sorted(c.active) for i, value in enumerate(c.args[y] or ()) if value == node]

    y2_uses = graph_uses(2044)
    y2_compiler_uses = value_uses[2044]
    assert y2_uses == [dict(consumer=2048, operand=1, consumer_group=1929, same_group=True)]
    assert y2_compiler_uses == []

    y_uses = graph_uses(2048)
    expected_uses = [(522, 2048, 1954, None), (571, 2048, 1974, None),
                     (801, 2048, 2066, None), (851, 2048, 2086, None)]
    assert [(u, *uses[u]) for u in value_uses[2048]] == expected_uses
    assert len(y_uses) == 4

    source_group = owner[2048]
    assert source_group == 1929
    source_frame = blocks[source_group]["frame"]
    source_rank = blocks[source_group]["rank"]
    copy_ops = [r for r in trace["operations"]
                if r["frame_group"] == source_group and r["cause"] == "duplicate_use_copy"]
    assert [r["index"] for r in copy_ops] == [75973, 75974, 75975]
    word = json.loads(frozen_raw)
    assert [word["ops"][i] for i in range(75969, 75976)] == [
        [21455, 17581, 1929], [17581, 1078, 1929], [21455, 1078, 1929],
        [17581, 21455, 1929], [22506, 21455, 1929], [22507, 21455, 1929], [22508, 21455, 1929]
    ]

    outgoing_slots = [21455, 22506, 22507, 22508]
    demands = []
    for (use_id, value, target, terminal), slot in zip(expected_uses, outgoing_slots):
        assert value == 2048 and terminal is None
        target_frame = blocks[target]["frame"]
        target_rank = blocks[target]["rank"]
        event = (slot, source_group, target)
        matches = [i for i, row in enumerate(word["events"]) if tuple(row) == event]
        assert len(matches) == 1, (use_id, slot, target, matches)
        old_frame = tuple(word["frames"][source_group])
        new_frame = tuple(word["frames"][target])
        assert old_frame == tuple(source_frame) and new_frame == tuple(target_frame)
        edge_rank = focused.frame_edge_rank(23, old_frame, new_frame)
        assert edge_rank == target_rank - source_rank == 2
        demands.append(dict(compiler_use=use_id, consumer_group=target, carrier_slot=slot,
                            event_index=matches[0], event=list(event), frame=target_frame,
                            frame_rank=target_rank, exact_Q23_edge_rank=edge_rank,
                            local_input_reconstruction=not compiler_ns["independent"](
                                [signal[y] for y in blocks[target]["inputs"] if y != 2048], signal[2048])))

    # Replay the frozen word to screen every frame-compatible, future-compatible role.
    terminal_by_slot = {row[0]: row for row in word["outputs"]}
    last_event = {}
    for i, event in enumerate(word["events"]):
        last_event[event[0]] = i
    terminal_cut = min(last_event[s] for s in terminal_by_slot)
    events_by_group = {}
    for i, event in enumerate(word["events"][:terminal_cut]):
        events_by_group.setdefault(event[2], []).append((i, event))
    uses_by_slot = {}
    input_slot = {}
    for gid, block in enumerate(blocks):
        if block["source"]:
            continue
        rows = events_by_group[gid][:len(block["inputs"])]
        assert len(rows) == len(block["inputs"])
        for value, (_, event) in zip(block["inputs"], rows):
            assert event[1] >= 0 and event[2] == gid
            slot = event[0]
            input_slot[gid, value] = slot
            uses_by_slot.setdefault(slot, []).append((gid, value))

    ops_by_group = {}
    for op in word["ops"]:
        ops_by_group.setdefault(op[2], []).append(op)
    order_position = {gid: i for i, gid in enumerate(order)}
    forms = [0] * word["R"]
    frames = [None] * word["R"]
    allocated = set()
    all_role_screens = []
    y2048_slots = set(outgoing_slots)
    for gid in order:
        block = blocks[gid]
        if gid in (1954, 1974, 2066, 2086):
            target_frame = block["frame"]
            compatible = []
            retired_count = 0
            for slot in allocated:
                old_group = frames[slot]
                if old_group is None or slot in y2048_slots or forms[slot] == signal[2048]:
                    continue
                if not contained(blocks[old_group]["frame"], target_frame):
                    continue
                future = [use_group for use_group, _ in uses_by_slot.get(slot, ())
                          if order_position[use_group] >= order_position[gid]]
                if any(use_group != gid and not contained(target_frame, blocks[use_group]["frame"])
                       for use_group in future):
                    continue
                if slot in terminal_by_slot and not contained(
                        target_frame, blocks[terminal_by_slot[slot][1]]["frame"]):
                    continue
                compatible.append((slot, forms[slot]))
                if not future and slot not in terminal_by_slot:
                    retired_count += 1
            basis = {}
            for _, form in compatible:
                row = form
                while row:
                    pivot = row.bit_length() - 1
                    if pivot not in basis:
                        basis[pivot] = row
                        break
                    row ^= basis[pivot]
            remaining = signal[2048]
            while remaining and remaining.bit_length() - 1 in basis:
                remaining ^= basis[remaining.bit_length() - 1]
            all_role_screens.append(dict(target_group=gid, available_other_roles=len(compatible),
                retired_roles=retired_count, live_future_compatible_roles=len(compatible)-retired_count,
                span_rank=len(basis), y2048_in_span=remaining == 0,
                conclusion=("NO_COMPATIBLE_CONTROL_SPAN" if remaining else "SPAN_EXISTS_REQUIRES_PAID_SCHEDULE")))
            assert input_slot[gid, 2048] in y2048_slots

        if block["source"]:
            source_node = block["nodes"][0]
            source_slot = int(word["sources"][str(source_node - 1)])
            forms[source_slot] = signal[source_node]
        for target, control, _ in ops_by_group.get(gid, ()):
            forms[target] ^= forms[control]
        for _, event in events_by_group.get(gid, ()):
            slot, old, new = event
            if old == -1:
                assert slot not in allocated
                allocated.add(slot)
                frames[slot] = new
            else:
                assert slot in allocated and frames[slot] == old
                frames[slot] = new
    assert len(allocated) == word["R"]
    assert all(not row["y2048_in_span"] for row in all_role_screens)

    comparable = {}
    for left in demands:
        for right in demands:
            a, b = tuple(left["frame"]), tuple(right["frame"])
            comparable[f"{left['consumer_group']}->{right['consumer_group']}"] = bool(contained(a, b))
    assert all(not comparable[f"{a['consumer_group']}->{b['consumer_group']}"]
               for a in demands for b in demands if a["consumer_group"] != b["consumer_group"])
    assert all(not row["local_input_reconstruction"] for row in demands)

    result = dict(status="PASS", source=dict(issue19_commit=head, pr63_commit=PR63, graph_sha256=GRAPH,
                  compiler_sha256=COMPILER, word_sha256=WORD, word_gzip_sha256=WORD_GZIP),
                  y2=dict(node=2044, graph_uses=y2_uses, cross_group_or_terminal_uses=y2_compiler_uses,
                          conclusion="NO_REUSE_DEMAND_FOR_Y2"),
                  fallback=dict(node=2048, graph_uses=y_uses, physical_copy_ops=[r["index"] for r in copy_ops],
                                demands=demands, pairwise_frame_containment=comparable,
                                one_carrier_retention="INADMISSIBLE: distinct equal-rank child frames are incomparable",
                                same_child_input_reconstruction="INADMISSIBLE: 2048 is independent of the other block inputs",
                                compatible_role_span_screens=all_role_screens,
                                retired_span_reconstruction="NO_ADMISSIBLE_CONTROL_SPAN"),
                  resources=dict(wall_seconds=time.monotonic() - started,
                                 peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
