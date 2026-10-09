# Matched cost gate

## One \(h=6\) invocation

Here \(v=20\), \(m=216\), and a fixed \((A,B)\) is one stage-3
invocation. It has 20 X data roles, 20 Y data roles, and arbitrary
scratch. From the original neighbor definitions:

| Side | Neighbors per triple | Side scratch | Center scratch | Local roles |
|---|---:|---:|---:|---:|
| bit | \(3\binom{3}{2}=9\) | 180 | 6 | \(40+180+6=226\) |
| complex | \(\binom{3}{3}+3\cdot3=10\) | 200 | 7 | \(40+200+7=247\) |

These are local invocation counts, not a global recurrence supplier.

## Direct sum versus lane storage

One application of the rank-three label adapter to ten independent
\(\tau\)-pair contexts has rank mass 30. Entry plus return has abstract
label rank mass 60. Section 4 does not charge label rank directly, so
these are diagnostics, not legal child counts.

Even under the favorable hypothetical that one legal rank-three frame
operation could act on all ten contexts packed into one lane stream, the
first-order paid work is unchanged: ten streams give
\(30\cdot(V/10)=3V\); one packed stream gives \(3\cdot V=3V\).
Equivalently, \(s/W=30/10=3/1=3\). The lane pack stores the same number
of values. Moving separate input tapes into lane-major storage and
decoding them again adds linear data movement unless the layout is
already present. This calculation is an equal-volume screen, not a new
recurrence proof.

No complete original recursive child has been identified as deleted or
replaced: the matched deletion count is zero. No physical entry/exit
frame, copied helper, auxiliary role, routing, decoder, or scratch
restoration cost is available for a new ledger. The role-compressed
layout changes scalar roles into vector-valued data and has no proved
\(W',m',s'\), positive-rank histogram, maximal-rank bound, or paid
moment \(M'(a)\). Thus there is no matched legal bit/complex child
ledger and no \(\kappa\) calculation.

## Existing upstream baseline

The current pinned [upstream PR 234](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/234)
already reports a conditional five-stage bit-plus-complex construction
at head
[af3fe331ca60c936229e060681ffccbc1c208678](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/af3fe331ca60c936229e060681ffccbc1c208678):

| Reported quantity | Bit | Complex |
|---|---:|---:|
| \(m\) | 120 | 110 |
| \(W\) | 23,683 | 14,692 |
| positive-rank calls | 495,304 | 361,405 |
| rank mass \(s\) | 2,837,560 | 1,613,040 |
| deficit \(mW-s\) | 4,400 | 3,080 |
| largest child | 100 | 46 |

That PR reports conditional \(\kappa=0.000703701743496697>2^{-11}\).
That report bundles five disjoint temporal address windows before paid
exterior completion and retains its stated source, analytic, precision,
and routing hypotheses. The temporal batching and paid helpers are
already credited there; this fibre relabeling is not a new temporal
sharing result. No full PR 234 verifier replay was needed for this
bounded obstruction checkpoint.
