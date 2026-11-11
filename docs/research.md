# Demand validation — 2026-11-10

## Authoritative technical sources

- [Kubernetes Application Security Checklist](https://kubernetes.io/docs/concepts/security/application-security-checklist/): recommends resource limits, separate service accounts, Restricted Pod Security, seccomp, read-only filesystems, no privilege escalation, dropped capabilities, NetworkPolicy, and stronger isolation such as gVisor or Kata for sensitive workloads.
- [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/): defines the Restricted profile controls used by this guard.
- [Kubernetes Multi-tenancy](https://kubernetes.io/docs/concepts/security/multi-tenancy/): explains that containers share the host kernel and stronger sandboxing can use userspace kernels or virtual machines.
- [Kubernetes RuntimeClass](https://kubernetes.io/docs/concepts/containers/runtime-class/): provides the mechanism for selecting a configured container runtime.
- [Kubernetes seccomp](https://kubernetes.io/docs/reference/node/seccomp/): documents syscall filtering and RuntimeDefault.
- [Enforce Pod Security Standards](https://kubernetes.io/docs/setup/best-practices/enforcing-pod-security-standards/): supports warn/audit-first rollout before enforcement.

## Recurring live-role requirements checked

- [San Francisco Tensor Company — Sandbox Infrastructure](https://jobs.ashbyhq.com/sf-tensor/7768fa39-742a-41dc-b329-edf75cdcd168/): untrusted generated kernels, sandbox runtimes, security/isolation, and distributed failure handling.
- [OpenAI — Software Engineer, Infrastructure Security](https://jobs.ashbyhq.com/openai/98ad9beb-4f91-496c-bd16-ac0b2a8d5bb2/): Kubernetes, network isolation, authentication, and infrastructure security.
- [Echelon — Senior/Staff AI Infrastructure Engineer](https://jobs.ashbyhq.com/echelon/1a5c0336-68d3-42fb-a609-01bf913a51f6): sandbox lifecycle for agent code, browser, document, and tool execution with Kubernetes and infrastructure as code.
- [Preference Model — Infrastructure Engineer](https://jobs.ashbyhq.com/Preference-Model/b77e59f1-e2ef-43c1-88f2-d05c7264479a): platform infrastructure, sandboxing, and untrusted-code operations.

## Rationale

The overlap is consistent: production AI agents need isolated execution, Kubernetes lifecycle controls, network boundaries, evidence, and operational reliability. This project therefore solves a current platform problem rather than presenting a generic AI demonstration.

