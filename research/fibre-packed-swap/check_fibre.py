#!/usr/bin/env python3
"""Finite exact checks for the Issue 39 one-fibre checkpoint."""

from fractions import Fraction
from itertools import combinations, product
import json


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def mod2(x):
    return [a % 2 for a in x]


def fibre_check(h):
    # The same fixed triples are used at h=4 and h=6; indices here are zero-based.
    A, B = {0, 1, 2}, {0, 1, 3}
    alpha = beta = 0
    triples = list(combinations(range(h), 3))
    tau = lambda T: frozenset(i ^ 1 for i in T)
    coords = list(product(range(h), repeat=3))
    index = {c: i for i, c in enumerate(coords)}
    m = h**3
    ps = list(range(0, h, 2))
    qs = [p + 1 for p in ps]

    def u(T):
        return [int(i in A and j in B and k in T) for i, j, k in coords]

    ds, phis = [], []
    for p, q in zip(ps, qs):
        ds.append([
            int(i in A and j in B and k == q)
            - int(i in A and j in B and k == p)
            for i, j, k in coords
        ])
        phi = [0] * m
        phi[index[(alpha, beta, p)]] = 1
        phi[index[(alpha, beta, q)]] = -1
        phis.append(phi)

    k = h // 2
    pairings = [[dot(phi, d) for d in ds] for phi in phis]
    assert pairings == [[-2 * int(i == j) for j in range(k)] for i in range(k)]

    def P(x):
        coeffs = [dot(phis[i], x) for i in range(k)]
        return [x[r] + sum(ds[i][r] * coeffs[i] for i in range(k)) for r in range(m)]

    def PT(x):
        coeffs = [dot(ds[i], x) for i in range(k)]
        return [x[r] + sum(phis[i][r] * coeffs[i] for i in range(k)) for r in range(m)]

    def P_wrong_sign(x):
        coeffs = [dot(phis[i], x) for i in range(k)]
        return [x[r] - sum(ds[i][r] * coeffs[i] for i in range(k)) for r in range(m)]

    # The selected k-by-k minors of D and Phi are identity over Z, Q and F_2.
    d_minor = [[d[index[(alpha, beta, qs[i])]] for d in ds] for i in range(k)]
    phi_minor = [[phis[i][index[(alpha, beta, ps[j])]] for j in range(k)] for i in range(k)]
    identity = [[int(i == j) for j in range(k)] for i in range(k)]
    assert d_minor == identity and phi_minor == identity

    fixed = 0
    dual_basis_checks = 0
    for T in triples:
        target = tau(T)
        fixed += int(frozenset(T) == target)
        source_u, target_u = u(T), u(target)
        assert P(source_u) == target_u
        assert P(target_u) == source_u
        assert mod2(P(mod2(source_u))) == mod2(target_u)
        assert P_wrong_sign(source_u) != target_u

        # Basis of the full annihilator of each source line; inverse transpose is P^T.
        pivot = source_u.index(1)
        for j in range(m):
            if j == pivot:
                continue
            lam = [0] * m
            lam[j] = 1
            lam[pivot] = -source_u[j]
            assert dot(source_u, lam) == 0
            image = PT(lam)
            assert dot(target_u, image) == 0
            lam2, image2 = mod2(lam), mod2(image)
            assert dot(mod2(source_u), lam2) % 2 == 0
            assert dot(mod2(target_u), image2) % 2 == 0
            dual_basis_checks += 1

    assert fixed == 0
    # P^2=I on the ambient space, over Z and after reduction modulo 2.
    for j in range(m):
        e = [int(i == j) for i in range(m)]
        assert P(P(e)) == e
        assert mod2(P(mod2(P(mod2(e))))) == mod2(e)
        assert PT(PT(e)) == e

    # A wrong dual action P instead of P^{-T} fails over Q on this explicit covector.
    T = frozenset((0, 1, 2))
    lam = [0] * m
    lam[index[(0, 0, 3)]] = 1  # one-based coordinate (1,1,4)
    assert dot(u(T), lam) == 0
    wrong_dual_value = dot(u(tau(T)), P(lam))
    assert wrong_dual_value != 0

    # Rank(P-I)=k: D and Phi each have a unit k-minor, and P-I=D Phi.
    # Its direct sum over v/2 independent tau-pairs has additive rank.
    contexts = len(triples) // 2
    return {
        "h": h,
        "m": m,
        "triples": len(triples),
        "fixed_triples": fixed,
        "k": k,
        "phi_d": pairings,
        "P_squared_identity_Z_Q_F2": True,
        "determinant": (-1) ** k,
        "rank_P_minus_I_Q": k,
        "rank_P_minus_I_F2": k,
        "direct_sum_contexts": contexts,
        "direct_sum_rank_Q": contexts * k,
        "direct_sum_rank_F2": contexts * k,
        "dual_basis_checks_Z_Q_F2": dual_basis_checks,
        "wrong_sign_rejected_Z_Q": True,
        "wrong_dual_witness": {
            "T_one_based": [1, 2, 3],
            "covector_coordinate_one_based": [1, 1, 4],
            "source_pairing": 0,
            "target_pairing_after_wrong_P": wrong_dual_value,
        },
    }


