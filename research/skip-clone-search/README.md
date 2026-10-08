# Issue 6: paid clone schedule search

This experiment starts from the pinned PR 54 snapshot `7210de7d0f9ccaeb64c3f60f188419e02be08d95` and its PR 53 producer `3ffd4021995c959ac02d12920e0279ae97dd03c7`. The baseline inputs are preserved here as `baseline-*`; the selected candidate is the schedule and matching under `research/skip-clones/`.

## Result

`search.py` sampled eight deterministic schedules for the final clone round. For each clone it selected one of the baseline or alternate complete continuation chains using SHA-256 of the seed, dimension, and job index. Every candidate replayed the clone invariants. A maximum-cardinality matching screen gave the same `R23=32693`, `R25=43056`, and `W=159592676` for all eight seeds. Seed `1` wins the documented tie break.

The selected schedule changes six h=23 and ten h=25 continuation chains. Its actual weighted matching was regenerated from the candidate graph. Full producer and assembly replay passed, but the exact rational `kappa=141532521/3125000000000` is unchanged from PR 54. No improvement is claimed.

This is a finite sample of final-round chain choices, not an exhaustive schedule search or an optimality proof. Changing the first clone round invalidates the second round's stored pre-matching and needs a fresh intermediate matching and clone schedule; that search is outside this experiment. The weighted matching score is a discovery aid only. The selected links are checked independently by the producer and exact witness.

## Reproduce

The weighted matching discovery step uses the repository's existing NumPy/SciPy optimizer and C++ profiler. The exact replay uses the repository's normal producer and witness.

```sh
python3 research/skip-clone-search/search.py
python3 research/skip-clones/pin_sources.py
python3 research/skip-clones/producer.py --work-dir build/issue6/generation --output build/issue6/producer-generation.json --write
python3 research/skip-clones/pin_sources.py
python3 research/skip-clones/witness.py --output research/skip-clones/certificate.json
make skip-clones-verify
```

`screening.json` records all eight schedules, their source hashes and screen values, the selected schedule hash, and the regenerated matching hashes. `replay-receipt.json` records the final exact replay and artifact hashes. The final `make` target also runs the focused clone tests.

The baseline source ledger and clone jobs are retained in `baseline-SOURCE.json` and `baseline-clone-jobs-{23,25}.json`; no upstream producer or order layout is changed. Primary sources: [PR 53](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/53), [PR 54](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/54), and [Issue 6](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/6).
