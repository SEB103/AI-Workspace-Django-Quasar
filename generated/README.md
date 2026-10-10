# Local Claude Code output — `generated/`

**This README and the documented subfolder READMEs are committed to Workspace Git. All other generated content is ignored by Workspace Git.**

`generated/` is the central **local output area** for temporary or project-specific work produced by Claude Code: plans, tickets, investigations, test notes, summaries, analysis results, screenshots, drafts, exported documents and other intermediate artifacts.

## Initial structure
- `plans/` — implementation plans, analyses and proposed milestones.
- `tickets/` — working records for individual tasks and acceptance checklists.
- `reports/` — explicitly requested progress, investigation, test or review reports.

New subdirectories (such as `artifacts/`, `screenshots/`, `exports/`, `diagrams/`) can be created whenever they become useful. They are ignored automatically; no `.gitignore` changes are necessary for ordinary generated files.

## Ownership and publishing
- **Workspace docs** with lasting reusable value go in tracked `docs/`, not here.
- **Product docs, code and permanent deliverables** go in `project/` under the independent Product Git, if they really are part of the product.
- This folder is not an archive or backup. Important local output must be backed up separately if needed.
- Never put secrets, credentials or real patient data in generated output.
- Avoid generating noisy session reports automatically; create them when the user requests them or when a workflow explicitly needs them.

Only the structural README files are versioned. To confirm: `git check-ignore -v generated/tickets/example.md` should identify the ignore rule.
