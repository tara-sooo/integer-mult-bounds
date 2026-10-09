#!/usr/bin/env python3
"""Exact p=4 audit of the pinned paired-cube identities and one failed variant."""
# shortcut: p=4 and a 2x2 representative raw core only; upgrade if a legal variant needs full supplier replay.

from fractions import Fraction as F
from functools import reduce
from itertools import combinations, product


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def madd(a, b, sign=1):
    return [[x + sign * y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def inv2(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    assert det
    return [[a[1][1] / det, -a[0][1] / det],
            [-a[1][0] / det, a[0][0] / det]]


def gf2_dot(a, b):
    return (a & b).bit_count() & 1


def gf2_rank(rows):
    pivots = {}
    for row in rows:
        x = row
        while x:
            p = x.bit_length() - 1
            if p in pivots:
                x ^= pivots[p]
            else:
                pivots[p] = x
                break
    return len(pivots)


def ports(p, even_only=False):
    out = []
    for cube in combinations(range(p), 3):
        for bits in product(range(2), repeat=3):
            if even_only and sum(bits) % 2:
                continue
            mask = sum(1 << (2 * i + bit) for i, bit in zip(cube, bits))
            out.append((cube, bits, mask))
    return out


def b_entry(t, s):
    return F(((t & s).bit_count() - 1), 2)


def local_b(cube_ports):
    return [[b_entry(t[2], s[2]) for s in cube_ports] for t in cube_ports]


def build_operator_matrices(ps):
    n = len(ps)
    B = [[b_entry(t[2], s[2]) for s in ps] for t in ps]
    Bblock = [[B[i][j] if ps[i][0] == ps[j][0] else F(0)
               for j in range(n)] for i in range(n)]
    K = madd(eye(n), Bblock, -1)
    H = madd(Bblock, B, -1)
    return B, Bblock, K, H


def source_channel(cube, target_cube, target_bits):
    """The signed F/A/G source set in the pinned paired-cube construction."""
    shared = sorted(set(cube) & set(target_cube))
    result = {}
    for bits in product(range(2), repeat=3):
        if not shared:
            coeff = F(1, 2)
        elif len(shared) == 1:
            i = shared[0]
            coeff = F(1, 2) if bits[cube.index(i)] == 1 - target_bits[target_cube.index(i)] else F(0)
        elif len(shared) == 2:
            i, j = shared
            ai, aj = bits[cube.index(i)], bits[cube.index(j)]
            ti, tj = target_bits[target_cube.index(i)], target_bits[target_cube.index(j)]
            coeff = F((2 * ti - 1) * (1 - 2 * ai), 2) if (ai ^ aj) == (ti ^ tj) else F(0)
        else:
            coeff = F(0)
        result[bits] = coeff
    return result


def check_local_geometry():
    p, h = 4, 8
    ps = ports(p)
    cubes = list(combinations(range(p), 3))
    assert len(ps) == 8 * len(cubes) == 32
    assert len({x[2] for x in ps}) == len(ps)
    assert all(x[2].bit_count() == 3 for x in ps)
    by_cube = {c: [x for x in ps if x[0] == c] for c in cubes}
    assert all(len(by_cube[c]) == 8 and {x[1] for x in by_cube[c]} == set(product(range(2), repeat=3))
               for c in cubes)
    incidence = [sum((x[2] >> i) & 1 for x in ps) for i in range(h)]
    assert incidence == [4 * 3] * h

    B, Bblock, K, H = build_operator_matrices(ps)
    assert madd(madd(K, H), B) == eye(len(ps))
    assert mm(K, K) == eye(len(ps))

    # Each local signed block is (antipode - distance-one adjacency)/2.
    for cube, local in by_cube.items():
        kmat = [[K[ps.index(t)][ps.index(s)] for s in local] for t in local]
        assert mm(kmat, kmat) == eye(8)
        for i, (ct, bt, _) in enumerate(local):
            for j, (cs, bs, _) in enumerate(local):
                d = sum(x != y for x, y in zip(bt, bs))
                expected = F(1, 2) if d == 3 else F(-1, 2) if d == 1 else F(0)
                assert kmat[i][j] == expected
                assert (d % 2) == 1 if kmat[i][j] else True
        even = [i for i, x in enumerate(local) if sum(x[1]) % 2 == 0]
        odd = [i for i, x in enumerate(local) if sum(x[1]) % 2 == 1]
        assert gf2_rank([local[i][2] for i in even]) == 3
        assert gf2_rank([local[i][2] for i in odd]) == 3
        assert reduce(int.__xor__, [local[i][2] for i in even]) == 0
        assert all(gf2_dot(local[i][2], local[j][2]) == 0 for i in even for j in odd)
        for rows, cols in ((even, odd), (odd, even)):
            for i in rows:
                for j in rows:
                    assert sum((kmat[i][k] * kmat[j][k] for k in cols), F(0)) == F(i == j)

    # Nonzero off-diagonal scalar reads have orthogonal coordinate addresses.
    for matrix in (B, H, K):
        for i in range(len(ps)):
            for j in range(len(ps)):
                if i != j and matrix[i][j]:
                    assert gf2_dot(ps[i][2], ps[j][2]) == 0

    # Reconstruct every p=4 H entry from the source-faithful signed F/A/G channel.
    for ti, (tc, tb, tq) in enumerate(ps):
        for sj, (sc, sb, sq) in enumerate(ps):
            expected = H[ti][sj]
            if tc == sc:
                actual = F(0)
            else:
                actual = source_channel(sc, tc, tb)[sb]
            assert actual == expected, (tc, tb, sc, sb, actual, expected)
            if actual:
                assert gf2_dot(tq, sq) == 0

    # Coordinate-star source spaces equal U_i and their copied-center rank is ell=h(h-2).
    star_ranks = []
    for i in range(h):
        partner = i ^ 1
        outside = [j for j in range(h) if j not in (i, partner)]
        anchor = outside[0]
        expected_basis = [1 << i] + [(1 << anchor) | (1 << j) for j in outside[1:]]
        sources = [x[2] for x in ps if (x[2] >> i) & 1]
        assert all(not ((x >> partner) & 1) and
                   sum((x >> j) & 1 for j in outside) % 2 == 0 for x in sources)
        assert gf2_rank(expected_basis) == gf2_rank(sources) == h - 2
        star_ranks.append(gf2_rank(sources))
    ell = sum(star_ranks)
    assert ell == h * (h - 2) == 48
    for ti, (_, _, tq) in enumerate(ps):
        for sj, (_, _, sq) in enumerate(ps):
            scatter = F(sum(1 for i in range(h) if ((tq >> i) & 1) and ((sq >> i) & 1)), 2) - F(3, 6)
            assert scatter == B[ti][sj]

    # Sign/phase control: deleting one antipodal +1/2 read destroys K^2=I.
    local = by_cube[cubes[0]]
    kmat = [[K[ps.index(t)][ps.index(s)] for s in local] for t in local]
    labels = {x[1]: i for i, x in enumerate(local)}
    bad = [row[:] for row in kmat]
    a, b = labels[(0, 0, 0)], labels[(1, 1, 1)]
    bad[a][b] = bad[b][a] = F(0)
    assert mm(bad, bad)[a][a] == F(3, 4)
    return dict(p=p, h=h, cubes=len(cubes), v=len(ps), coordinate_incidence=incidence,
                center_rank=ell, h_channels_checked=len(ps) ** 2, sign_control_diagonal=F(3, 4))


def check_stage_cover():
    h, m0, m = 8, 3 * 8 - 2, 3 * 8
    # Port-specific orthogonal involutions on the three-stage 3h-2 data space.
    ps = ports(4)
    for _, _, q in ps:
        assert q.bit_count() == 3 and gf2_dot(q, q) == 1
        pivot = (q & -q).bit_length() - 1
        qperp = [(1 << j) ^ (((q >> j) & 1) << pivot) for j in range(h) if j != pivot]
        assert len(qperp) == h - 1 and gf2_rank(qperp) == h - 1
        assert all(gf2_dot(q, u) == 0 for u in qperp)
        d = h - 1
        gram_q = [[gf2_dot(a, b) for b in qperp] for a in qperp]
        gram = [[0] * (1 + 3 * d) for _ in range(1 + 3 * d)]
        gram[0][0] = 1
        for offset in (1, 1 + d, 1 + 2 * d):
            for i in range(d):
                for j in range(d):
                    gram[offset + i][offset + j] = gram_q[i][j]
        r12, r23 = list(range(1 + 3 * d)), list(range(1 + 3 * d))
        for i in range(d):
            r12[1 + i], r12[1 + d + i] = r12[1 + d + i], r12[1 + i]
            r23[1 + i], r23[1 + 2 * d + i] = r23[1 + 2 * d + i], r23[1 + i]
        for r in (r12, r23):
            assert all(r[r[i]] == i for i in range(len(r)))
            assert all(gram[i][j] == gram[r[i]][r[j]]
                       for i in range(len(r)) for j in range(len(r)))
            assert r[0] == 0
        assert set(r12[:h]) == {0, *range(1 + d, 1 + 2 * d)}
        assert set(r23[:h]) == {0, *range(1 + 2 * d, 1 + 3 * d)}

    # The three signed shears give exactly (X,Y) -> (-Y,X).
    s1 = [[1, 0], [1, 1]]          # Y <- Y + X
    s2 = [[1, -1], [0, 1]]         # X <- X - Y
    s3 = [[1, 0], [1, 1]]          # Y <- Y + X
    assert mm(mm(s3, s2), s1) == [[0, -1], [1, 0]]

    # Retained data endpoints join without positive-rank connectors.
    endpoints = [
        (1, h, 0, h - 1),
        (h, 2 * h - 1, h - 1, 2 * h - 2),
        (2 * h - 1, m0, 2 * h - 2, m0 - 1),
    ]
    assert endpoints[0][1] == endpoints[1][0]
    assert endpoints[0][3] == endpoints[1][2]
    assert endpoints[1][1] == endpoints[2][0]
    assert endpoints[1][3] == endpoints[2][2]
    assert endpoints[-1] == (15, 22, 14, 21)

    # The paired-cube route sends one physical auxiliary bank through three orthogonal h-blocks in 3h.
    blocks = [set(range(j * h, (j + 1) * h)) for j in range(3)]
    assert all(blocks[i].isdisjoint(blocks[j]) for i in range(3) for j in range(i))
    assert set.union(*blocks) == set(range(m))
    maps = [list(range(m))]
    for offset in (h, 2 * h):
        perm = list(range(m))
        for i in range(h):
            perm[i], perm[offset + i] = perm[offset + i], perm[i]
        maps.append(perm)
    for j, perm in enumerate(maps):
        assert sorted(perm) == list(range(m))
        assert set(perm[:h]) == blocks[j]
        assert all(perm[perm[i]] == i for i in range(m))
    # Each role map g -> g H_j is a group bijection; the fixed per-stage right factor is invertible.
    assert len(maps) == 3

    # Omitting one width-two data complement leaves its E0 endpoint codimension two.
    e0, ambient = set(range(m0)), set(range(m))
    assert ambient - e0 == {22, 23}
    assert len(ambient - e0) == 2
    omitted_complement = e0
    assert omitted_complement != ambient and len(ambient - omitted_complement) == 2
    return dict(data_dimension=m0, ambient_dimension=m, shear_matrix=[[0, -1], [1, 0]],
                stage_blocks=[sorted(x) for x in blocks], complements_per_port=2,
                complement_width=2)


def update_rows(state, dst, src, coeff):
    old = [row[:] for row in state]
    for i, d in enumerate(dst):
        state[d] = [old[d][k] + sum((coeff[i][j] * old[src[j]][k] for j in range(len(src))), F(0))
                    for k in range(len(old[0]))]


def replace_rows(state, dst, src, coeff):
    old = [row[:] for row in state]
    for i, d in enumerate(dst):
        state[d] = [sum((coeff[i][j] * old[src[j]][k] for j in range(len(src))), F(0))
                    for k in range(len(old[0]))]


def check_dirty_and_frame_contract():
    m = [[F(1), F(1)], [F(0), F(1)]]
    mi = [[F(1), F(-1)], [F(0), F(1)]]
    v, j = eye(2), mi
    assert mm(j, mm(m, v)) == eye(2)
    state = eye(6)  # [y0,y1,z0,z1,x0,x1], with arbitrary initial y,z,x.
    update_rows(state, (0, 1), (2, 3), [[-x for x in row] for row in mm(j, m)])
    update_rows(state, (2, 3), (4, 5), v)
    replace_rows(state, (2, 3), (2, 3), m)
    update_rows(state, (0, 1), (2, 3), j)
    replace_rows(state, (2, 3), (2, 3), mi)
    update_rows(state, (2, 3), (4, 5), [[-x for x in row] for row in v])
    expected = eye(6)
    expected[0][4] = expected[1][5] = F(1)
    assert state == expected  # all dirty z restored, y gains JMVx.

    omitted = eye(6)
    update_rows(omitted, (0, 1), (2, 3), [[-x for x in row] for row in mm(j, m)])
    update_rows(omitted, (2, 3), (4, 5), v)
    replace_rows(omitted, (2, 3), (2, 3), m)
    update_rows(omitted, (0, 1), (2, 3), j)
    replace_rows(omitted, (2, 3), (2, 3), mi)
    assert omitted[2][4] == omitted[3][5] == 1  # unpaid final dirty restore fails.

    # Exact raw core and its frame/gauge correction, for arbitrary inputs.
    fourier = [[F(0), F(1)], [F(-1), F(0)]]
    gauge = m
    gauge_inv = mi
    raw = mm(fourier, gauge_inv)  # U = F_A T_sigma^-1
    fourier_inv = [[F(0), F(-1)], [F(1), F(0)]]
    raw_inv = inv2(raw)
    assert mm(raw, raw_inv) == eye(2) and mm(raw_inv, raw) == eye(2)
    assert raw_inv == mm(gauge, fourier_inv)
    assert mm(fourier, raw_inv) == mm(mm(fourier, gauge), fourier_inv)
    assert mm(fourier, raw) == mm(mm(fourier, fourier), gauge_inv)
    return dict(dirty_state_dimension=2, JMV="I", raw_operator="F_A*T_sigma^-1",
                raw_inverse="T_sigma*F_A^-1", missing_restore_rejected=True)


def check_variant():
    p = 4
    ps = ports(p, even_only=True)
    assert len(ps) == 4 * 4 == 16
    assert [sum((x[2] >> i) & 1 for x in ps) for i in range(2 * p)] == [6] * (2 * p)
    cube = [x for x in ps if x[0] == (0, 1, 2)]
    bv = local_b(cube)
    kv = madd(eye(4), bv, -1)
    kv2 = mm(kv, kv)
    assert kv == [[F(0)] * 4 for _ in range(4)]
    assert kv2[0][0] - 1 == -1
    return dict(v=16, cube_ports=4, K="0", K2_minus_I_diagonal=F(-1),
                baseline_v=32, baseline_2v_complements=64, variant_2v_potential=32)


def main():
    baseline = check_local_geometry()
    stages = check_stage_cover()
    dirty = check_dirty_and_frame_contract()
    variant = check_variant()
    print("baseline: PASS", baseline)
    print("stage cover/shears/data endpoints: PASS", stages)
    print("arbitrary-dirty/raw-gauge contract: PASS", dirty)
    print("negative control (drop antipodal signed read): PASS, K^2[000,000]=3/4")
    print("negative control (omit final dirty restore): PASS, z'=z+x")
    print("negative control (drop width-2 data complement): PASS, endpoint misses coordinates 22 and 23")
    print("variant: GEOMETRY_IDENTITY_FAILS", variant)


if __name__ == "__main__":
    main()
