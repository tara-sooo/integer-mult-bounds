# Exact NTT/CRT identity and finite pilot

## Typed map

For the pilot, `n=2`, `β=4`, `L=4`, and the input arrays are
`a,b in {0,1,2,3}^2`. The output is the full integer coefficient vector
`Conv_2(a,b) in {0,...,18}^3`; the corresponding integer operands are
`x=a[0]+4a[1]` and `y=b[0]+4b[1]`.

Use `(p,ω)=(17,4)` and `(97,22)`. In both fields, `ω^2=-1`, so `ω` has exact order four; `4` is invertible modulo both primes. For each prime, `E^A` and `E^B` pad the two input coefficients to length four and evaluate at `1,ω,ω^2,ω^3`. `P_2` multiplies the four corresponding residues. The decoder applies the inverse length-four DFT, takes coefficients 0, 1, and 2, and uses the two residues to CRT-lift to `[0,1649)`. Since `1649 > 2·3^2=18`, every lifted coefficient is the exact integer coefficient. The last product decoder carries those coefficients in radix four.

Input ownership is explicit: the caller owns the two source digit arrays; each forward transform reads its source and writes a fresh zero-padded frequency buffer; `P_2` owns the two frequency buffers and writes a product buffer; `D_2` owns that buffer and returns the coefficient vector and carry digits. The pilot uses fresh, initialized scratch. It does not claim restoration of arbitrary dirty scratch or a reversible physical frame.

## Symbolic identity

For any selected prime `p`, an `L`th primitive root `ω`, and padded vectors, let

```text
A[t] = sum_i a[i] ω^(it),   B[t] = sum_j b[j] ω^(jt).
```

The inverse transform of their pointwise product at index `k` is

```text
L^-1 sum_t A[t] B[t] ω^(-kt)
= sum_(i,j) a[i]b[j] (L^-1 sum_t ω^((i+j-k)t)).
```

The inner sum is one when `i+j=k mod L` and zero otherwise. Thus the inverse is the cyclic convolution modulo `p`. Since `L >= 2n-1`, every sum `i+j` is in `[0,L-1]`; no coefficient wraps. The result is `Conv_n(a,b) mod p` in every field. The bound `0 <= Conv_n(a,b)[k] <= n(β-1)^2 < P` makes the CRT representative unique and equal to the integer coefficient. Finally,

```text
x y = sum(k=0..2n-2) Conv_n(a,b)[k] β^k,
```

and the ordinary carry recurrence returns its exact canonical digits. This proves the complete typed map for every allowed digit input, not only basis labels.

## Deterministic checks

`check_exact.py` verifies the roots and inverse transforms, all four coefficient basis-pair products (the complete `2 x 2 -> 3` bilinear tensor), and all `4^4=256` pairs of pilot input vectors. It also checks the Kronecker width example and two adverse decoders:

1. Keeping only modulus 17 aliases the middle coefficient `18` to `1` for `a=b=(3,3)`, producing `157` instead of the correct product `225` after carry.
2. Treating raw convolution coefficients as canonical base-four digits fails because coefficient 18 is outside the digit alphabet.

The first control shows why the CRT product bound is part of the decoder type. The second is scoped to a decoder that promises a canonical digit stream; the raw coefficient-vector decoder itself remains exact.
