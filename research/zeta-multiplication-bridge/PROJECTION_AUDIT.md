# Projection audit

The pinned [PR #172](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/172) `verify.py` is a small graph/profile check, not a multiplication certificate. It runs the scalar zeta replay, calls the complex-side `compile_graph`, and feeds the returned root values into the 47-constraint assembly. It does not construct a bit supplier, multiplication-word physical placement or recycling, prime/phase compiler, recursive cost profile, or a source-defined zeta-to-multiplication bridge.

Its `dummy_bridge()` sets $E=2^{200}$, semantic `strict_literal_gap=E`, $B=2^{80}+E$, $C0=32\cdot66\cdot(2^{80}+E)^2$, `C1=1`, `induction_gap=E`, and fixed odd divisor 3. It also supplies rows with degree 70,000, coefficient 100 and degree gap 69,796. The script then calls `assembly(a,b,dummy_bridge(),...)`, where $a$ is the compiled complex graph's proposed saving and $b=1.001a$. These are deliberately hypothetical supplier inputs; $b$ is slightly better than $a$, and neither is supplied by a proved bit-side construction. Passing the assembly verifies arithmetic under those assumptions only.

The exact pinned verifier was run from a detached worktree at [PR #172](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/172) commit `427b23bc79489e7b2b7548bfd434dd9670fd5c47`:

```text
h  v     R     R/v   root       kappa      x-frontier
3    6    12   2.00 3.0519e-02 2.8764e-02     48.4x
4   14    38   2.71 1.7960e-02 1.7337e-02     29.2x
5   30   100   3.33 1.2279e-02 1.1985e-02     20.2x
6   62   242   3.90 9.0809e-03 8.9189e-03     15.0x
7  126   560   4.44 7.0573e-03 6.9591e-03     11.7x
8  254  1262   4.97 5.6780e-03 5.6142e-03      9.5x
PASS: semantic evaluation, scalar word/replay with tamper controls, in-tree compiler identities, in-tree assembly
wall_seconds=1.57 max_rss_kb=17860
```

Those κ values are two-sided conditional projections under the dummy bridge and supplier assumptions. The 15–48x comparison is not a proved improvement to integer multiplication.

## Source histogram audit

The pinned `zeta.py` always returns an override for every $h\ge4$: $\{2:v,1:v(h-3)\}$. The compiler default is `Counter({2:v, h-4:v, 1:v})`. The [PR #172](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/172) README says the default is used unchanged at $h\ge7$, but the code's non-null override prevents that. The actual $h=7,8$ profiles above use the override. The verifier's `EXPECTED` entries for $h=7,8$ match the default profile values and are never asserted.

| $h$ | zeta override | override mass | compiler default after duplicate-key collapse | default mass | audit |
|---:|---|---:|---|---:|---|
| 3 | {2:6} | 12 | {-1:6, 1:6, 2:6} | 12 | override avoids negative child width |
| 4 | {1:14, 2:14} | 42 | {0:14, 1:14, 2:14} | 42 | override removes zero-width class |
| 5 | {1:60, 2:30} | 120 | {1:30, 2:30} | 90 | default loses mass because duplicate rank 1 keys collapse |
| 6 | {1:186, 2:62} | 310 | {1:62, 2:62} | 186 | default loses mass because duplicate rank 2 keys collapse |
| 7 | {1:504, 2:126} | 756 | {1:126, 2:126, 3:126} | 756 | valid override, but not the default |
| 8 | {1:1270, 2:254} | 1778 | {1:254, 2:254, 4:254} | 1778 | valid override, but not the default |

Both $h=7,8$ distributions have the required rank mass, but produce different complex roots. Recompiling the pinned graphs gives:

| $h$ | override root used by the zeta proposal | root with compiler default |
|---:|---:|---:|
| 7 | 0.007057302490755306 | 0.007315044970258092 |
| 8 | 0.0056779905241130324 | 0.005961773166219573 |

The override is more conservative for these profile roots. The discrepancy is in the description/unused expectations, not a missing rank-mass check in the actual override path. It does not supply the missing multiplication, bit, or physical interfaces.

## Remaining proof obligations

No all-size multiplication improvement follows even if a local signed identity is later proved. The paired construction still needs its bit and complex suppliers, legal prime/phase and Clifford reductions, physical placement and recycling, complete paid recursion and fixed-tape costs, and the outer reduction's frame and proof conditions. The 47 inequalities and seven margins need to be re-established with lawful supplier data; the pinned verifier checks them only after inserting `dummy_bridge()`. Full physical compilation, global prime/CRT work, recursion profiles, `make verify`, and broad CI were not run.
