# Exhaustive search and exact checks

## Reproduce

From the repository root, run:

```sh
python3 research/parallel-c-exact-synthesis/search.py \
  --config research/parallel-c-exact-synthesis/search_config.json \
  --output research/parallel-c-exact-synthesis/search_receipt.json
```

The enumerator uses only the Python standard library. It is deterministic; there is no seed. `search.log` is the captured stdout and `search_receipt.json` contains every accepted candidate, orbit representatives, cost rows, controls, environment, and elapsed time.

## Finite coverage

The configured grammar has eight projective source forms, 64 ordered A/B bilinear terms, and `choose(64,3) = 41,664` unordered triples. The exact run reports:

| Check | Result |
|---|---:|
| Triples enumerated | 41,664 |
| Full-rank triples | 40,768 |
| Triples spanning all three convolution outputs | 56 |
| Candidates with decoder denominator 1 or 2 | 16 |
| Representatives after declared symmetries | 9 |
| Runtime | 8.086582 s |

The 56 exact spans are exactly the `choose(8,3)` triples formed by choosing three distinct projective forms and using the same form on the A and B roles. This is checked by set equality in the executable, not inferred from a sample. Exact decoder denominators among those 56 were: `1:6, 2:10, 3:6, 4:2, 6:12, 8:2, 9:2, 10:4, 12:4, 15:4, 60:4`. The configured search retains only denominators 1 and 2; it records the rest as excluded by the declared exact-division cost bound.

The symmetry quotient removes term order, per-form scalar sign, exchange of A and B, and simultaneous reversal of both input limbs with the corresponding output endpoint reversal. It does not call arbitrary rational source-basis transformations free. The nine retained cost representatives comprise one standard sum-evaluation Karatsuba form, one difference-evaluation Karatsuba form, and seven other three-point Toom-2 interpolation choices.

## Exact identity and actual multiplication

For term `i`, let `P_i = (p_i*a0 + q_i*a1)(r_i*b0 + s_i*b1)`. The receipt stores an integer numerator matrix `N[i,j]` and common denominator `d`. The checker proves coefficientwise that

`sum_i N[i,j] * P_i = d * c_j`

for each `j` in `0,1,2`. Thus any `d=2` division is exact for all integer source values, not just the replay points. It then evaluates all `4^4 = 256` two-bit-limb input quadruples for each of the 16 accepted candidates and checks

`c0 + 4*c1 + 16*c2 = (a0 + 4*a1)*(b0 + 4*b1)`.

All 4,096 direct multiplication comparisons passed.

## Adverse controls

Both controls are executable and required to pass:

1. **Wrong decoder:** add one to one decoder coefficient. The exact tensor check rejects it; the finite replay also finds `A=(0,1), B=(0,1)`, where the altered output is 17 and the correct product is 16.
2. **Independent source roles:** for the selected candidate, `A=(1,2), B=(3,1)` at base 4 yields product 63. Deliberately aliasing B's source values to A yields 81, so an A/A circuit does not satisfy the independent A/B contract.

The rational tensor identity is universal over integers. The two-bit replay is an additional implementation-level check. No F₂ circuit, arbitrary-dirty preservation, complex/precision lowering, or full recursive multiplier was run; rational division by 2 does not supply an F₂ decoder.
