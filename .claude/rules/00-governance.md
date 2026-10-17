# MedicalPractice governance and scope
- This workspace exists specifically to develop **MedicalPractice** with Claude Code and Codex. Do not introduce generic stack-selection profiles, mirrored skills, or unnecessary agent infrastructure.
- `CLAUDE.md` is the authoritative shared contract; `AGENTS.md` is the minimal Codex adapter, not an independent ruleset.
- Use only applicable rules and on-demand skills. Avoid unnecessary ticket/report generation for small edits.
- Prefer explicit scope and observed evidence. Never report a command/test passed unless actually executed.
- Claude reviewer agents operate read-only. Codex may use their files as checklists but must not assume native subagent support.
- Never bypass patient-data/privacy boundaries, explicit approvals or repository separation.
