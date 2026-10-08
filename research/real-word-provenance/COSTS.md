# Selected-use cost ledger

## What this run establishes

The h=23 compilation returned and its whole-axis receipt assertions matched the pinned PR 63 receipt: roles, rank mass, elementary XOR count, statistics, and rank histogram. The compiler log reported 37,025 matched uses and 52,473 regions. These are whole-axis aggregates, not charges for `FSa(2039) -> Y2(2044)`.

The compiler generated a canonical physical word in memory, but trace post-processing failed before comparing its hash with the pinned word. The actual digest values and the compiler peak RSS were not retained. `TRACE.json` records this boundary.

## Selected occurrence

| Item | Result |
|---|---|
| Logical occurrence | `(h=23, producer=2039, consumer=2044, operand=0)` |
| Selected carrier slot | `UNRESOLVED` |
| Consumer input slot | `UNRESOLVED` |
| Standalone `Y2` value slot | Captured as absent (`None`) in the failed trace pass |
| Related `ops[]` indices and causes | `UNRESOLVED` |
| Related `events[]` indices and frame transitions | `UNRESOLVED` |
| Exact selected physical frame-edge rank | `UNRESOLVED` |
| Orientation-specific execution | `NOT RUN` |
| Generated-word match to pinned SHA-256 | `NOT VERIFIED` |

Issue 18's local logical rank for `FSa -> Y2` is not an emitted-operation charge. Issue 17's rank-one product context can lift a known h=23 frame edge per h=25 triple context, but this run retained no selected physical frame event to which that rank could be attached. No cost is imputed to the missing slot or to any unrelated group operation.

The instrumentation self-check uses a fixture only; its ranks are not production costs. No one-to-one relationship between logical XORs and physical XOR instructions is assumed.
