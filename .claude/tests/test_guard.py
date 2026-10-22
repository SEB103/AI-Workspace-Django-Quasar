import sys
import tempfile
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'.claude/hooks'))
from guard import decide, product_ai_path, current_branch


def _decision(cmd, cwd=None):
    result=decide('Bash',{'command':cmd},ROOT,cwd)
    return result[0] if result else None


def _fake_repo(base: Path, branch: str) -> Path:
    (base/'.git').mkdir(parents=True)
    (base/'.git'/'HEAD').write_text(f'ref: refs/heads/{branch}\n',encoding='utf-8')
    return base


class GuardTests(unittest.TestCase):
    def test_forbid_ai_code_direct_file(self):
        self.assertEqual(decide('Write',{'file_path':'project/CLAUDE.md'},ROOT)[0],'deny')
        self.assertEqual(decide('Edit',{'file_path':'project/.claude/rules/foo.md'},ROOT)[0],'deny')
        self.assertEqual(decide('Write',{'file_path':str(ROOT/'project/AGENTS.md')},ROOT)[0],'deny')
    def test_allow_product_files_and_workspace_rules(self):
        self.assertIsNone(decide('Write',{'file_path':'project/backend/foo.py'},ROOT))
        self.assertIsNone(decide('Write',{'file_path':'.claude/rules/10-repository-boundaries.md'},ROOT))
    def test_destructive_commands_denied(self):
        for cmd in ['git -C project reset --hard HEAD','git push --force origin main','git push -f origin x',
                    'git push origin +feature','git -C project add -f .env','gh repo delete x/y','git clean -fdx',
                    'rm -rf build','rm -fr build','rm -r -f build','rm -Rf build','rm --recursive --force build',
                    'Remove-Item -Recurse -Force build']:
            with self.subTest(cmd=cmd):self.assertEqual(_decision(cmd),'deny')
    def test_approval_required_commands_ask(self):
        for cmd in ['gh pr merge 2 --repo x/y','gh release create v1.0.0','git push origin master',
                    'git -C project push origin main','git push origin HEAD:master','git push origin refs/heads/main',
                    'git push --tags','git push origin v1.2.3','git push origin --delete feature','git push origin :feature',
                    'git branch -D feature','git restore .','git -C project restore src/a.ts',
                    'git checkout -- .','git checkout .']:
            with self.subTest(cmd=cmd):self.assertEqual(_decision(cmd),'ask')
    def test_normal_commands_allowed(self):
        for cmd in ['git -C project status','git -C . diff --cached','python -m pytest','git push origin feature',
                    'git push -u origin fix/master-docs','git push origin master-notes','git branch -d merged',
                    'git restore --staged file.py','git checkout -b feature/x','git switch master',
                    'rm -f stale.tmp','rm -r emptydir','gh pr create --base master --head feature',
                    'gh pr checks 2 --repo x/y']:
            with self.subTest(cmd=cmd):self.assertIsNone(_decision(cmd))
    def test_bare_push_checks_checked_out_branch(self):
        with tempfile.TemporaryDirectory(prefix='mp-guard-') as tmp:
            on_master=_fake_repo(Path(tmp)/'ws',"master")
            on_feature=_fake_repo(Path(tmp)/'feat',"feature/x")
            self.assertEqual(current_branch(on_master/'sub'),'master')
            for cmd in ['git push','git push origin','git push -u origin','git push -o ci.skip origin']:
                with self.subTest(cmd=cmd):
                    self.assertEqual(_decision(cmd,on_master),'ask')
                    self.assertIsNone(_decision(cmd,on_feature))
            self.assertEqual(_decision('git -C ws push',Path(tmp)),'ask')
            self.assertIsNone(_decision('git -C feat push',Path(tmp)))
    def test_no_false_project_match(self):
        self.assertFalse(product_ai_path('other/project/CLAUDE.md',ROOT))
        self.assertTrue(product_ai_path('project/.codex/x',ROOT))

if __name__=='__main__':unittest.main()
