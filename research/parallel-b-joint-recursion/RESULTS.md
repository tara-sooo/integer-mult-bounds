# Results

## `NO_PAID_JOINT_GAIN`

**FAST result:** a typed shared-left child can return two exact full products, but in the field-bilinear model its rank is exactly the sum of the two ordinary convolution ranks. It saves no recursive scalar multiplication leaf. The only observed small saving is one shared linear evaluation (and, under a forced-private-copy ABI, one shared input record per Toom point) against an intentionally unoptimized baseline; a fair baseline can cache the immutable value and record too. The competing guarded-packing idea replaces two children with a roughly triple-width child and fails the same-model scaling screen for schoolbook, Karatsuba/Toom, and regular near-linear costs.

The result is deliberately scoped. It is not a no-go for nonlinear bit-level recursion, altered multiplication reductions, or a new source-typed Section 4 construction.

## Verification record

- **PROVED:** for all `n`, the output flattening rank of `J_n(A;B,C)=(AB,AC)` is `4n-2`; any field-bilinear algorithm uses at least that many scalar products. Two Toom products attain the bound when the field supports the required interpolation points.
- **EXACT SMALL:** at `n=2`, Karatsuba reconstruction equals the full coefficient outputs, the flattening matrix has rank `6`, the joint schedule uses six multiplications and seven linear gates, and the deliberately wrong cross-output reconstruction fails. The checker also verifies rank `10` at `n=3`.
- **MODELLED:** the complete Toom recurrences charge child multiplicity, all evaluation/interpolation, coefficient growth, copies, sequential data movement, two output arrays, carry normalization, cleanup, and workspace. Under the stated fixed-`r` model, the multiplication leaves are exactly twice the one-product count.
- **NOT RUN:** no FOCUSED source-frame pilot, full Section 4 child replay, bit/complex supplier, all-size fixed-tape proof, or `make verify`. The coefficient type does not satisfy the original Section 4 interface, and the exact rank result already rejects the proposed leaf-saving mechanism.

Verification phases: **FAST PASS** (symbolic proof plus exact small checker); **FOCUSED NOT RUN**; **FULL NOT RUN**.

The parent terms charge all listed work, but their implementation-dependent tape/movement constants are not numerically compared. The proved negative claim is about recursive multiplication leaves; a future fixed-tape implementation could still compare data-movement constants for this familiar common-input reuse.

## Commands and observed output

```text
python3 research/parallel-b-joint-recursion/check_joint_tensor.py
PASS: n=2 output-flattening rank 6; n=3 rank 10
PASS: exact n=2 Karatsuba reconstruction; wrong cross-output control rejected
PASS: n=2 costs: joint 6 multiplications/7 linear gates; naive pair 6/8; cached baseline 6/7
PASS: n=2 Toom child leaves: joint 6; expanded independent baseline 6
```

The final timed replay in the dedicated worktree took **0.12 s** and peaked at **13,408 KB RSS** (including Python startup). The script uses only the standard library and deterministic rational row reduction; no profile data was generated.

## Known method comparison and next discriminating question

Candidate A is shared evaluation inside classical Toom recursion. Candidate B is guarded digit packing. Neither is a novel cheap recursive multiplier. Karatsuba, Toom–Cook, FFT/NTT, middle product, and streaming carry are distinguished in `COMPARISON.md`; none supplies a missing paid-child reduction for this type.

The next mathematically discriminating step would need a joint child whose complete output tensor has fewer paid recursive products than the typed baseline **and** whose interface composes with the source's full-array role/frame and arbitrary-dirty-state contracts. This report identifies no such child, so no FOCUSED or integration phase is justified.

This checkpoint adds only research documentation and the exact checker under the fork's Apache-2.0 license. It includes substantial OpenAI Codex assistance; no independent peer review or κ claim is asserted.