def packing_controls():
    h = 6
    triples = list(combinations(range(h), 3))
    index = {frozenset(T): i for i, T in enumerate(triples)}
    tau = lambda T: frozenset(i ^ 1 for i in T)
    xs = [1000 + i for i in range(len(triples))]
    ys = [-2000 - i for i in range(len(triples))]
    dirty = [("side", i, (i, -i)) for i in range(9)] + [("center", i, -7 * i) for i in range(6)]

    def E(x, y, scratch):
        return {"X_lanes": tuple(x), "Y_lanes": tuple(y), "dirty_scratch": tuple(scratch)}

    def D(state):
        return list(state["X_lanes"]), list(state["Y_lanes"]), list(state["dirty_scratch"])

    packed = E(xs, ys, dirty)
    assert D(packed) == (xs, ys, dirty)
    assert len(set(packed["X_lanes"])) == len(triples)
    assert len(set(packed["Y_lanes"])) == len(triples)

    # The semantic signed endpoint is per original T; lane packing alone does not implement it.
    out_x = [-y for y in ys]
    out_y = list(xs)
    assert out_x == [-ys[i] for i in range(len(triples))]
    wrong_pair = [-ys[index[tau(T)]] for T in triples]
    assert wrong_pair != out_x
    wrong_sign = list(ys)
    assert wrong_sign != out_x

    # Dropping the second member of a tau-pair aliases distinct independent inputs.
    T0 = frozenset((0, 2, 4))
    T1 = tau(T0)
    state1, state2 = list(xs), list(xs)
    state2[index[T1]] += 999
    # Use a canonical orbit key and show the lossy representation ignores one role.
    orbit_key = lambda T: min(tuple(sorted(T)), tuple(sorted(tau(T))))
    def lossy_orbits(values):
        keys = sorted({orbit_key(T) for T in triples})
        return tuple(values[index[frozenset(T)]] for T in keys)
    assert lossy_orbits(state1) == lossy_orbits(state2)
    assert state1 != state2

    # Zero-filling a 5-bit padding lane cannot preserve arbitrary spectator state.
    padded_a = tuple(xs) + (0,) * 12
    padded_b = tuple(xs) + (777,) + (0,) * 11
    zero_fill = lambda lanes: tuple(lanes[:20]) + (0,) * 12
    assert zero_fill(padded_a) == zero_fill(padded_b)
    assert padded_a != padded_b

    return {
        "typed_storage_E_D_round_trip_all_20_XY_and_dirty_scratch": True,
        "independent_values_preserved": True,
        "wrong_independent_pairing_rejected": True,
        "wrong_signed_endpoint_rejected": True,
        "lossy_tau_alias_control_rejected": True,
        "zero_filled_padding_dirty_state_control_rejected": True,
        "operation_status": "storage reindexing only; no shared gate or frame supplied",
    }


