# Bit-side physical gate

The retained bit-frame note in [PR #130](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/130) sets the form on triple indicators $q_T=\chi_T\in\mathbb Q^{23}$. [PR #144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144) carries the [PR #97](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/97) bit ledger with

\[
H_0=\frac{I-J/9}{2},\qquad
q_T^{\mathsf T}H_0q_S=\frac{|T\cap S|-1}{2}.
\]

The physical root frame for an output $y_T$ is $q_T^\perp=\ker(9q_T-3\mathbf1)^{\mathsf T}$. The necessary support condition is that every source direction read at this root lies in that frame. The pinned [PR #97](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/97) side outputs have support $|S\cap T|=1$, which gives exact $H_0$-orthogonality.

Zeta roots instead select supports satisfying $u\cap t=\varnothing$. Under a literal triple-to-triple label identification, disjoint triples give

\[
q_t^{\mathsf T}H_0q_u=-\frac12\ne0,
\]

so their directions are outside the physical root cap. More generally, if arbitrary nonempty mask indicators are sent directly to coordinate indicators, then for disjoint masks of sizes $r,s>0$, their pairing is $-rs/18\ne0$. The exact values $-1/2$, $0$, and $-1/18$ are reproduced in `small_exact_receipt.json`.

This proves failure of the direct identity-on-coordinate interpretation against the source $H_0$ condition. The fixed [PR #172](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/172) source does not supply an alternate map or frame adapter. Its `verify.py` imports only the binary-address `paired_cube.frames.compile_graph`, zeta word and structured assembly; it never runs an $H_0$ bit compiler. The `compile_graph` side-root assertion uses the standard binary dot product, so it cannot serve as a bit-side pass. Its README reports a “root physical compatibility” rejection, but that rejection is not reproducible from the pinned verifier; the exact underlying necessary $H_0$ condition and the direct-label failure above are source-backed.

Classification: `MISSING_LEMMA` for a lawful bit encoding and physical frame proof, with an exact conditional obstruction for literal disjoint labels. Since the multiplication semantics bridge is itself unspecified, this is not promoted to the primary `BIT_COMPILER_OBSTRUCTION` result. No guard was bypassed or treated as passed.
