---
name: quasar-vue
description: Build accessible Vue 3 Quasar TypeScript pages and components consuming REST API
---

# quasar-vue

1. Inspect actual Quasar CLI structure, router, TS config and conventions; do not assume generated files already exist.
2. Define responsive page/component boundaries with reusable visual primitives, not 1-component-per-line fragmentation.
3. Keep typed API client outside components; include loading/empty/error/unauthorized and offline states.
4. Validate forms client-side for UX and assume server repeats every important check; never store secret keys in Vite env.
5. Include German-facing wording, accessibility semantics, keyboard/focus, mobile layout, theme contrast.
6. Write Vitest/unit and, for important flows, Playwright tests. Avoid framework/SSR architecture changes without ADR.
