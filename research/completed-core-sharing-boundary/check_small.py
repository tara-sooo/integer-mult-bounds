#!/usr/bin/env python3
"""Exact, bounded controls for the pinned core-sharing equations.

This checks algebraic subcases only. It does not replay a physical word or
prove an all-size multiplication bound.
"""
from fractions import Fraction
import sys


def dot(a, b):
    return (a & b).bit_count() & 1


def inverse_gf2(matrix):
    n = len(matrix)
    rows = []
    for i, row in enumerate(matrix):
        left = sum((value & 1) << j for j, value in enumerate(row))
        rows.append(left | (1 << (n + i)))
    for col in range(n):
        pivot = next((i for i in range(col, n) if (rows[i] >> col) & 1), None)
        if pivot is None:
            return None
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for i in range(n):
            if i != col and ((rows[i] >> col) & 1):
                rows[i] ^= rows[col]
    return [[(rows[i] >> (n + j)) & 1 for j in range(n)] for i in range(n)]


def q(basis, x):
    """Return wt(P_basis x) mod 4 for a nondegenerate binary subspace."""
    gram = [[dot(a, b) for b in basis] for a in basis]
    inverse = inverse_gf2(gram)
    assert inverse is not None, (basis, gram)
    rhs = [dot(a, x) for a in basis]
    coefficients = [sum(inverse[i][j] * rhs[j] for j in range(len(rhs))) & 1
                    for i in range(len(rhs))]
    projection = 0
    for vector, coefficient in zip(basis, coefficients):
        if coefficient:
            projection ^= vector
    return projection.bit_count() % 4


def signed_core(dirty, x):
    """M;-J;M^-1;V;M;J;M^-1;-V for M(a,b)=(a+b,b)."""
    a, b = dirty
    y = -(a + b)
    z = (a, b + x)
    z = (z[0] + z[1], z[1])
    y += z[0]
    z = (z[0] - z[1], z[1])
    z = (z[0], z[1] - x)
    return z, y


def mul_gaussian(left, right):
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c


def main():
    if sys.flags.optimize:
        raise SystemExit("run without -O so assertions remain enabled")

    v128, r128, n128, m128 = 2024, 28705, 2024**2, 576
    old_aux128 = 2 * v128 * r128
    old_w128 = 2 * n128 + old_aux128
    grouped_aux128 = 2 * 87 * r128
    grouped_w128 = 2 * n128 + grouped_aux128
    old_exterior_mass128 = old_aux128 * (m128 - 24)
    grouped_exterior_count128 = 2 * 4 * r128
    grouped_exterior_mass128 = grouped_exterior_count128 * 384
    assert (old_w128, grouped_w128) == (124390992, 13187822)
    assert old_exterior_mass128 == 64141207680
    assert (grouped_exterior_count128, grouped_exterior_mass128) == (229640, 88181760)
    assert 576 * grouped_w128 - 7594323392 == 1862080

    w130_complex = 2 * 2024 + 3 * 28705
    w130_bit = 2 * 1771 + 3 * 28866
    assert (w130_complex, 70 * w130_complex - 6309018) == (90163, 2392)
    assert (w130_bit, 67 * w130_bit - 6037356) == (90140, 2024)
    assert 67 * 90140 - 6037356 == 2024

    w144 = 2 * 1760 + 26417
    assert (w144, 72 * w144 - 2153528) == (29937, 1936)
    assert 2 * 1760 + 3 * 26417 == 82771

    group83 = (
        (0, 1, 2), (1, 2, 5), (6, 7, 8), (7, 8, 11),
        (12, 13, 14), (13, 14, 17), (18, 19, 20), (19, 20, 23),
    )
    labels = [sum(1 << i for i in triple) for triple in group83]
    gram = [[dot(a, b) for b in labels] for a in labels]
    assert gram == [[int(i == j) for j in range(8)] for i in range(8)]
    assert 24 * len(labels) == 192
    assert 576 - 24 * len(labels) == 384

    u, v, uv = [1], [2], [1, 2]
    assert all((q(u, x) + q(v, x)) % 4 == q(uv, x) for x in range(16))
    assert q([0b111], 0b111) == 3  # the source's triple-line phase is -i

    u_bad, v_bad, uv_bad = [1], [0b0011, 0b0110], [1, 0b0011, 0b0110]
    bad_exponents = (q(u_bad, 1), q(v_bad, 1), q(uv_bad, 1))
    assert bad_exponents == (1, 2, 1)
    assert (bad_exponents[0] + bad_exponents[1]) % 4 != bad_exponents[2]

    for a in range(-2, 3):
        for b in range(-2, 3):
            for x in range(-2, 3):
                restored, increment = signed_core((a, b), x)
                assert restored == (a, b)
                assert increment == x
    unrestored = (1, 1)  # M V(1) without the inverse cleanup
    assert unrestored != (0, 0)

    alpha = (Fraction(1, 2), Fraction(1, 2))
    beta = (Fraction(1, 2), Fraction(-1, 2))
    full_f_times_gauge_inverse_amp_10 = mul_gaussian(beta, alpha)
    actual_raw_amp_10 = (Fraction(0), Fraction(0))
    assert full_f_times_gauge_inverse_amp_10 == (Fraction(1, 2), Fraction(0))
    assert actual_raw_amp_10 != full_f_times_gauge_inverse_amp_10

    partial_amp_10 = beta
    full_amp_10 = full_f_times_gauge_inverse_amp_10
    assert partial_amp_10 == (Fraction(1, 2), Fraction(-1, 2))
    assert partial_amp_10 != full_amp_10

    print("PASS exact PR128/130/144 allocation, child-mass and deficit arithmetic")
    print("PASS source group groups[83]: Gram matrix I; dim 192; complement width 384")
    print("PASS orthogonal phase identity on all 16 Walsh coordinates; triple phase -i")
    print(f"REJECT nonorthogonal merge at x=e0: q={bad_exponents}, phases -i vs i")
    print("PASS arbitrary dirty two-role signed core; REJECT omitted cleanup")
    print("REJECT dropped entrance gauge and unpaid complement in exact two-coordinate model")


if __name__ == "__main__":
    main()
