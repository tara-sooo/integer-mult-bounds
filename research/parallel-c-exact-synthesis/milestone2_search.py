#!/usr/bin/env python3
"""Exact, lower-bound-pruned pilot for the Issue 42 second milestone."""

import itertools
import json
import math
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
CONFIG = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "milestone2_config.json"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "milestone2_receipt.json"


def child_values(left_width, right_width):
    return sorted(
        {
            left * right
            for left in range(1 << left_width)
            for right in range(1 << right_width)
        }
    )


def product_pairs(values):
    return {
        left * right: [left, right]
        for left in values
        for right in values
    }


def source_functions(width):
    radix = 1 << width
    return [
        tuple((code >> (width * i)) & (radix - 1) for i in range(4))
        for code in range(radix**4)
    ]


def term_table(left_width, right_width, cases, conflicts):
    left_functions = source_functions(left_width)
    right_functions = source_functions(right_width)
    terms = []
    for left_id, left_fn in enumerate(left_functions):
        for right_id, right_fn in enumerate(right_functions):
            values = tuple(left_fn[a] * right_fn[b] for a, b in cases)
            separated = 0
            for bit, (i, j) in enumerate(conflicts):
                if values[i] != values[j]:
                    separated |= 1 << bit
            terms.append(
                {
                    "left_id": left_id,
                    "right_id": right_id,
                    "values": values,
                    "separated": separated,
                }
            )
    return terms


def exact_decoder(term_list, case_products):
    decoder = {}
    for case, expected in enumerate(case_products):
        signature = tuple(term["values"][case] for term in term_list)
        if signature in decoder and decoder[signature] != expected:
            return None
        decoder[signature] = expected
    return [
        {"child_outputs": list(signature), "product": output}
        for signature, output in sorted(decoder.items())
    ]


def search_triples(terms, case_products, full_cover):
    separated = [term["separated"] for term in terms]
    raw_hits = 0
    transpose_orbits = 0
    examples = []
    known = tuple(sorted((6 * 16 + 6, 10 * 16 + 10, 12 * 16 + 12)))
    known_found = False
    for i, first in enumerate(separated):
        for j in range(i, len(terms)):
            pair = first | separated[j]
            for k in range(j, len(terms)):
                if pair | separated[k] != full_cover:
                    continue
                combo = (i, j, k)
                raw_hits += 1
                transposed = tuple(
                    sorted(
                        terms[index]["right_id"] * 16
                        + terms[index]["left_id"]
                        for index in combo
                    )
                )
                if combo <= transposed:
                    transpose_orbits += 1
                    if len(examples) < 8:
                        picked = [terms[index] for index in combo]
                        decoder = exact_decoder(picked, case_products)
                        assert decoder is not None
                        examples.append(
                            {
                                "term_ids": list(combo),
                                "encoders": [
                                    [t["left_id"], t["right_id"]] for t in picked
                                ],
                                "decoder": decoder,
                            }
                        )
                if combo == known:
                    known_found = True
    return {
        "unordered_encoder_sets_checked": math.comb(len(terms) + 2, 3),
        "exact_encoder_sets": raw_hits,
        "exact_sets_mod_child_permutation_and_source_swap": transpose_orbits,
        "known_f2_karatsuba_encoder_set_found": known_found,
        "examples": examples,
    }


def search_mixed(left_terms, wide_terms, case_products, full_cover):
    hits = 0
    examples = []
    for one_bit in left_terms:
        for two_bit in wide_terms:
            if one_bit["separated"] | two_bit["separated"] != full_cover:
                continue
            hits += 1
            if len(examples) < 8:
                decoder = exact_decoder([one_bit, two_bit], case_products)
                assert decoder is not None
                examples.append(
                    {
                        "encoders": [
                            [one_bit["left_id"], one_bit["right_id"]],
                            [two_bit["left_id"], two_bit["right_id"]],
                        ],
                        "decoder": decoder,
                    }
                )
    return {
        "encoder_pairs_checked": len(left_terms) * len(wide_terms),
        "exact_encoder_pairs": hits,
        "examples": examples,
    }


config = json.loads(CONFIG.read_text())
w = config["root_operand_width"]
types = [tuple(pair) for pair in config["child_types"]]
max_calls = config["max_child_calls"]
baseline = config["schoolbook_baseline_cost"]
budget = config["target_max_child_cost"]
assert w == 2 and types == [(1, 1), (1, 2), (2, 1)]
assert max_calls == 3 and baseline == 4 and budget == 3
domain = list(range(1 << w))
outputs = product_pairs(domain)
target_count = len(outputs)
cases = [(a, b) for a in domain for b in domain]
case_products = [a * b for a, b in cases]
conflicts = [
    (i, j)
    for i in range(len(cases))
    for j in range(i + 1, len(cases))
    if case_products[i] != case_products[j]
]
full_cover = (1 << len(conflicts)) - 1

