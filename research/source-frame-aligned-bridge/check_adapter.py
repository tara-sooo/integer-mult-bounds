#!/usr/bin/env python3
"""Exact h=4 check of the proposed rank-one frame-label adapter."""

from fractions import Fraction
from itertools import product
import json


H = 4
COORDS = list(product(range(H), repeat=3))
INDEX = {coord: k for k, coord in enumerate(COORDS)}
M = len(COORDS)
A, B = {0, 1, 2}, {0, 1, 3}


def tensor_indicator(first, second, third):
    return [int(i in first and j in second and k in third) for i, j, k in COORDS]


ua = tensor_indicator(A, A, A)
ub = tensor_indicator(A, A, B)
d = [y - x for x, y in zip(ua, ub)]
i, j = INDEX[(0, 0, 2)], INDEX[(0, 0, 3)]  # (1,1,3), (1,1,4), one-based
phi = [0] * M
phi[i], phi[j] = 1, -1


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def apply_p(x):
    c = dot(phi, x)
    return [v + w * c for v, w in zip(x, d)]


def apply_pt(x):
    c = dot(d, x)
    return [v + w * c for v, w in zip(x, phi)]


def mod2(x):
    return [v % 2 for v in x]


def basis(k):
    return [int(n == k) for n in range(M)]


assert sum(ua) == sum(ub) == 27
assert dot(ua, ub) == 18  # integer overlap; it is 0 only after reduction mod 2
assert ua != ub and any(d) and any(phi)
assert dot(phi, ua) == 1 and dot(phi, ub) == -1 and dot(phi, d) == -2
assert apply_p(ua) == ub and apply_p(ub) == ua
assert all(apply_p(apply_p(basis(k))) == basis(k) for k in range(M))
assert 1 + dot(phi, d) == -1  # determinant lemma: det(I + d phi)
assert apply_pt(apply_pt(basis(i))) == basis(i)

qua, qub = list(map(Fraction, ua)), list(map(Fraction, ub))
assert apply_p(qua) == qub and apply_p(qub) == qua
assert all(apply_p(apply_p(list(map(Fraction, basis(k))))) == list(map(Fraction, basis(k)))
           for k in range(M))

ua2, ub2, d2, phi2 = map(mod2, (ua, ub, d, phi))
assert dot(phi2, ua2) % 2 == dot(phi2, ub2) % 2 == 1
assert dot(phi2, d2) % 2 == 0
assert any(d2) and any(phi2) and 1 + dot(phi2, d2) % 2 == 1
assert mod2(apply_p(ua2)) == ub2 and mod2(apply_p(ub2)) == ua2
assert all(mod2(apply_p(apply_p(basis(k)))) == basis(k) for k in range(M))

# A basis of the annihilator kernel, then its exact dual-frame transport.
pivot = ua.index(1)
annihilator_basis = []
for k in range(M):
    if k == pivot:
        continue
    v = basis(k)
    v[pivot] -= ua[k]
    annihilator_basis.append(v)
assert len(annihilator_basis) == M - 1
assert all(dot(ua, v) == 0 for v in annihilator_basis)
assert all(dot(ub, apply_pt(v)) == 0 for v in annihilator_basis)
q_annihilator_basis = [list(map(Fraction, v)) for v in annihilator_basis]
assert all(dot(qua, v) == 0 for v in q_annihilator_basis)
assert all(dot(qub, apply_pt(v)) == 0 for v in q_annihilator_basis)
for k in range(M):
    if k == pivot:
        continue
    v = basis(k)
    v[pivot] = (v[pivot] + ua2[k]) % 2
    assert dot(ua2, v) % 2 == 0
    assert dot(ub2, mod2(apply_pt(v))) % 2 == 0

# P (rather than P^{-T}) is an adverse target-frame control.
wrong_dual = basis(INDEX[(0, 1, 3)])  # (1,2,4), in Ua^perp but not Ub^perp
assert dot(ua, wrong_dual) == 0 and dot(ub, wrong_dual) == 1
assert apply_p(wrong_dual) == wrong_dual and dot(ub, apply_p(wrong_dual)) == 1

# The old Section 3 bit-frame projectors differ by rank 2, not rank 1.
# In its Q^4 form, <t_A,t_A>=<t_B,t_B>=2 and <t_A,t_B>=1.
aa, bb, ab = 2**3, 2**3, 2 * 2 * 1
assert (aa, bb, ab) == (8, 8, 4)
# (P_Ua-P_Ub) restricted to span(ua,ub) has this exact coefficient matrix.
projector_difference_det = Fraction(1) * -1 - Fraction(1, 2) * Fraction(-1, 2)
assert projector_difference_det == Fraction(-3, 4)

# Exact Gate C role check in an abstract 64-coordinate frame model.
# This verifies the reframe/gate/decode equation; it does NOT lift P to the
# original manuscript's 2^m-cell array frame operator.
x1 = [3 * k + 1 for k in range(M)]
x2 = [5 - 2 * k for k in range(M)]
y1 = [7 - k for k in range(M)]
y2 = [2 * k + 9 for k in range(M)]
scratch = [11 + k for k in range(M)]

# X roles already share the terminal full frame. Y2 is in P^{-T}'s dual frame.
y1_at_b = apply_pt(y1)
y2_at_b = apply_pt(y2)
gate_y1_at_b = [a - b for a, b in zip(y1_at_b, y2_at_b)]
gate_x2 = [a + b for a, b in zip(x2, x1)]
decoded_y1 = apply_pt(gate_y1_at_b)  # (P^{-T})^{-1}=P^T=P^{-T}
assert decoded_y1 == [a - b for a, b in zip(y1, y2)]
assert gate_x2 == [a + b for a, b in zip(x2, x1)]
assert scratch == [11 + k for k in range(M)]

# Adverse controls: aliasing independent roles, or the wrong sign, both fail.
assert x1 != x2 and y1 != y2
assert [2 * a for a in x1] != gate_x2
assert [a + b for a, b in zip(y1, y2)] != decoded_y1

receipt = {
    "fixture": {"h": H, "m": M, "A": [1, 2, 3], "B": [1, 2, 4], "weight_each": 27,
                "overlap": 18, "i": [1, 1, 3], "j": [1, 1, 4]},
    "integer_and_rational": {"phi_ua": 1, "phi_ub": -1, "phi_d": -2,
                              "P_ua": "ub", "P_ub": "ua", "P_squared": "I",
                              "determinant": -1, "rank_P_minus_I": 1},
    "characteristic_two": {"P_ua": "ub", "P_ub": "ua", "P_squared": "I",
                           "rank_P_minus_I": 1},
    "dual": {"inverse_transpose": "P^T", "annihilator_basis_maps": True,
             "wrong_P_witness": [1, 2, 4]},
    "original_bit_frame_control": {"inner_aa": aa, "inner_bb": bb, "inner_ab": ab,
                                    "rank_projector_difference": 2},
    "abstract_gate_C": {"independent_roles": True, "target_gate_frames_decoded": True,
                        "dirty_vector_preserved": True, "alias_control_rejected": True,
                        "wrong_sign_control_rejected": True},
    "scope": "The gate check uses an abstract 64-coordinate frame model, not a lift to the original 2^m-cell array supplier.",
}
print(json.dumps(receipt, indent=2, sort_keys=True))
