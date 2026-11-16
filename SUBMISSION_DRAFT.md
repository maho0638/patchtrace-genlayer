# Portal draft — DO NOT SUBMIT WITHOUT LIVE PROOF

**Category:** Developer → Intelligent Contracts

**Title:** PatchTrace — Consensus-Backed Issue-to-Code Witness Mapping

**Description (less than 1,000 characters):**

PatchTrace introduces an auditable GenLayer primitive that links individual software bug symptoms to concrete code-change hunks. A maintainer freezes up to four numbered symptoms; a contributor supplies up to five before/after snippets. The GenLayer leader proposes a symptom-to-hunk mapping, and validators independently remap each symptom under a custom Equivalence Principle. Unknown references and incomplete outputs are rejected. Uncovered symptoms remain explicit; only a fully mapped patch can be acknowledged by the original issue owner. Inputs, witness references and SHA-256 commitments are stored on-chain. Unlike a three-label classification or API schema comparison, the output is a verifiable mapping graph. This is traceability, not proof that code compiled, tests passed or a bug was actually fixed.

**Required evidence:** GitHub repository URL; matching-source GenLayer Explorer contract URL; optional SDK/lint workflow and signed end-to-end test link. **None is claimed live yet.**
