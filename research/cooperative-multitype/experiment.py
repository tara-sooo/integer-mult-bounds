#!/usr/bin/env python3
"""Exact finite checker for the cooperative Boolean pair toy."""

from fractions import Fraction as Q
from itertools import product


def f(bits):
    if len(bits) == 1:
        return bits[0]
    mid = len(bits) // 2
    return f(bits[:mid]) ^ f(bits[mid:])


def g(bits):
    if len(bits) == 1:
        return bits[0] ^ 1
    mid = len(bits) // 2
    return f(bits[:mid]) & g(bits[mid:])


def c(bits):
    if len(bits) == 1:
        return bits[0], bits[0] ^ 1
    mid = len(bits) // 2
    f_left = f(bits[:mid])
    f_right, g_right = c(bits[mid:])
    return f_left ^ f_right, f_left & g_right


def work(depth):
    """(F,G,C) gates plus one charged frame unit per recursive call."""
    values = (0, 1, 1)
    for _ in range(depth):
        f_work, g_work, c_work = values
        values = (
            2 * f_work + 3,          # two frames, one XOR
            f_work + g_work + 3,     # two frames, one AND
            f_work + c_work + 4,     # two frames, two gates
        )
    return values


def main():
    for depth in range(3):
        n = 1 << depth
        for bits in product((0, 1), repeat=n):
            assert c(bits) == (f(bits), g(bits))

    # These child-count matrices are lower triangular, so their exact spectral
    # radii are their largest diagonal entries: 2 for both systems.
    baseline = ((2, 0), (1, 1))
    cooperative = ((2, 0, 0), (1, 1, 0), (1, 0, 1))
    assert baseline == ((2, 0), (1, 1))
    assert cooperative == ((2, 0, 0), (1, 1, 0), (1, 0, 1))
    assert baseline[0][0] == cooperative[0][0] == 2
    assert tuple(baseline[i][i] for i in range(2)) == (2, 1)
    assert tuple(cooperative[i][i] for i in range(3)) == (2, 1, 1)

    widths = (1, 1, 2)
    c_row_per_output = sum(
        Q(cooperative[2][j] * widths[j], widths[2]) for j in range(3)
    )
    assert c_row_per_output == Q(3, 2)
    for q in (0, 1, 2):
        scale = Q(1, 2) ** q
        assert max(baseline[i][i] * scale for i in range(2)) == max(
            cooperative[i][i] * scale for i in range(3)
        )
    assert max(baseline[i][i] * Q(1, 2) for i in range(2)) == 1

    # A free G-to-F conversion changes G_1(1,0): the correct result is 1.
    assert g((1, 0)) == 1
    illegal_g = f((1,)) & f((0,))
    assert illegal_g == 0 and illegal_g != g((1, 0))

    costs = {depth: work(depth) for depth in (0, 1, 2, 4, 8)}
    assert costs[1] == (3, 4, 5)
    assert costs[4] == (45, 46, 50)
    assert all(c_work < f_work + g_work for depth, (f_work, g_work, c_work)
               in costs.items() if depth > 0)

    print("truth_tables=depth_0_to_2 PASS")
    print("child_matrices=baseline_diag(2,1); cooperative_diag(2,1,1)")
    print(f"C_row_per_output={c_row_per_output}")
    print("spectral_radius=q-scaled baseline == cooperative; q=1 gives 1")
    print(f"depth_1_work(F,G,C)={costs[1]}; depth_4_work(F,G,C)={costs[4]}")
    print("illegal_free_conversion=detected")
    print("result=OPEN_INTERFACE_OBSTRUCTION")


if __name__ == "__main__":
    main()
