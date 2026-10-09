# Results

Primary status: **MULTIPLICATION_PORT_TYPE_MISSING**.

The pinned source indexes its source and target banks by triples; it does not define a typed five-port multiplication input/output or an actual decoder for this motif. The proposed \(K_*\) passes its exact local algebra checks, but it remains a scalar orthogonality-compatible involution. Following [Issue 30](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/30), work stops before a decoder attempt or focused physical/cost phase.

## FAST checks

| Check | Result |
|---|---|
| 32 distinct weight-five addresses and their complete 32-by-32 binary Gram matrix | PASS; every diagonal is one; address span rank is six |
| Walsh block \(A_{x,y}=(-1)^{x\cdot y}/4\) | PASS; exact \(AA^{\mathsf T}=I_{16}\) |
| \(K_*^2=I_{32}\), exact coefficients, support count | PASS; 512 directed nonzeros, each \(+1/4\) or \(-1/4\) |
| Binary cap on every nonzero \(K_*\) entry | PASS; all 512 connect opposite selector parities and are orthogonal |
| PR 144 original p4/h8 positive control | PASS; 32 weight-three ports, four cubes, \(K^2=I\), \(K+H+B=I\), counts \(K=128,H=384,B=544\), all 512 total \(K/H\) support entries orthogonal |
| Remove one Walsh sign | Expected failure observed; the exact row-0/row-1 inner product becomes \(-1/8\) |
| Remove the \(1/4\) scaling | Expected failure observed; \(AA^{\mathsf T}=16I\) |
| Add a same-parity distinct edge | Expected cap failure observed; selector pair \((0,3)\) has dot product one |
| Add a self edge | Expected cap failure observed; dot product is one, although the port's required self-norm remains one |
| Free port-index relabeling from PR 144 p4/h8 | Expected source-invariant failure observed; candidate span rank/weight are \(6/5\), control span rank/weight are \(8/3\) |
| Reuse PR 130's unchanged \(H_0=(I-J/9)/2\) on a formal five-coordinate vector in \(\mathbb Q^{23}\) | Expected reuse failure observed; its quadratic value is \(10/9\), versus one for a triple |

The checker uses only the Python standard library, integers, and Fraction arithmetic. Its deterministic machine-readable receipt is [receipt.json](receipt.json).

Run from the repository root: python3 research/source-first-signed-motif/check_small.py

## Semantic and implementation results

| Layer | State | Result |
|---|---|---|
| Local address and involution algebra | **PASS** | Exact finite checks succeeded. |
| Source-defined five-port multiplication type | **MISSING** | The frozen source data values are indexed by triples; no five-port encoding is defined. |
| Non-tautological multiplication decoder | **NOT RUN** | No source-typed candidate map exists to test. |
| Candidate bit supplier | **NOT RUN** | No map to the rational \(H_0\) roles or frames is defined. The unchanged \(H_0\) reuse check fails as above. |
| Candidate physical Walsh/4 word | **NOT RUN** | No reversible schedule, prime/precision proof, physical frame, or dirty restoration was built. |
| Candidate source/target roles, copies, corrections, routing, and endpoints | **NOT RUN** | The local matrix does not define these objects. |
| Paid child profile, recurrence, or \(\kappa\) | **NOT RUN** | No valid candidate \(W,m,s,n_r\) exists. |

**Decision:** NO-GO for advancing this local motif to a multiplication decoder or cost phase under the pinned interface. A new source-typed outer reduction theorem is the prerequisite. This is not a no-go theorem for other multiplication reductions or for the broader goal.

The exact checker was run on Python 3 in this Termux worktree. Elapsed time: **0.369779 seconds**; peak resident set: **17,880 kB**. No full repository verification, large CRT computation, full group enumeration, physical profile, production recurrence, or \(\kappa\) computation was run.
