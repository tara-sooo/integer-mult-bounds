# Paid-cost ledger

## Pinned PR193 baseline

The baseline below is the complete complex supplier in the pinned certificate, not the width-only aggregate.

| Quantity | Value |
| --- | ---: |
| `h`, `v`, `m=3h` | 22, 1320, 66 |
| Persistent roles `W` | 12,052 |
| Rank mass `s` | 794,112 |
| Deficit `D=mW-s` | 1,320 |
| Maximum child rank | 20 |
| Source histogram per supplier copy | `1:1320, 2:1320, 18:1320` |
| Target histogram per supplier copy | `0:6270, 1:3960, 18:1320` |

The complete all-role child histogram is:

```text
1:87534, 2:39834, 3:29769, 4:12627, 5:5850, 6:4815, 7:2118,
8:4593, 9:1287, 10:2790, 11:1062, 12:3591, 13:381, 14:2226,
15:5637, 16:264, 17:243, 18:7959, 19:501, 20:66
```

The PR203 source/target data submultiset is `1:15840, 2:6600, 18:7920`, rank mass 171,600. It consists of three copies of the source histogram, three copies of the target histogram, and `2v=2640` rank-two complement children. These counts are aggregate ledgers; they do not prove per-port chronology.

At `a=1/99`, the exact baseline moment is

```text
M(a) = [sum_r n_r r (66/r)^(1/99)] / (66 * 12052)
     ~= 1.0225702651514189653
```

The displayed decimal is a diagnostic for this fixed profile, not a κ estimate.

## Width-only counterfactual (not a paid result)

For `f_a(r)=r(66/r)^a` and `a=1/99`, the isolated difference is

```text
f(1) + f(2) + f(18) - f(21) ~= 0.1085998126836288588
```

If, without evidence, all 1,320 entries of each source rank were paired port-by-port and the existing three-copy multiplier were retained, the arithmetic-only full-histogram edit would remove `1:3960, 2:3960, 18:3960` and add `21:3960`. With every other cost artificially held fixed, this would lower `M(1/99)` by about `0.0005406562197990152` while preserving rank mass. This is only the numerical motivation; it is not a legal new supplier ledger.

## Complete delta

**No complete old/new delta exists at this checkpoint.** The old ledger above is fully pinned. The new `W`, rank mass, deficit, maximum child, moment, and all-role edge histogram are undetermined because there is no identified path to replace and no compensators or gate rewrites to charge. The conditional width-only edit cannot be used as the new ledger or as evidence of a saving.
