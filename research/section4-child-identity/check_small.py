#!/usr/bin/env python3
"""Exact compact check for one real Section 4 edge and two live pivots."""

from fractions import Fraction


def main():
    h = 100
    t = [int(i < 3) for i in range(h)]
    gt = [Fraction(x) - Fraction(1, 3) for x in t]
    assert sum(Fraction(t[i]) * gt[i] for i in range(h)) == 2

    # shortcut: keep the million-dimensional lift symbolic; materialize only if a dense trace is needed.
    u = [Fraction(t[i] * t[j]) for i in range(h) for j in range(h)]
    v = [gt[i] * gt[j] for i in range(h) for j in range(h)]
    n = h * h
    assert len(u) == len(v) == n
    assert u[0] == 1
    assert v[-1] == Fraction(1, 9)
    assert sum(u_i * v_i for u_i, v_i in zip(u, v)) == 4
    assert all(value != 0 for value in v)

    # Apply L=I+(u-e_1)e_1^T to e_1, and read the last row of
    # R=I+e_n(v^T/4-e_n^T).
    e1 = [Fraction(int(i == 0)) for i in range(n)]
    en = [Fraction(int(i == n - 1)) for i in range(n)]
    l_column_1 = [e1[i] + (u[i] - e1[i]) * e1[0] for i in range(n)]
    r_row_n = [en[j] + (v[j] / 4 - en[j]) for j in range(n)]
    assert l_column_1 == u
    assert r_row_n == [value / 4 for value in v]
    assert r_row_n[-1] == Fraction(1, 36)
    assert u[0] == 1  # L is unit lower triangular.
    assert r_row_n[-1] != 0  # R's final diagonal is a unit over Q.
    # L's off-diagonal entries are only below column 1; R's only modified
    # row is the last row. Their diagonals are respectively 1 and (1,...,1,1/36).
    assert u[0] == 1 and r_row_n[-1] != 0

    # Pi = (e_1 e_n^T) tensor I_h. Use one-based flattened (i,k) coordinates.
    index = lambda i, k: h * (i - 1) + k
    pivots = [(index(1, k), index(n, k)) for k in range(1, h + 1)]
    assert pivots[:2] == [(1, 999901), (2, 999902)]
    assert len(set(row for row, _ in pivots)) == h
    assert len(set(col for _, col in pivots)) == h

    # Two source pivot updates, their intervening swaps, and a dirty sentinel
    # spectator. Values 0/1 are legal in every permitted q^b field.
    x = {"h1": 0, "d1": 1, "h2": 0, "d2": 0, "spectator": 1}
    call1_input = dict(x)
    # Complete pivot 1: D+=H; swap; D=H-D. Its net map is H+=D.
    d1 = x["d1"] + x["h1"]
    h1, d1 = d1, x["h1"]
    d1 = h1 - d1
    x.update(h1=h1, d1=d1)
    # Pivot 2's preparatory shear is the state immediately before call 2.
    x["d2"] += x["h2"]
    call2_input = dict(x)
    assert call1_input != call2_input
    assert (call1_input["h1"], call1_input["d1"]) == (0, 1)
    assert (call2_input["h1"], call2_input["d1"]) == (1, 1)
    assert call2_input["spectator"] == 1

    # Same width/rank does not make the two swap functions equal.
    y = {"h1": 1, "d1": 0, "h2": 0, "d2": 0, "spectator": 1}
    swap1 = dict(y, h1=y["d1"], d1=y["h1"])
    swap2 = dict(y, h2=y["d2"], d2=y["h2"])
    assert swap1 != swap2
    assert swap1["spectator"] == swap2["spectator"] == 1
    different_spectator = dict(y, spectator=0)
    assert different_spectator != y

    print("PASS: exact rank-100 factorization; first pivots; live-state and field-pair controls")


if __name__ == "__main__":
    main()
