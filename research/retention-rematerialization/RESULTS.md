# Results

**FAST: PASS. FOCUSED: PASS. No local saving proved.** The first candidate, `Y2(2044)`, has no reuse demand. The fallback `Y2048` has four real outgoing uses, but a single retained carrier cannot traverse their pairwise incomparable frames, and `Y2048` is not in the span of the checked compatible roles at any destination. No alternative circuit was priced as free.

## Verification

- The Issue 19 source commit, PR 63 graph/compiler, canonical word, and deterministic gzip all match their pinned identities. Canonical word SHA-256: `640696dd7cd893add9d6e12d0d587956fecf113b2eff8c29547b82e5a6f3c0ad`; gzip SHA-256: `1a57c143380a063211653f1f35e7cc9710539523b0b34c90f354a0425c34bd59`.
- FAST checked the exact logical-use graph, frame-compatible role spans, child-local independence, and the baseline operations before launching the focused compile.
- FOCUSED re-emitted the exact frozen word, rebuilt the full rank profile from events and endpoints, checked the four actual rank-2 edges, validated the local dirty wrapper, and rejected the PR 96 merged-edge negative control.
- The wrapper's 13 basis-vector checks passed in both orientations. Full h=23 forward/reverse word replay was **not run**.

## Outcome boundaries

- **`Y2(2044)`:** no reuse demand; it is used once in its own group 1929. There is no retention/rematerialization tradeoff to charge for this value.
- **`Y2048`:** the measured baseline uses four physical roles and three outgoing copy XORs, with four distinct rank-2 child edges. One-carrier retention is inadmissible; tested rematerialization is unavailable from the checked physical states. No local XOR, rank, role, or endpoint saving is established.
- **Recursive child sharing and `κ`:** not established or improved. These local probes do not show a common recurrence source, a new Section 4 pivot, a `Swap` child, or a changed child-cost bound.

## Runtime and resources

| Stage | Wall time | Peak RSS |
|---|---:|---:|
| FAST checks | 1.828 s | 434,380 KiB |
| FOCUSED total | 76.716 s | 485,468 KiB |
| FOCUSED compiler call | 71.328 s | included above |

The pinned Issue 19 compiler call took 89.212 s in its run; that is a provenance reference, not a controlled speed comparison. Free disk after FOCUSED was 37,266,544 KiB. Reproduction commands and source identities are in [SOURCES.md](SOURCES.md); exact receipts are retained beside this report.
