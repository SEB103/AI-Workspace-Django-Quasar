---
name: wagtail-content
description: Build Wagtail editorial models admin workflow and headless content API for Quasar
---

# wagtail-content

1. Distinguish editorial content from private patient/appointment records. CMS stores public site pages and media, not confidential patient details.
2. Prefer Wagtail admin and built-in page/revision/publish functionality rather than bespoke CMS UI.
3. Define page types and structured fields for practice profile, services, FAQ, legal pages. Separate service pricing/scheduling operational data as appropriate.
4. Expose only published public content through a deliberately scoped API; verify Wagtail API permissions and drafts exclusion.
5. Keep Quasar frontend authoritative for public layout; Django templates are fine for Wagtail/Django staff admin.
6. Test content revision/publish, permission, missing fields, localisation/SEO metadata and frontend API type contracts.
