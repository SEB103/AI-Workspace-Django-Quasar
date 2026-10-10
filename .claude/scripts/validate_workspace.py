#!/usr/bin/env python3
"""Standalone structural validation of Claude Code Workspace (no Product needed)."""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = [
    'README_RU.md', 'CLAUDE.md', '.gitignore', 'LICENSE',
    '.claude/settings.json', '.claude/manifest/skills.json',
    '.claude/hooks/guard.py', '.claude/scripts/repo_audit.py',
    '.claude/profiles/django-quasar.example.yaml',
    'docs/README.md', 'docs/REPOSITORY_POLICY_RU.md',
    'reference/README.md', 'generated/README.md',
    'generated/plans/README.md', 'generated/tickets/README.md',
    'generated/reports/README.md',
    '.github/workflows/workspace-ci.yml',
]
IGNORE_RULES = [
    '/project/', '/reference/**', '!/reference/README.md',
    '/generated/**', '!/generated/README.md',
    '!/generated/plans/', '!/generated/plans/README.md',
    '!/generated/tickets/', '!/generated/tickets/README.md',
    '!/generated/reports/', '!/generated/reports/README.md',
    '/task-context/', '/generated-docs/',
]


def validate() -> list[str]:
    errors = []
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append('Missing ' + rel)
    ignored = (ROOT / '.gitignore').read_text(encoding='utf-8')
    ignore_lines = [line.strip() for line in ignored.splitlines()]
    for path in IGNORE_RULES:
        if path not in ignore_lines:
            errors.append('Missing exact ignore rule: ' + path)
    claude = (ROOT / 'CLAUDE.md').read_text(encoding='utf-8')
    for file in sorted((ROOT / '.claude/rules').glob('*.md')):
        if '@.claude/rules/' + file.name not in claude:
            errors.append('Missing CLAUDE.md import ' + file.name)
    settings = json.loads((ROOT / '.claude/settings.json').read_text(encoding='utf-8'))
    hooks = settings.get('hooks', {}).get('PreToolUse', [])
    if not any('guard.py' in str(h) for h in hooks):
        errors.append('No active PreToolUse guard')
    manifest = json.loads((ROOT / '.claude/manifest/skills.json').read_text(encoding='utf-8'))
    files = sorted((ROOT / '.claude/skills').glob('*/SKILL.md'))
    seen = {}
    for path in files:
        data = path.read_text(encoding='utf-8')
        m = re.match(r'\A---\n(.*?)\n---\n', data, re.S)
        if not m:
            errors.append('Missing frontmatter ' + str(path))
            continue
        fm = m.group(1)
        nm = re.search(r'^name:\s*([^\n]+)$', fm, re.M)
        ds = re.search(r'^description:\s*([^\n]+)$', fm, re.M)
        if nm is None or nm.group(1).strip() != path.parent.name:
            errors.append('Wrong skill name ' + path.parent.name)
        if ds is None:
            errors.append('Missing description ' + path.parent.name)
        if not data[m.end():].strip():
            errors.append('Empty skill ' + path.parent.name)
        seen[path.parent.name] = bool(re.search(r'^disable-model-invocation:\s*true$', fm, re.M))
    manifest_data = {it['name']: it.get('invocation') == 'manual'
                     for it in manifest.get('skills', [])}
    if len(files) != manifest.get('total'):
        errors.append('Skill count mismatch')
    if seen != manifest_data:
        errors.append('Skill names/invocation mismatch')
    for path in sorted((ROOT / '.claude/agents').glob('*.md')):
        data = path.read_text(encoding='utf-8')
        for literal in ('name: ' + path.stem, 'tools: Read, Grep, Glob'):
            if literal not in data:
                errors.append('Reviewer agent mismatch: ' + str(path))
    for rel in ('.codex', '.opencode', '.agents', 'AGENTS.md', 'opencode.jsonc'):
        if (ROOT / rel).exists():
            errors.append('Non-Claude adapter forbidden: ' + rel)
    return errors


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--strict', action='store_true')
    args = p.parse_args()
    problems = validate()
    if problems:
        for problem in problems:
            print('FAIL:', problem)
        sys.exit(1)
    print('Workspace validation OK (standalone; Product checkout not required).')
