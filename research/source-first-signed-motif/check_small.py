#!/usr/bin/env python3
"""Exact standard-library checks for Issue 30's local motif and controls."""

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json


def dot2(left, right):
    return (left & right).bit_count() & 1


def address(pair_ids, selector):
    out = 0
    for j, pair_id in enumerate(pair_ids):
        out |= 1 << (2 * pair_id + ((selector >> j) & 1))
    return out


def gram(ports):
    return [[dot2(a, b) for b in ports] for a in ports]


def gram_rows_hex(matrix):
    return [format(sum(value << j for j, value in enumerate(row)), "08x")
            for row in matrix]


def gf2_rank(vectors):
    pivots = {}
    for value in vectors:
        while value:
            pivot = value.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = value
                break
            value ^= pivots[pivot]
    return len(pivots)


def identity(size):
    return [[Fraction(i == j) for j in range(size)] for i in range(size)]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(left, right):
    return [[sum((left[i][k] * right[k][j]
                  for k in range(len(right))), Fraction(0))
             for j in range(len(right[0]))]
            for i in range(len(left))]


def matrix_digest(matrix):
    canonical = [[f"{Fraction(value).numerator}/{Fraction(value).denominator}"
                  for value in row] for row in matrix]
    payload = json.dumps(canonical, separators=(",", ":")).encode("ascii")
    return sha256(payload).hexdigest()


def coefficient_counts(matrix):
    counts = {}
    for row in matrix:
        for value in row:
            key = str(Fraction(value))
            counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


def row_signature(matrix):
    signatures = []
    for i, row in enumerate(matrix):
        ones = sum(row[j] for j in range(len(row)) if j != i)
        zeros = len(row) - 1 - ones
        signatures.append({"off_diagonal_ones": ones,
                           "off_diagonal_zeros": zeros,
                           "diagonal": row[i]})
    return signatures


def candidate_motif():
    selectors = list(range(32))
    ports = [address(range(5), selector) for selector in selectors]
    binary_gram = gram(ports)
    span_rank = gf2_rank(ports)

    even = []
    odd = []
    for x in range(16):
        parity = x.bit_count() & 1
        even.append(address(range(5), x | (parity << 4)))
        odd.append(address(range(5), x | ((parity ^ 1) << 4)))

    walsh = [[Fraction(-1 if (x & y).bit_count() & 1 else 1, 4)
              for y in range(16)] for x in range(16)]
    operator = [[Fraction(0) for _ in range(32)] for _ in range(32)]
    for x in range(16):
        for y in range(16):
            operator[x][16 + y] = walsh[x][y]
            operator[16 + y][x] = walsh[x][y]

    assert len(set(ports)) == 32
    assert all((port.bit_count() == 5) for port in ports)
    assert all(binary_gram[i][i] == 1 for i in range(32))
    assert all(sig == row_signature(binary_gram)[0]
               for sig in row_signature(binary_gram))
    assert span_rank == 6
    assert matmul(walsh, transpose(walsh)) == identity(16)
    assert matmul(operator, operator) == identity(32)

    nonzero = 0
    orthogonal = 0
    for i, row in enumerate(operator):
        for j, value in enumerate(row):
            if value:
                nonzero += 1
                left = even[i] if i < 16 else odd[i - 16]
                right = odd[j - 16] if i < 16 else even[j]
                orthogonal += dot2(left, right) == 0
    assert nonzero == 512
    assert orthogonal == nonzero
    assert set(value for row in operator for value in row) == {
        Fraction(0), Fraction(1, 4), Fraction(-1, 4)
    }
    assert coefficient_counts(operator) == {
        "-1/4": 240, "0": 512, "1/4": 272
    }

    bad_sign = [row[:] for row in walsh]
    bad_sign[0][0] = -bad_sign[0][0]
    bad_sign_cross = sum((bad_sign[0][k] * bad_sign[1][k]
                          for k in range(16)), Fraction(0))
    assert bad_sign_cross == Fraction(-1, 8)
    bad_sign_gram = matmul(bad_sign, transpose(bad_sign))
    assert bad_sign_gram != identity(16)

    unscaled = [[4 * value for value in row] for row in walsh]
    unscaled_square = matmul(unscaled, transpose(unscaled))
    assert unscaled_square == [[Fraction(16 if i == j else 0)
                                for j in range(16)] for i in range(16)]

    same_parity_dot = dot2(ports[0], ports[3])
    self_dot = dot2(ports[0], ports[0])
    assert same_parity_dot == 1 and self_dot == 1

    h0_triple_norm = Fraction(3) - Fraction(9, 9)
    h0_triple_norm /= 2
    h0_five_norm = (Fraction(5) - Fraction(25, 9)) / 2
    assert h0_triple_norm == 1
    assert h0_five_norm == Fraction(10, 9)

    return {
        "address_width": 10,
        "port_count": 32,
        "selector_weight": 5,
        "port_masks_hex": [format(port, "03x") for port in ports],
        "gram_rows_hex_lsb_is_column_zero": gram_rows_hex(binary_gram),
        "gram_diagonal_all_one": True,
        "gram_row_signature": row_signature(binary_gram)[0],
        "address_span_rank_gf2": span_rank,
        "walsh_sign_rows_x_then_y": [
            "".join("+" if value > 0 else "-" for value in row)
            for row in walsh
        ],
        "K_nonzero_count": nonzero,
        "K_coefficients": coefficient_counts(operator),
        "K_matrix_sha256_row_major_fraction_text": matrix_digest(operator),
        "K_support_orthogonal_count": orthogonal,
        "K_squared_identity": True,
        "walsh_squared_identity": True,
        "negative_controls": {
            "removed_one_walsh_sign": {
                "expected_failure_observed": bad_sign_cross != 0,
                "row_0_dot_row_1": str(bad_sign_cross),
            },
            "removed_one_quarter_scaling": {
                "expected_failure_observed": unscaled_square != identity(16),
                "unscaled_AA_transpose_diagonal": "16",
            },
            "same_parity_distinct_port_edge": {
                "selectors": [0, 3],
                "cap_dot": same_parity_dot,
                "expected_failure_observed": same_parity_dot != 0,
            },
            "self_edge": {
                "selector": 0,
                "cap_dot": self_dot,
                "expected_failure_observed": self_dot != 0,
                "port_norm_remains_one": self_dot == 1,
            },
            "free_relabel_from_PR144_p4_h8": {
                "candidate_span_rank_gf2": span_rank,
                "PR144_p4_h8_span_rank_gf2": None,
                "candidate_port_weight": 5,
                "PR144_p4_h8_port_weight": 3,
            },
            "unchanged_PR130_H0_reuse": {
                "ambient_dimension": 23,
                "formal_coordinate_check_only": True,
                "triple_indicator_norm": str(h0_triple_norm),
                "five_indicator_norm": str(h0_five_norm),
                "expected_failure_observed": h0_five_norm != 1,
            },
        },
    }


