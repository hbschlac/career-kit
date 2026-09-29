---
name: networking
description: >
  Outreach and networking skill, and the front door to the career kit. Use whenever the user wants
  to reach out to a professional contact: a hiring manager, a leader at a target company, a
  recruiter, a fellow alum, someone they found on LinkedIn, or a mutual who could introduce them.
  Drafts cover letters, LinkedIn DMs and connection notes, cold emails, intro requests,
  third-person referral blurbs, and follow-ups or replies ("follow up with", "reply to",
  "bump"). Routes resume tailoring to the resume skill, finding roles and people to the job-search
  skill, and tracker updates ("job tracker", "update my tracker",
  "what's in my pipeline", "log that I applied", "mark CV done for X") to references/pipeline.md.
---

# Networking Skill

This skill helps the user reach out to professional contacts with messages that sound like
*them*: specific, brief, direct, and centered on what the reader is building. It is also the front
door of the kit. When the request is really about something else, hand it to the right skill.

## Routing

| The user wants to… | Go to |
|---|---|
| Tailor, edit or build a resume / CV for a role | `skills/resume/SKILL.md` (it loads one gate at a time; do not pre-read the resume or evidence files here) |
| Find roles, companies, hiring managers, Boolean searches | `skills/job-search/SKILL.md`, then come back here to draft outreach for the results |
| Build a targeted project for an application | `skills/project/SKILL.md` |
| Check or update the application tracker | `references/pipeline.md` and its workbench helpers |
| Pull a JD from an Ashby link (`jobs.ashbyhq.com/...`) | `references/ashby-jobs.md` first; other job boards go to `skills/job-fetch/SKILL.md` |
| Score a CV against a job | `skills/recruiter-filter/SKILL.md` |
| Write a cover letter | `skills/resume/references/cover-letter.md` (the single source for length and structure) |
| Make a draft sound like them / strip AI slop | `skills/voice/SKILL.md`, `skills/aislop/SKILL.md` |

## Before you draft

Read what the task needs, not everything:

- **Who the user is:** `profile/me.md` (background, strengths, story bank, things never to say).
  For a specific claim or metric, grep `profile/evidence.md` for it. Never read the ledger whole,
  and never state a number that is not in it.
- **How they write:** `profile/voice.md` via the voice skill.
- **Their own rules:** `profile/rules.md` (naming, phrasing they have banned, sign-off preferences).
- **Warm paths:** `profile/contacts.md` if it exists.
- **Message craft:** `references/outreach-playbook.md` (structures per format, hard rules).
- **Framing gate:** `references/signal-in-the-noise.md`. Every draft runs its final gate.

If `profile/me.md` or `profile/voice.md` is empty or still has template placeholders (`<...>` or
`TODO`), say so and offer to run the `setup` skill. Do not invent facts about the user to fill the
gap.

**Check for an existing tailored draft before writing from scratch.** The user may have drafted a
cover letter or message for this company in an earlier session. Check, in order:

1. **The role's tracker row:** `find(["<Company>"])`, then `row(N)`. CV links sit in F to I; the
   Log (D) and Notes (E) often name a cover-letter doc.
2. **Google Drive:** search for documents whose name contains the company.
3. **Local files** the user points you to (downloads folder, a drafts folder).

## Tracker first when working across sessions

Users often run several sessions in parallel on different applications. Before starting work on
an application, `find()` the role in the tracker so you do not duplicate another session's work.
When you finish a real milestone (CV built, message sent, application submitted), add or update the
row and leave a dated Log line. Full rules in `references/pipeline.md`. If the Google Sheets
connector (Composio) is not present, say so, point to README "Connect your tools", and continue
with the draft.

---

## What the user will give you

Some or all of:
- **Who the person is:** name, role, company, what they do
- **How the user found them:** cold on LinkedIn, mutual connection, job posting, event, something
  they wrote
- **What the user wants:** informational chat, a warm path into an application, an intro,
  a referral, staying on their radar
- **Anything specific:** a shared school or employer, something they published, a product the user
  actually uses

Work with what you have. If something load-bearing is missing (the ask, or who the reader is), ask
before drafting.

