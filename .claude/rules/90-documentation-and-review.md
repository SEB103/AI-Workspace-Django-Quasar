# Docs, reviews, traceability
- Product docs (`project/docs/`, API contract, CI/deploy/readme/license) are source-controlled in Product Git.
- AI plans, tickets, summaries and reports go into ignored **contents** of `generated/`; source/reference materials into ignored **contents** of `reference/`. The README.md guide in each root/subfolder is tracked. Session summaries only by explicit request; do not auto-generate noisy reports.
- Architectural decisions that affect product users belong in `project/docs/adr/`; universal Claude Code design decisions in `docs/` of Workspace Git.
- Use concise Russian for discussion/workspace guidance, clear English for source identifiers and API names, German content in product if UI is German.
- Reviewer agents are independent read-only evaluators; findings prioritized by severity and grounded in file/line evidence. They must not silently fix or commit.
- Completion note: files changed, purpose, commands/tests and outcomes, limits/unverified items, risk/approval needed. No false claims of passing CI or deployed production.
- Retain legally required licenses and attribution when using third-party skills/templates; authored here from scratch.