def pr144_p4_h8_control():
    cubes = list(combinations(range(4), 3))
    ports = []
    cube_of = []
    for cube_index, cube in enumerate(cubes):
        for selector in range(8):
            ports.append(address(cube, selector))
            cube_of.append(cube_index)

    size = len(ports)
    whole_B = [[Fraction((ports[i] & ports[j]).bit_count() - 1, 2)
                for j in range(size)] for i in range(size)]
    star_B = [[Fraction((ports[i] & ports[j]).bit_count(), 2) -
               Fraction(3, 6) for j in range(size)] for i in range(size)]
    block_B = [[(whole_B[i][j] if cube_of[i] == cube_of[j]
                 else Fraction(0)) for j in range(size)] for i in range(size)]
    identity_32 = identity(size)
    K = [[identity_32[i][j] - block_B[i][j]
          for j in range(size)] for i in range(size)]
    H = [[block_B[i][j] - whole_B[i][j]
          for j in range(size)] for i in range(size)]

    assert size == 32 and len(cubes) == 4
    assert all(port.bit_count() == 3 for port in ports)
    assert all(dot2(port, port) == 1 for port in ports)
    assert star_B == whole_B
    assert matmul(K, K) == identity_32
    assert all(K[i][j] + H[i][j] + whole_B[i][j] == identity_32[i][j]
               for i in range(size) for j in range(size))

    support_counts = {
        "K": sum(value != 0 for row in K for value in row),
        "H": sum(value != 0 for row in H for value in row),
        "B": sum(value != 0 for row in whole_B for value in row),
    }
    assert support_counts == {"K": 128, "H": 384, "B": 544}
    orthogonal_supports = {}
    for name, matrix in (("K", K), ("H", H)):
        orthogonal_supports[name] = sum(
            dot2(ports[i], ports[j]) == 0
            for i, row in enumerate(matrix)
            for j, value in enumerate(row) if value
        )
        assert orthogonal_supports[name] == support_counts[name]

    return {
        "p": 4,
        "h": 8,
        "cube_count": len(cubes),
        "ports": size,
        "port_weight": 3,
        "port_masks_hex": [format(port, "02x") for port in ports],
        "gram_rows_hex_lsb_is_column_zero": gram_rows_hex(gram(ports)),
        "address_span_rank_gf2": gf2_rank(ports),
        "matrix_nonzero_counts": support_counts,
        "matrix_coefficients": {
            "K": coefficient_counts(K),
            "H": coefficient_counts(H),
            "B": coefficient_counts(whole_B),
        },
        "matrix_sha256_row_major_fraction_text": {
            "K": matrix_digest(K),
            "H": matrix_digest(H),
            "B": matrix_digest(whole_B),
        },
        "K_squared_identity": True,
        "K_plus_H_plus_B_identity": True,
        "copied_coordinate_star_scatter_equals_B": True,
        "K_H_support_orthogonal_counts": orthogonal_supports,
    }


def main():
    candidate = candidate_motif()
    control = pr144_p4_h8_control()
    candidate["negative_controls"]["free_relabel_from_PR144_p4_h8"][
        "PR144_p4_h8_span_rank_gf2"] = control["address_span_rank_gf2"]
    relabel = candidate["negative_controls"]["free_relabel_from_PR144_p4_h8"]
    relabel["expected_failure_observed"] = (
        relabel["candidate_span_rank_gf2"] !=
        relabel["PR144_p4_h8_span_rank_gf2"] or
        relabel["candidate_port_weight"] !=
        relabel["PR144_p4_h8_port_weight"]
    )
    assert relabel["expected_failure_observed"]
    assert control["address_span_rank_gf2"] == 8

    result = {
        "schema": "source-first-signed-motif-check-v1",
        "primary_status": "MULTIPLICATION_PORT_TYPE_MISSING",
        "method": "Python standard library; exact integers and fractions only",
        "candidate_5_pair_motif": candidate,
        "PR144_original_p4_h8_positive_control": control,
        "scope": {
            "p5_full_PR144_family_port_count": 8 * len(
                list(combinations(range(5), 3))
            ),
            "candidate_is_full_PR144_p5_family": False,
            "typed_5_port_decoder": "NOT RUN",
        },
    }
    assert result["scope"]["p5_full_PR144_family_port_count"] == 8 * 10
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
