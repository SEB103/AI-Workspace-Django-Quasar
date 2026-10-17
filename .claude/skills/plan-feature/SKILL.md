---
name: plan-feature
description: Plan nontrivial full-stack features and acceptance tests before implementation
disable-model-invocation: true
---

# plan-feature

## Procedure
1. Inspect the actual `project/` structure and current implementation. If there is no product scaffold yet, plan scaffolding without pretending it exists.
2. State objective, user roles and permissions, explicit **out-of-scope** items. Separate public content, patient, staff and infrastructure work.
3. Trace needed Django models/DRF serializers/endpoints/Wagtail page types and Quasar screens. Map data ownership, privacy and API contract.
4. Identify migration, login, CSRF and booking conflicts; note alternatives and why simpler design is preferred.
5. Define tests: backend permission/integration, frontend unit, Playwright journey, CI, documentation.
6. Give incremental milestones and decision points; do not change code or choose production secrets without authorization.

Output: clear implementation plan with testable acceptance criteria, changed paths and risks. Save only if asked, under ignored `generated/plans/`.
