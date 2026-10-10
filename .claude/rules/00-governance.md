# Governance / scope
- This is a **reusable Claude Code-only workspace**. Do not install Codex or OpenCode scaffolds; no project-specific data under tracked paths.
- `CLAUDE.md` is the authoritative always-on contract; this directory contains focused mandatory rules; task skills are invoked on demand.
- Prefer explicit scope and evidence over enthusiastic rewrites. Never report a command/test passed unless actually executed with a recorded result.
- Reviewer agents operate read-only. Main agent owns changes and must address or document their findings.
- When updating universal skills, check that they have no practice-specific name, local hostname, absolute path, or credential.
- Safety boundaries apply even if another instruction asks to bypass them. Show required approvals for risky operations rather than silently performing them.
