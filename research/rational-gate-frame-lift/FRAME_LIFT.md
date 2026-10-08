# Local rational frame lift: `FSa -> Y2`

**Status: `LOCAL_FRAME_LIFT_SUPPORTED`.** A rational frame assignment for the selected logical gate can be derived from the frozen PR 63 source. This is a local result; it does not instantiate the manuscript's whole finite-network theorem.

## Existing rational frame data

The statement in Issue 15 that the serialized rank-pair word does not contain per-use rational matrices is correct. The stronger inference that the inherited source has no rational frame assignment is not: PR 62 and PR 63 include `research/pair-assembly/original_timeline.py` and `research/pair-assembly/audit.py`.

`original_timeline.py` maps each active node's `(core, cover)` to an exact rational subspace basis and checks input-to-gate subspace containment. For a one-point core `{0}`, let `I` be the cover coordinates other than `0`.

```text
U_I = span_Q { b_i : i in I },     b_i = e_0 + 2 e_i.
```

For `G_h = I_h - J_h/9`, `b_i^T G_h b_j = 4 delta_ij`. Thus `U_I` is nondegenerate and its rational orthogonal projector is

```text
P_I = (1/4) sum_(i in I) b_i b_i^T G_h.
```

The PR 63 `audit.py` formula stores the same projector after the fixed coordinate change `L = I + J`, `L^-1 = I - J/(h+1)`: `P_hat_I = L P_I L^-1`. Its exact checks establish idempotence, rank, image containment, and self-adjointness in the transformed rational metric. A single conjugation is used for every envelope, so it preserves nesting, common-frame equality, and every edge rank. The checker below verifies this equality for the selected labels.

This fills a mathematical gap in Issue 15 while preserving its separate serialization finding: `(core, cover)` is a source-defined rational-subspace descriptor here, but the frozen rank-pair word still does not retain the source-use-to-word-event ID.

## Selected source gate and incidences

The selected h=23 graph is regenerated from the pinned `pair_graph.py` using `graph(23)`. At recursion level 2, group pair `(i,j)=(0,1)` and members `(a,a2)=(0,1)`, `(b,b2)=(2,3)`, the source expressions are:

```text
F = local node 456
Sa = local node 466
FSa = F + Sa = local node 505
Sb2 = local node 483
Y2 = FSa + Sb2 = local node 510
out[a,b2] = e(a2,b) + Y2 = local node 514
```

For common point 0, the shared-point graph maps these to logical graph nodes `FSa=2039`, `Sb2=2020`, `Y2=2044`, and consumer `2048`. The immediate arguments are `(1996,2006)`, `(1977,2019)`, `(2039,2020)`, and `(1952,2044)`, respectively. These are regenerated **logical DAG IDs**, not physical word-event IDs.

All four nodes have core mask `0x1`. Their cover masks and rational frame dimensions are:

| Logical value | Cover mask | Outside set `I` | `dim_Q U_I` |
|---|---:|---|---:|
| `FSa` (2039) | `0x7c03c3` | `{1,6,7,8,9,18,19,20,21,22}` | 10 |
| `Sb2` (2020) | `0x7c3c03` | `{1,10,11,12,13,18,19,20,21,22}` | 10 |
| `Y2` (2044) | `0x7c3fc3` | `{1,6,7,8,9,10,11,12,13,18,19,20,21,22}` | 14 |
| next consumer (2048) | `0x7c3fc3` | same as `Y2` | 14 |

Both input spaces are contained in `U_Y2`. `Y2` has one outgoing logical use, at node 2048; there is no direct output-terminal incidence in this selected graph slice. The logical roles are the `FSa` and `Sb2` value uses entering this gate and the single `Y2` value passed to its consumer. The reversible shear also has a preserved-`FSa` output role; the selected logical DAG does not give that role a separate use ID. The frozen rank-pair word does not say which physical slots own these uses, so `A_out` below refers only to the logical `Y2 -> 2048` edge.

## Matrices and exact edge ranks

The PR 63 certificate fixes address dimension `m=23*25=575`. The inherited audit supplies rational projectors on the h=23 envelope space, but no per-gate 575-by-575 matrix. For this local witness, choose the standard ordered-pair basis identification `Q^575 = Q^23 tensor Q^25`, place the h=23 envelope in the first factor, and select the source-defined h=25 triple `T={0,1,2}` in the second. This is an explicit local embedding derived here, not a matrix recovered from the serialized word or a claim that the full PR 63 graph already carries this assignment. Let `t_T=e_0+e_1+e_2`. Since `t_T^T G_25 t_T=2`,

