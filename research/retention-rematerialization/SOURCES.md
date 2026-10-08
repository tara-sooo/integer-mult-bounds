# Sources and reproduction

## Issue scope and source records

- [Issue 20](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/20) requests a FAST screen followed by focused verification of a real retention/rematerialization comparison.
- [Issue 19](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/19) and its verified [evidence commit](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/eaa21e97209357575ef462d189c0950b6da85e7c) pin the h=23 physical word and the `FSa(2039)→Y2(2044)` provenance.
- [PR 63](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/63), construction commit `aa7701b68540b7863d3b66a414e4319915d6282d`, supplies the frozen circuit source.

## Exact inputs

| Input | Identity |
|---|---|
| Issue 19 commit | `eaa21e97209357575ef462d189c0950b6da85e7c` |
| PR 63 graph commit | `aa7701b68540b7863d3b66a414e4319915d6282d` |
| PR 63 `pair_graph.py` SHA-256 | `3d47e89d2649c90800a276bdd0480131def50e0bdf92c122a19494b55bf17420` |
| Frozen compiler SHA-256 | `9984aaccf880e4840402322d76678bfddb33ce7e494af78430a43429f51b85fd` |
| Canonical h=23 word SHA-256 | `640696dd7cd893add9d6e12d0d587956fecf113b2eff8c29547b82e5a6f3c0ad` |
| Deterministic gzip SHA-256 | `1a57c143380a063211653f1f35e7cc9710539523b0b34c90f354a0425c34bd59` |
| In-memory focused instrumentation SHA-256 | `e2eb7063e5ca6788dd86b3c2affdc49b470efc3ba57ca89ef820e76e6843bb89` |
| Runtime instrumentation SHA-256 | `749e7efbe915f0d9e4979792e8c7737d5c95d5013ee5e163d134dcaa710d46d5` |

The Issue 19 runner's default graph is not PR 63's graph when imported alone. Both checks explicitly load the pinned `pair_graph.py`; the initial wrong-graph diagnostic was discarded. The focused compiler modifications are in memory only; the frozen compiler and word in the Issue 19 worktree are not edited.

## Method references and negative control

- [PR 74](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/74), pinned at `23468ac3867e778f54835ab66eb513934965160b`; selected verification commit `2eecf5f8e4eafb3dd13dbc70b9ecc5b4e6e9a77c`. Its deferred-span reconstruction pattern motivated checking actual compatible controls, destination reservation, physical frame transitions, next-use timing, and cleanup. It is a different circuit; its numerical results and schedule are not reused.
- [PR 96](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/96), withdrawn pin `606d16d6dfc714d2a467190dc91b2f8dcab38d9c`. The negative control rejects merging distinct physical transitions without a recorded event and common target frame.

## Reproduction

Provide a clean Issue 19 checkout at the pinned commit as the first argument. The commands below write the receipts included in this directory:

```sh
python3 research/retention-rematerialization/fast_check.py /path/to/issue-19-worktree > research/retention-rematerialization/FAST_RECEIPT.json
python3 research/retention-rematerialization/focused_probe.py /path/to/issue-19-worktree
```

The focused probe accepts `--output PATH` to choose a different receipt path; it writes a hash checkpoint beside that output. Both scripts assert the source commit and pinned graph/compiler/word hashes before accepting a result.

## Attribution

The code and frozen circuit inputs remain under the licenses and notices distributed with the pinned PR 63/Issue 19 source. This change adds local analysis scripts, receipts, and reports; it does not redistribute the source closure. Codex assisted with source inspection, check implementation, and report drafting; the reported claims are gated by the recorded deterministic checks.
