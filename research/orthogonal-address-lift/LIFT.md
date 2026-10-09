# Rank 2 Gram labels and source geometry

This note records the rank 2 witness from [Issue 29](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/29). The matrices remain exactly those pinned by [Issue 28 commit c4c9c6461d86b84774b9a8cd0b5907549275c740](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/c4c9c6461d86b84774b9a8cd0b5907549275c740); the source port geometry is pinned at [PR 144 commit c8b22bc5c10dba497ac25804e27d9647d818e2ff](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/c8b22bc5c10dba497ac25804e27d9647d818e2ff).

For each port $i$, let the proposed common label be $q'_i=(q_i,u_i)\in\mathbb F_2^{10}$. Use $u_i=(1,0)$ for $i\in\{0,10,12\}$, $u_i=(0,1)$ for $i\in\{2,4,8\}$, and $u_i=(0,0)$ for the other 26 ports. The same $q'_i$ labels its input/source and output/target roles. The receipt gives all vectors, confirms all 32 labels are distinct on both sides, and checks every nonzero edge of $K'$ and $H'$.

This assignment also preserves every original nonzero K/H support edge: 128 K edges and 384 H edges checked, with zero lifted-dot violations in each. B is kept separate as the center channel; it is not an edge-cap test. Its matrix remains unchanged, while reuse of the original coordinate-star root proof is still unproved for the lifted labels.

## Concrete paired-cube obstruction

The pinned construction requires every port address to be a weight-three indicator from three distinct coordinate pairs. Each original address has norm one. The proposed extension has 26 labels of weight three and six of weight four; those six have self-pairing zero. Its 10-dimensional address span and restricted Gram form both have rank 10, so the ambient form is nondegenerate. The obstruction is the source port type, not degeneracy of the full address span.

The obstruction also rules out a different rank 2 common assignment that preserves every source norm. To keep $q'_i\cdot q'_i=1$, each appended vector must satisfy $u_i\cdot u_i=0$. In $\mathbb F_2^2$ those vectors are only $(0,0)$ and $(1,1)$, and every pair among them has dot product zero. The required odd edge $(0,10)$ needs appended dot product one. Therefore no rank 2 common Gram solution can retain all 32 source norm-one lines. A source-approved global isometry cannot change this norm witness.

Treating the ambient width as ten would require five coordinate pairs in the PR 144 family, which has $8\binom53=80$ ports. The proposed map has the original 32 ports and does not define that larger family. The six extra-coordinate incidences are three per appended coordinate; original coordinate incidences are twelve each. The eight existing coordinate-star centers and their $\ell=48$ rank proof do not cover these labels.

## Roles, endpoints, and cleanup

The common label assignment is injective separately on all source ports and all target ports, with matching labels only for the same port index. It defines no map on arbitrary input values and no inverse decoder. In particular, it does not supply a physical operation for the two appended address bits or for the signed transvections $C$ and $C^{-1}$.

The old target frame is $q_i^\perp\subset\mathbb F_2^8$, of dimension seven. Its zero extension has dimension seven inside the proposed $q_i'^\perp\subset\mathbb F_2^{10}$, whose dimension is nine. Two target-frame directions and their endpoint adapters therefore need a new source construction and charge. For each nonzero $u_i$, the source line $\langle q_i\rangle$ also differs from $\langle q'_i\rangle$. The existing endpoint identities cannot be reused by padding with zero coordinates.

The PR 144 arbitrary-dirty signed cleanup applies to its typed scalar word, source injections, decoder, and inverse. No such word, decoder, phase schedule, or dirty restoration proof is defined for this lift. The matrix identities alone do not extend that contract.

## Separate bit-side frame

The [PR 130 frozen source](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/6a9970a530119174507904e23592fd59ede19a5d) gives a separate bit construction on $\mathbb Q^{23}$ with rational form $H_0=(I-J/9)/2$ and $q_S^tH_0q_S=1$ for its triples. No map from this p=4 complex address assignment to those bit-side roles or frames is defined, so the $H_0$ condition is NOT RUN. Signed halves in $\mathbb Z[i,1/2]$ are not reduced modulo two.

The smallest missing source result is a new typed, all-value encoder/decoder and physical-word theorem for the changed 32-port geometry, with source and target frames, sign-correct arbitrary-dirty cleanup, and a separately proved bit supplier preserving its rational $H_0$ frame. The current assignment cannot inherit the paired-cube theorem because it fails the necessary norm-one condition.
