---
name: playwright-e2e
description: Create browser E2E flows for booking login approvals and content publication
---

# playwright-e2e

1. Select user journey and accessibility expectations: visitor → account pending → clinician approval → authenticated booking → cancel.
2. Ensure an isolated test environment and seeded **fictional** profiles, no production URL/credentials.
3. Use stable selectors/accessible labels and wait for observable UI outcomes rather than sleeps.
4. Validate backend state and permissions; cover negative cases, no slots, already booked, denied cross-user changes, timezone DST.
5. Collect safe screenshots/traces only on failure and keep artifacts free of tokens and sensitive data.
6. Run locally and in GitHub Actions with browsers installed, pin tool versions in product lockfile.
