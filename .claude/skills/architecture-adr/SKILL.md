---
name: architecture-adr
description: Record significant architectural decisions in product or workspace ADRs
---

# architecture-adr

1. State context, options, decision, tradeoffs and consequences. Confirm why design does not overengineer a single-practice deployment.
2. Distinguish **product** decisions (API/rendering/auth/deployment) from reusable **workspace** design.
3. Save product ADR under `project/docs/adr/` (tracked Product Git); universal tooling ADR under `docs/adr/` (tracked Workspace Git).
4. Do not store private client names, patient data or operational secrets in ADRs. Use `docs/templates/ADR.md`.
5. When decision evolves, supersede via a new ADR rather than silently rewriting history.
