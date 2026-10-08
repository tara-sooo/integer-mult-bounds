# Physical event and cost ledger

## Exact logical-to-physical join

Selected occurrence: `(h=23, producer=2039, consumer=2044, operand=0)`. The canonical word hash scopes every `ops[]` and `events[]` identity.

| Stage | Actual identity | What it establishes | Exact `Q^23` event ranks |
|---|---|---|---|
| Build `FSa` | Group 1908, inputs `[1958,1959,1975,1996]`, coefficient `0b1111` | Producer value slot 17581; producer/use/consumer input slot is the same | Input raises 166275–166278: `2,4,6,4` |
| Producer XOR cone | `ops[55648]=(17581,160,1908)`, `ops[55650]=(733,740,1908)`, `ops[55655]=(17581,733,1908)` | The three exact XORs whose output cone yields `FSa` in slot 17581 | Their six raise events 166279–166280, 166283–166284, 166293–166294 are same-frame, rank `0` |
| Carry into consumer | `events[226456]=(17581,1908,1929)` | Exact `FSa` use slot entering the `Y2` block; the occurrence is unmatched by `match()` | `4` |
| Other `Y2` input | `events[226455]=(1078,1920,1929)` | Slot 1078 carries input `2020`, the other term of `Y2` | `4` |
| Materialize `Y2` | `ops[75970]=(17581,1078,1929)` | Slot 17581 changes from `FSa` to `2020 XOR 2039` | `events[226459:226461]`, both rank `0` |
| Produce block output | `ops[75971]=(21455,1078,1929)` | Together with the surrounding basis transform, slot 21455 becomes `Y2048 = 1952 XOR 2020 XOR 2039` | `events[226461:226463]`, both rank `0` |
| Consume/restore temporary | `ops[75972]=(17581,21455,1929)` | Slot 17581 changes from `Y2` to `1952`; block exit expresses `Y2 = slot 21455 XOR slot 17581` | `events[226463:226465]`, both rank `0` |

The notation `events[a:b]` above means the listed half-open index interval, not an inferred range of extra events. All IDs are present in the saved word and the JSON trace stores their exact tuples.

The producer frame is `(core=1, cover=8127427)`, group 1908, rank 10. The consumer frame is `(core=1, cover=8142787)`, group 1929, rank 14. The carrier raise from 1908 to 1929 has exact rational rank 4. This coincides numerically with the old source-local rank for `FSa -> Y2`, but it was independently recomputed from these actual old/new projectors.

## Copies, clearing, and roles

The block's complete operations are captured, including work outside the selected linear cone. `ops[75969]` and `ops[75971]` participate in the joint basis transform. After `Y2` is restored, `ops[75973]=(22506,21455,1929)`, `ops[75974]=(22507,21455,1929)`, and `ops[75975]=(22508,21455,1929)` perform three `duplicate_use_copy` operations for other outgoing uses of `Y2048`. Each follows a slot-allocation event with no prior frame, then same-frame raises of rank 0. They are not assigned to `FSa -> Y2`.

No `retired_slot_clear` XOR occurs in the captured producer or consumer group. The full compiler still has 1,612 clearing XORs across h=23; those aggregate operations do not identify a cost for this use. Slot 17581's final linear form is marked retired, so the exit identity `Y2 = Y2048 XOR 1952` is a virtual relation requiring generation/retention work if it is used again. The explicit restoring XOR at `ops[75972]` is included in the selected cone.

## Rank summary and attribution boundary

The exact producer-input support raises contribute `2+4+6+4=16`. The two consumer inputs used by `Y2` contribute `4+4=8`; the identified same-frame XOR raises contribute `0`. The gross support-cone rank sum is therefore 24. Every known event rank lifts to the same per-h25-triple-context rank in `Q^575` under the inherited rank-one factor.

The sum is not a logical-use price. Several physical basis operations jointly produce outputs and carry roles. The other input `1952` also participates in producing `Y2048` (its consumer input event has rank 6), while the three output copies serve other compiler uses. The trace keeps those events and XORs visible without assigning their full cost to `FSa -> Y2`.

The compiler word does not encode forward/reverse orientation in an array entry. Full expanded-word replay was not run. Exact physical pivot coordinates and a Section 4 `Swap` child remain unresolved. No selected-child cost or new `κ` follows from this local event ledger.
