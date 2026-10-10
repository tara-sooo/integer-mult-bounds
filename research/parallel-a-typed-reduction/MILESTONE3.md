# Milestone 3 — coupled source/target and center/side screen

**Disposition: `SCOPED_DATA_CENTER_OBSTRUCTION`.** A two-source block admits an exact, dirty-safe, non-diagonal center/side routing identity over both required scalar domains. It uses two independent rank-one channels, the minimum allowed by a source/target rank bound. It therefore replaces the routes but deletes no complete rank-one recursive child. The stated one-shot class cannot compress two independent source coordinates into one such child. This is not an obstruction to other multiplication algorithms or to a fused wider child.

This continues the existing `issue-40-source-typed-reduction` branch from [Milestone 2 commit `3e2d29668624d6096c57b948137511f005374abe`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/3e2d29668624d6096c57b948137511f005374abe). `RESULTS.md`, `MILESTONE2.md`, the first-wave checker, and the prior receipts were left unchanged. The source manuscript is pinned at [commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a); the cost inputs below are pinned at [PR 203 head `d2873e20750d0949d2ad75cbc4cd82b5b1a74e84`](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/d2873e20750d0949d2ad75cbc4cd82b5b1a74e84).

## DATA_LEDGER

### Original scalar source, target, center, and side paths

The Section 03 scalar domains are `R_b = F_2` and `R_c = Z[i,1/2]`. The fixed construction uses `h=100`, the port set `T = {S ⊂ [h] : |S|=3}`, `v=binom(100,3)=161700` ports, and two independent banks `X_a,Y_a` indexed by `a ∈ T^3`. One invocation has source entries `x_T`, target entries `y_S`, side scratch `A_ST` for each ordered neighboring pair, and center scratch `C_i` (plus `C_*` in the complex construction). Every scratch entry may start at an arbitrary value.

For one invocation, the complete source-to-target contract is

```text
(x, y, arbitrary side/center scratch) -> (x, y+x, same side/center scratch).
```

The eight chronological rows implement it as follows. “Subtract” and “undo” are real operations; they remove arbitrary dirty values and restore them after use.

| Row | Paid scalar action | Source/target route |
| --- | --- | --- |
| 0 | Subtract side injection | Old side scratch back out of each target |
| 1 | Subtract center scatter | Old center scratch back out of each target |
| 2 | Copy | Each source `x_T` enters its ordered side wires `A_ST` |
| 3 | Gather | `C_i += Σ_(T∋i) x_T`; complex also `C_* += Σ_T x_T` |
| 4 | Scatter | Center values enter every target; complex uses `(Σ_(i∈S) C_i-C_*)/2` |
| 5 | Side injection | Side wires enter their target with the construction's coefficients |
| 6 | Undo gather | Restore every center value |
| 7 | Undo copy | Restore every side value |

For bits, `S,T` are neighboring when `|S∩T|=1`; center coefficient is `|S∩T| mod 2`, and side injection cancels the distinct intersection-one entries. For complex values, distinct even-intersection triples are neighbors; center coefficient is `(|S∩T|-1)/2`, and side injection cancels the distinct intersection-zero and intersection-two entries. In both domains the coefficient sum is exactly `δ_ST`, so the target bank receives every independent source coordinate once. The complex halves are exact in `Z[i,1/2]`; they are not free conversions to `F_2`.

The arbitrary-dirty calculation is linear and explicit. If `a,c` are the initial side and center vectors and `V,J,G,R` denote copy, side injection, gather, and scatter, then rows 0–1 contribute `-Ja-Rc`; rows 2–3 change scratch to `a+Vx,c+Gx`; rows 4–5 contribute `R(c+Gx)+J(a+Vx)`; rows 6–7 restore `c,a`. The surviving target term is `(JV+RG)x=x`. Across the three stage schedule the full bank output is `(X,Y) ↦ (-Y,X)` over `R_c` and `(X,Y) ↦ (Y,X)` over `F_2`; every auxiliary value is restored.

