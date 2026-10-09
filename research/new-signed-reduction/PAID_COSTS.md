# Paid-cost ledger

The selected shear fails the necessary physical cap in FAST. The comparison
below records exact pinned baseline charges and the point at which proposed
charges become undefined. No candidate profile or saving is inferred.

| Item | Existing p=4 PR 144 baseline | First shear proposal |
|---|---|---|
| Typed data | 32 original source ports and 32 original target ports | Same ports intended, but moved entries fail their source-target cap |
| K/H support | 128 nonzero K entries and 384 nonzero H entries; all legal under the complex address dot product | 136 K and 386 H nonzeros; four violations in each matrix, so no legal producer |
| B and center | `B'=B` is unchanged; eight star roots, rank 6 each, copied-center sum `ell=48` | No B child is removed; Issue 27's B identity is reused exactly |
| H scalar roots | 140 source-defined root uses across four target cubes; the source graph specifies 35 per cube | No lawful H' root schedule is supplied |
| K scalar action | Four local cubes, each with two 4 by 4 Hadamard/2 parity blocks; source transitions `[2,4,1]` per port and target transitions `[4,1,1,1]` | Conjugation adds one `C` and one `C^-1` transvection on actual roles; their physical implementation and restoration costs are **UNKNOWN** |
| Rank-bearing edges / recursive children | The p=4 matrix audit has no independent all-size child histogram | No valid source-frame edge matrices, rank sum `s'`, child count or child-width multiset `n'_r`; **NOT RUN**, not zero |
| Dirty roles and signs | Original transparent word restores arbitrary dirty values; signed inverses and source subtraction are part of the charge | No source-typed `C`, `C^-1`, or K' dirty wrapper; **NOT RUN** |
| Parent frames / endpoints | Original Section 3–4 and PR 130 provide common gate frames, role endpoints and the paid routing construction | No candidate frames or endpoint identity; **NOT RUN** after cap failure |
| Complex phase / dyadic ring | The source complex construction uses `Z[i,1/2]`; its phase gates and inverse are explicitly charged | Half coefficients are rationally exact, but no new phase/frame implementation; **UNKNOWN** |
| Odd prime and denominator table | The original interchange chooses an odd prime avoiding the finite rational denominator and pivot table | No candidate rank factorization or terminal/gate table; **NOT RUN** |
| Bit supplier | Separate bit construction and its H0 form; not obtained by reducing the complex matrices | No F2 operator. `2` has no inverse in F2; the required typed H0-legal supplier is **UNKNOWN** |
| Rows, routing, tapes | The pinned Section 4 charges rank-many recursive calls plus row split/merge, spectators, fixed-tape stack and descriptor work | No candidate rank sum or row/tape schedule; **NOT RUN** |
| Normalized moment | Fixed only after a complete child multiset and parent width are supplied | No `n'_r`, `W'`, or `m'`; moment **NOT RUN** |

At the scalar algebra level the shear visibly requires two operations: add
port `b` into `a`, then subtract it back. Section 3/4 charges cannot treat
these as a free basis change. They need compatible frames at both actual
ports, source and target endpoint corrections, sign-correct inverses, and
arbitrary-dirty restoration. Since the first moved K/H support is illegal,
there is no lawful candidate edge graph on which to price those terms.

The source-defined fixed-profile control remains: if a relabeling preserves
the same complete role/frame/center/stage work and the same `n_r`, then
`(1/W) sum_r n_r (r/m)^(1-alpha)` is unchanged. No child is deleted by the
matrix identity, and no `kappa` or paid gain is claimed here.
