import sys
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / '.claude/scripts'))
import validate_workspace as validator_module
from validate_workspace import validate
from bootstrap import migrate_legacy_local_imports, bootstrap
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

    def test_legacy_migration_preserves_preexisting_backup(self):
        with tempfile.TemporaryDirectory(prefix='mp-profile-collision-') as tmp:
            path = Path(tmp) / 'CLAUDE.local.md'
            old = '@.claude/profiles/django-quasar/rules/20-backend-python-django.md\nMy own notes.\n'
            path.write_text(old, encoding='utf-8')
            path.with_name('CLAUDE.local.md.bak').write_text('prior copy', encoding='utf-8')
            path.with_name('CLAUDE.local.md.bak.1').write_text('older copy', encoding='utf-8')
            self.assertTrue(migrate_legacy_local_imports(path))
            self.assertEqual(path.with_name('CLAUDE.local.md.bak').read_text(encoding='utf-8'), 'prior copy')
            self.assertEqual(path.with_name('CLAUDE.local.md.bak.1').read_text(encoding='utf-8'), 'older copy')
            self.assertEqual(path.with_name('CLAUDE.local.md.bak.2').read_text(encoding='utf-8'), old)
            self.assertEqual(path.read_text(encoding='utf-8'), 'My own notes.\n')
            self.assertFalse(migrate_legacy_local_imports(path))

    def test_essential_manual_workflows_restored(self):
        import json
        manifest = json.loads((ROOT / '.claude/manifest/skills.json').read_text(encoding='utf-8'))
        by_name = {entry['name']: entry for entry in manifest['skills']}
        for name in ('git-pr-workflow', 'verification-before-completion'):
            self.assertEqual(by_name[name]['invocation'], 'manual')
            text = (ROOT / '.claude/skills' / name / 'SKILL.md').read_text(encoding='utf-8')
            self.assertIn('disable-model-invocation: true', text)
        self.assertEqual(manifest['total'], 22)

    def test_validator_allows_additional_imported_rule(self):
        with tempfile.TemporaryDirectory(prefix='mp-validate-extra-') as tmp:
            ws = Path(tmp) / 'workspace'
            shutil.copytree(ROOT, ws, ignore=shutil.ignore_patterns('.git', 'project', '__pycache__'))
            (ws / '.claude/rules/95-extra.md').write_text('# Extra rule\n', encoding='utf-8')
            with (ws / 'CLAUDE.md').open('a', encoding='utf-8') as f:
                f.write('\n@.claude/rules/95-extra.md\n')
            with patch.object(validator_module, 'ROOT', ws):
                self.assertEqual(validator_module.validate(), [])

    def test_validator_rejects_missing_critical_rule(self):
        with tempfile.TemporaryDirectory(prefix='mp-validate-missing-') as tmp:
            ws = Path(tmp) / 'workspace'
            shutil.copytree(ROOT, ws, ignore=shutil.ignore_patterns('.git', 'project', '__pycache__'))
            (ws / '.claude/rules/70-git-github.md').unlink()
            with patch.object(validator_module, 'ROOT', ws):
                errors = validator_module.validate()
            self.assertTrue(any('Missing mandatory MedicalPractice rule: 70-git-github.md' in err for err in errors))

    def test_bootstrap_does_not_modify_product_checkout(self):
        with tempfile.TemporaryDirectory(prefix='mp-bootstrap-product-') as tmp:
            ws = Path(tmp)
            (ws / 'project').mkdir()
            sentinel = ws / 'project' / 'existing-product.txt'
            sentinel.write_text('Keep this product file intact.\n', encoding='utf-8')
            bootstrap(ws)
            self.assertEqual(sentinel.read_text(encoding='utf-8'), 'Keep this product file intact.\n')
            self.assertFalse((ws / 'CLAUDE.local.md').exists())

    @unittest.skipUnless(shutil.which('git'), 'Git not installed')
    def test_tracked_sha256_manifest_is_complete(self):
        import hashlib
        manifest = (ROOT / 'MANIFEST_SHA256.txt').read_text(encoding='utf-8')
        lines = [line for line in manifest.splitlines() if line and not line.startswith('#')]
        recorded = {}
        for line in lines:
            digest, separator, rel = line.partition('  ')
            self.assertEqual(separator, '  ', line)
            self.assertNotIn(rel, recorded)
            recorded[rel] = digest
            self.assertEqual(hashlib.sha256((ROOT / rel).read_bytes()).hexdigest(), digest, rel)
        proc = subprocess.run(['git', '-C', str(ROOT), 'ls-files', '-z'], check=True,
                              stdout=subprocess.PIPE)
        files = {p.decode('utf-8') for p in proc.stdout.split(b'\0') if p}
        self.assertEqual(set(recorded), files - {'MANIFEST_SHA256.txt'})

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
                'CLAUDE.local.md.bak', 'CLAUDE.local.md.bak.1',
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
