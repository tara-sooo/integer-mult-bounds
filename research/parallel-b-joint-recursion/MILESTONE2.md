# Issue 41 — Milestone 2: no cheaper typed joint child

**Disposition: `NO_CHEAPER_TYPED_JOINT_CHILD`.** I screened two different correlated-child architectures. Overlapping windows collapse to one standard product-window request. A partial diagonal-plus-cross child is an exact dual-number convolution with a carry-bearing integer realization; its proposed Toom recursion pays the same multiplication leaves as its three-product baseline, and the full parent is already covered by Karatsuba with three children. The exact small checks below find no deleted paid multiplication child.

## Scope and fixed controls

The updated [Issue 41](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/41) asks for internal correlated children of one exact product. The first-wave result is preserved unchanged: [`NO_PAID_JOINT_GAIN`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/7ba7d3a4d8235f8aa74f136fb0c3678d1405dd72) applies to the complete-output type `J_n(A;B,C)=(AB,AC)`. I did not reopen that type or read another lane's worktree. This report adds no code or checker; its finite experiment is recorded inline.

The dedicated branch remains `research/parallel-b-joint-recursion`, based on the first-wave commit above in the linked worktree. The pinned manuscript is [`openai/math` commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a), vendored unchanged. Its introduction says radix splitting reduces integer multiplication to short-coefficient convolution (`upstream/build/sections/00-introduction.tex:40–46`). Its exact-product section explicitly charges signed packing, coefficient recovery, and conversion (`upstream/build/sections/06-transforms.tex:450–461, 573–609`). Those are the source semantics used below. The manuscript's Section 4 rank-pivot recurrence applies to its address-interchange child, not to these coefficient-product types; no `s/W` substitution is made (`upstream/build/sections/04-swap.tex:197–207`).

## B0: two typed architectures

### A. Merge overlapping windows of one convolution

For coefficient arrays `a,b`, let `c_k=Σ_i a_i b_{k-i}`, with out-of-range indices zero. For intervals `I=[u_1,v_1]` and `J=[u_2,v_2]` with `u_1≤u_2≤v_1≤v_2`, propose

```text
W_I,J(a,b) = ((c_k)_{k∈I}, (c_k)_{k∈J}).
```

The old graph has two product-window children, one for each interval. The joint child returns exactly the coefficients in `I∪J=[u_1,v_2]`, then copies the overlap into both requested output slots. Thus it deletes duplicate overlap work only against a baseline that issued two separate window calls. A strongest baseline issues one truncated/middle-product call for `I∪J` and makes the same required output copies. No complete multiplication child is deleted against that baseline; if the union is the whole convolution, this is an ordinary full product.

This is precisely a product-window wrapper, not a new recurrence. Transposition can implement a window operator but does not change this type identity. Relaxed/online multiplication has an additional arrival-order constraint absent here. A multi-output FFT can share forward transforms, but the pointwise products and requested coefficients remain; this is the same distinction as in the first-wave shared-input result. This architecture was screened out at B0 and was not selected for a separate experiment.

### B. Diagonal-plus-cross child with a carry-bearing residual

At the coefficient level over a characteristic-zero field, define

```text
H_d((A0,A1);(B0,B1)) = (P,Q)
P = A0 B0,
Q = A0 B1 + A1 B0,
```

where each input is a polynomial of length `d` and both outputs are complete coefficient arrays. This is not the first-wave two-independent-full-products type: the second output is a correlated cross sum. Algebraically it is multiplication of `A0+εA1` by `B0+εB1` in the dual-number ring `F[ε]/(ε²)`, retaining the `1` and `ε` coefficients.

For the exact integer parent, split at `B=2^m`:

```text
X = x0 + B x1,       Y = y0 + B y1,       0 ≤ x0,x1,y0,y1 < B,
pij = xi yj,
L = p00 mod B,
R = floor(p00/B) + p01 + p10.
```

Then the complete product is recovered by

```text
XY = L + B R + B² p11.
```

Dependency graph (all arrows are data dependencies; the four old leaves are full `m`-bit products):

```text
M(x0,y0) -> p00 -> low_m -> L --------------------------┐
                    └-> high_m -> q --┐                │
M(x0,y1) -> p01 -----------------------+-> R -> B*R ----+-> exact sum -> XY
M(x1,y0) -> p10 -----------------------┘                │
M(x1,y1) -> p11 ---------------------------> B²*p11 ---┘
```

