# Sources, pins, and reproduction

## Frozen sources

| Item | Pin |
|---|---|
| PR 63 h=23 circuit | commit `aa7701b68540b7863d3b66a414e4319915d6282d` |
| Issue 19 real-word provenance checkout | commit `eaa21e97209357575ef462d189c0950b6da85e7c` |
| Issue 20 result read for controls | commit `e2cf064a7976566e8a9e60719c16f0c7d12160d9` |
| PR 63 graph source SHA-256 | `3d47e89d2649c90800a276bdd0480131def50e0bdf92c122a19494b55bf17420` |
| PR 63 compiler source SHA-256 | `9984aaccf880e4840402322d76678bfddb33ce7e494af78430a43429f51b85fd` |
| Canonical frozen word SHA-256 | `640696dd7cd893add9d6e12d0d587956fecf113b2eff8c29547b82e5a6f3c0ad` |
| Deterministic frozen gzip SHA-256 | `1a57c143380a063211653f1f35e7cc9710539523b0b34c90f354a0425c34bd59` |
| PR 74 historical comparison pin | commit `23468ac3867e778f54835ab66eb513934965160b` |
| PR 74 selected verifier pin | commit `2eecf5f8e4eafb3dd13dbc70b9ecc5b4e6e9a77c` |

PR 74 is referenced through [the upstream PR](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/74). The current PR head was not substituted for the pinned historical source. PR 63 is [the upstream circuit PR](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/63). The task context is [Issue #21](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/21); the prior result is [Issue #20](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/20).

## Runs

The pinned Issue 19 worktree path used as source is `/data/data/com.termux/files/home/integer-mult-bounds-issue-19`.
The Issue 21 worktree is `/data/data/com.termux/files/home/integer-mult-bounds-issue-21`, on branch `issue-21-paid-reuse-candidate-screen`, based on fork `origin/main` commit `0605a24`.

```sh
python3 research/paid-reuse-candidate-screen/fast_check.py /data/data/com.termux/files/home/integer-mult-bounds-issue-19
python3 research/paid-reuse-candidate-screen/focused_probe.py /data/data/com.termux/files/home/integer-mult-bounds-issue-19 62984
python3 research/paid-reuse-candidate-screen/focused_probe.py /data/data/com.termux/files/home/integer-mult-bounds-issue-19 62985 --all-eligible
python3 research/paid-reuse-candidate-screen/focused_probe.py /data/data/com.termux/files/home/integer-mult-bounds-issue-19 --span-only 21
python3 research/paid-reuse-candidate-screen/focused_probe.py /data/data/com.termux/files/home/integer-mult-bounds-issue-19 --span-only 62985
python3 research/paid-reuse-candidate-screen/focused_probe.py /data/data/com.termux/files/home/integer-mult-bounds-issue-19 --all-spans
```

FAST verifies the source manifest, canonical word and source hashes before scanning. FOCUSED compiles the pinned baseline and alternative with `matching=True`, `reclaim=True`, `dirty=False`; it asserts all block input signals, global scatter, frame inclusions, complete rank histograms, and local M/inverse checks. The all-span pass executes the baseline once and writes one compact span row per screened demand to `regeneration_availability.json`.

## Resource record

| Pass | Wall time | Peak RSS |
|---|---:|---:|
| FAST inventory and carry-edge screen | 19.96 s | 557,636 KiB |
| FOCUSED value 62984 baseline plus one forced carry | 117.51 s | 489,600 KiB |
| FOCUSED value 62985 baseline plus two forced carries | 118.13 s | 494,116 KiB |
| FOCUSED value 21 baseline span screen | 53.65 s | 462,464 KiB |
| FOCUSED value 62985 span and small-carrier screen | 58.42 s | 414,396 KiB |
| All-demand availability screen | 926.11 s | 539,696 KiB |

The baseline and alternative hashes, source pins, timing details, and exact operation/profile ledgers are retained in the JSON receipts. Codex assisted with this research artifact; no upstream issue, pull request, or comment was created.
