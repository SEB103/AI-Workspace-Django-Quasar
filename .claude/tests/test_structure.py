import sys
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / '.claude/scripts'))
from validate_workspace import validate
from bootstrap import migrate_legacy_local_imports
from repo_audit import (invalid_paths, WORKSPACE_BLOCKED, PRODUCT_BLOCKED,
                        WORKSPACE_ALLOWED_LOCAL_GUIDES)


class StructureTests(unittest.TestCase):
    def test_scaffold(self):
        self.assertEqual(validate(), [])

    def test_codex_adapter_reuses_canonical_rules(self):
        adapter = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
        claude = (ROOT / 'CLAUDE.md').read_text(encoding='utf-8')
        self.assertIn('CLAUDE.md', adapter)
        self.assertIn('.claude/skills/', adapter)
        self.assertIn('.claude/agents/', adapter)
        self.assertIn('not automatically', adapter.lower())
        self.assertIn('MedicalPractice', claude)
        self.assertFalse(any(p.is_file() for p in (ROOT / '.claude/profiles').rglob('*')))
        self.assertFalse((ROOT / '.agents/skills').exists())

    def test_legacy_local_profile_migration_preserves_notes(self):
        with tempfile.TemporaryDirectory(prefix='mp-profile-') as tmp:
            path = Path(tmp) / 'CLAUDE.local.md'
            old = ('# Local active stack profile: django-quasar\n'
                   '# This file is ignored by Workspace Git; select another stack per project.\n\n'
                   '@.claude/profiles/django-quasar/rules/20-backend-python-django.md\n'
                   '@.claude/profiles/django-quasar/rules/30-frontend-typescript-quasar.md\n'
                   'Keep my local editor note.\n')
            path.write_text(old, encoding='utf-8')
            self.assertTrue(migrate_legacy_local_imports(path))
            self.assertIn('Keep my local editor note.', path.read_text(encoding='utf-8'))
            self.assertNotIn('@.claude/profiles/', path.read_text(encoding='utf-8'))
            self.assertEqual(path.with_name('CLAUDE.local.md.bak').read_text(encoding='utf-8'), old)
            self.assertFalse(migrate_legacy_local_imports(path))

    def test_workspace_allowed_readmes_and_blocked_generated(self):
        examples = [
            'project/backend/app.py', 'reference/example.pdf',
            'generated/tickets/A-1/README.md',
            'generated/plans/research.md', 'generated/random/screenshots/a.png',
        ]
        self.assertEqual(invalid_paths(examples, WORKSPACE_BLOCKED,
                                       WORKSPACE_ALLOWED_LOCAL_GUIDES), examples)
        allowed = sorted(WORKSPACE_ALLOWED_LOCAL_GUIDES)
        self.assertEqual(invalid_paths(allowed, WORKSPACE_BLOCKED,
                                       WORKSPACE_ALLOWED_LOCAL_GUIDES), [])

    def test_product_forbidden(self):
        for forbidden in ('CLAUDE.md', 'AGENTS.md', '.claude/skills/a/SKILL.md'):
            self.assertIn(forbidden, invalid_paths([forbidden], PRODUCT_BLOCKED))
        self.assertIn('generated/tickets/x.md', invalid_paths(['generated/tickets/x.md'], PRODUCT_BLOCKED))
        self.assertNotIn('backend/models.py', invalid_paths(['backend/models.py'], PRODUCT_BLOCKED))

    @unittest.skipUnless(shutil.which('git'), 'Git not installed')
    def test_real_gitignore_behavior(self):
        with tempfile.TemporaryDirectory(prefix='workspace-ignore-') as tmp:
            folder = Path(tmp)
            (folder / '.gitignore').write_bytes((ROOT / '.gitignore').read_bytes())
            subprocess.run(['git', 'init', '-q', str(folder)], check=True)
            should_ignore = [
                'project/backend/app.py', 'reference/source.pdf',
                'reference/nested/README.md',
                'generated/plans/plan.md', 'generated/tickets/A-1/README.md',
                'generated/reports/my-report.md', 'generated/new-folder/file.json',
                'task-context/tickets/a.md', 'generated-docs/summary.pdf',
            ]
            should_track = sorted(WORKSPACE_ALLOWED_LOCAL_GUIDES) + [
                'docs/README.md', 'docs/REPOSITORY_POLICY_RU.md', 'AGENTS.md',
            ]
            for name in should_ignore:
                result = subprocess.run(['git', '-C', str(folder), 'check-ignore',
                                         '-q', '--no-index', name])
                self.assertEqual(result.returncode, 0, 'Must ignore ' + name)
            for name in should_track:
                result = subprocess.run(['git', '-C', str(folder), 'check-ignore',
                                         '-q', '--no-index', name])
                self.assertEqual(result.returncode, 1, 'Must track ' + name)


if __name__ == '__main__':
    unittest.main()
