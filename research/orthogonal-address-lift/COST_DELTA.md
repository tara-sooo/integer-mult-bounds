# Known and unknown cost delta

This ledger uses the fixed operator and source pins in [Issue 29](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/29), [PR 144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144), [PR 130](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/130), and [Issue 28 commit c4c9c6461d86b84774b9a8cd0b5907549275c740](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/c4c9c6461d86b84774b9a8cd0b5907549275c740). The h=10 arithmetic below is conditional formula bookkeeping; the rank-2 Gram witness is not a source-defined h=10 construction.

## Conditional geometry arithmetic

| Quantity | Pinned baseline | Conditional rank-2 dimension | Meaning and limit |
|---|---:|---:|---|
| Address dimension h | 8 | 10 | Append r=2 coordinates to the F2^8 labels, giving an ambient F2^10 cap. |
| m=3h | 24 | 30 | Direct substitution: 3(8)=24 and 3(10)=30. The h=10 value is only the same formula evaluated conditionally; it is not a measured role or copy count for this 32-port operator. |
| 3h-2, if that source formula applies | 22 | 28 | Direct substitution: 24-2=22 and 30-2=28. Applicability to a new h=10 construction is UNKNOWN / NOT RUN. |
| Target-frame dimension | 7 | 9 | The formal dimension changes by two. No source theorem supplies the two new frame directions. |
| Paired-cube parameters | p=4, h=8, 32 ports | If h=10 is interpreted as p=5, the pinned family has 80 ports | That family size does not produce a valid 32-port h=10 child or authorize reuse of p=4 ranks. |

These are the requested conditional dimension deltas, not paid costs. No child profile or recurrence follows from the arithmetic.

## Known finite quantities

| Cost item | Pinned p=4 baseline | Fixed shear and rank-2 Gram experiment |
|---|---|---|
| Scalar matrices | B=544, H=384, K=128 nonzeros; all K/H edges pass the original cap | B'=544, H'=386, K'=136; four K' and four H' edges fail the old cap. The rank-2 labels satisfy all 516 K'/H' support pairs. |
| Original support preservation | Original K and H domains contain 128 and 384 edges | Rank-2 labels pass all 128 original K and 384 original H edges, zero violations in each. B remains a distinct center channel. |
| Center work | Eight coordinate-star roots of rank six, ell=48 | Scalar B is unchanged. The lifted labels' physical readouts, incidences, and rank charge are UNKNOWN / NOT RUN; the old weight-three star proof does not apply. |
| Formal shear arithmetic | No shear in the pinned baseline | C and C^-1 are one addition and one subtraction of role 8 into role 0 at matrix level. Physical frame changes, operations, routing, and dirty restoration are UNKNOWN / NOT RUN. |
| Signed H roots | 140 root uses in the p=4 source schedule | No source-typed H' root schedule or charged implementation is established. |

## Not established or not run

| Cost item | Status | What is missing |
|---|---|---|
| W and group multiplicities | UNKNOWN / NOT RUN | No new width W, finite group, or multiplicity certificate for a lawful lift. |
| Rank-bearing edge/frame correction | UNKNOWN / NOT RUN | No source-typed edge graph, frame corrections, or rank charge for the changed supports and directions. |
| Source/target copies | UNKNOWN / NOT RUN | The 32 algebraic labels do not determine physical input copies, target copies, adapters, or invocation counts. |
| Auxiliaries and arbitrary-dirty stock | UNKNOWN / NOT RUN | No auxiliary inventory, dirty stock, signed cleanup schedule, or arbitrary-dirty restoration proof. |
| Signed phases | UNKNOWN / NOT RUN | No physical signed phase schedule for the changed address frame. |
| Prime/ring | UNKNOWN / NOT RUN | The baseline scalar coefficients lie in Z[i,1/2]; no realizing family or prime/ring choice for the proposed lift is defined. |
| Exterior grouping | UNKNOWN / NOT RUN | No exterior grouping or corresponding rank/operation accounting is specified. |
| Row and fixed-tape routing | UNKNOWN / NOT RUN | No row reserve, fixed-tape router, endpoint adapters, or routing charge for h=10. |
| Complex cost | UNKNOWN / NOT RUN | No complex physical word, paid realization, or new operation/copy/routing count. |
| Bit cost | UNKNOWN / NOT RUN | No bit-side supplier or map to rational H0=(I-J/9)/2 frames; bit roles and costs are not established. |
| Child problem and recurrence | UNKNOWN / NOT RUN | No valid frame edge graph, rank sum, parent width, child count or widths, or paid recurrence. Therefore no kappa claim is made. |

The Gram check is exact algebra only. It does not provide a source-preserving encoder/decoder contract, endpoint realization, paired-cube integrity, or a bit-side H0 compatibility proof. No old p=12 histogram, finite-group multiplicity, row reserve, fixed-tape router, or bit moment was transplanted into this candidate.
