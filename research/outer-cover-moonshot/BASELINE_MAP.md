# Baseline map

This checkpoint follows the outer-construction pivot in [Issue 24](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/24). The preceding result, [Issue 23](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/23), is scoped to its tested Section 4 calls: it is a reason to stop frozen child caching, not a general no-go theorem.

## Pinned constructions

| Frozen source | Role in this audit | Mathematical profile kept separate |
|---|---|---|
| [Three-stage Cayley cover](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/130), [commit](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/6a9970a530119174507904e23592fd59ede19a5d) | Data-cover geometry, three signed shears, source/target endpoints and weighted bit interface. | Complex: `h=24, v=2024, R=28705, ell=552, m=70, W0=90163, rank=6309018`, deficit `2392`, largest child `68`. Bit: `h=23, v=1771, R=28866, m=67, W0=90140, rank=6037356`, deficit `2024`. The conditional saving is `3146011/10^10`. |
| [Paired-cube and shared-core construction](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144), [commit](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/c8b22bc5c10dba497ac25804e27d9647d818e2ff) | Fixed local paired-cube identity, completed dirty cores, orthogonal shared-bank routing and selected suppliers. | Complex: `h=24, v=1760, R=26417, ell=528, m=72, W0=29937, rank=2153528`, deficit `1936`, largest child `60`. Bit: `h=23, v=1771, R=28866, ell=506, m=69, W0=32408, rank=2234128`, deficit `2024`, largest child `66`. The conditional saving is `4609169/10^10`. |
| [Balanced structural/accounting comparison](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/163), pinned [head](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/e1813796ef5c3ca38c5dd7b9e8d81b3908ff5997) | Checklist for later accounting only; it is a different construction. | Its complex profile is `m=66, W0=15681` (13041 physical roles, 15681 virtual reserve), deficit `1320`, maximum child `20`; its bit profile is `m=72, W0=26888`, deficit `1936`, maximum child `60`. No dimension, supplier, moment, or exponent from this row is combined with either preceding row. |

The p=4 audit below specializes the paired-cube formulas to `p=4`, `h=2p=8`. It is a small exact geometry check, not a new production certificate or a complete p=4 supplier profile.

## Paired-coordinate ports and exact local algebra

Use coordinate pairs `(0,1), (2,3), (4,5), (6,7)`. For each 3-subset `I` of the four pair labels, make one cube containing all eight choices `epsilon in {0,1}^3`; the port selects coordinate `2i+epsilon_i` from each `i in I`. Thus p=4 has four cubes and `v=8*binom(4,3)=32` distinct weight-three ports. Each of the eight coordinates occurs in `4*binom(3,2)=12` ports. This is complete selector incidence, not a sampling of cube vertices.

For port supports `S,T`, the checker forms the exact rational matrix

```text
B[T,S]       = (|T intersect S| - 1)/2
B_block[T,S] = B[T,S] when T,S are in the same pair-label cube, else 0
K             = I - B_block
H             = B_block - B
```

The p=4 checker verifies `K+H+B=I`, `K^2=I`, and every entry of `H` against the signed source-channel rule. In one cube, if `d` is selector Hamming distance, `B_block=(3-d-1)/2`; hence `K` is zero for `d=0,2`, `-1/2` for `d=1`, and `+1/2` for `d=3`. With `P` the antipode and `A` distance-one adjacency, this is exactly `K=(P-A)/2`. Its two parity-crossing 4-by-4 blocks have entries `+/-1/2` and orthonormal rows and columns, so the signs/phases are part of the involution.

Address orthogonality is the binary dot product `q_T.q_S=|T intersect S| mod 2`. Every nonzero off-diagonal entry of `B`, `H`, or `K` in this model has even intersection. The diagonal `B[S,S]=1` is the direct data term; it is not an off-diagonal side read. For p=4, distinct pair-label triples meet in two pair labels, so the actual `H` channel is the signed two-pair `G` channel. The checker reconstructs all 1024 target/source entries and verifies every nonzero source in that channel is orthogonal to its target.

The source/target channels remain tied to their actual support sets: for disjoint cubes `F_I/2`; for one shared pair the opposite-selector `A` half-cube sum divided by two; for two shared pairs the signed `G` channel with its source-derived selector phase. The target root schedule in the source uses counts `1,2,4,4,8,8,8` within a cube and pays the nested target widths `[h-4,1,1,1]` per port. The p=4 target dimensions are `4,3,2,1`.

The copied coordinate stars also check exactly. For coordinate `i` and partner `i^1`, the source span is

```text
U_i = {u : u_(i^1)=0 and sum_(j not in {i,i^1}) u_j = 0}, dim(U_i)=h-2=6.
```

