---
name: github-actions
description: Develop diagnose and optimize two-repo GitHub Actions CI workflows
---

# github-actions

1. Identify target repository: Workspace CI validates scaffold only; Product CI builds backend/frontend and integrated tests. Do not mix.
2. Read existing workflow, triggers, runner OS, dependencies, permissions, lockfiles and action versions before editing.
3. Make local commands identical to CI; use separate backend/frontend jobs and PostgreSQL service as needed.
4. Pin runtime major/minor versions and dependencies; use least privilege, concurrency strategy and artifact retention; do not put secrets in logs.
5. Validate YAML, matrix path filters, required check semantics, service readiness, caches and deterministic versioning.
6. Read actual GitHub job logs to diagnose failure; don't declare success from YAML inspection alone.
