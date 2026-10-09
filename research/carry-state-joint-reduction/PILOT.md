# Exact pilot: four-bit integer products

## Child interface and reconstruction

Set \(n=4\), \(m=2\). Each parent input is a four-bit unsigned integer;
split it into low and high two-bit words. The four children are:

| Child | A input | B input | Return | Parent use |
|---|---:|---:|---:|---|
| \(p_{00}\) | \(A_0\), 2 bits | \(B_0\), 2 bits | full 4-bit product | low window and residual |
| \(p_{01}\) | \(A_0\), 2 bits | \(B_1\), 2 bits | full 4-bit product | high window |
| \(p_{10}\) | \(A_1\), 2 bits | \(B_0\), 2 bits | full 4-bit product | high window |
| \(p_{11}\) | \(A_1\), 2 bits | \(B_1\), 2 bits | full 4-bit product | high window |

Each child is a strictly smaller exact multiplication task and is itself
computed by the same four-way recursion down to one-bit products. All
buffers start at zero; there is no scratch oracle. The root computes
\[
L=p_{00}\bmod4,\quad q=\lfloor p_{00}/4\rfloor,\quad
H=q+p_{01}+p_{10}+4p_{11}.
\]
Here \(L\) has 2 bits, each \(p_{ij}\) has 4 bits, \(q\) has 2 bits,
the cross sum has 5 bits, \(H\) has 6 bits, and \(L+4H\) is the padded
8-bit product. For every pair \(0\le A,B<16\), the algebraic identity
\[
AB=p_{00}+4(p_{01}+p_{10})+16p_{11}=L+4H
\]
proves reconstruction.

## Exact exhaustive check

Run from the repository root:

```sh
python3 research/carry-state-joint-reduction/check_pilot.py
```

The standard-library checker exhausts all 256 four-bit input pairs, checks
all 16 possible two-bit child products, verifies the recursive node widths
\((4:1,2:4,1:16)\), and compares both windows and their concatenation with
Python's exact integer product. The algebraic identity above proves the
parameterized reconstruction; the script checks the finite semantics.

For the root's physical data flow, splitting the two four-bit inputs reads
and copies 8 source bits into the four half buffers. The four child calls
each receive two two-bit words: 16 argument bits are reread from the half
buffers and 16 destination bits are written into reusable child-input
slots. Each child writes its four-bit result; across the four children the
parent reads and copies 16 result bits into its reconstruction buffers.
The parent makes one reconstruction call, returns 2 low bits and 6 high
bits, and extracts the 2-bit state from the already charged \(p_{00}\)
output. The cross-sum accumulator, child slots, parent products, and
result buffers are initialized and cleared; these constant-size
operations are the pilot instance of the linear parent charge in COST.md.

## Residual separation and adverse controls

With the high input halves zero, low two-bit pairs \((0,0),(2,2),(3,3)\)
give residuals \(q=0,1,2\). The high window must return those different
values while receiving the same high input halves. A one-bit residual has
only two states, so it cannot satisfy this interface; two bits are
necessary and sufficient for this pilot.

The checker includes three negative controls and asserts each differs from
the exact product:

| Fault | Input | Correct | Faulty |
|---|---:|---:|---:|
| omit cross child \(p_{01}\) | \(A=1,B=4\) | 4 | 0 |
| decrement boundary state \(q\) | \(A=3,B=3\) | 9 | 5 |
| leave a stale one in the low-output accumulator | \(A=0,B=0\) | 0 | 1 |

The full-pair enumeration also covers all zero, maximal, and leading-zero
inputs. `receipt.json` contains the deterministic counts and witnesses.
