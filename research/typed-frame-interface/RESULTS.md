# First bounded result

**Outcome: `MISSING_TYPED_INTERFACE`.** The pinned construction contains a
legal-looking scalar carrier inside its finite bit-network DAG, but its
physical profile does not connect that value to a typed recursive child. The
requested physical cooperative-recursion comparison cannot be made from the
available source data.

## Bounded attempt

The sole child family examined is width `t=529`, with multiplicity
`64,211,400` in the pinned `m=575` profile. The sole sharing candidate is
`FSa = F⊕Sa`, consumed by `Y2 = FSa⊕Sb2` in the pair producer. For this local
GF(2) transformation, the boundary map `(x,z) ↦ (x,x⊕z)` is self-inverse;
an unrelated dirty bit is unchanged. Omitting `x` and treating the child as
if it received only `(Sa,Sb2)` is an invalid free conversion: it changes the
result whenever `F=1`.

The small checker below verifies that local truth table, the recorded
width-529 row, and the pinned whole-graph frame-inclusion, dirty-basis, role,
and XOR totals. It also checks the exact moment signs: the stored
accepted-savings certificate has positive strict gap, and the next-grid
lower bound is greater than one. It does not regenerate the profile or run a
physical replay, and cannot map the selected carrier to a typed call.

```sh
python3 research/typed-frame-interface/check_boundary.py
```

The checker reads the immutable source commit with `git show`; that commit
must already exist in the local object database. It performs no fetch.

Recorded result:

```text
PASS: source-derived GF(2) carrier/inverse, dirty spectator, and pinned whole-graph frame records
m=575 W=137151806 n_529=64211400; accepted moment gap > 0; next-grid lower bound > 1
This checks only the local scalar map and recorded certificate, not a typed recursive call.
```

## Physical comparison and controls

The pinned frame compiler certifies all frame inclusions, full input and
arbitrary dirty basis behavior in both orientations, and counts carrier
copies as XOR operations. Its match table has unique uses; a reused value
needs a separate acquired role and paid XOR. Those checks apply to the
compiled whole graph. The serialized record does not identify whether this
particular local carrier is selected, and it has no typed child boundary on
which to charge creation, transfer, erasure, or a conversion.

Consequently this bounded attempt cannot produce a legal multi-type row or
SCC comparison. A free conversion, duplicated child ownership, uncharged
fan-out, or omitted restoration would not be an admissible extension of the
existing compiler contract. There is no source-backed state conversion to
instantiate as a recursive negative-control test, so the check stops at the
missing interface instead of assigning favorable matrix entries.

The existing scalar certificate accepts `a_b=5103018/10^11` and excludes
`5103019/10^11` for its full child multiset. The carrier above has not been
shown to alter that multiset or the dominant scalar recurrence. No new
spectral-radius gain, conditional `κ` claim, or multiplication improvement
follows.

Validation tiers: **FAST PASS** (the focused exact checker); **FOCUSED NOT
RUN** (no typed candidate to replay); **FULL NOT RUN**. No large CRT
regeneration, physical-word replay, or `make verify` was run.

## Status and next gate

The first milestone is complete as a scoped obstruction. To reopen it, the
real producer/compiler must expose one recursive call boundary that ties a
logical parent and child function to the child payload and width, the
source/return frames and basis, arbitrary dirty-state pre/postconditions,
unique physical ownership, and all state and transition costs. This audit
does not regenerate CRT profiles, replay the large physical word, or test
another family.

Prepared with OpenAI Codex assistance. The inherited construction remains
attributed in `SOURCES.md`; no upstream code was copied into this checkpoint.
