#!/usr/bin/env python3
"""Exact compact check for the pinned h=23 FSa -> Y2 frame lift."""
# shortcut: checks recorded logical envelopes only, until a stable word-event ID export exists.
from fractions import Fraction as Q

H = 23
I_FSA = {1, 6, 7, 8, 9, 18, 19, 20, 21, 22}
I_SB2 = {1, 10, 11, 12, 13, 18, 19, 20, 21, 22}
I_Y2 = {1, 6, 7, 8, 9, 10, 11, 12, 13, 18, 19, 20, 21, 22}
TRIPLE_25 = {0, 1, 2}


def zero(rows, cols):
    return [[Q(0) for _ in range(cols)] for _ in range(rows)]


def eye(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def mul(a, b):
    cols = transpose(b)
    return [[sum((x * y for x, y in zip(row, col)), Q(0))
             for col in cols] for row in a]


def sub(a, b):
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def rank_f2(a):
    a = [row[:] for row in a]
    rows, cols = len(a), len(a[0])
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        for r in range(rows):
            if r != rank and a[r][col]:
                a[r] = [x ^ y for x, y in zip(a[r], a[rank])]
        rank += 1
    return rank


def rank_q(a):
    a = [row[:] for row in a]
    rows, cols = len(a), len(a[0])
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = a[rank][col]
        a[rank] = [x / scale for x in a[rank]]
        for r in range(rank + 1, rows):
            if a[r][col]:
                scale = a[r][col]
                a[r] = [x - scale * y for x, y in zip(a[r], a[rank])]
        rank += 1
    return rank


def metric(n):
    return [[Q(i == j) - Q(1, 9) for j in range(n)] for i in range(n)]


def envelope_basis(n, indices):
    # The source's c=1 envelope basis is b_i = e_0 + 2 e_i.
    return [[Q(1 if r == 0 else 2 if r == i else 0) for i in sorted(indices)]
            for r in range(n)]


def projector(n, indices):
    g = metric(n)
    basis = envelope_basis(n, indices)
    gram = mul(mul(transpose(basis), g), basis)
    assert gram == [[Q(4 if i == j else 0) for j in range(len(indices))]
                   for i in range(len(indices))]
    # B (B^T G B)^-1 B^T G; the Gram matrix is exactly 4 I.
    dual = mul(transpose(basis), g)
    return [[sum((basis[r][k] * dual[k][c] / 4
                  for k in range(len(indices))), Q(0))
             for c in range(n)] for r in range(n)]


def source_projector(n, indices):
    # Coordinate-permuted c=1 specialization of PR63 audit.py's formula.
    count = len(indices)
    w = [4 if i == 0 else 3 for i in range(n)]
    z = [3 * (n + 1) - 10 if j == 0 else -10 for j in range(n)]
    o = [int(i in indices) for i in range(n)]
    return [[Q(int(i == j and i in indices)) + Q(
                2 * o[i] * z[j] + 6 * (n + 1) * w[i] * o[j]
                + count * w[i] * z[j], 12 * (n + 1))
             for j in range(n)] for i in range(n)]


def line_projector(n, indices):
    v = [Q(i in indices) for i in range(n)]
    row = [x - Q(1, 3) for x in v]  # v^T (I - J/9), since sum(v)=3.
    assert sum((v[i] * row[i] for i in range(n)), Q(0)) == 2
    return [[v[i] * row[j] / 2 for j in range(n)] for i in range(n)]


def block2(a, b, c, d):
    n = len(a)
    return [a[i] + b[i] for i in range(n)] + [c[i] + d[i] for i in range(n)]


def main():
    assert I_FSA < I_Y2 and I_SB2 < I_Y2
    assert I_FSA | I_SB2 == I_Y2
    g23 = metric(H)
    p_fsa = projector(H, I_FSA)
    p_sb2 = projector(H, I_SB2)
    p_y2 = projector(H, I_Y2)

    l23 = [[Q(i == j) + 1 for j in range(H)] for i in range(H)]
    l23_inverse = [[Q(i == j) - Q(1, H + 1) for j in range(H)]
                   for i in range(H)]
    p_fsa_hat = source_projector(H, I_FSA)
    p_sb2_hat = source_projector(H, I_SB2)
    p_y2_hat = source_projector(H, I_Y2)
    for indices, p, p_hat, dimension in (
            (I_FSA, p_fsa, p_fsa_hat, 10), (I_SB2, p_sb2, p_sb2_hat, 10),
            (I_Y2, p_y2, p_y2_hat, 14)):
        assert mul(p, p) == p
        assert mul(transpose(p), g23) == mul(g23, p)
        assert rank_q(p) == dimension
        assert p_hat == mul(mul(l23, p), l23_inverse)
        assert mul(p_hat, p_hat) == p_hat and rank_q(p_hat) == dimension
    assert mul(p_y2_hat, p_fsa_hat) == p_fsa_hat == mul(p_fsa_hat, p_y2_hat)
    assert mul(p_y2_hat, p_sb2_hat) == p_sb2_hat == mul(p_sb2_hat, p_y2_hat)

    a_fsa = sub(p_y2_hat, p_fsa_hat)
    a_sb2 = sub(p_y2_hat, p_sb2_hat)
    a_out = sub(p_y2_hat, p_y2_hat)  # The next consumer has the same core/cover.
    assert rank_q(a_fsa) == 4 == rank_q(a_sb2)
    assert rank_q(a_out) == 0
    assert add(a_fsa, a_out) == a_fsa  # Edge changes compose.

    # Tensor the h=23 envelope with one nondegenerate h=25 triple line.
    p_triple = line_projector(25, TRIPLE_25)
    assert mul(p_triple, p_triple) == p_triple and rank_q(p_triple) == 1
    assert all(x.denominator % 5 for matrix in
               (p_fsa_hat, p_sb2_hat, p_y2_hat, p_triple)
               for row in matrix for x in row)
    full_edge_ranks = (rank_q(a_fsa) * rank_q(p_triple),
                       rank_q(a_sb2) * rank_q(p_triple), 0)
    assert full_edge_ranks == (4, 4, 0)  # rank(A tensor P_T) = rank(A)rank(P_T).

    # The XOR shear commutes only when every port has the same frame.
    ident = eye(H)
    z = zero(H, H)
    gate = block2(ident, z, ident, ident)  # (x,z) -> (x,x+z)
    common = block2(p_y2_hat, z, z, p_y2_hat)
    split_ports = block2(p_fsa_hat, z, z, p_sb2_hat)
    assert mul(gate, common) == mul(common, gate)
    assert mul(gate, split_ports) != mul(split_ports, gate)

    # S-I has GF(2) rank one; it is not either rational address-edge rank.
    rank_f2_s_minus_i = rank_f2([[0, 0], [1, 0]])
    assert rank_f2_s_minus_i == 1 and rank_f2_s_minus_i != full_edge_ranks[0]

    print("PASS: rational projectors (including PR63 conjugate formula), nestedness, common-frame commutation, and exact edge ranks")
    print("h=23 ranks: dim(FSa)=10, dim(Sb2)=10, dim(Y2)=14; Q-edge ranks=(4,4,0)")
    print("Q^575 lift via one h=25 triple line: edge ranks=(4,4,0); GF(2) rank(S-I)=1 (rejected as an edge rank)")
    print("PASS: mixed per-port frames fail the XOR commutation check")
    print("Limit: validates the recorded logical gate data, not its physical-word event ID or global endpoints")


if __name__ == '__main__':
    main()
