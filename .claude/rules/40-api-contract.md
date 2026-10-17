# REST API and OpenAPI contract
- All public/frontend/backend integration is via HTTP API with stable prefix (e.g. `/api/v1/`); API version is **distinct** from product version.
- Design resource/verb/error contracts explicitly: request/response schemas, validation, pagination, auth/CSRF or token scheme and permission failures.
- API endpoints must check object-level permissions, not only login or frontend visibility. Admin-only data must never appear in public serializers.
- Schema changes require compatibility review: old clients may remain deployed. Breaking changes need an API strategy and migration plan.
- OpenAPI is canonical generated/described contract; frontend API types and contract tests should derive from it where practical. Do not maintain divergent duplicates.
- Avoid giant endpoints exposing sensitive data unnecessarily. Standardize error handling, consistent date/time representations, and predictable status codes.
- Verify content API of Wagtail is read-only/public by default only where intended; never expose draft/private medical records through CMS.
