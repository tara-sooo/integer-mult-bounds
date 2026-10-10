# Paid recursive-cost gate

## Operations actually changed

Let the parent operands be `N`-bit nonnegative integers. Split into `n=ceil(N/b)` radix-`β=2^b` digits. Let `L` be the next power of two at least `2n-1`, and let `r` be the number of NTT primes. Write `w=max_j ceil(log2 p_j)`. One field multiplication on `w`-bit residues costs

```text
MulMod(w) = M(w) + Div(2w,w),
```

where `M` is an ordinary integer multiplication and `Div` is exact reduction modulo the prime. Both the pointwise products and every nontrivial twiddle multiplication are charged this way.

Two forward radix-two transforms and one inverse transform use at most

```text
A = r ((3/2) L log2(L) + 2L)
```

field multiplications: `L log2 L` forward butterflies across the two inputs, `(L/2)log2 L` inverse butterflies, `L` inverse scalings, and `L` pointwise products per prime. Additions/subtractions cost `O(rL log L·w)` bit operations. A fixed-tape implementation must also scan, copy, initialize, and clear transform buffers at every stage; each modular child call's `w`-bit argument/result copies and buffer clearing are included in this scan term, up to a constant factor. Keeping all three spectra for all primes takes `O(rLw)` bits of working storage. For fixed `r`, mixed-radix CRT reconstruction costs `O(n r^2 w^2)` with elementary multiplication and long division; the final carry pass costs `O(N+nrw)`.

The honest recurrence is therefore

```text
T_NTT(N) <= A·MulMod(w)
             + O(r L log L·w + n r^2 w^2 + N + G(n,L,r,w)).
```

`G` includes selecting and certifying the primes, finding primitive roots, generating twiddle tables, and uniformly describing them. A product bound alone does not pay for prime/root generation. At the small pilot, the moduli and roots are fixed constants; no scalable generator was tested.

## Asymptotic screen

Take `b=ceil(log2 N)`, so `n=Theta(N/log N)`, `L=Theta(n)`, and the coefficient bound is `n(β-1)^2`. Four primes all greater than `L` have product greater than `L^4`, which exceeds that coefficient bound for all sufficiently large `N`. If they also have `p_j <= L^C` for a fixed `C`, then `r=4` and `w=O(log N)`. The transform then makes `A=Theta(N)` recursive modular-multiplication calls on `O(log N)`-bit values. The matched schoolbook block recurrence is `T_school(N) <= n^2 M(b)+O(n^2 b+N)`; the NTT reduces its `n^2` block products to `Theta(N)` smaller modular products, at the cost of the transform layers.

It does not improve the fork's current pinned integer-multiplication bound. The charged radix-two additions and tape scans already contribute `O(rL log L·w)=O(N log N)` bit operations in this parameter range. Even granting a uniform low-cost prime/root generator and fast exact reduction with `MulMod(w)=O(M(w))`, substituting the current bound `M(t)=O(t(log t)^(1-κ0))`, `κ0=971668963/25000000000`, gives

```text
T_NTT(N) = O(N log N (log log N)^(1-κ0)) + G(N),
```

versus the existing `O(N(log N)^(1-κ0))`. The ratio grows with `N`. With elementary long division instead, the modular reductions cost up to `O(w^2)` each and the bound is worse. This is a charged cost comparison for this radix-two NTT schedule, not a lower bound against all exact transforms.

The fixed-width residue product is `w=O(log N)` bits, smaller than the parent for large `N`, so the reduction is non-circular in the stated conditional prime family. The `n=2` pilot itself has no such child-size advantage: its 7-bit largest residue multiplication exceeds its 4-bit source operands. No child call is credited as free.

## Missing bridge and stop condition

No source Section 04 roles, all-role endpoint frame, arbitrary-dirty restoration, or original bit/complex supplier is constructed. The Section 04 recurrence cannot be reused: its child is a full-array address interchange with volume `V/W`; these children are scalar modular products with coefficient bounds and a CRT/carry decoder.

The smallest unresolved uniformity lemma for this candidate is an explicit family/generator that, for every transform length `L`, supplies a constant number of pairwise-distinct primes `p_j <= L^C` with `L | p_j-1`, primitive roots, and certificates in time below the claimed saving. A polynomial bit-size existence bound alone does not pay for a uniform search, table, or root generator. Even if that lemma is supplied, the charged call count above still gives no improvement over the current bound. A new route would need to reduce the total `O(L log L)` modular multiplications per prime, or prove that a structured exact transform makes those operations cheaper while keeping modulus size and decoder costs bounded.

No `W,m,s`, paid moment, `κ`, full supplier, precision, or tape-transfer claim is derived here.