The proposed `H_m` replaces the first three calls by one typed call returning `(L,R)`; the high child `M(x1,y1)` remains. At leaf granularity, `H_m` still needs the three products `p00,p01,p10`. The high child brings the total back to four `M(m)` leaves, the same as the split schoolbook graph. A strong full-product baseline is the known Karatsuba graph: compute `p00`, `p11`, and `S=(x0+x1)(y0+y1)`, then recover `p01+p10=S−p00−p11`. That is two `M(m)` children and one `M(m+1)` child; the sum widths and all subtractions are charged. The proposed child therefore has no paid-child advantage over either baseline.

### Exact scalar rank screen for `H`

For one coefficient, the bilinear map is

```text
T(a0,a1;b0,b1) = (a0 b0, a0 b1 + a1 b0).
```

Its output slices are `M0=[[1,0],[0,0]]` and `M1=[[0,1],[1,0]]`. Any linear combination `uM0+vM1` has determinant `−v²`; its only rank-one direction is `M0`. A rank-two bilinear decomposition would express the two-dimensional slice space as the span of two rank-one matrices, which is impossible because that space contains only one rank-one direction. Hence the bilinear rank is at least three; the three products `a0b0`, `a0b1`, `a1b0` attain rank three. This proves the proposed scalar `H` leaf cannot save one multiplication in this model. It does **not** prove an all-size lower bound for every possible nonlinear bit algorithm or every different tensor decomposition.

## FAST exact pilot

For the integer carry realization, I exhaustively checked all 256 tuples `(x0,x1,y0,y1)∈{0,1,2,3}^4` at `B=4` using the exact identity above. The check is reproducible with:

```python
from itertools import product
B = 4
for x0, x1, y0, y1 in product(range(B), repeat=4):
    p00 = x0 * y0
    L = p00 % B
    R = p00 // B + x0 * y1 + x1 * y0
    assert (x0 + B*x1) * (y0 + B*y1) == L + B*R + B*B*x1*y1
```

Observed: all 256 reconstructions pass. A nonzero carry is necessary: `(x0,y0)=(0,0)` and `(2,2)` both give `L=0`, but their high residuals are `0` and `1`; with `x1=y1=0`, omitting `R` reconstructs `0` instead of `4` in the second case. A full nontrivial example is `(x0,x1,y0,y1)=(3,1,2,3)`: `X=7`, `Y=14`, `L=2`, `R=12`, `p11=3`, and `2+4·12+16·3=98=XY`.

The residual is not a constant-size carry for arbitrary block inputs. With `B=2^m`, set `x1=y1=0`, `x0=B/2`, and `y0=2k` for `0≤k<B/2`. Then every input has `L=0` while `R=floor(x0y0/B)=k` takes `2^(m−1)` distinct values. Any returned state that alone preserves the missing high part must distinguish at least `m−1` bits. This is a scoped information bound for this block-residual interface, not a lower bound for ordinary digitwise carry propagation; recomputing the missing value from the inputs must instead pay for that computation.

## B2: recurrence and fully charged comparison

Let `M_r(d,h)` be an `r`-way Toom multiplication on `d` coefficients of height `h`, `t=2r−1`, and let `Δ_r` bound evaluation height growth while `Γ_r` bounds product, cross-sum, and interpolation growth. At depth `j`, charge input height `h_j=h+jΔ_r` and product/interpolation records up to `2h_j+Γ_r`. For `d=r^j`, the candidate applies the same Toom points to all four input polynomials and interpolates `P` and `Q`:

```text
M_r(1,h) = μ(h)
M_r(d,h) = t M_r(d/r,h+Δ_r) + C_M(d,h)

H_r(1,h) = 3 μ(h)
H_r(d,h) = t H_r(d/r,h+Δ_r) + C_H(d,h)
```

Expanding gives `L_M(d)=t^j` and `L_H(d)=3t^j=3L_M(d)`. The spelling has `t` `H` children rather than `3t` `M` calls, but each `H` child still contains three base multiplication leaves. For the complete radix-split parent, `H_r+M_r` therefore has `4t^j` leaves. Replacing it with the `P,p11,S` Karatsuba schedule has two `M(m)` children and one `M(m+1)` child (the evaluation operands may grow by one bit). No leaf saving is established.

The per-node term is charged as

```text
C_H = Eval_4 + Interpolate_2 + Encode + ChildInputCopies
      + ChildInputReads + ChildOutputReads/Copies + CarryNormalize
      + TapeMoves + RestoreInputs + ClearScratch + Descriptors.
```

