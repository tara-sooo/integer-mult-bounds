# Exact toy results

## Outcome

**`NO_GAIN_IN_TESTED_MODEL`** at the common rational exponent
`a = 39859/781250000`. The better scalar profile is Type B. The alternating
matrix's spectral radius is strictly greater than Type B's moment with both
zero conversion cost and a positive conversion charge. The test therefore
does not establish an actual `κ` improvement.

## Certified moments and spectral radii

All intervals below are exact rational enclosures with denominator `10^24`.
The intervals include every child width in the corresponding pinned profile.

| Quantity | Lower numerator | Upper numerator |
|---|---:|---:|
| `M_A(a)` | 999999999998609463268091 | 999999999998609463268092 |
| `M_B(a)` | 999999995103647183328968 | 999999995103647183328969 |
| No-switch `rho(D)` | 999999999998609463268091 | 999999999998609463268092 |
| Alternating `rho`, `delta = 0` | 999999997551128320303447 | 999999997551128320303449 |
| Alternating `rho`, `delta = 1/10^10` | 999999997651128320058560 | 999999997651128320058562 |
| Alternating `rho`, `delta = 1/1000` | 1000999997548679448623750 | 1000999997548679448623752 |

Each row is the displayed numerator interval divided by `10^24`. The first
two intervals are disjoint: `M_A > M_B`, so Type B is the best standalone
baseline. Even with zero conversion cost, the alternating lower bound exceeds
the Type B upper bound by `2447481136974478/10^24`. With the positive
`1/10^10` charge, the excess is `2547481136729591/10^24`. The positive-cost
alternation is still below Type A, so it improves the worse no-switch choice
while losing to the best scalar choice. The `1/1000` stress switch has
`rho > 1` and is not contracting at this exponent.

The no-switch baseline matrix is `diag(M_A, M_B)`. The zero-fee alternating
matrix is `[[0, M_A], [M_B, 0]]`; the positive-fee matrix multiplies both
off-diagonal entries by `10000000001/10000000000`. Their exact spectral
radii are respectively `max(M_A, M_B)` and
`(1 + delta) sqrt(M_A M_B)`, enclosed by the rational intervals above.

The identical-type control gives `rho = M` at zero fee and
`rho = (11/10)M` for a `1/10` fee. Source-certificate containment and all
assert-based arithmetic checks pass. In this routing-only model, allocating
the complete child work among types preserves each row's baseline work; any
nonnegative conversion cost can only increase its row sum. The row-sum bound
in `MODEL.md` rules out beating the best scalar moment for any such allocation,
not just the alternating schedule tested numerically.

## Reproduction and verification status

Command:

```sh
/usr/bin/time -p python3 research/multitype-recursion-toy/experiment.py
```

Recorded stdout summary:

```text
common_a=39859/781250000
M_A=[999999999998609463268091,999999999998609463268092]/10^24
M_B=[999999995103647183328968,999999995103647183328969]/10^24
rho_no_switch=[999999999998609463268091,999999999998609463268092]/10^24
rho_alternating_zero_fee=[999999997551128320303447,999999997551128320303449]/10^24
rho_alternating_fee_1e-10=[999999997651128320058560,999999997651128320058562]/10^24
rho_alternating_fee_1e-3=[1000999997548679448623750,1000999997548679448623752]/10^24
controls=identical-type PASS; source-cert cross-check PASS; exact self-check PASS
result=NO_GAIN_IN_TESTED_MODEL
```

Elapsed time on this Termux run: `0.79 s` real (`0.70 s` user). No heavy
profile regeneration or physical-word replay was run. `make verify` was not
run, as required. This checks only the toy arithmetic and embedded profile
invariants; it does not check real type-conversion legality, outer assembly,
or inherited all-size multiplication hypotheses.

## Limitation

This result falsifies the hope that merely routing the two fixed child
histograms between recursive types improves on the better scalar moment.
It says nothing about a new circuit that jointly changes a row's child
histogram, a different potential/normalization with a proved interface, or
integer multiplication outside this toy family. No `κ` value is inferred from
the spectral-radius comparison.

Even a future toy spectral improvement would not itself improve `κ`. It would
need a legal adapter and a regenerated exact finite certificate for the mixed
child profiles; then the outer assembly's 47 strict inequalities and seven
margins would need to be recomputed. The all-size compiler, arbitrary-dirty
scratch restoration, fixed-tape layout, and inherited complex, routing,
analytic, and exact-recovery arguments would also need to cover the mixed
recursion. None of those obligations is discharged here.
