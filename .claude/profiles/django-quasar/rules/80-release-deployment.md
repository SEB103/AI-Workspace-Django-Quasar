# Build, releases and deployment
- Adapt ReqDeck principle: one metadata/version source -> local build/test -> verified canonical artifacts -> GitHub CI -> release -> staging -> production.
- Product CI/release workflows must be reproducible **without** AI Workspace. Version/tag consistency checked before publishing.
- Provide safe `workflow_dispatch` dry-run artifact generation; release by explicit `vX.Y.Z` tag only when every quality gate is green.
- Separate staging and production environments, secrets and databases; require explicit approval to deploy production. No accidental push-to-main auto-deploy to patient-facing site.
- Prefer Docker Compose + PostgreSQL + HTTPS reverse proxy for one-practice VPS, not Kubernetes/multi-tenant orchestration before real need.
- Publish Docker images to GHCR by immutable digest plus semver tags; perform health, migration, smoke tests and rollback planning. Do not bake database secrets into images.
- Distinguish public static Quasar demo on GitHub Pages from actual Django API and PostgreSQL server; Pages cannot host Python server.
- Treat mobile/Desktop packaging as later optional targets; do not block initial website for it.
