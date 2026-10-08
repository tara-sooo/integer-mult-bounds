# PR 54 pinned integration baseline

This map supports [origin issue 5](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/5). The experiment lives on branch `issue-5-pr54-baseline`, based on the immutable snapshot `chafreaky/integer-mult-bounds@7210de7d0f9ccaeb64c3f60f188419e02be08d95`. The original `main` worktree remains untouched.

PR 54 is currently open, non-draft, and unmerged. Its live head has advanced to `84eb0b067741dc2690da837743fda06d133da865`; this replay deliberately stays on the pinned snapshot. GitHub's API reports the current PR head as not mergeable against main. Status checked 2026-10-08.

## What composes in this baseline

| Layer | Pinned input and code | Boundary and evidence |
|---|---|---|
| Producer and order layout | [PR 53](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/53), commit `3ffd4021995c959ac02d12920e0279ae97dd03c7`; `research/skip-strips/skip_graph.py` | The PR 54 clone jobs are tied to this exact graph, chronology, and source hashes. The longer-climb variant from PR 52 is not silently substituted. |
| Paid clone operations | [PR 51](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/51) supplies the whole-chain source-partition method; [PR 54](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/54) pins the specialization in `research/skip-clones/cloned_graph.py` and `clone-jobs-{23,25}.json`. | Every moved continuation uses two unused earlier providers, an exact disjoint source partition, and the parent's original core/cover envelope. The 606 additions and 1,212 retained links are charged. `producer.py` replays chronology, graph support, profiles, and both dirty-state orientations. |
| Carrier matching | The selected links are frozen in `research/skip-clones/links-{23,25}.uses`; the PR 44 profiler and matching code are retained under `references/copied-fixed/pr44/` and `research/skip-strips/`. | Pinned links are checked against actual uses and admissibility. Search scores do not certify an optimum and are not proof inputs. Changing the layout or clone jobs requires a fresh matching and full replay. |
| Frames and bases | The inherited fixed `I+J` basis, corner geometry, and original rational core/cover envelopes are pinned through `research/skip-clones/SOURCE.json` and `research/copied-fixed/PROOF.md`. | PR 54 does not use PR 51's enlarged signed positive frames. Its proof establishes this conservative original-envelope specialization; the broader frame composition remains a separate proof obligation. |
| Exact exponent | `research/skip-clones/witness.py`, `certificate.json`, and `producer-receipt.json`. | The recorded finite values are `R23=32693`, `R25=43056`, `W=159592676`, and exact `kappa=141532521/3125000000000`. The witness checks 47 strict assembly conditions and seven margins after finite profile reconstruction. The all-size analytic and fixed-tape framework remains inherited. |

The combined, replayed result is PR 53's specific skip-prefix producer plus PR 54's paid clones under the original envelopes. Similar terminology, nearby exponent claims, or a dashboard lineage edge do not establish that another branch can be substituted.

## Adjacent claims and follow-ups

At the 2026-10-08 status check, PRs 51, 52, 53, and 54 were all open and unmerged. The immutable source pins used here and in the follow-ups are:

| PR | Current head at status check | Role in this map |
|---|---|---|
| [PR 51](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/51) | `ee552125fb82c1664740fcc6c5eb97cad74d6bbd` | Enlarged signed positive-frame construction; not the frame family used by this baseline. |
| [PR 52](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/52) | `5b58921c9757ffc48663ae010322c0f2a679b2ce` | Longer climbs and reordered exclusion sums; its schedule needs new clone jobs and certificates. |
| [PR 53](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/53) | `3ffd4021995c959ac02d12920e0279ae97dd03c7` | Producer/order layout used by the pinned PR 54 snapshot. |
| [PR 54](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/54) | `84eb0b067741dc2690da837743fda06d133da865` | Live PR head; this baseline uses its earlier pinned commit `7210de7d0f9ccaeb64c3f60f188419e02be08d95`. |

Separate follow-ups track clone-search improvements ([issue 6](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/6)), applying PR 54 clones to PR 52's layout ([issue 7](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/7)), and applying PR 54 clones to PR 51's enlarged frames ([issue 8](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/8)).

The Issue 6 sample search and exact candidate replay are recorded in [`research/skip-clone-search/README.md`](../../research/skip-clone-search/README.md). Eight final-round schedules tied on `R23`, `R25`, and `W`; the selected candidate's exact `kappa` equals the pinned PR 54 baseline. This is not an exhaustive search or an optimality claim.

## Reproduction and evidence boundary

Run `python3 scripts/replay_pr54_baseline.py` for the focused `make skip-clones-verify` check; add `--full` to run `make verify` as well. Each run writes command logs and an atomic JSON receipt under the ignored `build/pr54-baseline/` directory. The receipt records the pinned and checkout commits, tree, platform, runtime, status, relevant source SHA-256 values, result values, and log hashes.

The Actions workflow in this branch has read-only contents permission, pinned actions, a 125-minute job limit, an optional full-suite input, and artifact upload even after a failed check. GitHub requires a `workflow_dispatch` file to be present on the repository's default branch before it can be manually run ([GitHub documentation](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)). Thus the branch-local workflow is ready for review, but hosted dispatch needs this workflow file copied or merged to default branch. The candidate sources and generated certificates can remain isolated.

For research discovery, the [Beyond n log n dashboard](https://beyond-n-log-n.netlify.app/) exposes Timeline, Idea lineage, Field map, Contributions, and Forks views; its [source and methodology](https://redirect.github.com/Paureel/beyond-n-log-n) explain that lineage and field links do not prove composability. The dashboard is a discovery aid; primary PRs, immutable commits, source manifests, written proofs, and fresh replay remain the evidence.

Finite replay does not prove the inherited full multiplication theorem, formalize the whole machine, or establish practical runtime or global optimality.
