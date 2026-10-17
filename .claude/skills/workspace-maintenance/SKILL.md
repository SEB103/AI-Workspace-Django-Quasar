---
name: workspace-maintenance
description: Safely improve portable Claude Code rules skills hooks templates and validation
disable-model-invocation: true
---

# workspace-maintenance

1. Treat Workspace as MedicalPractice-specific AI tooling. Check `git -C . status` and **do not** access Product Git unless task explicitly requires it.
2. Keep rules focused on MedicalPractice; never embed real patient information, local absolute paths or credentials in tracked instructions.
3. Update manifest if adding/removing a skill; validate frontmatter, CLAUDE.md imports, AGENTS.md adapter and JSON settings.
4. Run `python .claude/scripts/validate_workspace.py --strict`, unittest and `repo_audit.py --workspace-only`.
5. Document compatibility and changes in `CHANGELOG.md`; provide diff for review; user decides to commit/push Workspace separately.
