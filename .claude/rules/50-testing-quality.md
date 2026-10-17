# Testing and quality gates
- Test pyramid: domain/unit tests → DRF permission/serializer/integration tests with PostgreSQL → frontend unit/component tests → Playwright critical user journeys.
- CI must run real commands; test evidence is command + exit code. No `|| true`, hidden skips or non-blocking critical checks.
- At minimum cover approved vs pending patient, duplicate bookings, unavailable slots, cancelled appointments, access to other users' records, anonymous access and timezone/DST edge cases.
- For new code: implement behavior tests before or alongside feature. When diagnosing bugs, add a regression test.
- Choose Ruff, pytest(+pytest-django), ESLint, vue-tsc, Vitest and Playwright when bootstrapping actual app; pin versions in lock files.
- Validate migrations against disposable PostgreSQL and check unapplied model changes. Do not run destructive maintenance against real DB.
- Browser E2E uses fictional seeded identities, ephemeral DB, isolated URLs, no real emails or live payment systems.
- External AI workspace CI validates only workspace config; Product CI validates actual app, never requires Claude tooling.
