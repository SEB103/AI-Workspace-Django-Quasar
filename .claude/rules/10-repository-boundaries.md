# MedicalPractice two-repository boundary
- Workspace root `.` is Git A; Product root `project/` is Git B. They are physically nested but independent; `.gitignore` must contain anchored `/project/`.
- Product Git owns application code, tests, lockfiles, migrations, release and product docs; Workspace Git owns shared AI instructions, Claude skills/reviewers/hooks and workspace docs. Product builds without the Workspace.
- Never create a Git submodule/subtree, symlink product-to-workspace, or copy `.claude/`, `CLAUDE.md`, `AGENTS.md`, `.agents/`, AI tickets or generated reports into Product.
- Use `git -C .` for Workspace and `git -C project` for Product. Check `rev-parse --show-toplevel`, status and staged paths before Git writes.
- `reference/` and `generated/` contain tracked structural README files only; other contents are ignored. `task-context/` and `generated-docs/` remain ignored for backward compatibility.
- Workspace validation and CI must work with no Product checkout. Bootstrap may create the empty `project/` directory, but must not initialize, replace or modify Product Git.