profiles = []
for count in range(max_calls + 1):
    for profile in itertools.product(types, repeat=count):
        assert all(p + q < 2 * w for p, q in profile)
        cost = sum(p * q for p, q in profile)
        signature_capacity = math.prod(
            len(child_values(p, q)) for p, q in profile
        )
        profiles.append(
            {
                "child_types": [list(pair) for pair in profile],
                "child_cost": cost,
                "signature_capacity_upper_bound": signature_capacity,
                "disposition": (
                    "over_cost_budget"
                    if cost > budget
                    else "pruned_by_output_cardinality"
                    if signature_capacity < target_count
                    else "survives_lower_bound"
                ),
            }
        )

eligible = [profile for profile in profiles if profile["child_cost"] <= budget]
survivors = [
    profile
    for profile in eligible
    if profile["signature_capacity_upper_bound"] >= target_count
]
assert len(profiles) == config["resource_budget"]["enumerate_ordered_child_type_profiles"]
assert len(eligible) == 10 and len(survivors) == 5

# Child order and global A/B exchange are exact isomorphisms for this source contract.
# Keep one representative for the all-(1,1) triple and for the mixed (1,1)+(1,2) pair.
triple_terms = term_table(1, 1, cases, conflicts)
wide_terms = term_table(1, 2, cases, conflicts)
triple_search = search_triples(triple_terms, case_products, full_cover)
mixed_search = search_mixed(
    triple_terms, wide_terms, case_products, full_cover
)
searched_candidates = (
    triple_search["unordered_encoder_sets_checked"]
    + mixed_search["encoder_pairs_checked"]
)
assert searched_candidates <= config["resource_budget"]["max_encoder_sets_checked"]
assert searched_candidates == 3_877_632
exact_scheme_count = (
    triple_search["exact_encoder_sets"] + mixed_search["exact_encoder_pairs"]
)
known_only = (
    triple_search["exact_encoder_sets"] == 1
    and triple_search["exact_sets_mod_child_permutation_and_source_swap"] == 1
    and triple_search["known_f2_karatsuba_encoder_set_found"]
    and mixed_search["exact_encoder_pairs"] == 0
)
assert known_only


def karatsuba_decode(xor_product, low_product, high_product):
    cross_parity = xor_product ^ low_product ^ high_product
    doubled_cross = low_product & high_product & (1 - xor_product)
    return low_product + 2 * cross_parity + 4 * doubled_cross + 4 * high_product


candidate_rows = []
for a, b in cases:
    a0, a1 = a & 1, (a >> 1) & 1
    b0, b1 = b & 1, (b >> 1) & 1
    xor_product = (a0 ^ a1) * (b0 ^ b1)
    low_product = a0 * b0
    high_product = a1 * b1
    decoded = karatsuba_decode(xor_product, low_product, high_product)
    assert decoded == a * b
    candidate_rows.append(
        {
            "A": a,
            "B": b,
            "xor_child": xor_product,
            "low_child": low_product,
            "high_child": high_product,
            "decoded_product": decoded,
        }
    )

negative_a = negative_b = 3
n_a0, n_a1 = negative_a & 1, negative_a >> 1
n_b0, n_b1 = negative_b & 1, negative_b >> 1
n_xor = (n_a0 ^ n_a1) * (n_b0 ^ n_b1)
n_low, n_high = n_a0 * n_b0, n_a1 * n_b1
gf2_only_value = n_low + 2 * (n_xor ^ n_low ^ n_high) + 4 * n_high
assert gf2_only_value == 5 and negative_a * negative_b == 9


def xor_half_signature(a, b, half_width):
    mask = (1 << half_width) - 1
    a0, a1 = a & mask, a >> half_width
    b0, b1 = b & mask, b >> half_width
    return ((a0 ^ a1) * (b0 ^ b1), a0 * b0, a1 * b1)


def first_product_collision(half_width):
    operand_max = (1 << (2 * half_width)) - 1
    seen = {}
    first_collision = None
    for a in range(operand_max + 1):
        for b in range(operand_max + 1):
            signature = xor_half_signature(a, b, half_width)
            product = a * b
            if signature not in seen:
                seen[signature] = (a, b, product, signature)
            elif seen[signature][2] != product and first_collision is None:
                first_collision = (seen[signature], (a, b, product, signature))
    return first_collision


