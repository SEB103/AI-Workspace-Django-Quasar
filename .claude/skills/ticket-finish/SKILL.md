---
name: ticket-finish
description: Close a local task after evidence-based tests, review and explicit outstanding risks
disable-model-invocation: true
---

# ticket-finish

Task: $ARGUMENTS

1. Inspect `git -C project diff` and `git -C project status`; if Workspace changed inspect its separate diff.
2. Run relevant tests and CI-equivalent commands with actual outcomes; if unavailable, record BLOCKED with reason.
3. Check OpenAPI consumers, migrations, security and product docs; request read-only review when appropriate.
4. Update ignored `generated/tickets/<ID>/README.md` with changed files, tests, review, accepted risks, and follow-ups. Summaries only when requested.
5. Never commit/push/tag/merge/release automatically; present proposed Git action for user approval.
