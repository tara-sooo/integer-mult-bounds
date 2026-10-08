# Common frames and terminal identities

**Status: PROVED_BY_PINNED_SOURCE for the PR #63 h=23/25 bit network.**
The global assignment is a compact source-defined projector family on
Q^575; Issue 16's one-gate tensor choice is not used as the whole-network
proof.

## Manuscript contract

Section 3 assigns one rational matrix M_v to every source, gate and sink,
with the same matrix on all incidences of a gate. Its frame invariant is

\[
D_out\,S_\Omega\,D_in^{-1}.
\]

Section 4 then requires a scalar permutation rho of all W input roles and

\[
M_out(\rho(w))-M_in(w)=I_m\quad\text{for every role }w,\qquad
s=\sum_e \operatorname{rank}_{\mathbb Q}(M_head(e)-M_tail(e))<Wm.
\]

These are the source's equations, not an interpretation of the pointwise
GF(2) XOR matrix. The original negative source projector is part of both
the endpoint identity and the rank sum.

## Source-defined 23/25 to 575 frame family

Put F_25=Q^25, F_23=Q^23 and F=F_25 tensor F_23, so m=575. On each factor,
the frozen rational metric is G_h=I-J/9. For a triple T, the source line
is spanned by its triple-indicator vector t_T; its norm under G_h is 2.
For a compiler envelope E_h(C,M), with core C and cover M, the PR #63
audit defines its rational orthogonal projector from that same metric.
The exact formula is checked for every canonical core/cover-size case and
coordinate permutations cover the remaining placements.

The old I+J coordinate change is a single fixed similarity, with inverse
I-J/(h+1); it transports all envelope projectors and preserves nesting and
edge ranks. A second fixed compatible basis is used for the 575-dimensional
pivot corners. Neither transform is a per-gate guess.

The product construction uses both axes and all source triple contexts. In
an h=23 local compiler context T in the 25-triples, its gate frame is the
source-defined h=25 triple-line projector tensored with the h=23 envelope
projector for that compiler group. In an h=25 context S in the 23-triples,
the factors are reversed. Outer data, center, exterior and endpoint gates
use the listed product subspaces and complements in the inherited
two-stage construction. Thus every physical XOR's compiler group and
context determine one rational 575 by 575 matrix.

For the two data banks indexed by a pair of triples, let

\[
U_a=\operatorname{im}(P_{T_{25}}\otimes P_{T_{23}}).
\]

This is a nondegenerate rank-one subspace. The source product-frame table
uses U_a, its orthogonal complement, the full product space, and the
stagewise product complements; it includes the copied-center and paid
endpoint-copy paths.

For each actual rank-first XOR, the saved operation names one compiler
group g. The compiler raises both participating slots to g before applying
XOR, so both inputs and outputs use the same frame M_g. Copy/clear XORs
follow the same path. The source formula maps g's core/cover key to its
rational projector. The common-frame equation therefore holds at every
emitted elementary gate, not only at the Issue 16 logical FSa -> Y2 gate.

## All-role endpoint calculation

For each data pair a, use the Section 3 source/sink assignment:

| Input role w | rho(w) | M_in(w) | M_out(rho(w)) | Difference |
|---|---|---|---|---|
| X_a | Y_a | -P_Ua | P_(U_a-perp) | I_575 |
| Y_a | X_a | 0 | I_575 | I_575 |
| Any Section 3 auxiliary/scratch input role A | A | 0 | I_575 | I_575 |

Because U_a is nondegenerate, P_(U_a-perp)=I_575-P_Ua. Thus the first
row is (I-P_Ua)-(-P_Ua)=I; the other two rows are I-0=I. The scalar map
rho is the X/Y bank exchange and fixes every restored auxiliary. The
copy-center pass is not a new independent input terminal: it temporarily
copies an existing center stream, pays for its transform and read/erase
route, and preserves the original role endpoints. The rank-first replay
establishes restoration of arbitrary dirty compiler slots.

One global similarity S preserves this equation:
S(M_out-M_in)S^-1=S I S^-1=I. This is why the fixed I+J and compatible
pivot basis changes do not weaken the endpoint contract.

## Evidence map and the Issue 16 boundary

| Arrow | Status | Pinned basis |
|---|---|---|
| Original Section 3 scalar motif -> full role permutation rho | PROVED_BY_PINNED_SOURCE | [03-motifs.tex](https://redirect.github.com/CrocSwap/integer-mult-bounds/blob/aa7701b68540b7863d3b66a414e4319915d6282d/upstream/build/sections/03-motifs.tex#L89) and [copied-fixed proof](https://redirect.github.com/CrocSwap/integer-mult-bounds/blob/aa7701b68540b7863d3b66a414e4319915d6282d/research/copied-fixed/PROOF.md#L168) |
| Rational endpoint matrices and all-role identity | PROVED_BY_PINNED_SOURCE | [03-motifs.tex](https://redirect.github.com/CrocSwap/integer-mult-bounds/blob/aa7701b68540b7863d3b66a414e4319915d6282d/upstream/build/sections/03-motifs.tex#L467) |
| Current pair graph -> same shear primitive, all dirty slots restored | PROVED_BY_PINNED_SOURCE | [pair-assembly proof](https://redirect.github.com/CrocSwap/integer-mult-bounds/blob/aa7701b68540b7863d3b66a414e4319915d6282d/research/pair-assembly/PROOF.md#L101), [rank-pair proof](https://redirect.github.com/CrocSwap/integer-mult-bounds/blob/aa7701b68540b7863d3b66a414e4319915d6282d/research/rank-pair/PROOF.md#L51) |
| Envelope key -> exact rational projector | PROVED_BY_PINNED_SOURCE; CHECKED_LOCALLY | [copied-fixed projector proof](https://redirect.github.com/CrocSwap/integer-mult-bounds/blob/aa7701b68540b7863d3b66a414e4319915d6282d/research/copied-fixed/PROOF.md#L230), [audit.py](https://redirect.github.com/CrocSwap/integer-mult-bounds/blob/aa7701b68540b7863d3b66a414e4319915d6282d/research/pair-assembly/audit.py#L15) |
| 23/25 projectors -> all two-factor data, auxiliary and terminal frames | PROVED_BY_PINNED_SOURCE | [product endpoint proof](https://redirect.github.com/CrocSwap/integer-mult-bounds/blob/aa7701b68540b7863d3b66a414e4319915d6282d/research/copied-fixed/PROOF.md#L168), [two-stage product frames](https://redirect.github.com/CrocSwap/integer-mult-bounds/blob/aa7701b68540b7863d3b66a414e4319915d6282d/notes/copied-centers-bit.tex#L27) |
| Issue 16 FSa -> Y2 tensor example -> all PR #63 gates | NOT_CLAIMED | Issue 16 proves only one logical neighborhood and one chosen h=25 line; the global family above comes from the pinned inherited proof, not extrapolation from that example. |
| Logical source/use -> one exact emitted XOR index | MISSING_PROVENANCE, not a global contract gap | The word stores slot and frame-group ids, but not the original graph node/use id; see [Issue 16 frozen result](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/cf0f30e932416a35147ec2e69f28b87a48e18b31). |

The last missing locator matters for attributing one selected pivot to one
logical use. It is not needed to define or verify the uniform rational
frame family on the entire emitted word.

Prepared with OpenAI Codex assistance.
