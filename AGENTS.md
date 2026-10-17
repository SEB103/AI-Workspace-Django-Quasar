# Codex adapter — MedicalPractice AI Workspace

**Canonical instructions:** `CLAUDE.md` in this directory. **Do not duplicate or independently reinterpret the rules.**

1. Start Codex **from this workspace root**, not from `project/`. Before editing, read `CLAUDE.md`. Its `@.claude/rules/...` lines are **Claude Code imports, not Codex syntax**: open the referenced rule files yourself as applicable. Always apply `00-governance.md` and `10-repository-boundaries.md`; consult Git, security, API, frontend, backend, testing and release rules for relevant work.
2. Two separate Git roots: `.` is the AI Workspace, `project/` is the independent MedicalPractice Product repository. `project/` is ignored by Workspace Git. Inspect both roots before Git writes. Never copy AI-only files (`.claude/`, `CLAUDE.md`, `AGENTS.md`, `generated/`, `reference/`) into the Product.
3. All data in source, demos, tests and AI context must be fictional. Never commit patient records, credentials or secrets. Push, merge, tags, releases, destructive Git/DB operations and production deployment need explicit approval.
4. Canonical reusable workflows: `.claude/skills/<skill-name>/SKILL.md`; index: `.claude/manifest/skills.json`. Read only relevant skills **on demand**. Do not mirror skills under `.agents/` or `.codex/`.
5. Canonical reviewer checklists: `.claude/agents/*.md`. Codex can read/apply them for independent, read-only review; they are **not automatically registered Codex subagents**.
6. Claude's `.claude/hooks/guard.py` **does not run in Codex**. Enforce the same safety boundaries manually and run `python .claude/scripts/validate_workspace.py --strict` and relevant tests. Report only verification actually performed.

Product code, tests and product documentation belong exclusively in `project/`. Workspace instructions, skills and reviewer definitions belong exclusively here. Keep changes narrow and do not add a generic multi-project profile system.
