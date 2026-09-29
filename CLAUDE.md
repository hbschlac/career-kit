# Career Kit: instructions for Claude

This repo is one person's job-search toolkit, copied from a public template. **The user is
whoever owns this copy.** Everything you know about them is in `profile/`. The skills in
`skills/` are generic workflows that read from it.

## First thing, every session

1. **Is the profile set up?** The SessionStart hook says `SETUP NEEDED` if not. If so, say so in
   your first reply and offer to run `skills/setup/SKILL.md` before anything else. Don't draft a
   resume or message from guessed facts.
2. **Which connectors are here?** Check your tool list against the table below before the first
   task that needs one. If one is missing, tell the user in 2–3 lines: which connector, what it
   unlocks, and that they add it at <https://claude.ai/customize/connectors> and then start a
   new session (connectors load at session start). The full walkthrough is in README.md →
   *Connect your tools*. Then carry on with whatever works without it. Drafting in chat always works.

| Connector | Tools you'd see | Needed by |
|-----------|-----------------|-----------|
| Google Docs / Drive | `find_and_replace_doc`, `copy_file`, `download_file_content`, or Composio `GOOGLEDOCS_*` / `GOOGLEDRIVE_*` | `resume` Gates 4–5, `setup` step 1 (every resume in Drive, work samples) |
| Google Sheets (via Composio) | `COMPOSIO_REMOTE_WORKBENCH`, `GOOGLESHEETS_*` | the tracker (`networking/references/pipeline.md`), `career-review` |
| Gmail | `search_threads`, `get_thread` | `career-review`, `recruiter-filter` outcome scan, `setup` step 4 voice samples, `networking` follow-ups (read-only, never send) |
| LinkedIn jobs (bundled) | `mcp__linkedin-jobs__*` | `linkedin-jobs`. Loads from `.mcp.json` when this repo is the project |

## Trigger phrases → skill

| When the user says… | Load |
|---------------------|------|
| "set me up", "get started", "fill in my profile", "update my profile" | `skills/setup/SKILL.md` |
| "tailor / update my resume", a job link plus "resume", "cover letter", "use the resume I made for <company>" | `skills/resume/SKILL.md` |
| "write a note / DM / cold email / intro request / referral ask", "follow up with", "reply to", "networking" | `skills/networking/SKILL.md` |
| "job tracker", "pipeline", "log that I applied", "what's in my pipeline" | `skills/networking/references/pipeline.md` |
| "score my resume against this job", "will this pass the ATS", "did I get rejected" | `skills/recruiter-filter/SKILL.md` |
| "find roles", "who's hiring", "Boolean search", "companies that just raised" | `skills/job-search/SKILL.md` |
| a linkedin.com/jobs URL, "search LinkedIn jobs" | `skills/linkedin-jobs/SKILL.md` |
| any other job-posting URL, "fetch this JD" | `skills/job-fetch/SKILL.md` |
| "does this sound like me", "voice check", "write this in my voice" | `skills/voice/SKILL.md` |
| "slop check", "does this sound like AI" | `skills/aislop/SKILL.md` |
| "what should I build for this application" | `skills/project/SKILL.md` |
| "learn from this", "resume learn" | `skills/resume-learn/SKILL.md` |
| "weekly review", "check my outcomes", "did anyone reply" | `skills/career-review/SKILL.md` |

## End of every session that used a kit skill

1. **Meter it.** Run `python3 scripts/session_meter.py` and show the user the summary: tokens, the
   skills used, anything over a threshold. Then save the counts so `career-review` can track cost
   per skill over time. With the tracker set up (`pipeline_sheet_id` in `profile/config.json`):
   `python3 scripts/session_meter.py --json`, then with the Pipeline helpers loaded
   `print(meter_row(<that dict>))`. Without it: `python3 scripts/session_meter.py --profile`, which
   appends the row to `profile/meter.md`; commit it with the session's other profile changes.
   Counts only, never transcript text.
2. **Corrections?** If the user corrected the same kind of thing more than once, offer
   `resume-learn` so it becomes a rule.

## Rules that hold everywhere

- **Facts come from `profile/` or the user's own words this session. Nothing else.** Grep before
  asking (`bash skills/resume/scripts/ledger_grep.sh <term> …`), ask once with all the gaps
  batched, and append the answers to `profile/evidence.md` the same turn.
- **Grep profile files, don't read them whole.** `evidence.md` grows long.
- **Personal learnings go to `profile/`** (`rules.md`, `voice.md`, `evidence.md`), never into
  `skills/`. That keeps `skills/` generic, so the user can pull kit updates without conflicts.
- **Never a whole-doc or markdown import into a Google Doc.** Copy the base doc, then edit with
  one find→replace per change, `match_case: true`. `cv_guard.py` enforces this.
- **Keep `profile/` out of anything public.** If the user wants to contribute a skill improvement
  back to the template, run `python3 scripts/leak_check.py` and fix every finding first.
- Hooks load only when this repo is the session's **only** repo. If `tail ~/.claude/cv-guard/guard.log`
  shows no `HOOKS career-kit` line for today, they're off: follow the rules by hand and say so.
