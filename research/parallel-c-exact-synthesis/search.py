#!/usr/bin/env python3
"""Deterministic exact search for rank-three two-limb multiplication tensors."""

import argparse
import itertools
import json
import math
import platform
import time
from fractions import Fraction
from pathlib import Path


TARGETS = ((1, 0, 0, 0), (0, 1, 1, 0), (0, 0, 0, 1))


def forms_with_bound(bound):
    # shortcut: coefficient bound 2 and decoder denominator 2, expand only with a new paid-cost screen
    forms = []
    for p in range(-bound, bound + 1):
        for q in range(-bound, bound + 1):
            if (p, q) == (0, 0) or math.gcd(abs(p), abs(q)) != 1:
                continue
            if p < 0 or (p == 0 and q < 0):
                continue
            forms.append((p, q))
    return sorted(forms)


def tensor_vector(a_form, b_form):
    a0, a1 = a_form
    b0, b1 = b_form
    return (a0 * b0, a0 * b1, a1 * b0, a1 * b1)


def solve_targets(columns, targets):
    """Solve all targets in the span of three independent 4-vectors over Q."""
    width = len(columns)
    rows = [
        [Fraction(columns[col][row]) for col in range(width)]
        + [Fraction(target[row]) for target in targets]
        for row in range(len(targets[0]))
    ]
    pivot_rows = {}
    next_row = 0
    for col in range(width):
        pivot = next((r for r in range(next_row, len(rows)) if rows[r][col]), None)
        if pivot is None:
            return None
        rows[next_row], rows[pivot] = rows[pivot], rows[next_row]
        scale = rows[next_row][col]
        rows[next_row] = [value / scale for value in rows[next_row]]
        for r in range(len(rows)):
            if r == next_row or rows[r][col] == 0:
                continue
            scale = rows[r][col]
            rows[r] = [x - scale * y for x, y in zip(rows[r], rows[next_row])]
        pivot_rows[col] = next_row
        next_row += 1
    for row in rows:
        if all(row[col] == 0 for col in range(width)) and any(
            row[width + j] != 0 for j in range(len(targets))
        ):
            return None
    return [
        [rows[pivot_rows[col]][width + j] for col in range(width)]
        for j in range(len(targets))
    ]


