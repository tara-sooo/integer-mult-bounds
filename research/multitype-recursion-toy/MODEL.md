# Two-type recursion toy model

## Status and inputs

This is a finite feasibility experiment, not a multiplication theorem or a
claim about `κ`. Type A is the PR 62 interval-strip graph with the PR 57 frame
compiler. Type B is the same graph with the PR 60 rank-first compiler used by
PR 63. Their complete pinned bit-child histograms are copied into
[`experiment.py`](experiment.py); `SOURCES.md` records immutable commits,
hashes, and attribution.

Both profiles have `m = 575`, `W = 137151806`, total child rank
`78860441550`, deficit `mW - rank = 1846900`, maximum child width `529`, and
27 distinct child widths. The child histograms differ. These common values
give the same normalization for both scalar moments.

The toy holds the inherited complex profile and outer assembly fixed; it has
no complex-type transition. The scalar `delta` is an artificial aggregate
charge for bit-frame, dirty-state, or tape-layout conversion at a recursive
boundary. It is not measured. If switching also requires a complex-state
conversion, that transition and its cost are **UNPROVEN** and outside this
matrix.

The measured interfaces stop at those finite profiles. The pinned reports do
not define an adapter that lets one compiler consume the other's recursive
child state, preserve arbitrary dirty scratch, or transfer the required tape
layout. Both cross-type edges are therefore **UNPROVEN**. Treating the two
profiles as interchangeable after conversion is an artificial toy
assumption.

## Scalar recurrence and interval arithmetic

For profile `i` and rational saving `a`, use the pinned sufficient moment

```text
M_i(a) = 1/(m W) * sum_t n_i(t) * t * (m/t)^a.
```

The common test point is Type A's pinned saving
`a = 39859/781250000`. Type B's pinned saving is
`2551509/50000000000`, which is greater by exactly `533/50000000000`.
Re-evaluating both complete histograms at Type A's exponent makes the scalar
comparison like-for-like.

All calculations use `fractions.Fraction`. For logarithms, range-reduce
`x = m/t = 2^k r`, with `1 <= r < 2`, then enclose
`log r = 2 sum z^(2j+1)/(2j+1)` for `z = (r-1)/(r+1) <= 1/3`; the omitted tail
is bounded by `2 z^(2N+1)/((2N+1)(1-z^2))`, with `N = 32`. The exponential
uses its degree-8 Taylor partial sum and a geometric upper bound on the
remaining positive terms. The script rounds interval endpoints outward to
denominator `10^24`. Its own-saving enclosures also fall inside the pinned
certificates' coarser `10^18` intervals.

## Typed schedule and conversion charges

Rows are parent types and columns are child-recursion types. Every child from
a parent profile is assigned exactly once. The no-switch baselines are

```text
D(a) = [[M_A(a), 0], [0, M_B(a)]].
```

The proposed alternating schedule assigns all Type A children to Type B and
all Type B children to Type A:

```text
A_delta(a) = [[0, (1 + delta) M_A(a)],
              [(1 + delta) M_B(a), 0]].
```

Here `delta * M_i(a)` is an explicitly charged conversion/work allowance:
`delta = 0` is the idealized zero-conversion control, `delta = 1/10^10` is a
small positive toy charge, and `delta = 1/1000` is an expensive-switch
control. None is measured from a real adapter. The positive values are
deliberately artificial and do not certify a legal physical transition.

For a nonnegative 2-cycle matrix, the exact spectral radius is
`(1 + delta) sqrt(M_A M_B)`. The script encloses that value with rational
square-root bounds. The no-switch spectral radius is `max(M_A, M_B)`; the
better standalone scalar baseline is `min(M_A, M_B)`.

More generally, in this routing-only model any schedule that assigns every
child once and charges nonnegative conversion work has row sum at least
`M_i(a)` in row `i`. Thus `A 1 >= min_i(M_i) 1`, and positivity gives
`rho(A) >= min_i(M_i)`. Such routing can never beat the best standalone
profile. A benefit would require a new mixed construction that changes the
child histogram or work normalization, or a proved adapter that changes the
child work itself; neither is represented by these pinned profiles.

## Self-check

The executable contains exact 2-by-2 controls: an identical-type reduction
with zero fee and a known positive-fee scaling. It also checks both pinned
rank identities, the source-certificate enclosures, and the strict ordering
of the tested moments. Run it with:

```sh
python3 research/multitype-recursion-toy/experiment.py
```
