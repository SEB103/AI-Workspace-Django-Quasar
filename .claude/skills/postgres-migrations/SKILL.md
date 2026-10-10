---
name: postgres-migrations
description: Safely author review and test PostgreSQL Django migrations
---

# postgres-migrations

1. Inspect current models, migrations, deployment DB assumptions and fixture dependencies.
2. Distinguish schema-only, backfill, irreversible/data deletion, index locking and rolling deploy compatibility.
3. Validate on disposable PostgreSQL with `makemigrations --check --dry-run`, `migrate --plan` and `migrate` when project is initialized.
4. Add constraints for business invariants, consider concurrent bookings and DST/timezone behavior.
5. Never reset DB, drop columns/tables or run against live/staging without explicit operator approval and backups.
6. Record rollback and data preservation strategy; update migration tests and run with realistic synthetic data.
