# Paid cost gate

## Candidate recurrence with explicit map costs

Let `T(n,b,d)` be bit/tape time for exact convolution of `n` rational
coefficients represented by numerators of at most `b` bits and a common
denominator of at most `d` bits. Let `M(w)` be the cost of multiplying
`w`-bit integers, and let `RatNorm(w)` be the actual fixed-tape cost of
reducing a rational numerator/denominator pair of at most `w` bits. At the
scalar leaf,
`T(1,b,d)=O(M(b+d)+RatNorm(2b+2d))`. For a proposed `n=rm` reduction,
write every encoder and
decoder coefficient with a common denominator `D` (`δ=ceil(log2 D)` bits)
and numerator of at most `H` bits. Define
\[
s_{in}=\max\text{ row support of the }U_t,V_t,\quad
s_{out}=\max\text{ total row support across the }W_t,
\]
\[
A_{in}=\sum_t(\operatorname{nnz}(U_t)+\operatorname{nnz}(V_t)),\qquad
A_{out}=\sum_t\operatorname{nnz}(W_t).
\]
With canonical rational coefficients, the child input widths obey
\[
b_E\le b+H+\lceil\log_2s_{in}\rceil+1,\qquad d_E\le d+\delta.
\]
Child output numerators need at most
`b_P = 2 b_E + ceil(log2 m) + 2` bits and denominator at most `2d_E`.
Before cancellation, decoder accumulators need at most
`b_D = b_P + H + ceil(log2 s_out) + 2` numerator bits and denominator at
most `2d_E+δ`. The exact identity forces the returned coefficients to be
the product of the original rational inputs, whose denominator divides
their squared common denominator; reducing the fractions is therefore
part of every parent return, not a free algebraic step.

The honest recurrence is
\[
\begin{aligned}
T(rm,b,d)\le{}&q\,T(m,b_E,d_E)
 +O\bigl(A_{in}(M(b_E+H)+b_E+H)\\
 &\quad+A_{out}(M(b_P+H)+b_P+H)
 +C_{move}+C_{copy}+C_{zero}+C_{clear}+C_{stack}+C_{norm}+G(r,m,H,\delta)\bigr),
\end{aligned}
\]
where `C_norm` is the actual exact rational normalization cost. Omitting it
would hide the denominator cancellation required by the identity. For
binary coefficient input, add `O(N log N)` bit/tape work for the final
carry pass. For signed `B`-bit input coefficients, the output coefficient
bound is `2B+ceil(log2 N)+O(1)` bits before the final product-specific
recovery.

The reusable-buffer terms can be bounded explicitly by
`C_copy+C_zero+C_clear = O(qm·w_E + qm·w_P + rm·w_D)` bit scans; these
cover both child input arrays, each child return, and the parent output
accumulator. With descriptors of `O(log(rm)+log q)` bits,
`C_stack=O(q(log(rm)+log q))` per parent, plus the depth-first frame scans
already included in tape movement. `C_norm` is one `RatNorm(w)` operation
for each of the `2rm−1` returned coefficients. `RatNorm` denotes the
actual gcd/division cost on the fixed tapes and remains an explicit
unresolved term if the map family is rational.

## Copies, space and fixed-tape schedule

Run children sequentially. For each child, generate and copy its two
length-`m` encoded inputs into reusable fresh buffers, run the child,
read its `2m−1` result, update the parent output accumulator through `W_t`,
normalize the completed result, then zero and reuse the child buffers.
The parent also stores its `rm` input coefficients and `2rm−1` output
accumulators. A descriptor records `r,m,t` and the recursion phase. Thus
each input copy, child return, accumulator read/write, initialization,
clearing, normalization, and stack scan has a place in the recurrence.

For arbitrary maps stored row-major on fixed read-only work tapes, the safe
fixed-tape bound is `C_move=O(q·(rm)·m·w)` bit scans: each of the `m`
encoder rows may rescan an `rm`-coefficient input, and each of the `rm`
decoder rows may rescan a `2m−1`-coefficient child result. It also covers
parking and restoring the parent frame around each child, since that costs
`O(qrm·w)` scans and `m≥1`. This does not assume random access. A
structured sequential transform could reduce that movement, but must
exhibit its address schedule. The maximum live storage
at one parent is `O(rm·w + m·w_E + S_child)` bits plus the matrix records;
depth-first storage across the recursion is the sum of these frame sizes.
The number of tapes stays fixed, and frames are cleared before reuse;
descriptor stack operations are included in `C_stack`.
Generating or storing the matrices costs `G(r,m,H,δ)` time and
`(A_in+A_out)(H+δ)` bits; a uniform fixed-alphabet generator is required
when `r,m` vary. Add `G(r,m,H,δ)` to the recurrence's parent term; it is
not included in the arithmetic big-O until such a generator is supplied.

