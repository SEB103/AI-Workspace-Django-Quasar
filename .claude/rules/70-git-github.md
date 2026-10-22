# Git and GitHub workflow — two independent repositories
- `.` is the AI Workspace Git repository; `project/` is the Product Git repository. No submodules or subtrees; never stage Product files in Workspace Git.
- Before Git mutations verify the intended repository root, current branch, status and exact staged diff. Stage explicit paths; avoid broad `git add .`.
- Default to feature branch → PR → CI → review → merge. Never merge into `master` without explicit user authorization.
- Push, PR merge, tag/release, deployment, remote changes, destructive history or database operations require explicit user approval; do not force-push or reset/clean destructively without specific consent.
- Commits use the user's own Git identity. Do not add AI attribution: no `Co-Authored-By: Claude`/Codex trailers and no "Generated with Claude Code"-style lines in commit messages, PR titles or PR descriptions.
- GitHub Actions workflows live in the correct repository: Workspace validates its own instructions/hooks; Product validates application code and builds independently.
- Never hardcode secrets in CI; prefer least-privilege permissions, protected environments and pinned dependencies.
