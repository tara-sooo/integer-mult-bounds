# Results: exact identity, no moonshot gain

**Outcome:** TYPED_JOINT_REDUCTION_EXACT_ALL_POWERS_OF_TWO; the tested
Karatsuba family has a paid child saving over independent binary splitting,
but gives no improvement to the fork's current kappa witness and is not
a new multiplication theory.

## Evidence

| Claim | State | Evidence |
|---|---|---|
| Length-four convolution identity over Z | **PASS** | Exact symbolic expansion and all 16 bilinear basis-pair checks |
| Parameterized identity for n=2^k | **PROVED** | Induction using p1-p0-p2=a0b1+a1b0 |
| Incorrect middle decoder | **REJECTED** | a=b=x^2 returns x^2+x^4 if -p2 is omitted |
| Child count and coefficient growth | **PROVED** | Three width-n/2 convolution calls; child sums add at most one bit per level |
| Clean workspace and fixed-tape charge | **PROVED for this schedule** | Fresh contiguous frames, sequential calls, paid copies, zeroing, clearing and stack movement |
| Exact binary-integer recovery | **PROVED** | Integer convolution coefficients followed by ordinary base-two carries |
| Improvement over four independent children | **PASS** | Recurrence exponent falls from 2 to log_2(3) |
| Improvement over current integer multiplication bound | **FAILED** | n^(log_2(3)) polylog n is asymptotically larger than n log^(1-kappa) n |
| Transfer into the original Section 4 recurrence or a kappa theorem | **NOT ESTABLISHED** | Child types and cost units do not match |
| Full repository verification or large certificate replay | **NOT RUN** | Excluded by the bounded first checkpoint |

The deterministic command is:

    python3 research/joint-recursion-reduction/check_pilot.py

Its exact result is recorded in receipt.json. No random products are used.

## Mathematical conclusion

The leading hypothesis survives only in its algebraic form: the cross term
can be generated from one summed-input child, reducing four independent
block convolutions to three. This is precisely the known Karatsuba
decomposition. Its honest paid recurrence improves on schoolbook block
splitting but remains far above the current near-linear-in-n integer
bound. It therefore does not satisfy the Issue's moonshot objective.

The alternative modular transform has a clear exact map, but its central
idea overlaps the pinned manuscript's synthetic transforms and it supplies
no new charged recursion. A genuinely useful next result must combine a
larger reduction in child work with a structured encoder/decoder whose
integer height, tape movement, and cleanup remain paid. The variable-arity
cost gate in COST.md is the first falsifiable target. No exponent is
projected for it.

## Attribution and scope

The original manuscript is credited to OpenAI at its fixed source commit.
This research folder and checker were prepared with substantial OpenAI
Codex assistance. The checker is a local exact implementation of the
displayed formula, not independent human review or a formal proof. No source
code, certificate, or physical circuit from prior research was imported.
