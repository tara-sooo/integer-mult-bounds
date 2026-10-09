# Sources and provenance

## Task and predecessor checkpoint

The full body of [fork Issue 39](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/39)
was read on 2026-10-09. Work starts from fork origin/main at
[commit 0605a24a28836168ad29d6239b46064b892298fc](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/0605a24a28836168ad29d6239b46064b892298fc).
The prior [Issue 38 checkpoint](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/b1741e7dd6e6b13f1b329d34415ee1e8cc1cc467)
is cited only as context; it was not assumed to be merged.

## Original multiplication source

The frozen manuscript is [OpenAI/math commit adc7f1241b42e322a6451854ab7e4b4c146bf78a](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a).
The checked-in upstream/manifest.json pins these files and hashes:

| Section | Use | SHA-256 |
|---|---|---|
| 03-motifs.tex | \(\mathcal T_h^3\) data roles, stage-3 common gate labels, arbitrary dirty scratch, complex array frames | ed76761194988a01af77ead0ea6469cb5dcd29690ab985a0b5a4006b0f2b69bb |
| 04-swap.tex | full-array F2 Swap, rational endpoint identity and paid rank rule | 412b170ccaab38dba96e95e3cbfae09f4876a9818f8d278776a746b0f8044906 |
| 06-transforms.tex | recorded-order inverse layout and coefficient recovery obligations | 924316e4bc905066281d8f9e8746a49d8829aeb393688608deb1e61c3c87853c |

The hashes were recomputed from the local pinned files. No manuscript
or external proof source was copied into this checkpoint.

## Upstream control

The current [upstream PR 234](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/234)
was read through the GitHub API on 2026-10-09. Its head was
[commit af3fe331ca60c936229e060681ffccbc1c208678](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/af3fe331ca60c936229e060681ffccbc1c208678),
open and not draft. Its report gives the five-stage bit and complex
figures and conditional \(\kappa=0.000703701743496697>2^{-11}\)
recorded in COST_GATE.md, states that the helpers cross five disjoint
temporal address windows before paid completion, and retains
source-bound, analytic, precision, and routing hypotheses. This
checkpoint did not replay that verifier.

## Validation, license, and assistance

Run the deterministic exact checker with:

~~~sh
python3 research/fibre-packed-swap/check_fibre.py
~~~

It uses only the Python standard library. The new checker and research
text are original work under the repository's Apache-2.0 license. The
paper and upstream PR are cited and attributed; their code and data were
not copied. This research text and checker were prepared by Codex with
substantial AI assistance.
