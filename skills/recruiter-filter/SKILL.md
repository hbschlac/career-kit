---
name: recruiter-filter
description: >
  Acts as the AI screening layer an Ashby / Greenhouse / Lever / Workday recruiter
  runs applicants through. Given a CV plus a job posting (link or pasted text), it returns
  a 0-100 fit score, the knockouts that would drop the application before scoring, what
  the filter and the 6-second human skim actually see, and a ranked list of fixes with the
  points each one recovers. Also runs a read-only scan of the user's own Gmail to find what
  actually happened to submitted applications and feed outcomes back into the rubric.
  Activates on "score my resume against this job", "will this pass the ATS", "rate my CV
  for this role", "what should I fix before I apply", a CV plus a job link, or "did I get
  rejected", "check my applications for outcomes", "is the score working".
---

# recruiter-filter

Screens a CV against a specific job the way the hiring stack actually screens it, then
says what to fix. Diagnosis, not rewriting — rewriting is a handoff (Step 6).

## What is actually being simulated

Get this right or the advice is wrong. **Almost nothing auto-rejects on resume content.**
In a 2026 Enhancv survey of 25 US recruiters, only 8% had configured any content-based
auto-rejection at all (small sample — directionally right, not a hard number).
Ashby's AI review deliberately emits *no numerical score* — it tags fit levels against
recruiter-defined criteria with citations. Greenhouse's AI surfaces strong candidates to
the top and removes no one. Workday/HiredScore grades A-D, but a human still decides.

So the filter is **three layers, and only the first one is a robot that says no**:

| Layer | Who/what | Kills you by |
|-------|----------|-------------|
| 1. Knockouts | Application-form rules | A wrong answer on work auth, location, years, or a required credential |
| 2. Ranking | ATS AI / recruiter search | Sorting you below the ~20 profiles a human will actually open |
| 3. The skim | A human, ~6 seconds, top third | Not making the JD's core requirement obvious on sight |

The goal is **not** "beat the bot." It is: survive Layer 1, rank in Layer 2, and win
Layer 3. Every fix this skill emits must serve one of those. Detail and sources:
`references/screening-stack.md`.

## Step 0 — Get both inputs. Do not score with one.

**Job posting.** If given a URL, the `job-fetch` skill (`skills/job-fetch/SKILL.md`) handles
it (ATS public APIs, with a Composio remote-exec fallback for a web sandbox's 403 egress
block); LinkedIn URLs go to `skills/linkedin-jobs/SKILL.md`. Note the ATS from the host — it
changes the Layer-1 advice. If given pasted text, use it as-is.

**CV.** Pasted or uploaded text wins — it is the version actually being sent. If none is
supplied, use `profile/resume.md` (the master resume) and say that's what you scored. If
that file is empty or still a template, say so and offer the `setup` skill.

Missing either one → ask for it. Never score against a remembered or assumed CV.

## Step 0.5 — List the whole board before you score

**Do this every time.** Companies post several reqs and candidates fixate on the one they
found. The ATS APIs in `job-fetch` return the full board from the same call that returns
one posting — enumerate it, and check whether a better-fitting req is open before scoring
the one the user named.

- A sibling req with a slightly different title can fit the same resume far better — a
  20+ point swing for free, purely from reading the board.
- Some roles are posted only on the company's own careers page (or another channel) and
  never on the ATS board. Check the careers page too, not just the ATS.

Report the alternatives before the scorecard. If a better-fitting req is open, say so
first — a 20-point gap is worth more than every fix in Step 5 combined.

## Step 1 — Rebuild the recruiter's criteria list

The step people skip. A recruiter configures screening criteria from the JD; reconstruct
that list before judging anything. Extract into a table:

- **Title(s)** the req is filed under, and the seniority band. **Derive the function from
  the responsibilities, never from the title.** A "Growth Engineer" req can turn out to be a
  marketing-ops role (email tooling, campaign reporting, CRM admin); scoring it as an engineering
  role would be wrong by 20+ points. Read the responsibilities first, then decide what job
  this actually is.
