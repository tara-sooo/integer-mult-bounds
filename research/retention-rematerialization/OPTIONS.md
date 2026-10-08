# Physical options

The comparison uses the pinned PR 63 h=23 circuit at the exact Issue 19 commit. `Y2(2044)` is excluded from reuse pricing because its only use is within its producing block. The fallback `Y2048` comparison is limited to its four traced child demands.

| Option | Physical result | Cost conclusion |
|---|---|---|
| Existing circuit | Group 1929 creates four distinct outgoing roles for the four child uses. It performs three `duplicate_use_copy` XORs after the output-basis operations. | Measured baseline; details and endpoint charges are in [COST_LEDGER.md](COST_LEDGER.md). |
| Retain one carrier | No legal serial schedule: the four equal-rank child frames are pairwise incomparable. A single physical role cannot occupy all four child frames or be advanced from one child to another. Keeping separate carriers is the existing four-role baseline. | No alternative retention saving is demonstrated. Do not treat four rank-2 frame edges or role endpoints as one free transition. |
| Rematerialize at each use | `Y2048` is independent of the other local inputs in each child. At each target, the complete checked set of other frame-compatible roles, including retired roles and live future-compatible roles, has `Y2048` outside its rational span. | No admissible reconstruction schedule was found in the tested physical state. Its cost is unavailable, not zero. Any future candidate must exhibit its source roles, physical XORs, actual frame edges, and cleanup/terminal endpoints. |

The FAST span screens contain 82, 79, 79, and 78 compatible other roles at groups 1954, 1974, 2066, and 2086, respectively. The respective span ranks equal those counts; `Y2048` is outside every span. This is stronger than a retired-only screen, but remains a screen of the frozen word's actual available roles, not an exhaustive search over alternate compiler schedules.

The deferred-span carrier-reconstruction idea from [PR 74](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/74) informed the checks: a candidate must use real available controls, reserve a valid destination frame, reach the next use, and pay its clear/restore endpoint. PR 74 is a different circuit; none of its numeric results or schedules is transferred here. The negative control rejects the withdrawn [PR 96](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/96) shortcut of merging separate physical transitions: the three proposed merged edges have no matching event or shared target frame.

## Outcome

There is no proven local saving for this traced case. The exact baseline is established; single-carrier retention is inadmissible for the four child frames; and the tested rematerialization sources do not span the value. These results do not rule out a different global schedule or prove recursive child sharing.
