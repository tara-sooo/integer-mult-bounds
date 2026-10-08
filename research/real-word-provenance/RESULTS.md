# Results

**FOCUSED result: `PASS`.** One h=23 compile on the isolated PR 63 compiler copy reproduced the pinned canonical word exactly. The saved trace confirms that `Y2(2044)` has no dedicated logical output slot, is materialized temporarily in physical slot 17581, and is a virtual linear form at the consumer block exit.

## Word identity and compiler checks

- Canonical JSON SHA-256: `640696dd7cd893add9d6e12d0d587956fecf113b2eff8c29547b82e5a6f3c0ad`; byte-for-byte equality with the frozen word: **PASS**.
- Gzip SHA-256 with the pinned output filename and settings: `1a57c143380a063211653f1f35e7cc9710539523b0b34c90f354a0425c34bd59`; exact equality: **PASS**. The first in-memory `BytesIO` wrapper omitted the gzip FNAME field; its different digest is retained in `WORD_HASH_RECEIPT.json`. Its DEFLATE stream and trailer equal the frozen file. Reproducing the frozen output name yields the exact gzip hash.
- Roles `27,918`, matched uses `37,025`, regions `52,473`, multi-node regions `10,350`, XORs `149,172`, clearing XORs `1,612`, rank mass `642,620`, and the complete histogram all match the PR 63 receipt.
- The word has `444,594` frame events and the same `621,482` expanded operation count recorded by the pinned receipt.

## Logical and physical result

`FSa(2039)` is in producer group 1908. Its block inputs are `1958, 1959, 1975, 1996`, and its coefficient mask is `0b1111`. The selected compiler use is index 455. The producer value slot, use carrier, and consumer input are all physical slot 17581. The use was not selected as a matched continuation (`matched=false`); it is passed directly to the consumer input.

`Y2(2044)` is in consumer group 1929 with inputs `[1952, 2020, 2039]`. Its coefficient mask is `0b110`, so its exact linear form is `2020 XOR 2039`. Its only graph child is `2048` at operand 1 in the same block. The block exports only `2048`, with coefficient mask `0b111`; there is no compiler-use entry or dedicated `value_slots[2044]` entry for `Y2`.

The actual consumer basis operations are `ops[75969..75972]`:

1. `ops[75969] = (21455, 17581, 1929)` starts the joint output-basis transform.
2. `ops[75970] = (17581, 1078, 1929)` changes slot 17581 from `FSa` to `Y2`.
3. `ops[75971] = (21455, 1078, 1929)` materializes block output `Y2048` in slot 21455.
4. `ops[75972] = (17581, 21455, 1929)` consumes the temporary `Y2` form and restores slot 17581 to input value `1952`.

At block exit, `Y2 = slot 21455 XOR slot 17581 = Y2048 XOR 1952`. Slot 17581 is retired at this boundary; this linear expression is not a free stored value. Recreating or forwarding `Y2` would require physical XOR work and an appropriate role/frame transition.

The producer-to-use cone is `ops[55648]`, `ops[55650]`, and `ops[55655]`. The consumer linear-form cone is `ops[75970]` and `ops[75972]`. Three additional `duplicate_use_copy` operations, `ops[75973..75975]`, copy `Y2048` into its other outgoing compiler-use slots. They are retained in the trace as block work and are not charged to `FSa -> Y2`.

## Exact frame ranks and limits

The selected FSa carrier enters group 1929 at `events[226456] = (17581, 1908, 1929)`. Exact rational projector subtraction gives rank 4 over `Q^23`; under the inherited rank-one h=25 triple factor the corresponding per-triple-context rank is also 4 over `Q^575`. The other `Y2` input arrives at `events[226455] = (1078, 1920, 1929)`, also rank 4. The materialization and restoration XOR raises are all same-frame events of rank 0. These ranks were recomputed from the actual old/new frame groups; Issue 16's `(4,4,0)` was not reused.

The FSa producer input raises have exact ranks `2, 4, 6, 4`; together with its three same-frame producer operations and the two target input raises, the selected linear support cone's gross event-rank sum is 24. This is a support-cone ledger, not a charge assigned to the logical use. Shared basis operations, output copies, role restoration, wrapper multiplicity, and child selection remain unallocated. No Section 4 pivot or `Swap` child is identified, so this trace does not support a new `κ` claim.

## Verification scope and resources

- FAST block diagnosis: **PASS**, build only; 1.34 s, peak RSS 203,976 KiB.
- FAST linear/replay/negative-control self-checks: **PASS**; 0.03 s, peak RSS 26,300 KiB.
- FOCUSED h=23 compile and trace: **PASS**; compile 89.21 s, compiler peak RSS 286,532 KiB. Saved-word trace processing took about 0.74 s. Highest recorded process RSS across the compile and recovery postprocessor was 473,856 KiB.
- Free disk was about 36.2 GiB before and 36.0 GiB after the run.
- FULL: **NOT RUN**. `make verify`, h=25 compilation, large CRT regeneration, and full physical-word replay were not run.

The previous `BLOCKED_AFTER_WORD_EMISSION` record remains under `runs/attempt-01/`. This continuation saved the word hashes and raw trace before analysis. A trace validator initially misread the two raise events around one XOR; the fix was verified by resuming from the saved word, without another compiler call. Details are in `runs/attempt-02/POSTPROCESS_RECOVERY.json`.
