# Fixed sources and provenance

This is the bounded first checkpoint for
[fork Issue 34](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/34),
read in full on 2026-10-09. The dedicated linked worktree and branch start
from fork `origin/main` at
[`0605a24a28836168ad29d6239b46064b892298fc`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/0605a24a28836168ad29d6239b46064b892298fc).

## Pinned fork research

- Issue 31 is pinned at
  [`99f1d2b1402604bc15e9dd6f23ac3056e0a2a1a2`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/99f1d2b1402604bc15e9dd6f23ac3056e0a2a1a2).
  I read `MODEL.md`, `PILOT.md`, `COST.md`, `RESULTS.md`, `SOURCES.md`,
  `check_pilot.py`, and `receipt.json`. Its exact typed three-child
  decomposition is Karatsuba; the script checks all 16 length-four basis
  pairs and rejects the omitted-subtraction control. Its child recurrence
  is different from this four-child integer-block recurrence.
- Issue 32 is pinned at
  [`08321451a18d590f2d07450887d6b570192eab66`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/08321451a18d590f2d07450887d6b570192eab66).
  I read `MODEL.md`, `PILOT.md`, `COST.md`, `RESULTS.md`, `SOURCES.md`,
  `check_obstruction.py`, and `receipt.json`. Its rank gate assumes exact
  `Conv_m` children with rational-linear input encoders and output decoder;
  it proves `q >= ceil((2rm-1)/(2m-1))` in that class. The present child
  type is full integer multiplication and uses a floor/mod carry map, so
  the assumption changes. That change alone is not a complexity saving.

## Original manuscript at the fixed commit

The original multiplication manuscript is credited to OpenAI and pinned
at
[`adc7f1241b42e322a6451854ab7e4b4c146bf78a`](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a).
I fetched each listed file at that commit and checked its SHA-256 against
the fork's `upstream/manifest.json`:

| Section | File | SHA-256 |
|---|---|---|
| Fixed-tape streams | `build/sections/02-streams.tex` | `606c80db61cad13aa0c3b6060dc4b88dbbe7ac60cdd831aa93f28d908fd09dab` |
| Source/target motif | `build/sections/03-motifs.tex` | `ed76761194988a01af77ead0ea6469cb5dcd29690ab985a0b5a4006b0f2b69bb` |
| Recursive array interchange | `build/sections/04-swap.tex` | `412b170ccaab38dba96e95e3cbfae09f4876a9818f8d278776a746b0f8044906` |
| Existing transform pipeline | `build/sections/06-transforms.tex` | `924316e4bc905066281d8f9e8746a49d8829aeb393688608deb1e61c3c87853c` |
| Integer multiplication and carries | `build/sections/08-assembly.tex` | `763d7945b1e1ec4ebae9b799bcefcc45fa9bae6e2ffad799868a9c3d513dbd4a` |
| Exact arithmetic | `build/sections/09-exact-arithmetic.tex` | `5714e5d0656c78c6a1fde8d01fd11f1ba856a7ea94149b283bd9a50fdbf516c3` |
| Transposition interface | `build/sections/10-transposition.tex` | `c14ad8d56112f6578678a58211bc8d63c3a4b60e55078ac73bc38f7348e713cb` |

Section 2 specifies one fixed finite alphabet and a fixed number of
one-dimensional tapes, with one-cell head movement per step. Sections 3–4
route source/target roles and implement a whole-array interchange with
full-array recursive children, explicit parking, copies, cleanup, and
head returns. Section 8 recovers ordinary coefficients and uses a
least-significant-first radix carry invariant before emitting the exact
fixed-width product. Those child types and volume units do not match
`Mul_m` in this pilot. Section 6's synthetic transforms are a comparison,
not a carry-state result.

## Classical comparisons

- Karatsuba is used in the pinned Issue 31 checkpoint above.
- A. Toom, “The complexity of a scheme of functional elements simulating
  the multiplication of integers,” *Doklady Akademii Nauk SSSR* 150(3),
  1963, [MathNet record](https://www.mathnet.ru/eng/dan/v150/i3/p496).
  The multi-block evaluation/interpolation family is a known comparison,
  not the selected direct four-product split.
- G. Hanrot, M. Quercia, and P. Zimmermann, “The Middle Product Algorithm
  I,” *Applicable Algebra in Engineering, Communication and Computing*
  14, 415–438 (2004), [DOI 10.1007/s00200-003-0144-2](https://doi.org/10.1007/s00200-003-0144-2).
  It computes a specified middle coefficient window; that output contract
  differs from the paired complete integer windows here.
- D. Harvey, “Faster truncated integer multiplication,” 2017,
  [arXiv:1703.00640](https://arxiv.org/abs/1703.00640). Its abstract gives
  a 25% asymptotic saving for high or low products under a real-cyclic-
  convolution assumption. It does not prove a saving for this joint
  recursion.
- M. J. Fischer and L. J. Stockmeyer, “Fast on-line integer
  multiplication,” STOC 1973, 67–72,
  [DOI 10.1145/800125.804037](https://doi.org/10.1145/800125.804037).
  Online multiplication has a streaming input/output contract; this pilot
  receives both operands in full before recursion.

The code in this checkpoint is a new exact checker using the Python
standard library. No paper source code, generated data, or certificate was
copied. This work was prepared with substantial OpenAI Codex assistance;
independent human review is not claimed.