For dense arbitrary matrices, `A_in+A_out=Θ(qrm²)`. A structured family
would need substantially smaller supports or a faster uniform linear
transform and decoder. The rank theorem says nothing about that cost.

## Fully charged classical control

Classical outer Toom uses `q=2r−1` length-`m` convolution children. For a
concrete control, evaluate at the `2r−1` integer nodes
`0,1,…,2r−2` and apply the inverse Vandermonde map coefficientwise in the
inner variable. Direct evaluation and dense interpolation take
`Θ(r²m)` rational multiply-adds. Each evaluation value has
`B+O(r log r)` bits for `B`-bit input blocks. The Vandermonde determinant
\(\prod_{0\le i<j<2r-1}(j-i)\) has `O(r² log r)` bits, a valid upper bound
on the common denominator carried by direct interpolation. Child output
coefficients have `2B+O(r log r+log m)` numerator bits; decoded values may
need an additional `O(r² log r)` bits before exact cancellation. A
sequential decoder keeps an `O(rm)`-coefficient output accumulator and one
child result, rather than retaining all child outputs. The decoder matrix
and its tape scans, all `2r−1` child input/output copies, rational
normalization, workspace initialization/clearing, and final integer
carries are included. Fast multipoint evaluation/interpolation may reduce
the linear-operation count ([Borodin–Moenck](https://doi.org/10.1016/S0022-0000(74)80029-2)
give the classical division and product-tree method), but that is known
machinery and its coefficient heights, uniform setup, space and tape
schedule must still be charged; it is not the proposed lever. Add
`G_Toom(r)` for generating/storing nodes, powers, and the exact decoder to
the direct-Toom parent cost; a variable-`r` implementation cannot hardcode
an unbounded table into one finite program.

The exact `q=2r−1` bilinear rank count is optimal when the children are
scalar multiplications (`m=1`). For `m>1`, the scoped lower bound is only
`q≥r+ceil((r−1)/(2m−1))`. It does not settle the cost of a better child
packing.

## Transform control (different child type)

For `N` binary coefficients, an exact NTT control would pad to a power of
two `L≥2N−1`, choose a prime `p>N` with `L | (p−1)`, and use a root of
exact order `L`. The type is `F_p^L`: two forward transforms, `L`
pointwise field products, and one inverse transform. Since each exact
coefficient is at most `N<p`, the first `2N−1` canonical residues are the
integer convolution coefficients, then carries recover the product.
Radix-two transforms take `O(L log L)` field operations. At
`λ=ceil(log2 p)` bits, charge `O(L log L·F_p(λ))` bit arithmetic, where
`F_p` includes field multiplication and modular reduction (for fast integer
multiplication/division, `F_p(λ)=O(M(λ))`). A stagewise Stockham layout
uses `O(Lλ log L)` fixed-tape movement,
`O(Lλ)` live workspace and initialization/cleanup, `O(N log N)` carry
work, and a separate `G_NTT(L,p)` for prime/root provision. This is a
known transform control; if `λ` or `G_NTT` is not `O(log N)` and
`O(L polylog N)`, respectively, it does not provide the desired baseline.
Its ring and scalar-product children do not instantiate the `Q`-linear
`Conv_m` family.

The pinned manuscript's Section 6 has another already-charged transform
control: on its disk arrays over `C[y]/(y^r+1)`, the transform-convolution
pipeline costs
`O(Tp[dK+pK^(τ−1)+ℓd^(λ′)+log(rp)])`, including layout construction and
restoration. It is an approximate disk-array interface with its own
precision and recovery hypotheses, not an exact `Conv_N` map. Neither
transform is used to claim a saving for the selected family.

## Asymptotic gate and source-model separation

For a variable-arity family the unresolved recurrence is
\[
T(N,b,d)\le q(N)T(m,b_E,d_E)+P(N,r,m,H,\delta),\quad N=r m,
\]
where `P` is the fully paid map, copy, normalization, output, carry,
workspace and fixed-tape work above. A rank-compatible `q` near `r` could
make `log_r q` close to one, but that is only a child-count observation.
No `κ` is inferred: there are no maps, no height/sparsity bound, and no
uniform decoder or tape program. The next useful lemma is either a
`(r,m)=(3,2), q=4` exact reduction with explicit matrices, or a stronger
obstruction for that case; any asymptotic claim then needs a uniform
family with paid `P` below the target.

The original manuscript's Section 4 uses full-array address interchanges
and proves `F_k≤(s/W)F_(k−1)+O(1)` after charging its fixed-tape parking and
movement. These `Conv_m` calls have a different type and volume, so that
recurrence and its κ arithmetic are not imported. Its Section 6 synthetic
transform is an existing transform-based control, not evidence for this
candidate. The fork's conditional witness at the starting commit is
`κ₀=971668963/25000000000000`; this checkpoint proves neither a change to
that witness nor a route into its hypotheses.
