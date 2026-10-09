#!/usr/bin/env python3
"""Exact p=4 paired-cube baseline and one predeclared cross-cube shear."""

# shortcut: p=4 and the first lambda=+1 shear only; extend only after support passes.

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


P = 4
H = 2 * P
V = 8 * (P * (P - 1) * (P - 2) // 6)


def eye(n, scale=1):
    return [[scale * int(i == j) for j in range(n)] for i in range(n)]


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def madd(a, b, sign=1):
    return [[x + sign * y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def digest(matrix):
    payload = json.dumps(matrix, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def q(value_twice):
    return str(Fraction(value_twice, 2))


def port_order():
    """PR 144 Graph.labels: combinations, then lexicographic selector bits."""
    return [(cube, bits, tuple(2 * i + bit for i, bit in zip(cube, bits)))
            for cube in combinations(range(P), 3)
            for bits in product(range(2), repeat=3)]


def address_mask(port):
    return sum(1 << coordinate for coordinate in port)


def dot_f2(a, b):
    return ((a & b).bit_count() & 1)


def rank_f2(rows):
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


def source_h_coefficient(source_cube, source_bits, target_cube, target_bits):
    """PR 144 F/A/G channel coefficient for one source in one target root."""
    shared = sorted(set(source_cube) & set(target_cube))
    if not shared:
        return Fraction(1, 2)
    if len(shared) == 1:
        i = shared[0]
        si, ti = source_cube.index(i), target_cube.index(i)
        return Fraction(1, 2) if source_bits[si] == 1 - target_bits[ti] else Fraction(0)
    if len(shared) == 2:
        i, j = shared
        ai, aj = source_bits[source_cube.index(i)], source_bits[source_cube.index(j)]
        ti, tj = target_bits[target_cube.index(i)], target_bits[target_cube.index(j)]
        if (ai ^ aj) == (ti ^ tj):
            return Fraction((2 * ti - 1) * (1 - 2 * ai), 2)
        return Fraction(0)
    return Fraction(0)


def first_mismatch(actual, expected):
    for i, row in enumerate(actual):
        for j, value in enumerate(row):
            if value != expected[i][j]:
                return [i, j, value, expected[i][j]]
    return None


def changed_nonzero(before, after, ports):
    result = []
    for i in range(V):
        for j in range(V):
            old, new = before[i][j], after[i][j]
            if old == new or (old == 0 and new == 0):
                continue
            t = ports[i][2]
            s = ports[j][2]
            result.append({
                "row": i,
                "column": j,
                "T": list(t),
                "S": list(s),
                "T_address_mask": address_mask(t),
                "S_address_mask": address_mask(s),
                "before": q(old),
                "after": q(new),
                "address_dot_F2": dot_f2(address_mask(t), address_mask(s)),
            })
    return result


def support_audit(matrix, ports):
    nonzero = 0
    violations = []
    for i in range(V):
        for j in range(V):
            if matrix[i][j] == 0:
                continue
            nonzero += 1
            t = ports[i][2]
            s = ports[j][2]
            parity = dot_f2(address_mask(t), address_mask(s))
            if parity:
                violations.append({
                    "row": i,
                    "column": j,
                    "T": list(t),
                    "S": list(s),
                    "T_address_mask": address_mask(t),
                    "S_address_mask": address_mask(s),
                    "coefficient": q(matrix[i][j]),
                    "address_dot_F2": parity,
                })
    return nonzero, violations


def main():
    ports = port_order()
    assert len(ports) == V == 32
    assert len({address_mask(port[2]) for port in ports}) == V
    index = {(cube, bits): i for i, (cube, bits, _) in enumerate(ports)}
    coordinate_incidence = [sum((address_mask(coords) >> coordinate) & 1
                                for _, _, coords in ports) for coordinate in range(H)]
    star_ranks = [rank_f2([address_mask(coords) for _, _, coords in ports
                           if (address_mask(coords) >> coordinate) & 1])
                  for coordinate in range(H)]
    assert coordinate_incidence == [12] * H
    assert star_ranks == [6] * H and sum(star_ranks) == H * (H - 2) == 48
    source_data_histogram = {"1": V, "2": V, str(H - 4): V}
    target_data_histogram = {"1": 3 * V, str(H - 4): V}
    assert sum(int(rank) * count for rank, count in source_data_histogram.items()) == V * (H - 1)
    assert sum(int(rank) * count for rank, count in target_data_histogram.items()) == V * (H - 1)
    side_root_group_sizes = [1, 2, 4, 4, 8, 8, 8]
    assert sum(side_root_group_sizes) == 35

    # Every coefficient is stored doubled, so no 1/2 is ever reduced mod 2.
    B2 = [[(len(set(t[2]) & set(s[2])) - 1) for s in ports] for t in ports]
    Bblock2 = [[B2[i][j] if ports[i][0] == ports[j][0] else 0
                for j in range(V)] for i in range(V)]
    K2 = madd(eye(V, 2), Bblock2, -1)
    H2 = madd(Bblock2, B2, -1)
    I2, I4 = eye(V, 2), eye(V, 4)

    # P-A source identity, with P the antipode and A distance-one adjacency.
    PminusA = [[0] * V for _ in range(V)]
    for i, (cube_t, bits_t, _) in enumerate(ports):
        for j, (cube_s, bits_s, _) in enumerate(ports):
            if cube_t != cube_s:
                continue
            distance = sum(x != y for x, y in zip(bits_t, bits_s))
            PminusA[i][j] = int(distance == 3) - int(distance == 1)
    assert K2 == PminusA
    assert madd(madd(K2, H2), B2) == I2
    assert mm(K2, K2) == I4
    assert all(K2[i][j] == K2[j][i] for i in range(V) for j in range(V))
    assert all(K2[i][j] in (-1, 0, 1) for i in range(V) for j in range(V))

    # Match PR 144's direct B coefficients, copied-star scatter, and F/A/G H roots.
    for i, (cube_t, bits_t, t) in enumerate(ports):
        for j, (cube_s, bits_s, s) in enumerate(ports):
            overlap = len(set(t) & set(s))
            star = sum(Fraction(1, 3) if coordinate in t else Fraction(-1, 6)
                       for coordinate in s)
            assert star == Fraction(overlap - 1, 2)
            assert B2[i][j] == overlap - 1
            expected_h = Fraction(0) if cube_t == cube_s else source_h_coefficient(
                cube_s, bits_s, cube_t, bits_t)
            assert Fraction(H2[i][j], 2) == expected_h, (i, j, expected_h, H2[i][j])

    baseline_support = {}
    baseline_h0_support = {}
    for name, matrix in (("K", K2), ("H", H2)):
        count, violations = support_audit(matrix, ports)
        assert not violations, (name, violations[:1])
        baseline_support[name] = {"nonzero_entries": count, "orthogonality_violations": 0}
        h0_bad = []
        for i in range(V):
            for j in range(V):
                if matrix[i][j] and len(set(ports[i][2]) & set(ports[j][2])) != 1:
                    h0_bad.append([i, j])
        baseline_h0_support[name] = len(h0_bad)

    # PR 27's existing B identity is a source equality, not new work.
    for i, (cube_t, bits_t, t) in enumerate(ports):
        for j, (cube_s, bits_s, s) in enumerate(ports):
            X = 1
            z = sum(int(coordinate not in s) for coordinate in t)
            assert Fraction(X, 1) - Fraction(z, 2) == Fraction(B2[i][j], 2)

    # Predeclared candidate: first lexicographic cross-cube pair, lambda=+1.
    cross_pair = next((i, j) for i in range(V) for j in range(V)
                      if ports[i][0] != ports[j][0])
    a, b = cross_pair
    assert (a, b) == (0, 8)
    Eab = [[int(i == a and j == b) for j in range(V)] for i in range(V)]
    C = madd(eye(V), Eab)
    Cinv = madd(eye(V), Eab, -1)
    assert mm(C, Cinv) == eye(V) and mm(Cinv, C) == eye(V)
    assert mm(Eab, Eab) == [[0] * V for _ in range(V)]
    Kp2 = mm(mm(C, K2), Cinv)
    Bp2 = [row[:] for row in B2]
    Hp2 = madd(madd(I2, Kp2, -1), Bp2, -1)
    assert mm(Kp2, Kp2) == I4
    assert madd(madd(Kp2, Hp2), Bp2) == I2

    changed = {
        "K_prime": changed_nonzero(K2, Kp2, ports),
        "H_prime": changed_nonzero(H2, Hp2, ports),
    }
    assert all(changed.values())
    candidate_support = {}
    for name, matrix in (("K_prime", Kp2), ("H_prime", Hp2)):
        count, violations = support_audit(matrix, ports)
        changed_here = changed[name]
        assert all(entry["address_dot_F2"] in (0, 1) for entry in changed_here)
        assert any(v["row"] == entry["row"] and v["column"] == entry["column"]
                   for v in violations for entry in changed_here)
        candidate_support[name] = {
            "nonzero_entries": count,
            "orthogonality_violations": len(violations),
            "violations": violations,
        }

    witness_index = index[((0, 1, 3), (0, 1, 0))]
    witness = next(v for v in candidate_support["K_prime"]["violations"]
                   if v["row"] == a and v["column"] == witness_index)
    assert witness_index == 10
    assert ports[a][2] == (0, 2, 4) and ports[b][2] == (0, 2, 6)
    assert ports[witness_index][2] == (0, 3, 6)
    assert K2[a][witness_index] == 0 and K2[b][witness_index] == -1
    assert Kp2[a][witness_index] == -1
    assert witness["coefficient"] == "-1/2" and witness["address_dot_F2"] == 1

    # Bit-side is a separate address form and scalar ring; do not reduce 1/2 in F2.
    no_half_inverse_in_f2 = not any((2 * bit) % 2 == 1 for bit in (0, 1))
    assert no_half_inverse_in_f2
    candidate_h0_support = {}
    for name, matrix in (("K_prime", Kp2), ("H_prime", Hp2)):
        bad = []
        for i in range(V):
            for j in range(V):
                overlap = len(set(ports[i][2]) & set(ports[j][2]))
                if matrix[i][j] and overlap != 1:
                    bad.append([i, j])
        candidate_h0_support[name] = {
            "nonzero_entries": sum(value != 0 for row in matrix for value in row),
            "nonorthogonal_entries_under_H0": len(bad),
        }

    # Negative controls: omit the inverse, use the wrong conjugating sign, and undo dirty data wrongly.
    omitted_inverse = mm(C, K2)
    omitted_square = mm(omitted_inverse, omitted_inverse)
    assert omitted_square != I4
    wrong_sign = mm(mm(C, K2), C)
    wrong_sign_square = mm(wrong_sign, wrong_sign)
    assert wrong_sign_square != I4

    x, dirty, target = Fraction(3), Fraction(7), Fraction(11)
    J, M, Vmap = Fraction(1, 2), Fraction(2), Fraction(1)
    y = target - J * M * dirty
    z = dirty + Vmap * x
    z *= M
    y += J * z
    z /= M
    correct_dirty = z - Vmap * x
    assert (y, correct_dirty) == (target + x, dirty)
    wrong_dirty_sign = z + Vmap * x
    omitted_dirty_undo = z
    assert wrong_dirty_sign == dirty + 2 * x
    assert omitted_dirty_undo == dirty + x

    # A tautological H' cannot pass the lawfulness guard, and B' reuses Issue 27's exact B.
    assert Hp2 == madd(madd(I2, Kp2, -1), Bp2, -1)
    assert Bp2 == B2 and digest(Bp2) == digest(B2)
    assert candidate_support["K_prime"]["orthogonality_violations"] > 0
    assert candidate_support["H_prime"]["orthogonality_violations"] > 0
    primary_status = "CROSS_CUBE_SUPPORT_OBSTRUCTION"
    assert primary_status != "NEW_SIGNED_DECOMPOSITION_EXACT_SMALL"

    coefficient_counts = {}
    for name, matrix in (("B", B2), ("H", H2), ("K", K2),
                         ("B_prime", Bp2), ("H_prime", Hp2), ("K_prime", Kp2)):
        values = Counter(value for row in matrix for value in row)
        coefficient_counts[name] = {q(value): values[value] for value in sorted(values)}

    receipt = {
        "schema": "new-signed-reduction-small-exact-v1",
        "primary_status": primary_status,
        "scope": "FAST; one predeclared lambda=+1 shear at the first lexicographic cross-cube port pair only",
        "ports": [{"index": i, "cube": list(cube), "selector_bits": list(bits),
                   "coordinates": list(coords), "address_mask": address_mask(coords)}
                  for i, (cube, bits, coords) in enumerate(ports)],
        "baseline": {
            "p": P, "h": H, "port_count": V,
            "coefficient_encoding": "all matrices are exact doubled entries: stored value n means coefficient n/2",
            "B_doubled": B2, "H_doubled": H2, "K_doubled": K2,
            "matrix_sha256": {"B_doubled": digest(B2), "H_doubled": digest(H2),
                              "K_doubled": digest(K2)},
            "coefficient_counts": {k: coefficient_counts[k] for k in ("B", "H", "K")},
            "identities": {
                "K_plus_H_plus_B_equals_I": True,
                "K_equals_P_minus_A_over_2": True,
                "K_inverse_equals_K": True,
                "K_squared_equals_I": True,
                "copied_star_scatter_equals_B": True,
                "source_fa_g_h_equals_H": True,
                "issue27_zeta_B_formula_equals_B": True,
            },
            "support": baseline_support,
            "physical_source_profile": {
                "coordinate_incidence": coordinate_incidence,
                "star_ranks": star_ranks,
                "copied_center_rank_sum": sum(star_ranks),
                "source_data_histogram": source_data_histogram,
                "target_data_histogram": target_data_histogram,
                "side_root_group_sizes_per_cube": side_root_group_sizes,
                "side_root_uses": len(ports) // 8 * sum(side_root_group_sizes),
                "copied_center_roots": H,
            },
        },
        "candidate": {
            "lambda": 1,
            "a": {"index": a, "cube": list(ports[a][0]), "selector_bits": list(ports[a][1]),
                  "coordinates": list(ports[a][2])},
            "b": {"index": b, "cube": list(ports[b][0]), "selector_bits": list(ports[b][1]),
                  "coordinates": list(ports[b][2])},
            "E_ab_convention": "row a, column b",
            "C_nonidentity_entry": {"row": a, "column": b, "value": 1},
            "C_inverse_nonidentity_entry": {"row": a, "column": b, "value": -1},
            "K_prime_doubled": Kp2, "H_prime_doubled": Hp2, "B_prime_doubled": Bp2,
            "matrix_sha256": {"K_prime_doubled": digest(Kp2), "H_prime_doubled": digest(Hp2),
                              "B_prime_doubled": digest(Bp2)},
            "coefficient_counts": {k: coefficient_counts[k]
                                   for k in ("B_prime", "H_prime", "K_prime")},
            "changed_nonzero_entries": changed,
            "support": candidate_support,
            "named_obstruction": witness,
            "formal_identities": {"K_prime_squared_equals_I": True,
                                  "K_prime_plus_H_prime_plus_B_prime_equals_I": True},
            "lawful_orthogonal_support": False,
        },
        "negative_controls": {
            "selected_cross_cube_shear_cap": "FAIL as candidate; exact obstruction recorded",
            "omitted_C_inverse": {"K_squared_equals_I": False,
                                  "first_doubled_entry_mismatch": first_mismatch(omitted_square, I4)},
            "wrong_inverse_phase_C_K_C": {"K_squared_equals_I": False,
                                           "first_doubled_entry_mismatch": first_mismatch(wrong_sign_square, I4)},
            "dirty_cleanup": {"correct": {"target": str(y), "dirty_after": str(correct_dirty)},
                              "wrong_inverse_sign_dirty_after": str(wrong_dirty_sign),
                              "omitted_dirty_undo_dirty_after": str(omitted_dirty_undo)},
        },
        "false_success_guards": {
            "H_prime_definition_is_tautological": True,
            "tautology_alone_accepted_as_success": False,
            "B_prime_reuses_issue27_exact_B": True,
            "reused_B_accepted_as_new_work": False,
            "positive_candidate_status": False,
        },
        "bit_side": {
            "status": "NO BIT OPERATOR CLAIMED; scalar/role bridge NOT RUN after the complex cap failure",
            "half_reduced_mod_2": False,
            "2x_equals_1_has_no_solution_in_F2": no_half_inverse_in_f2,
            "H0_pairing_for_two_triple_addresses": "(|T intersection S|-1)/2; this is a separate rational address form",
            "baseline_nonorthogonal_counts_under_H0": baseline_h0_support,
            "candidate_nonorthogonal_counts_under_H0": candidate_h0_support,
            "minimum_missing_lemma": "an independently typed F2/H0-legal supplier and decoder for a surviving new operator",
        },
        "focused_status": "NOT RUN",
        "full_status": "NOT RUN",
    }
    path = Path(__file__).with_name("small_exact_receipt.json")
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print("FAST baseline exact matrices PASS: 32 ports, 1,024 coefficients each; K^2=I; K/H support legal")
    print("FAST source/frame ledger PASS: incidence=12, star ranks=6x8, ell=48, H roots=140")
    print("FAST candidate formal identities PASS; cross-cube physical support FAIL with exact witness")
    print(f"selected shear: a={a}, b={b}, changed K entries={len(changed['K_prime'])}, "
          f"changed H entries={len(changed['H_prime'])}")
    print("negative controls PASS: omitted inverse, wrong phase, dirty undo")
    print("receipt=" + str(path))


if __name__ == "__main__":
    main()
