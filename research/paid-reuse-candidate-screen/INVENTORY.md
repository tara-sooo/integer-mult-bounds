# PR 63 h=23 paid reuse inventory

This inventory is built from the frozen PR 63 h=23 graph and canonical word. It addresses [Issue #21](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/21), after reading the [Issue #20 result](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/20) at commit `e2cf064a7976566e8a9e60719c16f0c7d12160d9`.

## What counts as a use

The pinned graph has 64,065 active nodes, 124,588 graph operand occurrences, and 58,729 values with outgoing graph uses. The compiler groups nodes by their PR 63 frame. It coalesces repeated graph operands that enter the same block into one external input demand, while terminal outputs are separate endpoint demands.

The frozen compiler reports 118,332 use points. Each inventory row keeps graph uses and compiler demands separate:

- `g` records `[consumer node, operand index, consumer block, same-block flag]`. A graph occurrence inside the producer block is not an external physical demand.
- `u` records each compiler use ID, consumer block, matching status, observed carrier slot, block-input event, source frame group, and exact Q23 edge rank. A terminal row records its output endpoint instead.
- `s` records slots observed at those demands. A graph count is not a count of separately charged copies.
- `r` and `t` record direct source-frame compatibility, the full ordered single-carrier path screen, and each tested transition.
- `z` records graph-use coalescing, external demand groups, distinct carrier slots, matched and unmatched compiler demands, and the baseline duplicate-use copy count.

The compact row format is defined in `inventory.json`. Event IDs and slot IDs refer to the canonical PR 63 word with SHA-256 `640696dd7cd893add9d6e12d0d587956fecf113b2eff8c29547b82e5a6f3c0ad`.

## FAST counts

| Screen | Values |
|---|---:|
| Values with at least two graph operand occurrences | 16,137 |
| Graph-multiple values with at least two physical demands | 15,102 |
| Graph-multiple values coalesced to one physical demand | 1,035 |
| Multiple external-group values without a complete serial frame path | 10,636 |
| Multiple external-group values with a complete serial frame path | 4,466 |
| Serial multi-group values with any baseline duplicate-use copy opportunity | 220 |
| Multi-demand values with at least one current other-role span hit | 786 |
| Demand points with a current other-role span hit | 1,080 of 79,075 |

Across the last 220 values, the maximum baseline duplicate-copy opportunity is one XOR. This is only a copy-count bound: it does not subtract matching exchanges, role creation or occupation, clearing, later reuse, or endpoints.

The overall pinned word has 149,172 physical XORs, 27,918 roles, 444,594 frame events, and a complete event-plus-endpoint rank mass of 642,620.

## Controls

`Y2(2044)` has one graph occurrence, inside group 1929, and no external compiler demand. It has no reuse tradeoff.

`Y2048` has four graph occurrences in four external groups and four physical demands: use IDs 522, 571, 801, and 851. They occupy four slots and four separate rank-2 events; three producer duplicate-copy XORs are present. The producer frame is compatible with each destination separately, but the destination frames are pairwise incomparable, so one carrier cannot serve the four demands in sequence.

## Reproducible files

- `FAST_RECEIPT.json` contains source pins, complete counts, candidate rankings, and the two controls.
- `inventory.json` contains every graph-multiple logical value and its observed physical demands.
- `REGENERATION_FAST_RECEIPT.json` and `regeneration_availability.json` contain the all-demand fresh-form span screen. It covers 15,102 values at 79,075 physical demand points; a hit is not a paid arbitrary-dirty schedule.
- `FOCUSED_RECEIPT_62984.json` and `FOCUSED_RECEIPT_62985.json` contain full-word forced-carry comparisons. `REGENERATION_RECEIPT_21.json` and `REGENERATION_RECEIPT_62985.json` contain focused span witnesses, including the PR 74 one-to-three-retired-carrier screen for value 62985.
