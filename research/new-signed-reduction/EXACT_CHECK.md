# Exact check

Run the sole deterministic verifier with:

```sh
python3 research/new-signed-reduction/check_small.py
```

It uses only the Python standard library and writes the complete exact
receipt to `small_exact_receipt.json`. The final successful run exited 0 in
0.28 seconds with peak RSS 20,552 kB. No random search or other test suite
was run.

## Baseline: PASS

All 32 source-defined ports and all 1,024 coefficients of each matrix are
checked. The verifier confirms the direct [PR 144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144) formulas, its source
`F/A/G` construction of `H`, the star scatter for `B`, the signed
`K=(P-A)/2` identity, `K^-1=K`, `K^2=I`, and `K+H+B=I`. It checks every
nonzero `K` and `H` entry against the actual `F2^8` address dot product;
both matrices have zero violations. The same baseline pass checks coordinate
incidence 12, eight star ranks of 6 (`ell=48`), source/target rank histograms,
and the 140 H root uses. Full matrices and their digests are in the receipt
and `BASELINE.md`.

## Candidate: formal PASS, support FAIL

The selected shear has eight changed K entries and eight changed H entries.
The table lists all changed entries, including removed nonzeros:

| Matrix | Row, column | `T` | `S` | Before → after | F2 address dot |
|---|---:|---|---|---:|---:|
| `K'` | 0, 9 | `(0,2,4)` | `(0,2,7)` | `0 → -1/2` | 0 |
| `K'` | 0, 10 | `(0,2,4)` | `(0,3,6)` | `0 → -1/2` | **1** |
| `K'` | 0, 12 | `(0,2,4)` | `(1,2,6)` | `0 → -1/2` | **1** |
| `K'` | 0, 15 | `(0,2,4)` | `(1,3,7)` | `0 → 1/2` | 0 |
| `K'` | 1, 8 | `(0,2,5)` | `(0,2,6)` | `0 → 1/2` | 0 |
| `K'` | 2, 8 | `(0,3,4)` | `(0,2,6)` | `0 → 1/2` | **1** |
| `K'` | 4, 8 | `(1,2,4)` | `(0,2,6)` | `0 → 1/2` | **1** |
| `K'` | 7, 8 | `(1,3,5)` | `(0,2,6)` | `0 → -1/2` | 0 |
| `H'` | 0, 9 | `(0,2,4)` | `(0,2,7)` | `-1/2 → 0` | 0 |
| `H'` | 0, 10 | `(0,2,4)` | `(0,3,6)` | `0 → 1/2` | **1** |
| `H'` | 0, 12 | `(0,2,4)` | `(1,2,6)` | `0 → 1/2` | **1** |
| `H'` | 0, 15 | `(0,2,4)` | `(1,3,7)` | `1/2 → 0` | 0 |
| `H'` | 1, 8 | `(0,2,5)` | `(0,2,6)` | `-1/2 → -1` | 0 |
| `H'` | 2, 8 | `(0,3,4)` | `(0,2,6)` | `0 → -1/2` | **1** |
| `H'` | 4, 8 | `(1,2,4)` | `(0,2,6)` | `0 → -1/2` | **1** |
| `H'` | 7, 8 | `(1,3,5)` | `(0,2,6)` | `1/2 → 1` | 0 |

Thus `K'[0,10]=-1/2` is a named exact separator. Its source mask is 21,
target mask 73, and their common support is `{0}`, so their address dot
product is 1. The original `K[8,10]=-1/2` is legal: masks 69 and 73 share
`{0,6}`, whose parity is zero. This is a concrete field-level failure of
the frozen source/target frame cap.

| Candidate matrix | Nonzero entries | SHA-256 of doubled matrix |
|---|---:|---|
| `B'=B` | 544 | `29697b4932e26c5d3df4ee33d944032b744d8c1eafbde8fd91640a78e1e909d1` |
| `K'` | 136 | `cf97073b6e09bfe1009fb12e81465fbbbca7901fbeb2f736fbf6252cedbc334d` |
| `H'` | 386 | `84f3c637fb8912a3b1be18d580998540cd35961597625c47701b73b3638a0186` |

## Negative controls: PASS

- **Cross-cube cap:** the selected shear fails the exact cap as shown above.
- **Omitted inverse:** using `C K` instead of `C K C^-1` gives a doubled
  `(K^2)[0,8]=4` where the identity requires 0.
- **Wrong inverse phase:** using `C K C` gives doubled `(K^2)[0,8]=8`,
  also not 0.
- **Dirty undo sign:** with `J=1/2`, `M=2`, `V=1`, `x=3`, dirty value 7,
  and target 11, the correct transparent schedule returns target 14 and
  dirty value 7. Omitting the final subtraction leaves 10; using the wrong
  sign leaves 13.
- **False success guard:** `H'=I-K'-B'` makes the matrix sum true by
  definition. The verifier rejects positive status because the cap fails.
  `B'=B` has exactly the baseline B digest and is the already existing
  [Issue 27](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/27) / [PR 144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144) center identity, not new work.

## Separate bit-side check

No scalar coefficient is reduced modulo 2. The checker verifies that
`2x=1` has no solution in `F2`; hence the rational/complex half coefficients
do not themselves define a bit operator. The manuscript's separate bit-side
network has its own scalar and frame/phase interface; for weight-three
indicators its rational label pairing is `|T intersection S| - 1`. No bit
supplier or decoder was built, so the required H0 cap is **NOT CHECKED** and
no bit-side compatibility is claimed. The minimum missing lemma is an
independently typed F2/H0-legal supplier and decoder, with its restoration
and endpoint contract, for a surviving operator. That work is **NOT RUN**
after the complex support failure.

## Scope

- **FAST:** exact p=4, h=8 matrices, source identities, sign/inverse,
  address-cap audit, one deterministic shear, exact changed-entry witness,
  and negative controls — verifier **PASS**; candidate support **FAIL**.
- **FOCUSED:** candidate typed roles, dirty wrapper, phases, frames,
  odd-prime lifting and complete charge — **NOT RUN** because support fails.
- **FULL:** all-size supplier, complete child profile, moment, fixed-tape
  integration, broader verifier — **NOT RUN**.
