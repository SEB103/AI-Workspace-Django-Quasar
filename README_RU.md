# AI Workspace — Django / Quasar

Версионируемый **Claude Code-only** Workspace для разработки через два независимых Git-репозитория. Концепция рабочего места вдохновлена ReqDeck; ticket workflow и reviewer-проверки учитывают опыт SimplexPass.

## Обязательная структура

```text
AI-Workspace-Django-Quasar/
├── .git/                     # Git A: только Workspace
├── .gitignore                # Исключения и разрешённые README
├── CLAUDE.md                 # Главные инструкции Claude Code
├── .claude/                  # Skills, agents, rules, hooks, validators
├── .github/                  # CI самого Workspace
├── .vscode/                  # Переносимые настройки редактора
├── docs/                     # Документация Workspace: полностью под Git
│   └── README.md
├── reference/                # Локальные входные материалы: под Git лишь README
│   └── README.md
├── generated/                # Локальные результаты: под Git лишь README
│   ├── README.md
│   ├── plans/README.md
│   ├── tickets/README.md
│   └── reports/README.md
└── project/                  # Git B: Product; целиком игнорируется Git A
```

`docs/` — опубликованные справочные документы **самого Workspace**. `reference/` — локальные документы, архивы и исходные материалы, которыми Claude Code пользуется как контекстом. `generated/` — планы, тикеты, отчёты и любые дополнительные результаты, созданные в процессе работы. Их можно группировать в новые подпапки без изменения `.gitignore`.

Все README внутри `reference/` и `generated/` служат **версионируемыми инструкциями для пользователя**; любые другие файлы внутри этих каталогов игнорируются. `project/` — исключение: её нельзя включать в Workspace Git даже с `.gitkeep` или README, иначе появится двойное владение файлами. Поэтому ZIP содержит пустой `project/`, а `bootstrap.py` создаёт её после обычного `git clone`, если отсутствует. Собственный `README.md` есть в независимом Product Scaffold.

## Первоначальная установка (Windows)

После создания двух пустых репозиториев GitHub:

```powershell
cd E:\AI
git clone https://github.com/OWNER/AI-Workspace-Django-Quasar.git AI-Workspace-Django-Quasar
cd AI-Workspace-Django-Quasar

# Сначала клонируем независимый Product Git внутрь Workspace.
git clone https://github.com/OWNER/MedicalPractice-Platform.git project

# Bootstrap безопасен: существующий project/ не изменяется.
python .claude/scripts/bootstrap.py
python .claude/scripts/validate_workspace.py --strict
python -m unittest discover -s .claude/tests -p 'test_*.py' -v
python .claude/scripts/repo_audit.py
code .
claude
```

Если до клонирования Product запустить bootstrap, он создаст пустой `project/`. Тогда можно инициализировать в нём Product Git вручную (`git -C project init`) либо удалить **только действительно пустую** папку и выполнить `git clone ... project`. Никогда не удаляй папку с исходниками/историей продукта ради повторного клонирования.

При распаковке двух ZIP извлеки **содержимое** первого в корень Workspace, а содержимое архива Product Scaffold — непосредственно в `project/`. Не создавай лишнего промежуточного каталога.

## Независимые Git-репозитории

- Workspace Git: инструкции, skills, agents, hooks, scripts, профили-шаблоны, CI, docs/ и структурные README.
- Product Git (`project/.git`): Django backend, Quasar frontend, миграции, тесты, Compose, packaging, CI/release, продуктовая документация.
- Не используем submodules/subtrees. Для Git-команд указывай корень явно (`git -C project ...`), при изменениях проверяй `git rev-parse --show-toplevel`.
- `reference/`, `generated/`: Git A сохраняет лишь README; контент остаётся локальным. Устаревшие `task-context/` и `generated-docs/` также исключаются ради совместимости.

## Claude Code

Claude Code запускается **из корня Workspace**, чтобы загрузить `.claude/` и `CLAUDE.md`.

Bootstrap создаёт локальный профиль `CLAUDE.local.md` и `.claude/project-profile.local.yaml` при их отсутствии; они игнорируются. Django/Wagtail/DRF и Vue/Quasar/PostgreSQL правила активируются через профиль `.claude/profiles/django-quasar/`. Для нового стека сохрани универсальный Workspace и выбери другой профиль.

Полезные skills: `/ticket-start`, `/ticket-finish`, `/plan-feature`, `/api-contract`, `/review-changes`, `/github-actions`, `/release-management`. Полный каталог — `docs/SKILLS_CATALOG_RU.md`.

## Проверки

```powershell
python .claude/scripts/bootstrap.py
python .claude/scripts/validate_workspace.py --strict
python -m unittest discover -s .claude/tests -p 'test_*.py' -v
python .claude/scripts/repo_audit.py

git -C . check-ignore -v project/
git -C . check-ignore -v generated/tickets/example.md
git -C . check-ignore -v reference/specification.pdf
```

GitHub Actions Workspace выполняет свои проверки **без продуктового checkout**. Product GitHub Actions не зависит от Workspace.

## Безопасность и зрелость

Настоящие персональные/медицинские данные, пароли и токены нельзя помещать в Workspace, demos, тесты или CI. Gitignore не гарантирует безопасность при `git add -f`; CI и audit дополнительно проверяют tracked paths.

Этот ZIP содержит только scaffold и правила: настоящие Django/Quasar приложения, production security review и deploy будут отдельными этапами. Git-repo/remotes и GitHub-релизы здесь не создаются.
