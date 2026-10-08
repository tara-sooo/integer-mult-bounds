#!/usr/bin/env python3
"""Tiny schema negative controls; fixture rows are not pinned word events."""
from copy import deepcopy
from fractions import Fraction as Q

if not __debug__:
    raise ValueError("Assertions must remain enabled")

GRAPH_SHA256 = "3d47e89d2649c90800a276bdd0480131def50e0bdf92c122a19494b55bf17420"
COMPILER_SHA256 = "9984aaccf880e4840402322d76678bfddb33ce7e494af78430a43429f51b85fd"
USE_FSA = "fixture:use:h23:producer=2039:consumer=2044:operand=0"
USE_SB2 = "fixture:use:h23:producer=2020:consumer=2044:operand=1"
USE_Y2 = "fixture:use:h23:producer=2044:consumer=2048:operand=1"
GROUP = "fixture:frame-group:Y2"
EXPECTED_COUNTS = {"raise": 2, "copy": 2, "xor": 2, "scatter": 1, "clear": 2}
ORIENTATIONS = {"forward", "reverse-complement"}


def fixture():
    events = []
    for orientation in sorted(ORIENTATIONS):
        prefix = f"fixture:{orientation}"
        source = f"{prefix}:slot:FSa"
        control = f"{prefix}:slot:Sb2"
        out_a = f"{prefix}:slot:carrier-a"
        out_b = f"{prefix}:slot:carrier-b"
        rows = [
            ("raise", {"slot": source, "from": "fixture:F_FSa", "to": GROUP}),
            ("raise", {"slot": control, "from": "fixture:F_Sb2", "to": GROUP}),
            ("copy", {"source_slot": source, "target_slot": out_a,
                      "carrier": f"{prefix}:carrier:a", "frame": GROUP}),
            ("xor", {"target_slot": out_a, "control_slot": control,
                     "carrier": f"{prefix}:carrier:a", "frame": GROUP,
                     "node": 2044, "use": USE_FSA}),
            ("copy", {"source_slot": source, "target_slot": out_b,
                      "carrier": f"{prefix}:carrier:b", "frame": GROUP}),
            ("xor", {"target_slot": out_b, "control_slot": control,
                     "carrier": f"{prefix}:carrier:b", "frame": GROUP,
                     "node": 2044, "use": USE_FSA}),
            ("scatter", {"slot": out_b, "frame": GROUP, "use": USE_Y2}),
            ("clear", {"slot": out_a, "frame": GROUP}),
            ("clear", {"slot": out_b, "frame": GROUP}),
        ]
        for seq, (kind, fields) in enumerate(rows):
            events.append({"fixture_event_ref": f"{prefix}:row:{seq}",
                           "orientation": orientation, "seq": seq,
                           "kind": kind, **fields})
    return {"fixture_only": True, "graph_sha256": GRAPH_SHA256,
            "compiler_sha256": COMPILER_SHA256, "production_word_sha256": "UNRESOLVED",
            "production_event_ref": "UNRESOLVED", "trace_confidence": "FIXTURE_ONLY",
            "selected_use": USE_FSA,
            "events": events}