The actual Section 03 scale is not a toy: `I=3v²=78,440,670,000` invocations; a fixed triple has `z_b=13,968` bit neighbors and `z_c=147,731` complex neighbors; there are 100 bit centers and 101 complex centers per invocation. The resulting fixed role counts are `W_b=177176569091445000000` and `W_c=1873807244643542670000`. The edge residual table has source/target edges as well as center/side edges: for `a=dim A=h^(j−1)`, `f=h^(3−j)`, and `P` the new `h`-dimensional center factor, representative residual dimensions are `X:in→2=(a−1)(h−1)`, `X:2→3=h−1`, `Y:0→1=(a−1)(h−1)`, `Y:4→5=h−1`, center `source→1=(a−1)h`, `1→3=3→4=4→6=h`, side `source→0=a−1`, `0→2=(a−1)(h−1)+1`, `2→5=h−2`, `5→7=1`, and scratch `last→sink=ah(f−1)`. The only decreasing edge is center `3→4`, with loss `h`; changing center and side together therefore changes both the data-edge residuals and the center-loss budget.

Section 04 makes these residuals matter physically: an edge operation of rank `r` invokes `r` smaller full-array interchanges, each on one role stream of volume `V/W`. The complete recurrence is `F_k ≤ (s/W)F_(k−1)+O(1)`, where `s` is the sum of all edge ranks. Row splitting, copying, merging, fixed-tape parking, and cleanup each cost `O(V)` at the parent and are not removed by a scalar identity. Thus a claimed saving must delete or replace a complete recursive child of stated width and stream volume; changing a coefficient table alone does not reduce `s`.

The exact multiplication boundary remains `a,b ∈ [0,2^N) ↦ ab ∈ [0,2^(2N))`, or equivalently radix-`β` digit vectors mapped to all `2n−1` exact convolution coefficients followed by carry recovery. Section 06's packed signed polynomial route explicitly pays four ordinary integer products and then extracts centered coefficients and carries. The local transfer candidate below does **not** implement this full product boundary; it is a test of whether a source/target child block inside the supplier can be coalesced. No integer product is hidden in its decoder.

### Retained bit and complex child ledgers

