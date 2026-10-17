#!/usr/bin/env python3
"""Prepare local MedicalPractice workspace directories; migrate old generated imports.

Never initialize or modify the independent Product repository in project/.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
LEGACY_IMPORT = re.compile(r'^@\.claude/profiles/django-quasar/rules/[^\r\n]+$', re.MULTILINE)


def migrate_legacy_local_imports(local_claude: Path) -> bool:
    """Remove only obsolete generated profile imports; preserve custom local notes."""
    if not local_claude.is_file():
        return False
    old = local_claude.read_text(encoding='utf-8')
    if not LEGACY_IMPORT.search(old):
        return False
    new = LEGACY_IMPORT.sub('', old)
    new = re.sub(r'^# Local active stack profile: django-quasar\n', '', new)
    new = re.sub(r'^# This file is ignored by Workspace Git; select another stack per project\.\n', '', new)
    new = re.sub(r'\n{3,}', '\n\n', new).strip() + '\n'
    if not new.strip():
        new = '# Local machine-specific Claude instructions (optional).\n'
    backup = local_claude.with_name('CLAUDE.local.md.bak')
    if backup.exists():
        raise FileExistsError('Refusing to overwrite existing migration backup: ' + str(backup))
    backup.write_text(old, encoding='utf-8')
    local_claude.write_text(new, encoding='utf-8')
    return True


def bootstrap(root: Path = ROOT) -> None:
    for rel in ('project', 'reference', 'generated', 'generated/plans',
                'generated/tickets', 'generated/reports', '.claude/local'):
        (root / rel).mkdir(parents=True, exist_ok=True)
        print('Directory ready:', rel)
    local = root / 'CLAUDE.local.md'
    if migrate_legacy_local_imports(local):
        print('Migrated obsolete stack imports in CLAUDE.local.md; backup: CLAUDE.local.md.bak')
    elif local.exists():
        print('Kept existing CLAUDE.local.md')
    print('Bootstrap OK. Product repository remains untouched.')


if __name__ == '__main__':
    bootstrap()
