"""Real network integration smoke: deploy, write, read, and AI consensus on Studionet.

NO test result fixtures, mocked LLMs, or user private keys. Only fresh auto-generated
accounts, with no transfers or value payments. This test performs real network writes.
"""
import json
import os
from pathlib import Path

from gltest import get_contract_factory, get_default_account
from gltest.assertions import tx_execution_succeeded

SYMPTOMS = (
    "S1|Missing authentication token currently permits access to the private API\n"
    "S2|Malformed credentials still reach protected route handlers"
)
HUNKS = (
    "H1|src/auth.py|accept_none_token()|reject_none_token()\n"
    "H2|src/routes.py|allow_if_present()|allow_if_verified()"
)


def record(message):
    print("STUDIONET_PROOF:", message, flush=True)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("- " + message + "\n")


def test_patchtrace_real_studionet():
    account = get_default_account()
    record("NETWORK studionet (RPC https://studio.genlayer.com/api; expected chain 61999)")
    record("DEPLOYER " + account.address + " (fresh ephemeral account; no key stored)")
    factory = get_contract_factory("PatchTrace")
    contract = factory.deploy(args=[], account=account, wait_interval=2000, wait_retries=50)
    record("CONTRACT " + str(contract.address))
    issue_id = "qa-studio-issue-20261116"
    patch_id = "qa-studio-patch-20261116"

    receipt = contract.open_issue(args=[
        issue_id, "Authentication regression on public protected routes", SYMPTOMS
    ]).transact(wait_interval=2000, wait_retries=50)
    assert tx_execution_succeeded(receipt), receipt
    record("OPEN_ISSUE receipt " + str(receipt.get("hash", receipt.get("transaction_hash", receipt.get("id", "unavailable")))))
    saved = json.loads(contract.get_issue(args=[issue_id]).call())
    assert list(sorted(saved["symptoms"])) == ["S1", "S2"]
    assert saved["owner"].lower() == account.address.lower()

    receipt = contract.propose_patch(args=[patch_id, issue_id, HUNKS]).transact(
        wait_interval=2000, wait_retries=50
    )
    assert tx_execution_succeeded(receipt), receipt
    record("PROPOSE_PATCH receipt " + str(receipt.get("hash", receipt.get("transaction_hash", receipt.get("id", "unavailable")))))
    before = json.loads(contract.get_patch(args=[patch_id]).call())
    assert before["state"] == "SUBMITTED"

    # Real AI consensus attempt: NO pre-canned LLM responses and leader_only is false.
    receipt = contract.trace_patch(args=[patch_id]).transact(
        consensus_max_rotations=3, wait_interval=2000, wait_retries=80
    )
    assert tx_execution_succeeded(receipt), receipt
    record("TRACE_PATCH receipt " + str(receipt.get("hash", receipt.get("transaction_hash", receipt.get("id", "unavailable")))))
    after = json.loads(contract.get_patch(args=[patch_id]).call())
    assert after["state"] in ("TRACE_COMPLETE", "TRACE_GAPS")
    assert set(after["mapping"]) == {"S1", "S2"}
    assert all(v in ("H1", "H2", "NONE") for v in after["mapping"].values())
    record("RESULT " + after["state"] + " mapping=" + json.dumps(after["mapping"], sort_keys=True))
    record("SUCCESS actual on-network deploy/write/read/AI-consensus without mocks")
