"""Deterministic policy evaluation for ephemeral Kubernetes agent sandboxes."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


def _result(rule: str, passed: bool, message: str, severity: str = "BLOCK") -> dict[str, Any]:
    return {"rule": rule, "passed": passed, "severity": severity, "message": message}


def _containers(spec: dict[str, Any]) -> list[dict[str, Any]]:
    return list(spec.get("containers", [])) + list(spec.get("initContainers", []))


def evaluate(document: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    """Evaluate a workload bundle and return a stable PASS/REVIEW/BLOCK decision."""
    doc = deepcopy(document)
    workload = doc.get("workload", {})
    sandbox = doc.get("sandbox", {})
    operations = doc.get("operations", {})
    kind = workload.get("kind")
    outer_spec = workload.get("spec", {})
    pod_spec = outer_spec.get("template", {}).get("spec", {}) if kind == "Job" else outer_spec
    containers = _containers(pod_spec)
    pod_sc = pod_spec.get("securityContext", {})
    rules: list[dict[str, Any]] = []

    rules.append(_result("SG-001", kind in {"Pod", "Job"} and bool(workload.get("metadata", {}).get("name")), "Supported named Pod or Job"))
    rules.append(_result("SG-002", pod_spec.get("runtimeClassName") in policy.get("allowed_runtime_classes", []), "Approved sandboxed RuntimeClass"))
    host_off = not any(pod_spec.get(k, False) for k in ("hostNetwork", "hostPID", "hostIPC"))
    rules.append(_result("SG-003", host_off, "Host namespace sharing disabled"))
    run_as_non_root = pod_sc.get("runAsNonRoot") is True and all(c.get("securityContext", {}).get("runAsNonRoot", True) is True for c in containers)
    rules.append(_result("SG-004", run_as_non_root, "Workload runs as non-root"))
    no_escalation = bool(containers) and all(c.get("securityContext", {}).get("allowPrivilegeEscalation") is False and c.get("securityContext", {}).get("privileged", False) is False for c in containers)
    rules.append(_result("SG-005", no_escalation, "Privilege escalation and privileged mode disabled"))
    read_only = bool(containers) and all(c.get("securityContext", {}).get("readOnlyRootFilesystem") is True for c in containers)
    rules.append(_result("SG-006", read_only, "Root filesystem is read-only"))
    caps = bool(containers) and all(set(c.get("securityContext", {}).get("capabilities", {}).get("drop", [])) == {"ALL"} and not c.get("securityContext", {}).get("capabilities", {}).get("add") for c in containers)
    rules.append(_result("SG-007", caps, "All Linux capabilities dropped"))
    seccomp = pod_sc.get("seccompProfile", {}).get("type") in {"RuntimeDefault", "Localhost"}
    rules.append(_result("SG-008", seccomp, "Seccomp profile configured"))
    required_resources = {"cpu", "memory", "ephemeral-storage"}
    bounded = bool(containers) and all(required_resources <= set(c.get("resources", {}).get("requests", {})) and required_resources <= set(c.get("resources", {}).get("limits", {})) for c in containers)
    rules.append(_result("SG-009", bounded, "CPU, memory, and ephemeral-storage are bounded"))
    deadline = outer_spec.get("activeDeadlineSeconds") if kind == "Job" else pod_spec.get("activeDeadlineSeconds")
    ttl = outer_spec.get("ttlSecondsAfterFinished") if kind == "Job" else sandbox.get("ttl_seconds")
    pids = sandbox.get("pids_max", policy.get("max_pids") + 1)
    lifetime = isinstance(deadline, int) and deadline <= policy.get("max_runtime_seconds", 0) and isinstance(ttl, int) and ttl <= policy.get("max_ttl_seconds", 0) and isinstance(pids, int) and pids <= policy.get("max_pids", 0)
    rules.append(_result("SG-010", lifetime, "Execution, cleanup, and PID bounds configured"))
    rules.append(_result("SG-011", pod_spec.get("automountServiceAccountToken") is False, "Service-account token automount disabled"))
    volumes = pod_spec.get("volumes", [])
    host_escape = not any("hostPath" in volume for volume in volumes) and all(not c.get("ports") and not c.get("volumeDevices") for c in containers)
    rules.append(_result("SG-012", host_escape, "Host paths, host ports, and raw devices absent"))
    egress = sandbox.get("egress", {})
    network = egress.get("default_deny") is True and egress.get("metadata_api_blocked") is True and isinstance(egress.get("allowlist"), list)
    rules.append(_result("SG-013", network, "Default-deny egress and metadata API block declared"))
    sensitive_env = any(any("secretKeyRef" in source.get("valueFrom", {}) for source in c.get("env", [])) or any("secretRef" in source for source in c.get("envFrom", [])) for c in containers)
    sensitive_volumes = any("secret" in volume for volume in volumes)
    rules.append(_result("SG-014", not sensitive_env and not sensitive_volumes and sandbox.get("secrets_exposed") is False, "Secrets are not exposed to untrusted code"))
    immutable = bool(containers) and all("@sha256:" in c.get("image", "") for c in containers) and sandbox.get("provenance_verified") is True
    rules.append(_result("SG-015", immutable, "Images are digest-pinned with verified provenance"))
    operational = all(operations.get(k) for k in ("owner", "runbook", "audit_sink", "alert_route")) and operations.get("human_approval_required") is True
    rules.append(_result("SG-016", operational, "Ownership, audit, alerts, runbook, and human approval recorded", "REVIEW"))

    failed = [rule for rule in rules if not rule["passed"]]
    decision = "BLOCK" if any(rule["severity"] == "BLOCK" for rule in failed) else "REVIEW" if failed else "PASS"
    score = round(100 * (len(rules) - len(failed)) / len(rules), 1)
    return {"decision": decision, "score": score, "passed": len(rules) - len(failed), "total": len(rules), "rules": rules}

