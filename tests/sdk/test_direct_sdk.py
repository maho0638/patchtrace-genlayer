"""Official GenLayer Direct Mode tests. Requires genlayer-test; not offline stubs."""
import json

SYMPTOMS = "S1|Missing token currently allows a request to access the API\nS2|Malformed credentials still reach the private route handler"
HUNKS = "H1|src/auth.py|accept_none_token()|reject_none_token()\nH2|src/routes.py|allow_if_present()|allow_if_verified()"


def mock(vm, links):
    vm.clear_mocks()
    vm.mock_llm(r"(?s).*PatchTrace\. Map EACH reported bug symptom.*", json.dumps({"links": links}))


def fixture(c):
    c.open_issue("issue-001", "Authentication regression on protected public API", SYMPTOMS)
    c.propose_patch("patch-001", "issue-001", HUNKS)


def test_complete_trace_and_validator_equality(direct_vm, direct_deploy):
    c = direct_deploy("contracts/PatchTrace.py")
    fixture(c)
    good = {"S1": "H1", "S2": "H2"}
    mock(direct_vm, good)
    c.trace_patch("patch-001")
    assert json.loads(c.get_patch("patch-001"))["state"] == "TRACE_COMPLETE"
    assert direct_vm.run_validator() is True
    mock(direct_vm, {"S1": "H2", "S2": "H1"})
    assert direct_vm.run_validator() is False
    c.acknowledge_patch("patch-001")
    assert json.loads(c.get_issue("issue-001"))["adopted_patch"] == "patch-001"


def test_gap_blocks_acknowledgment(direct_vm, direct_deploy):
    c = direct_deploy("contracts/PatchTrace.py")
    fixture(c)
    mock(direct_vm, {"S1": "H1", "S2": "NONE"})
    c.trace_patch("patch-001")
    assert json.loads(c.get_patch("patch-001"))["state"] == "TRACE_GAPS"
    with direct_vm.expect_revert("Full trace required"):
        c.acknowledge_patch("patch-001")


def test_invalid_llm_references_fail_closed(direct_vm, direct_deploy):
    c = direct_deploy("contracts/PatchTrace.py")
    fixture(c)
    mock(direct_vm, {"S1": "H99", "S2": "H2"})
    with direct_vm.expect_revert("Hallucinated hunk reference"):
        c.trace_patch("patch-001")
    assert json.loads(c.get_patch("patch-001"))["state"] == "SUBMITTED"


def test_duplicate_and_permissions(direct_vm, direct_deploy, direct_bob):
    c = direct_deploy("contracts/PatchTrace.py")
    fixture(c)
    with direct_vm.expect_revert("Duplicate patch"):
        c.propose_patch("patch-001", "issue-001", HUNKS)
    mock(direct_vm, {"S1": "H1", "S2": "H2"})
    c.trace_patch("patch-001")
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("Only issue owner"):
        c.acknowledge_patch("patch-001")


def test_manifest_safety(direct_vm, direct_deploy):
    c = direct_deploy("contracts/PatchTrace.py")
    c.open_issue("issue-001", "Authentication regression on protected public API", SYMPTOMS)
    with direct_vm.expect_revert("Unsafe path"):
        c.propose_patch("patch-001", "issue-001", "H1|../secret|allow_public()|deny_public()")
