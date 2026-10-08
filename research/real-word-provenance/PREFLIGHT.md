# FAST resource gate and FOCUSED run

## Inputs and scope

- PR 63 construction commit: `aa7701b68540b7863d3b66a414e4319915d6282d` ([redirected PR](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/63), [redirected commit](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/aa7701b68540b7863d3b66a414e4319915d6282d)).
- Issue 18's node/use/block/carrier/slot/event distinctions and fixture-only boundary were checked at fork commit `54e49f0301e09c08d2670a63af6fb15e72b9a146` ([redirected Issue 18](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/18)).
- Pinned h=23 canonical JSON SHA-256: `640696dd7cd893add9d6e12d0d587956fecf113b2eff8c29547b82e5a6f3c0ad`; gzip SHA-256: `1a57c143380a063211653f1f35e7cc9710539523b0b34c90f354a0425c34bd59`.
- Graph SHA-256: `3d47e89d2649c90800a276bdd0480131def50e0bdf92c122a19494b55bf17420`; frozen compiler SHA-256: `9984aaccf880e4840402322d76678bfddb33ce7e494af78430a43429f51b85fd`.

## FAST estimates

The pinned receipt has 52,473 groups, 37,025 matched uses, 27,918 roles, 149,172 XORs, rank mass 642,620, and 621,482 expanded word operations. Canonical JSON is 12.34 MB; gzip is 2.51 MB. The previous h=23 compile completed in about 93 seconds. A new run was budgeted at under 15 minutes, under 1 GiB peak RSS, and under 20 MiB temporary disk. The process was bounded by a 30-minute timeout.

FAST block inspection built only the graph/block table: 1.34 s and 203,976 KiB peak RSS. FAST GF(2), reverse-cone, frame-rank, gzip-header, operation-order, missing-copy/clear, and missing-raise checks passed in 0.03 s (26,300 KiB peak RSS). The block check found FSa in group 1908 and Y2 in group 1929; Y2's coefficient is `0b110`, while the block exports only Y2048 with coefficient `0b111`.

## Device snapshot and decision

Immediately before FOCUSED, Android/Termux reported 3,547,932 KiB available RAM (about 3.38 GiB) and 37,926,468 KiB free disk (about 36.2 GiB). One compiler process ran. No address-space limit was applied: a prior Termux `prlimit` launch failed before Python startup and spawned a recursive `crash_dump64` chain. The 30-minute wall timeout remained active.

The available RAM was several times the conservative 1 GiB estimate; disk was ample for the frozen word, hash receipt, and raw trace. The run was safe to proceed.

## FOCUSED result

The single continuation compile returned after 89.21 s with 286,532 KiB compile-process peak RSS. The runner wrote the canonical/gzip hash receipt and raw compiler trace before detailed trace analysis. Available disk after the run was about 36.0 GiB. The serialized word matched the canonical baseline exactly and the gzip matched once the frozen filename metadata was reproduced.

A postprocess assertion initially misread the two raises around an XOR as both belonging to the same slot. The assertion was corrected and the trace was completed from the saved raw trace and hash-matching frozen word without another compile. The postprocess recovery's highest recorded RSS was 473,856 KiB. `runs/attempt-01/` preserves the earlier `BLOCKED_AFTER_WORD_EMISSION` record; `runs/attempt-02/POSTPROCESS_RECOVERY.json` records this non-compile recovery.

`make verify`, h=25 compilation, large CRT regeneration, and full physical-word replay were not run. The compiler's dirty-basis self-replay was also disabled (`dirty=False`).
