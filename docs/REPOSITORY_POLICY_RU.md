# Два независимых Git-репозитория MedicalPractice

## Git A — AI Workspace

Отслеживает `CLAUDE.md`, `AGENTS.md`, `.claude/rules/`, `.claude/skills/`, `.claude/agents/`, Claude hooks, валидаторы, тесты, CI, документацию Workspace и структурные README в `reference/` и `generated/`.

Не отслеживает **весь** `/project/`, реальные исходные материалы в `reference/`, локальные планы/тикеты/отчёты в `generated/`, локальные инструкции, настройки, секреты, кэши и логи. Запрещено дублировать skills в `.agents/skills` или `.codex/skills`.

## Git B — MedicalPractice Product

Отслеживает Django backend, Quasar frontend, API, миграции, тесты, CI/CD, lockfiles, продуктовую документацию. Не отслеживает `.claude/`, `CLAUDE.md`, `AGENTS.md`, `.agents/`, AI-отчёты и реальные медицинские данные.

## Почему `project/` вложен физически

Claude Code и Codex запускаются из корня Workspace и получают доступ к коду `project/`, но **Git A не владеет файлами Git B**. Никаких submodules/subtrees и symlinks. Проверяй Git-корень явно:

```powershell
git -C . rev-parse --show-toplevel
git -C project rev-parse --show-toplevel
git -C . status
git -C project status
```

Bootstrap создаёт пустой `project/` при необходимости, но не инициализирует и не меняет Product Git. CI Workspace не требует наличия Product. Product CI не требует Workspace.

`AGENTS.md` автоматически читается Codex, но **не является автоматическим механизмом импорта `CLAUDE.md`**: Codex должен открыть файл по инструкции адаптера. Claude hooks и subagents не исполняются в Codex; review/skills доступны как текстовые инструкции.

Перед публикацией или разрушительными действиями требуется явное разрешение. Аудит: `python .claude/scripts/repo_audit.py --workspace-only`.
