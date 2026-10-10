---
name: django-domain
description: Implement Django domain models and services with transaction and migration discipline
---

# django-domain

1. Find the owning Django app and current models, migrations and tests. Avoid duplicate sources of truth.
2. Define domain invariants and related DB constraints: status, ownership, valid durations, cancellation, unique/overlap rules as feasible.
3. Choose services/queries/transactions only where business complexity warrants; validate on server even when frontend checks.
4. For booking concurrency use transaction strategy and tests against PostgreSQL, not only SQLite.
5. Make migration and backward compatibility plan; never delete patient data as convenience.
6. Add pytest(-django) tests for allowed/forbidden and races; update API/ADR if externally visible.
