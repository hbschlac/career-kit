---
name: resume
description: >
  Tailors the user's resume to a specific job and exports it as a PDF. Use when the user wants to
  tailor, edit or update their resume for a role or company, create a new resume copy for an
  application, rewrite bullets to match a job description, or export a finished resume. Runs a
  gated workflow: facts from the user's evidence ledger first, then a full swap list written in
  chat, a voice pass, a before/after ATS score, one round of targeted Google Docs edits on a copy
  of the base resume, and a PDF export. Triggers: "tailor my resume", "resume for this job",
  "update my CV", "resume skill", "export my resume".
---

# Resume — five gates, one file per gate

**Load one step at a time. Do not read the references in full up front.** Loading every
instruction before reading the job description burns context and still produces a doc edited
bullet by bullet. What a gate needs is in that gate's file. What must never be forgotten is on the
wall below. Paths are repo-relative.

**Profile preflight.** This skill reads personal data only from `profile/`: `me.md`, `resume.md`,
`evidence.md`, `voice.md`, `rules.md`, `targets.md` and `config.json` (`name`, `email`, `phone`,
`linkedin`, `website`, `cv_folder_id`, `base_cv_doc_id`, `pipeline_sheet_id`). If a file it needs
is empty or still holds template placeholders (`<…>` / `TODO`), say which one and offer to run the
`setup` skill. Never invent the missing facts.

## The wall — true at every gate

1. **A resume the user has called final is read-only.** Edit only a fresh copy made this session.
2. **Never a whole-doc or markdown import, any provider.** Copy the base doc; edit with
   find→replace only (`find_and_replace_doc` or Composio `GOOGLEDOCS_REPLACE_ALL_TEXT`). An import
   rewrites the document and destroys its native formatting.
3. **`match_case: true` on every replace.** `find_text` must match **exactly once** in the
   *latest* plaintext readback. 0 or 2+ matches → stop and re-read. Never insert or rewrite a
   paragraph to compensate; that is how the user's own edits get reverted.
4. **Read the doc before every write round.** The doc is the truth; the conversation is not.
5. **Never export a PDF into the conversation.** `bash skills/resume/scripts/cvcheck.sh <DOC_ID>`
   writes it to a file and returns only the line-fit summary.
6. **Score twice**: baseline and final. Never re-score after a rewording.
7. **Every fact traces** to `profile/evidence.md`, `profile/me.md`, `profile/resume.md`, or the
   user's words this session. Grep before asking; ask once, batched; append their answers to the
   ledger the same turn.
8. **The tagline (the line under the name) must answer "Why you?" for THIS role.** It passes all
   three or it is not done: **(a) Match**: names this JD's #1 requirement in the JD's own words;
   **(b) Metric**: carries at least one real number from the ledger (scale or total scope, e.g.
   `$40M revenue line`, `120-person org`, `2M monthly users`); **(c) Why you**: says the thing the
   user has already done that makes them the obvious match. Test: cover the page. Does this line
   alone say why *this* company should call *this* person? If it could head their resume for any
   company, rewrite. A stock line from `profile/resume.md` never passes as-is. In the swap list,
   print the tagline with `(a) … (b) … (c) …` ticked; Gate 3 re-checks it.
9. **1 page. 2 lines per bullet. 1 line for the tagline and each role descriptor. The user's
   nouns, not synonyms.** Never change fonts, sizes, spacing or margins to make content fit.
10. **Replaced text inherits the style of its first character.** A replace that starts at a bold
    label (`Skills:`) makes the whole new line bold. Start `find_text` after the label, or fix the
    run with one targeted style update. Details: `references/step4-apply.md`.
11. **Every rule in `profile/rules.md`** (naming bans, formatting conventions, tense, header and
    education line formats, section order). Read it once at Gate 1 and apply it at every gate.
    The user's rules override the generic defaults here where they conflict.

## Gate 0 — Facts → `references/step0-facts.md`
Get the JD. Parse it into requirements. `bash skills/resume/scripts/ledger_grep.sh <term> …` per
requirement. One batched question for the real gaps; append the answers. **No drafting until this
closes.**

## Gate 1 — Write → `references/step1-write.md` + `references/resume-rules.md`
Draft **all** bullets, the tagline and the skills line in the conversation as a from→to swap list.
No doc calls yet. The tagline passes rule 8, ticked in the swap list, and each role's first bullet
proves it.

## Gate 2 — Voice → `references/step2-voice.md`
One pass over the whole set. Wording only; facts are frozen.

## Gate 3 — Score → `references/step3-score.md`
`recruiter-filter`: baseline on the current doc, final on the swap list. Two runs, total.

## Gate 4 — Apply → `references/step4-apply.md`
Select and copy the base, read its plaintext, apply the swap list as **one round**, read back
once, `cvcheck.sh`, then the tracker.

## Gate 5 — Export (only when the user asks) → `references/step5-publish.md`
Cover letters: `references/cover-letter.md`.

## Why this order

Facts change everything downstream, so they come first. Line-fit changes nothing about meaning,
so it goes last and runs as a script whose output never enters the chat. The score responds to
content, not wording, so it runs after voice; scoring between rewrites measures noise. The user
reviews **one** swap list, not one preview per edit. Gates that each can send a bullet back are
how one bullet ends up with many versions.

## Connectors

- **Google Docs edit tool** (first-party `find_and_replace_doc`, or Composio
  `GOOGLEDOCS_REPLACE_ALL_TEXT`) for Gate 4. **Google Drive** for copy, search and PDF export.
- **Google Sheets** (Composio workbench) for the tracker update.
- If a connector is missing: stop, name it, tell the user "See README → Connect your tools", and
  continue with what still works (the swap list in chat for the user to paste via Docs' own
  Find and Replace).

## After the session

1. **Meter it.** Run `python3 scripts/session_meter.py` and show the user the summary. If the
   tracker is set up (`pipeline_sheet_id` in `profile/config.json`), also run
   `python3 scripts/session_meter.py --json` and, with the Pipeline workbench helpers loaded,
   `print(meter_row(<that dict>, kind="cv"))`. Counts only, never transcript text. `career-review`
   reads these rows.
2. **Capture corrections.** If the user gave meaningful corrections this session (verbs, phrasing, workflow, slop flags,
facts), suggest running `resume-learn`. It writes personal rules to `profile/rules.md`, voice
rules to `profile/voice.md` and facts to `profile/evidence.md`, never into `skills/`.
