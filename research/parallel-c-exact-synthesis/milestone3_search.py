#!/usr/bin/env python3
"""Exact bounded frame search for one three-role CNOT permutation network."""

from collections import Counter
from itertools import product
import json
from pathlib import Path
from time import monotonic


OUT = Path(__file__).with_name("milestone3_receipt.json")

# Row-major 2x2 integer matrices; ranks are computed exactly over Q.
PALETTE = (
    (0, 0, 0, 0),  # 0
    (1, 0, 0, 1),  # I
    (0, 1, 0, 0),  # E12
    (0, 0, 1, 0),  # E21
    (0, 1, 1, 0),  # E12 + E21
)
NAMES = ("0", "I", "E12", "E21", "E12+E21")
IDENTITY = PALETTE[1]
GATES = ((0, 1), (0, 2), (2, 0), (0, 2), (1, 2), (2, 1))
RHO = (1, 2, 0, 3)  # input role -> output role
INVERSE_RHO = tuple(RHO.index(out) for out in range(4))
ROLE_GATES = tuple(
    tuple(j for j, pair in enumerate(GATES) if role in pair)
    for role in range(3)
)
FRAME_ASSIGNMENTS = len(PALETTE) ** (3 + len(GATES))
BASELINE = 4 * 2


def add_identity(a):
    return (a[0] + 1, a[1], a[2], a[3] + 1)


def subtract(a, b):
    return tuple(x - y for x, y in zip(a, b))


def rank_q(a):
    """Exact rank over Q for a 2x2 integer matrix."""
    if a == (0, 0, 0, 0):
        return 0
    return 2 if a[0] * a[3] - a[1] * a[2] else 1


SINK_PALETTE = tuple(add_identity(a) for a in PALETTE)
RANK_BETWEEN = tuple(
    tuple(rank_q(subtract(head, tail)) for tail in PALETTE)
    for head in PALETTE
)
RANK_TO_SINK = tuple(
    tuple(rank_q(subtract(sink, gate)) for gate in PALETTE)
    for sink in SINK_PALETTE
)


def apply_gates(value, gates=GATES):
    bits = [(value >> role) & 1 for role in range(4)]
    for control, target in gates:
        bits[target] ^= bits[control]
    return sum(bit << role for role, bit in enumerate(bits))


def verify_truth_table(gates=GATES, rows=None):
    expected_domain = set(range(1 << 4))
    rows = expected_domain if rows is None else set(rows)
    if rows != expected_domain:
        return False, 0
    failures = 0
    for value in rows:
        out = apply_gates(value, gates)
        expected = sum(
            (((value >> INVERSE_RHO[role]) & 1) << role)
            for role in range(4)
        )
        failures += out != expected
    return failures == 0, failures


def verify_endpoints(source, sink):
    return all(
        subtract(sink[RHO[role]], source[role]) == IDENTITY
        for role in range(4)
    )