Concretely, all four input polynomials are evaluated with their grown coefficient widths; every child input record is copied or read under the chosen ABI; two complete `(2d−1)`-coefficient output arrays are interpolated, written, and retained; the cross sum and signed/range conversions are included; and every scan, input restoration, dirty-scratch cleanup, and descriptor update is charged. Recursive child costs include producing their result arrays; `C_H` charges the parent's reads, copies, and accumulation of those arrays, avoiding double counting. At each point, `H` consumes four evaluated coefficient records and produces three scalar products internally, then emits the `P` and summed-cross records. The matched three-product baseline uses the same four unique evaluated records for `(A0,B0)`, `(A0,B1)`, `(A1,B0)` and sums the last two before interpolation, so it too can retain only two output arrays. With `q=ceil(d/r)` child coefficients, if an ABI forces a private argument copy for every child call, the joint call copies `4tq` records per parent versus `6tq` for three separate calls, a conditional saving of `2tq` copied records; with borrowed immutable records a strong baseline can avoid those copies. This copy difference deletes no multiplication. Shared workspace or output packaging is not counted as a multiplication saving.

For the integer `H_m` node, `p00` has at most `2m` bits, `L` has `m` bits, and

```text
0 ≤ R ≤ 2(B−1)² + (B−2) = 2B²−3B < 2^(2m+1),
```

so its residual output is charged at `2m+1` bits. The three product children produce up to `6m` intermediate bits in total; their result writes are included in the child costs, while all parent reads/streams and cleanup are charged. In a private-input ABI, the three `H_m` calls copy `6m` input bits total (at most `2m` live for a sequential schedule); in a borrowed-read-only ABI the corresponding reads remain charged. `H_m` writes `m+(2m+1)=3m+1` output bits. A safe nonstreaming parent peak, before the active child’s own auxiliary space, is `13m+1` bits: either `4m` retained input + `6m` intermediate products + `3m+1` `H` output, or `4m` input + `3m+1` `H` output + `2m` `p11` + `4m` final result. Add one active `M(m)` child's scratch (excluding the already counted returned product) and, for a private-input ABI, its at-most-`2m` live argument copy. A sequential streaming schedule can lower this peak, but the same schedule is available to the split baseline. The final combination writes all `4m` product bits and pays the shift/add/carry scans. Thus the full paid recurrence is `4M(m)+C_4` for either the split-schoolbook or `H_m+M(m)` graph, versus `2M(m)+M(m+1)+C_K` for classical Karatsuba; `C_4` and `C_K` include all terms just listed, Toom coefficient growth, copies, storage, movement, restoration, and cleanup.

### Method comparison and boundary

| Method | Relationship to this milestone | Result |
|---|---|---|
| Middle/truncated product | Architecture A's two outputs are projections of one interval union. `H` is not a new middle-product algorithm; any coefficient window it exposes is the corresponding standard window problem. | No new child over the strongest single-window baseline. |
| Transposition | May implement a linear window map under an adjoint interface. | Does not change the output-union identity or delete a multiplication leaf. |
| Relaxed/online product | Adds an input-arrival or prefix-output contract. | No such contract is present in this offline exact type. |
| Karatsuba | Its `P,p11,S` identity computes the complete parent in two `M(m)` and one `M(m+1)` children and recovers the cross sum. | The full parent already has this known three-child schedule; `H+M` has four `M(m)` children. |
| Toom–Cook | Evaluating the four arrays at `2r−1` points gives the recurrence above; both `P` and `Q` are interpolated. | Three scalar products per `H` point, exactly the matched three-product count. |
| FFT/NTT | Shared forward transforms can serve the two correlated outputs. | Pointwise products and both requested coefficient arrays remain; only transform reuse is available. |
| Carry-state | `R` carries the high part of `p00` into the cross region. | The state must scale with block width in this interface; this is not a constant carry. It is narrower in scope than the separate carry-state direction in [Issue 34](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/34). |
| First-wave full-output rank screen | It concerns `(AB,AC)` and its exact full-output flattening rank. | Preserved as a separate scoped theorem; it is not applied to `H`. |

## Conclusion and limits

No complete recursive multiplication child is removed by either tested architecture. Window merging is exactly a standard product-window request. `H` is a genuine partial-output type, but its proposed Toom recursion expands to the same three multiplication trees as its strong cached baseline; the complete integer parent is covered by classical Karatsuba with three children. Its exact scalar bilinear rank is three, and the `B=4` exhaustive integer pilot confirms the carry-bearing reconstruction and its adverse missing-state case.

Unproved: a different tensor decomposition of `H_d` for `d>1` might use fewer than `3L_M(d)` leaves; no general lower bound for that type, nonlinear bit circuits, or different carry encodings is claimed. No concrete Section 4 role/frame supplier or fixed-tape constant comparison was run: neither candidate produced a cheaper typed child to carry into FOCUSED verification, and the coefficient types do not meet that source recurrence's interface. No `s/W` term is imported. First-wave files remain unchanged.
