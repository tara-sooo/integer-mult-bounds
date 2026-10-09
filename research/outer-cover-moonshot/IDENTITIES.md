# Exact identities and controls

The reproducible checker is [check_small.py](check_small.py), using only Python's standard library and exact `Fraction`/integer arithmetic. Run it with:

```sh
python3 research/outer-cover-moonshot/check_small.py
```

The p=4 positive model builds the actual eight-selector ports from four coordinate pairs and their 3-pair cubes. It checks unique/full port incidence, 12 incidences per coordinate, all 1024 cells of each rational `B`, `H` and `K` matrix, `K+H+B=I`, `K=(P-A)/2`, and `K^2=I`. It checks the signed 4-by-4 parity blocks, the source-channel reconstruction of every `H` entry, and binary source-target orthogonality for every nonzero off-diagonal `B/H/K` read. The identity `B[S,S]=1` is retained as a direct same-port data term.

For each port, the checker builds a basis of `q-perp`, copies its exact Gram matrix into two 7-dimensional banks, and verifies the two port-specific data-cover swaps are orthogonal involutions. It also checks all stage endpoint dimensions, the three signed shear product, three mutually orthogonal 8-blocks in the separate 24-dimensional auxiliary ambient space, and the rank-two full-ambient data complements.

The copied-center check verifies each actual coordinate-star source span has rank six and matches `U_i`; total center rank is `48`. Its exact scatter coefficient agrees with `B` entry by entry. The arbitrary-dirty check expands the full `(y,z,x)` state as a 6-by-6 rational transformation for the source's literal signed cleanup order. It proves for every initial `y,z,x` in that two-coordinate check that dirty `z` is restored and `y` gains `JMVx`. The raw-core matrix control independently checks `U=F_A T_sigma^-1`, `U^-1=T_sigma F_A^-1`, and both full-frame corrections `F_A U^-1=F_A T_sigma F_A^-1` and `F_A (U^-1)^-1=F_A^2 T_sigma^-1` on exact noncommuting matrices.

The check does not replay the frozen p=12 production DAG or prove the all-dimension Clifford/weighted-recursion theorem. The raw-core matrix is a compact exact check of the source's operator equation; the p=4 dirty matrix is a compact exact instance of the source's universal algebraic cleanup. The production proof and certificates remain the authority for their larger words.

## Variant and negative controls

| Control | Exact result | What it separates |
|---|---|---|
| Baseline p=4 | Pass: `v=32`, each coordinate incidence `12`, `ell=48`, `K^2=I`, all source identities pass. | Positive control for the frozen formulas. |
| Even-parity four-port variant | Fail: on cube port `000`, `(K^2-I)[000,000]=-1`. | Outer incidence/control: halving port density destroys the required K involution. |
| Delete the signed antipodal `+1/2` read | Fail: the modified baseline block has `K_bad^2[000,000]=3/4`. | Sign/read control: the antipodal phase is necessary, even with the original eight ports. |
| Omit the last `z <- z-Vx` cleanup | Fail: the arbitrary dirty output is `z'=z+x`. | Role cleanup control: clean-input scalar agreement cannot replace dirty restoration. |
| Omit a width-two data complement | Fail: endpoint support misses ambient coordinates 22 and 23. | Paid endpoint control: the codimension-two complement cannot be merged away. |

For the even-parity candidate, all within-cube distinct selectors have distance two, so `B_block=I_4`, `K=0`, and `K^2=0`. No source/target/frame theorem can repair that exact frozen identity without adding a new local operator and proving its full dirty and endpoint contract.

## Evidence run

The successful deterministic check was run as:

```sh
/usr/bin/time -v python3 research/outer-cover-moonshot/check_small.py
```

It exited 0 in `0.28 s` wall time, with `0.19 s` user time, `0.01 s` system time, and maximum RSS `15,620 kB` on 2026-10-09 UTC. No production profile, global CRT, full repository verifier or broad CI was run.
