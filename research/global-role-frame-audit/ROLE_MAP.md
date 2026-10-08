# Whole-role map for PR #63

**Status: GLOBAL_CONTRACT_SOURCE_BACKED for the pinned h=23/25 bit network.**
The source proves the full role map by composing its shear compiler with the
inherited two-bank construction. The compiler's dirty replay alone is not the
permutation proof.

## Scope and role inventory

This audit uses the fork's frozen PR #63 source at
[commit aa7701b68540b7863d3b66a414e4319915d6282d](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/aa7701b68540b7863d3b66a414e4319915d6282d),
the h=23/25 bit branch with N=4,073,300 data pairs and m=575. It does not
reuse the older copied-fixed W or rank totals. The current rank-first source
and certificate give R23=27,918, R25=36,586 and W=137,151,806.

Let v_h=binom(h,3), and let R_h be the compiler's complete role count,
including retained output carriers. The role partition is

| Roles | Count | Scalar action in the full finite circuit |
|---|---:|---|
| Data bank X, indexed by one 25-triple and one 23-triple | N | Sent to the matching Y role |
| Data bank Y, same index set | N | Sent to the matching X role |
| Replicated h=23 compiler scratch | v25 R23 = 64,211,400 | Fixed; arbitrary initial values restored |
| Replicated h=25 compiler scratch | v23 R25 = 64,793,806 | Fixed; arbitrary initial values restored |

Thus W=2N+v25 R23+v23 R25=137,151,806. The complete scalar permutation is

\[
\rho(X_a)=Y_a,\qquad \rho(Y_a)=X_a,\qquad \rho(A)=A
\]

for every data index a and every scratch role A. The bit network has no
nontrivial scalar sign. Retired/reclaimed compiler slots are members of the
scratch partition; they are not free or omitted roles.

The temporary copied-center stream in the tape realization is a charged
copy/transform/read/erase pass. It is not an uncounted terminal of the scalar
finite circuit: the inherited lemma keeps the original role endpoints and
restores arbitrary scratch.

## Why the rank-first replay is not itself rho

The saved h-axis word realizes a controlled XOR shear. Its replay checks the
full basis of both data banks and every dirty compiler slot, in both
orientations. For h=23 this is 31,460 basis vectors over 621,482 elementary
operations; for h=25 it is 41,186 vectors over 855,860 operations. The
recorded output is a shear, not a role permutation.

The separate inherited scalar proof supplies the missing composition:
the two shears, the rank-one endpoint correction, and the bank exchange at
merge send the data banks to a full interchange; each shear restores its
arbitrary auxiliary vector. This is the step that proves rho for every
input role. It does not infer a permutation from JLV=I or from output
correctness alone.

## Representative routes

### Ordinary input

In the pinned h=23 pair graph, input id 0 is the triple (0,1,2), at logical
source node 1. A source-to-center-output path in the regenerated logical DAG
is

\[
1\to1801\to1949\to1986\to1987\to1997\to2001.
\]

The additions on this path are respectively
1800 XOR 1, 1828 XOR 1801, 1985 XOR 1949, 1986 XOR 1948,
1990 XOR 1987, and 2000 XOR 1997. Node 2001 is the retained center output
(common point 0), whose support has 231 triples and includes input id 0.
Its scatter reads include data target id 0 because that triple contains 0.
Across all output uses, the pinned scalar identity is JLV=I.

This is a logical DAG route, not a fabricated physical-word event ID. The
rank-first word records compiler frame-group ids and physical slots but does
not preserve the pair-graph node/use id on each XOR. Issue 15's local
producer-use-to-word-event locator gap therefore remains for a single-event
trace. It does not prevent the universal word replay or the source-defined
whole-role map above.

### Retained/copy-center role

Take the h=23 retained center for common point 0. Its envelope rank is
r=h-1=22. In the forward orientation, the old original path is
D_U -> D_0 -> D_1, of ranks 22 and 23. The copied-center proof keeps the
original at D_U, pays rank 22 to transform a copy to D_0 for every
read-only scatter, erases that copy, then moves the original directly to
D_1 for rank 1. In the reverse orientation, the original moves D_0 ->
D_(U-perp) for rank 1; a copy is transformed to D_1 for rank 22, supplies
the early reads, and is erased. The original scalar value and both terminal
operators are unchanged in either orientation.

The output-use carrier is a separate terminal: matching cannot merge two
designated outputs or bypass a later producer use. The copy transform is
paid and remains in the profile.

### Arbitrary auxiliary/retired role

For an arbitrary dirty value z, the inherited chronological word
L,J,L^-1,V,L,J,L^-1,V cancels its old contribution, applies the requested
data shear, and restores z. The current rank-first compiler handles a
reclaimed slot s only when its current envelope is contained in the
requested frame. Its literal XOR clears run at that common frame; the
compiler asserts the slot is zero before reuse. Every such XOR and both
operand frame raises are included in the saved word and charged profile.

The pinned replay checks every dirty basis vector, so the auxiliary identity
is a finite linear identity for arbitrary dirty values, not a sample of
initializations. This covers ordinary scratch, retained/reclaimed slots, and
the reverse-complement orientation.

## Source trail

- Current graph, role counts and inherited proof dependencies:
  [PR #63 pair-assembly proof](https://redirect.github.com/CrocSwap/integer-mult-bounds/blob/aa7701b68540b7863d3b66a414e4319915d6282d/research/pair-assembly/PROOF.md#L101),
  [rank-pair proof](https://redirect.github.com/CrocSwap/integer-mult-bounds/blob/aa7701b68540b7863d3b66a414e4319915d6282d/research/rank-pair/PROOF.md#L25).
- Full rational envelope timeline, terminal uniqueness and dirty replay
  checker: [original_timeline.py](https://redirect.github.com/CrocSwap/integer-mult-bounds/blob/aa7701b68540b7863d3b66a414e4319915d6282d/research/pair-assembly/original_timeline.py#L233).
- Rank-first clear/reuse and complete-basis shear replay:
  [rank_pair_compiler.py](https://redirect.github.com/CrocSwap/integer-mult-bounds/blob/aa7701b68540b7863d3b66a414e4319915d6282d/scripts/experiments/rank_pair_compiler.py#L114),
  [rank-pair receipt](https://redirect.github.com/CrocSwap/integer-mult-bounds/blob/aa7701b68540b7863d3b66a414e4319915d6282d/research/rank-pair/frame-compiler.json).
- Product endpoint and copied-center schedule:
  [copied-fixed proof](https://redirect.github.com/CrocSwap/integer-mult-bounds/blob/aa7701b68540b7863d3b66a414e4319915d6282d/research/copied-fixed/PROOF.md#L155),
  [copied-center lemma](https://redirect.github.com/CrocSwap/integer-mult-bounds/blob/aa7701b68540b7863d3b66a414e4319915d6282d/notes/copied-centers-lemma.tex#L37).

Prepared with OpenAI Codex assistance.
