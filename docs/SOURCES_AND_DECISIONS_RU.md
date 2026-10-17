# Источники и решения MedicalPractice AI Workspace

## История

Первоначальный Workspace был основан на разделении внешней AI-среды и вложенного Product Git (опыт ReqDeck), локальном ticket workflow и read-only review (опыт SimplexPass), правилах безопасной разработки Django/DRF/Wagtail/PostgreSQL + Vue 3/Quasar/TypeScript. Первоначально он был универсальным и предназначался только для Claude Code.

## Актуальное решение

1. **MedicalPractice — единственный целевой продукт**. Нет переключаемых профилей стека и обещаний универсальной среды для будущих проектов.
2. **Два независимых Git-репозитория** сохраняются: внешний Workspace Git и внутренний Product Git в `project/`. Никаких submodules/subtrees.
3. **`CLAUDE.md` — канонические общие инструкции**, `.claude/rules/*.md` — конкретные правила MedicalPractice. Stack-specific правила перенесены из старого `.claude/profiles/django-quasar/rules/` в общий набор.
4. **`AGENTS.md` — минимальный адаптер Codex**, который предписывает открыть `CLAUDE.md` и применимые правила. Это не встроенный импорт: Codex автоматически читает `AGENTS.md`, но не обязан понимать Claude `@`-директивы.
5. **Один каталог skills и reviewers** под `.claude/`. Codex может читать их как инструкции, но Claude hooks/subagents и автообнаружение skills не становятся автоматически функциями Codex.
6. Избыточные skills объединены с правилами; оставшиеся 20 используются по задаче. Reviewer-агенты остаются read-only.
7. Bootstrap создаёт локальные каталоги и безопасно мигрирует старые автоматически сгенерированные импорты `CLAUDE.local.md`, не изменяя Product Git.
8. Workspace CI валидирует только Workspace; Product CI — независимо приложение. Секреты и реальные медицинские данные запрещены в обоих репозиториях.

См. `README_RU.md`, `docs/REPOSITORY_POLICY_RU.md` и `docs/SKILLS_CATALOG_RU.md`. Для разработки Codex ориентируйся на `AGENTS.md` в корне Workspace.
