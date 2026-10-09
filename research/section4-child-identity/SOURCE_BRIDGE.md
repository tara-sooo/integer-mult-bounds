# Source bridge: a real rational edge to Section 4 calls

## Source choice

The bounded source review started with [PR #144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144)'s selected bit supplier at
commit `c8b22bc5c10dba497ac25804e27d9647d818e2ff`, as requested. Its bit note
and pinned [PR #97](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/97) ledger record the `h=23` word, its finite frame transitions,
selected entrance gauges, and a complete paid outer child histogram. They do
not bind a particular transition to the original Section 4 rational matrix
`M_head-M_tail`, nor serialize an `E_1,Pi,E_2` factorization and its ordered
pivot calls. The `m=69` profile and its child widths therefore cannot identify
a Section 4 call.

[PR #128](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/128)'s completed scalar cores and [PR #130](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/130)'s three-stage data cover are also
different source levels. The [Issue #22](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/22) checkpoint records why their complete
core and outer-cover children are not Section 4 pivot calls. For this screen I
use the original manuscript's own Section 3 bit network, which is the network
to which its Section 4 theorem is applied. This is the clearer frozen
source-to-call connection: Section 3 names the actual wire/gate vertices and
assigns their rational matrices; Section 4 defines one child call for each
one of the chosen edge factorization's `Pi` entries.

The exact manuscript bytes are the ones pinned in `upstream/manifest.json`
under `openai/math@adc7f1241b42e322a6451854ab7e4b4c146bf78a`. No upstream
source or prior Issue worktree was edited.

## Deriving `A_e` from the selected edge's actual frames

In Section 3, for each gate or sink with label `U`, the rational frame matrix
is `M_v=P_U`, the projection onto `U` along `U^perp`. A source `X_a` has
`M_source=-P_{U_a}`; every other source has matrix zero. Thus, for a real wire
edge `e=(u,v)`,

```text
A_e = M_v - M_u.
```

If the endpoint labels are nested, the manuscript proves
`P_V-P_U=P_(V intersect U^perp)` (for `U subset V`), so its rational rank is
the dimension difference. A first `X_a` source edge is the stated exception:
its matrix is `P_Ua-(-P_Ua)=2P_Ua`, of rank one. These are rational
projectors, not ranks inferred from a role histogram.

Select the stage-3 invocation with fixed triples
`T0={1,2,3}` in both fixed coordinates, and its actual central scratch wire
`C_1`. The edge joins the time-1 center gate to the time-3 center gate. In the
source's gate-label table, at stage 3 the labels are

```text
time 1: B tensor F          (the subtract-scatter gate)
time 3: A tensor F = F^tensor3  (the gather gate)
```

Here `F=Q^100`, `A=F tensor F`, `P=<t_T0 tensor t_T0>`, and `B=P^perp` in
`A`. The center wire is untouched at time 1 (it is a control), and time 2
touches no center wire. Therefore the selected segment is a genuine
consecutive-vertex edge, not an invented transition. Its endpoint matrices
and difference are exactly

```text
M_tail = P_(B tensor F) = (I_10000 - P) tensor I_100,
M_head = P_(A tensor F) = I_1000000,
A_e    = M_head - M_tail = P tensor I_100.
```

For the standard basis `e_1,...,e_100` of `F`, let
`G=I-J/9` and `t=1_{T0}`. Then `t^T G t=2`. In the lexicographic tensor
basis of `F tensor F`, with the second coordinate varying fastest, put

```text
u = t tensor t,                 v = (G t) tensor (G t),
P = u v^T / 4.
```

This is the exact orthogonal projection for the manuscript's bilinear form
`G tensor G`: `v^T u=4`, `P^2=P`, and `rank_Q(P)=1`. The tensor extension
therefore has rank exactly 100.

## An exact lower-triangular factorization and actual pivots

Let `n=10000`, let `e_1` and `e_n` denote coordinate columns in `Q^n`, and
define

```text
L = I_n + (u-e_1)e_1^T,
R = I_n + e_n(v^T/4-e_n^T),
Pi_0 = e_1 e_n^T.
```

`L` is lower triangular with diagonal all one: `u_1=1` and its other
nonzero entries are below row 1. `R` is lower triangular because its only
modified row is the last row; its last diagonal entry is
`v_n/4=1/36`, so it is invertible. Direct multiplication gives

```text
L e_1 = u,       e_n^T R = v^T/4,
L Pi_0 R = u v^T/4 = P.
```

The exact factorization for the selected million-dimensional edge is

```text
E_1 = L tensor I_100,
Pi  = Pi_0 tensor I_100,
E_2 = R tensor I_100,
A_e = E_1 Pi E_2.
```

Both `E_1` and `E_2` are invertible lower triangular in the specified
lexicographic coordinate order. `Pi` has exactly 100 ones, at rows
`(1,k)` and columns `(10000,k)`, `1<=k<=100`. The source's elimination order
(topmost nonzero row, rightmost nonzero entry, then repeat) visits these in
increasing `k`: the first two exact pivot pairs are

```text
((1,1),(10000,1)) -> (row 1, column 999901),
((1,2),(10000,2)) -> (row 2, column 999902).
```

The last coordinate conversion uses `index(i,k)=100(i-1)+k`. Section 4
allows the finite factorizations to be selected once and for all; the paper
does not publish a global factorization table. This factorization is an
explicit valid choice for this real edge and supplies its actual pivot
occurrences. The small exact checker verifies the compact rank-one identity
and its tensor lift without materializing a million-by-million matrix.

## Boundary with the PR 144 bit source

The [PR #144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144) bit note remains relevant evidence about paid workspace sharing,
but not about these Section 4 calls. Its selected `h=23` frames and histogram
are generated in a separate local profile, and the fixed files do not give a
map from those records to the manuscript's `M_v` matrices or to ordered
`Pi` pivots. The [PR #144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144) 4,840 width-60 children, for example, are not being
renamed as Section 4 call IDs. This fallback uses the manuscript's own
`h=100`, `m=1,000,000` bit network and a direct real center edge instead.
