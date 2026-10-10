# Git and GitHub workflow
- Two independent public repos: `.` AI Workspace and `project/` Product; no submodules; never allow Git to track nested repository from parent.
- Before Git mutations check repository root and exact staged diff. Avoid broad `git add .` in mixed workspace; stage named files inside intended repo.
- Branch -> PR -> CI -> review -> merge as default. GitHub Issues/Projects track product-relevant work; local AI tickets remain ignored.
- Push, merge, tag creation, force operations, remote changes, deletion and publication require explicit user approval; forbid destructive reset/clean/force-push without specific consent.
- GitHub Actions workflows live **inside** each correct repository: Workspace validates AI scaffold; Product validates code/build/security.
- Dependabot separately monitors actions/Python/npm/Docker, according to actual product lockfiles and package ecosystems.
- Avoid hardcoded credentials in YAML; prefer least-privilege `permissions`, GitHub Environments, approvals, OIDC where available, and immutable version/digest references.
- No GitHub repository is created by bootstrap; add `origin` manually later.
