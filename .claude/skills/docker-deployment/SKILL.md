---
name: docker-deployment
description: Design Docker Compose local and VPS staging deployment for single-practice Django Quasar stack
disable-model-invocation: true
---

# docker-deployment

1. Check actual product compose/Dockerfiles and stage; no fake production deployment.
2. Separate immutable app image, static frontend assets, PostgreSQL durable volume, reverse proxy, media, secrets/config.
3. Provide local `.env.example`, health checks, readiness, schema migrations and deterministic bootstrap with demo-only fixtures gated by mode.
4. Production requires HTTPS, limited DB network exposure, backups+restore drill, logs without patient content, appropriate host patching.
5. Publish GHCR images by digest and product version only after tests; staging and production secrets must be independent.
6. No production deploy/migrate/rollback without explicit approval. Avoid Kubernetes or multi-tenant infrastructure without evidence.
