# Milestone 2 — Phase A0 paid-work gate

**Disposition: `NO_NOVEL_PAID_ARCHITECTURE_AT_GATE`.** Neither screened architecture supplies a novel, uniform operation network with a net reduction in paid multiplication work. Phase A1 exact pilot and Phase A2 recurrence were therefore not run. This is a bounded rejection of these two proposals, not a lower bound against other source-typed reductions.

## Scope and frozen history

This work continues on branch `issue-40-source-typed-reduction`, from the existing first-wave commit [`7961b107f6097f34645c82c38adbe38990242446`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/7961b107f6097f34645c82c38adbe38990242446). The first-wave `KNOWN_EQUIVALENCE_ONLY` record and its exact checker/receipt are unchanged. No NTT/CRT, Kronecker, FFT, Toom, Section 03/04 label or frame rewrite was run again.

The source boundary is the pinned manuscript commit [`adc7f1241b42e322a6451854ab7e4b4c146bf78a`](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a), especially Sections 03, 04, and 06 as hashed in [`SOURCES.md`](SOURCES.md). The frozen results for fork Issues 27–32 and 35–39, with individual issue and immutable commit links, remain scoped as recorded in `SOURCES.md`: center/label rewrites do not delete paid work; the tested address, frame, bridge, and fibre proposals have the stated counterexamples or missing physical bridges; and Issue 32's bilinear-rank obstruction is limited to its stated class.

For a paid-work comparison, the pinned upstream heads of [PR 244](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/244) ([`a568d94f941929232ab393c7d33dc5a30e017892`](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/a568d94f941929232ab393c7d33dc5a30e017892)), [PR 249](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/249) ([`96495746c786d6d0339dbb38c7f553d4af3f88ed`](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/96495746c786d6d0339dbb38c7f553d4af3f88ed)), and [PR 251](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/251) ([`2b030c06a811473ae8ed49dce07bc7ea50b72e9e`](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/2b030c06a811473ae8ed49dce07bc7ea50b72e9e)) were read as comparison records. PR 244 reports removing 355 recursive calls per local helper by retiming 353 additions while retaining the scalar sequence and charging all five stages and downstream costs. PR 249 transports 21 dirty entrances and includes the added charts, selectors, and full eight-stage replay in its bill. PR 251 extends that to 37 entrances; it reports 148 old reads becoming 150 new reads and includes selector, chart, cleanup, and full finite accounting. These are conditional physical-cost improvements within the inherited supplier, not evidence for a new multiplication identity. Their validators were not independently replayed in this lane.

For the maps below, `U_m={0,…,2^m−1}` is the unsigned `m`-bit type and `Z_m` is the signed two’s-complement `m`-bit type.

## Hypothesis 1 — polarization to square operations

**Typed map.** For unsigned `N`-bit inputs `x,y ∈ [0,2^N)`, set `E_A: U_N → U_N × Z_(N+1)`, `x ↦ (x,x)`, and `E_B: U_N → U_N × Z_(N+1)`, `y ↦ (y,-y)`. The operator

```text
P((a_+,a_-),(b_+,b_-)) = ((a_+ + b_+)², (a_- + b_-)²),
```

where the first pre-addition is unsigned `N+1`-bit and the second signed `N+1`-bit, returns exact nonnegative values `u=(x+y)^2`, `v=(x-y)^2` in `U_(2N+2)^2`. The decoder is the exact map `D: U_(2N+2)^2 → U_(2N)`, `D(u,v)=(u-v)/4`, defined on the reachable square pairs where `u≥v`.

The identity `(x+y)^2-(x-y)^2=4xy` proves exact recovery over `Z`; divisibility by four is part of the decoder contract. Inputs remain caller-owned. `E_A` zero-extends the second copy; `E_B` owns a signed representation of `-y`; `P` owns its two pre-additions and fresh square-result slots; the decoder owns subtraction/division scratch and must clear it before return. No F₂ or complex supplier is identified with these signed integer operations.

**Difference from known architectures.** This replaces one bilinear product by a symmetric-square network and a finite-difference decoder. It is not a transform, interpolation grid, coordinate-star mapping, or frame conjugation. The identity itself is the classical polarization identity; it changes the operation type explicitly but supplies no new multiplication mechanism.

**Claimed paid work and scalable parameter.** With `N` the source width, the only prospective saving is if a square call `S(N+1)`—an upper bound for either signed or unsigned input with sign work charged—has a sufficiently cheaper all-size recurrence than a general product `M(N)`. The necessary matched inequality is

```text
2 S(N+1) + C_copy/neg(N) + C_preadd(N) + C_subtract/divide(N) + C_copy/clear(N) < M(N),
```

with `S` and `M` measured in the same fixed-alphabet model. The identity itself deletes no child: it replaces one width-`N` multiply with two width-`N+1` squares, and adds signed extension, subtraction, exact division, and scratch cleanup. No square recurrence with lower paid recursive mass was found. Improving only the square evaluation basis would fail the milestone's novelty gate.

