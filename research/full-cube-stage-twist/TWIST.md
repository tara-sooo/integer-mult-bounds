# One full-cube stage twist

## Frozen geometry and candidate map

Use `p=4`, `h=8`, `m=24`. There are four cubes, one for each omitted pair label in `{0,1,2,3}`. Every cube retains all eight selector strings and all eight actual ports, for 32 ports total. `C0` is the cube omitting pair label `0`, so its pair labels are `(1,2,3)`.

Let `P1`, `P2`, and `P3` be the coordinate spans of `e0..e7`, `e8..e15`, and `e16..e23`. Let `H1=I`; let `H2` swap `ei` with `e(i+8)` for `i=0..7`, and let `H3` swap `ei` with `e(i+16)` for `i=0..7`. Thus `Hj(P1)=Pj`. Let `Q` swap `e0` and `e8`, fixing the other 22 coordinate vectors. Define the one candidate by

```text
H'_(j,C) = Q H1   if j=1 and C=C0
           Hj     otherwise.
route: g -> g H'_(j,C)
```

For each fixed stage `j`, cube `C`, and role label `r`, the candidate map on logical vertices is `g -> g H'_(j,C)`, with inverse `g' -> g'(H'_(j,C))^-1`; `r` is unchanged. The twelve multipliers are in `O(24,2)`: each is a coordinate permutation, and each is its own inverse (`I`, `H2`, `H3`, or `Q`). Therefore each individual stage/cube map is a bijection.

The data-port index is unchanged by this route. Each of the 32 support sets remains attached to its original cube, source/target roles, and all three stage calls. The local `B/H/K` operators, source channels, data shears, gauges, and complements are not edited by the candidate.

## Aggregate shared-stock occupancy

The pinned [PR 144 sharing note](https://redirect.github.com/CrocSwap/integer-mult-bounds/blob/c8b22bc5c10dba497ac25804e27d9647d818e2ff/notes/paired-cube-sharing.tex) indexes one physical auxiliary bank by `(g,r)`; it has no cube coordinate, and its stage route `g -> gH_j` is cube-independent. The candidate's four stage-1 maps instead send the same logical vertex `g` to `g` for the three cubes other than `C0`, and to `gQ` for `C0`. Since `Q != I`, cancellation in the group gives `gQ != g` for every `g`; right multiplication by `Q` is itself a bijection. At `g=I` the exact image multiplicities are three `I` images and one `Q` image, so the image set is `{g,gQ}` with multiplicities `3,1` for every `g`.

This proves the per-cube maps are bijective, but does not establish a one-to-one occupancy map for the retained shared physical role stock across cube components. The source does not establish that a particular role label `r` is shared across those cube calls, so this is not a proven physical-role collision. Aggregate shared-stock occupancy is **UNRESOLVED / NOT PASSED**. A cube-split schedule, extra routing, or copied role stock would need its own ownership proof and price; none is supplied here. The candidate is not established as a legal drop-in.

## Exact active-block invariant

For one cube `C`, its three active blocks at the identity group vertex are `H'_(j,C) P1`; at an arbitrary vertex `g`, they are `g H'_(j,C) P1`. The baseline has dimension-zero intersections for all three stage pairs in every cube.

In `C0`, the candidate has

```text
QP1 = span(e1,e2,e3,e4,e5,e6,e7,e8)
H2P1 = P2 = span(e8,e9,e10,e11,e12,e13,e14,e15)
```

so `dim(QP1 intersect H2P1)=1`, with the exact witness `e8`. Its self-pairing is `<e8,e8>=1`, so these blocks are not orthogonal. The other two `C0` stage-pair intersection dimensions are zero. In each of the other three cubes all three pair dimensions remain zero. Across the twelve per-cube stage pairs, the invariant is one dimension-one intersection and eleven zero intersections; the baseline has twelve zero intersections.

The intersection dimensions and pairings persist for every `g in O(24,2)` because a common invertible orthogonal map preserves both subspace intersections and the bilinear form. Stage/cube relabeling, pair-coordinate permutation or flip, group action, orthogonal conjugation, and role-label permutation can only permute this invariant. Thus the candidate is genuinely non-equivalent to the baseline, while failing the required orthogonality contract. It is not a legal construction.

The data part remains separate: the signed shears, adjacent 22-dimensional data frames, and one representative isolated dirty core (including its `Q`-routed conjugate) pass their exact checks. The three-way exterior grouping cannot be used for `C0` stage 1/2 because the active blocks overlap nonorthogonally. No full construction follows from this twist.
