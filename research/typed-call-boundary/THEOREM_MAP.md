# Original theorem map: one real recursive call

## Scope and finding

The original multiplication theorem is Theorem `thm:main` in
`upstream/build/sections/00-introduction.tex`. Its proof uses two distinct
recursive array procedures: radix-address chunk interchange in Section 4 and
the numerical butterfly layer in Section 5. This checkpoint selects one
recursive call in the Section 4 chunk-interchange construction. This is a
recursive *address-permutation subroutine used by multiplication*, not a
recursive call that multiplies two smaller integer operands.

That call has a source-defined function, shape, decreasing parameter, role
stream, frame context, and paid volume. The theorem does not expose an
independent mutable state object that can be retained between sibling calls.
In particular, the source does not identify the Issue 13 `FSa` carrier as the
payload or frame of one of these calls.

## Source-to-recursion map

| Source | What it proves | Call-level meaning |
|---|---|---|
| `00-introduction.tex`, Theorem `thm:main` and “The two tape operations” | One fixed finite-alphabet, fixed-tape machine multiplies every pair of `n`-bit integers. The first tape procedure swaps address chunks at cost `O(V u^tau)`; the second applies a numerical layer at cost `O(V d^lambda')`. | A top-level multiplication theorem and two subroutine bounds; neither statement alone labels individual network edges as calls. |
| `02-streams.tex`, Lemma `lem:elementary-streams` and the array-order definitions | Arrays are bit streams over complete Cartesian address sets. `V` counts logical data bits. Shape lengths use canonical binary descriptors. Splits, aligned pointwise maps, merges, and cleanup have `O(V)` fixed-tape implementations. | The executable stream representation and base digit interchange used by the recursive boundary. |
| `03-motifs.tex`, Proposition `prop:bit-motif-interface`, equations `eq:bit-wire-count` and `eq:rank-budget-labels` | The bit network has `W_b = 177176569091445000000` roles, pointwise XOR gates, an endpoint role permutation, and assigned `m x m` rational matrices. Its edge-rank sum is `s_b = 177176569088785861287000000 < W_b m`, with `m = 1000000`. | A fixed finite network. Its edge matrices are data for the Section 4 recursion; `W_b` is the role count, not a child width. |
| `04-swap.tex`, Lemmas `lem:matrix-shear` and `lem:lower-lower`; Proposition `prop:power-interchange`; equation `eq:swap-recurrence` | For an edge matrix `A_e`, a fixed factorization `A_e = E_1 Pi E_2` has exactly `rank_Q(A_e)` pivots. Each pivot is implemented by one recursive interchange of a pair of `b=e/m` digit fields on one role stream. Across the network there are exactly `s_b` such calls per parent invocation. | This is the selected actual recursive call. For `e=m^k`, its child has width `m^(k-1)`, one of the `W_b` disjoint row classes, and volume `V/W_b`. The recurrence is `F_0=O(1)`, `F_k <= (s_b/W_b)F_(k-1)+O(1)`. The fixed-tape depth-first schedule parks and restores inactive streams and descriptors. |
| `04-swap.tex`, Lemma `lem:chunk-swap` | Removes the power-width and row-divisibility restrictions and gives the arbitrary-width `O(V u^tau)` address interchange. | This is the surrounding procedure used by the multiplication proof; its arbitrary-width padding is not an extra child type of the power-width recurrence. |
| `05-layers.tex`, Proposition `prop:simultaneous-layer` | A separate numerical recursion applies `C^(tensor e)`. Its phase-frame residual bases give `s_c` child calls on `e/m` selected axes, each on volume `V/W_c`; it has record, precision, padding, and truncation conditions. | A real recursive family too, but with a different logical function and payload. It must not be substituted for the Section 4 bit-array interchange call. |
| Issue 13 frozen result, fork commit `26ff3802cfa1b4b6ee081703509c394fa71526a0` | The pinned pair-assembly compiler and profile give aggregate frame, role, rank, and width records. At `m=575`, width `529` has multiplicity `64,211,400` in a profile with `W=137,151,806` and total rank `78,860,441,550`. | The histogram entry has no child function, call identifier, payload, or call-boundary frame. It is not one of the individually named Section 4 pivot calls. |

## Four counts that must stay separate

1. **XOR DAG operations.** Nodes such as `FSa = F XOR Sa` and
   `Y2 = FSa XOR Sb2` are pointwise logical operations in a finite producer.
   A node name does not imply a recursive invocation.
2. **Physical frame transitions.** The rank-pair compiler records selected
   carriers, acquired roles, copies, and paid XOR transitions for its compiled
   whole graph. These are physical transition and cost records.
3. **Section 4 recursive calls.** For a fixed theorem network and edge `e`,
   each pivot in the chosen rank factorization causes one actual call to the
   smaller chunk-interchange routine. The rank sum `s_b` counts these calls;
   row splitting gives each call exactly `V/W_b` logical volume.
4. **Issue 13 profile rows.** `n_t` and `W` in the stored moment are
   aggregate width multiplicities and their profile normalization; total
   rank and whole-graph transitions are separate aggregate records. For
   example, the width-529 multiplicity is not a set of 64,211,400 typed,
   separately addressable semantic calls. Its moment contribution is an
   analytic profile term.

The symbols `W_b`, `s_b`, and `m` in the original theorem describe role count,
recursive-call count, and the fixed matrix dimension. Issue 13's `W=137,151,806`,
`n_529`, and `m=575` belong to a different pinned physical profile. Reusing
those symbols as though they were the theorem's call objects would invent a
mapping absent from the source.

## Exact quantification of the selected call

Fix the bit network, its matrices, the admissible radix `q`, and rational
`tau` with `s_b/W_b < m^tau`. For every `k >= 0`, put `e=m^k`. For every
complete bit array with a row field of length divisible by `W_b^k`, two
disjoint `q^e` address chunks, and any finite spectator fields, the fixed
procedure returns the exact array with those chunks interchanged. It
preserves every spectator field, acts on arbitrary array contents, and uses
`O(V e^tau)` time on a fixed finite number of finite-alphabet tapes.

At an internal node (`k>0`), each parent chunk is split into `m` fields of
`b=e/m` radix-`q` digits. For each network edge and each pivot of its rational
rank factorization, the procedure calls the same interchange routine on one
pair of those `b`-digit fields in one role stream. The parent row index is
written `r=W_b g+(w-1)`. The child receives the complete row class `w`, so
its row length is divided by `W_b` and remains divisible by
`W_b^(k-1)`. These are genuine recursive calls with a common stateless array
interface; they are not reconstructed from a later histogram.

The theorem therefore supports a typed boundary for a `Swap_k` call. It does
not support a bridge from the Issue 13 `FSa` value to one selected call in
that network or in the rank-pair compiler. That bridge needs a source-pinned
mapping from a particular producer value and compiler transition to a
particular theorem edge, pivot, role stream, and child payload.
