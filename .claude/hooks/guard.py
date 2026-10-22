#!/usr/bin/env python3
"""Claude Code PreToolUse guardrails.

Conservative heuristic guard for accidental repository crossing and destructive
Git/shell actions. NOT a sandbox or substitute for explicit user approvals.
Reads Claude Code tool-call JSON from stdin; emits a PreToolUse decision JSON:
"deny" for blocked actions, "ask" for actions that need explicit user approval.
"""
from __future__ import annotations
import json
import os
import re
import sys
from pathlib import Path

AI_BASENAMES = {"CLAUDE.md", "AGENTS.md", "opencode.jsonc"}
AI_ROOT_DIRS = {".claude", ".codex", ".agents", ".opencode", "generated", "reference", "task-context", "generated-docs"}
PROTECTED_BRANCHES = {"master", "main"}

_GIT = r"\bgit\s+(?:-C\s+\S+\s+)?"
_SEG = r"[^\n;|&]*"  # rest of the current shell command segment
_I = re.IGNORECASE

# This deliberately avoids running ANY incoming shell command.
DENY_SHELL = [
    (re.compile(_GIT + r"push\b" + _SEG + r"\s(?:--force(?:-with-lease)?|-f)\b", _I), "force push requires user action"),
    (re.compile(_GIT + r"push\b" + _SEG + r"\s\+\S", _I), "force push (+refspec) requires user action"),
    (re.compile(_GIT + r"reset\s+--hard\b", _I), "hard reset is blocked"),
    (re.compile(_GIT + r"clean\b" + _SEG + r"\s-[^\s]*f", _I), "force git clean is blocked"),
    (re.compile(_GIT + r"add\s+(?:-\S*\s+)*-f\b", _I), "force git add bypasses ignore"),
    (re.compile(_GIT + r"rm\s+" + _SEG + r"-r\b", _I), "recursive git rm requires review"),
    (re.compile(_GIT + r"(?:filter-repo|filter-branch)\b", _I), "history rewrite blocked"),
    (re.compile(r"\brm\b(?=" + _SEG + r"\s-(?:[a-z]*r|-recursive\b))(?=" + _SEG + r"\s-(?:[a-z]*f|-force\b))", _I),
     "recursive force removal blocked"),
    (re.compile(r"\bRemove-Item\b" + _SEG + r"(?:-Recurse\b" + _SEG + r"-Force\b|-Force\b" + _SEG + r"-Recurse\b)", _I),
     "recursive force removal blocked"),
    (re.compile(r"\bgh\s+repo\s+delete\b", _I), "GitHub repo deletion blocked"),
    (re.compile(r"\bgh\s+release\s+delete\b", _I), "GitHub release deletion blocked"),
]

ASK_SHELL = [
    (re.compile(r"\bgh\s+pr\s+merge\b", _I), "PR merge needs explicit user approval"),
    (re.compile(r"\bgh\s+release\s+create\b", _I), "GitHub release needs explicit user approval"),
    (re.compile(_GIT + r"push\b" + _SEG + r"\s(?:\S*:)?(?:refs/heads/)?(?:master|main)\b(?![-/\w])", _I),
     "push to protected branch needs explicit user approval"),
    (re.compile(_GIT + r"push\b" + _SEG + r"\s(?:--tags\b|--follow-tags\b|refs/tags/|v\d+\.\d+)", _I),
     "tag push needs explicit user approval"),
    (re.compile(_GIT + r"push\b" + _SEG + r"\s(?:--delete\b|-d\b|:\S)", _I), "remote branch deletion needs explicit user approval"),
    (re.compile(_GIT + r"branch\b" + _SEG + r"\s(?:-D\b|--delete\b" + _SEG + r"--force\b|--force\b" + _SEG + r"--delete\b)"),
     "force branch deletion needs explicit user approval"),
    (re.compile(_GIT + r"restore\b(?!" + _SEG + r"--staged\b)", _I), "discarding working-tree changes needs explicit user approval"),
    (re.compile(_GIT + r"checkout\b" + _SEG + r"\s(?:--|\.)(?=\s|$)", _I),
     "discarding working-tree changes needs explicit user approval"),
]

_PUSH = re.compile(r"\bgit\s+(?:-C\s+(\S+)\s+)?push\b(" + _SEG + r")", _I)
# Push options whose value is a separate token.
_PUSH_VALUE_OPTS = {"-o", "--push-option", "--repo", "--receive-pack", "--exec"}


def _normalized_path(value: str) -> str:
    return value.strip().strip('"\'').replace('\\', '/').replace('//', '/')


