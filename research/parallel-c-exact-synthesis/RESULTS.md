# First checkpoint results

## Decision

The first milestone found no new multiplication operator in the selected grammar. Every surviving rank-three decomposition is a three-point evaluation/interpolation algorithm; the formulas with different fixed-basis costs are known Toom-2/Karatsuba variants.

The exact tensor search also proves a scoped structural statement: over `Q`, every rank-three bilinear decomposition of the two-limb convolution tensor is an evaluation/interpolation decomposition. Its three rank-one terms must lie in the symmetric `2 x 2` tensor subspace, so each term uses the same projective linear form on the independent A and B inputs. This rules out a different rank-three bilinear primitive for this tensor, but not higher rank, nonlinear encoders, signed/bit circuits, or other recursion architectures.

## Proved claim and typed contract

For independent integer sources `A=(a0,a1)` and `B=(b0,b1)`, the source output is the raw convolution `C=(a0*b0, a0*b1+a1*b0, a1*b1)`. For every base `B=2^n`, `A0+B*A1` times `B0+B*B1` equals `C0+B*C1+B^2*C2`. The exact checker verifies the complete bilinear tensor, including integer divisibility for any denominator-2 decoder, for every accepted candidate. A separate finite replay verifies actual integer multiplication on every two-bit-limb input.

Within the exhaustive configured search, all 56 exact spans are exactly the triples of distinct diagonal source forms. Six use denominator 1 and ten use denominator 2; 16 candidates reduce to nine cost-preserving symmetry representatives. They classify as one sum-Karatsuba, one difference-Karatsuba, and seven other Toom-2 point choices. The finite bounds, denominator histogram, full candidate list, decoder matrices, controls, environment, and timing are in `search_receipt.json`.

## Novelty and cost conclusion

The difference-Karatsuba variant makes one specific known child cheaper than sum-Karatsuba: `M(n+1,n+1)` becomes `M(n,n)` because both differences have magnitude below `2^n`. It keeps three recursive calls and adds two difference formations, two signed-magnitude normalizations, a product-sign restoration, and middle-coefficient recombination. This is a potentially useful local trade, not a new discovery and not a claimed `kappa` improvement. The smallest absent result is a fully paid recursive comparison showing that this child-width saving exceeds its signed-wrapper, copies, result precision, carry, and restoration charges at every used level.

The full source/output, algebraic/physical blocker context, and immutable upstream comparison pins are in `GRAMMAR.md`. In particular, this search does not import the preceding port or frame families as its search grammar. The modern paid-mechanism comparisons are [PR 203](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/203), [PR 231](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/231), [PR 244](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/244), and [PR 246](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/246), pinned to the commit IDs recorded in `GRAMMAR.md`.

## Checks and reproducibility

| Stage | Status | Evidence |
|---|---|---|
| FAST exhaustive exact synthesis | PASS | 41,664 triples enumerated; 56 exact spans; exact decoder checks and two adverse controls pass |
| FOCUSED recursive/full-word replay | NOT RUN | No candidate survived as a new operator with a proven full paid benefit |
| FULL project verification | NOT RUN | No integration was selected |

Reproduce from the repository root with:

```sh
python3 research/parallel-c-exact-synthesis/search.py \
  --config research/parallel-c-exact-synthesis/search_config.json \
  --output research/parallel-c-exact-synthesis/search_receipt.json
```

This run used Python 3.14.6 on Android 15 aarch64 and took 8.086582 seconds inside the search. Enumeration was deterministic and used no seed. The source baseline is [`0605a24a28836168ad29d6239b46064b892298fc`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/0605a24a28836168ad29d6239b46064b892298fc); the original source is [`adc7f1241b42e322a6451854ab7e4b4c146bf78a`](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a). Work was performed in the dedicated linked worktree and branch `issue-42-exact-operator-synthesis`. No sibling lane, fork main, upstream branch, issue, or PR was modified; no PR or external notification was created.

## Missing proof and implementation bridges

- No F₂/bit decoder follows from a rational decoder with denominator 2; the bit-side obligation is NOT RUN.
- No recursive signed-child interface, actual copy/routing schedule, scratch-restoration proof, precision supplier, or uniform recurrence was built.
- No complete comparison with the pinned paid recursion or upstream certificates was attempted. The local operand-width screen is not a physical rank ledger or a bound on `kappa`.
- The next useful experiment is the parameterized signed-child cost comparison described in `COST_SCREEN.md`, followed by an independent bit-side construction only if the fully charged child delta is favorable.

Substantive AI assistance: Codex designed and implemented the exhaustive search/checker and drafted this research record. No upstream source code was copied; existing source notices and license files were left untouched.

KNOWN_ISOMORPHISM_ONLY