The applicable pinned finite supplier profiles are PR 187's bit profile and PR 193's complex profile as imported by PR 203: [bit input](https://redirect.github.com/CrocSwap/integer-mult-bounds/blob/d2873e20750d0949d2ad75cbc4cd82b5b1a74e84/research/percent-exponent-architecture/inputs/bit-pr187.json), [complex input](https://redirect.github.com/CrocSwap/integer-mult-bounds/blob/d2873e20750d0949d2ad75cbc4cd82b5b1a74e84/research/percent-exponent-architecture/inputs/complex-pr193.json). These are smaller retained supplier profiles (`h=24,m=72,v=1760` bit; `h=22,m=66,v=1320` complex), not the `h=100` Section 03 counting example above.

The source/target data submultisets are exact. PR 203 counts three copies of the source and target itineraries plus `2v` rank-two complement children:

| Role | Source histogram | Target histogram | Full data histogram `n_r` |
| --- | --- | --- | --- |
| Complex | `1:1320, 2:1320, 18:1320` | `0:6270, 1:3960, 18:1320` | `1:15840, 2:6600, 18:7920` |
| Bit | `1:1760, 2:880, 20:880, 22:880` | `1:4400, 20:880, 21:880` | `1:18480, 2:6160, 20:5280, 21:2640, 22:2640` |

The full paid child histograms (including auxiliary/center calls) are encoded in the checker and pinned input files. Their exact aggregates are:

| Role | `m` | `W` | `Σ_r n_r r` | `D=mW−Σ_r n_r r` |
| --- | ---: | ---: | ---: | ---: |
| Complex | 66 | 12052 | 794112 | 1320 |
| Bit | 72 | 21108 | 1517840 | 1936 |

The complete raw multiplication endpoint includes all source coefficients and output coefficients; the histograms here count only the finite supplier's full recursive child transfers by child width. They do not make scalar center or side injections free.

## COUPLED_IDENTITY

### Candidate: re-route two independent source coordinates through one center and one side channel

Let `x=(x_1,x_2)ᵀ ∈ K²` be two independent source values, `y=(y_1,y_2)ᵀ ∈ K²` two independent target accumulators, and `d_c,d_s ∈ K` arbitrary dirty center and side state. The required typed map is

```text
E_A(x)=x; E_B(y)=(y,d_c,d_s);
P(x,y,d_c,d_s)=(x,y+x,d_c,d_s).
```

The target decoder must produce both exact target values and restore both dirty inputs for every `x,y,d_c,d_s`. Instead of the direct routes `x_1→y_1`, `x_2→y_2`, use the following changed source/target paths.

Over the bit field `K=F_2`, set

```text
U_c=(1,1),  V_c=(1,0)ᵀ;
U_s=(0,1),  V_s=(1,1)ᵀ.
```

Then `V_c U_c + V_s U_s = I_2` in `F_2`. The center gathers `x_1+x_2` and scatters it to target 1; the side channel reads `x_2` and scatters it to both targets. Their target effects add to `(x_1,x_2)` without aliasing the two source inputs.

Over the complex scalar ring `K=Z[i,1/2]`, set

```text
U_c=(1,1),    V_c=(1/2,1/2)ᵀ;
U_s=(1,-1),   V_s=(1/2,-1/2)ᵀ.
```

Again `V_c U_c + V_s U_s = I_2`, now by the exact symmetric/difference decomposition. The combined source encoder has matrix `[[1,1],[1,-1]]` with determinant `-2`, a unit in `Z[i,1/2]`; the bit encoder has matrix `[[1,1],[0,1]]` with determinant `1`. Thus the two channels jointly preserve the two independent source degrees of freedom in both domains.

For either channel `(U,V,d)`, the dirty-safe decoder is the four-update sequence

```text
y <- y - V d
d <- d + U x
y <- y + V d
d <- d - U x
```

It sends `d` back to its initial arbitrary value and changes `y` by exactly `VUx`. Applying it once to the center and once to the side yields `y+x`, with `x` untouched. These equations are a complete local source/target identity, including independent ports and dirty restoration. They change the actual data paths together with center and side operators; they are not a label/frame rewrite. The two-by-two linear decomposition is elementary, so no broad novelty claim is made for the identity itself.

### Scoped one-shot obstruction

Let a one-shot linear source/target block over a field have `q` independent source coordinates and `q` independent target outputs. Suppose every source-dependent route is carried once through a total of `k` scalar center coordinates and `s` scalar side channels, followed by arbitrary linear target decoders. Initial scratch is arbitrary and must be restored. The source coefficient of the final target update factors as

```text
A = V_c U_c + V_s U_s,
rank(A) <= k+s.
```

Terms depending on initial dirty values must cancel because the output is required for every dirty state; that cancellation does not add source rank. Exact output `y↦y+x` requires `A=I_q`, so

```text
q = rank(I_q) <= k+s.
```

For `q=2`, one scalar center channel and no remaining source-dependent side channel cannot replace two independent rank-one source/target routes. With one center and one side channel, the bit and complex constructions above attain `k+s=2`, so the bound is sharp. Reusing a center in another source pass counts as another channel traversal; a vector-valued child of width `2r` is outside this scalar-child statement and must be costed on its own. This coupled source/target statement has a different scope from the PR 203 center-basis result: it permits arbitrary source encoders, target decoders, and a changed side path, and asks for the complete identity map rather than a factorization of the old fixed center matrix.

## PAID_SCREEN

In Section 04's scalar-channel model, the old two-coordinate identity uses two rank-one recursive child units, each on its own role stream of volume `V/W`. The coupled candidate still has two independent rank-one channels: one center child and one side child. It changes which source combination reaches which target, but it replaces the two old child problems with two new complete child problems. It saves **zero** children and has no reduction in rank mass. The four dirty-safe updates per channel also keep the pre-cancellation and cleanup work paid. A proposed one-child replacement fails the theorem; a single wider child would need a new child type, width, recurrence, and decoder charge.

For the retained PR 187/193 profiles, recompute the PR 203 moment with natural logarithms:

```text
D = mW - Σ_r n_r r
C = Σ_r n_r r ln(m/r)
```

The checker computes a rigorous rational lower bound `C_lo` by reducing each `m/r` to `[1,2)` and truncating the positive series `ln z = 2 Σ_(j≥0) t^(2j+1)/(2j+1)`, `t=(z−1)/(z+1)`, after 80 terms. When the power-of-two exponent is negative, it uses a rational tail upper bound for `ln 2` before multiplying by that negative exponent; this preserves the lower-bound direction. Therefore `D−C/99 ≤ D−C_lo/99`:

| Profile | Full `D` | Full `C_lo` | Upper bound for `D−C/99` |
| --- | ---: | ---: | ---: |
| Complex | 1320 | 1881413.992825956 | −17684.181745717 |
| Bit | 1936 | 2883179.705656429 | −27187.027329863 |

PR 203's favorable data-only relaxation discards every auxiliary entropy cost and grants zero center loss, so it uses `D≤2v` but retains all source/target data calls:

| Profile | Favorable `D≤2v` | Data `C_lo` | Upper bound for `D−C/99` |
| --- | ---: | ---: | ---: |
| Complex | 2640 | 297743.813142666 | −367.513264067 |
| Bit | 3520 | 395619.425474255 | −476.155812871 |

The retained assembly requires `a>1/99` as a necessary condition for `κ≥0.01`, hence `D−C/99>0` for its relevant ordinary supplier. It fails even under the favorable data-only relaxation for both roles. These are strict necessary-condition failures for the pinned histograms, not a sufficient test for improvement and not a theorem about a changed global recurrence. The candidate above does not delete a child or produce a changed profile, so the current `D,C` remain the applicable screen; no new `κ` follows.

The pinned PR 203 package reports the same data-only ceilings, `<0.008866683` complex and `<0.008897440` bit, and explicitly limits them to retained data itineraries. Its `verify.py --deep` was **NOT RUN** in this lane; the new standard-library checker independently reconstructs the listed ranks and verifies the coupled block and moment signs. This local check passed with `python3 -B -S research/parallel-a-typed-reduction/check_milestone3.py`.

The cost comparison remains in the scope of actual complete operations. For context, [PR 244](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/244) reports 355 recursive calls removed by retiming 353 additions while keeping the scalar sequence, and [PRs 249](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/249) and [251](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/251) charge the extra routing, selector, and cleanup reads for their dirty-entrance work. Those are physical accounting examples, not evidence that this two-channel identity saves a child.

## OBSTRUCTION_OR_WITNESS

**Result: `SCOPED_DATA_CENTER_OBSTRUCTION`.** The exact small witness proves that a changed source itinerary and changed center/side decoder can preserve all independent source and target values and restore arbitrary dirty state. The rank theorem proves that this one-shot scalar family cannot lower the two independent rank-one child units to one. Thus the candidate is a real coupled operation, but it does not meet the paid-reduction gate.

The adverse control in the checker uses `x=(0,1)`, `y=(0,0)`, and dirty value `1` with the false decoder `U=(1,0), V=(1,0)`: it restores dirty state but returns the wrong target because it aliases away the independent second source. The exhaustive bit-field check covers all center/side coefficients and all `x,y,d_c,d_s` values for the displayed exact candidate; it verifies the identity, dirty restoration, one-channel exclusion, and this adverse control.

Scope limits: the result does not exclude nonlinear operations, multiple time-separated center passes whose extra channel traversals are paid, a wider child with a separately proved recurrence, overcomplete cross-stage decoding, or a wholly new multiplication recurrence. The next useful research task is to test whether a fused width-`2r` child can carry two independent rank-one source directions for less than the two width-`r` calls after charging its encoder, decoder, dirty cleanup, and fixed-tape traffic in both the bit and complex suppliers. No claim is made that such a cheaper fused child exists.

The note and checker were prepared with substantial OpenAI Codex assistance. The finite proof and script are not independent review or formal verification of the full integer-multiplication theorem.
