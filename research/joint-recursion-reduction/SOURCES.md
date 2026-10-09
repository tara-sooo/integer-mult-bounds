# Sources and provenance

This folder is the bounded first checkpoint for
[Issue 31](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/31),
read in full on 2026-10-09. The worktree was created from fork origin/main
at commit
[0605a24a28836168ad29d6239b46064b892298fc](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/0605a24a28836168ad29d6239b46064b892298fc).

## Immutable mathematical and cost anchors

- Original manuscript, authored by OpenAI, pinned at
  [commit adc7f1241b42e322a6451854ab7e4b4c146bf78a](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a).
  Sections 3 and 4 are
  preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/03-motifs.tex
  and 04-swap.tex. Their SHA-256 values are
  ed76761194988a01af77ead0ea6469cb5dcd29690ab985a0b5a4006b0f2b69bb
  and
  412b170ccaab38dba96e95e3cbfae09f4876a9818f8d278776a746b0f8044906,
  matching the fork's pinned upstream/manifest.json. Section 6,
  06-transforms.tex, has SHA-256
  924316e4bc905066281d8f9e8746a49d8829aeb393688608deb1e61c3c87853c.
  These files ground the triple-indexed source/target network, full-array
  interchange, rank-charged recurrence, and existing synthetic-transform
  comparison.

- Original three-pair construction, pinned at
  [PR 144 source commit c8b22bc5c10dba497ac25804e27d9647d818e2ff](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/c8b22bc5c10dba497ac25804e27d9647d818e2ff).
  The checked files were docs/paired-cube.md and
  notes/paired-cube-sharing.tex. This is a comparison source only; none of
  its circuit, code, or certificate is reused here.

## Fork research checkpoints

- The fixed-profile switching screen is pinned at
  [Issue 10 research commit d0579057de829105fa1376981c75564ac0ceff34](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/d0579057de829105fa1376981c75564ac0ceff34).
- The two-type routing toy is pinned at
  [Issue 11 commit 33afe0a77afc806ba67e5f3119e6e4219580326](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/33afe0a77afc806ba67e5f3119e6e4219580326).
- The cooperative Boolean producer is pinned at
  [Issue 12 commit f1d3f14627fc0574514ae362237174e412fbad4a](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/f1d3f14627fc0574514ae362237174e412fbad4a).
  It changes a toy child profile but not its spectral radius and has no
  multiplication semantics.
- The completed-child identity screen is pinned at
  [Issue 23 commit 267c24dfa448fbf43fa68b7d2cfdd5f9580be458](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/267c24dfa448fbf43fa68b7d2cfdd5f9580be458).
  Its tested pair is not identical; this new candidate changes the work at
  decomposition time and does not claim reuse of a completed child.
- The source-first signed-motif stop is pinned at
  [Issue 30 commit 9a82556e5e39e6b76a9dcdf636abbf10651791f4](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/9a82556e5e39e6b76a9dcdf636abbf10651791f4),
  with its follow-up at
  [commit 78f4a20fa1be5fb7366ae93c808a93d191491472](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/78f4a20fa1be5fb7366ae93c808a93d191491472).
  That candidate had a local matrix but no typed multiplication decoder.
  The present pilot starts from actual convolution input and output spaces.

- The current conditional exponent witness and attribution are recorded at
  the fork's starting commit above, in docs/releases/community-kappa-15.md.
  The reported value is
  971668963/25000000000000 = 3.886675852e-5, conditional on the inherited
  framework.

## Verification and attribution

The only new executable is check_pilot.py, using Python's standard
library and exact integers. Run it from the repository root with the command
in RESULTS.md. Source files are cited by immutable commit and path; no
mutable GitHub branch or pull-request head is a proof source.

The original manuscript author and source license remain credited and
unchanged. This folder and checker were prepared with substantial OpenAI
Codex assistance. No upstream source code or notice text was copied.
