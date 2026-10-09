#!/usr/bin/env python3
# shortcut: only pinned p=4 and the Issue 28 shear; extend after a source-approved geometry exists.
"""Exact p=4 baseline, fixed Issue 28 shear, and bounded address screen.

The port formulas are reimplemented from the frozen PR 144 source. The
operator is fixed by the Issue 28 commit; this checker never tunes it.
Prepared with OpenAI Codex assistance; the repository Apache-2.0 license applies.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


P, H, V = 4, 8, 32
ISSUE = "https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/29"
ISSUE28 = "https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/c4c9c6461d86b84774b9a8cd0b5907549275c740"
PR144 = "https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144"
PR144_COMMIT = "https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/c8b22bc5c10dba497ac25804e27d9647d818e2ff"
PR130 = "https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/130"
PR130_COMMIT = "https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/6a9970a530119174507904e23592fd59ede19a5d"


def eye(n, scale=1):
    return [[scale * int(i == j) for j in range(n)] for i in range(n)]


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def madd(a, b, sign=1):
    return [[x + sign * y for x, y in zip(ra, rb)]
            for ra, rb in zip(a, b)]


def digest(matrix):
    payload = json.dumps(matrix, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def coefficient(value_twice):
    return str(Fraction(value_twice, 2))


def port_order():
    return [(cube, bits, tuple(2 * i + bit for i, bit in zip(cube, bits)))
            for cube in combinations(range(P), 3)
            for bits in product(range(2), repeat=3)]


def address_mask(coords):
    return sum(1 << coordinate for coordinate in coords)


def dot_f2(a, b):
    return (a & b).bit_count() & 1


def gf2_rank(rows):
    basis = {}
    for value in rows:
        x = value
        for pivot in sorted(basis, reverse=True):
            if (x >> pivot) & 1:
                x ^= basis[pivot]
        if x:
            pivot = x.bit_length() - 1
            for old_pivot, old_row in list(basis.items()):
                if (old_row >> pivot) & 1:
                    basis[old_pivot] = old_row ^ x
            basis[pivot] = x
    return len(basis)


def source_h_twice(source_cube, source_bits, target_cube, target_bits):
    shared = sorted(set(source_cube) & set(target_cube))
    if not shared:
        return 1
    if len(shared) == 1:
        i = shared[0]
        si, ti = source_cube.index(i), target_cube.index(i)
        return int(source_bits[si] == 1 - target_bits[ti])
    if len(shared) == 2:
        i, j = shared
        ai = source_bits[source_cube.index(i)]
        aj = source_bits[source_cube.index(j)]
        ti = target_bits[target_cube.index(i)]
        tj = target_bits[target_cube.index(j)]
        if (ai ^ aj) == (ti ^ tj):
            return (2 * ti - 1) * (1 - 2 * ai)
    return 0


def support(matrix, ports):
    result = []
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value:
                result.append({
                    "row": i,
                    "column": j,
                    "coefficient_doubled": value,
                    "coefficient": coefficient(value),
                    "old_address_dot": dot_f2(
                        address_mask(ports[i][2]), address_mask(ports[j][2])),
                })
    return result


def compact_support(edges):
    return [[edge["row"], edge["column"], edge["coefficient_doubled"]]
            for edge in edges]


def matrix_counts(matrix):
    return {coefficient(value): count
            for value, count in sorted(Counter(x for row in matrix for x in row).items())}


def violations(edges):
    return [edge for edge in edges if edge["old_address_dot"]]


def lifted_violations(edges, labels):
    result = []
    for edge in edges:
        i, j = edge["row"], edge["column"]
        parity = dot_f2(labels[i], labels[j])
        if parity:
            result.append({
                "row": i,
                "column": j,
                "coefficient_doubled": edge["coefficient_doubled"],
                "lifted_address_dot": parity,
            })
    return result


def changed_entries(before, after, ports):
    changes = []
    for i in range(V):
        for j in range(V):
            old, new = before[i][j], after[i][j]
            if old != new:
                changes.append({
                    "row": i,
                    "column": j,
                    "before_doubled": old,
                    "after_doubled": new,
                    "before": coefficient(old),
                    "after": coefficient(new),
                    "old_address_dot": dot_f2(
                        address_mask(ports[i][2]), address_mask(ports[j][2])),
                })
    return changes


def main():
    ports = port_order()
    assert len(ports) == V and len({address_mask(p[2]) for p in ports}) == V
    index = {(cube, bits): i for i, (cube, bits, _) in enumerate(ports)}
    masks = [address_mask(port[2]) for port in ports]
    assert all(mask.bit_count() == 3 for mask in masks)
    assert all(dot_f2(mask, mask) == 1 for mask in masks)

    # Exact doubled matrices: n represents coefficient n/2.
    B2 = [[len(set(t[2]) & set(s[2])) - 1 for s in ports] for t in ports]
    Bblock2 = [[B2[i][j] if ports[i][0] == ports[j][0] else 0
                for j in range(V)] for i in range(V)]
    K2 = madd(eye(V, 2), Bblock2, -1)
    H2 = madd(Bblock2, B2, -1)
    I2, I4 = eye(V, 2), eye(V, 4)

    # P-A is the source-defined signed Hadamard/2 involution in each cube.
    PminusA = [[0] * V for _ in range(V)]
    for i, (cube_t, bits_t, _) in enumerate(ports):
        for j, (cube_s, bits_s, _) in enumerate(ports):
            if cube_t == cube_s:
                distance = sum(x != y for x, y in zip(bits_t, bits_s))
                PminusA[i][j] = int(distance == 3) - int(distance == 1)
    assert K2 == PminusA
    assert madd(madd(K2, H2), B2) == I2
    assert mm(K2, K2) == I4

    # Independent source formulas: copied coordinate stars and F/A/G channels.
    for i, (cube_t, bits_t, t) in enumerate(ports):
        for j, (cube_s, bits_s, s) in enumerate(ports):
            overlap = len(set(t) & set(s))
            star_scatter_twice = overlap - 1
            assert B2[i][j] == star_scatter_twice
            expected_h = 0 if cube_t == cube_s else source_h_twice(
                cube_s, bits_s, cube_t, bits_t)
            assert H2[i][j] == expected_h, (i, j, expected_h, H2[i][j])

    base_support = {
        "B": support(B2, ports), "H": support(H2, ports), "K": support(K2, ports)}
    assert len(base_support["B"]) == 544
    assert len(base_support["K"]) == 128 and not violations(base_support["K"])
    assert len(base_support["H"]) == 384 and not violations(base_support["H"])

    # Issue 28's one frozen shear: C=I+E_(0,8), with its exact inverse.
    a, b = 0, 8
    Eab = [[int(i == a and j == b) for j in range(V)] for i in range(V)]
    C, Cinv = madd(eye(V), Eab), madd(eye(V), Eab, -1)
    assert mm(C, Cinv) == eye(V) and mm(Cinv, C) == eye(V)
    Kp2 = mm(mm(C, K2), Cinv)
    Bp2 = [row[:] for row in B2]
    Hp2 = madd(madd(I2, Kp2, -1), Bp2, -1)
    assert mm(Kp2, Kp2) == I4
    assert madd(madd(Kp2, Hp2), Bp2) == I2

    candidate_support = {
        "B_prime": support(Bp2, ports),
        "K_prime": support(Kp2, ports),
        "H_prime": support(Hp2, ports),
    }
    assert len(candidate_support["B_prime"]) == 544
    assert len(candidate_support["K_prime"]) == 136
    assert len(candidate_support["H_prime"]) == 386
    assert len(violations(candidate_support["K_prime"])) == 4
    assert len(violations(candidate_support["H_prime"])) == 4
    union = sorted({
        (edge["row"], edge["column"])
        for name in ("K_prime", "H_prime")
        for edge in candidate_support[name]
    })
    assert len(union) == 516
    assert sum(dot_f2(masks[i], masks[j]) for i, j in union) == 4

    # Rank-1 common-label UNSAT certificate, using three exact support edges.
    common_edges = {
        "odd_0_10": (Kp2[0][10], dot_f2(masks[0], masks[10])),
        "odd_2_8": (Kp2[2][8], dot_f2(masks[2], masks[8])),
        "even_0_2": (Kp2[0][2], dot_f2(masks[0], masks[2])),
    }
    assert common_edges == {
        "odd_0_10": (-1, 1), "odd_2_8": (1, 1), "even_0_2": (-1, 0)}
    # The first two equations force u0=u2=1; the third requires u0*u2=0.

    # Rank-1 separate-label UNSAT certificate uses a different oriented edge.
    separate_edges = {
        "odd_0_10": (Kp2[0][10], dot_f2(masks[0], masks[10])),
        "odd_2_8": (Kp2[2][8], dot_f2(masks[2], masks[8])),
        "even_0_8": (Hp2[0][8], dot_f2(masks[0], masks[8])),
    }
    assert separate_edges == {
        "odd_0_10": (-1, 1), "odd_2_8": (1, 1), "even_0_8": (-1, 0)}
    # They force x0=y8=1, while H'[0,8] requires x0*y8=0.

    # The sole rank-2 common-label experiment has a complete witness.
    # Integer bits are little-endian: bit 0 is coordinate 8, bit 1 is 9.
    u = [1, 0, 2, 0, 2, 0, 0, 0, 2, 0, 1, 0, 1] + [0] * 19
    lifted = [mask | (u[i] << H) for i, mask in enumerate(masks)]
    assert len(u) == V and len(set(lifted)) == V
    assert sum(value != 0 for value in u) == 6
    original_support_audit = {
        name: {
            "edge_count": len(base_support[name]),
            "orthogonality_violations": len(
                lifted_violations(base_support[name], lifted)),
            "violations": lifted_violations(base_support[name], lifted),
        }
        for name in ("K", "H")
    }
    assert original_support_audit == {
        "K": {"edge_count": 128, "orthogonality_violations": 0, "violations": []},
        "H": {"edge_count": 384, "orthogonality_violations": 0, "violations": []},
    }
    assert all(dot_f2(lifted[i], lifted[j]) == 0 for i, j in union)

    # The Gram fit is not the source address geometry: six ports become
    # weight four and isotropic, while the pinned ports all have weight three.
    self_pairings = [dot_f2(value, value) for value in lifted]
    assert self_pairings.count(0) == 6 and self_pairings.count(1) == 26
    assert sum(value.bit_count() == 4 for value in lifted) == 6
    assert sum(value.bit_count() == 3 for value in lifted) == 26
    assert gf2_rank(lifted) == 10
    assert gf2_rank([1 << i for i in range(H + 2)]) == H + 2
    lifted_incidence = [
        sum((value >> coordinate) & 1 for value in lifted)
        for coordinate in range(H + 2)
    ]
    assert lifted_incidence == [12] * H + [3, 3]
    gram_rows = [sum(dot_f2(x, y) << j for j, y in enumerate(lifted))
                 for x in lifted]
    assert gf2_rank(gram_rows) == 10
    # Any norm-preserving appended vector in F2^2 is 00 or 11; both choices
    # pair to zero with each other, so the required odd edge cannot be fixed.
    isotropic_appends = [value for value in range(4) if dot_f2(value, value) == 0]
    assert isotropic_appends == [0, 3]
    assert all(dot_f2(x, y) == 0 for x in isotropic_appends for y in isotropic_appends)
    # A zero-extended old target hyperplane has dimension 7; the new
    # orthogonal hyperplane has dimension 9 and needs two new directions.
    assert all(lifted[i] & ((1 << H) - 1) == masks[i] for i in range(V))

    old_digests = {
        "B_doubled": digest(B2),
        "H_doubled": digest(H2),
        "K_doubled": digest(K2),
    }
    candidate_digests = {
        "B_prime_doubled": digest(Bp2),
        "H_prime_doubled": digest(Hp2),
        "K_prime_doubled": digest(Kp2),
    }
    assert old_digests == {
        "B_doubled": "29697b4932e26c5d3df4ee33d944032b744d8c1eafbde8fd91640a78e1e909d1",
        "H_doubled": "412b494e4c618cd5f5767868e57d1741cfa202c3f573505db34a8ac62da74697",
        "K_doubled": "a3194574b22d6bf37add70f3b3f9989f853e25740016dc9a466678d6a315cb97",
    }
    assert candidate_digests == {
        "B_prime_doubled": "29697b4932e26c5d3df4ee33d944032b744d8c1eafbde8fd91640a78e1e909d1",
        "H_prime_doubled": "84f3c637fb8912a3b1be18d580998540cd35961597625c47701b73b3638a0186",
        "K_prime_doubled": "cf97073b6e09bfe1009fb12e81465fbbbca7901fbeb2f736fbf6252cedbc334d",
    }

    receipt = {
        "schema": "orthogonal-address-lift-exact-v1",
        "scope": "FAST exact p=4/h=8; fixed Issue 28 shear; rank 1 common and separate; one rank 2 common Gram experiment",
        "source_pins": {
            "issue_29": ISSUE,
            "issue_28_fixed_commit": ISSUE28,
            "pr_144": PR144,
            "pr_144_frozen_commit": PR144_COMMIT,
            "pr_130": PR130,
            "pr_130_frozen_commit": PR130_COMMIT,
        },
        "parameters": {"p": P, "h": H, "port_count": V,
                       "coefficient_encoding": "all matrices are doubled integers; n means n/2",
                       "address_form": "ordinary dot product over F2",
                       "support_domain_row_encoding": "[row, column, coefficient_doubled]"},
        "ports": [
            {"index": i, "cube_pair_indices": list(cube),
             "selector_bits": list(bits), "coordinates": list(coords),
             "address_mask": masks[i]}
            for i, (cube, bits, coords) in enumerate(ports)
        ],
        "baseline": {
            "matrices_doubled": {"B": B2, "H": H2, "K": K2},
            "matrix_sha256": old_digests,
            "coefficient_counts": {
                "B": matrix_counts(B2), "H": matrix_counts(H2), "K": matrix_counts(K2)},
            "support_domains": {
                name: compact_support(edges) for name, edges in base_support.items()},
            "identities": {
                "K_plus_H_plus_B_equals_I": True,
                "K_equals_P_minus_A_over_2": True,
                "K_squared_equals_I": True,
                "copied_star_scatter_equals_B": True,
                "source_fa_g_h_equals_H": True,
                "all_K_H_supports_orthogonal": True,
            },
            "support_counts": {"B": sum(x != 0 for row in B2 for x in row),
                               "H": len(base_support["H"]), "K": len(base_support["K"])},
        },
        "issue_28_fixed_candidate": {
            "a": {"index": a, "coordinates": list(ports[a][2])},
            "b": {"index": b, "coordinates": list(ports[b][2])},
            "C": "I+E_(0,8)",
            "C_inverse": "I-E_(0,8)",
            "matrices_doubled": {"B_prime": Bp2, "H_prime": Hp2, "K_prime": Kp2},
            "matrix_sha256": candidate_digests,
            "coefficient_counts": {
                "B_prime": matrix_counts(Bp2),
                "H_prime": matrix_counts(Hp2),
                "K_prime": matrix_counts(Kp2),
            },
            "support_domains": {
                name: compact_support(edges) for name, edges in candidate_support.items()},
            "support_union": [[i, j, dot_f2(masks[i], masks[j])] for i, j in union],
            "support_counts": {"B_prime": len(candidate_support["B_prime"]),
                               "K_prime": len(candidate_support["K_prime"]),
                               "H_prime": len(candidate_support["H_prime"]),
                               "union": len(union), "overlap": 6},
            "violations": {
                name: violations(candidate_support[name])
                for name in ("K_prime", "H_prime")},
            "changed_entries": {
                "K_prime": changed_entries(K2, Kp2, ports),
                "H_prime": changed_entries(H2, Hp2, ports),
            },
            "formal_identities": {
                "C_times_C_inverse_equals_I": True,
                "K_prime_squared_equals_I": True,
                "K_prime_plus_H_prime_plus_B_prime_equals_I": True,
                "operator_unchanged_from_issue_28": True,
            },
        },
        "constraints": {
            "equation": "(q_T dot q_S)+(u_T_tgt dot u_S_src)=0 over F2 on every nonzero K_prime or H_prime edge",
            "rank_1_common": {
                "status": "UNSAT",
                "certificate": common_edges,
                "reason": "odd edges force u_0=u_2=1; the even K_prime edge (0,2) requires u_0*u_2=0",
            },
            "rank_1_separate": {
                "status": "UNSAT",
                "certificate": separate_edges,
                "reason": "odd edges force u_0_tgt=u_8_src=1; the even H_prime edge (0,8) requires their product to be 0",
            },
            "rank_2_common": {
                "status": "FEASIBLE_GRAM_ONLY",
                "appended_bits_coordinate_order": [8, 9],
                "appended_bits_low_bit_first": [[u_i & 1, (u_i >> 1) & 1] for u_i in u],
                "appended_vectors_as_masks": u,
                "lifted_address_masks": lifted,
                "checked_support_edges": len(union),
                "K_prime_edges_checked": len(candidate_support["K_prime"]),
                "H_prime_edges_checked": len(candidate_support["H_prime"]),
                "violations": 0,
            },
            "rank_2_original_baseline_support_audit": original_support_audit,
            "B_center_channel": {
                "matrix_unchanged": Bp2 == B2,
                "included_in_K_H_pairwise_cap": False,
                "center_root_geometry_reused": False,
                "note": "B remains the distinct coordinate-star center channel",
            },
        },
        "source_geometry_audit": {
            "source_ports_all_weight_three": True,
            "lifted_weight_counts": {"3": 26, "4": 6},
            "lifted_self_pairing_counts": {"0": 6, "1": 26},
            "lifted_coordinate_incidence": lifted_incidence,
            "original_coordinate_incidence": [12] * H,
            "paired_p_if_h_were_10": 5,
            "paired_port_count_if_p_were_5": 80,
            "existing_semantic_port_count": V,
            "all_norm_one_common_rank_2_extensions_possible": False,
            "norm_preserving_appended_vectors": isotropic_appends,
            "norm_preserving_append_pairings": [[dot_f2(x, y) for y in isotropic_appends]
                                                for x in isotropic_appends],
            "lifted_port_labels_injective": True,
            "lifted_port_span_rank": 10,
            "lifted_span_gram_rank": 10,
            "ambient_F2_10_dot_form_non_degenerate": True,
            "source_line_changed_for_nonzero_appends": 6,
            "zero_extended_old_target_hyperplane_dimension": 7,
            "new_target_orthogonal_hyperplane_dimension": 9,
            "new_target_hyperplane_dimension_gap": 2,
            "copied_star_scatter_geometry_reusable": False,
            "source_defined_encoder_decoder": "NOT PROVIDED",
            "arbitrary_dirty_signed_lift": "NOT PROVIDED",
            "paired_cube_geometry": "FAIL: six labels have weight four and self-pairing zero",
            "bit_H0_form_from_pr_130": "(I-J/9)/2 on Q^23, with q_S^T H0 q_S=1",
            "bit_H0_frame_compatibility": "NOT RUN; no bit-side map for these appended labels",
        },
        "negative_controls": {
            "global_orthogonal_isometry_cannot_repair_old_witness": {
                "pair": [0, 10], "old_dot": dot_f2(masks[0], masks[10]),
                "preserved_dot": True,
            },
            "r1_models_are_not_conflated": True,
            "coefficient_halves_reduced_mod_2": False,
        },
        "primary_status": "ADDRESS_OR_FRAME_OBSTRUCTION",
    }
    output = Path(__file__).with_name("receipt.json")
    output.write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n")
    print("baseline PASS: 32 ports, exact doubled B/H/K, source identities and support cap")
    print("Issue 28 fixed shear PASS: exact identities and 4+4 address violations reproduced")
    print("rank 1 common UNSAT and rank 1 separate-label UNSAT: exact three-edge certificates")
    print("rank 2 common Gram PASS on all 516 support pairs; source paired-cube geometry FAIL")
    print("rank 2 original supports PASS: K 128/0, H 384/0; B remains a separate center channel")
    print(f"receipt={output}")


if __name__ == "__main__":
    main()
