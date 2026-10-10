---
name: django-rest-api
description: Design and implement DRF resource endpoints with safe permissions and schema
---

# django-rest-api

1. Identify resource, URL, serializer, authentication mode, permissions, ownership filtering and failure contract.
2. Apply object-level and queryset restrictions; never trust input `user_id`, patient status, or admin flags.
3. Use Django validation/model constraints and transactions for state changes; return consistent status codes.
4. Keep `/api/v1/` contract and OpenAPI synchronized, including documentation of error cases.
5. Add auth/anonymous/approved/pending/other-user tests, pagination when needed, and HTTP edge cases.
6. Check frontend consumers or generated DTOs to prevent accidental breaking changes.
