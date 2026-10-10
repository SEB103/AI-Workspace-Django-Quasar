# Workspace changelog

## [0.2.0] — Explicit reusable workspace directory layout
- Standardized mandatory roots: `docs/`, `reference/`, `generated/`, `project/`.
- Added tracked instructional README.md files for reference, generated, generated/plans, generated/tickets, generated/reports and docs.
- The `/project/` directory is created by bootstrap and included empty in ZIP, yet remains completely excluded from Workspace Git.
- Replaced local `task-context/` and `generated-docs/` workflow paths with `generated/{tickets,plans,reports}`; old paths remain ignored for backward compatibility.
- Updated Git ignore allowlist, repository audit, standalone validator, Claude instructions, skills and tests.
- Standardized ZIP/project identity as `AI-Workspace-Django-Quasar`.

## [0.1.0] — Initial portable Claude Code-only workspace
- Two independent Git repos (outer workspace; inner product), with separate ignore policies.
- 24 original stack-aware Claude Code skills, 6 read-only reviewer agents, focused rules and project profile templates.
- Python guard, standalone scaffold validator, repository boundary auditor, bootstrap helper, unit tests and GitHub Actions CI.
- No project-specific tickets, generated docs, private files or product sources tracked in Workspace.
- Stack-specific rules isolated in a selectable local profile.
