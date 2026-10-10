---
name: testing-strategy
description: Design and execute Django pytest Quasar Vitest and cross-stack test gates
---

# testing-strategy

1. Classify feature requirements into unit, API integration, database, component and E2E tests.
2. For backend target `pytest`, `python manage.py check`, migration check and PostgreSQL service in CI once initialized.
3. For frontend target `vue-tsc`, ESLint, `vitest` and Quasar production build per chosen package scripts; no fictional commands.
4. For cross-stack, run local disposable PostgreSQL + Django + frontend and verify main appointment journey; Playwright must use fake records.
5. Investigate flaky tests and genuine error output; never silence a failing quality gate or report green without execution.
6. Report exact commands, status and tests not run.
