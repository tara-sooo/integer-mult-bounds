# FAST preflight

**Initial FAST decision: GO with a planned 1.5 GiB address-space limit and a 30 minute wall timeout.** The execution record below explains why Termux could not apply that memory limit and how the single compile was then gated. FAST did not compile an axis.

## Pinned inputs and path

- PR 63 construction commit: `aa7701b68540b7863d3b66a414e4319915d6282d` ([redirected PR](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/63), [redirected commit](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/aa7701b68540b7863d3b66a414e4319915d6282d)).
- Issue 18's source/use/block/carrier/slot/event distinctions and fixture-only result were read at fork commit `54e49f0301e09c08d2670a63af6fb15e72b9a146` ([redirected Issue 18](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/18)).
- The immutable h=23 baseline is `research/rank-pair/frame-word-23.json.gz`: gzip SHA-256 `1a57c143380a063211653f1f35e7cc9710539523b0b34c90f354a0425c34bd59`, canonical JSON SHA-256 `640696dd7cd893add9d6e12d0d587956fecf113b2eff8c29547b82e5a6f3c0ad`.
- The graph source hash is `3d47e89d2649c90800a276bdd0480131def50e0bdf92c122a19494b55bf17420`; frozen compiler hash is `9984aaccf880e4840402322d76678bfddb33ce7e494af78430a43429f51b85fd`. Exact copies and dependency hashes are in `pinned/SOURCE_MANIFEST.json`.

## Expected work

The frozen receipt reports 52,473 blocks, 37,025 matched uses, 27,918 roles, 149,172 elementary XORs, rank mass 642,620, and a 621,482-operation serialized word. The compressed word is 2.51 MB and canonical JSON is 12.34 MB. The compiler's stored receipt does not retain a per-axis compile duration or peak memory.

The FOCUSED runner calls the same h=23 graph, matcher, rank-first reclamation and word emitter once with `dirty=False`. This still emits the complete physical word. It skips the compiler's internal arbitrary-dirty-basis replay, which would apply the 621,482-operation word to 31,460 basis vectors in each of two orientations (about 39 billion Python loop iterations), and skips the independent full-word replay. No h=25, CRT, profile, or all-size regeneration is needed for the requested hash and local trace.

## Device snapshot before execution

- Termux / Android arm64; 8 logical CPUs; one compiler process only.
- `/proc/meminfo`: 3,572,836 KiB available (about 3.41 GiB) out of 11,544,356 KiB total.
- Workspace filesystem: 36.47 GiB available.
- Battery: 57%, charging; USB power online.
- No concurrent rank-pair compiler process was visible at the snapshot.

## Estimate and guard

- Expected peak RSS: below 1 GiB, from the 52k-block graph and the saved word's 12.34 MB canonical size; conservative process address-space ceiling: 1.5 GiB.
- Expected wall time: 2–15 minutes. Matching is the main uncertainty; the frozen receipt does not include elapsed time. Hard stop at 30 minutes, then SIGKILL 30 seconds after SIGTERM.
- Additional temporary disk: under 20 MiB (expected word is compared in memory); over 36 GiB is free.
- The attempt marker is written before graph construction. If the process hits the cap, times out, or reports drift, no retry is permitted in this milestone.

The remaining Android memory is more than 2 GiB after the address-space ceiling, storage is ample, and the device is charging. This bounded single-axis run is within the available resource envelope.

## Execution and outcome

The first guarded launch used `prlimit --as=1610612736` around Python. On this Termux Android host, that process stayed inside `prlimit` and produced a recursive `crash_dump64` child chain before Python started. The process group was killed. `FOCUSED_STARTED.json` was absent, so no compiler call occurred in that launch.

After memory recovered, the FAST gate was repeated: immediately before the sole compiler run, `/proc/meminfo` reported 2,785,176 KiB available (2.66 GiB), disk remained 36 GiB free, and the battery was charging. The run used a 30 minute timeout and no address-space limit because `prlimit` was incompatible with this host. Expected RSS remained below 1 GiB. The h=23 compiler returned after building 52,473 regions and matching 37,025 uses; progress reached step 50,000 at 92.374 seconds. The runner's whole-axis receipt and histogram assertions passed.

Trace post-processing then failed because the captured `target_value_slot` for node 2044 was `None`, and the original cone walker attempted `1 << None`. The compiler had already emitted and canonicalized its word in memory, and computed raw and gzip digests, but the exception happened before the runner compared or persisted either digest. Peak RSS and the digest values were not retained. The single compile is not repeated. Therefore the pinned word match is **unverified**, and no operation or event IDs can be reported from this run.

The isolated runner now treats a missing output slot as unresolved and writes a word-hash receipt before building trace relations. Those code changes were checked by the fixture self-check only; the h=23 compiler was not run again.
