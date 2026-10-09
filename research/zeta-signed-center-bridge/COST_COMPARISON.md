# Cost comparison with the PR144 coordinate-star

## Same center map

PR144’s selected star source is S_i=∑_{S∋i}x_S, with

\[
(Bx)_T=\frac12\sum_{i\in T}S_i-\frac16\sum_iS_i.
\]

Every triple occurs in exactly three stars, so ∑_i S_i=3X. Since Z_i=X−S_i,

\[
X-\frac12\sum_{i\in T}Z_i
=\frac12\sum_{i\in T}S_i-\frac12X
=\frac12\sum_{i\in T}S_i-\frac16\sum_iS_i.
\]

Thus the proposed decoder is the existing B scatter in complementary coordinates. It removes no B work, K/H operation, or recursive child.

There is an even more direct source comparison. The pinned PR144 scripts/paired_cube/graph.py has an unselected center_kind="disjoint" branch. Its center_scatter is ∑_i E_i/(h−3)−(1/2)∑_{i∈T}E_i, and center_channels() constructs those complementary E_i. Because ∑_i Z_i=(h−3)X, this is the same candidate after substituting X=∑_i Z_i/(h−3). PR144’s selected profile uses center_kind="star"; the new zeta factorization is not a new center identity.

For P_4, the eight selected star supports have rank 6 each, totaling 48 and matching the source ℓ=h(h−2) copied-center charge. The eight literal complement supports have rank 7 each, totaling 56; the full X support has rank 8. The 56+8 versus 48 comparison is an address-span diagnostic, not a certified physical charge.

## Explicit ledger

| Item | Known bounded count | Still required for a paid comparison |
|---|---:|---|
| P_4 input ports | 32 | Source/target frame mapping for E |
| Direct X from 32 independent inputs | At least 31 additions; X is used by 32 outputs | Carry, retention, dirty pre-read/inverse, fanout, terminal ranks |
| Each Z_i | 20 P_4 inputs; 12 decoder uses | Root role/frame, broadcast, endpoint corrections |
| C_B decoder | 32 output rows; 96 singleton-root uses | Signed decoder, output copies, half phases, cleanup |
| Shared arithmetic schedule | 8 half-scalings + 96 additions | Copies and movement are not included |
| PR144 star centers | 8 forms; rank 6 each; ℓ=48 | Existing copied-center transitions stay charged |
| Literal complement centers plus direct X | Rank 7 each plus rank 8 for X | No physical schedule; 64 is not a claimed ℓ |
| Full pinned h=8 zeta graph | 254 inputs, 1,008 accumulator nodes, 1,262 roles; 2,016 forward and 2,016 inverse updates | P_4 placement, zero contributions, routing, readout, endpoint maps |
| Dirty old-value reads | 11,846 terms for all roots; 2,024 for singleton roots alone | No pruning of the pinned word is credited |

The 222 zero data contributions are 198 nontriple masks plus 24 triple masks outside P_4. Each singleton root sees 127 possible input slots, of which 20 carry P_4 data and 107 contribute zero. The full word retains all roots and their dirty reads.

The PR172 README’s addition formula gives 769 at h=8, while executable zeta.py appends 1,008 accumulator nodes and reports R=1,262; word.py expands them to 2,016 forward updates. The receipt records all three quantities separately.

## Where X could come from

1. A direct tree over 32 independent x_S values needs at least 31 additions; retaining and distributing X also needs a carrying role and 32 output uses.
2. If the eight S_i roots are already retained, X=(∑_i S_i)/3 reuses the star computation and its denominator-three grid. That is the original coordinate-star work, not a zeta saving.
3. The four P_4 cube totals F_I in the existing H producer sum to X, so three more additions are an arithmetic option. The source does not certify their joint retention, frame reconciliation, dirty restoration, or 32-way delivery as a P_4 center.
4. From the complement roots, X=(∑_i Z_i)/5. This is valid over ℚ but not over ℤ[i,1/2]. In a q-adic ring it needs q≠5 and an explicit prime/denominator contract.

No net saving is established. The candidate has no complete cost, profile, or κ.
