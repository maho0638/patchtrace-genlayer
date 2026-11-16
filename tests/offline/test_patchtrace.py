import json
import pytest

SYMPTOMS = "S1|Public API returns a wrong status when request lacks auth\nS2|A malformed token still reaches the protected handler"
HUNKS = "H1|src/auth.py|accept_missing_token()|reject_missing_token()\nH2|src/routes.py|allow_if_token_present()|allow_if_token_verified()"

def setup_issue(h):
    c=h.contract
    c.open_issue("issue-001","Missing token authentication regression",SYMPTOMS)
    h.set_sender("0xDEV")
    c.propose_patch("patch-001","issue-001",HUNKS)
    return c

def mapping(h, data=None):
    h.response={"links": data if data is not None else {"S1":"H1","S2":"H2"}}

def test_complete_trace_and_owner_acknowledgement(host):
    h=host;c=setup_issue(h);mapping(h)
    c.trace_patch("patch-001")
    p=json.loads(c.get_patch("patch-001"))
    assert p["state"]=="TRACE_COMPLETE"
    assert p["mapping"]=={"S1":"H1","S2":"H2"}
    assert len(p["mapping_hash"])==64
    with pytest.raises(h.error, match="Only issue owner"):
        c.acknowledge_patch("patch-001")
    h.set_sender("0xOWNER")
    c.acknowledge_patch("patch-001")
    assert json.loads(c.get_patch("patch-001"))["state"]=="ACKNOWLEDGED"
    assert json.loads(c.get_issue("issue-001"))["adopted_patch"]=="patch-001"
    with pytest.raises(h.error, match="Issue already adopted"):
        c.acknowledge_patch("patch-001")

def test_missing_witness_fails_closed(host):
    h=host;c=setup_issue(h);mapping(h,{"S1":"H1","S2":"NONE"})
    c.trace_patch("patch-001")
    assert json.loads(c.get_patch("patch-001"))["state"]=="TRACE_GAPS"
    h.set_sender("0xOWNER")
    with pytest.raises(h.error, match="Full trace required"):
        c.acknowledge_patch("patch-001")

def test_hallucinated_references_or_keys_rejected(host):
    h=host;c=setup_issue(h)
    for bad in ({"S1":"H99","S2":"H2"},{"S1":"H1"},{"S1":"H1","S2":"H2","S3":"H1"}):
        mapping(h,bad)
        with pytest.raises(h.error):c.trace_patch("patch-001")
    assert json.loads(c.get_patch("patch-001"))["state"]=="SUBMITTED"

def test_validator_independently_remaps(host):
    h=host;c=setup_issue(h);mapping(h);c.trace_patch("patch-001")
    # Validator independently computes, not merely checking JSON shape.
    from types import SimpleNamespace
    assert h.validator(SimpleNamespace(calldata={"S1":"H1","S2":"H2"})) is False
    # Real run uses the VM return type; check mismatch using saved runner class.
    class ReturnLike:pass
    # Inspect the closure and exercise through the mocked interface below.
    vm = h.contract.trace_patch.__func__.__globals__["gl"].vm
    assert h.validator(vm.Return({"S1":"H1","S2":"H2"})) is True
    h.response={"links":{"S1":"H2","S2":"H1"}}
    assert h.validator(vm.Return({"S1":"H1","S2":"H2"})) is False

def test_duplicate_unauthorized_and_replay(host):
    h=host;c=setup_issue(h)
    with pytest.raises(h.error, match="Duplicate issue"):
        h.set_sender("0xOWNER");c.open_issue("issue-001","Missing token authentication regression",SYMPTOMS)
    h.set_sender("0xDEV")
    with pytest.raises(h.error,match="Duplicate patch"):
        c.propose_patch("patch-001","issue-001",HUNKS)
    mapping(h);c.trace_patch("patch-001")
    with pytest.raises(h.error,match="Already traced"):c.trace_patch("patch-001")

def test_manifest_bad_paths_and_control_characters(host):
    h=host;c=h.contract
    for symptoms in ("S1|a short note", "S2|Only second item is present", "S1|A valid long symptom report\nS1|A duplicated symptom report"):
        with pytest.raises(h.error):c.open_issue("issue-001","Missing token authentication regression",symptoms)
    c.open_issue("issue-001","Missing token authentication regression",SYMPTOMS)
    for bad in ("H1|../secret|before state|after state", "H1|src/a.py|same code|same code", "H2|src/a.py|old code|new code", "H1|src/a.py|old code|new code\nH1|src/b.py|old code|new code"):
        with pytest.raises(h.error):c.propose_patch("patch-001","issue-001",bad)
    with pytest.raises(h.error):c.open_issue("issue-002","Bad title \u202e injected",SYMPTOMS)

def test_multiple_patches_distinct_and_owner_choice(host):
    h=host;c=setup_issue(h)
    mapping(h,{"S1":"H1","S2":"NONE"});c.trace_patch("patch-001")
    c.propose_patch("patch-002","issue-001",HUNKS)
    mapping(h);c.trace_patch("patch-002")
    h.set_sender("0xOWNER");c.acknowledge_patch("patch-002")
    assert json.loads(c.get_issue("issue-001"))["adopted_patch"]=="patch-002"
    with pytest.raises(h.error,match="Issue already adopted"):
        h.set_sender("0xDEV");c.propose_patch("patch-003","issue-001",HUNKS)
