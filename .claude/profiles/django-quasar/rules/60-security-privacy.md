# Security and medical privacy (Germany / EU)
- All current data is fictional. Never introduce actual patient personal data, medical records, addresses, health questionnaires, passwords or emails into source, demos, snapshots, CI or AI prompts.
- Login account ≠ approved patient. Backend checks permission at object level for every read/write. Principle of least privilege for staff/admin and admin-only Wagtail.
- Use CSRF for cookie-based session writes; secure cookie attributes and HTTPS; consider token flow for later mobile app without casually storing tokens in localStorage.
- Minimize stored patient data: appointments may be personal data; sensitive health data requires stricter treatment and legal/security review before production.
- Protect API from abuse via appropriate rate limiting, login hardening, audit logging without PHI, safe file uploads, secret management and dependency updates.
- CI and logs contain synthetic data; redact secrets from errors; `.env` and production data must not be committed or placed in container images.
- Only publication-ready demos may be public. Production release requires separate DPIA/DSGVO-oriented assessment as needed, DPA/AVV with service providers, backup/restore verification and access controls. This workspace is no legal certification.