def product_ai_path(value: str, workspace_root: Path) -> bool:
    """Checks obvious direct writes to AI-only paths within Product.

    Supports relative paths and absolute workspace-root paths. This is a
    heuristic defense in depth: alternative shell spellings can bypass it.
    """
    raw = _normalized_path(value)
    if not raw:
        return False
    norm = raw.lower().removeprefix('./')
    root = workspace_root.resolve().as_posix().lower().rstrip('/') + '/'
    if norm.startswith(root):
        norm = norm[len(root):]
    # Do not match an unrelated external directory with 'project' in its name.
    if not norm.startswith('project/'):
        return False
    part = norm[len('project/'):].split('/')
    if not part or not part[0]:
        return False
    return part[0] in AI_ROOT_DIRS or part[0].lower() in {x.lower() for x in AI_BASENAMES}


def current_branch(repo_dir: Path) -> str | None:
    """Read the checked-out branch from .git/HEAD without running Git."""
    try:
        for folder in (repo_dir, *repo_dir.parents):
            dot_git = folder / '.git'
            if dot_git.is_file():  # worktree: "gitdir: <path>"
                text = dot_git.read_text(encoding='utf-8').strip()
                if not text.startswith('gitdir:'):
                    return None
                dot_git = (folder / text[len('gitdir:'):].strip()).resolve()
            if dot_git.is_dir():
                head = (dot_git / 'HEAD').read_text(encoding='utf-8').strip()
                return head.removeprefix('ref: refs/heads/') if head.startswith('ref: refs/heads/') else None
    except OSError:
        return None
    return None


def bare_push_on_protected_branch(cmd: str, cwd: Path) -> bool:
    """True for `git push [remote]` (no refspec) while master/main is checked out."""
    for match in _PUSH.finditer(cmd):
        tokens = match.group(2).split()
        positional, skip = [], False
        for token in tokens:
            if skip:
                skip = False
            elif token in _PUSH_VALUE_OPTS:
                skip = True
            elif not token.startswith('-'):
                positional.append(token)
        if len(positional) > 1:
            continue  # explicit refspec: handled by ASK_SHELL patterns
        target = Path(_normalized_path(match.group(1))) if match.group(1) else Path('.')
        repo_dir = target if target.is_absolute() else cwd / target
        if current_branch(repo_dir) in PROTECTED_BRANCHES:
            return True
    return False


def decide(tool_name: str, tool_input: dict, workspace_root: Path,
           cwd: Path | None = None) -> tuple[str, str] | None:
    """Return ("deny" | "ask", reason) for a guarded action, else None."""
    name = tool_name.lower()
    if name in {"write", "edit", "multiedit", "notebookedit"}:
        paths = [tool_input.get(k, '') for k in ('file_path', 'path', 'notebook_path')]
        for p in paths:
            if isinstance(p, str) and product_ai_path(p, workspace_root):
                return "deny", f"AI-only path is forbidden inside Product repository: {p}"
    if name in {"bash", "powershell"}:
        cmd = str(tool_input.get('command', ''))
        for pattern, reason in DENY_SHELL:
            if pattern.search(cmd):
                return "deny", reason
        # Prevent accidental explicit copying of workspace AI state into product.
        if re.search(r"(?:\bcp\b|\bCopy-Item\b|\bmv\b|\bMove-Item\b).*?(?:\.claude|CLAUDE\.md|task-context|generated-docs|generated|reference).*?\bproject[/\\]",cmd,re.I):
            return "deny", "copying AI workspace internals into Product repository is blocked"
        for pattern, reason in ASK_SHELL:
            if pattern.search(cmd):
                return "ask", reason
        if bare_push_on_protected_branch(cmd, cwd or workspace_root):
            return "ask", "push from protected branch needs explicit user approval"
    return None


def _emit(decision: str, reason: str) -> None:
    print(json.dumps({'hookSpecificOutput': {
        'hookEventName': 'PreToolUse',
        'permissionDecision': decision,
        'permissionDecisionReason': reason,
    }}))


def main():
    try:
        event=json.load(sys.stdin)
        tool=event.get('tool_name','')
        inp=event.get('tool_input') or {}
        root=Path(os.environ.get('CLAUDE_PROJECT_DIR', Path(__file__).resolve().parents[2]))
        cwd=Path(event['cwd']) if event.get('cwd') else root
        result=decide(str(tool), inp if isinstance(inp,dict) else {}, root, cwd)
        if result:
            _emit(*result)
        return 0
    except Exception as e:
        # Fail closed if the hook is invoked but its expected data is broken;
        # avoid uncaught exceptions because they could be treated as no decision.
        _emit('deny', 'Workspace guard failed to validate action: '+type(e).__name__)
        return 0


if __name__=='__main__':
    sys.exit(main())
