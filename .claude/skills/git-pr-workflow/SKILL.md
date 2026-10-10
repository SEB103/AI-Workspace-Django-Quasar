---
name: git-pr-workflow
description: Prepare focused branch commit and pull request workflows for either independent repository
disable-model-invocation: true
---

# git-pr-workflow

1. Identify **target** repo (workspace or product) and verify `rev-parse --show-toplevel`, status and remotes before changing anything.
2. Create feature branch if requested; stage only intended files by explicit paths; inspect `diff --cached`, ignored paths and secret scan.
3. Use scoped commit message and mention relevant GitHub Issue if real; no fabricated IDs.
4. Open PR only after authorization and availability of remote; describe changes, tests, known limitations and migration impacts.
5. Push, merge, rebase, release or force operations are never implicit. Do not reinitialize existing `.git` histories.
