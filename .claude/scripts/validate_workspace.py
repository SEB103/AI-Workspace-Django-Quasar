#!/usr/bin/env python3
"""Validate MedicalPractice AI Workspace without requiring a Product checkout."""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = [
    'README_RU.md', 'CLAUDE.md', 'AGENTS.md', '.gitignore', 'LICENSE',
    '.claude/settings.json', '.claude/manifest/skills.json',
    '.claude/hooks/guard.py', '.claude/scripts/repo_audit.py',
    '.claude/scripts/bootstrap.py',
    'docs/README.md', 'docs/REPOSITORY_POLICY_RU.md',
    'reference/README.md', 'generated/README.md',
    'generated/plans/README.md', 'generated/tickets/README.md',
    'generated/reports/README.md', '.github/workflows/workspace-ci.yml',
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
    if errors:
        return errors
    ignored = (ROOT / '.gitignore').read_text(encoding='utf-8')
    ignore_lines = [line.strip() for line in ignored.splitlines()]
    for rule in IGNORE_RULES:
        if rule not in ignore_lines:
            errors.append('Missing exact ignore rule: ' + rule)
    claude = (ROOT / 'CLAUDE.md').read_text(encoding='utf-8')
    agents = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
    if 'CLAUDE.md' not in agents or '.claude/skills/' not in agents or '.claude/agents/' not in agents:
        errors.append('AGENTS.md must point to canonical Claude instructions, skills and reviewers')
    if 'project/' not in agents or 'not automatically' not in agents.lower():
        errors.append('AGENTS.md must document repository boundary and Codex limitations')
    if 'MedicalPractice' not in claude or 'Codex' not in claude:
        errors.append('CLAUDE.md must be project-specific and acknowledge Codex adapter')
    rules = sorted((ROOT / '.claude/rules').glob('*.md'))
    for path in rules:
        if '@.claude/rules/' + path.name not in claude:
            errors.append('Missing CLAUDE.md import ' + path.name)
    if len(rules) != 10:
        errors.append('Expected 10 MedicalPractice rule files, got ' + str(len(rules)))
    if any(p.is_file() for p in (ROOT / '.claude/profiles').rglob('*')):
        errors.append('Obsolete generic stack profile files are still present')
    settings = json.loads((ROOT / '.claude/settings.json').read_text(encoding='utf-8'))
    hooks = settings.get('hooks', {}).get('PreToolUse', [])
    if not any('guard.py' in str(h) for h in hooks):
        errors.append('No active Claude PreToolUse guard')
    manifest = json.loads((ROOT / '.claude/manifest/skills.json').read_text(encoding='utf-8'))
    if manifest.get('canonical_root') != '.claude/skills':
        errors.append('Incorrect canonical skills root')
    files = sorted((ROOT / '.claude/skills').glob('*/SKILL.md'))
    seen = {}
    for path in files:
        data = path.read_text(encoding='utf-8')
        match = re.match(r'\A---\n(.*?)\n---\n', data, re.S)
        if not match:
            errors.append('Missing frontmatter ' + str(path))
            continue
        fm = match.group(1)
        name = re.search(r'^name:\s*([^\n]+)$', fm, re.M)
        desc = re.search(r'^description:\s*([^\n]+)$', fm, re.M)
        if name is None or name.group(1).strip() != path.parent.name:
            errors.append('Wrong skill name ' + path.parent.name)
        if desc is None:
            errors.append('Missing description ' + path.parent.name)
        if not data[match.end():].strip():
            errors.append('Empty skill ' + path.parent.name)
        seen[path.parent.name] = bool(re.search(r'^disable-model-invocation:\s*true$', fm, re.M))
    manifest_data = {it['name']: it.get('invocation') == 'manual' for it in manifest.get('skills', [])}
    if len(files) != manifest.get('total'):
        errors.append('Skill count mismatch')
    if seen != manifest_data:
        errors.append('Skill names/invocation mismatch')
    for path in sorted((ROOT / '.claude/agents').glob('*.md')):
        data = path.read_text(encoding='utf-8')
        for literal in ('name: ' + path.stem, 'tools: Read, Grep, Glob'):
            if literal not in data:
                errors.append('Reviewer agent mismatch: ' + str(path))
    for rel in ('.codex', '.opencode', '.agents', 'opencode.jsonc'):
        if (ROOT / rel).exists():
            errors.append('Duplicate or unsupported adapter: ' + rel)
    return errors


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--strict', action='store_true')
    p.parse_args()
    problems = validate()
    if problems:
        for problem in problems:
            print('FAIL:', problem)
        sys.exit(1)
    print('MedicalPractice AI Workspace validation OK (Product checkout not required).')