- **Must-haves** — everything in Requirements / Qualifications stated without a hedge,
  plus anything repeated in the summary. Years, domain, scale, tools, credentials.
- **Nice-to-haves** — "preferred," "bonus," "a plus."
- **Outcomes** — what the role is measured on ("own the roadmap for X," "grow Y," "cut
  latency," "ship the design system"). These matter more than the skills list; they are
  what evidence gets matched against.
- **Hard gates** — location/onsite days, work authorization, clearance, degree, comp band.
- **Vocabulary** — the exact nouns this company uses for the work. Copy them verbatim.

Then mark which must-haves are **load-bearing**. A req's requirement list is part real
bar, part copied-from-the-last-req padding. Load-bearing = it appears in the title, or in
the role summary, or in the first three responsibility bullets — ideally two of those.
Everything else is wishlist. Score all of them, but weight fixes toward the load-bearing
ones; a perfect score against padding wins nothing.

## Step 2 — Knockout gate (pass/fail, before scoring)

Check each hard gate against `profile/me.md` and `profile/targets.md` (work authorization,
location, comp floor). Any fail is reported **first and on its own** — a 92 that fails work
authorization is a 0, and saying "great match!" above it is malpractice. If a gate depends
on a fact the profile doesn't hold, ask.

Also screen the **application questions**, not just the resume: on Ashby and Greenhouse
the custom questions are where knockouts are actually wired, and free-text boxes ("why
this company") are increasingly LLM-read. If the posting's questions are visible, flag
the ones that gate.

Distinguish **hard** gates (authorization, clearance, licensure, physical location for
onsite roles) from **soft** ones (an "8+ years" against the user's 6, a degree
preference). Soft gates cost points in Step 3; they do not end the run.

**Check for over-qualification, not just under.** The rubric rewards seniority everywhere,
so it will happily score a candidate high on a role that would reject them for being too
expensive or too senior. Two hard gates run in this direction:

- **Comp band.** A posted maximum below the user's floor is a silent knockout — they are
  filtered before anyone reads a word. If the posting shows a range, say plainly whether
  they would take the top of it, and treat "no" as a knockout rather than a detail.
- **Years over the stated band.** "3-5 years" against the user's 12 is a flag, not a
  bonus. Note it; many companies hire over-band, but it is never free.

**Check whether the req is alive.** A high score on a dead posting is worse than useless.
Tells: posted date older than ~4 weeks, the same req reposted repeatedly, a listing open
far longer than its peers on the same board, or a company in a public freeze or recent
layoff. The ATS APIs in `job-fetch` return posting dates — use them. Report req health
next to the score. If it looks stale, say the highest-EV move is a human, not an edit.

## Step 3 — Score, 100 points

| # | Dimension | Pts | How to award |
|---|-----------|-----|--------------|
| 1 | Title & seniority match | 20 | Full if a CV title matches a title a recruiter would search for this req. Partial for adjacent-but-searchable ("Product Owner" vs "Product Manager", "Software Developer" vs "Software Engineer"). Low if the mapping needs a human to infer it. |
| 2 | Must-have coverage | 25 | Score each Step-1 must-have: **full** = present with evidence, **half** = claimed but unevidenced, **zero** = absent. Sum, normalize to 25. |
| 3 | Evidence & impact | 20 | Quantified outcomes that match the JD's *own* success metrics. Scope numbers (users, revenue, volume, team, budget, latency, uptime) beat activity verbs. Unquantified duty lists score low however senior. |
| 4 | Vocabulary alignment | 15 | The JD's exact nouns, present in context on the CV. Both the search index and the embedding match run on these. Stuffing scores zero — see Anti-patterns. |
| 5 | Recency & trajectory | 10 | Matches in the current/most recent role are worth far more than the same matches six years ago. Rising scope, no unexplained gaps. |
| 6 | Parse & skim safety | 10 | Machine-readable *and* human-skimmable: single column, real text, standard section headers, consistent dates, contact details in the body not the header image. |

**Bands**

- **85-100 — Top of stack.** Apply as-is. Spend the time on outreach instead.
- **70-84 — Makes the pile.** Two or three fixes move it to the top.
- **55-69 — Buried mid-stack.** Real work needed; the fixes below are the job.
- **Under 55 — Will not surface.** Either a structural rewrite, or the honest read is
  that this is the wrong req. Say which. A cold application at this level is a lottery
  ticket; a referral is worth more than any edit.

Show the per-dimension breakdown, not just the total — the total says how they're doing,
the breakdown says where the work is.

### Score freeze — score twice, not after every edit

**Baseline once. Final once. That is the budget.**

Re-running the rubric after every small edit produces a creeping number (each re-run nudging it up
a few points) that is mostly noise: re-reading the same bullets moves an uncalibrated rubric
several points either way. The user loses track of their own number and chases rounding
error.

Rules:

1. **Re-score only when new evidence lands on the page** — a fact the user supplied that
   wasn't there before. A re-score is a response to *content*, never to *wording*.
2. **Never re-score after a rewrite.** Rewording a bullet that already scored does not
   change the score; reporting that it does is noise dressed as progress.
3. **Hard cap: 2 re-scores after the baseline.** At the cap, say so and stop: *"Further
   scoring is below this rubric's resolution."*
4. **State the number once per report and never revise it mid-conversation.** If the
   current score is 87, it is not "about 90."
5. **When the remaining gaps are structural, say so and stop scoring.** Seniority band and
   recency cannot be edited. Points that can only be moved by a lie are not a fix list.

## Step 4 — The two things a screener actually sees

Report these verbatim before the fixes. They are more persuasive than the score.

**What the AI review cites.** For each must-have, the exact CV line the tool would cite
as evidence — or "no evidence found." Ashby-style review is citation-based; a must-have
with no citable line is functionally uncovered even if the user has done the work.

**What the 6-second skim retains.** Read only the top third of page one — headline,
current title, first two bullets. State what a recruiter walks away knowing, then say
which of the JD's must-haves that covers. If the role's core requirement is not visible
in that block, that is almost always the single highest-value fix on the page.

## Step 5 — The fix list, ranked by points recovered

The deliverable. Every fix carries: the dimension, the **exact before → after line**, the
points it recovers, and which of the three legal moves it is. Close with the projected
score: *"62 → 84 if you do the top three."* Patterns: `references/fix-playbook.md`.

**Three legal moves. Everything else is a gap, not a fix.**

1. **Surface** — the user has it; it's buried, late, or unlabeled. Move it up, name it in
   the JD's words. Highest yield, zero risk, most commonly available.
2. **Reframe** — same work, the JD's vocabulary. "Ran the help desk" →
   "owned tier-1 IT support for a 900-person hospital." The work is identical;
   the words are the ones the req was written in.
3. **Quantify** — the user knows the number and it isn't on the page. **Ask them for it.**
   Never estimate a number onto a resume. Check `profile/evidence.md` first (grep it for
   the claim; never read it whole) — if the number is logged there with a source, use it.

If a requirement can't be met by one of those three, it is a **gap**. Report it as a gap
and say whether it is survivable (most are — reqs are wishlists) or effectively
disqualifying. Do not paper over it. Fabricating experience fails the first screening call
and is the one failure mode that costs more than not applying.

Cap the list at the top 5-7. A fix list longer than the resume gets ignored.

**If the application says not to use an LLM, switch to critique-only.** Some forms say
outright that they want the candidate's own words and screen for AI-drafted text. In that
mode: proofread, flag, and point at what's missing — never hand over sentences the user
could paste. Their rough voice outperforms polished prose with those readers anyway.

**Verify every superlative before it lands.** Any "largest / first / only / biggest in X"
needs a search first, and the narrow true version beats the broad unverifiable one
("largest private round in the state that year" beats "largest raise of its kind" if only
the first is checkable). Checkable claims that are slightly wrong cost more than no claim.

**Stop optimizing before it costs voice.** Dimension 4 rewards drifting toward the JD's
language, and 15 points is not worth a resume that reads machine-tailored. Mirror the
req's nouns for the load-bearing requirements only, leave the rest in the user's words
(`profile/voice.md`), and route every rewritten line through `aislop`. Applying this skill
across twenty applications must not produce twenty near-identical resumes.

## Step 6 — Handoffs (only when asked)

- **Apply the edits** → `skills/resume/SKILL.md`. Pass it the fix list; it owns resume
  format, rules (`profile/rules.md`), and the Google Doc editing.
- **Check any rewritten line** → `skills/aislop/SKILL.md`. Resume bullets are exactly where
  AI phrasing reads as filler.
- **Log the application** → Pipeline sheet (`skills/networking/references/pipeline.md`);
  the score goes in column J (Recruiter score) as a bare number, so Step 7 can pair it with
  the outcome later. That pairing is the only route this rubric has to ever becoming
  calibrated.
- **Under 55, or a role worth extra** → `skills/project/SKILL.md` (build something for the
  team) and `skills/job-search/SKILL.md` (find better-fitting reqs at the same company).

## Step 7 — Outcome scan (separate mode; run it on its own)

Scoring is a guess until an outcome lands. This mode reads the user's own Gmail
(**read-only**, via the Gmail connector) for what actually happened to submitted
applications and turns each one into evidence about the rubric. Mechanics, query shapes,
and classification tells: `references/outcome-scan.md`. Read it before running — the
obvious design is wrong in four specific ways. No Gmail connector → say so and point to
README → "Connect your tools".

1. **Scope the search.** Company names do not appear in ATS sender addresses — most mail
   arrives from `no-reply@ashbyhq.com` or similar whatever the employer — so match on
   subject and body. Never run bare keyword searches like `subject:application`: a mailbox
   holds financial and medical mail a broad query will surface.
2. **Classify inbound messages only.** Users often forward rejections onward, so their own
   `SENT` mail sits in the same thread. And a candidate-experience survey ("Thanks for
   interviewing with X!") is not a rejection — the easiest mistake available here.
3. **Pair confirmation with decision** for days-to-decision, then read the layer:
   - **Under ~72h, no human contact** → knockout or fast skim. If this skill scored the
     application well, **the rubric was wrong** — say so, and re-examine the knockout gate.
   - **1-4 weeks, no interview** → the user made the pile and lost on rank. The fix list
     was aimed correctly; Dimensions 2, 3 and 4 are the work.
   - **After an interview** → not a resume problem. Do not open the CV. Route to interview
     prep.
   - **30+ days silent** → ghosted, or the req was never live. Feed back into Step 2.
4. **Write the outcome back** to Pipeline as an `[rf]` line in Log (D) with `log(N, ...)`
   (`skills/networking/references/pipeline.md`) — the sheet has no outcome column.

Never commit any of this — scores, tracker contents, email text — to a repo. Application
data lives in the sheet and the mailbox, not in version control (and this kit may be
public).

## What this does not see — state it, don't bury it

The score is the most quotable thing in the output and the least trustworthy. Say so in
the run; a confident number that hides its own limits is the main way this skill could do
harm.

- **It is uncalibrated.** No outcome data sits behind the rubric *yet*. A 74 is not a 74%
  chance of anything — it is ordinal, and re-reading the same bullets can move it several
  points. Lead with the **band**; use the number to rank fixes against each other, never
  as a forecast. Step 7 is the route out, and it needs roughly 15-20 scored applications
  with landed outcomes before it means anything. Until then the honest output is "not
  enough data yet," not a trend.
- **Ranking is relative; this score is absolute.** No view of applicant volume or who else
  applied. The same 74 is a reject in a 400-deep pool and an interview in a 12-deep one.
  If the user can see an applicant count, factor it into the band read.
- **The layout is invisible.** This reads text, which is what a working parser does — so a
  multi-column interleave, contact details locked in a header, and skills rendered as an
  image are exactly the failures it cannot observe. Score Dimension 6 as inference and say
  so, or ask the user to describe the file.
- **The projection is self-graded.** "74 → 87" is this skill's estimate of its own edits.
  Re-scoring after applying them proves nothing.
- **It sees one version of the resume.** Users keep a tailored copy per application, and
  numbers drift between them ("900 staff supported" in one, "900 tickets a month" in another, "$5M
  budget" vs "$5M saved"). No single document looks wrong; anyone comparing a resume to an
  email might. When a claim is load-bearing, check it against `profile/evidence.md` rather
  than trusting the copy in front of you.
- **It only sees the resume.** LinkedIn, GitHub, the portfolio, the cover letter, and
  whether a human inside will vouch for the user are all outside the frame, and any one of
  them can outweigh every point on this rubric.

## Anti-patterns — do not emit these as advice

- **Keyword stuffing or white-text keywords.** Parsers read hidden text regardless of
  color, recruiters see the wall instantly, and enterprise teams treat it as a trust flag
  and reject on sight. Terms without supporting evidence collapse at the first call.
- **"The ATS auto-rejected you."** It almost certainly did not. Repeating the debunked
  "75% of resumes are auto-rejected" line (traced to a 2012 vendor claim, never
  substantiated) sends the fix effort to the wrong layer.
- **Template panic.** Plain single-column formatting matters, but a clean CV that doesn't
  evidence the must-haves loses to a plain one that does. Dimension 6 is 10 points for a
  reason.
- **Rewriting the whole CV per application.** Tailor the headline, the top third, and the
  current-role bullets. The rest is stable.
- **Scoring generously.** An inflated score costs the user a week of silence. If it's a
  58, it's a 58.
- **Score-chasing.** Re-running the rubric after every rewrite manufactures the feeling of
  progress while the CV stands still. See Score freeze. If the last three points are
  seniority band, the answer is outreach, not another pass.

## Output shape

Fictional example:

```
VERDICT   Makes the pile (74/100, uncalibrated). Three fixes puts it top.
KNOCKOUTS Pass (hybrid Chicago ✓ · work auth ✓ · 5+ yrs ✓)
REQ       Posted 9 days ago, not reposted — live.

SCORE     Title & seniority    16/20
          Must-have coverage   17/25   ← weakest
          Evidence & impact    18/20
          Vocabulary           10/15
          Recency              8/10
          Parse & skim         5/10

SEES      Top-third skim: "Senior Software Engineer at Acme Corp, payroll platform, 40K employers."
          Covers 2 of 5 must-haves. Missing: public API ownership, 0→1.

FIX 1  (+6, must-haves · surface)  The partner API you built sits on page 2 under
       "Other projects"; it is your strongest evidence of API ownership. Move it
       into the current role's first bullet.
       before: "Other: built partner API"
       after:  "Designed and shipped Acme's public partner API (40 endpoints) — now
                used by 120 partner integrations."
FIX 2  (+4, vocabulary · reframe)  ...
FIX 3  (+3, parse · surface)  ...

PROJECTED  74 → 87
GAPS       No Kubernetes experience (survivable — 1 of 9 "preferred" bullets).
```

Adapt the shape to the case; keep the order: verdict → knockouts → req health → score →
what it sees → ranked fixes → projected → gaps. Close any run that leans on the number
with the one-line caveat: the rubric is uncalibrated and ranks fixes, it does not predict
callbacks.
