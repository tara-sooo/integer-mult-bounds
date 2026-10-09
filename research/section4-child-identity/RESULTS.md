# Results

**Outcome: `NO_IDENTICAL_CHILD_INPUTS_IN_TESTED_SCOPE`.** Under the explicit
valid factorization and call order recorded here, the bounded screen found no
legal reusable pair among the first two actual `Swap_1` calls of one real
rank-100 Section 4 edge. The exact live-input counterexample and the different
pivot functions reject the apparent same-rank/same-shape match. This is not a
global impossibility claim.

## Evidence

- **FAST source map: PASS.** Read [Issue #23](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/23) and [Issue #22](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/22) at commit
  `a59478900d41aaac56f2a1f9418440cf5a49a47d`; inspected the pinned
  [PR #128](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/128),
  [PR #130](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/130),
  and [PR #144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144) sources, then traced the original manuscript's Section 3
  rational labels into the Section 4 pivot generator.
- **[Issue #22](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/22) checkpoint: PASS.** Its `check_small.py` was rerun read-only;
  the exact group, orthogonal phase, arbitrary-dirty cleanup, entrance-gauge,
  and paid-complement checks all passed with the source's negative controls.
- **FOCUSED exact algebra: PASS.** The selected stage-3 center edge has
  `A_e=P tensor I_100`, rank 100. An explicit lower-triangular
  `E_1,Pi,E_2` factorization gives the first two real pivots at
  `(1,999901)` and `(2,999902)`. The standard-library checker verifies the
  compact rational identities and exact separating controls.
- **FULL: NOT RUN.** No PR producer rebuild, million-dimensional dense
  matrix, complete Section 4 compilation, full paper verification, or global
  edge search was run. The exact tensor factorization avoids materializing
  the million-by-million matrix.

The call records are source-derived semantic edge/pivot keys, not fabricated
run IDs. The finite theorem is quantified over arbitrary bit arrays and does
not supply a concrete production tape instance. The checker instead gives a
legal exact input that separates the two complete symbolic input maps.

## Decision

**NO-GO for this duplicate-child handoff branch.** The first child returns a
full array to the active stream; the next call has a different target pair and
receives the post-pivot stream. No child result can be removed from the
complete paid profile on this evidence. Close this bounded local search and
move the next experiment to a changed outer cover or multiplication
construction that changes the paid child-work operator. [PR #130](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/130)'s data-cover
change and [PR #144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144)'s paired-cube/shared-bank construction are useful distinct
design references; neither should be relabeled as a Section 4 child cache.

No `kappa` improvement, typed recursive handoff, or recurrence-cost reduction
is proved. The original conditional recurrence remains the only claim at
that layer.
