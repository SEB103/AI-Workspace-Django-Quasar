---
name: systematic-debugging
description: Investigate regressions in Django Quasar PostgreSQL CI or deployment with reproducible evidence
---

# systematic-debugging

1. State observed result, expected result and exact environment/version; do not fix on intuition alone.
2. Reproduce minimally and capture safe logs (no tokens/patient data); decide backend/frontend/API/database/infra ownership.
3. Narrow fault with contract trace and tests; verify assumptions against code and network request/response.
4. Introduce a regression test first where feasible, implement minimal fix, run all impacted checks.
5. Avoid risky database resets and broad refactors; explain root cause and verify fix or label inconclusive.
