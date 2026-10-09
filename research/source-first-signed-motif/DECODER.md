# Decoder boundary

Primary state: **MULTIPLICATION_PORT_TYPE_MISSING.** The exact check proves a local involution on 32 formal selector addresses. It does not define what any input value means in the source multiplication construction. The frozen source contract is summarized in [SOURCE_INTERFACE.md](SOURCE_INTERFACE.md) and pinned in [SOURCES.md](SOURCES.md).

## What is known

For the proposed labels, \(K_*^2=I\) and each nonzero \(K_*\) coefficient is binary-orthogonal. This is a local scalar-matrix fact. It does not give the source and target spaces, the role permutation, or the map from multiplication data to the 32 ports.

The manuscript's typed local identity is \(\mathcal J\mathcal V+\mathcal R\mathcal G=I\), where the side-copy path and the center path add to the identity on actual triple-indexed values. PR 144's separate arbitrary-dirty word uses \(JMV=I\), where \(V\) injects source values into dirty carriers, \(M\) is the signed carrier word, and \(J\) decodes to target values. Their domains and mechanisms differ; neither identity follows from \(K_*^2=I\).

## Missing theorem required to continue

A new outer reduction theorem must first specify genuine source and target value spaces, the five-port input/output types and their relationship to multiplication data, and a non-tautological decoder on those values. If its source and target are different representations, it must state their prescribed identification. It must then prove the correctly typed identity for its chosen construction:

- for a carrier construction on a common typed data space \(\mathcal D_*\), \(V_*:\mathcal D_*\to\mathcal Z_*\), \(M_*:\mathcal Z_*\to\mathcal Z_*\), and \(J_*:\mathcal Z_*\to\mathcal D_*\) with \(J_*M_*V_*=I_{\mathcal D_*}\); or
- for a side-plus-center construction on \(\mathcal D_*\), typed maps \(\mathcal V_*,\mathcal J_*,\mathcal G_*,\mathcal R_*\) with \(\mathcal J_*\mathcal V_*+\mathcal R_*\mathcal G_*=I_{\mathcal D_*}\).

If it uses a signed decomposition, it must derive legal, non-tautological \(B_*,H_*\) from that value-level theorem and prove \(K_*+H_*+B_*=I\) with the required source supports. A matrix identity on abstract port indices alone does not establish the multiplication interchange.

It must separately define the bit supplier and its rational \(H_0\) frame, the complex scalar ring and signs, source/target roles and frames, copies, old-value corrections, arbitrary-dirty restoration, stage routing, endpoint action, and the full-array recursion contract. Reusing PR 144 would require proving its exact triple-port hypotheses for this different family; a bijection between two sets of 32 labels is not such a proof.

## Work stopped here

No \(B_*,H_*\), source-value encoding, target decoder, or candidate \(V_*,M_*,J_*\) is proposed. No basis-vector decoder experiment is run because no source-typed map exists to test. The existence of some different outer multiplication reduction remains UNKNOWN; this result is not a no-go theorem for such a reduction.
