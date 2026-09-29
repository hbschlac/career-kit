# Career Kit — Claude skills for a job search

A set of [Claude Code](https://claude.com/claude-code) skills that do the heavy lifting of a job
search **in your own voice, from your own facts**:

| Say this | Skill | What you get |
|----------|-------|--------------|
| "Set me up" | `setup` | A 15-minute onboarding that builds your profile from your resume |
| "Tailor my resume for <job link>" | `resume` | A copy of your resume doc, edited for that job, still one page, formatting intact |
| "Write a note to <person> at <company>" | `networking` | Cover letters, LinkedIn DMs, cold emails, referral asks |
| "Score my resume against this job" | `recruiter-filter` | A 0–100 fit score the way an ATS + recruiter skim sees it, with ranked fixes |
| "Find roles like X" / a LinkedIn jobs link | `job-search`, `linkedin-jobs`, `job-fetch` | Open roles, full job descriptions, rows in your tracker |
| "Does this sound like me?" | `voice`, `aislop` | Drafts rewritten in your voice, AI-sounding lines flagged |
| "Help me build a project for this application" | `project` | A scoped work sample that shows the team what you'd do |
| "Learn from this session" | `resume-learn` | Your corrections saved as rules so you never repeat them |
| "Weekly review" | `career-review` | Replies and rejections from Gmail logged to your tracker |

The skills never make up facts. Everything they say about you comes from the `profile/` folder,
which you fill in once, or from what you tell Claude in the session.

---

## Get started (about 20 minutes)

### 1. Make your own private copy

Click **Use this template → Create a new repository** at the top of this page. Set it to
**Private**, because your copy will hold your resume, phone number and work history.

> Don't fork. A fork of a public repo can't be made private, and your profile would be public.

### 2. Connect your tools

The kit works with whatever you connect. With nothing connected, Claude can still draft everything
in the chat. Each connector unlocks more:

| Connector | Unlocks | How |
|-----------|---------|-----|
| **GitHub** (required) | Claude can open your copy of the kit | claude.ai/code prompts you the first time. Pick your new repo when you start a session |
| **Google Drive** + **Google Docs** | Claude reads every resume you've saved (any year you pick) and your work samples for facts, then edits a copy of your resume right in Google Docs and exports the PDF | [claude.ai/customize/connectors](https://claude.ai/customize/connectors) → connect Google Drive (and Google Docs if listed) |
| **Gmail** (read-only use) | Claude learns your voice from emails you've sent, reads the earlier thread before a follow-up, and `career-review` finds recruiter replies and rejections. It never sends | Same page → Gmail |
| **Composio** (optional, free plan) | The Google Sheets job tracker, plus a second path for Docs edits | One link, added on the same connectors page. Steps below |
| **LinkedIn jobs** | Search LinkedIn postings, pull full job descriptions | Nothing to do. It's bundled in this repo (`mcp/linkedin-jobs`) and uses LinkedIn's public job pages, no login |

**Adding Composio** (optional). There's nothing to set up on composio.dev first:

1. On [claude.ai/customize/connectors](https://claude.ai/customize/connectors), click **+**, then
   **Add custom connector**.
2. Name it `Composio` and paste this URL: `https://connect.composio.dev/mcp`. Leave
   **Advanced settings** empty and click **Add**.
3. Click **Connect**, then **Continue with Google** (or **Sign up**) in the Composio window. That
   creates your free Composio account. No credit card.
4. That's it. The first time Claude needs Google Sheets, Docs or Drive through Composio, it gives
   you a sign-in link. Click it, pick your Google account and approve.

If Claude asks before every Composio action, you can stop that on the same page: **Composio →
Tool permissions → Always allow**. On a Team or Enterprise plan, only an owner can add a custom
connector.

Connectors load when a session starts, so **start a new session after connecting one.** Claude
checks what's connected at the start of each session and tells you if something a skill needs is
missing.

### 3. Run setup

Start a session at [claude.ai/code](https://claude.ai/code) (or the Claude app) with **only your
copy of this repo** selected, and say:

> **set me up**

Claude will ask for your resume (a Google Doc link works best), a few quick questions about what
you're looking for, and 3–5 things you've written yourself so it can learn your voice. It writes
all of it into `profile/`, creates your tracker, and commits to your private repo.

### 4. Use it

Paste a job link and say "tailor my resume for this", or "score my resume against this job".
When Claude gets something wrong, correct it, then say **"learn from this"** and it won't happen
again.

---

## How it's organized

```
profile/          ← YOU. The only folder with personal data. Private to your copy.
  me.md             contact line, status, background, story bank, never-say list
  resume.md         your master resume
  evidence.md       every fact and number a resume may use, with its source
  voice.md          your writing samples + the voice rules drawn from them
  rules.md          your personal rules (grows as you correct Claude)
  targets.md        roles, industries, locations, comp, dealbreakers
  contacts.md       warm contacts for referrals (optional)
  tailored.md       every resume tailored to a job, so a similar job can start from it
  meter.md          token use per session, when there's no tracker sheet (created on first use)
  config.json       your tracker sheet ID, resume doc ID, contact details
skills/           ← the engine: generic workflows, no personal data
.claude/          ← skill links + safety hooks (see below)
mcp/linkedin-jobs ← the bundled LinkedIn jobs server
templates/        ← the tracker's header row
scripts/          ← leak check, session meter
```

**Safety hooks.** `.claude/hooks/cv_guard.py` runs on every Google Docs call and blocks the moves
that wreck a resume: a whole-document rewrite that wipes formatting, a find-and-replace that
matches the wrong text or matches twice, and editing before checking your facts. It also blocks
reading your whole tracker into the chat, which costs a lot of tokens. When it blocks something,
it says why. Hooks only load when **this repo is the only repo in the session**.

**It gets better the more you use it.** Three loops, all in your private copy. Say "learn from
this" after correcting a draft and the correction becomes a rule. Every tailored resume is logged
in `profile/tailored.md`, so the next similar job starts from the closest version instead of from
scratch. And every session records its token use and which skills it ran. The weekly
`career-review` finds the skill that costs the most, proposes a fix as a pull request you approve,
and checks the next week whether the cost came down.

**Privacy note on the line-fit check.** `cvcheck.sh` reads a resume copy through Google's
link-sharing export, so it asks you to set that copy to *Anyone with the link: Viewer*. While it is
shared, anyone with the link can see its contact line (phone, email). Turn link sharing off once the
check has passed, or use the Drive-export path in `skills/resume/references/step5-publish.md`.

**Getting kit updates.** Because your data lives only in `profile/`, you can pull improvements to
`skills/` from the original template without conflicts:
`git remote add kit <this template's URL> && git pull kit main --allow-unrelated-histories` the
first time, then `git pull kit main`.

**Sharing your improvements.** If you improve a skill in a way that would help everyone, run
`python3 scripts/leak_check.py` first. It fails if a skill file contains an email, phone number,
Google doc ID or other identifying detail. Then open a PR here.

## Tests

```bash
python3 tests/test_cv_guard.py      # the resume-safety hook
python3 scripts/leak_check.py       # no personal data outside profile/
```
