---
name: setup
description: >
  One-time onboarding for the career kit. Turns the user's resume, a short interview and a few of
  their own writing samples into the files in profile/ that every other skill reads, checks which
  connectors are available, and creates their job tracker sheet. Trigger on "set me up", "setup",
  "get started", "onboard me", "fill in my profile", "I just copied this kit", or when the
  SessionStart hook says SETUP NEEDED. Also re-run when the user says "update my profile" after a
  new job, a new resume, or a change in what they're looking for.
---

# Setup — make the kit yours

The kit is an engine; `profile/` is the fuel. Every other skill reads only `profile/` for facts
about the user, so this skill's job is to fill it with true, well-sourced facts. It takes about
15 minutes. Work through the steps in order, **one message per step**, and keep each question
batched: ask everything a step needs at once, never one question per turn.

**Never invent a fact.** If the user doesn't know a number, write the claim without it and add
`(number TBD)`. A resume built on a guessed metric is worse than one without the metric.

## Step 0 — Privacy check and tools (one message)

1. Confirm this copy of the repo is **private** (GitHub → Settings → General → Danger Zone →
   visibility). `profile/` will hold their phone number, work history and writing. If it is public,
   stop and ask them to make it private first.
2. Check your own tool list and report in a small table which of these are connected:

   | Needed for | Look for | If missing |
   |---|---|---|
   | Editing resume docs | `find_and_replace_doc` (Google Docs connector) **or** Composio `GOOGLEDOCS_REPLACE_ALL_TEXT` | Resumes can still be drafted in chat; the user pastes them into their doc |
   | Finding / copying docs, PDF export | Google Drive connector (`copy_file`, `download_file_content`) or Composio `GOOGLEDRIVE_*` | Same as above |
   | Job tracker | Composio Google Sheets (`GOOGLESHEETS_*`, `COMPOSIO_REMOTE_WORKBENCH`) | Tracker can live in `profile/pipeline.md` as a markdown table instead |
   | Checking replies from recruiters, learning voice from sent mail, follow-up context | Gmail connector (read-only is enough) | `career-review`, the outcome scan and the Gmail options in Step 4 and `networking` are skipped |
   | LinkedIn job search | `mcp__linkedin-jobs__*` (bundled in this repo, no login) | Only needs the repo attached as the session's project |

   For anything missing, point them to **README.md → Connect your tools** and continue. Only Step 5
   needs a connector; Steps 1 and 4 do more when Drive and Gmail are connected.

## Step 1 — The resume

Ask for their best current resume, in whichever form they have it:
- **A Google Doc link** (best): read it, then record its ID as `base_cv_doc_id` and its folder as
  `cv_folder_id` in `profile/config.json`. Every tailored CV will be a *copy* of this doc, so it
  keeps their formatting.
- **A PDF or Word file / pasted text**: use the text. Tell them tailoring works best from a Google
  Doc base and offer to walk them through File → Open in Google Docs to make one; fill the IDs later.

Write the full text into `profile/resume.md` under its headings, and fill `name`, `email`,
`phone`, `linkedin`, `website` in `profile/config.json` from the contact line.

**Every resume they've made, not only the latest (Google Drive connected).** Older versions often
hold facts and numbers the current one dropped. In the same message, offer: "Want me to read every
resume in your Google Drive, or only ones from a date range (say, 2021 to now)?" If yes:
1. Search Drive for docs and PDFs with "resume", "CV" or their name in the title (or the folder
   they name), limited to the range they gave, newest first.
2. Read each as plain text (Drive `read_file_content`, never `download_file_content`), one at a
   time, and turn it into ledger lines right away in Step 3's format, tagged
   `(source: <file title>, <modified date>)`. Never paste a whole document into the chat. Past 20
   files, read the 20 newest in full and list the rest by title only.
3. A version tailored to one company or role (the title or tagline usually says so) also goes into
   `profile/tailored.md`, one line each, so the resume skill can start from it later.
4. Still confirm which one is the base. Default: the newest general-purpose version.

