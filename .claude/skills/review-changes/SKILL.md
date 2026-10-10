---
name: review-changes
description: Perform structured security architecture test and product-boundary code review of diffs
disable-model-invocation: true
---

# review-changes

1. Determine which repo changed by checking **both** Git statuses/diffs separately.
2. Review product diff for contracts, migrations, patient-data permissions, UI behavior, tests, docs and secrets; workspace diff for universal reach and skill frontmatter.
3. Delegate independent read-only subagents as useful: backend-reviewer, frontend-reviewer, security-reviewer, test-reviewer, ci-release-reviewer.
4. Present findings severity-first (paths and reasons), then test evidence and unresolved risks.
5. Do not change files, merge or auto-commit as part of review without separately requested implementation.
