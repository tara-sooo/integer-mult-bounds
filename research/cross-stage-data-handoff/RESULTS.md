# Results

## Primary checkpoint result

**`LEGAL_HANDOFF_BUT_NO_DATA_GAIN`.** The existing stage-1 output `Y1_a` is a
lawful typed value: stage 2 reads it as source, and stage 3 later uses the
same unchanged value as target input. Exact composition gives the original
signed endpoint on the complete triple-indexed bank. This pass-through does
not alter the source/target itinerary, frame edges, or role stock, and removes
no recursive data child.

The p=5,h=10 fixture verifies ten full eight-selector cubes and 80 local
three-element ports. It also checks the original Section 3 formulas over all
120 triples at h=10, and exhibits a consumer at a real `T^3` address. The 80
local ports and 120-port source type remain distinct in the checker and
ledger.

## Exact checks

- Complex local coefficients are exact `Fraction` values; the local
  `K+H+B=I`, `K^2=I`, orthogonality, and center factorization checks pass.
- The complex and bit side-plus-center identities pass on all 80 local ports
  and all 120 h=10 triples. The bit instance is built directly over `F2`.
- Every local forward and inverse shear passes on each source basis vector
  with nonzero arbitrary dirty scratch; the dirty state returns exactly.
- Three completed stages send `(X,Y)` to `(-Y,X)` over the signed complex
  domain and exchange the banks over `F2`.
- The actual witness `a=({0,2,4},{0,2,4},{0,2,4})` shows `Y1_a` read by
  stage 2 and retained as the stage-3 target value.
- Both adverse controls reproduce their exact failures: late cleanup after
  stage 2 leaves side and center scratch dirty; omitted cleanup and a wrong
  complex stage-2 sign fail their expected state or endpoint.
- The exact h=10 Section 4 bit edge histograms reproduce
  `s=Wm-N+2L`. Both the local 80-port and full 120-port profiles have `s>Wm`.

The bounded checker completed with exit status 0. `FULL` all-size compilation,
all-size recursion, precision/recovery, and a new physical supplier were not
run.

## Stop decision

No frame search or moment tuning follows: every charged data transition is
unchanged, and the p=5 local block does not satisfy the Section 4 rank-saving
gate. The [PR 203](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/203)
ceilings also stop any attempt to reach `a=0.01` while retaining the
[PR 193](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/193)/
[PR 187](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/187)
data child multisets. [Issue 25](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/25)
rules out using a pure stage route permutation as a substitute for a changed
data itinerary.

The bounded result does not rule out a new full-array data map. The missing
bridge for a p=5 paired-cube-derived change must assign all 120 triples,
including the 40 repeated-pair triples, preserve every ordered incidence and
dirty correction, match both stage-boundary frames and all-role endpoints,
and produce a complete paid rank ledger with a strictly smaller data
submultiset.

## Next research direction

Choose a candidate that changes a specific source/target data edge. Before
building frames, write its full `T^3` input/output equation and identify the
complete old child and proposed replacement child, including spectator data.
Use [Issue 23](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/23)'s
complete-payload separation and the [PR 203](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/203)
fixed-data ceiling as early rejection tests. Continue only if that equation covers all triples
and deletes a non-tautological paid data rank transition after auxiliary,
cleanup, complement, and routing costs are included.
