---
name: dependency-review
description: Review Django Python Quasar npm and GitHub Actions dependencies and supply-chain risk
---

# dependency-review

1. Inventory pinned direct/transitive deps, Python/Node compatibility and Wagtail/DRF/Django matrix from official release notes.
2. Identify vulnerable/outdated dependencies and license/maintenance risks; changes must be scoped and compatible.
3. Update lockfiles deterministically; review dependency tree, reproducible install and actual security notices.
4. Test backend/frontend, API and build; update Dependabot settings only when package manifests exist.
5. No surprise framework major upgrade or changes to tooling without user approval and risk assessment.
