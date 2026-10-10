---
name: workspace-maintenance
description: Safely improve portable Claude Code rules skills hooks templates and validation
disable-model-invocation: true
---

# workspace-maintenance

1. Treat Workspace as a standalone product. Check `git -C . status` and **do not** access Product Git unless task explicitly requires it.
2. Update skills or rules generically; never bake project name, local absolute paths, medical text or private materials into shared instructions.
3. Update manifest if adding/removing a skill; validate YAML frontmatter, all CLAUDE.md @imports and JSON settings.
4. Run `python .claude/scripts/validate_workspace.py --strict`, unittest and `repo_audit.py --workspace-only`.
5. Document compatibility and changes in `CHANGELOG.md`; provide diff for review; user decides to commit/push Workspace separately.
