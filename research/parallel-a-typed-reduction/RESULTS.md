# Results

## Primary status: `KNOWN_EQUIVALENCE_ONLY`

The finite-field NTT/CRT path is an exact, non-circular source-typed reduction for bounded radix-digit convolution, and its entire coefficient tensor is proved by the inverse-DFT identity and the CRT coefficient bound. The implementation is standard NTT/CRT arithmetic, however, and does not establish a new multiplication architecture or a `κ` improvement. The alternative Kronecker map is an exact convolution identity but embeds one larger full integer multiplication and fails the non-circular child requirement.

## What passed

- **FAST exact proof:** for `n=2`, `β=4`, `L=4`, primes 17 and 97, roots 4 and 22, and CRT modulus 1649, all allowed coefficients are recovered exactly.
- **Runtime:** the checked receipt records 11.102 ms on Python 3.14.6.
- **Checker SHA-256:** `17c6b0388c6507e4750ca912857ffd1df39ac6ecc78907f394a42ff4d6022a54`.
- **Complete tensor check:** all four input basis-pair products recover the corresponding coefficient basis vector.
- **Exhaustive pilot:** all 256 pairs of two-digit input vectors in `{0,1,2,3}^2` recover the full convolution and integer product.
- **Adverse controls:** the single-prime decoder maps the true middle coefficient 18 to 1 and returns the wrong product; omitting carry cannot return canonical radix-four digits. The Kronecker example requires a 7-bit child multiplication for a 4-bit source operand.
- **Cost gate:** the NTT pays `Theta(N)` recursive modular products of `O(log N)` bits under its favorable constant-prime-width assumption, plus transform, CRT, carry, storage, and prime/root setup. This beats the schoolbook block-product count but is asymptotically worse than the pinned fork bound even before the unresolved prime/root generation term.

## What did not pass or was not run

- **Novelty gate:** this is the classical finite-field transform and CRT reconstruction pattern. Section 06 already supplies a transform/convolution architecture, though with a different synthetic ring and exact product subroutine.
- **Uniform all-size generator:** no low-overhead prime/root generator was constructed or timed; `G` remains explicit in the cost recurrence.
- **Source-supplier bridge:** no Section 03/04 physical roles, dirty-state restoration, bit/complex suppliers, or compatible recursive recurrence were produced.
- **FOCUSED and FULL:** not run because the exact known transform has no paid advantage over the current bound. Full repository verification and `make verify` were not run.

The result is scoped to these two arithmetic architectures. It is not a no-go theorem for exact transforms, modular methods, or a different source-typed multiplier. A future positive candidate must remove a real recursive multiplication charge after transform, prime/root setup, CRT, carries, copying, memory scans, and cleanup are paid.

## Reproduction

From the repository root, run:

```sh
python3 -B research/parallel-a-typed-reduction/check_exact.py
```

The deterministic receipt is `receipt.json`. The new checker is standard-library Python and was prepared with substantial OpenAI Codex assistance; it is not independently reviewed or formally verified.
