# Two source-typed architectures

Both options start from nonnegative integer operands written in radix `β=2^b`:

```text
x = sum(i=0..n-1) a[i] β^i,   y = sum(j=0..n-1) b[j] β^j,
0 <= a[i], b[j] < β.
Conv_n(a,b)[k] = sum(i+j=k) a[i] b[j],   0 <= k < 2n-1.
```

The desired integer output is obtained from the coefficient vector by the ordinary radix-`β` carry recurrence. This makes coefficient bounds and output recovery part of the type.

## A. Finite-field NTT with exact CRT — selected for the pilot

For `L` a power of two with `L >= 2n-1`, take pairwise distinct primes `p_1,...,p_r` with `L | p_j-1`, and primitive `L`th roots `ω_j` in each `F_{p_j}`. Encode each input separately by its padded evaluations:

```text
E^A_{n,j}(a)[t] = sum(i=0..n-1) (a[i] mod p_j) ω_j^(it),  0 <= t < L,
E^B_{n,j}(b)[t] = sum(i=0..n-1) (b[i] mod p_j) ω_j^(it).
```

The smaller-operation network has type

```text
P_n : (product_j F_{p_j}^L) x (product_j F_{p_j}^L) -> product_j F_{p_j}^L,
P_n(A,B)[j,t] = A[j,t] B[j,t].
```

Decoder `D_n` applies the inverse NTT, reconstructs each coefficient by CRT in `[0,P)`, where `P=product_j p_j`, and then carries in radix `β`. If `P > n(β-1)^2`, every coefficient is recovered as an integer. The source type is a pair of `n`-digit radix-`β` vectors; the convolution output type is `Z^(2n-1)` with the stated coefficient bound. For the integer-product interface, the final carry stream is a canonical radix-`β` representation of `xy`.

This is a real algebraic representation change: the child gates are modular products of `w=ceil(log2(max p_j))`-bit residues, not the original full-width product. Their width is smaller than the `N`-bit parent for sufficiently large `N`, but it is larger than the input digits in the `n=2` pilot. Exactness is independent of numerical precision. Moduli are separate coefficient rings; no map identifies signed dyadics or `F_2` with these fields.

For signed integer inputs, run the same map on magnitudes and apply the product sign after carry recovery; this adds linear sign handling and does not change the convolution type.

Cheapest fatal tests: use `L < 2n-1` and exhibit a wrapped coefficient; use `P <= n(β-1)^2` and exhibit two coefficient vectors with the same CRT residue; or omit the coefficient bound and show a single modulus aliases a coefficient. All three are direct checks of the proposed type, not frame-label checks.

## B. Kronecker packing into one integer product — rejected before a pilot

Let `R=2^g` with `R > n(β-1)^2`. Encode:

```text
K^A_n(a) = sum(i=0..n-1) a[i] R^i,
K^B_n(b) = sum(j=0..n-1) b[j] R^j.
```

One ordinary integer multiplication gives

```text
K^A_n(a) K^B_n(b) = sum(k=0..2n-2) Conv_n(a,b)[k] R^k.
```

Since each coefficient is less than `R`, base-`R` extraction is an exact decoder. The maps are typed and the identity is exact, but `P_n` is one integer multiplication on packed operands of up to `ng` bits. It is the full multiplication problem embedded in a larger call, so it fails the non-circular smaller-operation requirement. For `n=2`, `β=4`, the input `15=3+3·4` is packed as `99=3+3·32` with `g=5`; the child is a 7-bit multiplication for a 4-bit input. Larger `N` has the same width expansion. The cheap fatal test is this child-width comparison; no recursive-cost search is warranted.

## Selection

The NTT/CRT route is selected because it passes the semantic gate and has genuinely smaller child widths at large input sizes. It is classical NTT/CRT architecture and overlaps the transform/convolution purpose already present in Section 06 of the pinned manuscript. The pilot can establish an exact source-typed instance and price its children; it cannot claim novelty or a new `κ` from restating that method.
