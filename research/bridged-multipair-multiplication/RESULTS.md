# Results

## Primary status

**NO_SOURCE_TYPED_BRIDGE**

The five-stage bridge is exactly checked for two bank pairs in the pinned Walsh–Hadamard RAM project. It does not give the source-typed finite circuit required by the original integer-multiplication reduction. The natural assignment of its twin pairs to existing multiplication data pairs contradicts the original source-frame equality; using one index aliases the independent bank roles. The bit supplier and the original full-array decoder are also absent.

## PROVED from the pinned manuscript

- Section 3's completed stage sequence sends every data pair to \((-Y_a,X_a)\) over \(\mathbb Z[i,1/2]\), exchanges it over \(\mathbb F_2\), and restores each invocation's arbitrary initial private side and center scratch.
- Its array frames have explicit source/sink labels, a full-role permutation, and common gate frames.
- Section 4's actual \(\mathbb F_2\) operation is a full address-chunk interchange with spectators and row order restored. It requires the all-role endpoint equation and \(s<Wm\); each edge rank is charged as recursive swaps.
- The original source-line map \(a\mapsto\langle u_a\rangle\) is injective. Thus two distinct original data pairs cannot be WHT twins at the equal source frame, and identifying them as one pair loses independent role values.
- There is no ring homomorphism that reduces the signed dyadic scalar ring \(\mathbb Z[i,1/2]\) to \(\mathbb F_2\).

## REPORTED BY THE PINNED WHT CERTIFICATE; NOT REBUILT HERE

- The WHT theorem's input is a complex vector of length \(2^k\); its output is the Walsh–Hadamard transform in natural order.
- Its Bridge2 certificate gives two signed pair exchanges using five invocations and three equal-frame gate layers, with arbitrary helper-state contract in its own role model.
- Its \(7.474547\times10^{-4}\) saving belongs only to that exact-complex RAM WHT statement. It is neither an integer-multiplication \(\kappa\) nor a bit-side/full-array multiplication result.

## Not done

Phase 1 and Phase 2 were not entered: no multiplication \(t=2\) pilot, \(t=3\) fixture, general \(S_t\), new rank/copy/center ledger, or \(\kappa\) estimate was produced. The missing typed embedding theorem is listed in [BRIDGE.md](BRIDGE.md) and the necessary scaling statement in [SCALING.md](SCALING.md).

No full WHT Lean build, upstream supplier rebuild, physical compiler run, exhaustive verifier, fixed-tape reconstruction, or all-size analytic transfer was run. Those checks cannot answer the missing source-role map.
