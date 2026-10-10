# Claude Code — reusable AI Development Workspace

**Claude Code only.** Workspace Git root: this directory; nested Product Git root: `project/`. Always start Claude Code **from this workspace root** to load `.claude` skills, subagents and hooks. Never start inside `project/` for this setup.

## Non-negotiable two-repository boundaries
1. Workspace Git holds **only** reusable Claude Code rules, skills, agents, hooks, scripts, profile templates, Workspace documentation and structural directory README files.
2. Product Git in `project/` independently holds product sources, tests, CI/CD, lockfiles and documentation; it must build and test without the Workspace.
3. Ignored and local in **both** repositories: `generated/` work output, `reference/` contents (except directory README files), legacy `task-context/`/`generated-docs/`, `CLAUDE.local.md`, `.claude/project-profile.local.yaml`, `.claude/settings.local.json`, caches and credentials.
4. Never copy `.claude/`, `CLAUDE.md`, `AGENTS.md`, AI skills or generated AI reports into `project/`. Never use Git submodules/subtrees between them.
5. Before Git mutation verify root and stage precisely: `git -C .` for Workspace; `git -C project` for Product.
6. Never use real personal/medical records or secrets in source, demos, tests, AI prompts, CI outputs or screenshots.

## Selectable project profiles
- The always-on core rules below are general and safe for future Qt, Python, web or other projects.
- Project-dependent rules are maintained under `.claude/profiles/<stack>/rules/`. The ready-made `django-quasar` profile covers Django/DRF/Wagtail/PostgreSQL + Vue3/Quasar/TypeScript.
- Run `python .claude/scripts/bootstrap.py` once: it creates an **ignored** `CLAUDE.local.md` that imports selected stack rules plus `.claude/project-profile.local.yaml`.
- For another product choose/create another stack profile, then change the **local files**. Do not change the universal `CLAUDE.md` just to select a new stack.
- If local activation file is missing, initialize profile before product work.
- On-demand skills remain in `.claude/skills/`; apply a skill only when its technology is relevant to the current product.

## Development principles
- Understand existing code, contracts, migration history and tests before edits; plan complex changes and keep diffs narrow.
- Prefer readable code, simple architecture, purposeful functions and minimal dependencies. No speculative rewrite, needless layers, multitenancy or Kubernetes.
- Use real test evidence and read-only reviewer agents; report unrun commands rather than inventing passing CI.
- User authorization is required before push, PR merge, tags, releases, production deployments, destructive Git/DB operations.
- Product documentation belongs in `project/docs/`; stable Workspace guidance belongs in tracked `docs/`; AI working notes and outputs belong in ignored `generated/` files. `reference/` holds local source materials.
- Workspace CI must pass with no product checkout; Product CI must pass without AI Workspace. Bootstrap creates `project/` if missing, without adding it to Workspace Git.

## Mandatory universal rules
@.claude/rules/00-governance.md
@.claude/rules/10-repository-boundaries.md
@.claude/rules/70-git-github.md
@.claude/rules/90-documentation-and-review.md

## Commands and guides
- Skills: `.claude/skills/*/SKILL.md`; catalog `docs/SKILLS_CATALOG_RU.md`.
- Agents: `.claude/agents/` (read-only).
- Bootstrap: `python .claude/scripts/bootstrap.py`.
- Validate: `python .claude/scripts/validate_workspace.py --strict`.
- Tests: `python -m unittest discover -s .claude/tests -p 'test_*.py' -v`.
- Git boundary audit: `python .claude/scripts/repo_audit.py`.
