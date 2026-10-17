# Backend engineering — Django/DRF/Wagtail/PostgreSQL
- Django owns domain objects, state changes, user permissions, transaction boundaries, validation, and persistence. No business rules enforced **only** in frontend.
- Isolate domain responsibilities in meaningful Django apps (e.g. accounts, services, appointments, cms), not one class/file per tiny function and not premature microservices.
- Wagtail admin and Django Admin can use internal Django templates; public app stays API-driven. Wagtail is CMS/content workflow, Django Admin is trusted operational control.
- Use Django ORM and standard migrations. Avoid raw SQL unless justified. For booking race conditions reason about transactions, DB constraints, locking and retries.
- Choose custom User model early if requirements need one; avoid adding it late without a migration plan. Separate approved-patient status from login account and never trust client-supplied roles.
- Use explicit timezone-aware dates, time zones, appointment durations and DST constraints (Europe/Berlin local time vs persisted UTC).
- Prefer built-in Django/DRF features over new dependencies; document the purpose of any third-party package.
- Python style: comprehensible functions, types where useful, Ruff formatting/lint; short docstrings on non-obvious contracts; no speculative architecture.
- Be careful about Wagtail/DRF API compatibility and permissions; official docs are version-sensitive.