**Follow-ups and replies: read the thread first (Gmail connected).** When the message continues a
conversation (a bump, a thank-you after a call, a reply, a second referral nudge), search the
user's mailbox for the person's name or email address, newest first, and read that one thread as
plain text. Then match it: don't repeat the intro, answer what they asked, pick up what they said,
and keep the tone the user already used with them. Read-only: never draft, send or label in
Gmail. The message comes back to the chat for the user to send. No Gmail connector → ask the user
to paste the last message.

---

## Your job

### Step 1: Pick the frame

**Which part of the user's story matters to this reader?** Look at the reader's company and the
opportunity. Pick the one angle from `profile/me.md` (story bank) that answers "why this person
for what you are building". Different audiences get different angles; do not summarize the resume.

**Ladder to the opportunity, not to the recipient's own job.** When the user is reaching out about
open roles at a company in general, the recipient's background explains *why them* (alum, works
there), but the pitch should ladder to the role being pursued. Mirroring the recipient's own job
description when the ask is broader shows you did not think about the actual opportunity.

**Which format?**
- LinkedIn connection note: 300 characters, hard cap
- LinkedIn DM: short
- Email: 3 short paragraphs max, readable on a phone, ask first
- Cover letter: follow `skills/resume/references/cover-letter.md` (length, structure, checklist)
- Intro request: ask in the first line, brief
- Referral blurb: third person, meant to be forwarded

If the user does not specify, choose from context and say which you chose.

### Step 2: Apply the hard rules

From `references/outreach-playbook.md`, plus anything in `profile/rules.md` (the user's rules win
where they conflict):

- **Lead with the ask** in emails and DMs (cover letters are the exception)
- **3 paragraphs max** for emails; fits one phone screen
- **No "pick your brain"** and no "compare notes"
- **No jargon**; plain language
- **No generic openers**; nothing that could be pasted to anyone
- **Never presume the recipient's situation.** No "right in your wheelhouse", "just like what
  you're doing", or any line that asserts their day-to-day. State the user's facts and what the
  company has said publicly; let the reader draw the connection.
- **No invented facts.** Every credential and number comes from `profile/evidence.md` or
  `profile/me.md`.

### Step 3: Draft

**Opener** (where you are not leading with the ask): a specific, true hook. Something the user
actually noticed, a shared connection, a real reason they are writing now. The smaller true reason
beats a bigger manufactured one.

**Lead with proof when it exists.** If the user has built something that maps to the role (a
portfolio piece, a `project`-skill build), the link goes in the first lines, not a P.S. Check that
the link is live.

**The bridge:** *what you are building (from public facts) → the user's specific experience that
helps you get there.* One story element, connected directly to their world.

**The ask:** light and low-pressure. A short chat, staying in touch, or a genuine question. No
referral request in a first message to a stranger. When in doubt, end with a question.

**Sign-off:** match the user's recorded sign-off for this context in `profile/voice.md`. If none
is recorded, ask once which sign-off they use, then offer to save it to `profile/voice.md`.

### Step 4: Present and explain

Run the final gate in `references/signal-in-the-noise.md` and fix what fails. Then show:
- the draft, with a one-line signal check
- which story angle you led with and why (1 sentence)
- what you framed as the ask (1 sentence)

Ask whether it sounds like them. Be ready to change the hook, tighten length, or shift the angle.
For anything longer than a DM, run `skills/voice/SKILL.md` and `skills/aislop/SKILL.md` before
showing it.

---

## The core principle

The best outreach does not just say who the user is. It makes clear why the user and this reader
are working on the same problem. Find that overlap and make it specific, not manufactured. If the
draft is polished but could go to anyone, it is wrong. Start over.

---

## Resume work

Hand off to `skills/resume/SKILL.md`. It owns tailoring, the Google Doc edit rules, and the fact
gates. The short version of its editing rule, because it matters everywhere: edit resume docs only
with targeted find-and-replace (first-party Google Docs `find_and_replace_doc`, or Composio
`GOOGLEDOCS_REPLACE_ALL_TEXT` with `match_case: true`), always on a copy of the base doc. Never
use a whole-document or markdown import; it destroys the resume's formatting.
