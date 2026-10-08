# Literal rational rank and paid-transition ledger

**Status: PROVED_BY_PINNED_SOURCE; FAST arithmetic check passed.**
The current total is tied to the rank-first word, its frame-group labels,
the exact envelope-projector family, and the inherited 575-dimensional
profile constructor. It is not inferred from the numerical deficit alone.

## The Section 4 quantity

For each physical wire segment e, the required edge matrix is

\[
A_e=M_head(e)-M_tail(e),\qquad
s=\sum_e \operatorname{rank}_{\mathbb Q}(A_e).
\]

The rank-first compiler's elementary operation has a physical target slot,
control slot and frame-group id g. Before XOR, both slots are raised to the
same group frame. Each raise records the old and new frame; reclamation
uses literal XORs at the requested frame and clears the retired slot before
reuse. Therefore clears and frame raises are charged transitions, not free
bookkeeping.

For nested source-defined envelopes E_old subset E_new, their rational
orthogonal projectors satisfy

\[
\operatorname{rank}_{\mathbb Q}(P_new-P_old)
=\dim E_new-\dim E_old.
\]

The compiler's rank difference is exactly this dimension difference. The
pair-assembly audit checks exact rational projectors and containment; the
rank-pair receipt pins the word and its frame groups; the rank-pair screen
reconstructs transitions from the serialized word. A fixed rational
similarity and the 575-dimensional product construction preserve these
ranks. Data-corner and exterior classes use the inherited simultaneous
basis and exact corner certificates.

## Current PR #63 totals

| Quantity | Exact value |
|---|---:|
| m | 575 |
| N = binom(25,3) binom(23,3) | 4,073,300 |
| R23 | 27,918 |
| R25 | 36,586 |
| B23 = binom(25,3) R23 | 64,211,400 |
| B25 = binom(23,3) R25 | 64,793,806 |
| W = 2N+B23+B25 | 137,151,806 |
| L = binom(25,3)·23·22 + binom(23,3)·25·24 | 2,226,400 |
| Wm | 78,862,288,450 |
| s = Wm-N+L | 78,860,441,550 |
| Wm-s = N-L | 1,846,900 |
| Maximum child width | 529 < 575 |

The per-axis compiler masses are also pinned:

\[
s_{23}=23R_{23}+23\cdot22=642,620,\qquad
s_{25}=25R_{25}+25\cdot24=915,250.
\]

The rank-first dirty replays record 1,612 clearing XORs at h=23 and 2,092
at h=25. Their frame raises are reconstructed from the actual words. The
full rank-pair profile then separates internal h=23/h=25 profiles, the
23/529 and 25/525 auxiliary exteriors, data macros of widths
9 singletons + 21 + 17 + 481, the h-axis data growths, and N distinct
rank-one endpoint-copy calls. The copied-center transforms remain charged
in the internal profiles; the endpoint-copy calls are separate.

The rank-pair screen asserts that the weighted multiplicity profile equals
Wm-N+L and pins the full child multiplicities. This is a proof chain for
the literal Section 4 sum: actual word -> frame transitions -> rational
projector differences -> exact per-class ranks -> s.

## Rejected shortcuts

- Equality Wm-s=N-L is not by itself a proof that the edge matrices have
  that rank sum. The transition-to-projector and profile-class links above
  are required.
- The GF(2) rank of a pointwise XOR shear is not an address-edge rank.
  Issue 16's selected local example has GF(2) rank 1 and rational 575-edge
  ranks (4,4,0); its value is local only.
- Omitting the negative source projector loses the source-endpoint identity
  and the N source-rank contribution.
- Treating reclaimed-role clearing as free understates the profile. PR #60's
  rank-first word includes every clear XOR and raises its operands first.

## Limits

The old copied-fixed proof in the PR #63 tree contains earlier producer
counts and a different W. Its structural projector, product-basis and
endpoint lemmas are reused; none of those old numeric totals are used here.
The current W, s and profile come from the PR #63 rank-pair word and
screen certificate.

The per-use graph-node-to-emitted-XOR event id is still absent. The global
sum does not need it because the emitted word carries a common frame-group
id for each physical XOR and all transitions are accounted. A separate
single-pivot attribution task would still need that stable provenance id
plus the chosen rational pivot coordinates.

Prepared with OpenAI Codex assistance.
