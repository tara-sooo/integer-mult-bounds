# Results

## Primary status

**`PROFILE_ONLY_NO_TYPED_CHAIN`**

### Checkpoint decision

**NO-GO on a coalescence claim at this checkpoint; mathematical feasibility is unclassified.** The fixed PR193 generator reproduces its complex input and the source-width aggregate, but does not export a per-port path tying the three widths to one chronological role. No guessed path, gate collision, or impossibility theorem is substituted for that missing record.

### Proved and checked

- The PR193 producer was replayed from its pinned commit. It regenerated the local graph and matched its pinned certificate with exit status 0.
- The generated `h=22`, `v=1320` graph reports the source histogram `1:1320, 2:1320, 18:1320` and target histogram `1:3960, 18:1320`.
- The PR193 certificate and PR203 input give the complete old complex child histogram, `W=12052`, rank mass `794112`, deficit `1320`, and maximum rank `20`.
- A focused accounting pass checked the pinned child-rank total, data submultiset, and moment evaluation at 50-digit decimal precision; the moment formula and histogram are recorded in [PAID_DELTA.md](PAID_DELTA.md).
- The source edge, role, frame, gate, consumer, and full-payload mapping needed to test a replacement is absent from these records.

### Not proved

No endpoint matrix difference or rank-21 equality, gate common-frame compatibility, source-control legality, sign identity, arbitrary dirty-state restoration, compensator ledger, new all-role cost, or mathematical obstruction was established. No bit-side, copied-center redesign, recursive-cost, or κ claim follows.

### Verification scope

- **FAST:** pinned input and code path audit performed.
- **FOCUSED:** deterministic `scripts/paired_cube_producer.py` replay performed; it regenerated and matched the pinned local complex certificate.
- **FULL:** not run. No full Section 4 rank-one pivot replay, router replay, complete supplier rebuild, bit supplier, center-copy redesign, or recursive proof was attempted.

No separate exact checker or `receipt.json` was added: the focused producer validates the pinned local graph, while no typed source path exists for a checker to certify. The next smallest mathematical task is to export the per-port event record listed in [SOURCE_CHAIN.md](SOURCE_CHAIN.md), then test one path's endpoint rank and first intermediate gate.
