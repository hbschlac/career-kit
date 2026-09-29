#!/usr/bin/env python3
"""Unit tests for scripts/session_meter.py — run: python3 tests/test_session_meter.py

Feeds the meter a small synthetic transcript and checks the numbers career-review relies on:
token totals deduped by requestId, the kit skills the session used, and the profile/meter.md
fallback row for copies without a tracker sheet.
"""
import importlib.util
import json
import os
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("session_meter", ROOT / "scripts" / "session_meter.py")
sm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sm)

failures = []
# The meter resolves the kit root from CLAUDE_PROJECT_DIR; run against this checkout.
os.environ.pop("CLAUDE_PROJECT_DIR", None)


def check(name, ok):
    print(("ok   " if ok else "FAIL ") + name)
    if not ok:
        failures.append(name)


def assistant(rid, usage, *tools):
    return {"type": "assistant", "requestId": rid, "message": {
        "id": rid, "model": "claude-test", "usage": usage,
        "content": [{"type": "tool_use", "name": n, "input": i} for n, i in tools]}}


U = {"input_tokens": 1000, "cache_creation_input_tokens": 2000, "cache_read_input_tokens": 3000,
     "output_tokens": 500}
lines = [
    {"type": "user", "message": {"role": "user", "content": "tailor my resume for this job"}},
    assistant("r1", U, ("Skill", {"skill": "resume"})),
    # the same API call written again for a second content block: must not double-count tokens
    assistant("r1", U, ("Read", {"file_path": str(ROOT / "skills/resume/references/step0-facts.md")})),
    assistant("r2", U, ("Bash", {"command": "bash skills/resume/scripts/ledger_grep.sh SQL"}),
              ("Skill", {"skill": "career-kit:recruiter-filter"})),
    assistant("r3", U, ("Read", {"file_path": "skills/not-a-kit-skill/SKILL.md"}),
              ("Grep", {"pattern": "x", "path": "profile/evidence.md"})),
]

with tempfile.TemporaryDirectory() as tmp:
    t = pathlib.Path(tmp, "abcdef1234567890.jsonl")
    t.write_text("\n".join(json.dumps(l) for l in lines), encoding="utf-8")
    r = sm.meter(t)
    check("tokens are deduped by requestId (3 API calls, not 4)", r["api_calls"] == 3)
    check("input processed sums uncached + cache write + cache read", r["total_input_processed"] == 18000)
    check("one real user message is counted", r["user_messages"] == 1)
    check("skills used, in first-use order", r["skills"] == ["resume", "recruiter-filter"])
    check("a path that isn't a kit skill is ignored", "not-a-kit-skill" not in r["skills"])
    check("the recruiter-filter Skill call counts as a rubric run", r["cv"]["rubric_runs"] == 1)
    check("the text summary names the skills", "skills used: resume, recruiter-filter" in sm.render(r))

    # --profile appends a counts-only row to profile/meter.md under CLAUDE_PROJECT_DIR
    proj = pathlib.Path(tmp, "copy")
    (proj / "profile").mkdir(parents=True)
    (proj / "skills" / "resume").mkdir(parents=True)
    (proj / "skills" / "recruiter-filter").mkdir(parents=True)
    os.environ["CLAUDE_PROJECT_DIR"] = str(proj)
    try:
        sm.main(["--profile", str(t)])
        sm.main(["--profile", str(t)])
    finally:
        os.environ.pop("CLAUDE_PROJECT_DIR", None)
    body = (proj / "profile" / "meter.md").read_text(encoding="utf-8")
    rows = [l for l in body.splitlines() if l.startswith("| 20")]
    check("--profile writes the header once and one row per run", body.count("| Date |") == 1 and len(rows) == 2)
    check("the row carries the session id, skills and token counts", "| abcdef12 | resume, recruiter-filter | 3 |" in rows[0]
          and "| 18 |" in rows[0])
    check("the row holds counts only, no transcript text", "tailor my resume" not in body)

print()
if failures:
    print(f"{len(failures)} FAILED: " + ", ".join(failures))
    sys.exit(1)
print("all session_meter tests passed")
