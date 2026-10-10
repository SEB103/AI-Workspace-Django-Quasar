---
name: api-contract
description: Maintain OpenAPI as contract between independent Python backend and TypeScript frontend
---

# api-contract

1. Review existing `/api/v1/` endpoint schema, current responses, auth and error handling.
2. Change Django serializer/view first and regenerate OpenAPI with the selected schema tool once installed.
3. Generate or validate frontend DTO/client types against the schema, never hand-edit generated types.
4. Test backwards compatibility, nullable fields, date/time and paging, status/error cases and permission denial.
5. Add a Product CI contract check; commit schema and/or generation config as appropriate in `project/`.
