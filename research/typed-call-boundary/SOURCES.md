# Source pins and provenance

This checkpoint is based on fork `main` at
`0605a24a28836168ad29d6239b46064b892298fc`. The original manuscript is pinned
to OpenAI Math commit
[`adc7f1241b42e322a6451854ab7e4b4c146bf78a`](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a),
the commit named by `upstream/manifest.json`. The checked-in section files
have the same SHA-256 values as that manifest. No manuscript or upstream
construction code was modified or copied into this checkpoint.

## Original manuscript files used

| File at pinned commit | SHA-256 | Use |
|---|---|---|
| `upstream/README.md` | `8d1ceff898a4e0e681679f91c4def485820be9e99f04e4861f2ce601a364723e` | Paper title, authorship, and citation. |
| `upstream/LICENSE` | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` | Retained source license notice. |
| `upstream/manifest.json` | `16ab13971694cabab09440c47ebf2fc0496a9d35fc3af33950fda3498f8e2392` | Immutable commit and file hash ledger. |
| `upstream/build/main.tex` | `42f0f506976bc2084374a71e97edc1549689a7accf35dda4db2a18af4f13c1aa` | Fixed-tape theorem context. |
| `upstream/build/sections/00-introduction.tex` | `98721f03682ccf1cc7d0850b07adabaa2d8f3afe552e3861753eba9d284d0da0` | Theorem `thm:main`, operation summary, and finite-network recurrence explanation. |
| `upstream/build/sections/02-streams.tex` | `606c80db61cad13aa0c3b6060dc4b88dbbe7ac60cdd831aa93f28d908fd09dab` | Array model, logical volume, descriptor, and elementary tape operations. |
| `upstream/build/sections/03-motifs.tex` | `ed76761194988a01af77ead0ea6469cb5dcd29690ab985a0b5a4006b0f2b69bb` | Bit-network interface, role count, and edge-rank sum. |
| `upstream/build/sections/04-swap.tex` | `412b170ccaab38dba96e95e3cbfae09f4876a9818f8d278776a746b0f8044906` | Matrix shear, power-width recursive interchange, recurrence, and tape schedule. |
| `upstream/build/sections/05-layers.tex` | `20cfc8d12099d4e4ed9e3e7eeb6162edd9b6e0e076f24693364cd24377252594` | Separate numerical butterfly recursion. |
| `upstream/build/sections/08-assembly.tex` | `763d7945b1e1ec4ebae9b799bcefcc45fa9bae6e2ffad799868a9c3d513dbd4a` | Use of both procedures in the full multiplication proof. |

## Issue 13 frozen result

The predecessor was read from immutable fork commit
`26ff3802cfa1b4b6ee081703509c394fa71526a0`, branch
`issue-13-typed-frame-interface`. Its focused checker was rerun in that
worktree; it reported the recorded local GF(2) and aggregate-profile checks
as PASS. Hashes of the exact frozen files read:

| File at commit `26ff380...` | SHA-256 |
|---|---|
| `research/typed-frame-interface/BOUNDARY.md` | `487e7776af7aa42b52224d8ac64a0856a1bddaa654c2537a3a2334aea82574e4` |
| `research/typed-frame-interface/RESULTS.md` | `095e95970f4654b5047fd1eb5af801bdf80ba3703c81b0b8660edd502afc196c` |
| `research/typed-frame-interface/SOURCES.md` | `dda9e0ff8e4d61cfa4c5a2831e9d0c152631876e58d15ddd030618e8a62e46f9` |
| `research/typed-frame-interface/check_boundary.py` | `170cf7c2ad2f500efe30809c7e72f3b7d87bb6363bb68e515dfbe0d5630cbd29` |

Issue 13's source ledger pins the pair-assembly/compiler basis to CrocSwap
commit `aa7701b68540b7863d3b66a414e4319915d6282d`, linked as a redirected
[source commit](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/aa7701b68540b7863d3b66a414e4319915d6282d).
The specific source hashes used to distinguish the physical profile from the
manuscript theorem are:

| Pinned construction file | SHA-256 | Role in this checkpoint |
|---|---|---|
| `research/pair-assembly/pair_graph.py` | `3d47e89d2649c90800a276bdd0480131def50e0bdf92c122a19494b55bf17420` | Defines the local `FSa` producer dependency. |
| `research/pair-assembly/frame/frame_verify.py` | `fafe25d57166a747eeb847444a2e02dd7eed19038b93a2c495014d147d04a8fb` | Derives aggregate child-width profile rows. |
| `research/rank-pair/frame_compile.py` | `c5d11d944d8c6195d7b03efe5adfdde9d1ae508956fa9287b4ca9d3c7de7b750` | Pins the whole-graph frame compiler inputs. |
| `research/rank-pair/frame-compiler.json` | `e34d155e32b03451d3fd5b39fc39b0aefcf09bc2a8e803ab9cacf21c91ee6ba1` | Aggregated role, rank, XOR, and dirty-basis records. |
| `research/rank-pair/screen-certificate.json` | `4aea9e9a2610f26f28872e2918c94c402bc93aa2203796af77021982e9120d8e` | Exact scalar profile moment certificate. |

The complete attribution and inherited assumptions remain in the frozen
Issue 13 `SOURCES.md`. This checkpoint reuses that ledger rather than
downloading or regenerating its artifacts.

## New files and validation

`THEOREM_MAP.md`, `CONTRACT.md`, and `RESULTS.md` were written for this
checkpoint. `check_call_boundary.py` uses only the Python standard library
and checks a reduced rank-one instance of the source matrix-shear rule. The
manuscript theorem supplies the general fixed-network proof; the checker is
not a reimplementation of its network or physical tape program.

Prepared with OpenAI Codex assistance. Original manuscript and pair-assembly
attributions are retained; no upstream code was copied.