**Cheapest fatal test.** Compare those two same-model recurrences, including widths and decoder work. As written, this does not pass the non-circular child screen: the children are `N+1`-bit squares and no independent all-size square cost or smaller recurrence is supplied. The larger child width alone is not a lower bound, but the proposal has no claimed reduction in child count or paid recursive mass. The exact identity is true, but there is no paid-work premise to test with a pilot.

## Hypothesis 2 — bit-column carry automaton with diagonal popcounts

**Typed map.** Let `x=Σ_{i=0}^{N-1} a_i 2^i` and `y=Σ_{j=0}^{N-1} b_j 2^j`, where `a_i,b_j∈{0,1}`. For `0≤k≤2N-2`, define

```text
m_k = max(0, k-(N-1)),       r_k = min(k,N-1),
d_k = Σ_{i=m_k}^{r_k} a_i b_(k-i).
```

`E^A_N(x)=(a_0,…,a_(N−1))` and `E^B_N(y)=(b_0,…,b_(N−1))` are the binary digit encoders; they read caller-owned inputs and write fresh streams. `P` forms each diagonal dot product `d_k∈[0,N]⊂Z`, for example as the integer population count of the bitwise AND of the corresponding reversed source slices; the count is over `Z`, not a coefficient interpreted in `F₂`. The decoder maintains integer carry `c_0=0` and emits

```text
t_k = d_k + c_k,   z_k = t_k mod 2,   c_(k+1) = floor(t_k/2).
```

It returns `z_0,…,z_(2N-2),z_(2N-1)`, where `z_(2N-1)=c_(2N-1)∈{0,1}`; this is the canonical `2N`-bit product. Since `xy=Σ_k d_k 2^k`, the invariant `Σ_(j<k) d_j 2^j = Σ_(j<k) z_j 2^j + c_k 2^k` proves the recurrence exact over integers. The final carry is at most one because `xy<2^(2N)`. Carry state and all slice/popcount buffers are owned by `P`/`D` and must be cleared; no dirty or reversible restoration is presumed free.

**Difference from known architectures.** This is a nonlinear Boolean/carry computation with per-output-column state, rather than a bilinear transform followed by coefficient reconstruction. It changes the immediate source-derived primitive to bitwise AND plus population count. It is not equivalent to a change of evaluation basis. The underlying pairwise-AND schoolbook multiplier and carry normalization are known, however; the formulation adds no new multiplication identity.

**Claimed paid work and scalable parameter.** A candidate word width `W(N)` would group each diagonal into `ceil((r_k-m_k+1)/W)` AND/popcount operations. With unit-cost `W`-bit primitives, the arithmetic count is `Θ(N²/W+N)`, but slice construction, routing, precision, and scratch add a separate `R(N,W)`. To beat the pinned `O(N(log N)^(1-κ))` multiplication bound, even the unit-cost arithmetic count requires `W=Ω(N/(log N)^(1-κ))`; the total condition is `Θ(N²/W+N)+R(N,W)+C_carry(N)+C_clear(N)=O(N(log N)^(1-κ))`. The target finite-alphabet tape model has no unbounded unit-cost word primitive: reading a packed `W`-bit operand and emitting its population count costs at least proportional to `W` scanned symbols in this direct implementation, before `R(N,W)`. Charging those scans restores `Θ(N²)` work. Fixed `W` only changes a constant.

**Cheapest fatal test.** First specify and charge a legal all-size `W`-bit AND/popcount implementation, including reading its `W` source bits, forming/routing each diagonal slice, and writing its count. Without that interface it changes the cost model. With the direct diagonal implementation every source pair contributes once (`Σ_k (r_k-m_k+1)=N²`), the direct network does avoid recursive multiplication calls, but replaces them with `N²` paid source-pair terms, so the total work stays quadratic. The all-ones input is the simplest adverse density control: it gives nonzero terms on every pair and defeats a sparsity-only skip argument.

## Gate result and next discriminating lemma

Both formulas have exact input/output semantics, but neither has a novel, non-circular, uniformly cheaper operator network. Hypothesis 1 is a known polarization identity with wider square children; Hypothesis 2 is a known schoolbook Boolean multiplier whose apparent compression requires an unpriced growing-width primitive. Neither compares favorably to the fully priced physical savings in PR 244/249/251, which identify actual removed calls or bank stock and retain the rest of their paid ledgers.

**No small exact pilot, checker, or receipt was added**: by the Issue's Phase A0 rule, neither candidate passed novelty and paid-work preflight. The first-wave files remain the only exact checker/receipt in this directory. FOCUSED and FULL were not run.

A useful next lemma would be an explicit family of source encoders and a decoder for an integer product whose intermediate nonlinear/bilinear network has fewer than the baseline's recursive child mass, while charging every intermediate coefficient, copy, carry, precision, and cleanup operation in the fixed-alphabet model. Issue 32 leaves bilinear classes outside its stated `q=r` obstruction open; a candidate there still needs a full exact product map and a strict matched cost inequality before any larger verifier is justified.

This A0 screen and analysis were prepared with substantial OpenAI Codex assistance. It is not an independent review or formal verification.
