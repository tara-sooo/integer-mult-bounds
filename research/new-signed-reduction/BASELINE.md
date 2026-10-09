# Frozen p=4, h=8 baseline

## Source-defined ports and matrices

This FAST check uses the pinned [PR 144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144) `Graph.labels` order: iterate the four
three-element subsets of pair indices in lexicographic order, then the eight
selector bit strings in lexicographic order. A port for pair set
`I=(i0,i1,i2)` and bits `e` is
`T=(2*i0+e0, 2*i1+e1, 2*i2+e2)`. Coordinates and tuples here are zero-based,
as in the source graph. There are four cubes and 32 distinct ports.

For source `S` and target `T`, the exact doubled matrices are

```text
2 B[T,S]       = |T intersection S| - 1
2 B_block[T,S] = 2 B[T,S] if T and S belong to the same cube, else 0
K               = I - B_block
H               = B_block - B
```

`small_exact_receipt.json` stores all six baseline/candidate 32 by 32
matrices as row-major doubled integers. A stored integer `n` means the exact
coefficient `n/2`. Digests are SHA-256 of compact JSON for those doubled
integer arrays.

| Matrix | Exact coefficient counts | Nonzero entries | SHA-256 of doubled matrix |
|---|---|---:|---|
| `B` | `-1/2: 224`, `0: 480`, `1/2: 288`, `1: 32` | 544 | `29697b4932e26c5d3df4ee33d944032b744d8c1eafbde8fd91640a78e1e909d1` |
| `H` | `-1/2: 192`, `0: 640`, `1/2: 192` | 384 | `412b494e4c618cd5f5767868e57d1741cfa202c3f573505db34a8ac62da74697` |
| `K` | `-1/2: 96`, `0: 896`, `1/2: 32` | 128 | `a3194574b22d6bf37add70f3b3f9989f853e25740016dc9a466678d6a315cb97` |

The checker verifies every coefficient against the pinned graph and note:
`K=(P-A)/2` within each cube, where `P` is the antipode and `A` is
distance-one adjacency. Thus `2K=P-A`, including the negative adjacency
sign, and `K^{-1}=K`, `K^2=I`, and `K+H+B=I` all hold exactly. The direct
`F/A/G` source-channel formula reproduces every `H` coefficient. The copied
coordinate-star scatter reproduces every `B` coefficient.

The complex scalar port form is over `Z[i,1/2]`; its physical address
vectors are `q_T=chi_T` in `F2^8` with the ordinary dot product. Every
nonzero `K` and `H` entry has even `|T intersection S|`, hence
`q_T dot q_S=0` in `F2`. The checker finds zero support violations in both
matrices.

## Existing B identity and prior audit

The copied-star formula is

```text
(Bx)_T = (1/2) sum_(i in T) S_i - (1/6) sum_i S_i,
S_i = sum_(S containing i) x_S.
```

Every source port occurs in three stars, so `sum_i S_i=3X`. With
`Z_i=X-S_i`, the [Issue 27](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/27) decoder `X-(1/2)sum_(i in T)Z_i` is exactly this
same `B` matrix. The equality holds coefficient by coefficient in this
receipt. [Issue 27](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/27) established an identity for the existing [PR 144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144) center;
it did not supply a new center, remove K/H work, or prove a paid saving.
See the [Issue 27 audit snapshot](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/91661785056376ecafebf8e00b0ebd7226cd23a0).

## Source and target roles

- The complex scalar type is `Z[i,1/2]`; the complex physical address space
  here is `F2^8` with its ordinary dot product. This is distinct from the
  manuscript's separate bit network, whose scalars are in `F2` and whose
  address labels use the rational form `I-J/9`.
- The 32 original source ports and 32 target ports are the typed data space.
  `B`, `H`, and `K` act on those ports; the source identity is not a claim
  about an invented untyped vector space.
- The pinned graph records source data transitions at ranks `[2,4,1]` for
  each port (`{2:32, 4:32, 1:32}`), and target data transitions at ranks
  `[4,1,1,1]` (`{4:32, 1:96}`). For `K`, the source note raises the original
  sources to a common representative, applies the signed Hadamard/2 blocks
  to opposite cube parities, then restores the original values before the
  inverse producer and source subtraction. It needs no separate K bank.
- `H` uses the source-defined `F/A/G` channels and 35 root uses per target
  cube (140 total). The group sizes are `1,2,4,4,8,8,8`.
- `B` uses eight copied coordinate-star roots. Each source span has rank 6,
  giving the pinned copied-center rank sum `ell=48` at `h=8`.
- The original Section 3 array lift gives every pointwise gate one common
  invertible frame `D_v` on all its incident roles; an edge from `u` to `v`
  applies `D_v D_u^-1`. Thus the implemented operator is
  `D_out S_Omega D_in^-1`. Source and target roles retain their specified
  endpoints, including scratch roles; common gate frames commute with the
  pointwise scalar gate.
- The transparent dirty-state word is
  `y-=JMz; z+=Vx; z=M z; y+=Jz; z=M^-1 z; z-=Vx`. For every initial
  scratch value it restores `z` and adds `JMVx` to `y`. The three-stage
  signed exchange and its inverse use the original role permutation and
  signs; a signed addition must be undone with the opposite sign.
- The manuscript Section 4 endpoint condition is
  `M_out(rho(w))-M_in(w)=I` on every role. Its rank sum, prime choice,
  recursive calls, rows, spectators, routing and fixed-tape cleanup are
  charged. The [PR 130](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/130) pinned assembly supplies its own explicit stage
  involutions and endpoint frames. Neither contract follows from a matrix
  sum alone.

## Conditions for a genuinely new paid operator

A candidate must preserve the original 32 typed endpoints and semantic
inputs/outputs. Its `K'` must be an involution or have a new exact inverse
and cleanup proof. Every nonzero `K'` and `H'` source-target edge must obey
the physical address cap, or have an independently proved adapter. `B'`
must have its own lawful center roots. Signed phases, arbitrary dirty-state
restoration, parent frames, and odd-prime interpretation must be source
faithful. The bit supplier is a separate F2 construction; `1/2` is never
reduced modulo 2.

A measurable gain would remove at least one source-defined, fully paid
recursive child or strictly improve the complete charged child multiset
after all new operators and corrections are paid. A changed support count,
matrix norm, rank, or XOR count alone is not a cost lever.

If a proposal is only an isomorphic relabeling with the same source/target
and correction frames, center copies, stage calls, and child widths `n_r`,
its normalized moment stays

```text
(1/W) sum_r n_r (r/m)^(1-alpha).
```

That fixed-profile control prevents a changed router constant from being
reported as a recursion saving.
