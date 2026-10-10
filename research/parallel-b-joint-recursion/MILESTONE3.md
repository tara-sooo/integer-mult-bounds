# Issue 41 — Milestone 3: scoped rigidity for a deleted transform-layout exchange

**Disposition: `SCOPED_CONTEXT_RIGIDITY`.** In the fixed Section 06 transform/convolution schedule, deleting one width-1 chunk exchange from the two forward layouts while retaining the original pointwise product and inverse decoder changes the exact integer product. The smallest check below uses a legal pair of independent integer inputs and the complete product decoder. A consistently changed forward and inverse layout remains algebraically correct, but no paid transfer is deleted by that identity alone.

## Scope, frozen results, and sources

This continues the existing linked worktree and branch `research/parallel-b-joint-recursion`, based on fork main `0605a24a28836168ad29d6239b46064b892298fc`. The frozen first-wave result [`NO_PAID_JOINT_GAIN`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/7ba7d3a4d8235f8aa74f136fb0c3678d1405dd72) and second-wave result [`NO_CHEAPER_TYPED_JOINT_CHILD`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/948281b5394e11b7852b699b69ec225896c07675), including `MILESTONE2.md`, are unchanged. I read no sibling worktree.

The exact source is the frozen manuscript [`openai/math` commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a). I used Section 04's arbitrary-array interchange and cleanup contract (`upstream/build/sections/04-swap.tex:197–211,285–301`), Section 06's grouped transform and layout (`06-transforms.tex:131–169,171–274`), exact operators and product (`06-transforms.tex:422–448,612–683`), and Sections 07–08's chirp/source/integer-product path (`07-resampling.tex:416–490`; `08-assembly.tex:386–463,468–555,701–815`). The local source-file SHA-256 values are recorded in the source checkout; the relevant M3 files are `03-motifs.tex` `ed76761194988a01af77ead0ea6469cb5dcd29690ab985a0b5a4006b0f2b69bb`, `04-swap.tex` `412b170ccaab38dba96e95e3cbfae09f4876a9818f8d278776a746b0f8044906`, `06-transforms.tex` `924316e4bc905066281d8f9e8746a49d8829aeb393688608deb1e61c3c87853c`, `07-resampling.tex` `8a6b91670f9163afb54892489fa2210c77fe1b058f0325ec7d18b44b94be6e2c`, and `08-assembly.tex` `763d7945b1e1ec4ebae9b799bcefcc45fa9bae6e2ffad799868a9c3d513dbd4a`.

