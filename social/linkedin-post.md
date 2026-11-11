Imagine an AI agent receives a pull request, generates a helper script, and executes it in the same Kubernetes cluster that runs customer workloads. The script is useful—but it is still untrusted code, and a standard container shares the host kernel.

That boundary matters to the whole organization. One permissive service-account token, metadata endpoint, secret mount, or unlimited process tree can turn an automation feature into a cloud-security incident.

The security issues are concrete: weak runtime isolation, privileged pod settings, unrestricted egress, leaked credentials, mutable images, missing resource limits, and sandboxes that never get destroyed.

I built Kubernetes AI Agent Sandbox Guard to turn those risks into a deterministic PASS, REVIEW, or BLOCK decision before an agent workload may run.

- Requires a gVisor or Kata RuntimeClass and disables host namespace access.
- Enforces Restricted Pod Security: non-root, seccomp, read-only filesystem, no privilege escalation, and dropped capabilities.
- Checks CPU, memory, PID, storage, timeout, and automatic-cleanup bounds.
- Requires default-deny egress, metadata blocking, no exposed secrets, and digest-pinned verified images.
- Records ownership, audit, alerts, runbook, and human approval; optional AI explanations can never override policy.

This is game-changing because it joins AI automation with the controls platform teams already need: Kubernetes isolation, evidence-driven admission, network policy, supply-chain integrity, and measurable operations. The result is testable, CI-ready, and designed for audit-first deployment.

Repository: https://github.com/ohjeffkuston/kubernetes-ai-agent-sandbox-guard

Architecture image alt text: Architecture flow showing AI-agent inputs entering a deterministic Kubernetes sandbox policy guard, producing PASS, REVIEW, or BLOCK, followed by a human-approved isolated runtime and telemetry feedback.

Where should your organization draw the execution boundary for model-generated code?

