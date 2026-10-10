# Issue 42, lane C: milestone 2

**Result: `BOUNDED_NEW_GRAMMAR_OBSTRUCTION`.** The only exact low-cost operator at the tested two-bit parent is the known bitwise Karatsuba product triple. No exact two-child heterogeneous operator survived. The simple XOR-half recursion fails at half-width 3. These are bounded results, not an impossibility result for richer state or other widths.

The work continues on branch `issue-42-exact-operator-synthesis`, based on fork commit [`0605a24a28836168ad29d6239b46064b892298fc`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/0605a24a28836168ad29d6239b46064b892298fc). The first-round `KNOWN_ISOMORPHISM_ONLY` result and its files are unchanged; the first-round snapshot is [`a8cea8b0a139aef76f9bdab73125f9fdf0abc69b`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/a8cea8b0a139aef76f9bdab73125f9fdf0abc69b). Issue reference: [Issue 42](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/42).

## Grammar comparison and choice

The unexecuted Grammar B in [`GRAMMAR.md`](GRAMMAR.md) is a reversible gate-sequence grammar: at width `w=2` it allows at most three strictly smaller child calls, 24 reversible gates, and four clean scratch bits. It preserves the two source registers, restricts child-role tags, and prevents the decoder from reading original sources. This represents carry-producing reversible implementations, but an exhaustive gate-sequence search is much larger than needed for a first bounded check.

This pilot instead uses a typed **functional encoder–child–decoder grammar**. Each independent two-bit source can be mapped by any truth table to a child operand. Children may have different types, and the decoder may be any exact function of child products. The decoder cannot read either original source. There is no borrowed scratch or hidden source-dependent multiplication in the decoder. Unlike Grammar B, encoders need not be reversible and may be arbitrary nonlinear functions; unlike the first-round bilinear grammar, the child forms need not be linear and the decoder need not be rational-linear.

We selected this grammar because exact candidate existence reduces to a small separating-signature problem before constructing any decoder. At the root, child types `(p,q)` must satisfy `p+q<4`; we allow `(1,1)`, `(1,2)`, and `(2,1)`. A bounded child of type `(p,q)` is charged `p*q` elementary `1×1` products, matching its direct schoolbook expansion. The baseline for a two-bit-by-two-bit product is four such products. We searched only profiles costing at most three, which is the first budget that could remove one whole elementary child product. Encoding and decoding work is charged separately below.

## Exact finite search

The source roles are independent `A,B ∈ {0,1,2,3}` and the required output is the ordinary integer `A*B`, not a carryless product. Its exact image is `{0,1,2,3,4,6,9}`, of size seven. Therefore output-state cardinality alone does **not** rule out three one-bit children or the mixed `(1,1)+(1,2)` profile: each can expose up to eight signatures. The search uses all 96 pairs of source cases whose required products differ. A set of child encoders is valid exactly when every one of those pairs differs in at least one child output; this condition is necessary and sufficient for some source-free decoder to exist.

The deterministic search checked all 40 ordered child-type profiles with zero to three calls. Of these, 10 have cost at most three; five fail the exact child-output cardinality bound. The remaining profiles reduce by child permutation and global `A/B` exchange to two searches:

- Three `(1,1)` children: each source has 16 Boolean functions, giving 256 possible child terms. All `C(258,3) = 2,829,056` unordered triples, with repetition, were checked.
- One `(1,1)` and one `(1,2)` child: 256 choices for the first term and 4,096 for the second, or 1,048,576 pairs. The `(1,1)+(2,1)` profile is covered by exchanging source roles.

That is 3,877,632 encoder sets checked against a configured ceiling of 4,000,000. Decoder tables were not enumerated: for a fixed encoder set a decoder exists iff different required products have different child-output signatures, and its values on unused signatures do not affect correctness. The full raw three-child encoder-plus-decoder table space would contain `2^56` assignments, so this exact semantic test avoids that enumeration. The seed is `null`; the exploration is exhaustive within the stated quotient and has no random choices. Run it with:

```sh
python3 research/parallel-c-exact-synthesis/milestone2_search.py
```

The exact parameters are in [`milestone2_config.json`](milestone2_config.json), the generated counts and truth tables are in [`milestone2_receipt.json`](milestone2_receipt.json), and the concise run output is [`milestone2.log`](milestone2.log).

## Exact result and known equivalence

There is exactly one valid three-child encoder set, and it is one class after child permutation and global source exchange. Its three terms are:

`x = (a0 XOR a1) * (b0 XOR b1)`, `l = a0*b0`, and `h = a1*b1`.

Truth-table function IDs `6`, `10`, and `12` in the receipt are respectively `[0,1,1,0]` (XOR), `[0,1,0,1]` (low bit), and `[0,0,1,1]` (high bit), for both independent source roles. This is the standard low/high/XOR Karatsuba triple, not a new multiplication reduction. The heterogeneous two-child search found zero exact encoder pairs.

For the three child results define

`q = x XOR l XOR h`, `c = l AND h AND NOT x`, and `P = l + 2q + 4c + 4h`.

For one-bit source halves, `q` is the parity of the two cross products. Both cross products are one exactly when `l=h=1` and `x=0`, so `c` records their carry. Thus `P=a*b` for every one of the 16 source pairs. The script replays and records every row and checks this integer formula exactly. The decoder table in the receipt is the corresponding source-free four-bit output decoder.

Negative controls include source-role aliasing (`1*2=2`, but the aliased square gives `1`), a three-partial-product truncation whose signature is the same for `(0,0)` and `(2,2)` although the products are `0` and `4`, and the carryless-only decode of `(3,3)` which gives `5` instead of `9`. A restricted `{0,1,2}` source domain and the one-bit multiplier are also sanity controls: their smaller product images correctly pass the cardinality bound rather than being rejected by it.

## Paid-cost screen and extension limit

At this finite size, the candidate changes four elementary product children to three, so it removes one paid `1×1` child. It adds two source XORs. One exact decoder implementation uses three XORs, three ANDs, and one NOT. With a uniform two-input XOR/AND/NOT gate count, the schoolbook reference is four partial-product ANDs plus two XORs and two carry ANDs: eight gates. The stated Karatsuba decoder and encoders use six ANDs, five XORs, and one NOT: twelve gates. This is an explicit correct decoder, not a proof of the minimum decoder size. It shows that the local child reduction alone is not a total data-gate saving. No physical cost or `κ` improvement is claimed.

The necessary all-size condition for this grammar would be a uniform family of independent source encoders `E_i^A,E_i^B`, strictly smaller child types, and a decoder that sees only the child products, with

`D_w((E_i^A(A) * E_i^B(B))_i) = A*B`

for every width and every input, while the fully charged child, encoding, decoding, carry, storage, and restoration cost beats the chosen baseline. The finite truth table does not prove such a family. In particular, the direct XOR-half extrapolation fails: splitting six-bit operands into three-bit halves, the inputs `(A,B)=(1,43)` and `(3,25)` both yield child signature `(6,3,0)` from `(XOR-half product, low product, high product)`, but their products are `43` and `75`. The checker verifies all 4,096 six-bit input pairs and records this collision. A decoder using only those three child results therefore cannot extend this recipe to all widths.

The next proof would need a different uniform typed family with enough charged carry/overlap state to distinguish such cases, an exact decoder identity for all inputs, strict child-size reduction, and a complete recurrence comparison including all source formation and output logic. The current result rules out only a novel lower-cost operator in the bounded grammar and range above; it does not rule out grammars that expose additional correlated state or carry information.
