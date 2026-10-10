#!/usr/bin/env python3
"""Set up missing local folders and active Claude profile safely.

The Workspace owns project/ as a location only. Its contents are independent,
ignored, and NEVER initialized, overwritten, staged, or modified here.
"""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]

# The versioned README.md files already establish reference/ and generated/.
# On a fresh clone, the Product location must be created, because Git cannot
# store a completely ignored/empty project/ directory.
for rel in ('project', 'reference', 'generated', 'generated/plans',
            'generated/tickets', 'generated/reports', '.claude/local'):
    target = ROOT / rel
    target.mkdir(parents=True, exist_ok=True)
    print('Directory ready:', rel)

profile = ROOT / '.claude/project-profile.local.yaml'
example = ROOT / '.claude/profiles/project-profile.local.example.yaml'
if not profile.exists():
    shutil.copyfile(example, profile)
    print('Created ignored local profile:', profile.relative_to(ROOT))
else:
    print('Kept existing local profile.')

local_claude = ROOT / 'CLAUDE.local.md'
if not local_claude.exists():
    profile_imports = [
        '20-backend-python-django.md', '30-frontend-typescript-quasar.md',
        '40-api-contract.md', '50-testing-quality.md',
        '60-security-privacy.md', '80-release-deployment.md',
    ]
    lines = ['# Local active stack profile: django-quasar',
             '# This file is ignored by Workspace Git; select another stack per project.', '']
    lines.extend('@.claude/profiles/django-quasar/rules/' + name for name in profile_imports)
    local_claude.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('Created ignored Claude profile:', local_claude.relative_to(ROOT))
else:
    print('Kept existing CLAUDE.local.md')

print('Bootstrap OK. project/ exists but is fully ignored by Workspace Git.')
print('Clone/unpack the independent Product repository into project/ when ready.')
