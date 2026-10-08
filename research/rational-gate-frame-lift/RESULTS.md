# FAST result

**Outcome: `LOCAL_FRAME_LIFT_SUPPORTED`.** PR 63's inherited rational envelope basis and exact projector formula support a concrete local frame assignment for the h=23 `FSa -> Y2` gate. The lift into `m=575` is constructed here with `Q^575 = Q^23 tensor Q^25` and one source-defined h=25 triple line; no 575-dimensional per-gate matrix is serialized. This corrects the interpretation of the Issue 15 result: rational matrices are mathematically derivable from the pinned source even though they are not serialized per event in the rank-pair word.

## Exact check

```sh
python3 research/rational-gate-frame-lift/check_local.py
```

Recorded result:

```text
PASS: rational projectors (including PR63 conjugate formula), nestedness, common-frame commutation, and exact edge ranks
h=23 ranks: dim(FSa)=10, dim(Sb2)=10, dim(Y2)=14; Q-edge ranks=(4,4,0)
Q^575 lift via one h=25 triple line: edge ranks=(4,4,0); GF(2) rank(S-I)=1 (rejected as an edge rank)
PASS: mixed per-port frames fail the XOR commutation check
Limit: validates the recorded logical gate data, not its physical-word event ID or global endpoints
```

The h=23 logical graph was regenerated directly from the frozen PR 63 `pair_graph.py` and its small Python dependencies to locate this one source use. No frame compiler, physical-word serializer, profile generator, CRT pass, or full build was run. The exact checker materializes only 23-by-23 and 25-by-25 rational matrices; the 575-by-575 matrix is represented by its exact tensor/rank-one formula.

The Issue 13, 14, and 15 focused checkers were also rerun from their immutable worktrees and all passed. Their scope remains as stated in those checkpoints: they validate the GF(2) producer, generic Section 4 pivot, and selected-edge locator gap, respectively.

## Boundary

The local assignment proves neither a role permutation for the whole PR 63 network nor the endpoint identity `M_out(rho(w))-M_in(w)=I_575` for all physical roles. It also does not map the selected logical node/use to an event or physical slot in the frozen serialized word. The recorded `W`, rank mass, and child-width histogram remain aggregate certificate data; they are not per-edge ownership records.

- **FAST:** PASS — exact local checker and bounded logical-node locator; predecessor focused checkers PASS.
- **FOCUSED:** NOT RUN.
- **FULL:** NOT RUN.

No `make verify`, large CRT/profile regeneration, full compiler rebuild, or physical-word replay was run. No new child profile, `Swap` call attribution, exponent, or multiplication theorem is claimed.

Prepared with OpenAI Codex assistance. Upstream notices and contributor attributions are retained in the pinned sources.
