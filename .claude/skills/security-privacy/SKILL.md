---
name: security-privacy
description: Audit application security and EU/German medical privacy by threat modeling and tests
---

# security-privacy

1. Identify data classification and trust boundaries. In this demo ALL people/data fictional.
2. Check authorization at every API view/query, login brute-force/rate limits, CSRF/cookies/token handling, input validation, uploads and audit logs.
3. Ensure no PHI/secrets in repository, images, Actions logs, screenshots, public CMS, test fixtures, generated schemas.
4. Review vendor/hosting data processing, restricted staff access, retention/erasure, backups, incident handling before actual use.
5. Report findings by severity with concrete file/line and proof; separate code defects from legal obligations needing independent assessment.
6. Do not assert compliance or production readiness after an automated scan alone.
