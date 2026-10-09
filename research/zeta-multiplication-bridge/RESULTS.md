# Results

## Primary result: `REDUCTION_BRIDGE_NOT_SPECIFIED`

The [PR #172](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/172) Yates DAG computes the integer linear map $D_h[t,u]=[u\mathbin\&t=0]$, restores dirty scratch in its own word, and satisfies the binary side-root condition accepted by the complex-side graph compiler. The pinned multiplication sources use differently typed triple ports, signed half-coefficient identities, and port-indexed endpoint frames. They provide no Boolean-mask-to-multiplication-port encoder or output decoder. The proposed operators cannot be composed; no honest exact multiplication equality or real zeta-versus-source basis-vector counterexample is available.

The exact $h=3$ and $h=4$ computations reproduce both sides separately: $D_h$ is 6-by-6 and 14-by-14, while the original Section 3 local maps are 1-by-1 and 4-by-4 identities on $\mathcal T_h$. The [PR #144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144) paired-cube identity first has a valid instance at $h=8$. This is a type/dimension mismatch for the requested small cases, not evidence that all possible encodings fail.

## Evidence status

- `PROVED_SOURCE`: original Sections 3–4 source map and endpoint-frame contract; [PR #144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144)'s $H+K+B=I$, $K^2=I$, coordinate-star scatter, and dirty-source schedule.
- `PROVED_EXACT_SMALL`: exact zeta DAG matrices at $h=3,4$; exact original local motif matrices at $h=3,4$; valid $h=8$, $p=4$ paired-cube identities; exact dirty-pre-read and inverse controls; exact $H_0$ pairings.
- `COUNTEREXAMPLE`: a synthetic disjointness-only replacement on [PR #144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144)'s own $p=4$ port labels fails on one basis vector. This is not a source-backed zeta embedding and is kept out of the primary result.
- `MISSING_LEMMA`: a typed zeta-to-port map, signed replacement identity and its frame/cleanup proof; a centerless replacement for the coordinate-star $B$ scatter; and a legal bit-side frame adapter.
- `TYPE_OR_DIMENSION_MISMATCH` substatus: the raw $h=3,4$ zeta and source port spaces have dimensions 6 vs 1 and 14 vs 4.

The direct-label bit interpretation has an exact physical obstruction: disjoint triple indicators have $H_0$ pairing $-1/2$, while the source root cap requires zero. The pinned [PR #172](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/172) verifier does not execute an $H_0$ bit compiler, so this is recorded as the source-side necessary-condition failure for the literal identity interpretation, not as a global zeta impossibility theorem.

The 15–48x and κ values in [PR #172](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/172) remain conditional projections because `verify.py` supplies `dummy_bridge()` and hypothetical supplier savings. No integer-multiplication improvement is claimed.

## Run receipts

- **FAST:** `python3 research/zeta-multiplication-bridge/check_small.py` — passed in 0.23 s, max RSS 14,868 KiB; exact rational/integer matrices and assertions; small and deterministic.
- **FAST:** pinned [PR #172](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/172) `python3 research/zeta-family/verify.py` — passed in 1.57 s, max RSS 17,860 KiB. This verifies the author's finite graph, dirty replay, complex graph compiler and arithmetic projection only.
- **FOCUSED:** inspected the pinned [PR #130](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/130) and [PR #144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144) local notes and source Sections 3/4; exactly evaluated the $p=4$ paired-cube identity and $H_0$ support condition.
- **FULL: NOT RUN:** no physical bit/complex compile, huge word regeneration, recursion profile, global prime/CRT run, `make verify`, or broad CI.

The exact reproducible receipt is `small_exact_receipt.json`. The next justified mathematical task is to state and prove a lawful source/output map from the zeta mask basis to the actual multiplication ports, including the signed scalar identity and endpoint frame maps. If no such map is proposed, this audit stops here.
