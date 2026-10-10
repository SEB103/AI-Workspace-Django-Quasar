# Каталог Claude Code skills

Skills размещены в `.claude/skills/<name>/SKILL.md`. **Manual** вызываются только пользователем через `/name`; остальные Claude может загрузить при релевантной задаче. Это локальные оригинальные playbooks: они не выполняют сетевые действия без отдельного решения.

| Skill | Режим | Назначение |
|---|---|---|
| `api-contract` | По контексту | Maintain OpenAPI as contract between independent Python backend and TypeScript frontend |
| `architecture-adr` | По контексту | Record significant architectural decisions in product or workspace ADRs |
| `auth-permissions` | По контексту | Plan and review patient/staff login authorization approval and session flows |
| `demo-fixtures` | По контексту | Create reproducible fictional demo practice users services and appointment fixtures |
| `dependency-review` | По контексту | Review Django Python Quasar npm and GitHub Actions dependencies and supply-chain risk |
| `django-domain` | По контексту | Implement Django domain models and services with transaction and migration discipline |
| `django-rest-api` | По контексту | Design and implement DRF resource endpoints with safe permissions and schema |
| `docker-deployment` | Manual | Design Docker Compose local and VPS staging deployment for single-practice Django Quasar stack |
| `documentation` | По контексту | Write concise product and workspace docs based on verified implementation |
| `git-pr-workflow` | Manual | Prepare focused branch commit and pull request workflows for either independent repository |
| `github-actions` | По контексту | Develop diagnose and optimize two-repo GitHub Actions CI workflows |
| `plan-feature` | Manual | Plan nontrivial full-stack features and acceptance tests before implementation |
| `playwright-e2e` | По контексту | Create browser E2E flows for booking login approvals and content publication |
| `postgres-migrations` | По контексту | Safely author review and test PostgreSQL Django migrations |
| `quasar-vue` | По контексту | Build accessible Vue 3 Quasar TypeScript pages and components consuming REST API |
| `release-management` | Manual | Prepare release dry run version tag artifacts and GHCR without automatic publication |
| `review-changes` | Manual | Perform structured security architecture test and product-boundary code review of diffs |
| `security-privacy` | По контексту | Audit application security and EU/German medical privacy by threat modeling and tests |
| `systematic-debugging` | По контексту | Investigate regressions in Django Quasar PostgreSQL CI or deployment with reproducible evidence |
| `testing-strategy` | По контексту | Design and execute Django pytest Quasar Vitest and cross-stack test gates |
| `ticket-finish` | Manual | Close a local task after evidence-based tests, review and explicit outstanding risks |
| `ticket-start` | Manual | Create a local untracked task ticket and implementation checklist for Claude Code |
| `verification-before-completion` | Manual | Verify actual code edits with tests and show factual evidence before marking task complete |
| `wagtail-content` | По контексту | Build Wagtail editorial models admin workflow and headless content API for Quasar |
| `workspace-maintenance` | Manual | Safely improve portable Claude Code rules skills hooks templates and validation |

## Принцип умеренного расширения

Не устанавливать сотни сторонних skills ради количества. Новые навыки добавлять только под повторяемый сценарий, который действительно встречается в проекте. При добавлении обновить `manifest/skills.json`, протестировать `validate_workspace.py` и существующие hooks.
