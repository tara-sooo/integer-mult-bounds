# Results

Primary status: **ADDRESS_OR_FRAME_OBSTRUCTION**.

This bounded check answers [Issue 29](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/29). It reproduces the p=4 baseline and fixed [Issue 28 commit](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/c4c9c6461d86b84774b9a8cd0b5907549275c740) exactly. Rank 1 is UNSAT in both the common-label and separate-label models, with three-edge algebraic certificates. The one permitted rank 2 common-label experiment satisfies the complete partial Gram system on all 516 required K'/H' support pairs.

The rank 2 witness is not a legal PR 144 lift. Six proposed labels have weight four and self-pairing zero, while all 32 pinned source ports have weight three and norm one. More strongly, in rank 2 every appended vector preserving source norm must be 00 or 11; these vectors pair to zero with each other and cannot correct the required odd support edge. The target-frame dimensions also increase from seven to nine, and the existing source endpoints do not provide the missing directions. No source-defined encoder/decoder or arbitrary-dirty physical schedule exists for the candidate.

## Verification

| Check | Result |
|---|---|
| Exact baseline matrices, source identities, coefficients, support domains, and SHA-256 hashes | PASS |
| Issue 28 shear identities, unchanged operator, support counts, and four plus four violations | PASS |
| Rank 1 common model | FAIL as a model; exact UNSAT certificate |
| Rank 1 separate source/target model | FAIL as a model; exact UNSAT certificate |
| Rank 2 common partial Gram constraints | PASS; explicit 32-label witness checks all 516 support pairs |
| Rank 2 labels on original baseline K/H supports | PASS; 128 K and 384 H edges checked, zero violations in each; B kept separate |
| Source port injectivity and lifted address-span form | PASS; 32 distinct labels, span and Gram rank 10 |
| Existing paired-cube and norm-one geometry | FAIL; six lifted labels are weight four and isotropic |
| Existing source/target endpoint and arbitrary-dirty realization | NOT RUN; no source-defined physical lift |
| Separate rational bit-side H0 supplier compatibility | NOT RUN; no bit-side map is defined |
| Paid child profile, recurrence, full proof, and $\kappa$ | NOT RUN; no paid candidate recurrence exists |

The exact check is the standard-library script [check_small.py](check_small.py); its deterministic receipt is [receipt.json](receipt.json). Run:

~~~sh
python3 research/orthogonal-address-lift/check_small.py
~~~

Measured run: 0.17 seconds elapsed, peak RSS 21,568 kB. SHA-256:

| Artifact | SHA-256 |
|---|---|
| check_small.py | 3f7e3d7aae4af6aec59587b148629ead397f3b55bbb4d43582a7a1ad4eb3a6b4 |
| receipt.json | 0336cea880cca5eb62b85a173976bbf6c4cb8d5b8d865fee0ba15dbc6d47e594 |

The check is FAST and finite. No whole-repository verify, large CRT regeneration, full group enumeration, full bit word, or full recurrence proof was run. No multiplication improvement or $\kappa$ is claimed.
