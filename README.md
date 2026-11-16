# PatchTrace — Issue-to-Change Witness Graph

**An auditable GenLayer Intelligent Contract that maps a bug report's individual symptoms to specific code-change hunks.** It does not classify an entire patch as simply PASS/FAIL, and does not pretend that AI has executed the patch.

## The novel primitive

A maintainer publishes 1–4 numbered symptoms (`S1..S4`). A contributor records 1–5 specific old-to-new hunk snippets (`H1..H5`). GenLayer leader and validators **independently** determine a concrete hunk witness for *each* symptom, or `NONE` when the supplied changes do not obviously address it. The chain records the exact mapping and a SHA-256 commitment. A maintainer may acknowledge only a complete trace; incomplete alternatives remain inspectable.

This turns one vague patch verdict into a **bipartite issue → change reference graph**, with explicit uncovered symptoms and non-replayable acknowledgments. All stored fields are public.

## Example

Symptoms:

```text
S1|Missing authentication token currently permits access to the private API
S2|A malformed token still reaches protected route handlers
```

Hunks:

```text
H1|src/auth.py|accept_none_token()|reject_none_token()
H2|src/routes.py|allow_if_present()|allow_if_verified()
```

Expected meaningful consensus mapping: `S1 -> H1`, `S2 -> H2`; then `TRACE_COMPLETE`. If no credible change addresses `S2`, the result should be `S2 -> NONE` and `TRACE_GAPS`. **The AI outcome is an independent mapping assessment, not executable test evidence.**

## Contract API

- `open_issue(issue_id, title, symptoms_manifest)` — opens immutable issue, records owner and symptoms hash.
- `propose_patch(patch_id, issue_id, hunks_manifest)` — records immutable source-change examples and hash; multiple competing proposals are allowed until acknowledgment.
- `trace_patch(patch_id)` — runs one bounded GenLayer nondeterministic mapping and independent validator re-evaluation; stores links, SHA-256, uncovered symptoms, state.
- `acknowledge_patch(patch_id)` — issue owner only; allowed only when every symptom has a hunk witness. Does **not** mean the code was tested or fixed.
- `get_issue`, `get_patch` — public JSON view methods.

Contract: [`contracts/PatchTrace.py`](contracts/PatchTrace.py).

## Why different from existing repositories?

Unlike ClauseMirror, LicenseProof and TenderLens, there is no generic three-way classification or appeal. Unlike SchemaSentinel, this does not compare API schema compatibility. Unlike Sightline's before/after images, it creates a **per-symptom reference mapping** across multiple code changes, with gaps preserved and issue-owner acknowledgment separate from AI consensus. It does not duplicate ResolveGraph's escrow or dependency settlement.

## Trust and security boundaries

See [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md): user-supplied text is untrusted; no GitHub code or commits are fetched; no code is compiled or executed; a hunk reference is **not** independently authenticated source provenance or proof of remediation. A malicious maintainer and developer can stage plausible data. Stronger CI/commit binding must be provided by an external integration.

Duplicate IDs, malformed mappings, fabricated hunk IDs, unauthorized acknowledgment, and repeat trace calls are prevented. Under the Equivalence Principle, validators **re-run the mapping**, not just inspect JSON syntax.

## Test without spending testnet GEN

```bash
python -m pip install pytest
python -m pytest -q tests/offline
```

These are **offline host-mock** regression tests, not real GenVM execution. For real official SDK Direct Mode and GenVM lints use the manual-only `.github/workflows/verify.yml` GitHub Actions workflow. It intentionally contains **no deployment, signing, secret or transaction step**.

## Proof status

- Offline state-machine tests: see [`docs/PROOF_STATUS.md`](docs/PROOF_STATUS.md).
- Official Direct Mode, lint, live Studionet, on-chain Explorer: **not claimed until actually verified**.
- Portal evidence requires this repository **plus the Explorer address of a genuinely deployed copy**; do not submit an old contract address.

See [`SUBMISSION_DRAFT.md`](SUBMISSION_DRAFT.md) when live evidence exists. No promise of Community Points or mainnet readiness.
