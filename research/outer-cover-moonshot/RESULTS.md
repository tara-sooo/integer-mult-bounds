# Results

**Primary status: `GEOMETRY_IDENTITY_FAILS`.** The one candidate tested keeps only even-parity selectors in each paired-coordinate cube. At p=4 its frozen `B_block` is `I_4`, so `K=I-B_block=0` and `(K^2-I)[000,000]=-1`. It cannot reuse the pinned local involution or its dirty-frame proof.

## Evidence

- **FAST source/proof audit: PASS.** Read [Issue 24](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/24), then [Issue 23](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/23) and its pinned `research/section4-child-identity/RESULTS.md` at [fork commit](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/267c24dfa448fbf43fa68b7d2cfdd5f9580be458). Inspected the immutable source trees for [the three-stage baseline](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/130), [the paired-cube baseline](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144), and [the separately pinned balanced comparison](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/163). Relevant source hashes and preserved notices are in [SOURCES.md](SOURCES.md).
- **FOCUSED exact p=4 audit: PASS for the frozen baseline; exact fail for the candidate.** The checker verifies all four eight-port cubes, coordinate incidence, every rational `B/H/K` entry, `K+H+B=I`, `K=(P-A)/2`, `K^2=I`, signed source channels, and required off-diagonal source-target orthogonality. It also checks the copied-center spans/scatter, per-port data-cover involutions and endpoints, the three signed shears, separate orthogonal h-blocks, raw dirty restoration, raw gauge operator equations and width-two ambient complement.
- **Adverse controls: PASS.** Deleting the antipodal signed read gives `K_bad^2[000,000]=3/4`; omitting final dirty cleanup gives `z'=z+x`; omitting one width-two complement leaves coordinates 22 and 23 outside the full endpoint. Each fails a different required identity or charge.
- **FULL: NOT RUN.** No p=12 production replay, new source producer, complete supplier histogram, moment, global CRT, full project verifier, `make verify`, broad CI or exhaustive port search was run. No p=4 bit supplier is claimed.

## Resource and command record

The fork baseline was fetched with `git fetch origin main`. The immutable source fetch selected the three redirected commit pins listed in [SOURCES.md](SOURCES.md); the source trees were inspected with `git ls-tree` and `git show`.

The exact check command was:

```sh
/usr/bin/time -v python3 research/outer-cover-moonshot/check_small.py
```

It exited 0 in `0.28 s` wall time (`0.19 s` user, `0.01 s` system) with maximum RSS `15,620 kB`, on 2026-10-09 UTC. The check creates no production or certificate files.

## Decision

**NO-GO** for the parity-sliced four-port cube under the frozen paired-cube operator. The port count would halve, but the exact local involution fails, so the candidate has no complete data action, dirty restoration, legal child profile or paid moment. Do not carry the nominal `2v` count decrease into a histogram.

**GO** only for a later outer geometry that first supplies a new exact local decomposition and proves its port cover, signed source/target orthogonality, arbitrary-dirty action, frame/shear endpoints and complete bit/complex paid profiles. The current result does not rule out other incidence systems or prove a general obstruction. No new moment improvement or `kappa` is claimed.
