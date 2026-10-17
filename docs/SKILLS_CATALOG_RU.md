# Навыки и reviewer-агенты MedicalPractice

**Один канонический набор**: `.claude/skills/<name>/SKILL.md` и `.claude/agents/*.md`. Claude Code использует свои механизмы skills/subagents. Codex читает те же файлы по инструкции из `AGENTS.md`, **по мере необходимости**. Отдельных копий для Codex нет; автоматическое обнаружение и запуск Claude subagents в Codex не гарантируются.

## Skills (20)

| Skill | Режим Claude | Для чего |
|---|---|---|
| `api-contract` | По контексту | Maintain OpenAPI as contract between independent Python backend and TypeScript frontend |
| `auth-permissions` | По контексту | Plan and review patient/staff login authorization approval and session flows |
| `demo-fixtures` | По контексту | Create reproducible fictional demo practice users services and appointment fixtures |
| `dependency-review` | По контексту | Review Django Python Quasar npm and GitHub Actions dependencies and supply-chain risk |
| `django-domain` | По контексту | Implement Django domain models and services with transaction and migration discipline |
| `django-rest-api` | По контексту | Design and implement DRF resource endpoints with safe permissions and schema |
| `docker-deployment` | Manual | Design Docker Compose local and VPS staging deployment for single-practice Django Quasar stack |
| `github-actions` | По контексту | Develop diagnose and optimize two-repo GitHub Actions CI workflows |
| `plan-feature` | Manual | Plan nontrivial full-stack features and acceptance tests before implementation |
| `playwright-e2e` | По контексту | Create browser E2E flows for booking login approvals and content publication |
| `postgres-migrations` | По контексту | Safely author review and test PostgreSQL Django migrations |
| `quasar-vue` | По контексту | Build accessible Vue 3 Quasar TypeScript pages and components consuming REST API |
| `release-management` | Manual | Prepare release dry run version tag artifacts and GHCR without automatic publication |
| `review-changes` | Manual | Perform structured security architecture test and product-boundary code review of diffs |
| `security-privacy` | По контексту | Audit application security and EU/German medical privacy by threat modeling and tests |
| `systematic-debugging` | По контексту | Investigate regressions in Django Quasar PostgreSQL CI or deployment with reproducible evidence |
| `ticket-finish` | Manual | Close a local task after evidence-based tests, review and explicit outstanding risks |
| `ticket-start` | Manual | Create a local untracked task ticket and implementation checklist for Claude Code |
| `wagtail-content` | По контексту | Build Wagtail editorial models admin workflow and headless content API for Quasar |
| `workspace-maintenance` | Manual | Safely improve portable Claude Code rules skills hooks templates and validation |

## Reviewers (6)

`architecture-reviewer`, `backend-reviewer`, `frontend-reviewer`, `security-reviewer`, `test-reviewer`, `ci-release-reviewer` — read-only reviewer-инструкции. В Claude Code могут запускаться как специализированные агенты; в Codex используются как чеклисты, если нет отдельной совместимой механики запуска.

## Принцип простоты

Удалены пересекавшиеся playbooks `architecture-adr`, `documentation`, `git-pr-workflow`, `testing-strategy`, `verification-before-completion`: их требования уже закреплены в основных правилах и других skills. Новые skills добавлять только при повторяющейся реальной потребности, обновляя `manifest/skills.json` и тесты. Не создавать отдельный Codex-каталог копий.
