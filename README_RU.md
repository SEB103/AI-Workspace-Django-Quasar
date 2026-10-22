# MedicalPractice — AI Workspace для Claude Code и Codex

Специализированная среда разработки MedicalPractice. **Два независимых Git-репозитория**: Workspace хранит AI-инструкции, skills, reviewer-агентов и инструменты; вложенный `project/` содержит только приложение MedicalPractice. Workspace не является универсальным шаблоном для других стеков.

## Локальная структура

```text
AI-Workspace-Django-Quasar/        # Git A: Workspace
├── .git/
├── CLAUDE.md                      # Канонические общие инструкции
├── AGENTS.md                      # Тонкий адаптер для Codex
├── .claude/
│   ├── rules/                     # Правила MedicalPractice (без профилей)
│   ├── skills/                    # Один каталог skills для Claude/Codex
│   ├── agents/                    # Claude reviewers / Codex review checklists
│   ├── hooks/                     # Только Claude Code
│   └── scripts/                   # Bootstrap, валидация, аудит
├── docs/                           # Документация Workspace
├── reference/                      # Локальные исходные материалы (игнорируются)
├── generated/                      # Локальные планы/тикеты/отчёты (игнорируются)
└── project/                        # Git B: MedicalPractice-Platform
    ├── .git/
    ├── backend/
    ├── frontend/
    ├── docs/
    └── ...
```

`project/` **полностью игнорируется** Workspace Git; вложенный Git не является submodule или subtree. Два репозитория имеют собственные ветки, коммиты, CI и `.gitignore`.

## Первоначальная установка (Windows / PowerShell)

```powershell
cd E:\AI
git clone https://github.com/SEB103/AI-Workspace-Django-Quasar.git
cd AI-Workspace-Django-Quasar
git clone https://github.com/SEB103/MedicalPractice-Platform.git project
python .claude/scripts/bootstrap.py
python .claude/scripts/validate_workspace.py --strict
python -m unittest discover -s .claude/tests -p 'test_*.py' -v
python .claude/scripts/repo_audit.py
```

Backend и Quasar frontend уже находятся в `master` Product-репозитория. Перед работой обновляй **только** `project/` после проверки локальных изменений:

```powershell
git -C project status
git -C project switch master
git -C project pull --ff-only origin master
```

Для PR и проверки CI из терминала установи GitHub CLI (`winget install --id GitHub.cli -e --source winget`) и выполни `gh auth login` (GitHub.com → SSH → Login with a web browser).

## Как запускать AI-инструменты

**Claude Code:** из корня Workspace выполни `claude`. Он читает `CLAUDE.md` с прямыми импортами правил, обнаруживает `.claude/skills/` и `.claude/agents/`, использует PreToolUse hook. Отдельный stack profile и `CLAUDE.local.md` для активации правил больше не нужны.

**Codex:** из того же корня Workspace запусти `codex`. Codex автоматически получает `AGENTS.md`. Этот файл предписывает прочитать `CLAUDE.md`, нужные `.claude/rules/*.md` и по задаче `.claude/skills/<name>/SKILL.md`. **Codex не интерпретирует `@`-импорты Claude автоматически**, не запускает Claude hooks и не регистрирует Claude reviewer-агентов как свои subagents. Reviewer-файлы можно использовать как read-only чеклисты.

Не запускай Codex/Claude Code из `project/` для этой схемы: там намеренно нет AI-инструкций. Не копируй `.claude/`, `CLAUDE.md`, `AGENTS.md` и AI-артефакты в Product Git. Skills/agents **не дублируются** в `.agents/` или `.codex/` — их автоматическое обнаружение Codex не обещается.

## Обновление существующего Workspace

После `git pull` запусти `python .claude/scripts/bootstrap.py`. Если старый локальный `CLAUDE.local.md` содержит автоматически сгенерированные импорты удалённого профиля, bootstrap удалит **только устаревшие импорты**, сохранит остальные заметки и создаст `CLAUDE.local.md.bak` (игнорируемую резервную копию). Если она уже существует, создаётся отдельная `.bak.1`, `.bak.2` и так далее, без перезаписи предыдущих копий. Если файл уже не содержит устаревших импортов, он не изменяется. Старый `.claude/project-profile.local.yaml` не нужен и может остаться локально; bootstrap его не трогает.

## Git и безопасность

- `git -C . status` — Workspace, `git -C project status` — Product; проверяй корень, ветку и staged diff перед записью.
- Product Git хранит код, тесты, миграции, CI, lockfiles и документацию продукта. Workspace Git — только AI-инфраструктуру.
- Никаких реальных пациентов, медицинских записей, паролей и секретов в репозиториях, тестах, логах и AI-контексте.
- Push, merge, теги, релизы, разрушительные операции и production deployment — только после явного разрешения.
- Claude guard — дополнительная защита, **не** песочница и **не** защита Codex. Он запрещает разрушительные команды (force-push, `reset --hard`, `rm -rf` и т. п.) и запрашивает подтверждение пользователя для merge PR, push в `master`/`main`, тегов, релизов, удаления веток и отката рабочих изменений. Для обоих инструментов необходимы Git-аудит и тесты.

## Проверки

```powershell
python .claude/scripts/validate_workspace.py --strict
python -m unittest discover -s .claude/tests -p 'test_*.py' -v
python .claude/scripts/repo_audit.py --workspace-only
```

Перед Git/PR-действиями используй `.claude/skills/git-pr-workflow/SKILL.md`, перед объявлением задачи завершённой — `.claude/skills/verification-before-completion/SKILL.md`. Оба — ручные Claude skills; Codex может прочитать их как чеклисты, без автоматической интеграции.

Workspace CI работает без Product checkout. Приложение собирается и тестируется отдельно через Product CI. Каталог навыков: `docs/SKILLS_CATALOG_RU.md`.
