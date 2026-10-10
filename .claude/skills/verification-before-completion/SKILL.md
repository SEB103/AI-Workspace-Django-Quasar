---
name: verification-before-completion
description: Verify actual code edits with tests and show factual evidence before marking task complete
disable-model-invocation: true
---

# verification-before-completion

1. Identify requested acceptance criteria and changed paths; establish expected commands from actual project scripts and lockfiles.
2. Run relevant checks locally; for API change verify both backend and frontend and schema, for DB change migration and PostgreSQL tests.
3. Check repository tracked file boundary with `repo_audit.py`, staged diff, and no secrets/medical content.
4. If CI needed, inspect **actual** GitHub Actions run; config presence ≠ executed success.
5. Final report: commands, outputs/pass/fail, unverified items, risks, and operator actions. Never say 'done' solely because code compiles.
