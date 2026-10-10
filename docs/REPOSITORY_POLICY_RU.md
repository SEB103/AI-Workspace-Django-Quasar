# Политика двух независимых Git-репозиториев

## Repository A — AI Workspace

**Отслеживается:** `CLAUDE.md`, Claude rules/skills/agents/hooks/scripts/tests/профили-шаблоны, `.github/` Workspace CI, переносимые `.vscode` настройки, универсальные `docs/` и **только утверждённые структурные README** в `reference/` и `generated/`.

**Не отслеживается:** `/project/` целиком, любые другие файлы в `reference/`, `generated/`, вложенные материалы планов, тикетов и отчётов, устаревшие `/task-context/`, `/generated-docs/`, локальные настройки, `.env`, credentials, logs, кэши, базы данных.

Исключения в `.gitignore` реализуют: `/reference/**` с разрешением `reference/README.md`; `/generated/**` с разрешением `generated/README.md` и README каталогов `plans/`, `tickets/`, `reports/`. Новые вложенные папки и выходные файлы остаются игнорируемыми по умолчанию.

## Repository B — Product

**Отслеживается:** код backend/frontend, миграции, dependency lockfiles, тесты, Compose, GitHub Actions, релизные метаданные, документация API/deployment и лицензии.

**Не отслеживается:** чужие AI инструкции/skills/agents (`.claude/`, `CLAUDE.md` и т. п.), настоящие данные пациентов, `.env`, секреты, дампы БД, собранные дистрибутивы, локальные логи и AI-тексты.

## Специальное правило `project/`

`project/` **обязательна в локальной структуре Workspace**, но полностью исключена из Repository A. Это не противоречие: ZIP может содержать пустую папку, а Git — нет; `python .claude/scripts/bootstrap.py` создаёт папку после клонирования Git. Не добавляйте в неё `.gitkeep` или Workspace `README`: этот каталог целиком принадлежит отдельному Product Git.

## Проверка

```powershell
python .claude/scripts/bootstrap.py
python .claude/scripts/validate_workspace.py --strict
python .claude/scripts/repo_audit.py

git -C . check-ignore -v project/
git -C . check-ignore -v reference/manual.pdf
git -C . check-ignore -v generated/tickets/local-1/README.md
```

При наличии двух Git-репозиториев отдельно проверяйте `git -C . rev-parse --show-toplevel` и `git -C project rev-parse --show-toplevel` и staged changes обоих. Не создавайте Git submodule/subtree.

`.gitignore` не запрещает `git add -f`, поэтому `repo_audit.py` отклоняет любой tracked файл в `generated/`/`reference/`, кроме явно разрешённых README. GitHub Actions запускает этот аудит; для Product важно также настроить secret scanning и review.

Для обзора назначения каталогов читайте `docs/README.md`, `reference/README.md`, `generated/README.md`.
