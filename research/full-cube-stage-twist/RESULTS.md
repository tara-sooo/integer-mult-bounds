# Results

**Primary first-checkpoint status: `STAGE_ROUTING_COLLISION_OR_NONORTHOGONALITY`.** The one focused `p=4` stage/cube twist is genuinely non-equivalent to the baseline, but it fails orthogonality exactly: for `C0` at stage 1, `QP1` intersects the stage-2 block `P2` in `span(e8)`, and `<e8,e8>=1`. The attempted full construction is illegal.

## FAST

**PASS.** Before testing the candidate, [INVARIANCE.md](INVARIANCE.md) proves the exact source-defined child-multiset lemma for pure completed-core assignments. If completed-core calls, source/target/gauge multisets, two width-two complements per port, three-way grouping of each residual `sigma`, and full persistent role stock all stay fixed, a width-preserving child bijection gives `n'_r=n_r` and the same normalized moment for every source-defined `alpha`. A finite router constant may still differ without changing that normalized moment.

## FOCUSED

**Exact p=4 check completed for the single specified candidate.** The checker confirms all four full eight-port cubes and 32 ports, frozen `B/H/K` identities and `K^2=I`, all twelve stage/cube right-multiplication maps with explicit inverses in `O(24,2)`, all 96 port-stage visits, and all per-cube stage-pair active-block intersections. The baseline intersections are all zero; the candidate has exactly one dimension-one intersection, `C0` stages 1/2. A common `g in O(24,2)` preserves this overlap and its nonzero pairing, so the group-wide failure is exact without enumerating the group.

The data contracts survive: all 32 ports retain their exact adjacent frames in dimension `3h-2=22`, both width-two complements per port remain, and the signed shears multiply to `(X,Y)->(-Y,X)`. The representative completed dirty core and its `Q`-routed conjugate restore arbitrary dirty contents on every one of 72 basis vectors. The triple exterior grouping fails at the nonorthogonal overlap, so the full construction is not legal.

The two focused negative controls pass: the candidate overlap has `<e8,e8>=1`, and omitting final dirty cleanup gives `z'=z+x`. The earlier [Issue 24 result](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/6cb527acd8f96019638bf33f520db333d9b26031) remains an external control only: its even-parity half-cube had frozen `B_block=I4`, `K=0`, and `K^2 != I`. It is not reused as this candidate.

## Paid outcome and scope

**Profile comparison is gated off for the failed candidate.** No child histogram, normalized moment comparison, or new `kappa` is computed. This is one tested nonorthogonal twist, not a general no-go theorem. The frozen paired-cube construction is pinned to [PR 144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144) at [commit c8b22bc](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/c8b22bc5c10dba497ac25804e27d9647d818e2ff); [PR 130](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/130) at [commit 6a9970a](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/6a9970a530119174507904e23592fd59ede19a5d) is the separate three-stage data-cover comparator. [PR 163](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/163), pinned at [commit e181379](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/e1813796ef5c3ca38c5dd7b9e8d81b3908ff5997), is only a separate structural comparison; its values are not combined with this baseline.

**FULL checks: NOT RUN.** No production supplier replay, complete paid profile, full repository verifier, `make verify`, broad CI, global group enumeration, or twist search was run. The workflow stops at the exact focused failure.

## Resource receipt

Command:

```sh
/usr/bin/time -v python3 research/full-cube-stage-twist/check_small.py
```

On 2026-10-09 UTC the checker exited `0` (the expected obstruction was verified): user time `0.17 s`, system time `0.02 s`, elapsed wall time `0.25 s`, maximum RSS `15,076 kB`. The zero exit status means the exact baseline checks and expected candidate failure were reproduced; it does not certify candidate legality.

## Decision

**NO-GO for this twist; stop after the exact failure.** The data shear/frame contracts and representative isolated dirty core survive the twist, but the `C0` stage-1/stage-2 exterior blocks are nonorthogonal. This result does not rule out other outside incidence changes and establishes no new paid saving.
