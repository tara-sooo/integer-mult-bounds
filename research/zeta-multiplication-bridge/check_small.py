#!/usr/bin/env python3
"""Exact small audit for the Boolean zeta / multiplication interface question."""
from fractions import Fraction as Q
from itertools import combinations, product
import json


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def rank_q(matrix):
    a = [[Q(x) for x in row] for row in matrix]
    rank = 0
    for col in range(len(a[0])):
        pivot = next((r for r in range(rank, len(a)) if a[r][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        d = a[rank][col]
        a[rank] = [x / d for x in a[rank]]
        for r in range(len(a)):
            if r != rank and a[r][col]:
                d = a[r][col]
                a[r] = [x - d * y for x, y in zip(a[r], a[rank])]
        rank += 1
    return rank


def zeta_matrix(h):
    full = (1 << h) - 1
    masks = list(range(1, full))
    index = {u: i for i, u in enumerate(masks)}
    prev = {u: [int(i == index[u]) for i in range(len(masks))] for u in masks}
    for bit in range(h):
        cur = {}
        for w in masks:
            row = list(prev[w])
            lower = w ^ (1 << bit)
            if (w >> bit) & 1 and lower and lower in prev:
                row = [a + b for a, b in zip(row, prev[lower])]
            cur[w] = row
        prev = cur
    dag = [prev[full ^ t] for t in masks]
    direct = [[int((t & u) == 0) for u in masks] for t in masks]
    assert dag == direct
    return masks, direct


def source_motif(h):
    triples = [frozenset(s) for s in combinations(range(h), 3)]
    n = len(triples)
    center = [[Q(len(s & t) - 1, 2) for t in triples] for s in triples]
    side = [[(-center[i][j] if i != j and len(s & t) % 2 == 0 else Q(0))
             for j, t in enumerate(triples)] for i, s in enumerate(triples)]
    complex_map = [[side[i][j] + center[i][j] for j in range(n)] for i in range(n)]
    bit_map = [[(int(len(s & t) == 1) + len(s & t)) % 2 for t in triples]
               for s in triples]
    assert complex_map == [[Q(x) for x in row] for row in eye(n)]
    assert bit_map == eye(n)
    return dict(
        labels=[[i + 1 for i in sorted(s)] for s in triples],
        ports=n,
        complex_side=[[str(x) for x in row] for row in side],
        complex_center=[[str(x) for x in row] for row in center],
        complex_sum=[[str(x) for x in row] for row in complex_map],
        bit_sum=bit_map,
    )


def paired_cube_control():
    p = 4
    ports = []
    for labels in combinations(range(p), 3):
        for choices in product((0, 1), repeat=3):
            ports.append(frozenset(2 * i + b for i, b in zip(labels, choices)))
    labels = [tuple(sorted(i // 2 for i in port)) for port in ports]
    n = len(ports)
    b = [[Q(len(t & s) - 1, 2) for s in ports] for t in ports]
    block = [[b[i][j] if labels[i] == labels[j] else Q(0)
              for j in range(n)] for i in range(n)]
    k = [[Q(int(i == j)) - block[i][j] for j in range(n)] for i in range(n)]
    hmat = [[block[i][j] - b[i][j] for j in range(n)] for i in range(n)]
    assert all(k[i][j] + hmat[i][j] + b[i][j] == int(i == j)
               for i in range(n) for j in range(n))
    assert mm(k, k) == [[Q(x) for x in row] for row in eye(n)]
    for matrix in (k, hmat):
        for i, t in enumerate(ports):
            for j, s in enumerate(ports):
                if matrix[i][j]:
                    assert len(t & s) % 2 == 0

    target = frozenset((0, 2, 4))
    source = frozenset((0, 2, 6))
    ti, si = ports.index(target), ports.index(source)
    assert b[ti][si] == Q(1, 2)
    assert int(not target.intersection(source)) == 0
    return dict(
        h=2 * p, p=p, ports=n, block_count=n // 8,
        identity_decomposition=True, K_squared_is_identity=True,
        side_supports_are_binary_orthogonal=True,
        synthetic_disjointness_control=dict(
            target=[x + 1 for x in sorted(target)],
            source=[x + 1 for x in sorted(source)],
            intersection=2, B_coefficient=str(b[ti][si]),
            disjointness_indicator=0,
            scope="synthetic restriction on source port labels; not a zeta embedding"),
        coordinate_star_loss=2 * p * (2 * p - 2),
    )


def source_histograms():
    rows = []
    for h in range(3, 9):
        v = (1 << h) - 2
        supplied = {2: v}
        if h >= 4:
            supplied[1] = v * (h - 3)
        # Mirrors Counter({2: v, h-4: v, 1: v}); duplicate keys collapse.
        default = {2: v, h - 4: v, 1: v}
        rows.append(dict(
            h=h, v=v,
            supplied={str(r): n for r, n in sorted(supplied.items())},
            supplied_mass=sum(r * n for r, n in supplied.items()),
            required_mass=v * (h - 1),
            default={str(r): n for r, n in sorted(default.items())},
            default_mass=sum(r * n for r, n in default.items()),
            supplied_overrides_default=supplied != default,
        ))
    return rows


def h0_pair(a, b):
    return (Q(len(a & b)) - Q(len(a) * len(b), 9)) / 2


def dirty_word(y, z, x, m, j=1, v=1, *, pre_read=True, inverse=True):
    if pre_read:
        y -= j * m * z
    z += v * x
    z *= m
    y += j * z
    if inverse:
        z /= m
    z -= v * x
    return y, z


def main():
    zeta = []
    for h in (3, 4):
        masks, d = zeta_matrix(h)
        d2 = mm(d, d)
        zeta.append(dict(
            h=h, labels=masks, D=d, rank_over_Q=rank_q(d),
            symmetric=d == [list(row) for row in zip(*d)],
            zero_diagonal=all(d[i][i] == 0 for i in range(len(d))),
            row_sums=[sum(row) for row in d],
            D2_diagonal=[d2[i][i] for i in range(len(d))],
            D2_first_column=[row[0] for row in d2],
        ))

    small_sources = {str(h): source_motif(h) for h in (3, 4)}
    assert [len(zeta_matrix(h)[0]) for h in (3, 4)] == [6, 14]
    assert [small_sources[str(h)]['ports'] for h in (3, 4)] == [1, 4]

    y, z = dirty_word(Q(7), Q(5), Q(3), Q(2))
    assert (y, z) == (Q(13), Q(5))
    dropped_pre = dirty_word(Q(7), Q(5), Q(3), Q(2), pre_read=False)
    dropped_inverse = dirty_word(Q(7), Q(5), Q(3), Q(2), inverse=False)
    assert dropped_pre == (Q(23), Q(5))
    assert dropped_inverse == (Q(13), Q(13))

    t, u = frozenset((0, 2, 4)), frozenset((1, 3, 6))
    one_common = frozenset((0, 2, 4)), frozenset((0, 3, 6))
    singleton_masks = frozenset((0,)), frozenset((1,))
    assert h0_pair(t, u) == Q(-1, 2)
    assert h0_pair(*one_common) == 0
    assert h0_pair(*singleton_masks) == Q(-1, 18)

    receipt = dict(
        status="REDUCTION_BRIDGE_NOT_SPECIFIED",
        scope="Exact operator diagnostics and source-defined controls; no mask-to-port encoding is asserted.",
        zeta_matrices=zeta,
        original_section3_small_port_maps=small_sources,
        paired_cube_source_control=paired_cube_control(),
        h0_exact_values=dict(
            disjoint_triples=str(h0_pair(t, u)),
            one_point_intersection_triples=str(h0_pair(*one_common)),
            disjoint_singleton_coordinate_masks=str(h0_pair(*singleton_masks)),
            formula="(intersection_size - |left|*|right|/9)/2"),
        dirty_word_control=dict(
            inputs=dict(y=7, z=5, x=3, M=2, J=1, V=1),
            correct=dict(y=str(y), z=str(z)),
            expected=dict(y="y + J*M*V*x", z="original z"),
            skipped_pre_read=dict(y=str(dropped_pre[0]), z=str(dropped_pre[1])),
            skipped_inverse=dict(y=str(dropped_inverse[0]), z=str(dropped_inverse[1]))),
        source_histogram_audit=source_histograms(),
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
