# Pinned sources and attribution

This checkpoint uses immutable snapshots and does not chase later upstream
changes. Its Boolean recursion is a new, self-contained toy model.

| Source | Immutable pin and file | SHA-256 | Use |
|---|---|---|---|
| Issue 12 base | `tara-sooo/integer-mult-bounds` commit `33afe0a77afc8069ba67e5f3119e6e4219580326` | — | Dedicated worktree base; contains Issue 11's complete toy and source ledger. |
| Parent Issue 10 barrier map | commit `d0579057de829105fa1376981c75564ac0ceff34`, `research/kappa-one-barriers/BARRIERS.md` ([redirected commit](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/d0579057de829105fa1376981c75564ac0ceff34)) | `a0249c25c460b313aeeadfdc71682dbbb7f9abb26f0a20b611ba80cf54c712d3` | Recurrence/moment dependency chain, scoped ceilings, and outer proof gates. |
| Parent Issue 10 direction | same commit, `research/kappa-one-barriers/research-directions.md` ([redirected commit](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/d0579057de829105fa1376981c75564ac0ceff34)) | `0561134ea09fa8ee274972d5a948a57f246bbf0b08f1854c73876a3ac0fc62f3` | Identifies multi-type recursion and typed-interface obligations. |
| Parent source ledger | same commit, `research/kappa-one-barriers/sources.json` ([redirected commit](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/d0579057de829105fa1376981c75564ac0ceff34)) | `cdc37fa8b38d4aa19a78bf8e1cbd505a9ab57644fc2615afde4753244149189c` | Immutable primary-source pins and inherited attribution. |
| Issue 11 model | commit `33afe0a77afc8069ba67e5f3119e6e4219580326`, `research/multitype-recursion-toy/MODEL.md` ([redirected commit](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/33afe0a77afc8069ba67e5f3119e6e4219580326)) | `0d886f8277d127b790b594abfb8bea516b7931d123f134f5d7534cc5b355d04e` | Scope of the unchanged-profile routing model and its unproven adapter limits. |
| Issue 11 results | same commit, `research/multitype-recursion-toy/RESULTS.md` ([redirected commit](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/33afe0a77afc8069ba67e5f3119e6e4219580326)) | `8ed02a77049e26623917d19a46fc4d9b38782d49613fabc41182ea721cc1ca01` | Exact fixed-profile and positive-switch controls reused here. |
| Issue 11 source ledger | same commit, `research/multitype-recursion-toy/SOURCES.md` ([redirected commit](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/33afe0a77afc8069ba67e5f3119e6e4219580326)) | `00f98418c1fbec7a1494d4d1e05c4c56d395e147890d5c84c2d8d80dc3f3a3b0` | Pins/hashes and complete construction and AI-assistance attribution for its inputs. |
| Issue 11 checker | same commit, `research/multitype-recursion-toy/experiment.py` ([redirected commit](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/33afe0a77afc8069ba67e5f3119e6e4219580326)) | `270af7547c29a6d478621e37dfaac3126e86586816adbc60ba0fb2b0a38ecc1c` | Re-run for the exact pinned-profile controls; no profile regeneration. |

The new `MECHANISM.md` and `experiment.py` are authored for this checkpoint
with OpenAI Codex assistance. No PR #62/#63 source code or circuits are copied
into the toy. The construction authors and AI assistance for the parent
research remain as documented in the pinned Issue 11 source ledger. The
repository's Apache-2.0 license applies, subject to source-specific notices.
