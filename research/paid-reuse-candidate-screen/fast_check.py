#!/usr/bin/env python3
"""Inventory real multi-use values in the frozen PR 63 h=23 word."""
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

PR63 = "aa7701b68540b7863d3b66a414e4319915d6282d"
ISSUE19 = "eaa21e97209357575ef462d189c0950b6da85e7c"
ISSUE20 = "e2cf064a7976566e8a9e60719c16f0c7d12160d9"
PR74 = "23468ac3867e778f54835ab66eb513934965160b"
PR74_CHECK = "2eecf5f8e4eafb3dd13dbc70b9ecc5b4e6e9a77c"
WORD = "640696dd7cd893add9d6e12d0d587956fecf113b2eff8c29547b82e5a6f3c0ad"
WORD_GZIP = "1a57c143380a063211653f1f35e7cc9710539523b0b34c90f354a0425c34bd59"
GRAPH = "3d47e89d2649c90800a276bdd0480131def50e0bdf92c122a19494b55bf17420"
COMPILER = "9984aaccf880e4840402322d76678bfddb33ce7e494af78430a43429f51b85fd"
KNOWN = (2044, 2048)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def verify_sources(root: Path):
    head = __import__("subprocess").run(
        ["git", "-C", str(root), "rev-parse", "HEAD"], check=True,
        capture_output=True, text=True).stdout.strip()
    assert head == ISSUE19, f"Issue 19 source checkout drift: {head}"
    pin = root / "research/real-word-provenance/pinned"
    manifest = json.loads((pin / "SOURCE_MANIFEST.json").read_text())
    assert manifest["source_commit"] == PR63
    for name, digest in manifest["files"].items():
        path = pin / name
        if name == "scripts/experiments/rank_pair_compiler.py":
            path = path.with_name(path.name + ".original")
        assert sha(path.read_bytes()) == digest, f"pinned source drift: {name}"
    assert manifest["files"]["research/pair-assembly/pair_graph.py"] == GRAPH
    assert manifest["files"]["scripts/experiments/rank_pair_compiler.py"] == COMPILER
    archive = pin / "research/rank-pair/frame-word-23.json.gz"
    zipped = archive.read_bytes()
    assert sha(zipped) == WORD_GZIP
    raw = gzip.decompress(zipped)
    word = json.loads(raw)
    canonical = (json.dumps(word, separators=(",", ":")) + "\n").encode()
    assert raw == canonical and sha(canonical) == WORD
    return pin, manifest, word


