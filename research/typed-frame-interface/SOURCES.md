# Pinned sources and attribution

This checkpoint starts from the user's fork `main` at
`0605a24a28836168ad29d6239b46064b892298fc` and reads predecessor work from
the immutable commits below. External issue, pull-request, and commit links
use GitHub's redirect host as required by the research source boundary.

## Prior research

| Source | Immutable file(s) | SHA-256 | Use |
|---|---|---|---|
| [Issue 10 fork snapshot](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/d0579057de829105fa1376981c75564ac0ceff34), commit `d0579057de829105fa1376981c75564ac0ceff34` | `research/kappa-one-barriers/BARRIERS.md`; `research-directions.md`; `sources.json` | `a0249c25c460b313aeeadfdc71682dbbb7f9abb26f0a20b611ba80cf54c712d3`; `0561134ea09fa8ee274972d5a948a57f246bbf0b08f1854c73876a3ac0fc62f3`; `cdc37fa8b38d4aa19a78bf8e1cbd505a9ab57644fc2615afde4753244149189c` | Parent barrier map, typed-recursion requirements, pinned source ledger. |
| [Issue 11 fork snapshot](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/33afe0a77afc8069ba67e5f3119e6e4219580326), commit `33afe0a77afc8069ba67e5f3119e6e4219580326` | `research/multitype-recursion-toy/MODEL.md`; `RESULTS.md`; `SOURCES.md`; `experiment.py` | `0d886f8277d127b790b594abfb8bea516b7931d123f134f5d7534cc5b355d04e`; `8ed02a77049e26623917d19a46fc4d9b38782d49613fabc41182ea721cc1ca01`; `00f98418c1fbec7a1494d4d1e05c4c56d395e147890d5c84c2d8d80dc3f3a3b0`; `270af7547c29a6d478621e37dfaac3126e86586816adbc60ba0fb2b0a38ecc1c` | Fixed-profile negative control and its exact model/source pins. |
| [Issue 12 fork snapshot](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/f1d3f14627fc0574514ae362237174e412fbad4a), commit `f1d3f14627fc0574514ae362237174e412fbad4a` | `research/cooperative-multitype/MECHANISM.md`; `RESULTS.md`; `SOURCES.md`; `experiment.py` | `2ba710e96c0ba0404c02fbc80c51fd30c6f6e42f89d5a0237bb3f45521814020`; `0ec34d688d7a8d2cf708654db619b394db20d7603a6cc71d71cc075a08b5e62e`; `9ebad5fdf2aa971dce6832094971a642244345aebbf09bef292ff16ca3201ae2`; `5da13658a773dd0e94b6aee8f6d2c5996d333870e6d36d8c288277fe6ca533d1` | Cooperative Boolean toy, unchanged dominant child cycle, and source boundary. |

## Real construction pin

The selected baseline is [CrocSwap construction commit
`aa7701b68540b7863d3b66a414e4319915d6282d`](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/aa7701b68540b7863d3b66a414e4319915d6282d), the rank-first frame compiler on the pair-assembly producer. The issue points to the [pinned rank-pair pull request](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/63). Hashes below are SHA-256 of the exact file bytes at that commit.

| File | SHA-256 | Use / attribution |
|---|---|---|
| `research/pair-assembly/PROOF.md` | `30685624bf922bb9d9f7ed4b0d367a660fe373cc9ee28fec33585bd8c7023e75` | Pair-assembly mechanism, source notices, finite profile and inherited proof limits. |
| `research/pair-assembly/pair_graph.py` | `3d47e89d2649c90800a276bdd0480131def50e0bdf92c122a19494b55bf17420` | Scalar producer and the `FSa` to `Y2` local dependency. |
| `research/pair-assembly/frame/frame_verify.py` | `fafe25d57166a747eeb847444a2e02dd7eed19038b93a2c495014d147d04a8fb` | Constructs the scalar child-width profile from the physical axis profiles. |
| `research/rank-pair/PROOF.md` | `b61b3cd554114f6eff6747133a980ac6525d1e2cdf0607056bf421dd331a261c` | Rank-first result, costs, validation scope, and attribution. |
| `research/rank-pair/frame_compile.py` | `c5d11d944d8c6195d7b03efe5adfdde9d1ae508956fa9287b4ca9d3c7de7b750` | Pins graph/compiler hashes and records compiled axes. |
| `research/rank-pair/frame-compiler.json` | `e34d155e32b03451d3fd5b39fc39b0aefcf09bc2a8e803ab9cacf21c91ee6ba1` | Whole-graph role, rank, XOR, dirty-basis, and replay records. |
| `research/rank-pair/frame-profiles-23.json` | `ba810de465295485090c5027bf073cc391e11b36ebf57963adba2e4bc78cfac4` | Physical rank histogram at `h=23`. |
| `research/rank-pair/frame-profiles-25.json` | `5c5dedf2f2d3373dd18f8aee8e30b8fb088a883351dd6350eb46edeef65494d1` | Physical rank histogram at `h=25`. |
| `research/rank-pair/frame-transitions-23.json` | `e2715ef2ff15abf43ced9a1e1b37fed8383cca9ff3e2ded3260ec5c21bfb88f3` | Aggregated physical transitions at `h=23`. |
| `research/rank-pair/frame-transitions-25.json` | `10c2f2e526ab4ddb97c8aa65960a72f5b81dbe38de0db26b71972782dd9c44a3` | Aggregated physical transitions at `h=25`. |
| `research/rank-pair/screen-certificate.json` | `4aea9e9a2610f26f28872e2918c94c402bc93aa2203796af77021982e9120d8e` | Exact scalar child multiplicities, moment, and accepted/excluded saving. |
| `scripts/experiments/rank_pair_compiler.py` | `9984aaccf880e4840402322d76678bfddb33ce7e494af78430a43429f51b85fd` | Rank-first carrier matching, frame containment, role copies, and word synthesis; derived from Chafik Boukhalfa's PR 60 compiler, itself from eumemic's PR 57. |
| `scripts/experiments/binary_frame_replay.py` | `392e78e62d7685c99a5888a7da743ea6c3dcad631af4a743c91e0c09348442bc` | Independent full-word, frame, and dirty-basis replay. |
| `scripts/experiments/binary_frame_math.py` | `1f96e8aafc8ae89f8eeec5d03800131d93d58e01bf8a7fca8feb03702d1740d0` | Exact rational moment arithmetic. |

The pair graph originates in Avi Eisenberg's pair-assembly work and retains
its documented Claude assistance and inherited attributions. The frame
compiler retains Chafik Boukhalfa's and eumemic's contributions and the
recorded OpenAI assistance. This checkpoint copies no upstream source. Its
docs and tiny checker were prepared with OpenAI Codex assistance.

## Inherited assumptions and scope

The finite profile is not an all-size multiplication proof. The fixed
finite-alphabet, finite-tape transfer; residual compiler; dirty-state and
frame transfer; analytic/Gaussian estimates; routing and layout; prime
selection; exact recovery; and the outer assembly constraints remain
inherited obligations in the pinned research. The Issue 11 and 12 toy results
do not discharge those obligations. This checkpoint claims no new `κ`, no
spectral improvement, and no theorem about other constructions.
