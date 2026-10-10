# Paid-cost screen

## What is counted

The screen prices the actual source-derived recursive operands, not tensor rank alone. Let each input limb have `n` bits, `B=2^n`, and digits in `[0,B-1]`. For a form `l=(p,q)`, the exact maximum magnitude on this digit box is

`M(l) = max(sum(max(p_i,0)), sum(max(-p_i,0))) * (B-1)`.

Its child magnitude width is `ceil(log2(M(l)+1))`; a variable-sign form additionally needs signed handling before a nonnegative recursive multiplier can consume it. The values below are parameterized in `n`; the receipt gives exact bounds for the concrete `n=2, B=4` replay.

| Form | Maximum magnitude | Child magnitude width for `n >= 2` | Sign |
|---|---:|---:|---|
| `a0` or `a1` | `B-1` | `n` | fixed nonnegative |
| `a0+a1` | `2(B-1)` | `n+1` | fixed nonnegative |
| `a0-a1` | `B-1` | `n` | variable |
| `a0-2a1` or `2a0-a1` | `2(B-1)` | `n+1` | variable |
| `a0+2a1` or `2a0+a1` | `3(B-1)` | `n+2` | fixed nonnegative |

## Best local comparison found

Classical two-limb schoolbook multiplication has four `n x n` child products. Standard sum-Karatsuba has

`2 M(n,n) + M(n+1,n+1)`

and two input additions plus two middle-output subtractions. Difference-Karatsuba has

`3 M(n,n)`

on magnitudes, but its third product is formed from signed differences. The exact identity therefore changes one specific old child from `M(n+1,n+1)` to `M(n,n)`; it does not remove a product call. This operand-width change is proved by `|a0-a1|, |b0-b1| <= B-1`.

The extra charges for a positive-only recursive child are two `n`-bit input subtractions, two absolute-value/sign normalizations, one product-sign restoration, and two middle-coefficient additions/subtractions. The resulting `c1` is at most `2(B-1)^2` and needs `2n+1` output bits; endpoint coefficients are direct `2n`-bit products. Ordinary carry normalization is still required after the raw convolution output. If the child interface natively accepts signed inputs, its exact sign contract and cost must replace the wrapper charges; that interface was not established here.

This is a plausible local data-cost trade: one recursive child is narrower, while signed preprocessing and restoration are added. It is a known Karatsuba difference variant, not a newly discovered saving. Whether `M(n+1,n+1)-M(n,n)` exceeds those extra costs for the actual recursive implementation is the next test. No `kappa` claim follows from three products or from this local width comparison.

## Other discovered representatives

The seven other Toom-2 choices have at least one child wider than `n`, frequently `n+2`; some use two signed evaluations, nonunit scalar coefficients, or a decoder with exact halves. The exact per-child magnitude, sign flags, decoder constants, reduced per-output division, and required additions are in `search_receipt.json`. None has a demonstrated complete child or data-operation advantage over the difference-Karatsuba profile.

The denominator-2 identities are valid over integer inputs because the exact numerator tensor equals twice the target tensor. At the implementation level, each output decoder is reduced by common factors before charging division. A remaining exact `/2` is still an integer-side operation and is not an F₂ operation. No bit decoder was inferred from it.

## Charges still outside this FAST screen

The tensor kernel does not provide a full recursive implementation. A complete multiplier comparison must also charge:

- materializing and storing the input linear forms and child outputs, including any copies or routing required by the real recursion interface;
- nonunit constant scales and all output additions at their actual word precision;
- signed absolute-value and product-sign logic for every recursive level using differences;
- exact divisions where a reduced output decoder still has denominator 2;
- output carry propagation from raw convolution coefficients;
- source preservation and scratch restoration if embedded in a reversible physical/data-frame construction;
- an independent F₂/bit implementation, precision/complex supplier, and uniform recursion theorem if those are required by the chosen multiplication bound.

These items are not assigned zero cost. They are unimplemented or unpriced interfaces, so this artifact is a local cost screen only. The contrast is the pinned upstream [PR 244 retiming](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/244), which reports 355 whole recursive calls removed per local helper while retaining scalar work, restoration, endpoints, and other full-model charges; and [PR 246](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/246), whose rank-three bank target is supported by its whole-bank and bit-bound ledger. The exact paid mechanism in those sources is not comparable to a scalar rank-three tensor count.

## Smallest discriminating follow-up

Implement one parameterized signed-child adapter and compare, for each `n`, the actual paid cost of `M(n+1,n+1)` against `M(n,n)` plus two difference formations, two absolute-value/sign normalizations, sign restoration, middle recombination, and copies. The minimal missing lemma is that this complete delta is negative uniformly over the intended recursive levels and that the existing child accepts the resulting signed/magnitude types. Then test its independent bit-side and carry behavior. Until that passes, this is a known local width trade rather than an integrated bound improvement.
