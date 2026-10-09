# Exact p=4 checks

Run the standalone standard-library checker with:

```sh
/usr/bin/time -v python3 research/full-cube-stage-twist/check_small.py
```

The script uses exact rational arithmetic for the frozen incidence operators and exact integer arithmetic over `F2` for coordinate supports, permutations, orthogonality, subspaces, and basis-vector checks. An exit status of zero means the baseline contracts pass and the expected candidate obstruction is reproduced; it does not mean the candidate is legal.

## Frozen full-cube baseline

The checker constructs all four 3-subsets of four pair labels and all eight selector strings in each cube. It verifies 32 distinct weight-three ports and incidence 12 at every one of the eight coordinates. For all 1024 matrix entries it constructs the frozen `B`, within-cube `B_block`, `K=I-B_block`, and `H=B_block-B`, checks `K+H+B=I`, `K^2=I`, reconstructs every signed cross-cube `H` source coefficient, and verifies orthogonality of every nonzero off-diagonal `B/H/K` read.

This internal algebra is intentionally unchanged by the candidate. The earlier even-parity half-cube from [Issue 24's result](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/6cb527acd8f96019638bf33f520db333d9b26031) is recorded by a separate external-control assertion: its frozen `B_block=I4`, `K=0`, and `K^2 != I`. It is not the Issue 25 candidate.

## Routes and active blocks

For each of four cubes and three stages, the checker tests its explicit 24-coordinate permutation matrix against `H^T H=I` over `F2` and tests both compositions with its explicit inverse. These twelve right-multiplication maps are group-wide bijections because `gH H^-1=g` and `gH^-1 H=g` for every group element `g`.

The checker also asserts `Q != I` and, at logical vertex `g=I`, records the four stage-1 images: three cubes map to `I`, while `C0` maps to `Q`. For arbitrary `g`, the images are three copies of `g` and one `gQ`; they are distinct because `gQ=g` would imply `Q=I` by cancellation. The map `g -> gQ` is bijective.

This is only a per-cube map check. The pinned sharing note at [commit c8b22bc](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/c8b22bc5c10dba497ac25804e27d9647d818e2ff), `notes/paired-cube-sharing.tex`, indexes its retained physical auxiliary stock by `(g,r)`, without a cube coordinate. The candidate does not establish one-to-one aggregate occupancy for that stock. The source does not establish that a particular `r` is shared across cube components, so this is **UNRESOLVED / NOT PASSED**, not a proven collision. Any cube-split schedule, added route, or copied role stock is unpriced.

For each cube it computes the three active-block pair intersections. The baseline has all zero dimensions. The candidate has exactly one nonzero entry: `C0`, stage pair `(1,2)`, dimension one. The exact shared vector is `e8` and its self-pairing is one. The same overlap and pairing hold at every group vertex by orthogonal invariance. This is the expected focused failure; no orthogonality is claimed for the attempted full construction.

The 12 route maps cover all 32 ports at all three intended stages, or 96 port-stage visits. Every data bank retains its two coordinate complements `e22,e23`, giving two width-two children per port (64 complement children, rank mass 128).

## Data shears and exact endpoint frames

For every port `q`, the checker uses `E0=A perp B perp C` with dimensions `8+7+7=22`, and forms `A intersect q-perp` from an exact `F2` basis. It checks equality of adjacent spaces, not only matching dimensions:

| Stage | X input -> output | Y input -> output |
|---|---|---|
| 1 | `<q>` -> `B + <q>` | `0` -> `B` |
| 2 | `B + <q>` -> `A + B` | `B` -> `(A intersect q-perp) + B` |
| 3 | `A + B` -> `E0` | `(A intersect q-perp) + B` -> `E0 intersect q-perp` |

The dimensions are respectively `1 -> 8`, `8 -> 15`, `15 -> 22` for `X`, and `0 -> 7`, `7 -> 14`, `14 -> 21` for `Y`. The signed shear matrices for `Y+=X`, `X-=Y`, `Y+=X` multiply exactly to `[[0,-1],[1,0]]`, or `(X,Y)->(-Y,X)`. The checker verifies these frames and the signed product for all 32 original ports.

## Arbitrary-dirty core and controls

Use the representative 24-coordinate maps `M=I+E_(0,1)`, `J=M^-1=I-E_(0,1)`, and `V=I`. The source cleanup sequence is applied to arbitrary `(y,z,x)`:

```text
y <- y - J M z
z <- z + V x
z <- M z
y <- y + J z
z <- M^-1 z
z <- z - V x
```

The completed action is `(y,z,x)->(y+x,z,x)`. The checker evaluates the exact map on all 72 standard basis vectors of the state space, and also on all 72 basis vectors after conjugating by `W=diag(I24,Q,I24)` on the dirty auxiliary bank. Both maps restore arbitrary dirty `z`. The accompanying two-coordinate frame sample verifies `U=F_A T_sigma^-1`, `U^-1=T_sigma F_A^-1`, and both exact corrections:

```text
F_A U^-1         = F_A T_sigma F_A^-1
F_A (U^-1)^-1    = F_A^2 T_sigma^-1
```

These two frame identities are checked on the same exact noncommuting `2x2` matrices. This representative does not replace the source's all-subspace Clifford theorem.

The two source-faithful negative controls are:

1. The candidate's `C0` stage-1/stage-2 block overlap: `e8` lies in both and `<e8,e8>=1`, so the three-way exterior grouping fails orthogonality.
2. Omitting the last dirty cleanup gives exactly `z'=z+x`; the checker reproduces this for every basis vector and for the witness `x=e0`.

The data shear/frame checks and the isolated dirty core survive the twist. The full construction fails at the triple exterior grouping, so checking further stages of the paid construction is not justified.

## Scope limit

These exact checks cover the stated p=4 finite operators and derive the all-group route/intersection facts from algebraic identities; they do not enumerate `O(24,2)`. They do not run a production supplier, compute a candidate child histogram, compare a moment, prove a new `kappa`, or establish a general obstruction. FULL checks are not run.
