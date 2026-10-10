# Search grammars and pinned context

## Source contract

The immutable starting point is the fork snapshot [`0605a24a28836168ad29d6239b46064b892298fc`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/0605a24a28836168ad29d6239b46064b892298fc). The original multiplication source is pinned at [`adc7f1241b42e322a6451854ab7e4b4c146bf78a`](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a).

The source and physical obstacles from the preceding fork research are recorded at immutable snapshots: [Issue 27 result](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/91661785056376ecafebf8e00b0ebd7226cd23a0), [Issue 28 result](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/c4c9c6461d86b84774b9a8cd0b5907549275c740), [Issue 29 result](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/69e77d2d32b06b9f5b7e2d27d5946535d4d6f4f5), [Issue 30 result](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/78f4a20fa1be5fb7366ae93c808a93d191491472), [Issue 35 result](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/f6618ae74e6e2ad4c2583c915f967809887d4794), [Issue 36 result](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/6a9cdb35d76d73e3f2367b494366c230b78a2ce6), [Issue 37 result](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/03c030320085b211d9b5f2c5d94715db4547136b), [Issue 38 result](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/b1741e7dd6e6b13f1b329d34415ee1e8cc1cc467), and [Issue 39 result](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/98e8fe60598592d1550e596c22da36b8d0dba0da). The corresponding discussion records are [Issue 27](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/27), [Issue 28](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/28), [Issue 29](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/29), [Issue 30](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/30), [Issue 35](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/35), [Issue 36](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/36), [Issue 37](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/37), [Issue 38](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/38), and [Issue 39](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/39).

Those bounded results warn against treating a local identity as a new multiplication algorithm: a zeta-derived center matched an existing coordinate-star construction; a signed shear passed rational algebra but failed its physical F₂ address cap; a small address lift did not preserve the pinned source type; a five-pair local operator lacked an outer multiplication decoder; and later frame/packing work exposed source-role aliasing, illegal paid edges, or no complete paid-child deletion. They are scoped results, not impossibility theorems. This lane therefore searches the ordinary scalar multiplication tensor directly, without assuming a port count, Walsh/zeta transform, star, or signed-network motif.

Modern upstream comparisons are pinned to the task's cited heads: [PR 203](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/203) at [`d2873e20750d0949d2ad75cbc4cd82b5b1a74e84`](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/d2873e20750d0949d2ad75cbc4cd82b5b1a74e84), [PR 231](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/231) at [`3c11e696a2fb2c454585d72710de27cd6bd3be68`](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/3c11e696a2fb2c454585d72710de27cd6bd3be68), [PR 244](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/244) at [`a568d94f941929232ab393c7d33dc5a30e017892`](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/a568d94f941929232ab393c7d33dc5a30e017892), and [PR 246](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/246) at [`b21f0963da45e7728a47ed1138d438141ef3c1db`](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/b21f0963da45e7728a47ed1138d438141ef3c1db). PR 203 supplies structural ceilings, PR 231 a scoped parity obstruction, PR 244 a concrete retiming that removes whole recursive calls while retaining its other charges, and PR 246 a globally priced rank-three bank target. These are comparison points for what counts as a paid change, not candidate generators for this search.

## Grammar A: bounded bilinear tensor decompositions (selected)

### Typed source and output

For a limb base `B = 2^n`, the two independent source roles are

`A = (a0, a1)` and `Bsrc = (b0, b1)`, with each digit in `[0, B-1]`.

The exact output type is the raw convolution triple

`C = (c0, c1, c2) = (a0*b0, a0*b1 + a1*b0, a1*b1)`.

Then `(a0 + B*a1)*(b0 + B*b1) = c0 + B*c1 + B^2*c2`. This equality connects every candidate to actual integer multiplication; ordinary carry normalization is downstream and common to every candidate. The polynomial identity is over `Z`, and the tensor search solves its coefficients over `Q` before checking the scaled integer identity exactly.

