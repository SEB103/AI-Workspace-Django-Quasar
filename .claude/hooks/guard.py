#!/usr/bin/env python3
"""Claude Code PreToolUse guardrails.

Conservative heuristic guard for accidental repository crossing and destructive
Git/shell actions. NOT a sandbox or substitute for explicit user approvals.
Reads Claude Code tool-call JSON from stdin; emits PreToolUse deny JSON on match.
"""
from __future__ import annotations
import json
import os
import re
import sys
from pathlib import Path

AI_BASENAMES = {"CLAUDE.md", "AGENTS.md", "opencode.jsonc"}
AI_ROOT_DIRS = {".claude", ".codex", ".agents", ".opencode", "generated", "reference", "task-context", "generated-docs"}

# This deliberately avoids running ANY incoming shell command.
DANGEROUS_SHELL = [
    (r"\bgit\s+(?:-C\s+\S+\s+)?push\b[^\n;]*\s(?:--force(?:-with-lease)?|-f)\b", "force push requires user action"),
    (r"\bgit\s+(?:-C\s+\S+\s+)?reset\s+--hard\b", "hard reset is blocked"),
    (r"\bgit\s+(?:-C\s+\S+\s+)?clean\b[^\n;]*\s-[^\s]*f", "force git clean is blocked"),
    (r"\bgit\s+(?:-C\s+\S+\s+)?add\s+(?:-\S*\s+)*-f\b", "force git add bypasses ignore"),
    (r"\bgit\s+(?:-C\s+\S+\s+)?rm\s+[^\n;]*-r\b", "recursive git rm requires review"),
    (r"\bgit\s+(?:-C\s+\S+\s+)?(?:filter-repo|filter-branch)\b", "history rewrite blocked"),
    (r"\brm\s+-rf\b", "recursive force removal blocked"),
    (r"\bRemove-Item\b[^\n;]*(?:-Recurse\b[^\n;]*-Force\b|-Force\b[^\n;]*-Recurse\b)", "recursive force removal blocked"),
    (r"\bgh\s+repo\s+delete\b", "GitHub repo deletion blocked"),
    (r"\bgh\s+release\s+delete\b", "GitHub release deletion blocked"),
]


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


def decide(tool_name: str, tool_input: dict, workspace_root: Path) -> str | None:
    name = tool_name.lower()
    if name in {"write", "edit", "multiedit", "notebookedit"}:
        paths = [tool_input.get(k, '') for k in ('file_path', 'path', 'notebook_path')]
        for p in paths:
            if isinstance(p, str) and product_ai_path(p, workspace_root):
                return f"AI-only path is forbidden inside Product repository: {p}"
    if name in {"bash", "powershell"}:
        cmd = str(tool_input.get('command', ''))
        for pattern, reason in DANGEROUS_SHELL:
            if re.search(pattern, cmd, flags=re.IGNORECASE):
                return reason
        # Prevent accidental explicit copying of workspace AI state into product.
        if re.search(r"(?:\bcp\b|\bCopy-Item\b|\bmv\b|\bMove-Item\b).*?(?:\.claude|CLAUDE\.md|task-context|generated-docs|generated|reference).*?\bproject[/\\]",cmd,re.I):
            return "copying AI workspace internals into Product repository is blocked"
    return None


def main():
    try:
        event=json.load(sys.stdin)
        tool=event.get('tool_name','')
        inp=event.get('tool_input') or {}
        root=Path(os.environ.get('CLAUDE_PROJECT_DIR', Path(__file__).resolve().parents[2]))
        reason=decide(str(tool), inp if isinstance(inp,dict) else {}, root)
        if reason:
            print(json.dumps({'hookSpecificOutput':{
                'hookEventName':'PreToolUse',
                'permissionDecision':'deny',
                'permissionDecisionReason':reason
            }}))
            return 0
        return 0
    except Exception as e:
        # Fail closed if the hook is invoked but its expected data is broken;
        # avoid uncaught exceptions because they could be treated as no decision.
        print(json.dumps({'hookSpecificOutput':{
            'hookEventName':'PreToolUse',
            'permissionDecision':'deny',
            'permissionDecisionReason':'Workspace guard failed to validate action: '+type(e).__name__
        }}))
        return 0


if __name__=='__main__':
    sys.exit(main())
