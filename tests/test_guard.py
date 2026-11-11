from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from agent_sandbox_guard import evaluate

ROOT = Path(__file__).parents[1]
POLICY = yaml.safe_load((ROOT / "policy/sandbox-policy.yaml").read_text())
GOOD = yaml.safe_load((ROOT / "samples/compliant-job.yaml").read_text())
BAD = yaml.safe_load((ROOT / "samples/unsafe-job.yaml").read_text())


def test_compliant_job_passes_all_sixteen_checks():
    result = evaluate(GOOD, POLICY)
    assert result["decision"] == "PASS"
    assert result["score"] == 100.0
    assert result["passed"] == result["total"] == 16


def test_unsafe_job_is_blocked():
    result = evaluate(BAD, POLICY)
    assert result["decision"] == "BLOCK"
    assert result["score"] < 50


@pytest.mark.parametrize(
    ("mutate", "rule"),
    [
        (lambda d: d["workload"]["spec"]["template"]["spec"].update(runtimeClassName="runc"), "SG-002"),
        (lambda d: d["workload"]["spec"]["template"]["spec"].update(hostPID=True), "SG-003"),
        (lambda d: d["workload"]["spec"]["template"]["spec"]["securityContext"].update(runAsNonRoot=False), "SG-004"),
        (lambda d: d["workload"]["spec"]["template"]["spec"]["containers"][0]["securityContext"].update(allowPrivilegeEscalation=True), "SG-005"),
        (lambda d: d["workload"]["spec"]["template"]["spec"]["containers"][0]["securityContext"].update(readOnlyRootFilesystem=False), "SG-006"),
        (lambda d: d["workload"]["spec"]["template"]["spec"]["containers"][0]["securityContext"].update(capabilities={"drop": []}), "SG-007"),
        (lambda d: d["workload"]["spec"]["template"]["spec"]["securityContext"].pop("seccompProfile"), "SG-008"),
        (lambda d: d["workload"]["spec"]["template"]["spec"]["containers"][0]["resources"]["limits"].pop("ephemeral-storage"), "SG-009"),
        (lambda d: d["sandbox"].update(pids_max=1000), "SG-010"),
        (lambda d: d["workload"]["spec"]["template"]["spec"].update(automountServiceAccountToken=True), "SG-011"),
        (lambda d: d["sandbox"]["egress"].update(metadata_api_blocked=False), "SG-013"),
        (lambda d: d["sandbox"].update(secrets_exposed=True), "SG-014"),
        (lambda d: d["sandbox"].update(provenance_verified=False), "SG-015"),
    ],
)
def test_security_regressions_block(mutate, rule):
    candidate = deepcopy(GOOD)
    mutate(candidate)
    result = evaluate(candidate, POLICY)
    assert result["decision"] == "BLOCK"
    failed = {item["rule"] for item in result["rules"] if not item["passed"]}
    assert rule in failed


def test_missing_operations_requires_review_only():
    candidate = deepcopy(GOOD)
    candidate["operations"].pop("runbook")
    result = evaluate(candidate, POLICY)
    assert result["decision"] == "REVIEW"
    assert result["score"] == 93.8

