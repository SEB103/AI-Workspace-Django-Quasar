# Источники и технические решения

Источники, предоставленные пользователем:
- `ReqDeck.zip`: разделение внешнего AI Workspace и вложенного `project/`, Claude Code policies/skills, GitHub Actions CI, release workflow, единый `packaging/product.json`, dry run.
- `SimplexPass_261005.zip`: локальный ticket workflow, review/test/security subagents и строгие правила завершения задач.
- `AI_GUIDELINES_Qt_CPP_QML_Project_Qt5_V4.md`: только общие принципы читаемого, поддерживаемого, минимально изменяемого кода; конкретные C++/Qt5 ограничения не переносились.
- `Rules_for_Generating_DOCX_and_PDF_Technical_Documentation_v2_7.md`: при **отдельном** запросе создания документов соблюдать документные требования; универсальный Workspace не содержит закрытых внутренних reference-файлов.

Ключевые отличия новой реализации:
1. Claude Code **единственный** AI-инструмент; удалены адаптеры Codex/OpenCode и их дублированные skills.
2. Внешний Workspace стал самостоятельным Git-репозиторием; `project/` — второй, полностью независимый репозиторий.
3. Проектно-локальные задачи и генерации исключены из обоих Git.
4. Stack profiles переключаются без изменения универсальных правил; для этого проекта готов шаблон Django+DRF+Wagtail+PostgreSQL / Vue3+Quasar+TypeScript.
5. Встроены валидаторы структуры/skills/Git boundary и ограниченный Python PreToolUse guard (защита от типичных случайностей; не песочница безопасности).
6. Workspace CI проходит без продуктов. Product CI самостоятельный.
7. Программный код и сторонние skills из архивов **не копировались**. Skills, rules и hooks в этом ZIP созданы специально для новой задачи.

Для выбора механики Claude Code сверено с официальными материалами:
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/settings

Версии SDK, Django, Wagtail, Node и Python намеренно не выдумывались: при фактическом bootstrap будут закреплены проверенные совместимые версии и lockfiles.

7. Стековые правила изолированы в `.claude/profiles/django-quasar/rules/` и активируются через игнорируемый `CLAUDE.local.md`. Общий `CLAUDE.md` не привязан к стеку.
