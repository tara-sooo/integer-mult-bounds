# Obligation ledger

| Obligation | Status | Evidence / remaining condition |
|---|---|---|
| Rational subspace for the selected `FSa`, `Sb2`, `Y2` labels | `PROVED` | The pinned `original_timeline.py` basis rule gives `span{e_0+2e_i}` for these one-point-core envelopes. |
| Nondegeneracy and a rational projector | `PROVED` | `b_i^T G_23 b_j=4 delta_ij`; PR 63's `audit.py` exact formula is the fixed conjugate `L P L^-1`. The h=25 triple line has norm 2. |
| Local embedding into PR 63 dimension `m=575` | `PROVED` | The explicitly chosen basis identification `Q^575 = Q^23 tensor Q^25` and source triple line give compact rational matrices in the required dimension; this embedding is derived for the checkpoint, not serialized by PR 63. |
| Common frame on every incidence of the Y2 XOR shear | `PROVED` | Assign the same `M_Y2` to both input and both output roles; exact commutation and an unequal-port negative control are in `check_local.py`. |
| Rational ranks on the selected neighborhood | `PROVED` | Input edges have rank 4 each; the next same-envelope edge has rank 0. The computation uses exact `Fraction` arithmetic and a rank-one tensor descriptor. |
| Mapping the selected logical use to its exact PR 63 serialized slot/event | `BLOCKED` | Logical DAG IDs can be regenerated, but the pinned rank-pair word schema has no stable source-node/use ID, including for the reversible shear's preserved-`FSa` output. The independent rational timeline is not an ID map into that serialized word. |
| Paid local rank charge in a Section 4 recurrence | `PROPOSED` | If the whole-network substitution is proved, each rank-4 edge contributes four lower-width pivots. Copies, slot ownership, and cleanup for this exact saved-word event are not attributable. |
| Section 4 role-permutation hypothesis for the substituted full circuit | `NOT_EVALUATED` | Need a fixed scalar circuit on all roles whose output is a role permutation `rho`; the pair producer node alone is not such a theorem input. |
| Section 4 endpoint equation | `NOT_EVALUATED` | Need `M_out(rho(w))-M_in(w)=I_575` for every physical role, including data, copied, and auxiliary roles. No local gate check proves this. |
| Global rational edge-rank budget | `INHERITED_WITH_PIN` | PR 63 records aggregate `m=575`, `W=137151806`, rank mass `78860441550`, and deficit `1846900`. This checkpoint does not rederive that as the Section 4 rank sum for a full role-permutation network with verified endpoints. |
| Fixed-prime and finite-tape transfer for a substituted PR 63 matrix family | `NOT_EVALUATED` | Requires the complete finite rational matrix set, denominator/pivot avoidance, and a matching all-size tape argument. |
| Width profile, moment, exponent, or multiplication conclusion | `NOT_EVALUATED` | No local edge is inserted into a new child profile; no `kappa` or global proof claim follows. |

The local rational lift is supported. The global Section 4 instantiation remains open at the exact role-permutation, endpoint, and physical-event ownership interfaces above.
