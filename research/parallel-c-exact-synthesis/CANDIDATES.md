# Candidate classification

## What the exact search found

The accepted 16 fixed-basis formulas fall into nine cost-preserving symmetry orbits. Two are the familiar Karatsuba sum and difference formulas. The other seven choose different three-point evaluation sets; each is still a Toom-2 evaluation/interpolation algorithm. There is no non-evaluation rank-three operator in the tested grammar.

The structural reason is short. The three target coefficient tensors span the three-dimensional space of symmetric `2 x 2` matrices. In any rank-three exact decomposition over `Q`, the three independent product tensors must span that same space. Therefore each product tensor is itself symmetric. A nonzero rank-one matrix `u*v^T` is symmetric only when `u` and `v` are proportional. Every valid child is consequently `(l(A), l(B))` for the same linear form `l` on the two independent source roles. Three distinct projective forms give an invertible quadratic evaluation matrix. This proves the evaluation form for every rank-three bilinear decomposition over `Q`, without a coefficient bound; the executable additionally verifies that the bounded grammar's exact set is all 56 choices of three distinct forms among the eight configured forms.

Any ordered triple of distinct points on the projective line is related to `{0, 1, infinity}` by a rational projective change of basis. This explains the abstract isomorphism to Toom-2. Such a change of basis is not free in an integer multiplier: its form construction, operand widths, exact divisions, and output interpolation must be paid. The search therefore keeps distinct fixed-basis formulas for cost screening while classifying their operator family as known Toom-2.

## Representative formulas

Use `e0=(1,0)`, `e1=(0,1)`, `sum=(1,1)`, and `diff=(1,-1)`. Products are listed in the search's sorted term order. The decoder matrix is in `search_receipt.json`.

### Karatsuba sum form

`p0 = a0*b0`, `p1 = a1*b1`, `ps = (a0+a1)*(b0+b1)`.

`c0=p0`, `c1=ps-p0-p1`, `c2=p1`.

This is the standard evaluation set `{0, 1, infinity}`. Both source encoders form one sum each; the middle coefficient uses two subtractions.

### Karatsuba difference form

`p0 = a0*b0`, `p1 = a1*b1`, `pd = (a0-a1)*(b0-b1)`.

`c0=p0`, `c1=p0+p1-pd`, `c2=p1`.

The identity is exact over `Z`. For nonnegative base-`B` digits, each difference has magnitude at most `B-1`, so the third child magnitude is `n` bits rather than the `n+1` bits required by the sum form. The differences have variable sign and need signed-child handling (or absolute-value plus sign restoration).

### Other retained Toom-2 points

The seven other symmetry representatives use these three forms on both source roles:

| Forms | Decoder denominator | Main cost feature |
|---|---:|---|
| `e1, (1,-2), diff` | 1 | One `n+1`-bit child and two variable-sign evaluations |
| `e1, sum, (1,2)` | 1 | Child widths `n, n+1, n+2` |
| `e1, diff, sum` | 2 | One `n+1`-bit child, one signed evaluation, exact half-decoder |
| `e1, diff, (2,-1)` | 2 | One `n+1`-bit child, two signed evaluations, exact half-decoder |
| `e1, (1,-2), e0` | 2 | One `n+1`-bit child, signed evaluation, exact half-decoder |
| `e1, e0, (1,2)` | 2 | One `n+2`-bit child and exact half-decoder |
| `e1, sum, (2,1)` | 2 | Child widths `n, n+1, n+2` and exact half-decoder |

The exact per-output decoder coefficients, which outputs actually need division after common-factor reduction, and the `n=2` digit-box bounds are stored in the receipt. No formula in this list is asserted to be cheaper than the difference form after all sign and data costs.

## Novelty result

The candidates are mathematically real multiplication identities with independent A and B data, but they are not new multiplication operators: they are all three-point evaluation/interpolation. The one candidate that changes the local child-width profile is the known difference-Karatsuba form. Thus the discovery result is **KNOWN_ISOMORPHISM_ONLY**, not a novel source-typed candidate. The rank-three theorem says nothing about rank four or higher, nonlinear bit encoders, or other recursive architectures.
