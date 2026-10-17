# MedicalPractice AI Workspace documentation

Versioned in **Workspace Git**. This directory documents the AI development environment for MedicalPractice, not the Product application.

- `REPOSITORY_POLICY_RU.md`: two independent Git repositories and tracked/ignored boundaries.
- `SKILLS_CATALOG_RU.md`: canonical Claude skills; Codex can read relevant `SKILL.md` files on demand, without duplication.
- `SOURCES_AND_DECISIONS_RU.md`: provenance and current decisions, including the Codex adapter.
- `../CLAUDE.md`: canonical shared instructions and direct Claude rule imports.
- `../AGENTS.md`: short Codex adapter; does not duplicate skills, reviewers or hooks.

Product architecture, API and deployment documentation belong in `project/docs/` under Product Git. Temporary AI plans/reports belong in ignored `generated/`, source material in ignored `reference/`. Never commit secrets or real patient data.
