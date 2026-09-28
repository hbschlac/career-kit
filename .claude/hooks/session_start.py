#!/usr/bin/env python3
"""SessionStart: tell Claude whether the profile is set up and which tools the kit expects, and
leave proof the project hooks loaded (~/.claude/cv-guard/guard.log gets a HOOKS line).
Kept short on purpose: this text is paid for in every session. Fails silent."""
import json, os, pathlib, sys, time

ROOT = pathlib.Path(os.environ.get("CLAUDE_PROJECT_DIR") or pathlib.Path(__file__).resolve().parents[2])
PROFILE_FILES = ["me.md", "resume.md", "evidence.md", "voice.md", "targets.md"]

RULES = (
    "career-kit hooks are live (cv_guard refuses rule-breaking doc/sheet calls and names the rule).\n"
    "- Personal facts live ONLY in profile/. Never invent a fact; grep profile/ first "
    "(`bash skills/resume/scripts/ledger_grep.sh <term>`), then ask the user once, batched.\n"
    "- CV work: follow skills/resume/SKILL.md one gate at a time; never pull a PDF into the chat "
    "(`bash skills/resume/scripts/cvcheck.sh <DOC_ID>`).\n"
    "- Tracker sheet: never read a whole tab; use skills/networking/scripts/pipeline_workbench.py."
)

CONNECTORS = (
    "Before the first task that needs one, check your tool list for: Google Docs editing "
    "(find_and_replace_doc, or Composio GOOGLEDOCS_REPLACE_ALL_TEXT), Google Drive, Google Sheets "
    "(Composio GOOGLESHEETS_* / COMPOSIO_REMOTE_WORKBENCH), and Gmail. If one is missing, name it and "
    "point the user to README.md -> 'Connect your tools' (claude.ai -> Settings -> Connectors), then "
    "carry on with what works (drafting in chat needs no connector)."
)


def profile_state():
    """'missing', 'template' (placeholders left) or 'ready'."""
    try:
        cfg = json.loads((ROOT / "profile" / "config.json").read_text(encoding="utf-8"))
    except Exception:
        return "missing"
    if not cfg.get("name") or str(cfg.get("name")).startswith("<"):
        return "template"
    for f in PROFILE_FILES:
        p = ROOT / "profile" / f
        if not p.exists() or "TODO(setup)" in p.read_text(encoding="utf-8", errors="ignore"):
            return "template"
    return "ready"


def main():
    try:
        d = pathlib.Path(os.environ.get("CV_GUARD_DIR") or os.path.expanduser("~/.claude/cv-guard"))
        d.mkdir(parents=True, exist_ok=True)
        with (d / "guard.log").open("a", encoding="utf-8") as fh:
            fh.write(time.strftime("%Y-%m-%dT%H:%M:%S ") + "HOOKS career-kit SessionStart\n")
    except Exception:
        pass
    state = profile_state()
    msg = RULES + "\n" + CONNECTORS
    if state != "ready":
        msg = ("SETUP NEEDED: profile/ is not filled in yet. In your first reply, tell the user the kit "
               "needs a one-time setup (~15 min) and offer to run the `setup` skill "
               "(skills/setup/SKILL.md). Until it has run, do not draft resumes or outreach from "
               "guessed facts.\n\n") + msg
    json.dump({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": msg}}, sys.stdout)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