assert first_product_collision(1) is None
assert first_product_collision(2) is None
generalization_collision = first_product_collision(3)
assert generalization_collision == (
    (1, 43, 43, (6, 3, 0)),
    (3, 25, 75, (6, 3, 0)),
)

# Adverse controls: preserve independent source roles and check the bound's scope.
alias_left, alias_right = 1, 2
alias_expected = alias_left * alias_right
alias_actual = alias_left * alias_left
assert alias_expected == 2 and alias_actual == 1 and alias_expected != alias_actual

restricted = range(3)
restricted_image = sorted({a * b for a in restricted for b in restricted})
assert restricted_image == [0, 1, 2, 4]
assert len(restricted_image) <= 2**3

# A concrete incomplete three-partial-product proposal has an unavoidable collision.
def truncated_signature(a, b):
    a0, a1 = a & 1, (a >> 1) & 1
    b0, b1 = b & 1, (b >> 1) & 1
    return (a0 & b0, a1 & b0, a0 & b1)


collision_pairs = [(a, b) for a in domain for b in domain]
collision = next(
    (x, y)
    for x in collision_pairs
    for y in collision_pairs
    if x[0] * x[1] != y[0] * y[1]
    and truncated_signature(*x) == truncated_signature(*y)
)
assert collision == ((0, 0), (2, 2))

one_bit_image = sorted({a * b for a in range(2) for b in range(2)})
assert one_bit_image == [0, 1] and len(one_bit_image) <= 2

one_bit_child_count = 3
encoder_tables = 16**2
decoder_tables = 16 ** (2**one_bit_child_count)
naive_three_call_circuits = encoder_tables**one_bit_child_count * decoder_tables
assert naive_three_call_circuits == 2**56

