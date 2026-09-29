---
name: resume-learn
description: >
  Learns from a hands-on resume or outreach editing session so the user never has to give the same
  feedback twice. Captures the user's corrections (verbs, phrasing, naming, formatting, facts,
  workflow) and writes each one into the right profile file: personal rules to profile/rules.md,
  voice rules to profile/voice.md, facts to profile/evidence.md. Never edits skills/ directly;
  a genuinely generic improvement is proposed as a pull request instead. Triggers: "resume learn",
  "learn from this session", "learn from this", "remember these corrections", "update my rules".
---

# Resume Learn

Turns friction from the current session into permanent rules. If the user had to correct the same
thing twice, it belongs in a profile file after this skill runs.

## Where learnings go: profile/, not skills/

`skills/` is the shared engine; the user pulls kit updates into it. `profile/` is theirs. Writing
personal learnings into `skills/` would cause merge conflicts on every kit update and would leak
their preferences into a shared file. So:

| Learning type | File |
|---|---|
| A personal resume/outreach rule: a naming ban ("never call it X"), a formatting convention, section order, skills-line order, date or degree format, tense, what is bold | `profile/rules.md` |
| A voice rule: a banned word, a phrasing they prefer, a register note, a sample of their own writing | `profile/voice.md` |
| A fact: a number, a date, a thing they did, a hedge, a boundary ("I have not done X"), a corrected metric | `profile/evidence.md` (with its source: "user, <session date>") |
| A story or background detail for the story bank | `profile/me.md` |
| A change to their master resume content (a canonical bullet, a tagline option, the contact line) | `profile/resume.md` |
| A target-role or company preference | `profile/targets.md` |
| A positioning call: which story to lead with for a kind of role, what to downplay, a better "why me" line | `profile/positioning.md` (that role family's section) |
| A **generic** rule that would help any user (a workflow gate, a Google Docs API pitfall, a slop pattern, a scoring rule) | Propose it as a PR against `skills/` (see step 6) |

**One source of truth per rule.** Never create a new file, never start a "recent learnings" log.
If a rule already exists in weaker form, strengthen it in place; don't add a second copy. If a
learning fits two files, put it in the most specific one.

## Workflow

### 1. Scan the session for real feedback

Extract every instance where the user:
- corrected a bullet, verb, phrasing, name or framing;
- rejected an approach ("no", "don't", "stop", "that's slop");
- flagged a workflow or tool mistake (wrong tool, wrong order, missing step);
- confirmed a non-obvious choice ("yes, exactly", "keep that one");
- supplied a new fact, number or story detail that wasn't in the profile.

Ignore small typo fixes, one-off wording for this one job description, and anything tied only to
this company. **Capture only rules that will apply to future resumes and messages.** Facts are the
exception: every new or corrected fact goes to `profile/evidence.md` (it may already be there if
Gate 0's same-turn rule was followed; check before adding).

### 2. Classify each learning

For each item: **file** (table above), **action** (UPDATE an existing rule or ADD a new one), and
**why** (the underlying reason, so a future session can judge edge cases).

### 3. Check for existing coverage before writing

Grep the target file for the key noun or verb of each learning. If a related rule exists, edit it
in place to absorb the new nuance. Don't append a near-duplicate. Also grep `skills/resume/` for
the rule: if the generic skill already says it, the learning is a reminder, not a new rule; skip
it or note that the session ignored an existing rule.

### 4. Show the user the plan before writing

```
| # | Learning | File | Action | Target section |
|---|----------|------|--------|----------------|
| 1 | "Never call the internal tool 'Atlas'; say 'deploy dashboard'" | profile/rules.md | ADD | Naming |
| 2 | "Led the migration, did not support it" | profile/evidence.md | UPDATE | Acme Corp — migration |
| 3 | "'Orchestrated' reads as slop" | profile/voice.md | ADD | Banned words |
```

Ask: **"Write these N edits?"** Wait for confirmation. The user can edit or remove items.

### 5. Apply the edits

Edit each profile file in place, one edit per rule. Preserve existing headings and formatting; don't
reorder unrelated content. Write each rule as a plain imperative ("Never …", "Always …") in the
file's format, `- <rule> (why) — <YYYY-MM-DD>`, dated today, so `career-review` can find what
changed since its last run. Quote the user's own words where they are the rule.

### 6. Generic improvements: propose, don't push

If a learning is genuinely generic (it would help any user of the kit, and contains nothing about
this user), draft it as a change to the relevant `skills/` file and offer to open a pull request.
Strip every personal detail from it first: no names, employers, numbers, or quotes from this
session. Never commit it straight to the main branch.

### 7. Confirm

Report: files touched, count of UPDATE vs ADD, any PR proposed, and any learning you chose not to
capture and why (e.g. "specific to this one job description").

## What not to do

- Never write learnings into `skills/` directly.
- Never create a new file, section header or "learnings" log.
- Never capture JD-specific phrasings or one-off company quirks as rules.
- Never duplicate a rule across files "for safety".
- Never skip the plan confirmation step.
- Never edit the user's base resume doc from this skill.

## What counts as meaningful feedback

Capture:
- "Don't open bullets with 'Led'; use 'Built' or 'Shipped'" → `profile/rules.md`
- "That project closed 2 deals, not 3" → `profile/evidence.md`
- "I never say 'synergy'" → `profile/voice.md`
- "Always check for an existing tailored draft before writing from scratch" → generic; propose a
  PR to `skills/resume/references/step4-apply.md` (if not already there)

Skip:
- "Use 'launched' instead of 'shipped' for this role": specific to one JD
- "Move this bullet up": one-off ordering for this doc
