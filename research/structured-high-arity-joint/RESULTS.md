# Results: scoped linear-child obstruction

**Outcome:** `SCOPED_DECODER_COST_OBSTRUCTION`.

## Proved and checked

- The candidate class is an exact typed identity from `q` length-`m`
  convolution calls, arbitrary rational linear encoders, and a linear
  decoder to length-`rm` convolution.
- Using the classical rank `rank(Conv_s)=2s−1`, every member of this class
  needs
  `q ≥ r + ceil((r−1)/(2m−1))`. In particular, `q=r` is impossible for
  every `r≥2`.
- At `(r,m)=(3,2)`, the target tensor rank is `11`, each child rank is `3`,
  and three children have capacity `9`; four have capacity `12`. The
  `q=3` target is rejected and `q=4` remains undecided.
- The exact pilot checked all 36 coefficient basis pairs and exhaustively
  checked all 4096 pairs of six-bit integer inputs through carry recovery.
- The target is actual integer convolution on binary digits followed by
  exact base-two carries. This transfer does not make rational intermediate
  arithmetic free.
- The rank lower bound is known mathematics. The derived child-count bound
  is a scoped corollary; no new bilinear-rank theorem or multiplication
  algorithm is claimed.

## Not proved

- No encoder/decoder for `q=4` at `(3,2)` and no stronger lower bound for
  that case.
- No uniform family with low-sparsity maps, small rational heights, cheap
  normalization, or a fixed-tape generator.
- No asymptotic improvement, integer-multiplication recurrence with a
  positive `κ`, or bridge to the original manuscript's Section 4 child
  recurrence.

## Next mathematical step

Resolve the exact `q=4` tensor decomposition for `Conv_6` into four copies
of `Conv_2` with arbitrary linear pre/post maps. A positive result must
print all maps and pass the full basis-pair tensor check; a negative result
must prove the added structure beyond the rank-capacity bound. If `q=4`
survives, only then test whether the same mechanism scales with controlled
matrix sparsity and height. Do not infer an exponent until the paid
recurrence in COST.md is closed.

## Verification scope

Run from the repository root:

    python3 research/structured-high-arity-joint/check_obstruction.py

The script checks all 36 coefficient basis pairs and the exact small rank
gate. The lower-bound theorem is proved on paper from the cited classical
convolution-rank theorem; the script does not re-prove tensor rank.
`receipt.json` records the observed output and runtime. The fixed Issue 31
checker at commit
[`99f1d2b1402604bc15e9dd6f23ac3056e0a2a1a2`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/99f1d2b1402604bc15e9dd6f23ac3056e0a2a1a2)
also passed from its existing worktree. No broad arity search, transform
replay, full repository verification or production compilation was run.

This folder and its exact checker were prepared with substantial OpenAI
Codex assistance. No paper source code, data, or certificates were copied;
the mathematical sources and their license/provenance anchors are recorded
in SOURCES.md. Independent mathematical review was not performed.
