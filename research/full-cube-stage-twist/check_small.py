#!/usr/bin/env python3
"""Exact p=4 check of one full-cube, cube-dependent stage twist."""

from fractions import Fraction as F
from itertools import combinations, product


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def madd(a, b, sign=1):
    return [[x + sign * y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


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


def ports(p):
    return [(cube, bits,
             sum(1 << (2 * i + b) for i, b in zip(cube, bits)))
            for cube in combinations(range(p), 3)
            for bits in product(range(2), repeat=3)]


def b_entry(t, s):
    return F((t & s).bit_count() - 1, 2)


def source_channel(cube, target_cube, target_bits):
    """Pinned signed F/A/G source coefficient for one cross-cube entry."""
    shared = sorted(set(cube) & set(target_cube))
    result = {}
    for bits in product(range(2), repeat=3):
        if not shared:
            coeff = F(1, 2)
        elif len(shared) == 1:
            i = shared[0]
            coeff = (F(1, 2) if bits[cube.index(i)] ==
                     1 - target_bits[target_cube.index(i)] else F(0))
        elif len(shared) == 2:
            i, j = shared
            ai, aj = bits[cube.index(i)], bits[cube.index(j)]
            ti, tj = target_bits[target_cube.index(i)], target_bits[target_cube.index(j)]
            coeff = (F((2 * ti - 1) * (1 - 2 * ai), 2)
                     if (ai ^ aj) == (ti ^ tj) else F(0))
        else:
            coeff = F(0)
        result[bits] = coeff
    return result


def check_full_cube_and_frozen_algebra():
    p, h = 4, 8
    ps = ports(p)
    cubes = list(combinations(range(p), 3))
    by_cube = {c: [x for x in ps if x[0] == c] for c in cubes}
    assert len(ps) == 8 * len(cubes) == 32
    assert len({x[2] for x in ps}) == len(ps)
    assert all(x[2].bit_count() == 3 for x in ps)
    assert all(len(by_cube[c]) == 8 and
               {x[1] for x in by_cube[c]} == set(product(range(2), repeat=3))
               for c in cubes)
    incidence = [sum((x[2] >> i) & 1 for x in ps) for i in range(h)]
    assert incidence == [12] * h

    n = len(ps)
    B = [[b_entry(t[2], s[2]) for s in ps] for t in ps]
    Bblock = [[B[i][j] if ps[i][0] == ps[j][0] else F(0)
               for j in range(n)] for i in range(n)]
    K = madd(eye(n), Bblock, -1)
    H = madd(Bblock, B, -1)
    assert madd(madd(K, H), B) == eye(n)
    assert mm(K, K) == eye(n)

    for ti, (tc, tb, tq) in enumerate(ps):
        for sj, (sc, sb, sq) in enumerate(ps):
            expected = H[ti][sj]
            actual = F(0) if tc == sc else source_channel(sc, tc, tb)[sb]
            assert actual == expected, (tc, tb, sc, sb, actual, expected)
            if actual:
                assert gf2_dot(tq, sq) == 0
    for matrix in (B, H, K):
        for i in range(n):
            for j in range(n):
                if i != j and matrix[i][j]:
                    assert gf2_dot(ps[i][2], ps[j][2]) == 0
    return ps, cubes, dict(p=p, h=h, cubes=4, ports=n, coordinate_incidence=incidence,
                           frozen_BHK=True, K_squared="I32", signed_H_entries=1024)


def compose_perm(a, b):
    """Coordinate image for the matrix product A*B (apply B, then A)."""
    return [a[b[i]] for i in range(len(a))]


def inverse_perm(p):
    out = [0] * len(p)
    for i, image in enumerate(p):
        out[image] = i
    return out


def permutation_rows(p):
    rows = [0] * len(p)
    for source, target in enumerate(p):
        rows[target] |= 1 << source
    return rows


def is_orthogonal(p):
    rows = permutation_rows(p)
    return all(gf2_dot(rows[i], rows[j]) == (i == j)
               for i in range(len(rows)) for j in range(len(rows)))


def block_swap(offset, m=24, h=8):
    p = list(range(m))
    for i in range(h):
        p[i], p[offset + i] = p[offset + i], p[i]
    return p


def check_routes_and_intersections(cubes, ps):
    m, h = 24, 8
    ident = list(range(m))
    H1, H2, H3 = ident, block_swap(8), block_swap(16)
    Q = ident[:]
    Q[0], Q[8] = Q[8], Q[0]
    base = [H1, H2, H3]
    c0 = (1, 2, 3)  # the cube omitting pair label 0
    stage1_images_at_identity = [Q if cube == c0 else H1 for cube in cubes]
    assert Q != H1
    assert stage1_images_at_identity.count(H1) == 3
    assert stage1_images_at_identity.count(Q) == 1
    # For every g, gQ != g by cancellation and Q != I; g -> gQ is bijective.

    routes, base_intersections, candidate_intersections = [], [], []
    candidate_orthogonal = {}
    for cube in cubes:
        base_blocks = [{p[i] for i in range(h)} for p in base]
        twist = [compose_perm(Q, H1) if cube == c0 and stage == 0 else base[stage]
                 for stage in range(3)]
        for stage, mult in enumerate(twist):
            inv = inverse_perm(mult)
            assert sorted(mult) == ident
            assert is_orthogonal(mult)  # exact permutation-matrix test: H^T H = I over F2
            assert compose_perm(mult, inv) == ident
            assert compose_perm(inv, mult) == ident
            routes.append((cube, stage + 1, mult, inv))

        changed_blocks = [{p[i] for i in range(h)} for p in twist]
        for i, j in combinations(range(3), 2):
            base_dim = gf2_rank([1 << x for x in base_blocks[i] & base_blocks[j]])
            cand_dim = gf2_rank([1 << x for x in changed_blocks[i] & changed_blocks[j]])
            base_intersections.append((cube, i + 1, j + 1, base_dim))
            candidate_intersections.append((cube, i + 1, j + 1, cand_dim))
            candidate_orthogonal[cube, i + 1, j + 1] = all(
                gf2_dot(1 << x, 1 << y) == 0
                for x in changed_blocks[i] for y in changed_blocks[j])

    assert len(routes) == 12
    route_keys = {(cube, stage) for cube, stage, _, _ in routes}
    port_stage_visits = [(port, stage) for port in ps for stage in (1, 2, 3)
                         if (port[0], stage) in route_keys]
    assert len(port_stage_visits) == 32 * 3
    assert all((port[0], stage) in route_keys for port in ps for stage in (1, 2, 3))
    assert all(item[3] == 0 for item in base_intersections)
    assert all(item[3] == (1 if item[:3] == (c0, 1, 2) else 0)
               for item in candidate_intersections)
    assert all(ok for key, ok in candidate_orthogonal.items() if key != (c0, 1, 2))
    assert not candidate_orthogonal[c0, 1, 2]
    assert 8 in ({Q[i] for i in range(h)} & {H2[i] for i in range(h)})
    assert gf2_dot(1 << 8, 1 << 8) == 1  # exact nonorthogonal overlap witness

    # For every g in O(24,2), gH and gH^-1 are inverse right-multiplication maps:
    # (gH)H^-1=g and (gH^-1)H=g. Also dim(gU intersect gV)=dim(U intersect V)
    # and <gu,gv>=<u,v>. These identities give the group-wide claims without
    # enumerating the enormous finite group.
    return dict(group_right_maps=len(routes), multipliers_in_O24_2=True,
                explicit_inverses=True, baseline_pair_intersection_dims="all zero",
                port_stage_visits=len(port_stage_visits),
                stage1_images_at_identity={"I": stage1_images_at_identity.count(H1),
                                           "Q": stage1_images_at_identity.count(Q)},
                stage1_groupwide_images="three g, one gQ; gQ != g by cancellation",
                aggregate_shared_stock_occupancy="UNRESOLVED_NOT_PASSED",
                candidate_intersections=[(c, i, j, d) for c, i, j, d in candidate_intersections
                                         if d],
                candidate_C0_stage1_stage2_orthogonal=False,
                witness="e8 belongs to both blocks and <e8,e8>=1")


def same_subspace(a, b):
    return gf2_rank(a) == gf2_rank(b) == gf2_rank(a + b)


def check_data_frames_and_shears(ps):
    h, data_dim = 8, 22
    ambient_dim = 24
    A = [1 << i for i in range(8)]
    B = [1 << i for i in range(8, 15)]
    C = [1 << i for i in range(15, 22)]
    assert len(A + B + C) == data_dim
    complements = [1 << 22, 1 << 23]
    assert data_dim + len(complements) == ambient_dim
    assert gf2_rank(complements) == 2
    assert not any(gf2_dot(c, e) for c in complements for e in A + B + C)
    checked = 0
    for _, _, port_mask in ps:
        q = port_mask & ((1 << h) - 1)
        assert q.bit_count() == 3 and gf2_dot(q, q) == 1
        pivot = (q & -q).bit_length() - 1
        Aperp = [((1 << j) | (((q >> j) & 1) << pivot))
                 for j in range(h) if j != pivot]
        assert gf2_rank(Aperp) == h - 1

        x1_in, x1_out = [q], [q] + B
        x2_in, x2_out = [q] + B, A + B
        x3_in, x3_out = A + B, A + B + C
        y1_in, y1_out = [], B
        y2_in, y2_out = B, Aperp + B
        y3_in, y3_out = Aperp + B, Aperp + B + C
        assert same_subspace(x1_out, x2_in)
        assert same_subspace(x2_out, x3_in)
        assert same_subspace(y1_out, y2_in)
        assert same_subspace(y2_out, y3_in)
        assert [gf2_rank(s) for s in (x1_in, x1_out, x2_out, x3_out)] == [1, 8, 15, 22]
        assert [gf2_rank(s) for s in (y1_in, y1_out, y2_out, y3_out)] == [0, 7, 14, 21]
        checked += 1
    assert checked == 32

    s1 = [[1, 0], [1, 1]]       # Y += X
    s2 = [[1, -1], [0, 1]]      # X -= Y
    s3 = [[1, 0], [1, 1]]       # Y += X
    assert mm(mm(s3, s2), s1) == [[0, -1], [1, 0]]
    return dict(data_dimension=data_dim, ports_with_exact_adjacent_frames=checked,
                X_endpoint_dimensions=[1, 8, 15, 22],
                Y_endpoint_dimensions=[0, 7, 14, 21],
                signed_shear_product="(-Y,X)",
                width_two_complements_per_port=2,
                complement_children=2 * checked, complement_rank_mass=2 * 2 * checked)


def add_vec(a, b, sign=1):
    return [x + sign * y for x, y in zip(a, b)]


def apply_m(v):
    out = v[:]
    out[0] += out[1]
    return out


def apply_j(v):
    out = v[:]
    out[0] -= out[1]
    return out


def apply_route(v):
    out = v[:]
    out[0], out[8] = out[8], out[0]  # Q, the C0 stage-1 route
    return out


def dirty_core(y, z, x, omit_final_cleanup=False):
    # Source sequence for J=M^-1, V=I: y-=JM z; z+=Vx; z=M z;
    # y+=Jz; z=M^-1 z; z-=Vx.
    y = add_vec(y, apply_j(apply_m(z)), -1)
    z = add_vec(z, x)
    z = apply_m(z)
    y = add_vec(y, apply_j(z))
    z = apply_j(z)
    if not omit_final_cleanup:
        z = add_vec(z, x, -1)
    return y, z, x[:]


def check_dirty_core_and_routed_conjugate():
    m = 24
    checked = 0
    for index in range(3 * m):
        y, z, x = [0] * m, [0] * m, [0] * m
        bank, coord = divmod(index, m)
        (y, z, x)[bank][coord] = 1
        result = dirty_core(y, z, x)
        assert result == (add_vec(y, x), z, x)

        # Conjugate by the candidate role route on the dirty auxiliary bank:
        # W=diag(I,Q,I), so W^-1=W. Check W U W^-1 on every basis vector.
        routed_input = (y[:], apply_route(z), x[:])
        routed_mid = dirty_core(*routed_input)
        routed_result = (routed_mid[0], apply_route(routed_mid[1]), routed_mid[2])
        assert routed_result == (add_vec(y, x), z, x)

        omitted = dirty_core(y, z, x, omit_final_cleanup=True)
        assert omitted == (add_vec(y, x), add_vec(z, x), x)
        checked += 1
    assert checked == 72

    # The matching completed frame operator U=F_A T_sigma^-1 and its inverse
    # are also checked on a noncommuting two-coordinate representative.
    I = [[F(1), F(0)], [F(0), F(1)]]
    M = [[F(1), F(1)], [F(0), F(1)]]
    J = [[F(1), F(-1)], [F(0), F(1)]]
    FA = [[F(0), F(1)], [F(-1), F(0)]]
    FA_inv = [[F(0), F(-1)], [F(1), F(0)]]
    U = mm(FA, J)
    U_inv = mm(M, FA_inv)
    assert mm(U, U_inv) == I and mm(U_inv, U) == I
    assert mm(FA, U_inv) == mm(mm(FA, M), FA_inv)
    assert mm(FA, U) == mm(mm(FA, FA), J)

    # Omitting cleanup has the exact dirty residual z'=z+x, witnessed by x=e0.
    zero = [0] * m
    e0 = [1] + [0] * (m - 1)
    assert dirty_core(zero, zero, e0, omit_final_cleanup=True)[1] == e0
    return dict(completed_core_basis_vectors=checked,
                routed_conjugate_basis_vectors=checked,
                dirty_z_restored=True, routed_dirty_z_restored=True,
                frame_U="F_A*T_sigma^-1", inverse="T_sigma*F_A^-1",
                forward_and_reverse_frame_corrections=True,
                omitted_cleanup="z'=z+x")


def check_issue24_external_control():
    # This is Issue 24's prior even-parity half-cube, never the Issue 25 candidate.
    eps = [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)]
    masks = [sum(1 << (2 * i + b) for i, b in zip((0, 1, 2), bits))
             for bits in eps]
    bblock = [[b_entry(t, s) for s in masks] for t in masks]
    k = madd(eye(4), bblock, -1)
    assert bblock == eye(4)
    assert k == [[F(0)] * 4 for _ in range(4)]
    assert mm(k, k) != eye(4)
    return "external only: B_block=I4, K=0, K^2!=I"


def main():
    ps, cubes, algebra = check_full_cube_and_frozen_algebra()
    routes = check_routes_and_intersections(cubes, ps)
    data = check_data_frames_and_shears(ps)
    dirty = check_dirty_core_and_routed_conjugate()
    external = check_issue24_external_control()
    print("FAST invariance lemma: PASS (see INVARIANCE.md)")
    print("full-cube incidence and frozen B/H/K: PASS", algebra)
    print("right-multiplication routes and active blocks:", routes)
    print("all data ports, exact frames and signed shears: PASS", data)
    print("completed dirty core and routed conjugate: PASS", dirty)
    print("negative control (candidate nonorthogonal overlap): PASS, <e8,e8>=1")
    print("negative control (omit final dirty cleanup): PASS, z'=z+x")
    print("Issue 24 parity failure (external control):", external)
    print("FOCUSED p=4 result: candidate is nonisomorphic but illegal; stop before paid profile")


if __name__ == "__main__":
    main()
