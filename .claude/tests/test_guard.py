import sys
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'.claude/hooks'))
from guard import decide, product_ai_path

class GuardTests(unittest.TestCase):
    def test_forbid_ai_code_direct_file(self):
        self.assertIsNotNone(decide('Write',{'file_path':'project/CLAUDE.md'},ROOT))
        self.assertIsNotNone(decide('Edit',{'file_path':'project/.claude/rules/foo.md'},ROOT))
        self.assertIsNotNone(decide('Write',{'file_path':str(ROOT/'project/AGENTS.md')},ROOT))
    def test_allow_product_files_and_workspace_rules(self):
        self.assertIsNone(decide('Write',{'file_path':'project/backend/foo.py'},ROOT))
        self.assertIsNone(decide('Write',{'file_path':'.claude/rules/10-repository-boundaries.md'},ROOT))
    def test_destructive_git_denied(self):
        for cmd in ['git -C project reset --hard HEAD','git push --force origin main','git -C project add -f .env','gh repo delete x/y','git clean -fdx']:
            with self.subTest(cmd=cmd):self.assertIsNotNone(decide('Bash',{'command':cmd},ROOT))
    def test_normal_git_read_allowed(self):
        for cmd in ['git -C project status','git -C . diff --cached','python -m pytest','git push origin feature']:
            with self.subTest(cmd=cmd):self.assertIsNone(decide('Bash',{'command':cmd},ROOT))
    def test_no_false_project_match(self):
        self.assertFalse(product_ai_path('other/project/CLAUDE.md',ROOT))
        self.assertTrue(product_ai_path('project/.codex/x',ROOT))

if __name__=='__main__':unittest.main()
