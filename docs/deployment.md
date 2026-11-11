# Safe deployment guide

1. Install and benchmark a sandboxed runtime such as gVisor or Kata on a non-production node pool.
2. Label and taint the pool; configure the `gvisor` or `kata` RuntimeClass and matching scheduling rules.
3. Enable Pod Security `warn` and `audit` at Restricted level, then inspect violations before enforcing.
4. Install a NetworkPolicy-capable CNI. Apply default-deny ingress/egress and explicit DNS/provider allowlists; block link-local cloud metadata addresses.
5. Run this guard in pull-request CI or a platform API using read-only evidence. Do not give it cluster-admin permissions.
6. Archive the JSON decision, policy version, manifest digest, image attestation, approver, and execution ID.
7. Require an operator approval for every initial deployment class. Add policy exceptions only through time-bounded, reviewed records.
8. Enforce TTL cleanup and monitor orphaned pods, admission latency, denied-rule distribution, runtime alerts, and evidence delivery.
9. Promote to blocking only after an audit-only baseline shows acceptable false positives and runtime compatibility.

Rollback removes the platform workflow requirement while leaving cluster-native Pod Security, admission, NetworkPolicy, and sandbox runtime controls intact. Never weaken those controls merely to restore agent throughput.

