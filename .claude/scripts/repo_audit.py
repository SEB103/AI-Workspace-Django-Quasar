#!/usr/bin/env python3
"""Audit two independent Git tracked-file lists; allow only local-dir guides."""
from pathlib import Path
import subprocess
import argparse
import sys

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_BLOCKED = {'project', 'task-context', 'reference', 'generated-docs', 'generated'}
WORKSPACE_ALLOWED_LOCAL_GUIDES = {
    'reference/README.md',
    'generated/README.md',
    'generated/plans/README.md',
    'generated/tickets/README.md',
    'generated/reports/README.md',
}
PRODUCT_BLOCKED = {'.claude', '.codex', '.agents', '.opencode', 'task-context',
                   'reference', 'generated', 'generated-docs', 'CLAUDE.md',
                   'AGENTS.md', 'opencode.jsonc'}


def tracked(root: Path):
    proc = subprocess.run(['git', '-C', str(root), 'ls-files', '--cached', '-z'],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode:
        if (root / '.git').exists():
            raise RuntimeError('git ls-files failed: ' + proc.stderr.decode('utf-8', 'replace'))
        return None
    return [s.decode('utf-8', 'replace').replace('\\', '/')
            for s in proc.stdout.split(b'\x00') if s]


def invalid_paths(items: list[str], forbidden: set[str], allowed: set[str] | None = None):
    allowed = allowed or set()
    return [p for p in items if p not in allowed and
            (p.split('/')[0] in forbidden or p.split('/')[-1] in {'.env', '.env.production'})]


def audit(workspace_only=False):
    issues = []
    checks = [('Workspace', ROOT, WORKSPACE_BLOCKED, WORKSPACE_ALLOWED_LOCAL_GUIDES)]
    if not workspace_only:
        checks.append(('Product', ROOT / 'project', PRODUCT_BLOCKED, set()))
    for label, root, forbidden, allowed in checks:
        if not root.exists():
            continue
        paths = tracked(root)
        if paths is None:
            print(label + ': no Git metadata (normal before init/clone)')
            continue
        failures = invalid_paths(paths, forbidden, allowed)
        issues.extend(f'{label}: forbidden tracked: {p}' for p in failures)
        print(label + f': {len(paths)} tracked file(s), {len(failures)} forbidden')
    return issues


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--workspace-only', action='store_true')
    options = p.parse_args()
    errors = audit(options.workspace_only)
    if errors:
        for e in errors:
            print('FAIL:', e)
        sys.exit(1)
    print('Repository boundary audit OK')
