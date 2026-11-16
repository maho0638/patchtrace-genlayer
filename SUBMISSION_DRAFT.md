# Portal submission text — source + official Direct Mode QA verified

**Category:** Developer → Intelligent Contracts

**Title:** PatchTrace — Consensus-Backed Issue-to-Code Witness Mapping

**Description (less than 1,000 characters):**

PatchTrace introduces an auditable GenLayer primitive that links individual software bug symptoms to concrete code-change hunks. A maintainer freezes up to four numbered symptoms; a contributor supplies up to five before/after snippets. The GenLayer leader proposes a symptom-to-hunk mapping, and validators independently remap each symptom under a custom Equivalence Principle. Unknown references and incomplete outputs are rejected. Uncovered symptoms remain explicit; only a fully mapped patch can be acknowledged by the original issue owner. Inputs, witness references and SHA-256 commitments are stored on-chain. Unlike a three-label classification or API schema comparison, the output is a verifiable mapping graph. This is traceability, not proof that code compiled, tests passed or a bug was actually fixed.

**Evidence:** Public source: https://github.com/maho0638/patchtrace-genlayer . Real Studionet network integration: https://github.com/maho0638/patchtrace-genlayer/actions/runs/43894417604 . Contract deployed on chain ID 61999: `0x5bda02f47FA5A822Bf560FDe6D25f8B6Ca6Ba1E7`. Exact accepted write receipts, readbacks and consensus result: https://github.com/maho0638/patchtrace-genlayer/blob/main/docs/STUDIONET_PROOF.md . Separate on-chain finality and Explorer deep link were not claimed; no Portal submission has been made.
