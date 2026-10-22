# MedicalPractice — AI development workspace

This is the **MedicalPractice-specific** development workspace for Claude Code and Codex. The workspace root (`.`) and nested Product root (`project/`) are **two independent Git repositories**. Start either coding tool from the workspace root so it can find the workspace instructions. Product sources are owned exclusively by `project/`.

## Mandatory boundaries
1. Workspace Git tracks AI instructions, Claude skills/reviewers/hooks, validation scripts, and workspace documentation; **never** track `project/` contents in Workspace Git.
2. Product Git (`project/.git`) owns Django backend, Quasar frontend, tests, migrations, lockfiles, deployment and product documentation. The Product must build/test without AI Workspace.
3. Do not copy `.claude/`, `CLAUDE.md`, `AGENTS.md`, AI skills/reviewer files, `generated/` or `reference/` into Product Git. No Git submodules/subtrees between the repositories.
4. Never place real patient data, medical records, identifiable persons, credentials, secrets or live database dumps in public source, demos, tests, prompts, logs, screenshots or CI. Use clearly fictional data.
5. Before any Git write, identify the intended root and inspect its status/diff (`git -C .` for Workspace, `git -C project` for Product). Stage only intended paths. Never assume a Git push, merge, tag, release or production deployment is authorized without an explicit user request.
6. Do not claim tests, CI, builds or deployments passed unless actually observed. Do not bypass failing gates. Protect existing data and migrations; destructive Git/DB operations require specific authorization.

## Product and working principles
- **MedicalPractice**: one medical practice per deployment; Django/DRF/Wagtail/PostgreSQL backend and Vue 3/Quasar/TypeScript frontend, communicating over versioned `/api/v1/` REST endpoints. Check the *actual* Product code before assuming a component is implemented.
- Prefer targeted fixes, readable code, minimal dependencies and backwards-compatible API changes. No speculative multi-tenancy, framework changes, major redesigns or broad refactors.
- Enforce authentication, object-level authorization, appointment consistency and privacy on the backend. Frontend validation is only a UX aid.
- Keep product decisions and API docs in `project/docs/`; workspace operational documentation in `docs/`; local AI plans/tickets/reports in ignored `generated/`; input reference material in ignored `reference/`.
- For substantial work, plan acceptance criteria, run relevant tests and report exact results, remaining risks and unverified items. Reviewer agents are read-only; the implementing agent owns changes.
- Globally installed plugins (e.g. superpowers) follow these rules: save their specs/plans/design docs under ignored `generated/plans/` (never `docs/superpowers/` in either repository) and never commit them automatically. Where a plugin skill shares a name with a workspace skill (`systematic-debugging`, `verification-before-completion`), the workspace version and these rules take precedence.

## MedicalPractice engineering rules (Claude Code imports)
@.claude/rules/00-governance.md
@.claude/rules/10-repository-boundaries.md
@.claude/rules/20-backend-python-django.md
@.claude/rules/30-frontend-typescript-quasar.md
@.claude/rules/40-api-contract.md
@.claude/rules/50-testing-quality.md
@.claude/rules/60-security-privacy.md
@.claude/rules/70-git-github.md
@.claude/rules/80-release-deployment.md
@.claude/rules/90-documentation-and-review.md

## Tool-specific adapters and on-demand guidance
- **Claude Code:** `CLAUDE.md` imports the rules above; `.claude/skills/` and `.claude/agents/` are its canonical skills and read-only reviewer definitions; `.claude/hooks/guard.py` is a Claude PreToolUse hook.
- **Codex:** `AGENTS.md` is the thin adapter. It directs Codex to read this file and the applicable rules/skills. The Claude `@` imports, skills discovery, reviewer subagents and PreToolUse hooks are **not automatically executed by Codex**.
- There is only **one** copy of each skill and reviewer definition. Codex may read these files on demand as task instructions/checklists; do not create mirrored `.agents/skills` or `.codex/skills` directories.
- Optional ignored `CLAUDE.local.md` may contain machine-specific instructions; it is not needed to activate MedicalPractice rules.

## Checks
- Bootstrap/migrate legacy local profile: `python .claude/scripts/bootstrap.py`
- Validate workspace: `python .claude/scripts/validate_workspace.py --strict`
- Tests: `python -m unittest discover -s .claude/tests -p 'test_*.py' -v`
- Git boundary audit: `python .claude/scripts/repo_audit.py --workspace-only`
- Skills catalog: `docs/SKILLS_CATALOG_RU.md` (load individual skills only when relevant).
