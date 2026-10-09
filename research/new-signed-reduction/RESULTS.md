# Results

## Primary status: `CROSS_CUBE_SUPPORT_OBSTRUCTION`

Scope is the single predeclared first-ordered cross-cube shear with
`lambda=+1`. Its exact conjugation preserves `K'^2=I` and
`K'+H'+B'=I`, but the actual `F2^8` source-target address cap fails on
`T=(0,2,4)`, `S=(0,3,6)`, coefficient `K'[T,S]=-1/2`, with address dot
product 1. Four nonzero entries in each of K' and H' violate the cap. This
is an exact obstruction to this candidate, not a global no-go for other
decompositions or encodings.

## Evidence and scope

- **FAST baseline: PASS.** All 32 source-defined ports and all exact B, H,
  K coefficients match the pinned [PR 144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144) graph and construction identities.
  `K^-1=K`, `K^2=I`, `K+H+B=I`, the source H channels, B star scatter, and
  every original K/H orthogonality check pass. Full matrices and digests are
  in `small_exact_receipt.json`.
- **FAST candidate algebra: PASS.** The exact C and C inverse are verified;
  the formal involution and matrix-sum identities hold.
- **FAST candidate legality: FAIL.** The first shear creates four illegal
  K' and four illegal H' nonzero entries. The source-target witness and the
  full changed-entry list are in `EXACT_CHECK.md` and the receipt.
- **Negative controls: PASS.** Omitted C inverse, wrong inverse phase,
  incorrect dirty undo, and false success from tautological H' or reused B
  are detected.
- **Bit-side scalar/role bridge: NOT RUN.** The exact ring check confirms
  that `1/2` is not defined in F2. The missing requirement is an independent
  typed F2/H0-legal supplier, decoder and restoration contract.
- **FOCUSED candidate implementation and paid comparison: NOT RUN** after
  the exact cap failure. **FULL integration: NOT RUN.**

The [Issue 27](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/27) result was the existing [PR 144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144) B identity in complementary
coordinates. It removes no paid K/H or center work and contributes no new
operator here. No multiplication improvement or `kappa` is claimed. Stop
candidate exploration at this scoped obstruction.
