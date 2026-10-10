---
name: ticket-start
description: Create a local untracked task ticket and implementation checklist for Claude Code
disable-model-invocation: true
---

# ticket-start

Task: $ARGUMENTS

1. Confirm task ID/scope, or assign a temporary `LOCAL-YYYYMMDD-brief` ID when no tracking ID is given; do not invent GitHub issue numbers.
2. Read affected product code, contract and existing tests; record starting Git status separately for Workspace and Product.
3. Create `generated/tickets/<ID>/README.md` with summary, assumptions, acceptance criteria, impacted modules, risks and planned tests. Do not create files in `project/` other than requested implementation.
4. Note owner, branch or PR link only if actually known; no personal/clinical sample data.
5. Do not commit the ticket to either repository. Proceed through `/plan-feature` if multi-layer change.
