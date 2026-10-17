# Workspace changelog

## [0.3.0] — MedicalPractice-specific Claude Code + Codex workspace
- Removed generic stack profile selection; promoted six Django/Quasar/API/testing/privacy/release rules into `.claude/rules/` and imported them directly from `CLAUDE.md`.
- Added minimal root `AGENTS.md` adapter for Codex. Canonical rules, 20 skills and 6 read-only reviewer definitions remain shared without duplicated Codex copies.
- Removed five overlapping skills and updated skill manifest/catalog. Preserved manual ticket/review/release workflows.
- Simplified bootstrap and added safe migration of old local Claude profile imports, with backup and custom-note preservation.
- Updated validation/tests, repository policy and onboarding; kept two independent Git repositories and existing safety boundaries.

## [0.2.0] — Explicit reusable workspace directory layout
- Standardized mandatory roots: `docs/`, `reference/`, `generated/`, `project/`.
- Added tracked instructional README.md files for reference, generated, generated/plans, generated/tickets, generated/reports and docs.
- The `/project/` directory is created by bootstrap and included empty in ZIP, yet remains completely excluded from Workspace Git.
- Replaced local `task-context/` and `generated-docs/` workflow paths with `generated/{tickets,plans,reports}`; old paths remain ignored for backward compatibility.
- Updated Git ignore allowlist, repository audit, standalone validator, Claude instructions, skills and tests.

## [0.1.0] — Initial portable Claude Code-only workspace
- Two independent Git repos (outer workspace; inner product), with separate ignore policies.
- Original Claude Code skills, six read-only reviewer agents, focused rules and project profile templates.
- Python guard, standalone scaffold validator, repository boundary auditor, bootstrap helper, unit tests and GitHub Actions CI.