The pinned architectural comparison is [`CrocSwap/integer-mult-bounds` commit `d2873e20750d0949d2ad75cbc4cd82b5b1a74e84`](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/d2873e20750d0949d2ad75cbc4cd82b5b1a74e84), including its `coordinated-frames-and-entrance-banks/PROOF.md` and `FRAME-DISCOVERY.md`. Its paid finite-supplier and physical-frame conclusions apply to that retained supplier model; I do not transfer its `s/W` recurrence or its conditional `D,C` bound to a changed transform schedule. Physical comparison references, pinned by the heads read for this screen, are [#244, head `a568d94f941929232ab393c7d33dc5a30e017892`](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/244), [#249, head `96495746c786d6d0339dbb38c7f553d4af3f88ed`](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/249), and [#251, head `2b030c06a811473ae8ed49dce07bc7ea50b72e9e`](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/251). Those retime or transport finite scalar supplier frames; they do not establish a cheaper address-array exchange in Section 06.

## ACTUAL_CALL_SITE

Section 06's transform-layout lemma calls the Section 04 chunk interchange while building `L`. For `D=2`, both axes of length `8=2^3`, and chunk width `K=1`, the prefix move places the two high address bits first. The remaining axis-major chunk order is

```text
(1,1),(1,2),(2,1),(2,2)
```

and the target chunk-major order is

```text
(1,1),(2,1),(1,2),(2,2).
```

Exactly one width-1 exchange swaps the middle two chunks. In address-bit notation the full `L` order is `(x2,y2,x1,y1,x0,y0)`; omitting that one call leaves `(x2,y2,x1,x0,y1,y0)`. This is a real Section 06 instance of the procedure in Section 04, not an abstract role relabeling.

The exact call has the following types and order. Let `u,v` be the two independent operands to `\mathcal M_r` and let `F^-` be the exact tensor transform. Section 06's predecessor and complete stored forward permutation are

```text
E(u) = B F^- u,
S = L,
S E(u) = L B F^- u.
```

The later operation is nonlinear: `Q(a,b)=a·b/r`, the corresponding polynomial-record product. Its exact decoder is

```text
D(z) = M F^+ B^-1 L^-1 z,
```

with the stated normalizations, so `D(Q(S E(u), S E(v)))=(u*v)/(rM)`. Section 06 proves `Q(LBf,LBg)=LBQ(f,g)`, which is why both forward results may stay in the common retained layout until the product.

In the actual Section 08 integer path, independent digit vectors `a,b` first become padded source arrays `u=Φ(a), v=Φ(b)`. Each source transform applies `\mathcal A`, then the chirp path. For a chirp input `x=\mathcal A u`, that path forms `x0=\bar c·x`, calls `\mathcal M_C(c,x0)`, and applies the final `\bar c` endpoint. The complex convolution in that call twists both operands, maps them through `\iota`, calls Section 06's `\mathcal M_r`, then untwists and unmaps the result. Thus the Section 04 calls in question occur in each of the two forward transforms inside this `\mathcal M_r` invocation; there one operand is the fixed chirp-derived kernel and the other depends on the integer input.

After the two top-level source transforms, Section 08 multiplies corresponding complex records, applies the opposite source transform, restores the two `S` normalizations and the input digit scale, rounds real coefficients, applies `Φ^-1` and removes padding, then propagates radix carries and writes the fixed-length product. Its exact counterpart gives `(u*v)/S^2` before the two stated `S` scales, and then the ordinary integer coefficient convolution. The exact digit/carry decoder is part of the demand tested below.

## Two candidate architectures screened

**A. Retain a common virtual layout and fuse the final inverse layout with coefficient decoding.** Applying the same record permutation to both transformed operands commutes with the pointwise product, and its inverse can be moved to the decoder. This is the familiar FFT output-order freedom (including DIF/DIT layouts). It is algebraically sound when every intervening layer and the inverse use that same layout. It does not itself delete a paid exchange: Section 06 needs `L` to put butterfly address bits at common offsets, and the final coefficient-order/carry decoder still needs its input in the expected order. No fixed-tape implementation that saves a transfer after fusing these obligations was found. This is not a new middle product or multiplication child.

**B. Replace the boundary permutation `L` by `L'`, omitting its middle chunk exchange on both forward operands, while keeping the exact predecessor `E=BF^-`, pointwise product, and full inverse decoder unchanged.** This removes two complete forward address-transfer calls in the `D=2,K=1,q=2` example, one for each independent operand. It is the selected exact screen because it has a specific paid move to delete. The following exact check rejects it. It is distinct from A: it leaves the later decoder on the original full layout and asks the nonlinear product context to tolerate a changed forward map. The Section 06 grouped-layer implementation realizes `LBF^-` by conjugating its layers with `L`; this boundary substitution does not prove that `L'BF^-` can be scheduled with the same layer cost.

Middle/truncated products concern requested coefficient windows, not this address permutation; no window child is removed. Karatsuba and Toom–Cook reduce scalar multiplication children, while this candidate retains all `M` pointwise record products. FFT/NTT already allows a common permutation to be carried through pointwise multiplication, which is candidate A's known identity. Ordinary carry propagation begins only after coefficient recovery and cannot repair a wrong frequency/address order. The prior Issue 34 carry-state and Milestones 1–2 results therefore provide no shortcut for this screen.

## REACHABILITY_AND_DEMAND

The real Section 08 chirp call has a fixed kernel and a restricted data set; it is not an arbitrary pair of vectors. For an integer input with digit vector `a`, the data-side input at the Section 06 convolution boundary is exactly

```text
g(a) = iota( theta+ · (bar(c) · A(Φ(a))) ),
f    = iota( theta+ · c ),
```

up to the explicitly stated grid truncations in the numerical algorithm. The set of such `g(a)` is finite and bounded by the digit alphabet. Its linear span is not the set itself. The exact tensor map `A` is injective: `B0 Q F_t A = 2^-γ R F_s`, while `R F_s` has full column rank. The following Fourier transform is invertible and the phase multipliers are nonzero, so this path can spread a low-support digit input over the whole record grid. I neither infer a low-dimensional coordinate support from the input padding nor replace the actual finite reachable set by the full vector space.

The bounded witness checks the independent digit-pair context at the exact Section 06 normalized-convolution interface. It uses two `8×8` axes and two independent integer inputs encoded from four binary slots each:

```text
X = Σ_(a,b∈{0,1}) x[a,b] 2^(a+8b),
Y = Σ_(a,b∈{0,1}) y[a,b] 2^(a+8b),      x[a,b],y[a,b]∈{0,1}.
```

Each input has 16 possible payloads, so all 256 independent pairs are checked. The product has coordinate sums at most `2` in each axis, hence no cyclic wrap modulo `8`. The integer decoder identifies output coordinate `(i,j)` with radix position `i+8j`, performs all binary carries, and returns `XY`. For the exact scalar-record slice, Section 06's `1/r` and `1/M` factors are canceled by its declared output normalizations; the polynomial suffix can equivalently be a constant-only record.

The multiplication is performed after the full two-dimensional Fourier transforms. In particular, the test does not use a linear kernel argument before `Q`: it forms both transformed operands, multiplies them coordinate by coordinate, applies the full fixed inverse layout and Fourier decoder, then rounds and carries. The script checks the full original decoder for all 256 pairs over `F_17`; `2` has order `8` and `2^4=-1`, so this is an exact reduction of the `Q(ζ_8)` transform identities. The original output coefficients are at most `4<17`, so their residues identify the exact integer coefficients.

## CONTEXT_EQUIVALENCE_OR_RIGIDITY

Let `L'` omit only the width-1 middle exchange, and keep the original inverse `D`. Define the residual frequency-record permutation `R=(LB)^-1(L'B)`. It is nonidentity because `L'≠L`. Pointwise multiplication is explicitly accounted for:

```text
(L'B F^-u) · (L'B F^-v)
  = L'B ((F^-u) · (F^-v)).
```

The unchanged decoder therefore applies the nonidentity `R` to the true pointwise product before the inverse Fourier map. A permutation of frequency coordinates cannot be hidden by the inverse: the inverse transform is injective. In the 2D size-8 group, the characters generated by the two legal input monomials `(1,0)` and `(0,1)` separate every pair of distinct frequency addresses. For any nonidentity `R`, choose a moved address pair; one of these two characters changes there. Taking the other operand to be the unit monomial makes its transform the constant character, so the nonlinear pointwise product is exactly the distinguishing character. This proves a scoped rigidity lemma for this fixed-transform/fixed-decoder class and the stated digit support. It is not a claim that every possible global multiplication redesign must use `L`.

For the concrete omitted-exchange candidate, the exact `Q(ζ_8)` witness is `X=2` (`f=δ_(1,0)`) and `Y=1` (`g=δ_(0,0)`). The true decoder yields coefficient `1` at `(1,0)` and zero elsewhere, hence integer product `2`. Under `L'` followed by the original `L^-1` decoder, each decoded real coefficient is

```text
Re(c[x,y]) = (n0-n4)/64
             + (n1-n3-n5+n7) √2 / 128,
```

where `ne` counts the corresponding powers `ζ_8^e` in the exact inverse sum. The checker bounds `√2` by `141421356/10^8 < √2 < 141421357/10^8` (verified by squaring) and proves all 64 real coefficients lie strictly between `-1/2` and `1/2`. The prescribed nearest-integer decoder therefore writes all-zero coefficients and the carry scan returns `0`, not `2`. This is an exact cyclotomic and rational-interval check, not floating-point evidence.

As a negative control, if both forward transforms and the inverse decoder use `L'` consistently, the convolution is unchanged for all 256 input pairs: the common permutation and its inverse cancel through `Q`. The checker verifies this too. This control is the standard common-layout identity; it does not delete a move from the transform's grouped butterfly schedule.

The control descriptor `(D=2, ell=3, K=1, q=2, prefix bits, two chunks per axis)` is fixed and data-independent. The candidate changes only the specified data permutation. A separate arbitrary dirty scalar is a spectator and is unchanged for all 17 values in the exact field model; symbolically it is passed through unchanged for any scalar domain. Section 06's existing butterfly temporary rows and work streams are still created and cleared by the unchanged routines. The counterexample already fails with those obligations satisfied and no new scratch state. The small checker is an exact semantic check of this substitution class, not a reimplementation of the lower-level fixed-tape `chunk-swap` executor.

## RECURSION_GATE

For `T=64` records of `w` bits, the selected Section 04 width-1 exchange is charged on a full address array. The chosen `L` has one such forward call; using it for both operands charges two calls. At the exact-map level, the hypothetical deletion would remove `2·Swap(64w,1)` from the two forward boundaries. Each is an `O(64w)` call at `u=1`, including its fixed-tape setup, padding, cleanup, and dirty-scratch restoration. The inverse procedure still pays the original `L^-1` exchange. All prefix bit moves, all remaining `L` factors, `\ell` grouped layers and their temporary rows, record reads/writes/copies, all `64` pointwise products, inverse-transform work, coefficient scales, `Φ^-1`, padding removal, rounding, carry state, and output reversal remain charged. The invalid candidate has no repair cost only because it returns the wrong integer. A physical implementation would also need to reschedule the conjugated butterfly layers; that additional schedule and cost were not constructed.

At general size, Section 06 charges both layout construction and restoration in

```text
O(Tp [ dK + p K^(τ-1) + ell d^(λ') ]).
```

Removing one of at most `Dq−1` forward chunk exchanges from each of two operands would be a strict total saving only if a replacement layer schedule and decoder satisfy the exact product identity and their extra reads, copies, memory, movement, carries, and cleanup cost less than the removed calls. The fixed-schedule candidate fails the identity above. If a later operation applies the inverse residual `R^-1`, that operation and its data movement must be charged; no deleted exchange has been demonstrated. If the butterfly pair schedule itself changes, the current `s/W` recurrence does not apply. No new recursion inequality or `κ` is claimed.

Composition across rounds has the same gate. A consistent common layout can pass through the nonlinear product, but the physical layout is still required at each grouped layer. A locally omitted exchange that leaves a nonidentity residual at the product is detected by the characters above. A family of omitted exchanges whose residuals cancel must exhibit where the compensating data movement or altered butterfly schedule went; that uniform lemma and its paid cost are open.

## Exact controls, comparison, and limits

Reproducible command:

```text
python3 research/parallel-b-joint-recursion/check_context_rigidity.py
```

Observed result: **PASS** — original exact transform/decoder and binary carry agree for all 256 independent input pairs; a consistently changed common layout also agrees for all pairs; omitting the one forward exchange fails for 221 pairs in the exact `F_17` control; the exact `Q(ζ_8)` witness `2×1` rounds and decodes to `0`; control descriptor and arbitrary spectator dirty scalar are restored. Runtime was about 10 seconds in this worktree. `make verify` and a full fixed-tape replay were **NOT RUN**; neither is needed for the finite algebraic obstruction.

This is not Karatsuba, Toom–Cook, a middle/truncated product, a carry-state recursion, or a new FFT: it neither changes the multiplication child count nor finds a new transform. It is a scoped counterexample to deleting one real paid layout transfer while holding the surrounding Section 06 schedule and decoder fixed. The previous exact full-swap construction remains an all-input operation; no `s/W` estimate has been copied into this changed context.

Unresolved conditions: (1) this lemma does not prove that the narrower digit-derived `g(a)` set in the actual fixed-kernel `\mathcal M_C(c,x0)` call spans the tested monomials; that exact reachable-set question is not answered here, despite the full path being traced above; (2) no different global transform or output decoder was synthesized; (3) no all-size family of context-specific replacements with a cheaper paid recurrence is known; (4) no low-level fixed-tape implementation of a changed butterfly schedule was replayed. Thus the result blocks the stated local deletion, not all possible contextual reductions in integer multiplication.

**Frozen lane result:** `SCOPED_CONTEXT_RIGIDITY`. The only new files are this report and its exact checker; Milestones 1 and 2 remain preserved.