receipt = {
    "status": "BOUNDED_NEW_GRAMMAR_OBSTRUCTION",
    "status_scope": "only the bounded typed encoder-child-decoder grammar and child-cost budget in milestone2_config.json",
    "exact_scheme_count": exact_scheme_count,
    "config": CONFIG.name,
    "deterministic": True,
    "seed": None,
    "source_domain": {"A": domain, "B": domain},
    "source_pair_count": len(domain) ** 2,
    "exact_product_image": sorted(outputs),
    "exact_product_image_size": target_count,
    "witness_pair_by_product": {str(k): v for k, v in sorted(outputs.items())},
    "child_type_profiles_checked": len(profiles),
    "profiles_over_cost_budget": sum(p["child_cost"] > budget for p in profiles),
    "profiles_with_cost_at_most_budget": len(eligible),
    "low_cost_profiles_pruned_by_cardinality": sum(
        p["disposition"] == "pruned_by_output_cardinality" for p in eligible
    ),
    "profiles_retained_after_cardinality_bound": [
        p for p in eligible if p["signature_capacity_upper_bound"] >= target_count
    ],
    "maximum_low_cost_signature_capacity": max(
        p["signature_capacity_upper_bound"] for p in eligible
    ),
    "profile_details": profiles,
    "conflicting_input_pair_constraints": len(conflicts),
    "exact_encoder_search": {
        "symmetries_quotiented": [
            "child permutation",
            "global A/B source-role exchange",
        ],
        "encoder_sets_checked": searched_candidates,
        "resource_budget_encoder_sets": config["resource_budget"]["max_encoder_sets_checked"],
        "all_one_bit_children": triple_search,
        "heterogeneous_children_1x1_plus_1x2": mixed_search,
        "heterogeneous_1x1_plus_2x1_covered_by_global_source_swap": True,
    },
    "classification": {
        "only_exact_encoder_orbit": "known bitwise Karatsuba: low-bit product, high-bit product, and XOR-form product",
        "known_toom_or_karatsuba_isomorphism": True,
        "novel_operator_found": False,
    },
    "natural_uniform_extension_check": {
        "extension": "split each 2m-bit operand into m-bit halves; use low product, high product, and product of bitwise-XOR halves",
        "parent_operand_width": 6,
        "source_pairs_checked": 4096,
        "halfwidth_1_collision": first_product_collision(1),
        "halfwidth_2_collision": first_product_collision(2),
        "halfwidth_3_collision": {
            "first": {
                "A": generalization_collision[0][0],
                "B": generalization_collision[0][1],
                "product": generalization_collision[0][2],
                "child_signature": list(generalization_collision[0][3]),
            },
            "second": {
                "A": generalization_collision[1][0],
                "B": generalization_collision[1][1],
                "product": generalization_collision[1][2],
                "child_signature": list(generalization_collision[1][3]),
            },
            "decoder_exists": False,
        },
    },
    "exact_candidate": {
        "source_encoders": [
            "A0 XOR A1 and B0 XOR B1",
            "A0 and B0",
            "A1 and B1",
        ],
        "child_calls": 3,
        "child_cost_units": 3,
        "schoolbook_child_cost_units": baseline,
        "decoder_formula": "q = x XOR l XOR h; c = l AND h AND NOT x; product = l + 2*q + 4*c + 4*h",
        "decoder_truth_table": triple_search["examples"][0]["decoder"],
        "complete_input_output_truth_table": candidate_rows,
        "exact_replay_pairs": len(candidate_rows),
        "decoder_boolean_gate_upper_bound": {
            "xor": 3,
            "and": 3,
            "not": 1,
            "gate_model": "two-input XOR/AND/NOT; this is a direct implementation, not a minimum-circuit proof",
        },
        "encoding_boolean_gates": {"xor": 2, "and": 0, "not": 0},
        "schoolbook_reference_boolean_gates": {
            "partial_product_and": 4,
            "recombination_xor": 2,
            "recombination_and": 2,
            "total_elementary_gates": 8,
        },
        "candidate_boolean_gate_count_for_stated_decoder": {
            "and_including_children": 6,
            "xor_including_encoders_and_decoder": 5,
            "not": 1,
            "total_elementary_gates": 12,
        },
    },
    "three_one_bit_call_raw_function_space": {
        "encoder_assignments": encoder_tables**one_bit_child_count,
        "decoder_assignments": decoder_tables,
        "combined_assignments": naive_three_call_circuits,
        "enumerated": False,
        "scope_note": "7 distinct exact products fit within 8 signatures; the exact encoder enumeration, not this bound alone, leaves only the known Karatsuba orbit",
    },
    "adverse_controls": {
        "aliased_source_roles": {
            "inputs": [alias_left, alias_right],
            "independent_product": alias_expected,
            "square_after_aliasing": alias_actual,
            "rejected": True,
        },
        "restricted_domain_scope": {
            "domain_per_role": list(restricted),
            "product_image": restricted_image,
            "three_bit_signature_capacity": 8,
            "cardinality_bound_rejects": False,
        },
        "omitted_partial_product_collision": {
            "source_pairs": [list(x) for x in collision],
            "shared_three_product_signature": list(truncated_signature(*collision[0])),
            "products": [collision[0][0] * collision[0][1], collision[1][0] * collision[1][1]],
            "rejected": True,
        },
        "one_bit_multiplication_sanity": {
            "product_image": one_bit_image,
            "one_child_signature_capacity": 2,
            "cardinality_bound_rejects": False,
        },
        "carryless_f2_decode_is_not_integer_decode": {
            "inputs": [negative_a, negative_b],
            "karatsuba_child_outputs": [n_xor, n_low, n_high],
            "carryless_polynomial_product": gf2_only_value,
            "integer_product": negative_a * negative_b,
            "rejected": True,
        },
    },
    "checks": {
        "all_source_pairs_replayed": True,
        "all_cost_feasible_profiles_either_pruned_or_searched": True,
        "all_exact_encoder_hits_have_checked_decoder_examples": (
            len(triple_search["examples"]) == triple_search["exact_encoder_sets"]
            and len(mixed_search["examples"]) == mixed_search["exact_encoder_pairs"]
        ),
        "all_encoder_decoder_tables_enumerated": False,
        "reason_decoder_tables_not_enumerated": "a decoder exists exactly when the child-output signatures separate distinct products; unused entries do not affect correctness",
        "known_candidate_full_truth_table_exact": len(candidate_rows) == 16,
        "natural_extension_collision_replayed": generalization_collision[0][3]
        == generalization_collision[1][3]
        and generalization_collision[0][2] != generalization_collision[1][2],
    },
}

OUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
print(
    json.dumps(
        {
            "status": receipt["status"],
            "source_pairs": receipt["source_pair_count"],
            "profiles_checked": receipt["child_type_profiles_checked"],
            "encoder_sets_checked": searched_candidates,
            "exact_known_schemes": exact_scheme_count,
            "mixed_schemes": mixed_search["exact_encoder_pairs"],
            "width_6_extension_collision": generalization_collision,
        },
        sort_keys=True,
    )
)