def validate(trace):
    assert trace["fixture_only"] is True
    assert trace["graph_sha256"] == GRAPH_SHA256
    assert trace["compiler_sha256"] == COMPILER_SHA256
    assert trace["production_word_sha256"] == "UNRESOLVED"
    assert trace["production_event_ref"] == "UNRESOLVED"
    assert trace["trace_confidence"] == "FIXTURE_ONLY"
    events = trace["events"]
    assert {e["orientation"] for e in events} == ORIENTATIONS
    assert len({e["fixture_event_ref"] for e in events}) == len(events)

    for orientation in ORIENTATIONS:
        rows = [e for e in events if e["orientation"] == orientation]
        assert [e["seq"] for e in rows] == list(range(9))
        assert {kind: sum(e["kind"] == kind for e in rows)
                for kind in EXPECTED_COUNTS} == EXPECTED_COUNTS
        selected_node_xors = [e for e in rows if e["kind"] == "xor" and e.get("node") == 2044]
        assert len(selected_node_xors) == 2  # The fixture rejects a one-node/one-XOR rule.
        assert len(selected_node_xors) != 1
        prefix = f"fixture:{orientation}"
        frames = {f"{prefix}:slot:FSa": "fixture:F_FSa",
                  f"{prefix}:slot:Sb2": "fixture:F_Sb2",
                  f"{prefix}:slot:carrier-a": None,
                  f"{prefix}:slot:carrier-b": None}
        carriers = {f"{prefix}:carrier:a": f"{prefix}:slot:carrier-a",
                    f"{prefix}:carrier:b": f"{prefix}:slot:carrier-b"}
        for event in rows:
            kind = event["kind"]
            if kind == "raise":
                assert frames[event["slot"]] == event["from"]
                assert event["to"] == GROUP
                frames[event["slot"]] = event["to"]
            elif kind == "copy":
                assert frames[event["source_slot"]] == event["frame"] == GROUP
                assert frames[event["target_slot"]] is None
                assert carriers[event["carrier"]] == event["target_slot"]
                frames[event["target_slot"]] = event["frame"]
            elif kind == "xor":
                assert event["target_slot"] != event["control_slot"]
                assert frames[event["target_slot"]] == frames[event["control_slot"]] == event["frame"] == GROUP
                assert carriers[event["carrier"]] == event["target_slot"]
                assert event["node"] == 2044 and event["use"] == trace["selected_use"]
            elif kind == "scatter":
                assert frames[event["slot"]] == event["frame"] == GROUP
                assert event["use"] == USE_Y2
            else:
                assert kind == "clear" and frames[event["slot"]] == event["frame"] == GROUP
                frames[event["slot"]] = None

    # These are source-local logical frame ranks, not costs assigned to fixture rows.
    ranks = (Q(14) - Q(10), Q(14) - Q(10), Q(14) - Q(14))
    assert ranks == (Q(4), Q(4), Q(0))


def rejects(trace):
    try:
        validate(trace)
    except (AssertionError, KeyError):
        return
    raise AssertionError("negative control unexpectedly passed")


def main():
    trace = fixture()
    validate(trace)

    wrong = deepcopy(trace)
    next(e for e in wrong["events"] if e["kind"] == "xor")["use"] = USE_SB2
    rejects(wrong)  # Wrong operand-use identity.
    wrong = deepcopy(trace)
    xor = next(e for e in wrong["events"] if e["kind"] == "xor")
    xor["control_slot"] = xor["target_slot"]
    rejects(wrong)  # Swapped/aliased physical slots.
    wrong = deepcopy(trace)
    next(e for e in wrong["events"] if e["kind"] == "xor")["frame"] = "fixture:wrong-group"
    rejects(wrong)  # Wrong frame or group.
    wrong = deepcopy(trace)
    next(e for e in wrong["events"] if e["kind"] == "xor")["carrier"] = "fixture:stale-carrier"
    rejects(wrong)  # Stale matching/carrier assignment.
    for omitted in ("raise", "copy", "clear", "scatter"):
        wrong = deepcopy(trace)
        index = next(i for i, e in enumerate(wrong["events"]) if e["kind"] == omitted)
        wrong["events"].pop(index)
        rejects(wrong)  # Omitted charged or output event.
    wrong = deepcopy(trace)
    wrong["events"] = [e for e in wrong["events"] if e["orientation"] != "reverse-complement"]
    rejects(wrong)  # Missing reverse-complement attribution.

    print("PASS: toy provenance fixture and negative controls; source-local Q ranks=(4,4,0)")
    print("LIMIT: fixture rows are synthetic; selected pinned production event remains UNRESOLVED")


if __name__ == "__main__":
    main()
