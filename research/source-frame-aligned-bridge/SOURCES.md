# Sources and provenance

This checkpoint read the full [Issue 38](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/38) body and the immutable Issue 37 result before writing. It copies no paper or Lean source.

## Fork checkpoint and issue

- Issue 38: [source-frame adapter task](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/38).
- Issue 37 failure checkpoint: [commit 03c030320085b211d9b5f2c5d94715db4547136b](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/03c030320085b211d9b5f2c5d94715db4547136b), files under `research/bridged-multipair-multiplication/`. Its direct twin assignment fails for distinct original source lines; aliasing the two roles loses independent data.
- This branch starts from fork `origin/main`, commit [0605a24a28836168ad29d6239b46064b892298fc](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/0605a24a28836168ad29d6239b46064b892298fc).

## Original manuscript

The frozen source is [OpenAI/math commit adc7f1241b42e322a6451854ab7e4b4c146bf78a](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a).

| Path at the pin | Use | SHA-256 |
| --- | --- | --- |
| `preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/03-motifs.tex` | $\mathcal T_h^3$ data roles, signed endpoint, dirty scratch, source/sink labels, complex frame operator | `ed76761194988a01af77ead0ea6469cb5dcd29690ab985a0b5a4006b0f2b69bb` |
| `preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/04-swap.tex` | bit all-role endpoint, rational rank charges, chunk interchange and recursion | `412b170ccaab38dba96e95e3cbfae09f4876a9818f8d278776a746b0f8044906` |
| `preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/06-transforms.tex` | recorded transform order, pointwise product, inverse layout and coefficient recovery | `924316e4bc905066281d8f9e8746a49d8829aeb393688608deb1e61c3c87853c` |

The three hashes match the vendored manifest in the prior Issue 37 checkpoint. Relevant source locations: Section 3 lines 20–125, 148–186, 210–245, 467–525, 530–583, and 627–665; Section 4 lines 103–127 and 165–211; Section 6 lines 656–736.

## [PR 209](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/209) and its pinned Lean source

- [Upstream PR 209](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/209), fixed head [a7aeea067ec1e2b7e91b0ecec660512b7cafca26](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/a7aeea067ec1e2b7e91b0ecec660512b7cafca26). The fixed commit changes only `CONTRIBUTORS.md`; the PR points to the external proof project.
- [WHT Lean project commit fdfb7815c15ec43af0fb54818a6a57ae4025126b](https://redirect.github.com/jacobalansussman/wht-power-saving-lean/commit/fdfb7815c15ec43af0fb54818a6a57ae4025126b), actual gate sources:
  - `Work/Bridge/Net.lean`, `Bridge2` frame/role fields and `S0` through `S8` (especially lines 51–82, 103–125, 147–183).
  - `Work/Bridge/Cert.lean`, `pC`, `kCc`, `Bridge2.gateC`, the five-stage route, and helper-state chain (lines 49–56, 88–93, 133–169).
  - `Work/GCert/Data/ChallengeB2Gp193x.lean` and `Work/GCert/Data/SolutionB2Gp193x.lean`, the exact-complex WHT theorem statement and wrapper.
  - `Work/GCert/Data/P193Cert.lean`, the certificate label replay and invocation price for the rebuilt complex word.

The WHT project credits Jacob Sussman and its underlying community contributors, and discloses directed Claude-agent assistance. No source code or certificate data from that project was copied.

## Validation and authorship

`python3 research/source-frame-aligned-bridge/check_adapter.py` completed successfully; its exact JSON output is checked in `receipt.json`. Original source hashes were matched against the earlier checkpoint. The Lean project, physical supplier, full multiplication verifier, and all-size transfer were not rebuilt because the missing lift and rank gate already stop this bounded checkpoint.

Research text and the small exact checker were prepared by Codex with substantial AI assistance.
