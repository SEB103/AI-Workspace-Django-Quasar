# MedicalPractice AI Workspace

Project-specific AI development workspace for [MedicalPractice-Platform](https://github.com/SEB103/MedicalPractice-Platform), shared by **Claude Code** and **Codex**. The independent Product Git checkout lives in the ignored `project/` directory.

- **Claude Code:** start from the Workspace root; reads `CLAUDE.md`, `.claude/rules/`, and native skills/reviewers/hooks.
- **Codex:** start from the Workspace root; reads `AGENTS.md`, which points to canonical `CLAUDE.md` and the same on-demand skills/reviewer checklists. Claude-specific imports, hooks and subagents do not automatically run in Codex.
- **One copy** of rules, skills and reviewer definitions; no generic multi-stack profiles or duplicated Codex skills.

See [README_RU.md](README_RU.md) for setup, repository boundaries and verification commands.
