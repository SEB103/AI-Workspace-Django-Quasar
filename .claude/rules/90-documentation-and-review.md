# MedicalPractice documentation and review
- Product docs (`project/docs/`, API contract, CI/deploy/readme/license) are source-controlled in Product Git.
- AI plans, tickets, summaries and reports go into ignored `generated/` only when useful; external reference material into ignored `reference/`. Structural README files in these folders are tracked by Workspace Git.
- Architectural decisions affecting product users belong in `project/docs/adr/`; decisions about this AI workspace belong in tracked `docs/`.
- Use concise Russian for internal discussion and workspace guides, English for code identifiers and API names, German where appropriate for product UI.
- Reviewers are independent read-only evaluators; findings prioritized by severity and grounded in file/line evidence. Do not silently fix or commit during review.
- Completion report: files changed, purpose, commands/tests and actual results, unverified items, risks and needed approvals.
- For substantial delivery, consult `.claude/skills/verification-before-completion/SKILL.md` as a final checklist; for Git/PR changes consult `.claude/skills/git-pr-workflow/SKILL.md`. They are manual Claude skills, not automatically run hooks.
