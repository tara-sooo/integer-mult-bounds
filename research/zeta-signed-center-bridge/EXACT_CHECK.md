# Exact checks

Run the deterministic standard-library checker:

    python3 research/zeta-signed-center-bridge/check_small.py

It checks the coefficient identity first, then the bounded h=8 zeta DAG inventory, and writes small_exact_receipt.json.

## Matrix results

| Case | Rows × columns | Exact coefficients compared | Result |
|---|---:|---:|---|
| Full h=4 triple space | 4 × 4 | 16 | C_B(X,Z)=B |
| All legal P_4 ports at h=8 | 32 × 32 | 1,024 | C_B(X,Z)=B |

The checker compares every Fraction coefficient, tests deterministic input vectors with denominator 8, and records a SHA-256 digest of the full integer matrix 2B in the receipt. The symbolic overlap cases k=0,1,2,3 all reduce to 1−(3−k)/2=(k−1)/2. This proves a coefficient identity, not a multiplication improvement.

## Negative controls

- **Missing X:** on the basis input e_S with T=S={1,3,5}, B[T,S]=1, while −(1/2)∑_{i∈T}Z_i=0.
- **Disjointness is not B:** for T={1,3,5}, S={1,3,7}, the overlap is 2, so B[T,S]=1/2 and the disjointness indicator is 0.
- **Dropping the half:** on that same overlap-two pair, X−∑_{i∈T}Z_i=0, not 1/2.
- **Forbidden division:** on a basis input at h=8, ∑_i Z_i=5 and X=1. Modulo 5 these are 0 and 1; the equation cannot be inverted there. Also 1/5 is not dyadic.

## Focused h=8 inventory

The checker reconstructs the pinned PR172 recurrence for h=8. It verifies chronological parent nodes, every root’s exact disjoint-mask support, and the adjoint support count for raw-dirty pre-reads. This is a finite graph and support check, not a physical compile or a replay of the new encoder/decoder wrapper.

| Quantity | Exact count |
|---|---:|
| zeta input masks / roles | 254 |
| P_4 data inputs | 32 |
| zero data contributions | 222 = 198 nontriple masks + 24 other triple masks |
| appended accumulator nodes | 1,008 |
| total graph roles R | 1,262 |
| roots / singleton roots | 254 / 8 |
| singleton source slots / P_4 inputs / zero slots | 127 / 20 / 107 per root |
| raw-dirty pre-read terms per singleton root | 253 |
| singleton-root pre-read terms | 2,024 |
| all-root raw-dirty pre-read terms | 11,846 |
| forward / inverse scalar updates | 2,016 / 2,016 |
| forward plus inverse updates | 4,032 |

The 246 nonsingleton roots remain in the pinned full word. The singleton roots are read after all eight bit passes, at node prev[255 XOR (1<<i)]. No root or input pruning is credited.

The pinned README addition formula evaluates to 8·2^7−(2^8−1)=769. The executable zeta.py recurrence appends 1,008 accumulator nodes, and its h=8 table and executable graph have R=1,262. The word.py expansion performs two forward scalar updates per accumulator, 2,016 total. This source-count discrepancy is recorded rather than reconciled by assumption.

## Address-span diagnostic

In the natural binary address field for P_4, the eight star-source supports S_i each have span rank 6, totaling 48. The eight complement supports Z_i each have rank 7, totaling 56; the full X support has rank 8. These are source-span dimensions only. The sum 56+8 is not asserted as a physical copied-center charge without a frame proof.