The p=4 checker gets rank six from the real port supports for each of eight coordinates, for total copied-center rank `ell=48=h(h-2)`. It also verifies the exact scatter coefficient `B[T,S]=1/2*|T intersect S|-1/2`, equivalent to `1/2 sum_(i in T) S_i - 1/6 sum_i S_i` because every port has size three.

## Three-stage data cover, signs and endpoints

The source construction's data space is `E0=A perp B perp C` of dimension `3h-2=22`, where `dim(A)=8` and `dim(B)=dim(C)=7`. Every port vector `q` has odd weight three, hence `q.q=1` and `A=<q> perp (A intersect q-perp)`. Port-specific orthogonal involutions exchange `A intersect q-perp` with `B` or `C` while fixing `q`; therefore they send `A` to `B+<q>` and `C+<q>`. The checker realizes these swaps on a basis with the exact copied Gram form and verifies orthogonality and involution for all 32 p=4 ports.

The stage endpoint table is:

| Stage | Signed shear | Active space | X entrance -> exit | Y entrance -> exit |
|---|---|---|---|---|
| 1 | `Y <- Y+X` | `B+<q>` | `<q> -> B+<q>` | `0 -> B` |
| 2 | `X <- X-Y` | `A` | `B+<q> -> A+B` | `B -> (A intersect q-perp)+B` |
| 3 | `Y <- Y+X` | `C+<q>` | `A+B -> E0` | `(A intersect q-perp)+B -> E0 intersect q-perp` |

Adjacent endpoints agree exactly, so the retained proof has no positive-rank data connector between stages. The signed shear matrices multiply to `[[0,-1],[1,0]]`, namely `(X,Y)->(-Y,X)`. The source then applies its actual source-dependent Pauli/sign and bank normalization; it does not identify this signed interchange with `(X,Y)` for free. The p=4 core checker tests the three-shear matrix and endpoint dimensions, not a production tape replay.

The paired-cube sharing construction embeds `E0` in a separate `m=3h=24` ambient space. Its one physical auxiliary bank is routed through three mutually orthogonal 8-dimensional blocks `P1,P2,P3`. For each stage, the fixed orthogonal map `H_j` takes the local active space to `P_j`; right multiplication `g -> gH_j` is a bijection of the full group. These are auxiliary role routes, separate from the data-cover isometries and the three data shears. Each data bank retains one width-two complement child per port; the p=4 accounting category is `2v=64` children of width two. The full ambient group factor is not dropped from scalar work, row stock, or router cost.

## Raw dirty action and frame/gauge boundary

The source's completed local core is specified on arbitrary dirty contents. Its literal signed sequence is

```text
y <- y - J M z
z <- z + V x
z <- M z
y <- y + J z
z <- M^-1 z
z <- z - V x
```

It restores every initial `z` and adds `J M V x`; the p=4 checker verifies the entire state transformation matrix, including all dirty input columns, for a nontrivial exact signed `M` with `J M V=I`. Omitting the last subtraction leaves `z'=z+x` and is rejected. The retained mathematical source gives this identity for its actual producer, not just for a clean zero auxiliary.

At a prescribed gauge `T_sigma`, a completed raw core has operator `U=F_A T_sigma^-1`, and its completed reverse has `U^-1=T_sigma F_A^-1`. The full-frame corrections are `F_A U^-1=F_A T_sigma F_A^-1` or `F_A (U^-1)^-1=F_A^2 T_sigma^-1`; each pays Fourier rank `dim(sigma)`. In three orthogonal blocks the grouped exterior child has width `3 dim(sigma)`. Exact endpoint Pauli/phase reconciliation remains a charged router adapter. The p=4 matrix control checks these noncommuting operator identities on exact matrices; it does not replace the arbitrary-subspace Clifford proof or the source's production dirty replay.

All three completed core copies, source and target frontiers, copied centers, entrance-frame gauges, two width-two data complements, signed phase adapters, role/bank permutations and the finite router remain in the paid construction. The local per-vertex complex ledger is `W0=2v+R`; the complete child histogram is

```text
n_r = 3(H_r + D_r + T_r) + 2v*[r=2] + sum_(a>0) s_a*[r=3a].
```

`H_r` is local internal work, `D_r/T_r` are exact source/target fronts, and `s_a` counts entrance gauges. The group multiplicity cancels only in the normalized moment, not in router, finite scalar, or stock costs. The bit supplier and its prime/atom logic are a distinct local construction; the production figures and the p=4 unknowns are itemized in [PAID_LEDGER.md](PAID_LEDGER.md).