**Work samples and projects (optional, Drive).** Ask for a folder or a few docs they're proud of:
PRDs, decks, case studies, launch memos, portfolio pieces. Skim each for facts with numbers
(scope, users, revenue, time saved) and add them to the ledger the same way. Docs they wrote
themselves also count as writing samples in Step 4.

## Step 2 — The short interview (one batched message)

Ask these together, numbered, and tell them short answers are fine:
1. Where are you right now: employed, between roles (since when), graduating? How do you want a gap described, and what should never be said about it?
2. What roles and seniority are you targeting? Industries you want, and ones you'll skip?
   How many years of relevant experience do you have, and what is the most a posting can ask for
   before you'd skip it? Any key qualifications, certifications or licenses?
3. Locations or remote, company size or stage, compensation floor, dealbreakers?
4. Five to ten dream companies, and which companies you are actively pursuing right now?
5. Your 3–5 strongest stories: the ones you'd tell in any interview. One line each.
6. Anything Claude should never claim or say about you (titles, tools, numbers)?
7. Any formatting or wording rules you already know you want (e.g. "Skills line always starts with SQL")?
8. Anyone who could refer or introduce you (name, company, how you know them)? Optional.

Write the answers to `profile/me.md` (1, 5, 6), `profile/targets.md` (2–4), `profile/rules.md`
(7) and `profile/contacts.md` (8).

## Step 3 — The evidence ledger

Seed `profile/evidence.md` from the resume: one line per claim, in the format the file shows
(`[Company] [Project] what — number — why (source: resume)`). Then list, in **one** message, every
bullet that has no number or no "why it mattered" and ask for what they remember: team size,
users, revenue, time saved, percent change, before/after. Append their answers the same turn with
`(source: user, <date>)`. It is fine to leave gaps; the resume skill will ask again when a job
needs that fact.

## Step 4 — Voice

Ask for 3–5 things they wrote themselves with no AI help: a cover letter, a cold email, a
LinkedIn post, a few Slack messages. Paste them into `profile/voice.md` under *Writing samples*,
then follow `skills/voice/references/building-a-voice-profile.md` to write the voice rules and
the banned-words list. Show them the rules and ask: "Does this sound like you? Anything off?"
Fix what they flag.

**Gmail connected? Offer to find the samples for them.** Search their sent mail (`in:sent`) for
emails they wrote to people outside their own company: networking notes, follow-ups, thank-yous,
cover emails. Newest first. Show the subject lines of up to 10 and let them pick before reading any
in full. Keep only their own words (drop quoted replies and signatures). Read-only: never draft,
send, label or delete. Docs from Step 1's work samples that they wrote themselves count too.

## Step 5 — The tracker (needs Google Sheets; otherwise use markdown)

- **With Composio Google Sheets:** create a sheet named `Pipeline` with a tab named for the
  current month (`Oct-2026` style) and the header row from `templates/pipeline.csv` (A–L), bold
  and frozen. Put its ID in `pipeline_sheet_id` and the tab in `pipeline_tab`. Then load the
  workbench helpers (`skills/networking/references/pipeline.md`) and run
  `print(status_colors("<tab>"))` once, so rows colour by Status.
- **Without it:** tell them to make one by hand (File → Import `templates/pipeline.csv` in
  Google Sheets) and paste the link, or keep the tracker as a markdown table in
  `profile/pipeline.md` with the same columns.

## Step 6 — Finish

1. Remove every `TODO(setup)` comment from the profile files you completed. The SessionStart hook
   keeps saying SETUP NEEDED until they are gone and `config.json` has a real name.
2. Replace any `<placeholder>` you couldn't fill with `TBD` so nothing looks like a real value.
3. Commit (`Fill in my profile`) and push to their private repo.
4. Close with a short "what you can do now" list, in plain words:
   - "Here's a job link, tailor my resume" → `resume`
   - "Write a note to <person> at <company>" → `networking`
   - "Score my resume against this job" → `recruiter-filter`
   - "Find me roles like X" → `job-search` / `linkedin-jobs`
   - "Does this sound like me?" → `voice`
   - "Learn from this session" after correcting a draft → `resume-learn`
   and offer to try one now with a real job posting.
