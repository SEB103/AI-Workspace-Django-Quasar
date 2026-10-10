# Workspace documentation — `docs/`

**Versioned in Workspace Git.** This directory contains stable documentation for the reusable **Claude Code Workspace itself**: architecture, usage, repository policies, supported profile templates, skill catalog, validation instructions, and ADRs about the workspace tooling.

## What belongs here
- Reusable procedures and conventions for configuring or maintaining this workspace.
- Descriptions of Claude Code rules, skills, agents, hooks, scripts, validators and release procedures.
- Stable templates for universal documents; documented workspace changes and design decisions.

## What does NOT belong here
- Documentation of the Django/Quasar application itself: put it in `project/docs/` in the **Product Git**.
- Temporary plans, task records, investigations, AI chat summaries, generated PDF/DOCX or screenshots: put these in `generated/` (ignored).
- Outside reference files used for context: put them in `reference/` (ignored except its `README.md`).
- Secrets, passwords, real patient records, private client documents or personal data: do not place them in this public workspace.

All ordinary files in this directory are tracked by Workspace Git. Keep published documentation free from specific project secrets and temporary operational notes.
