# Two-repository filesystem boundary
- Workspace root `.` is Git Repository A; application root `project/` is Git Repository B, **physically nested but independent**.
- Workspace `.gitignore` MUST have `/project/` anchored at the root. Product `.gitignore` MUST ignore AI artifacts without ignoring `.github/`, migrations, lockfiles or product docs.
- No Git submodule/subtree, vendor copy of outer skills, or symlink pointing from product into workspace.
- For workspace status/commit: `git -C . status`; for product: `git -C project status`. Avoid ambiguous bare Git commands inside shell scripts.
- Before staging check `git -C . rev-parse --show-toplevel` and `git -C project rev-parse --show-toplevel` (when initialized). Check staged files with `git -C <root> diff --cached --name-only`.
- `generated/` and `reference/` contain tracked **structural README.md files only**; all working content is ignored. Legacy `task-context/` and `generated-docs/` remain ignored. Docs needed by product consumers go in `project/docs/`, not AI working directories.
- NEVER copy `.claude`, `CLAUDE.md`, `.agents`, AI ticket folders or generated reports into product. `gitignore` alone is not a security barrier.
- Bootstrap must create `project/` when missing; Workspace validation/CI must not inspect product sources or require a Product checkout. Product must build standalone without Workspace.
