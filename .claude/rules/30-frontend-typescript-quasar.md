# Frontend engineering — Vue 3 / Quasar / TypeScript
- Prefer Vue 3 Composition API with `<script setup lang="ts">` where useful; follow Quasar CLI (Vite) conventions selected by the real frontend initializer.
- Use strict TS types and generated API DTO types when available; avoid `any` and duplicated hand-maintained server schemas.
- UI components present state; domain/API access goes through typed frontend services/composables/stores as justified, not direct database or ad hoc fetch in every view.
- Handle loading, empty, validation, unavailable/error, auth-expired states, cancellation and network timeouts.
- Responsive/mobile-first, keyboard access, labels, focus indication, contrast, screen-reader semantics; evaluate German copy and potential localization.
- SEO/public-site strategy SPA vs SSR is a separate documented choice; do not silently introduce Nuxt/Next or a Node.js business backend.
- Do not embed secrets in client environment variables or static bundles. Server verifies ownership and permissions on all endpoints.
- Avoid excessive component fragmentation, framework mixing and speculative global stores. Reuse where it reduces duplication.
