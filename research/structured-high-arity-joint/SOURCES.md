# Sources and provenance

This is the bounded first checkpoint for
[fork Issue 32](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/32),
read in full on 2026-10-09. It was created in a dedicated linked worktree
from fork `origin/main` at
[`0605a24a28836168ad29d6239b46064b892298fc`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/0605a24a28836168ad29d6239b46064b892298fc).

## Fixed manuscript and prior checkpoint

- Original multiplication manuscript by OpenAI, pinned at
  [`adc7f1241b42e322a6451854ab7e4b4c146bf78a`](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a).
  The exact Section 3, 4, and 6 files were fetched from that commit and
  their SHA-256 values matched the fork's `upstream/manifest.json`:
  `build/sections/03-motifs.tex`
  `ed76761194988a01af77ead0ea6469cb5dcd29690ab985a0b5a4006b0f2b69bb`,
  `build/sections/04-swap.tex`
  `412b170ccaab38dba96e95e3cbfae09f4876a9818f8d278776a746b0f8044906`,
  and `build/sections/06-transforms.tex`
  `924316e4bc905066281d8f9e8746a49d8829aeb393688608deb1e61c3c87853c`.
  Section 4 charges recursive calls as full-array interchanges; Section 6
  names the Nussbaumer/Quandalle and Harvey–van der Hoeven transform route.
  Neither provides a typed bridge for this `Conv_m` child model. The
  pinned source license hash is recorded as
  `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` in
  the same manifest.
- Issue 31's exact checkpoint is fork commit
  [`99f1d2b1402604bc15e9dd6f23ac3056e0a2a1a2`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/99f1d2b1402604bc15e9dd6f23ac3056e0a2a1a2),
  under `research/joint-recursion-reduction/`. Its typed length-four
  identity is Karatsuba; its checker covered all 16 basis pairs and its
  recorded adverse decoder failed as intended. I ran that pinned checker:
  `PASS`, 16 pairs, exact integer arithmetic. Its paid recurrence has
  `3` half-size children and exponent `log_2(3)`, so it is not a new
  near-linear `κ` result.
- The fork's conditional comparison witness comes from the starting fork
  commit above and is `κ₀=971668963/25000000000000`. It is not used in the
  rank proof.

## Canonical convolution-rank sources

- C. M. Fiduccia and Y. Zalcstein, “Algebras Having Linear Multiplicative
  Complexities,” *JACM* 24(2), 311–331 (1977),
  [DOI 10.1145/322003.322014](https://doi.org/10.1145/322003.322014).
  Source for the lower-bound side of the classical bilinear complexity
  result used in MODEL.md.
- A. Lempel, G. Seroussi, and S. Winograd, “On the Complexity of
  Multiplication in Finite Fields,” *Theoretical Computer Science* 22(3),
  285–296 (1983), [DOI 10.1016/0304-3975(83)90108-1](https://doi.org/10.1016/0304-3975(83)90108-1).
  Its discussion of polynomial bilinear complexity records the
  `2s−1` lower bound, Toom's matching construction over infinite fields,
  and the fact that minimal algorithms use interpolation.
- A. Borodin and R. Moenck, “Fast Modular Transforms,” *Journal of Computer
  and System Sciences* 8(3), 366–386 (1974),
  [DOI 10.1016/S0022-0000(74)80029-2](https://doi.org/10.1016/S0022-0000(74)80029-2).
  This is the classical fast multipoint evaluation/interpolation control:
  the paper reduces those tasks to polynomial division and product trees.
  It is not a novel decoder in this checkpoint.
- A. L. Toom, “The complexity of a scheme of functional elements
  simulating the multiplication of integers,” *Doklady Akademii Nauk SSSR*
  150(3), 496–498 (1963),
  [MathNet record](https://www.mathnet.ru/eng/dan/v150/i3/p496). Cited as
  the historical construction source, not as a new method here.
- A. Schönhage and V. Strassen, “Schnelle Multiplikation großer Zahlen,”
  *Computing* 7(3–4), 281–292 (1971),
  [DOI 10.1007/BF02242355](https://doi.org/10.1007/BF02242355). Historical
  transform-based integer-multiplication comparison; no part of that
  algorithm is rederived or claimed here.

## Verification and attribution

The checker uses Python's standard library and exact integers. No code,
certificates, or text from the mathematical sources were copied; their
authors and provenance are cited above. This research note and checker were
prepared with substantial OpenAI Codex assistance. No independent review
or full repository verification is claimed.
