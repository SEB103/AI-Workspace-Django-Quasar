import sys
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / '.claude/scripts'))
from validate_workspace import validate
from repo_audit import (invalid_paths, WORKSPACE_BLOCKED, PRODUCT_BLOCKED,
                        WORKSPACE_ALLOWED_LOCAL_GUIDES)


class StructureTests(unittest.TestCase):
    def test_scaffold(self):
        self.assertEqual(validate(), [])

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
        self.assertIn('CLAUDE.md', invalid_paths(['CLAUDE.md'], PRODUCT_BLOCKED))
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
                'docs/README.md', 'docs/REPOSITORY_POLICY_RU.md',
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
