# Fully charged recurrence and model boundary

## Cost model

Use a sequential, coefficient-record model for an `r`-way Toom recursion. A node has `n` coefficient slots, each input coefficient has at most `h` bits, and the output is exact. `r` is fixed and `t=2r-1`. Let `Δ_r` bound the per-level input-height increase from evaluation constants, and let `Γ_r` bound the product/output-height increase from exact interpolation coefficients and denominators. Thus at depth `j`, child input height is bounded by `h_j=h+jΔ_r`; product/interpolation records have width at most `2h_j+Γ_r`. Both constants are fixed for fixed `r`. All arithmetic is exact. A record copy or tape scan costs its number of moved bits.

For one product `M_r(n,h)`, charge

```text
M_r(n,h) = t M_r(ceil(n/r), h+Δ_r) + C_M(r,n,h),   M_r(1,h)=μ(h).
```

For the paired full-output type `J_r`, charge

```text
J_r(n,h) = t J_r(ceil(n/r), h+Δ_r) + C_J(r,n,h),   J_r(1,h)=2μ(h).
```

`μ(h)` is the cost of one base integer-coefficient multiplication; the base joint type computes both products and so costs two such operations. Each parent term is defined as the sum of every item below, not just the arithmetic gates:

```text
C_X = E_X + I_X + Encode_X + ChildInputCopy_X + ChildOutputCopy_X
      + TapeMoves_X + CarryNormalize_X + RestoreAndCleanup_X + Descriptor_X.
```

- `E`: split and evaluate all operands. `J` evaluates the common `A` once; an unoptimized pair of calls evaluates it twice. A strong baseline can cache the same linear forms.
- `I`: interpolate both full products separately. There are two output coefficient arrays of length `2n-1`; neither is a projection of the other.
- `Encode` and copies: for child size `m=ceil(n/r)`, two isolated `M` calls per evaluation point receive `4m` input records (`A` twice, plus `B,C`); one `J` call receives `3m`. Both return the same `2(2m-1)` output records. Across `t` points this is `4tm` versus `3tm` input records, and `t(4m-2)` output records in either case. If an ABI forces private copies, `J` saves at most `tm` input-record copies per parent. A matched baseline can pass/cache the immutable `A` evaluation once and then has the same `3tm` input records; this is scheduler/data reuse, not a deleted product.
- `TapeMoves`: sequential scans for evaluation, child scheduling, and output placement. No random-access or free pointer handoff is assumed. A concrete machine compiler must show these scans; the present bound charges `O_r(n(h+Δ_r+Γ_r))` bits per parent.
- `CarryNormalize`: normalize the two integer coefficient products independently after interpolation/packing. Each full output requires its own carry propagation and exact range check, bounded by `O_r(n(h+Δ_r+Γ_r))` bit movement and arithmetic at this node.
- `RestoreAndCleanup`: restore/preserve the input records, clear temporary child/evaluation records, and write both outputs. All are charged within the same `O_r(n(h+Δ_r+Γ_r))` node bound.
- `Descriptor`: child sizes, evaluation index, and stack state. The depth is `O(log_r n)`; descriptor and stack traffic is included in `TapeMoves`/cleanup.

For fixed `r`, a sequential schedule has peak live storage `O_r(n(h+Δ_r+Γ_r))` bits: the input records, `t` evaluation slots (processed sequentially), both output arrays, and one child workspace. The joint child still has to retain two outputs. It does not asymptotically reduce peak storage versus running the two products sequentially while retaining the first output. The per-node movement and carry terms above are upper-bounded by `O_r(n(h+Δ_r+Γ_r))`; no coefficient-height or bit movement is omitted.

## Recursive multiplication count

Let `L_M(n)` and `L_J(n)` count base coefficient multiplications only. For `n=r^d`:

```text
L_M(1)=1,       L_M(n)=t L_M(n/r) = t^d.
L_J(1)=2,       L_J(n)=t L_J(n/r) = 2t^d = 2L_M(n).
```

The paired spelling has `t` child calls instead of `2t`, but each paired child returns and pays for two products. After expanding child types, every one of the original `2t^d` scalar multiplication leaves is still present. This is a change of node name and output packaging, not a reduction in recursive multiplication work.

The fully charged total recurrences differ only in `C_M` versus `C_J`. A naive baseline may pay for duplicate evaluation and private copies of `A`; an optimized baseline shares those same immutable records, so it matches the joint input-evaluation/copy saving. Both schedules still pay two interpolations, two carry-normalizations, all output writes, and all remaining input/output record movement. The exact `n=2` count confirms this: the joint form saves one addition only against the deliberately unshared baseline, and saves none against the cached baseline. The copy count above makes any forced-private-copy benefit explicit instead of treating it as free.

For fixed `r`, the multiplication-leaf exponent is `α_r=log_r(2r-1)>1`. `r=2` is Karatsuba (`α=log_2 3`); larger `r` is classical Toom–Cook. Parent evaluation/interpolation/copy/movement costs are charged at each node through `C_X`; they are not treated as free. FFT/NTT changes the transform schedule and can reuse a common operand transform, but still pays each pointwise product and the full output/carry path. Middle-product savings do not apply because `J_n` returns both complete products.

## Boundary to the source recurrence

The original Section 4 recurrence counts rank-one pivots in a specific full-array address interchange: each edge-rank unit is one smaller interchange, and `F_k <= (s/W)F_{k-1}+O(1)`. `J_n` returns polynomial products; it has no original role permutation `rho`, frame endpoints, dirty-wire contract, or edge-rank ledger. The recurrence above cannot replace `s` or be substituted into the paper's `m,W` moment. A new source-typed compiler and matching full output contract would be required even if a coefficient-level cost saving existed.
