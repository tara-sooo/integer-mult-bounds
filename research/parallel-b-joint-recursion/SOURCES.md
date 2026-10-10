# Sources and scope

## Immutable starting point and original semantics

- Fork start: [`tara-sooo/integer-mult-bounds` commit `0605a24a28836168ad29d6239b46064b892298fc`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/0605a24a28836168ad29d6239b46064b892298fc). The research branch is based directly on this commit.
- Original manuscript: [`openai/math` commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a), vendored unchanged under `upstream/`.

| Pinned file | SHA-256 | Use |
|---|---|---|
| `upstream/build/sections/00-introduction.tex` | `98721f03682ccf1cc7d0850b07adabaa2d8f3afe552e3861753eba9d284d0da0` | Exact `n`-bit integer product semantics; reduction to coefficient convolution |
| `upstream/build/sections/03-motifs.tex` | `ed76761194988a01af77ead0ea6469cb5dcd29690ab985a0b5a4006b0f2b69bb` | Source/target roles, arbitrary dirty scratch, and finite network semantics |
| `upstream/build/sections/04-swap.tex` | `412b170ccaab38dba96e95e3cbfae09f4876a9818f8d278776a746b0f8044906` | Rank-pivot child calls and the actual `F_k <= (s/W) F_{k-1} + O(1)` recurrence |
| `upstream/build/sections/06-transforms.tex` | `924316e4bc905066281d8f9e8746a49d8829aeb393688608deb1e61c3c87853c` | Transform/convolution interface, exact coefficient widths, packing and cleanup charges |
| `upstream/LICENSE` | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` | Original manuscript license retained |

The cited source lines are in `00-introduction.tex` 15–47, `03-motifs.tex` 1–80 and 140–190, `04-swap.tex` 90–130 and 190–210, and `06-transforms.tex` 450–480 and 570–720. The fork manifest records the same hashes. No manuscript text or code was copied into this checkpoint.

## Prior fork results used as novelty controls

These are scope controls, not premises of the tensor proof below.

| Record | Pinned reference | Relevant boundary |
|---|---|---|
| Issue 11, multi-type profile switching | [Issue 11](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/11) | Existing-profile switching is not an automatically composable typed multiplication child. |
| Issue 23, completed-child identity | [Result commit `267c24dfa448fbf43fa68b7d2cfdd5f9580be458`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/267c24dfa448fbf43fa68b7d2cfdd5f9580be458) | The tested Section 4 child payloads differed; equal shape or rank is not equal work. |
| Issue 31, typed Karatsuba pilot | [Result commit `99f1d2b1402604bc15e9dd6f23ac3056e0a2a1a2`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/99f1d2b1402604bc15e9dd6f23ac3056e0a2a1a2) | Exact typed convolution recursion, but the construction is classical Karatsuba. |
| Issue 32, rational-linear rank screen | [Result commit `08321451a18d590f2d07450887d6b570192eab66`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/08321451a18d590f2d07450887d6b570192eab66) | Restricted `Conv_m` encodings face the stated convolution-rank bound; this does not cover nonlinear bit state. |
| Issue 34, carry-state recursion | [Issue 34](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/34) | The Issue 41 brief classifies the tested carry-state direction as schoolbook-equivalent. This checkpoint does not rely on it as a theorem. |
| Issue 35, data handoff | [Result commit `f6618ae74e6e2ad4c2583c915f967809887d4794`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/f6618ae74e6e2ad4c2583c915f967809887d4794) | Legal chronology reuse removed no charged data child. |
| Issue 36, frame-transition coalescing | [Result commit `6a9cdb35d76d73e3f2367b494366c230b78a2ce6`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/6a9cdb35d76d73e3f2367b494366c230b78a2ce6) | Aggregate width counts did not identify a legal typed call chain. |
| Issue 37, source-typed bridge | [Result commit `03c030320085b211d9b5f2c5d94715db4547136b`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/03c030320085b211d9b5f2c5d94715db4547136b) | The raw twin-source mapping aliases independent data or fails the common-frame condition. |
| Issue 38, frame adapter | [Result commit `b1741e7dd6e6b13f1b329d34415ee1e8cc1cc467`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/b1741e7dd6e6b13f1b329d34415ee1e8cc1cc467) | Label-rank adapters do not supply a cheaper legal full-array child after entry/exit costs. |
| Issue 39, fibre packing | [Issue 39](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/39) | Direct-sum relabeling preserves additive rank; label rank is not a paid Section 4 rank. |

The Issue 41 brief is [`tara-sooo/integer-mult-bounds` Issue 41](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/41). No sibling worktree or in-progress lane artifact was read. The Issue 34 and 39 links above are issue records rather than immutable completed-checkpoint commits; they are included only as requested novelty context, not as proof inputs.

## Attribution and reproducibility

The upstream manuscript is authored by OpenAI and remains under its retained Apache-2.0 license. This checkpoint adds original analysis and a small exact checker under the fork's Apache-2.0 license; it does not copy upstream implementation. The derivation, experiment design, checker, and report were prepared with substantial OpenAI Codex assistance at the repository maintainer's direction. No independent human review is claimed.

Reproduce the exact pilot from the repository root with:

```sh
python3 research/parallel-b-joint-recursion/check_joint_tensor.py
```
