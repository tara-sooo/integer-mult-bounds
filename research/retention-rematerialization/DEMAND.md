# Demand audit

## Pinned scope

This audit starts from the verified [Issue 19 result](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/eaa21e97209357575ef462d189c0950b6da85e7c), using its PR 63 graph and exact h=23 physical word. The graph/compiler/word pins and hashes are in [SOURCES.md](SOURCES.md).

## `Y2(2044)` has no reuse demand

In the frozen PR 63 graph, `Y2(2044)` has exactly one child: `2048`, operand 1, in consumer group 1929. It has no cross-group child and no terminal use. The compiler does not allocate a separate value slot for 2044; the Issue 19 trace shows it as a temporary linear form inside group 1929 and as a virtual relation at that block's exit. Therefore there is no later use for which keeping `Y2` could replace regeneration. A retention saving for `Y2` would be hypothetical.

## Fallback: actual `Y2048` demands

`Y2048` has four graph uses in four distinct child groups:

| Child | Operand | Group | Compiler use | Physical carrier | Frame rank |
|---:|---:|---:|---:|---:|---:|
| 2349 | 0 | 1954 | 522 | 21455 | 16 |
| 2350 | 0 | 1974 | 571 | 22506 | 16 |
| 2351 | 0 | 2066 | 801 | 22507 | 16 |
| 2352 | 0 | 2086 | 851 | 22508 | 16 |

The value is produced in group 1929 (frame rank 14). Each actual carrier crosses a separate rank-2 edge from group 1929 to its child. The four child frames have equal rank and are pairwise incomparable, so no one carrier can be advanced through all four destinations. The observed peak is four simultaneously live `Y2048` roles.

FAST also checks direct reconstruction from each child's other inputs and checks the span of all other currently available roles whose frames are compatible with that child. Direct reconstruction fails in all four children. The compatible-role pools and ranks are recorded in [FAST_RECEIPT.json](FAST_RECEIPT.json) and [FOCUSED_RECEIPT.json](FOCUSED_RECEIPT.json); none spans `Y2048`.

This fallback gives a bounded, real-use comparison. It does not establish sharing between recursive child problems or a change to `κ`.
