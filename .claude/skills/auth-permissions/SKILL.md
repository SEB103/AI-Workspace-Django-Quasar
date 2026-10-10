---
name: auth-permissions
description: Plan and review patient/staff login authorization approval and session flows
---

# auth-permissions

1. Model anonymous, registered-pending, approved patient, clinician, practice-admin and superuser separately; avoid role conflation.
2. Define exactly who may read/write each resource, plus patient approval/revocation, session expiration and audit events.
3. Prefer proven Django auth; select authentication for browser sessions with CSRF, reserve mobile tokens for explicitly designed flow.
4. Never use authorization based solely on frontend UI state or Wagtail group naming.
5. Add tests for IDOR, cross-user booking access, denied unauthenticated request and role downgrade, avoid real names.
6. Require security review before public-facing authentication/production.
