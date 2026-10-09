# Two-pair bridge check

## Status

**NO_SOURCE_TYPED_BRIDGE.** Phase 0 failed at the role and source-frame map. No two-pair multiplication pilot, bit construction, dirty-scratch translation, or adverse execution test was run. This is the required stop point; it does not assert that a new multiplication architecture is impossible.

## What the pinned WHT bridge proves in its own types

[Upstream PR 209](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/209) points to the WHT theorem pinned at [commit fdfb7815c15ec43af0fb54818a6a57ae4025126b](https://redirect.github.com/jacobalansussman/wht-power-saving-lean/commit/fdfb7815c15ec43af0fb54818a6a57ae4025126b). Its abstract Bridge2 roles contain four independent bank roles \(X_1,Y_1,X_2,Y_2\), shared helper slots \(S\), and center roles \(C\), for every class \((g,t)\). The exact pre-exchange chronology is:

1. forward on pair 1: \(Y_1=y_1+x_1\);
2. backward on pair 1: \(X_1=-y_1\);
3. at equal twin frames, \(X_1\mathrel{+}=X_2\) and \(Y_2\mathrel{-}=Y_1\);
4. forward on pair 1: \(Y_1=x_1+x_2\);
5. at equal twin frames, \(Y_2\mathrel{+}=Y_1\) and \(X_1\mathrel{-}=X_2\);
6. backward then forward on pair 2;
7. after final paid climbs, \(Y_1\mathrel{-}=Y_2\) and \(X_2\mathrel{+}=X_1\).

The exact scalar identity is \(X_i=-y_i,\;Y_i=x_i\) on both pairs before the final signed exchange. The invocation contract allows arbitrary helper matrices \(Z(q)\), carries those values through the shared helper windows, and closes the helper state. This verifies a genuine two-pair signed exchange in the WHT role type; it is not merely a count of five names.

The external WHT theorem then computes the Walsh–Hadamard transform in its exact-complex RAM model. The theorem statement itself is over \(\mathbb C\), with input and output length \(2^k\), and does not state an \(\mathbb F_2\) bit supplier, the manuscript's full array \(\rho\), or a chunk-swap decoder. The finite certificate is also specifically scoped to its own live role family and frame-price semantics.

## Failed translation to the multiplication data

The manuscript's source type has one pair \((X_a,Y_a)\) per \(a\in\mathcal T^3\), with source labels \(\langle u_a\rangle,0\). A WHT bridge class has two distinct pairs with equal twin \(X\)-source lines. The source-line map \(a\mapsto\langle u_a\rangle\) is injective, so a direct map into two distinct original data pairs cannot satisfy that twin equality. Mapping both twins to one original pair aliases four independent bank roles. Mapping a twin to scratch violates its data endpoints and its fixed-scratch role permutation.

The paper also assigns fresh side and center scratch to every invocation; the WHT bridge's helper slots are shared and re-framed through five invocations. The WHT proof checks its own helper contract, but there is no map from those slots to all original \(A_{ST},C_i,C_\ast\) roles, their consumers, and their endpoints. It therefore does not establish restoration of the original multiplication's complete dirty state.

The bit-side gap is independent: the WHT circuit and theorem are over exact complex values. Since 2 is invertible in \(\mathbb Z[i,1/2]\) and zero in \(\mathbb F_2\), reducing its complex coefficients modulo two is not a valid ring homomorphism. No separate bit circuit and role-frame proof were supplied.

## Smallest missing lemma

Before any \(t=2\) multiplication execution can be checked, prove a source-typed map that:

- injects all four bridged bank roles into a complete multiplication data type, or defines and prices a changed source type with independent data values;
- identifies every twin frame at all three inter-pair gate layers and respects each pointwise gate's common frame;
- maps every source, target, spectator, side role, center, and dirty helper to a complete input/output role, with exact signed exchange and arbitrary dirty restoration;
- supplies a distinct bit network over \(\mathbb F_2\) whose all-role endpoint equation is \(M_{\mathrm{out}(\rho(w))}-M_{\mathrm{in}(w)}=I_m\);
- gives the decoder to the paper's bit-array chunk permutation and accounts for every recursive rank child and data movement.

The first bullet already fails for the natural mapping to existing roles by the source-line argument above. No guessed pairing or local \(K^2=I\) calculation repairs it. No \(t=3\) extension was attempted.