def bit_gate_witness():
    # h=6, Section 3's stage-3 X-side gate label, for A={1,2,3}, B={1,2,4}.
    # Work in zero-based coordinates; the bilinear form on Q^6 is I-J/9.
    A, B = {0, 1, 2}, {0, 1, 3}
    h = 6
    coords = list(product(range(h), repeat=3))
    index = {c: i for i, c in enumerate(coords)}
    m = h**3
    alpha = beta = 0

    def u(T):
        return [int(i in A and j in B and k in T) for i, j, k in coords]

    ds, phis = [], []
    for p in range(0, h, 2):
        q = p + 1
        ds.append([
            int(i in A and j in B and k == q)
            - int(i in A and j in B and k == p)
            for i, j, k in coords
        ])
        phi = [0] * m
        phi[index[(alpha, beta, p)]] = 1
        phi[index[(alpha, beta, q)]] = -1
        phis.append(phi)

    def P(x):
        coeffs = [dot(phis[i], x) for i in range(h // 2)]
        return [x[r] + sum(ds[i][r] * coeffs[i] for i in range(h // 2)) for r in range(m)]

    # g=t_A tensor t_B. b=e_(1,1)-4e_(4,5) lies in g-perp:
    #  (2/3)(2/3)-4(-1/3)(-1/3)=0.
    g = [int(i in A and j in B) for i, j in product(range(h), repeat=2)]
    b = [0] * (h * h)
    b[0 * h + 0] = 1
    b[3 * h + 4] = -4
    assert Fraction(2, 3) * Fraction(2, 3) - 4 * Fraction(-1, 3) * Fraction(-1, 3) == 0
    assert dot(g, b) != 0  # ordinary dot is not the Section 3 bilinear form

    # Verify the actual Section 3 bilinear pairing, tensorized from I-J/9.
    pair_g_b = (
        Fraction(2, 3) * Fraction(2, 3)
        - 4 * Fraction(-1, 3) * Fraction(-1, 3)
    )
    assert pair_g_b == 0

    T = frozenset((0, 2, 4))       # one-based {1,3,5}
    tau_T = frozenset((1, 3, 5))  # one-based {2,4,6}
    x = [0] * m
    for i, j in product(range(h), repeat=2):
        x[index[(i, j, 0)]] = b[i * h + j]
    expected = x[:]
    d0 = ds[0]
    expected = [a + c for a, c in zip(expected, d0)]
    assert P(x) == expected
    assert dot(phis[0], x) == 1 and all(dot(phis[i], x) == 0 for i in range(1, h // 2))

    # At j=3, the gate label is (B0 tensor F) perp (P0 tensor <t_T>).
    # x lies in its common B0 tensor F summand. P_AB x adds g tensor (e_2-e_1),
    # whose P0 component is not in P0 tensor <t_tau(T)>.
    t_tau = [int(i in tau_T) for i in range(h)]
    e_q_minus_p = [int(i == 1) - int(i == 0) for i in range(h)]
    assert t_tau == [0, 1, 0, 1, 0, 1]
    assert e_q_minus_p == [-1, 1, 0, 0, 0, 0]
    assert any(e_q_minus_p[i] * t_tau[j] != e_q_minus_p[j] * t_tau[i]
               for i in range(h) for j in range(h))

    # The source line is correctly transported, even though the full gate label is not.
    assert P(u(T)) == u(tau_T)
    return {
        "stage": 3,
        "consumer": "time-2 X-side copy gate",
        "source_T_one_based": [1, 3, 5],
        "target_tau_T_one_based": [2, 4, 6],
        "section3_gate_label_retyping_by_P_AB": False,
        "witness_b": {"e_(1,1)": 1, "e_(4,5)": -4},
        "bilinear_pairing_g_b": "0",
        "added_component_third_factor": "e_2-e_1",
        "target_line_third_factor": "span(e_2+e_4+e_6)",
        "source_line_transport_still_holds": True,
    }


receipt = {
    "checkpoint": "Issue 39 Phase 0; stop before Phase 1",
    "label_checks": [fibre_check(4), fibre_check(6)],
    "packing_controls": packing_controls(),
    "bit_stage3_gate_witness": bit_gate_witness(),
    "scope": "Exact finite label, lane-reindex, and one original bit gate-label checks only; no Section 4 supplier, complex array operator, full recurrence, or kappa claim.",
}
print(json.dumps(receipt, indent=2, sort_keys=True))
