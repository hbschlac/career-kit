# Gate 2 — Voice, one pass over the finished set

Facts are frozen after Gate 0; this gate changes **wording only**. Run it once over the whole swap
list, not per bullet. For bullets the quick reference below is enough; load `profile/voice.md` and
`skills/voice/SKILL.md` in full only for a cover letter or application answers.

## Use the user's own voice

`profile/voice.md` and `profile/me.md` may hold the user's own words from real writing
(application answers, emails, posts). Prefer their natural phrasing over generic professional
language; grep for it before drafting (`bash skills/resume/scripts/ledger_grep.sh <term>`).

### The user's-noun rule

**When the user supplies a fact in their own words, the bullet keeps their noun.** Don't improve
it into a synonym. If they said "playbook" and the bullet says "process doc", they will report
their own content as missing. If the author can't spot it, a reader won't.

| They said | It became | What goes wrong |
|---|---|---|
| playbook | "process doc" | they can't find their own work on the page |
| cut the vendor | "optimized vendor spend" | a decision reads as routine cost work |
| rewrote the onboarding | "improved the new-user experience" | the concrete act disappears |

Also honor explicit vetoes: every banned word or phrase in `profile/voice.md` and
`profile/rules.md` stays off the page.

## No AI slop

AI slop is generic, fluffy language that could appear on anyone's resume. The full checklist and
correction workflow is the `aislop` skill (`skills/aislop/SKILL.md`). **Run it on all drafted
bullets after the verb scan and before any doc edit.** Fix every flag.

### Quick-reference red flags

- **Buzzword stacking:** "Leveraged data-driven insights to drive strategic alignment across
  cross-functional stakeholders"
- **Outcome-free claims:** "Improved team efficiency" (by how much? doing what?)
- **Passive framing:** "Was responsible for", "Helped to ensure", "Contributed to", "Played a key
  role in"
- **Corporate filler:** "Partnered with", "Collaborated with", "Worked closely with"
- **Vague scope:** "large-scale system", "significant impact", "major initiative"

### The correction standard

- Plain, short verbs: "built" not "constructed", "shipped" not "operationalized".
- Action + measurable outcome + why it mattered.
- Specific numbers, team names, tool names: things only this user could claim.
- Gut check: cover the name. Could this bullet belong to anyone with the same title? If yes, it's
  still slop.
