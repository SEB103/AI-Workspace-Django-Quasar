# Workspace changelog

## [Unreleased]
- Added `.gitattributes` forcing LF line endings so `MANIFEST_SHA256.txt` checksums and workspace tests pass on Windows checkouts with `core.autocrlf=true`.
- Removed root `.vscode/` settings from Workspace Git (VS Code is used from `project/`); the root `.vscode/` is now fully ignored.
- Guard hook: new `ask` decisions for PR merge, push to `master`/`main` (explicit refspec or bare push from a checked-out protected branch), tag push, GitHub release, remote/forced branch deletion and discarding working-tree changes; closed `rm -fr`/`rm -r -f`/`--recursive --force` and `+refspec` force-push bypasses; extended guard tests.
- `CLAUDE.md`: globally installed plugins (superpowers) save specs/plans under ignored `generated/plans/`, never auto-commit; workspace skills win on name clashes.
- `70-git-github` rule and `git-pr-workflow`: no AI attribution in commits/PRs; GitHub CLI command checklist.
- Workspace CI: actions pinned by commit SHA (`checkout` v7.0.1, `setup-python` v7.0.0, Node 24), push trigger limited to `master`; Dependabot for GitHub Actions.
- `review-changes` lists `architecture-reviewer`; `settings.local.json.example` is now a valid settings skeleton; README_RU updated (Quasar already in Product `master`, GitHub CLI setup, guard behaviour); skills catalog documents global plugin precedence.

## [0.3.1] — Restore essential workflows and harden bootstrap migration
- Restored `git-pr-workflow` and `verification-before-completion` with their original manual-invocation safeguards (22 skills in one canonical directory).
- Bootstrap now keeps existing `CLAUDE.local.md.bak` files, allocating numbered backups for further migrations; migration regression tests added.
- Workspace validator permits additional imported project rules but still requires all critical MedicalPractice rules and the two manual workflows.
- Updated skills catalog, provenance, tests, onboarding and SHA-256 manifest. Codex remains a thin `AGENTS.md` adapter with no separate configuration.

## [0.3.0] — MedicalPractice-specific Claude Code + Codex workspace
- Removed generic stack profile selection; promoted six Django/Quasar/API/testing/privacy/release rules into `.claude/rules/` and imported them directly from `CLAUDE.md`.
- Added minimal root `AGENTS.md` adapter for Codex. Canonical rules, 22 skills and 6 read-only reviewer definitions remain shared without duplicated Codex copies.
- Initially removed five skills; v0.3.1 restored two essential Git and final-verification workflows. Three overlapping skills remain consolidated into rules.
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