```text
P_T = (1/2) t_T t_T^T G_25
M_I = P_hat_I (h=23) tensor P_T (h=25),   M_I in Q^(575 x 575).
```

This is a compact exact description of a 575-by-575 rational matrix. The tensor lift over one selected h=25 triple is derived here; PR 63 does not serialize a dense per-gate 575-by-575 matrix. The local matrix denominators have only 2 and 3 as prime factors, so `q=5` defines the address shear `Phi_M:(H,D)->(H+MD,D)` modulo `5^b`. It is invertible even though `M` is a projection: `Phi_-M` is its inverse. This does not select the separate prime required by a global Section 4 pivot table.

At the Y2 gate, assign the **same** `M_Y2` to both input incidences and both output roles of the reversible XOR shear `(x,z)->(x,x+z)`. Assign `M_FSa` and `M_Sb2` at the preceding producer vertices; assign `M_Y2` at the next consumer. Pointwise linearity then gives the common-frame commutation required by Section 3.

The exact edge differences are

```text
A_FSa = M_Y2 - M_FSa
       = (P_hat_Y2 - P_hat_FSa) tensor P_T,   rank_Q = 4
A_Sb2 = M_Y2 - M_Sb2
       = (P_hat_Y2 - P_hat_Sb2) tensor P_T,   rank_Q = 4
A_out = M_next - M_Y2 = 0,                   rank_Q = 0.
```

For the normalized projectors, `P_Y2-P_FSa` is the orthogonal projection onto the four new directions indexed by `{10,11,12,13}`; `P_Y2-P_Sb2` uses `{6,7,8,9}`. Each has rational rank 4. Conjugation by `L` preserves those ranks, and tensoring with the rank-one `P_T` preserves them again. The exact rank-one-sum description is

```text
P_Y2 - P_FSa = (1/4) sum_(i in {10,11,12,13}) b_i b_i^T G_23,
P_Y2 - P_Sb2 = (1/4) sum_(i in {6,7,8,9}) b_i b_i^T G_23.
```

Writing `K=L^-1` and `G_575=G_23 tensor G_25`, the actual compact 575-dimensional edge matrix for FSa is

```text
A_FSa = (L tensor I_25) [ (1/8) sum_(i in {10,11,12,13})
          (b_i tensor t_T)(b_i tensor t_T)^T G_575 ] (K tensor I_25).
```

Replace the index set by `{6,7,8,9}` for `A_Sb2`. This gives each edge matrix as four exact rational rank-one terms, conjugated by a fixed invertible rational matrix. Thus Section 4's factorization would yield four pivots per rank-4 edge if this finite network were otherwise a valid Section 4 input. The two scalar incidences do not themselves establish eight calls in the frozen PR 63 compiler.

The local scalar shear has `rank_F2(S-I)=1`. That value is not either address-edge rank: the relevant ranks are over `Q` on the 575-dimensional address-frame differences, and are 4. The checker rejects both this rank substitution and assigning different frames to the two XOR ports.

## Proven and missing arrows

```text
(core,cover) -> rational envelope basis -> rational P_hat_I in Q^(23x23)
             -> P_hat_I tensor P_T in Q^(575x575)             [PROVED locally]
common M_Y2 on every Y2 gate incidence -> XOR commutation     [PROVED locally]
source/target matrices -> ranks (4,4,0) on the incident edges  [PROVED locally]
logical node/use -> exact slot/event in saved rank-pair word    [NOT SERIALIZED]
local neighborhood -> complete role permutation and endpoints [NOT ESTABLISHED]
```

The original Section 4 endpoint condition remains the exact global equation

```text
M_out(rho(w)) - M_in(w) = I_575  for every physical role w,
```

for a fixed scalar circuit that permutes all roles. This local producer gate is internal and does not contradict that equation; it does not supply a whole-network `rho`, terminal matrices, the global rational rank sum, or the fixed-prime/tape transfer. The recorded width histogram and rank totals cannot fill those missing fields by interpreting an aggregate row as this edge.
