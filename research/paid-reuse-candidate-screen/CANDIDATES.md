# Candidate screen

FAST ranked real graph-multiple values by distinct physical demand, baseline copy count, ordered frame compatibility, candidate carry edges, and current other-role span hits. A compiler carry edge is only an optimistic opportunity: its source frame is contained in the target frame and its input row is independent of that block's output basis. The edge may still displace another match or change later role and endpoint costs.

## Candidate families

| Family | Values | Physical pattern | Disposition |
|---|---|---|---|
| Broad carry-edge leaders | 62984, 62985, 62986 | Six graph uses, six external demands, five baseline copy XORs; two unmatched target uses per value have legal candidate carry edges | Focus 62985: two forced edges save five physical XORs, but add two roles and 46 rank mass |
| Copy-heavy reconstruction leaders | 21, 460, 819 | Twelve graph uses and physical demands, nine baseline duplicate-copy XORs each; no candidate carry edges | Focus value 21: none of its twelve demand points has an eligible other-role span hit |
| Complete serial-path leaders | 2525, 2696, 2876 | Two demands each, one baseline copy, rank-18→19→20 chain with exact rank-1 edges | Lower copy ceiling; not promoted after the stronger families were measured |

The all-demand span scan covers all 15,102 graph-multiple values with at least two physical demands and all 79,075 external demand points. It finds 1,080 span hits across 786 values. A span hit is a clean fresh-form relation over roles that are currently frame- and future-use-eligible; it is not itself an arbitrary-dirty physical schedule.

Value 62985 is the best measured case: it has six of six span hits and two distinct legal carry targets. Value 21 is the strongest baseline copy-count case but has no carry edge and no span hit. The local carry choices for 62985 were both forced together, and its current eligible retired roles contain no one-, two-, or three-carrier reconstruction witness at any of its six uses. The local hold/reconstruction search stops here.

## Focused carry case: value 62985

Value 62985 is produced in group 51779 and has six actual compiler demands in groups 51855, 51875, 52185, 52186, 52187, and 52188. Its baseline has five producer duplicate-use copy XORs. Four compiler candidate edges cover two unmatched uses:

- group 52185 or 52186 → group 51875, use 111481;
- group 52187 or 52188 → group 51855, use 111432.

The FOCUSED alternative selects 52185→51875 and 52187→51855. Each is an exact Q23 rank-1 transition. The two target uses become matched through the existing value carriers. The other four candidate uses remain separate demands, with their own observed slots and frame events in `FOCUSED_RECEIPT_62985.json`.

The current other-role fresh-form span hits all six demands. The recorded Gaussian witnesses use 5, 6, 5, 5, 5, and 10 role forms. An exact subset search over the currently eligible retired roles finds no one-, two-, or three-carrier witness at any of the six points. This rules out the direct small-carrier PR 74 primitive on the current retired-role pool; it does not rule out a different schedule that first changes role availability.

## Focused reconstruction control: value 21

Value 21 has 12 graph occurrences, 12 separate external compiler demands, and nine baseline duplicate-use copies. It has no complete serial carrier path and no compiler candidate carry edge for an unmatched use.

At all twelve actual demand points, the other currently frame- and future-use-eligible role forms do not span the value. The highest baseline copy count therefore does not provide a PR 74-style reconstruction witness in this fixed h=23 schedule.

## PR 74 comparison boundary

The comparator is the deferred-span reconstruction method pinned to PR 74 commit `23468ac3867e778f54835ab66eb513934965160b`, with its selected verifier pinned to `2eecf5f8e4eafb3dd13dbc70b9ecc5b4e6e9a77c`. Its h=25 word uses 144 migrations: 121 two-carrier and 23 three-carrier reconstructions. The method reserves retired roles to a deadline, clears the old role, and reconstructs by literal XORs. It charges clearing, carrier frame raises, reconstruction XORs, role occupation, cleanup, and endpoints.

Those h=25 costs are not transferred to the PR 63 h=23 word. No PR 74 migration was compiled here. The full-word carry alternatives and the all-demand screens above are enough to stop this local search; they do not disprove every possible schedule with newly reserved roles.
