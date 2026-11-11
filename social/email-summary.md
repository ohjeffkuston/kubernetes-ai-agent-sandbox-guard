Subject: Day 27 — Kubernetes AI Agent Sandbox Guard

To: ohjeffkuston@yahoo.ca

I completed Day 27 of the Cloud + AI portfolio: Kubernetes AI Agent Sandbox Guard.

The production problem is safe execution of untrusted or model-generated code. The guard makes 16 deterministic checks across sandbox RuntimeClass selection, Restricted Pod Security, network isolation, metadata blocking, resource and lifetime bounds, credential exposure, immutable images, provenance, auditability, ownership, and approval. It returns PASS, REVIEW, or BLOCK; an optional AI explanation cannot override enforcement.

Deployment approach: begin in CI and Pod Security warn/audit modes, benchmark gVisor or Kata on a separate node pool, enable default-deny NetworkPolicy and metadata blocking, retain decision evidence, enforce cleanup TTLs, and move to blocking only after measuring compatibility and false positives. No production infrastructure is mutated by the repository.

Validation: the suite covers a compliant bundle, a deliberately unsafe bundle, operational review behavior, and 13 targeted regressions. CI also invokes the real CLI.

Measurable outcomes: 100% policy coverage, zero executions missing core isolation controls, p95 decisions below 250 ms, less than 5% false positives after audit-mode tuning, and complete TTL cleanup.

What I learned: sandbox security is layered. Runtime isolation, Pod Security, egress control, image integrity, resource limits, lifecycle cleanup, audit evidence, and human approval reinforce each other. AI can explain results, but deterministic policy must own enforcement.

Interview positioning: this project demonstrates Kubernetes security, secure AI workload operations, policy-as-code design, CI testing, platform reliability, observability, and explicit performance-versus-isolation trade-offs for Cloud, DevOps, SRE, Platform, and AI-infrastructure roles.

Repository: https://github.com/ohjeffkuston/kubernetes-ai-agent-sandbox-guard