def search():
    start = monotonic()
    histogram = Counter()
    e12_e21_histogram = Counter()
    e12_e21_count = 0
    deficit_count = 0
    e12_e21_deficit_count = 0
    best = None
    best_examples = []

    # Endpoint equations depend on source frames, not gate frames. Check every
    # distinct source tuple once rather than once per gate-frame assignment.
    endpoint_equations_checked = 0
    for active_source_ids in product(range(len(PALETTE)), repeat=3):
        source = tuple(PALETTE[i] for i in active_source_ids) + (PALETTE[0],)
        sink = tuple(
            add_identity(source[INVERSE_RHO[role]]) for role in range(4)
        )
        assert verify_endpoints(source, sink)
        endpoint_equations_checked += 4

    for assignment in product(range(len(PALETTE)), repeat=9):
        source_ids = assignment[:3]
        gate_ids = assignment[3:]
        total = 0
        for role, gate_indices in enumerate(ROLE_GATES):
            if not gate_indices:
                raise AssertionError("unexpected gate-free data role")
            first, *rest = gate_indices
            total += RANK_BETWEEN[gate_ids[first]][source_ids[role]]
            for before, after in zip(gate_indices, rest):
                total += RANK_BETWEEN[gate_ids[after]][gate_ids[before]]
            sink_source_id = source_ids[INVERSE_RHO[role]]
            total += RANK_TO_SINK[sink_source_id][gate_ids[gate_indices[-1]]]
        # The arbitrary scratch role is untouched by every bit gate and has
        # the required direct edge source->sink whose difference is I_2.
        total += rank_q(IDENTITY)

        histogram[total] += 1
        contains_e12 = 2 in assignment
        contains_e21 = 3 in assignment
        has_nontriangular_pair = contains_e12 and contains_e21
        if has_nontriangular_pair:
            e12_e21_count += 1
            e12_e21_histogram[total] += 1
        if total < BASELINE:
            deficit_count += 1
            if has_nontriangular_pair:
                e12_e21_deficit_count += 1
        if best is None or total < best:
            best = total
            best_examples = [assignment]
        elif total == best and len(best_examples) < 10:
            best_examples.append(assignment)

    ok, truth_failures = verify_truth_table()
    assert ok and truth_failures == 0
    wrong_gates = list(GATES)
    wrong_gates[0] = (1, 0)
    wrong_gate_ok, wrong_gate_failures = verify_truth_table(wrong_gates)
    assert not wrong_gate_ok and wrong_gate_failures == 12
    aliased_rows = [
        value for value in range(16)
        if ((value >> 0) & 1) == ((value >> 1) & 1)
    ]
    alias_ok, _ = verify_truth_table(rows=aliased_rows)
    assert not alias_ok
    scratch_ok = all(
        ((apply_gates(value) >> 3) & 1) == ((value >> 3) & 1)
        for value in range(16)
    )
    assert scratch_ok

    # Exact rank controls distinguish zero, singular nonzero and full rank.
    assert rank_q(PALETTE[0]) == 0
    assert rank_q((1, 2, 2, 4)) == 1
    assert rank_q(IDENTITY) == 2

    # An endpoint perturbation must be rejected by the rational checker.
    bad_source = (PALETTE[0], PALETTE[0], PALETTE[0], PALETTE[0])
    good_sink = tuple(
        add_identity(bad_source[INVERSE_RHO[role]]) for role in range(4)
    )
    bad_sink = list(good_sink)
    bad_sink[RHO[0]] = tuple(
        x + y for x, y in zip(bad_sink[RHO[0]], PALETTE[2])
    )
    endpoint_control_rejected = not verify_endpoints(
        bad_source, tuple(bad_sink)
    )
    assert endpoint_control_rejected

    # E12 and E21 have distinct unique eigenlines, so this subgrammar really
    # includes frames outside every common triangular flag, over Q-bar too.
    expected_nontri_count = 5**9 - 2 * 4**9 + 3**9
    assert e12_e21_count == expected_nontri_count
    assert best is not None
    assert best == BASELINE
    assert deficit_count == 0 and e12_e21_deficit_count == 0
    assert sum(histogram.values()) == FRAME_ASSIGNMENTS
    assert sum(e12_e21_histogram.values()) == expected_nontri_count
    elapsed = monotonic() - start

    return {
        "result": "SCOPED_FRAME_NO_GO",
        "search": {
            "field": "Q",
            "m": 2,
            "W": 4,
            "data_roles": [0, 1, 2],
            "scratch_roles": [3],
            "gate_word_control_target": [list(pair) for pair in GATES],
            "rho_input_to_output": list(RHO),
            "frame_palette_names": list(NAMES),
            "frame_palette_matrices": [list(a) for a in PALETTE],
            "common_translation_quotiented": True,
            "scratch_frame_quotiented": True,
            "raw_palette_assignments_including_scratch": len(PALETTE) ** 10,
            "scratch_frame_palette_choices_quotiented": len(PALETTE),
            "enumerated_assignments": FRAME_ASSIGNMENTS,
            "elapsed_seconds": round(elapsed, 3),
            "seed": None,
            "limit": "exhaustive over the stated fixed topology and palette; no timeout",
        },
        "verification": {
            "f2_all_independent_inputs": 16,
            "f2_permutation_pass": ok,
            "f2_wrong_control_gate_rejected": not wrong_gate_ok,
            "f2_wrong_control_mismatching_rows": wrong_gate_failures,
            "f2_aliased_role_domain_rejected": not alias_ok,
            "f2_scratch_arbitrary_and_preserved": scratch_ok,
            "q_endpoint_equations_checked_all_distinct_source_tuples": endpoint_equations_checked,
            "q_rank_formula": "0 for zero, 1 for nonzero determinant-zero, 2 for nonzero determinant",
            "q_rank_controls_pass": True,
            "q_endpoint_perturbation_rejected": endpoint_control_rejected,
            "common_gate_frame": "one matrix variable per gate shared by both incident roles",
        },
        "result_counts": {
            "baseline_Wm": BASELINE,
            "rank_sum_histogram": {
                str(k): histogram[k] for k in sorted(histogram)
            },
            "best_rank_sum": best,
            "strict_deficit_assignments": deficit_count,
            "assignments_containing_E12_and_E21": e12_e21_count,
            "E12_and_E21_histogram": {
                str(k): e12_e21_histogram[k]
                for k in sorted(e12_e21_histogram)
            },
            "E12_and_E21_strict_deficit_assignments": e12_e21_deficit_count,
            "assignments_containing_E12_and_E21_expected": expected_nontri_count,
            "best_frame_examples_palette_ids": [
                list(a) for a in best_examples
            ],
        },
    }


if __name__ == "__main__":
    receipt = search()
    OUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps(receipt["result_counts"], sort_keys=True))
    print(f"receipt={OUT.name}")
