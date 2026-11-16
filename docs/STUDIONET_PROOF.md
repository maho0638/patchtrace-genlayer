# Real Studionet acceptance proof — patchtrace-genlayer

**Observed on 2026-11-16, not simulated.** GitHub Actions executed the official `gltest` Studio Mode against the stable hosted GenLayer Studionet RPC `https://studio.genlayer.com/api`. A JSON-RPC `eth_chainId` check confirmed **61999** before any network writes.

- Successful public GitHub Actions run: https://github.com/maho0638/patchtrace-genlayer/actions/runs/43894417604
- Tested contract source: [contracts/PatchTrace.py](../contracts/PatchTrace.py) (source file in `main` unchanged from QA run)
- Network: GenLayer Studionet (temporary hosted development network, **not Bradbury**)
- Contract deployed and read back: `0x5bda02f47FA5A822Bf560FDe6D25f8B6Ca6Ba1E7`
- Ephemeral SDK-generated sender (address only): `0x33105a44af79503EC62DE7999240d592BC0ba266`
- Integration test: **PASS 1/1 (51.42 s)**
- Recorded post-consensus state: `TRACE_COMPLETE; mapping {"S1":"H1","S2":"H2"}`

## Real accepted transaction receipts

- **open_issue**: `0xbae43aada21cdf573ddaee418b44c843d39622fe0197db39430964f0312f9d9d`
- **propose_patch**: `0xb9c4182eec482482b9eec4b949d7856f4674e923410c1edf0f1ec5b0fcb6c73a`
- **trace_patch**: `0xa1a94384b847dc166ef2d5ef5e1ed15afca8e6db0d1ce8e60ec0f5b1821718ec`

## Scope and limitations

- The test runs on GitHub's free `ubuntu-24.04` runner, with `genlayer-test==0.29.2` and `genlayer-py==0.16.3`.
- Genuine remote contract deployment, write transaction receipts, on-network readbacks and one AI/validator consensus call. `leader_only=false`, **no LLM response mocks** in this Studio test.
- No user's wallet keys, repository secrets, paid cloud service, mainnet or Bradbury activity. Generated temporary test account key is never printed or stored.
- Receipt success was verified using `tx_execution_succeeded` and readbacks; **separate post-acceptance finality check was not conducted**. Do not claim mainnet readiness or unrestricted reproducibility; this hosted network can reset.
- Existing separate Direct Mode SDK tests and GenVM static lint have also passed; see [PROOF_STATUS.md](PROOF_STATUS.md).
- Portal: **not submitted**.

Run the network test again only by explicitly using the `workflow_dispatch` manual workflow; do not introduce automatic network deployment triggers.
