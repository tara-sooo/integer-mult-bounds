# Source and assumption ledger

The snapshot is fixed to the commits named below. No later source was chased.
GitHub references use redirected immutable paths as required by the research
issue. SHA-256 values are of the exact pinned file bytes.

| Input | Immutable source | SHA-256 | Use / status |
|---|---|---|---|
| Fork base | `tara-sooo/integer-mult-bounds` commit `0605a24a28836168ad29d6239b46064b892298fc` | — | Issue 11 worktree base (`origin/main`). |
| Parent barrier map | `tara-sooo/integer-mult-bounds` commit `d0579057de829105fa1376981c75564ac0ceff34`, `research/kappa-one-barriers/BARRIERS.md` ([commit](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/d0579057de829105fa1376981c75564ac0ceff34)) | `a0249c25c460b313aeeadfdc71682dbbb7f9abb26f0a20b611ba80cf54c712d3` | Read; pinned dependency chain, source status, and limitations. |
| Parent multi-type direction | Same commit, `research/kappa-one-barriers/research-directions.md` ([commit](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/d0579057de829105fa1376981c75564ac0ceff34)) | `0561134ea09fa8ee274972d5a948a57f246bbf0b08f1854c73876a3ac0fc62f3` | Read; matrix recurrence and conversion obligations. |
| Parent source ledger | Same commit, `research/kappa-one-barriers/sources.json` ([commit](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/d0579057de829105fa1376981c75564ac0ceff34)) | `cdc37fa8b38d4aa19a78bf8e1cbd505a9ab57644fc2615afde4753244149189c` | Read for immutable source pins, hashes, and contributor attribution. |
| PR 58 report (considered, not selected) | `CrocSwap/integer-mult-bounds` commit `bc2f7ed4c20dc18898305ab17165c0c995cbb804`, `research/joint-dual/PROOF.md` ([commit](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/bc2f7ed4c20dc18898305ab17165c0c995cbb804)) | `dccf893d6f6e8be7d40192b7976aa6712a32d7573e382c16056b703c29780b0d` | Read; its reported normalization differs (`W = 150593466`), so it is outside the common-normalization pair. No claims copied. |
| Type A proof | `CrocSwap/integer-mult-bounds` commit `ad0f25ff7b23cff7f08ad237c2254e6ecf74257e`, `research/pair-assembly/PROOF.md` ([commit](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/ad0f25ff7b23cff7f08ad237c2254e6ecf74257e)) | `30685624bf922bb9d9f7ed4b0d367a660fe373cc9ee28fec33585bd8c7023e75` | Read; PR 62 graph and PR 57 stacked compiler context. |
| Type A profile certificate | Same commit, `research/pair-assembly/frame/frame-certificate.json` ([commit](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/ad0f25ff7b23cff7f08ad237c2254e6ecf74257e)) | `70bc8a24a5565b840a5aac845703819c89c83b8c607acae021f64cf296f10c6e` | Source of the complete Type A width histogram embedded in `experiment.py`; read only, not regenerated. |
| Type B proof | `CrocSwap/integer-mult-bounds` commit `aa7701b68540b7863d3b66a414e4319915d6282d`, `research/rank-pair/PROOF.md` ([commit](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/aa7701b68540b7863d3b66a414e4319915d6282d)) | `b61b3cd554114f6eff6747133a980ac6525d1e2cdf0607056bf421dd331a261c` | Read; PR 63 rank-first profile and remaining interface hypotheses. |
| Type B profile certificate | Same commit, `research/rank-pair/screen-certificate.json` ([commit](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/aa7701b68540b7863d3b66a414e4319915d6282d)) | `4aea9e9a2610f26f28872e2918c94c402bc93aa2203796af77021982e9120d8e` | Source of the complete Type B width histogram and pinned moment enclosure; read only, not regenerated. |

## Measured versus assumed

- **Measured from pinned finite certificates:** the two exact width histograms,
  `m`, `W`, maximum child, total rank, deficit, each source saving, and each
  source moment enclosure. The script rechecks rank/deficit identities and
  recomputes both moments at a common rational exponent with its own rational
  log/exponential intervals.
- **Toy-only assumptions:** both types can be selected recursively at every
  child; all produced children retain their pinned sizes and are assigned
  exactly once; a conversion consumes a fixed fraction `delta` of the same
  normalized recursive work. Values `delta = 0`, `1/10^10`, and `1/1000` are
  scenarios, not measured costs.
- **UNPROVEN / not assumed true:** actual A-to-B or B-to-A compatibility,
  restoration of dirty scratch across the type boundary, tape-layout and
  ownership legality, and preservation of the complete outer assembly.

PR 58 is retained as a considered pinned input but not used in the numerical
operator because its reported `W` does not match the selected profiles. This
experiment and its notes were prepared with OpenAI Codex assistance; the
construction authors and inherited AI-assistance disclosures remain those
recorded in the pinned proofs. In brief, the PR 62 graph is attributed to Avi
Eisenberg with Anthropic Claude assistance; the PR 57 compiler is attributed
to eumemic with OpenAI Codex assistance. The PR 63 rank-first compiler is
attributed to Chafik Boukhalfa with OpenAI Codex assistance, and the
composition report credits Dominik Scholz with substantial OpenAI GPT-6 Astra
assistance. The considered PR 58 proof credits Rohan Gupta with Anthropic
Claude assistance for its dual-suffix layout and eumemic with OpenAI Codex
assistance for the joint frame compiler. Full inherited credits remain in
each pinned proof. The repository's Apache-2.0 license applies subject to the
source-specific notices.