### Finite operator grammar

The allowed input forms are primitive, sign-normalized pairs `(p,q)` with `max(|p|,|q|) <= 2`. There are exactly eight:

`(1,0), (0,1), (1,1), (1,-1), (1,2), (1,-2), (2,1), (2,-1)`.

A product term is `(p*a0+q*a1)*(r*b0+s*b1)`. There are 64 typed A-by-B terms. A candidate is an unordered set of three distinct terms. For each output coefficient, its decoder is a rational linear combination of those three child products. The common denominator must be 1 or 2. A denominator 2 is admitted only when the exact tensor equation has numerator `2*C`; that proves every integer decoder result is integral for all integer inputs. No nonlinear decoder, source-free identity, dirty scratch, or full multiplication inside the decoder is permitted.

The exhaustive search space is `choose(64,3) = 41,664` candidate term sets. The search is deterministic and has no random seed. The full setting is in [`search_config.json`](search_config.json).

### Exact checks, symmetries, and cost features

The checker tests every coefficient of the four-variable bilinear tensor. It also evaluates every accepted candidate on all two-bit-limb inputs. The denominator-2 cases are integer-valid by the exact coefficient equation; this does not establish an F₂ algorithm because division by 2 is not defined in F₂.

Term order, per-form scalar sign, A/B exchange, and simultaneous reversal of both limb pairs with endpoint-output reversal are quotiented. General rational changes of basis are not treated as free: they can change source formation, operand bounds, division, and decoder costs. Each quotient representative retains its actual forms and decoder.

Cost features are three recursive child calls, each child operand's exact maximum magnitude on the digit box, magnitude bit width, variable-sign handling, form-generation additions/scales, output combination additions/scales, and exact divisions. This is a local scalar screen, not a physical implementation or a `kappa` certificate.

### Expressivity boundary

This grammar finds rank-three bilinear algorithms whose three child calls multiply bounded integer linear forms in two-limb sources. It excludes nonlinear source encoders, carry-aware Boolean circuits, more than three products, coefficients outside this projective bound, and decoders with denominators above 2. It proves no negative result outside that envelope.

## Grammar B: source-typed reversible bit circuits (designed, not run)

This is a distinct finite grammar for exact multiplication of two `w`-bit nonnegative integers to a `2w`-bit output. For one bounded instance choose `w=2`, a maximum of three strictly smaller child multiplication calls, at most 24 reversible word/bit gates, and at most four clean scratch bits.

The state has separate A-source and B-source registers, a zero-initialized output register, and clean scratch. The gate vocabulary is bit permutation, NOT, CNOT/XOR, and reversible modular addition/subtraction on same-role words. A multiplication call may read one A-tagged value and one B-tagged value only when both widths are strictly below `w`; its result is added to a separate AB-tagged accumulator. Decoder gates may read AB-tagged products but may not read original A/B registers, which prevents hiding a complete multiplication in the decoder. Scratch must be restored to zero; dirty scratch is not free. A candidate passes only if its complete reversible circuit maps every `(A,B,0,0)` to `(A,B,A*B,0)` exactly. The finite Boolean truth table is over `F2`, with carries represented by the circuit rather than inferred from a rational identity.

For fixed `w`, wire count, gate limit `L`, and the finite gate set, exhaustive sequence enumeration is bounded by `sum_{j=0}^L |G(w)|^j`; a SAT encoding could enumerate the same finite grammar. The cost record would include child widths, gate counts, scratch/restoration, bit routing, and output precision. This grammar can express nonlinear bit encoders and decoder logic that Grammar A cannot, but says nothing by itself about unbounded integer inputs or a uniform recursive family. Its finite circuit count and implementation work are materially larger, so Grammar A was selected for the first FAST milestone.

## AI and source notices

Codex provided substantive assistance by designing and implementing the exhaustive enumerator/checker and drafting the research record. The pinned upstream sources are linked above; no source code, license, or NOTICE text was copied or modified.