def main() -> None:
    started = time.monotonic()
    root = Path(sys.argv[1]).resolve()
    out = Path(__file__).resolve().parent
    pin, manifest, word = verify_sources(root)
    sys.path.insert(0, str(pin / "scripts"))
    for name in ("partial_swap", "partial_swap.paired", "partial_swap.shared", "exclusion_circuit"):
        sys.modules.pop(name, None)
    compiler_path = pin / "scripts/experiments/rank_pair_compiler.py"
    compiler = load_module("issue21_pinned_compiler", compiler_path)
    graph = load_module("issue21_pinned_pair_graph", pin / "research/pair-assembly/pair_graph.py")
    compiler.graph = graph.graph
    frame_tools = load_module("issue21_issue19_frame_tools", root / "research/real-word-provenance/run_focused.py")
    c, blocks, uses, value_uses, owner, signal, order, contains = compiler.build(23)
    edges, chosen, right, match_stats = compiler.match(blocks, uses, True)

    graph_uses: dict[int, list[dict]] = collections.defaultdict(list)
    for consumer in sorted(c.active):
        for operand, producer in enumerate(c.args[consumer] or ()):
            graph_uses[producer].append(dict(consumer=consumer, operand=operand,
                                             consumer_group=owner[consumer],
                                             same_group=owner[consumer] == owner[producer]))

    terminal_by_slot = {row[0]: row for row in word["outputs"]}
    assert len(terminal_by_slot) == len(word["outputs"])
    last_event = {}
    for i, event in enumerate(word["events"]):
        last_event[event[0]] = i
    terminal_cut = min(last_event[slot] for slot in terminal_by_slot)
    events_by_group: dict[int, list[tuple[int, list[int]]]] = collections.defaultdict(list)
    for i, event in enumerate(word["events"][:terminal_cut]):
        events_by_group[event[2]].append((i, event))

    def q23_rank_from_dimension(old_group: int, new_group: int) -> int | None:
        old = tuple(word["frames"][old_group])
        new = tuple(word["frames"][new_group])
        if not contains(blocks[old_group]["frame"], blocks[new_group]["frame"]):
            return None
        # For these pinned common-metric projectors, the exact Q23 difference
        # rank equals the nested frame-dimension increase (Issue 19 helper).
        return frame_tools.frame_dim(new) - frame_tools.frame_dim(old)

    # One compiler use is one distinct external block input; duplicate graph
    # operands inside a block have already been coalesced by build().
    input_site: dict[tuple[int, int], dict] = {}
    for gid, block in enumerate(blocks):
        if block["source"]:
            continue
        rows = events_by_group[gid][:len(block["inputs"])]
        assert len(rows) == len(block["inputs"])
        for value, (event_index, event) in zip(block["inputs"], rows):
            assert event[1] >= 0 and event[2] == gid
            rank = q23_rank_from_dimension(event[1], event[2])
            assert rank is not None
            input_site[gid, value] = dict(slot=event[0], event_index=event_index,
                                          event=event, exact_Q23_rank=rank,
                                          rank_method="exact pinned Q23 frame-dimension identity")

    terminal_site: dict[int, dict] = {}
    for use_id, (value, gid, terminal) in enumerate(uses):
        if terminal is None:
            continue
        rows = [row for row in word["outputs"]
                if row[1] == gid and row[2] == terminal[0]
                and tuple(row[3]) == tuple(terminal[1])]
        assert len(rows) == 1
        terminal_site[use_id] = dict(slot=rows[0][0], group=gid,
                                     output_record=rows[0], terminal_endpoint=True)

    place = {gid: i for i, gid in enumerate(order)}
    inventory = []
    counters = collections.Counter()
    demand_hist = collections.Counter()
    path_hist = collections.Counter()
    candidate_rankings = []
    for value in sorted(graph_uses):
        occurrences = graph_uses[value]
        if len(occurrences) < 2:
            continue
        producer_group = owner[value]
        demand_rows = []
        for use_id in value_uses.get(value, ()):
            _, gid, terminal = uses[use_id]
            if terminal is None:
                site = input_site[gid, value]
                demand_rows.append(dict(use_id=use_id, consumer_group=gid, terminal=None,
                    matched=use_id in right, carrier_slot=site["slot"],
                    event_index=site["event_index"], event=site["event"],
                    exact_Q23_rank=site["exact_Q23_rank"]))
            else:
                site = terminal_site[use_id]
                demand_rows.append(dict(use_id=use_id, consumer_group=gid,
                    terminal=terminal, matched=use_id in right,
                    carrier_slot=site["slot"], output_record=site["output_record"],
                    endpoint="terminal output; charged in the output profile"))
        demand_hist[len(demand_rows)] += 1
        groups = sorted({r["consumer_group"] for r in demand_rows if r["terminal"] is None},
                        key=place.__getitem__)
        frames = [tuple(word["frames"][gid]) for gid in groups]
        source_frame = tuple(word["frames"][producer_group])
        transitions = []
        chain = [producer_group, *groups]
        for a, b in zip(chain, chain[1:]):
            old, new = tuple(word["frames"][a]), tuple(word["frames"][b])
            rank = q23_rank_from_dimension(a, b)
            compatible = contains(blocks[a]["frame"], blocks[b]["frame"])
            transitions.append(dict(old_group=a, new_group=b,
                                    old_rank=blocks[a]["rank"], new_rank=blocks[b]["rank"],
                                    compatible=compatible,
                                    exact_Q23_rank=rank,
                                    rank_method=("exact pinned Q23 frame-dimension identity"
                                                 if compatible else "UNDEFINED: incompatible frames")))
        direct = all(contains(blocks[producer_group]["frame"], blocks[gid]["frame"])
                     for gid in groups)
        serial = bool(groups) and all(row["compatible"] for row in transitions)
        pairwise = all(contains(blocks[a]["frame"], blocks[b]["frame"])
                       for a, b in zip(groups, groups[1:]))
        multi_group_path = len(groups) >= 2 and serial and not any(
            r["terminal"] is not None for r in demand_rows)
        unmatched = sum(not row["matched"] for row in demand_rows)
        baseline_copy_xors = max(0, unmatched - 1)
        slots = sorted({r["carrier_slot"] for r in demand_rows})
        same_group_occurrences = sum(row["same_group"] for row in occurrences)
        cross_group_by_group = collections.Counter(row["consumer_group"] for row in occurrences
                                                   if not row["same_group"])
        assert len([r for r in demand_rows if r["terminal"] is None]) == len(cross_group_by_group)
        row = dict(value=value, producer_group=producer_group,
            producer_frame=list(source_frame), producer_frame_rank=blocks[producer_group]["rank"],
            graph_use_count=len(occurrences), graph_uses=occurrences,
            same_group_graph_uses=same_group_occurrences,
            graph_uses_coalesced_by_consumer_group=sum(max(0, n - 1)
                                                       for n in cross_group_by_group.values()),
            compiler_demand_count=len(demand_rows), physical_demands=demand_rows,
            distinct_demand_groups=len(groups), distinct_carrier_slots=len(slots),
            carrier_slots=slots, matched_demand_count=len(demand_rows) - unmatched,
            unmatched_demand_count=unmatched,
            baseline_duplicate_use_copy_xors=baseline_copy_xors,
            retention_screen=dict(source_to_each_consumer_compatible=direct,
                serial_frame_chain_compatible=serial, pairwise_demand_frames_compatible=pairwise,
                terminal_use_present=any(r["terminal"] is not None for r in demand_rows),
                transitions=transitions,
                result=("SERIAL_FRAME_PATH" if serial else "NO_SINGLE_CARRIER_FRAME_PATH")),
            recursive_child_relation="NOT_SHOWN: graph/compiler block groups are not a Section 4 call identity")
        inventory.append(row)
        counters["graph_multi_value_count"] += 1
        if len(demand_rows) >= 2:
            counters["physical_multi_demand_count"] += 1
        else:
            counters["graph_multi_but_one_physical_demand"] += 1
        if len(groups) >= 2 and not any(r["terminal"] is not None for r in demand_rows):
            counters["multiple_external_group_values"] += 1
            if multi_group_path:
                counters["serial_multi_group_path_count"] += 1
            else:
                counters["multi_group_frame_path_rejected_count"] += 1
        else:
            counters["single_group_or_terminal_only_values"] += 1
        if serial:
            counters["serial_frame_path_count"] += 1
        if multi_group_path:
            if baseline_copy_xors:
                counters["serial_with_copy_opportunity_count"] += 1
                candidate_rankings.append((baseline_copy_xors, len(demand_rows),
                                           len(occurrences), -value, value))
        if not serial:
            counters["frame_path_rejected_count"] += 1
        if any(r["terminal"] is not None for r in demand_rows):
            counters["terminal_demand_present_count"] += 1
        path_hist["serial" if serial else "nonserial"] += 1

    assert counters["graph_multi_value_count"] == 16137
    assert counters["physical_multi_demand_count"] == 15102
    assert counters["serial_multi_group_path_count"] == 4466, dict(counters)
    assert counters["serial_with_copy_opportunity_count"] == 220, dict(counters)
    candidate_rankings.sort(reverse=True)
    serial_finalists = [row[-1] for row in candidate_rankings[:3]]
    by_value = {row["value"]: row for row in inventory}
    # A complete serial path is too restrictive: a value can be copied for
    # earlier branches and still be carried across a later compatible pair.
    # Count exact compiler candidate edges which could carry an otherwise
    # unmatched use, before cross-edge matching capacity is charged.
    carry_edges: dict[int, list[dict]] = collections.defaultdict(list)
    for gid, block in enumerate(blocks):
        for use_id, input_index in block["candidates"]:
            value, target_group, terminal = uses[use_id]
            if value not in by_value or terminal is not None:
                continue
            new_frame = tuple(word["frames"][target_group])
            rank = q23_rank_from_dimension(gid, target_group)
            assert rank is not None
            carry_edges[value].append(dict(from_group=gid, to_group=target_group,
                use_id=use_id, input_index=input_index, target_already_matched=use_id in right,
                exact_Q23_rank=rank, old_rank=blocks[gid]["rank"],
                new_rank=blocks[target_group]["rank"]))
    broad_rankings = []
    for row in inventory:
        value = row["value"]
        edges_for_value = carry_edges.get(value, [])
        open_targets = sorted({edge["use_id"] for edge in edges_for_value
                               if not edge["target_already_matched"]})
        unmatched = row["unmatched_demand_count"]
        copy_bound = min(row["baseline_duplicate_use_copy_xors"], len(open_targets))
        broad_rankings.append((copy_bound, len(open_targets),
            row["baseline_duplicate_use_copy_xors"], row["compiler_demand_count"], -value, value))
        row["carry_screen"] = dict(eligible_carry_edge_count=len(edges_for_value),
            unmatched_target_uses_with_eligible_edge=len(open_targets),
            optimistic_duplicate_copy_saving_bound=copy_bound,
            eligible_carry_edges=edges_for_value)
    broad_rankings.sort(reverse=True)
    broad_finalists = [row[-1] for row in broad_rankings[:3]]
    copy_rankings = sorted((row["baseline_duplicate_use_copy_xors"],
                            row["unmatched_demand_count"], row["compiler_demand_count"],
                            -row["value"], row["value"])
                           for row in inventory
                           if row["distinct_demand_groups"] >= 2
                           and not row["retention_screen"]["terminal_use_present"])
    copy_rankings.reverse()
    copy_finalists = [row[-1] for row in copy_rankings[:3]]
    finalists = list(dict.fromkeys([*broad_finalists, *serial_finalists]))
    finalists = finalists[:3]
    for value in finalists:
        for edge in by_value[value]["carry_screen"]["eligible_carry_edges"]:
            exact = frame_tools.frame_edge_rank(23,
                tuple(word["frames"][edge["from_group"]]),
                tuple(word["frames"][edge["to_group"]]))
            assert exact == edge["exact_Q23_rank"]
            edge["rational_projector_check"] = "PASS"
    assert 2525 in serial_finalists
    assert 2048 in by_value
    assert by_value[2048]["compiler_demand_count"] == 4
    y2_graph_uses = graph_uses.get(2044, [])
    assert len(y2_graph_uses) == 1 and value_uses.get(2044, []) == []
    max_copy = max((row["baseline_duplicate_use_copy_xors"] for row in inventory
                    if row["retention_screen"]["serial_frame_chain_compatible"]), default=0)
    assert max_copy == 1
    for value in set(finalists) | {2048}:
        for demand in by_value[value]["physical_demands"]:
            if "event" not in demand:
                continue
            _, old_group, new_group = demand["event"]
            exact = frame_tools.frame_edge_rank(
                23, tuple(word["frames"][old_group]), tuple(word["frames"][new_group]))
            assert exact == demand["exact_Q23_rank"]
            demand["rational_projector_check"] = "PASS"
        for transition in by_value[value]["retention_screen"]["transitions"]:
            if not transition["compatible"]:
                continue
            exact = frame_tools.frame_edge_rank(
                23, tuple(word["frames"][transition["old_group"]]),
                tuple(word["frames"][transition["new_group"]]))
            assert exact == transition["exact_Q23_rank"]
            transition["rational_projector_check"] = "PASS"

    summary = dict(status="PASS", phase="FAST", source=dict(issue19_commit=ISSUE19,
        issue20_result_commit=ISSUE20, pr63_commit=PR63, graph_sha256=GRAPH,
        compiler_sha256=COMPILER, word_sha256=WORD, word_gzip_sha256=WORD_GZIP,
        issue19_source_manifest_files=len(manifest["files"]), pr74_historical_pin=PR74,
        pr74_selected_verification_pin=PR74_CHECK),
        universe=dict(active_graph_nodes=len(c.active), compiler_blocks=len(blocks),
            graph_values_with_uses=len(graph_uses), graph_operand_occurrences=sum(map(len, graph_uses.values())),
            compiler_use_points=len(uses), word_physical_xors=len(word["ops"]),
            word_roles=word["R"], word_frame_events=len(word["events"])),
        counts=dict(counters), physical_demand_histogram={str(k): v for k, v in sorted(demand_hist.items())},
        serial_screen=dict(max_baseline_duplicate_use_copy_xors=max_copy,
            multi_group_path_count=counters["serial_multi_group_path_count"],
            serial_with_copy_opportunity_count=counters["serial_with_copy_opportunity_count"],
            interpretation="A screen only; it does not prove role availability after consumer synthesis."),
        candidate_ranking=dict(serial_finalists=serial_finalists,
            broad_finalists=broad_finalists, copy_finalists=copy_finalists,
            focused_values=finalists,
            interpretation="Compiler candidate edges are frame-legal and independent of the block output basis, but may require a matching exchange or another competing row to move; the copy bound is optimistic. Joint exchanges, physical role lifetimes, reconstruction and endpoints remain to be charged."),
        known_controls=dict(Y2_2044=dict(graph_uses=y2_graph_uses,
            compiler_demand_count=0, result="NO_REUSE_DEMAND"),
            Y2048=by_value[2048]),
        finalist_values=finalists,
        finalist_summaries=[by_value[y] for y in finalists],
        serial_finalist_summaries=[by_value[y] for y in serial_finalists],
        copy_finalist_summaries=[by_value[y] for y in copy_finalists],
        resources=dict(wall_seconds=time.monotonic() - started,
            peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
    compact_values = []
    for row in inventory:
        frame_groups = {row["producer_group"]}
        frame_groups.update(use["consumer_group"] for use in row["graph_uses"])
        frame_groups.update(use["consumer_group"] for use in row["physical_demands"])
        physical = []
        for use in row["physical_demands"]:
            if use["terminal"] is None:
                physical.append([use["use_id"], use["consumer_group"], int(use["matched"]),
                    use["carrier_slot"], use["event_index"], use["event"][1],
                    use["exact_Q23_rank"]])
            else:
                physical.append([use["use_id"], use["consumer_group"], int(use["matched"]),
                    use["carrier_slot"], "T", use["terminal"][0], list(use["terminal"][1])])
        compact_values.append(dict(
            v=row["value"],
            p=[row["producer_group"], row["producer_frame"], row["producer_frame_rank"]],
            f=[[g, word["frames"][g][0], word["frames"][g][1], blocks[g]["rank"]]
               for g in sorted(frame_groups)],
            g=[[use["consumer"], use["operand"], use["consumer_group"], int(use["same_group"])]
               for use in row["graph_uses"]],
            u=physical,
            s=row["carrier_slots"],
            z=[row["graph_uses_coalesced_by_consumer_group"], row["distinct_demand_groups"],
               row["distinct_carrier_slots"], row["matched_demand_count"],
               row["unmatched_demand_count"], row["baseline_duplicate_use_copy_xors"]],
            r=[int(row["retention_screen"]["source_to_each_consumer_compatible"]),
               int(row["retention_screen"]["serial_frame_chain_compatible"]),
               int(row["retention_screen"]["pairwise_demand_frames_compatible"]),
               int(row["retention_screen"]["terminal_use_present"])],
            t=[[edge["old_group"], edge["new_group"], int(edge["compatible"]), edge["exact_Q23_rank"]]
               for edge in row["retention_screen"]["transitions"]]))
    inventory_document = dict(summary=summary, schema=dict(
        v="logical producer node", p="producer [group,core-mask/cover-mask,rank]",
        f="observed group frame labels [group,core-mask,cover-mask,rank]",
        g="graph use occurrences [consumer-node,operand,consumer-group,same-group]",
        u="physical demand [use-id,group,matched,carrier-slot,event-index,old-group,Q23-rank]; terminal uses store T,common,triple",
        s="observed carrier slots", z="coalesced-graph-uses,physical-groups,carrier-slots,matched,unmatched,baseline-copy-XORs",
        r="source compatibility,serial path,pairwise path,terminal use flags",
        t="retention frame transitions [old-group,new-group,compatible,Q23-rank]"),
        values=compact_values)
    (out / "inventory.json").write_text(json.dumps(inventory_document, separators=(",", ":")) + "\n")
    (out / "FAST_RECEIPT.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