def independent_columns(columns):
    rows = [[columns[col][row] for col in range(len(columns))] for row in range(len(columns[0]))]
    rank = 0
    for col in range(len(columns)):
        pivot = next((r for r in range(rank, len(rows)) if rows[r][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for r in range(rank + 1, len(rows)):
            if rows[r][col]:
                scale = Fraction(rows[r][col], rows[rank][col])
                rows[r] = [x - scale * y for x, y in zip(rows[r], rows[rank])]
        rank += 1
        if rank == len(columns):
            return True
    return False


def lcm(values):
    out = 1
    for value in values:
        out = math.lcm(out, value)
    return out


def identity_holds(terms, denominator, decoder_numerators):
    columns = [tensor_vector(a, b) for a, b in terms]
    for output, target in enumerate(TARGETS):
        rebuilt = tuple(
            sum(decoder_numerators[i][output] * columns[i][k] for i in range(len(terms)))
            for k in range(4)
        )
        if rebuilt != tuple(denominator * x for x in target):
            return False
    return True


def max_abs_on_digit_box(form, base):
    positive = sum(max(value, 0) for value in form)
    negative = sum(max(-value, 0) for value in form)
    return max(positive, negative) * (base - 1)


def normalize_form(form):
    """Return primitive sign-normalized form and the sign removed from it."""
    p, q = form
    divisor = math.gcd(abs(p), abs(q))
    p //= divisor
    q //= divisor
    sign = 1
    if p < 0 or (p == 0 and q < 0):
        p, q = -p, -q
        sign = -1
    return (p, q), sign


def transform_candidate(candidate, swap_inputs, reverse_limbs):
    terms = []
    numerators = []
    for (a_form, b_form), row in zip(candidate["terms"], candidate["decoder_numerators"]):
        if swap_inputs:
            a_form, b_form = b_form, a_form
        sign = 1
        if reverse_limbs:
            a_form, sign_a = normalize_form((a_form[1], a_form[0]))
            b_form, sign_b = normalize_form((b_form[1], b_form[0]))
            sign = sign_a * sign_b
        terms.append((a_form, b_form))
        output_row = (row[2], row[1], row[0]) if reverse_limbs else tuple(row)
        numerators.append(tuple(sign * value for value in output_row))
    ordered = sorted(zip(terms, numerators))
    return {
        "denominator": candidate["denominator"],
        "terms": [term for term, _ in ordered],
        "decoder_numerators": [row for _, row in ordered],
    }


def record_key(candidate):
    return json.dumps(candidate, separators=(",", ":"))


def symmetry_orbit(candidate):
    orbit = {}
    for swap_inputs in (False, True):
        for reverse_limbs in (False, True):
            transformed = transform_candidate(candidate, swap_inputs, reverse_limbs)
            assert identity_holds(
                transformed["terms"], transformed["denominator"], transformed["decoder_numerators"]
            )
            orbit[record_key(transformed)] = transformed
    return orbit


def known_variant(candidate):
    e0, e1 = (1, 0), (0, 1)
    summed, difference = (1, 1), (1, -1)
    sum_terms = sorted(((e0, e0), (e1, e1), (summed, summed)))
    difference_terms = sorted(((e0, e0), (e1, e1), (difference, difference)))
    if sorted(candidate["terms"]) == sum_terms:
        return "Karatsuba sum-evaluation (Toom-2 at 0, 1, infinity)"
    if sorted(candidate["terms"]) == difference_terms:
        return "Karatsuba difference-evaluation"
    if all(a_form == b_form for a_form, b_form in candidate["terms"]):
        return "three-point Toom-2 evaluation/interpolation"
    return "other in the bounded tensor grammar"


def eval_candidate(candidate, a, b, base):
    products = [
        (ta[0] * a[0] + ta[1] * a[1]) * (tb[0] * b[0] + tb[1] * b[1])
        for ta, tb in candidate["terms"]
    ]
    outputs = []
    for output in range(3):
        numerator = sum(
            candidate["decoder_numerators"][i][output] * products[i]
            for i in range(3)
        )
        denominator = candidate["denominator"]
        assert numerator % denominator == 0
        outputs.append(numerator // denominator)
    return outputs, sum(outputs[i] * (base**i) for i in range(3))


def find_replay_failure(candidate, base, wrong_decoder=False):
    test_candidate = json.loads(json.dumps(candidate))
    if wrong_decoder:
        test_candidate["decoder_numerators"][0][0] += 1
    for a0, a1, b0, b1 in itertools.product(range(base), repeat=4):
        a, b = (a0, a1), (b0, b1)
        try:
            outputs, value = eval_candidate(test_candidate, a, b, base)
        except AssertionError:
            return {"a": list(a), "b": list(b), "failure": "wrong decoder lost exact divisibility"}
        expected = (a0 + base * a1) * (b0 + base * b1)
        if value != expected:
            return {"a": list(a), "b": list(b), "candidate_output": value, "expected": expected,
                    "failure": "wrong integer product"}
    return None


def cost_row(candidate, limb_bits):
    base = 1 << limb_bits
    child_rows = []
    for index, (a_form, b_form) in enumerate(candidate["terms"]):
        a_bound = max_abs_on_digit_box(a_form, base)
        b_bound = max_abs_on_digit_box(b_form, base)
        child_rows.append({
            "child": index + 1,
            "a_form": list(a_form),
            "b_form": list(b_form),
            "a_abs_bound": a_bound,
            "b_abs_bound": b_bound,
            "a_magnitude_bits": a_bound.bit_length(),
            "b_magnitude_bits": b_bound.bit_length(),
            "a_sign_variable": a_form[0] * a_form[1] < 0,
            "b_sign_variable": b_form[0] * b_form[1] < 0,
        })
    decoder = []
    for output in range(3):
        raw_coeffs = [candidate["decoder_numerators"][i][output] for i in range(3)]
        reduction = math.gcd(candidate["denominator"], *(abs(x) for x in raw_coeffs))
        coeffs = [x // reduction for x in raw_coeffs]
        decoder.append({
            "output_coefficient": output,
            "integer_coefficients_after_common_factor_reduction": coeffs,
            "nonzero_products": sum(x != 0 for x in coeffs),
            "minimum_binary_adds_to_combine": max(0, sum(x != 0 for x in coeffs) - 1),
            "nonunit_constant_scales": [x for x in coeffs if abs(x) > 1],
            "exact_division_by": candidate["denominator"] // reduction,
        })
    return {
        "limb_bits": limb_bits,
        "base": base,
        "children": child_rows,
        "variable_sign_input_normalizations": sum(
            child["a_sign_variable"] + child["b_sign_variable"] for child in child_rows
        ),
        "variable_sign_product_restorations": sum(
            child["a_sign_variable"] or child["b_sign_variable"] for child in child_rows
        ),
        "decoder": decoder,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("search_config.json"))
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("search_receipt.json"))
    args = parser.parse_args()
    start = time.monotonic()
    config = json.loads(args.config.read_text())
    forms = forms_with_bound(config["max_abs_linear_coefficient"])
    terms = sorted((a, b) for a in forms for b in forms)
    products_per_candidate = config["products_per_candidate"]
    raw_candidates = []
    rank_three = 0
    in_span = 0
    denominator_histogram = {}
    examined = 0
    spanning_term_sets = []
    for chosen_terms in itertools.combinations(terms, products_per_candidate):
        examined += 1
        columns = [tensor_vector(a, b) for a, b in chosen_terms]
        if independent_columns(columns):
            rank_three += 1
        decoder = solve_targets(columns, TARGETS)
        if decoder is None:
            continue
        in_span += 1
        spanning_term_sets.append(tuple(chosen_terms))
        denominator = lcm(value.denominator for row in decoder for value in row)
        denominator_histogram[str(denominator)] = denominator_histogram.get(str(denominator), 0) + 1
        if denominator not in config["decoder_denominators"]:
            continue
        scaled = [
            [int(decoder[output][product] * denominator) for output in range(len(TARGETS))]
            for product in range(products_per_candidate)
        ]
        candidate = {
            "denominator": denominator,
            "terms": chosen_terms,
            "decoder_numerators": scaled,
        }
        assert identity_holds(candidate["terms"], denominator, scaled)
        raw_candidates.append(candidate)

    expected_evaluation_triples = {
        tuple(sorted((form, form) for form in selected))
        for selected in itertools.combinations(forms, products_per_candidate)
    }
    assert set(spanning_term_sets) == expected_evaluation_triples

    representatives = {}
    for candidate in raw_candidates:
        orbit = symmetry_orbit(candidate)
        representatives[min(orbit)] = min(orbit.values(), key=record_key)
    reps = list(representatives.values())
    classes = {}
    for candidate in reps:
        label = known_variant(candidate)
        classes[label] = classes.get(label, 0) + 1

    replay_base = 1 << config["finite_replay_limb_bits"]
    for candidate in raw_candidates:
        assert identity_holds(candidate["terms"], candidate["denominator"], candidate["decoder_numerators"])
        for a0, a1, b0, b1 in itertools.product(range(replay_base), repeat=4):
            _, actual = eval_candidate(candidate, (a0, a1), (b0, b1), replay_base)
            expected = (a0 + replay_base * a1) * (b0 + replay_base * b1)
            assert actual == expected

    assert reps, "the bounded search unexpectedly found no candidate for its negative controls"
    control = reps[0]
    bad_decoder = json.loads(json.dumps(control))
    bad_decoder["decoder_numerators"][0][0] += 1
    wrong_decoder_rejected = not identity_holds(
        bad_decoder["terms"], bad_decoder["denominator"], bad_decoder["decoder_numerators"]
    )
    wrong_decoder_witness = find_replay_failure(control, replay_base, wrong_decoder=True)
    assert wrong_decoder_rejected and wrong_decoder_witness
    alias_a, alias_b = (1, 2), (3, 1)
    _, independent_value = eval_candidate(control, alias_a, alias_b, replay_base)
    _, aliased_value = eval_candidate(control, alias_a, alias_a, replay_base)
    assert independent_value == (1 + 2 * replay_base) * (3 + replay_base)
    assert aliased_value != independent_value

    receipt = {
        "method": "deterministic exhaustive enumeration; no RNG seed",
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "config": config,
        "input_forms": [list(form) for form in forms],
        "term_count": len(terms),
        "triples_examined": examined,
        "rank_three_triples": rank_three,
        "triples_spanning_all_three_convolution_outputs": in_span,
        "exact_span_classification": "PASS: the complete valid set is exactly every triple of distinct diagonal source forms (same projective linear form on A and B)",
        "all_evaluation_triples_in_projective_form_set": len(expected_evaluation_triples),
        "decoder_denominator_histogram_for_exact_spans": denominator_histogram,
        "accepted_candidates_before_symmetry": len(raw_candidates),
        "accepted_candidates": [
            {
                "denominator": candidate["denominator"],
                "terms": [{"a": list(a), "b": list(b)} for a, b in candidate["terms"]],
                "decoder_numerators": candidate["decoder_numerators"],
            }
            for candidate in raw_candidates
        ],
        "symmetry_quotient": ["product permutation", "A/B input exchange", "simultaneous limb reversal with endpoint-output reversal", "per-factor sign normalization"],
        "symmetry_orbits": len(reps),
        "orbit_class_counts": classes,
        "representatives": [
            {
                **candidate,
                "terms": [{"a": list(a), "b": list(b)} for a, b in candidate["terms"]],
                "known_class": known_variant(candidate),
                "cost_screen_at_configured_limb_bits": cost_row(candidate, config["finite_replay_limb_bits"]),
            }
            for candidate in sorted(reps, key=record_key)
        ],
        "exact_tensor_checks": "PASS for every accepted candidate: integer numerator tensors equal denominator times convolution tensor",
        "actual_integer_multiplication_replay": {
            "status": "PASS",
            "limb_bits": config["finite_replay_limb_bits"],
            "base": replay_base,
            "input_quadruples_per_candidate": replay_base**4,
            "candidate_count": len(raw_candidates),
        },
        "adverse_controls": {
            "wrong_decoder": {"status": "PASS: rejected by exact tensor check and finite replay", "witness": wrong_decoder_witness},
            "independent_source_roles": {
                "status": "PASS: aliasing B's source to A's values fails on a != b",
                "a": list(alias_a), "b": list(alias_b), "independent_product": independent_value,
                "aliased_product": aliased_value,
            },
        },
        "elapsed_seconds": round(time.monotonic() - start, 6),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: receipt[k] for k in (
        "triples_examined", "rank_three_triples", "triples_spanning_all_three_convolution_outputs",
        "decoder_denominator_histogram_for_exact_spans", "accepted_candidates_before_symmetry",
        "symmetry_orbits", "orbit_class_counts", "elapsed_seconds"
    )}, indent=2, sort_keys=True))
    print(f"receipt={args.output}")


if __name__ == "__main__":
    main()
