# Pure-assignment invariance (FAST)

## Claim and hypotheses

Fix the paired-cube source and its ambient parameter `m`. Consider two executions of the three-stage construction related only by reassigning already completed local cores to stage routes. Assume all of the following remain fixed:

1. Every port makes the same three completed-core calls, with the same source-defined local core inputs and widths.
2. The source-frontier and target-frontier child multisets are unchanged.
3. The residual gauge multiset is unchanged, and every residual `sigma` of width `a` still receives the source's three-way orthogonal grouping and one exterior child of width `3a`.
4. Every data port pays both width-two data complements.
5. The full persistent role stock `W0` is unchanged.

These hypotheses describe a pure assignment. They do not assume a new decomposition, a removed call, a different gauge, or a cheaper word.

## Exact multiset argument

Index every child call in the source ledger, retaining its category and source identity. The assignment changes only which stage route carries a completed call. Match each old child to the same source-identified call after reassignment. The first three hypotheses preserve the widths of the local, source, target, and grouped-gauge calls. The fourth preserves exactly `2v` width-two children, and the fifth preserves the normalizing role stock. This is a width-preserving bijection of the complete child-call multisets.

The source ledger expresses these counts per group vertex as

```text
W0 = 2v + R
n_r = 3(H_r + D_r + T_r) + 2v * [r=2] + sum_(a>0) s_a * [r=3a]
```

Here `H_r`, `D_r`, and `T_r` are the local internal, source-frontier, and target-frontier width counts, and `s_a` is the count of residual gauges of width `a`. The hypotheses preserve each term and its source identity; therefore, for every width `r`,

```text
n'_r = n_r
W0' = W0
M'(alpha) = (1/W0') sum_r n'_r (r/m)^(1-alpha)
         = (1/W0)  sum_r n_r  (r/m)^(1-alpha)
         = M(alpha)
```

The equality holds for every `alpha` for which the source defines the moment. In particular, this assignment cannot strictly improve the normalized recursive moment.

The normalized moment is not the full finite construction bill. A different finite router constant can change a guard, row threshold, or finite-size cost while leaving this child multiset and normalized moment exactly unchanged. Such a router saving is not a new recursive supplier saving and does not establish a new `kappa`.

If a proposed change alters any listed multiset, complement count, grouping, or persistent stock, the bijection no longer applies. That changed charge must be recomputed and paid in the complete source profile before comparing moments.

## Orbit diagnostic

For pure relabelings, a common invertible orthogonal action, stage/cube/port ordering, or role-label permutation preserves the multiset of pairwise active-block intersection dimensions. The focused candidate in [TWIST.md](TWIST.md) changes this invariant: the baseline has only zero pairwise intersections, while its `C0` stage-1 block meets the stage-2 block in dimension one. This proves the candidate is not a relabeling; its separate failure of orthogonality is checked in [CHECKS.md](CHECKS.md).

The baseline identities and charge definitions are pinned to the paired-cube source at [commit c8b22bc](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/c8b22bc5c10dba497ac25804e27d9647d818e2ff). The preceding half-cube failure at [Issue 24's result commit](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/6cb527acd8f96019638bf33f520db333d9b26031) is an external control only; its even-parity cube had frozen `B_block=I4`, `K=0`, and `K^2 != I` and is not reused as this candidate.
