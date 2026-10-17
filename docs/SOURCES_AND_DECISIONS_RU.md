# Источники и решения MedicalPractice AI Workspace

## История

Первоначальный Workspace был основан на разделении внешней AI-среды и вложенного Product Git (опыт ReqDeck), локальном ticket workflow и read-only review (опыт SimplexPass), правилах безопасной разработки Django/DRF/Wagtail/PostgreSQL + Vue 3/Quasar/TypeScript. Первоначально он был универсальным и предназначался только для Claude Code.

## Источники исходной архитектуры (по документации первоначального Workspace)

- `ReqDeck.zip` — два Git-репозитория, политики Claude Code, CI и релизные практики.
- `SimplexPass_261005.zip` — локальный ticket workflow, read-only reviewer-агенты и процедуры закрытия задач.
- `AI_GUIDELINES_Qt_CPP_QML_Project_Qt5_V4.md` — общие принципы минимальных, поддерживаемых изменений; ограничения Qt/C++ в MedicalPractice не переносились.
- `Rules_for_Generating_DOCX_and_PDF_Technical_Documentation_v2_7.md` — требования только для отдельных документных задач, не часть обязательного цикла MedicalPractice.

Эти источники описывают происхождение принципов, **не** означают сохранения универсальных Qt/других профилей. Файлы оригинальных материалов не помещаются в публичный Workspace и хранятся локально в игнорируемом `reference/`, если необходимы.

## Актуальное решение

1. **MedicalPractice — единственный целевой продукт**. Нет переключаемых профилей стека и обещаний универсальной среды для будущих проектов.
2. **Два независимых Git-репозитория** сохраняются: внешний Workspace Git и внутренний Product Git в `project/`. Никаких submodules/subtrees.
3. **`CLAUDE.md` — канонические общие инструкции**, `.claude/rules/*.md` — конкретные правила MedicalPractice. Stack-specific правила перенесены из старого `.claude/profiles/django-quasar/rules/` в общий набор.
4. **`AGENTS.md` — минимальный адаптер Codex**, который предписывает открыть `CLAUDE.md` и применимые правила. Это не встроенный импорт: Codex автоматически читает `AGENTS.md`, но не обязан понимать Claude `@`-директивы.
5. **Один каталог skills и reviewers** под `.claude/`. Codex может читать их как инструкции, но Claude hooks/subagents и автообнаружение skills не становятся автоматически функциями Codex.
6. Три дублирующих skills объединены с правилами; 22 skills остаются, включая отдельные процедурные `git-pr-workflow` и `verification-before-completion`. Reviewer-агенты остаются read-only.
7. Bootstrap создаёт локальные каталоги и безопасно мигрирует старые автоматически сгенерированные импорты `CLAUDE.local.md`; существующие резервные копии не перезаписывает, не изменяет Product Git.
8. Workspace CI валидирует только Workspace; Product CI — независимо приложение. Секреты и реальные медицинские данные запрещены в обоих репозиториях.

См. `README_RU.md`, `docs/REPOSITORY_POLICY_RU.md` и `docs/SKILLS_CATALOG_RU.md`. Для разработки Codex ориентируйся на `AGENTS.md` в корне Workspace.
