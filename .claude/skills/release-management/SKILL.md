---
name: release-management
description: Prepare release dry run version tag artifacts and GHCR without automatic publication
disable-model-invocation: true
---

# release-management

Target release: $ARGUMENTS

1. Verify **Product** repository and clean state; no changes to workspace origin or tags.
2. Read `project/packaging/product.json` as version source, checks and CHANGELOG. Match proposed tag `vX.Y.Z` exactly.
3. Require green product CI, successful reproducible build, migrations check, contract tests and security review.
4. Prefer a manual `workflow_dispatch` DRY RUN that creates artifacts but no Release, deploy, Pages update or external effects.
5. On explicit user permission only: prepare/push tag, publish GHCR/images, GitHub Release, deployment artifacts; verify digests and download URLs.
6. Never claim a tested release before actual GH run; note production deployment is separately approved.
