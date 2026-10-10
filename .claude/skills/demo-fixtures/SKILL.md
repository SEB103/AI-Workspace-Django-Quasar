---
name: demo-fixtures
description: Create reproducible fictional demo practice users services and appointment fixtures
---

# demo-fixtures

1. Define clear demo identity and deterministic fixture seeds; NO references to real people, addresses, records or credentials.
2. Separate sample public content (Wagtail) from synthetic private test accounts and appointments.
3. Fixture loader must refuse non-demo and production modes by default; no silent replacement of a working database.
4. Idempotent fixtures where feasible; stable IDs or uniqueness checks; avoid credential reuse outside demo.
5. Document reset/seed command and CI integration; never include database dumps in Git.
6. Cover both normal scenarios and permission/overbooking negative tests.
