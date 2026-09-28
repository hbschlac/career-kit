---
name: aislop
description: >
  AI slop detector and corrector. Use when the user says "aislop", "check for AI slop", "slop
  check", "does this sound like AI", or when the resume or networking skill calls for a slop audit.
  Scans any draft (resume bullets, cover letters, application answers, outreach) for generic,
  jargon-heavy, inflated AI writing, reports what is wrong line by line, and rewrites flagged lines
  in the user's own voice from profile/voice.md.
---

# AI Slop Detector

Audits draft text for AI-generated slop and rewrites flagged lines in the user's voice.

## Step 1: Load the voice

Read `profile/voice.md`. It is the ground truth for what "sounds like the user" means. Pay
attention to its vocabulary defaults, sentence rhythm, punctuation habits, and banned list, and
merge the banned list into the kill list at the bottom of this file. Also check `profile/rules.md`
for wording rules.

If `profile/voice.md` is empty or still a template, say so, offer the `setup` skill, and run the
audit with the generic categories only; rewrites will be plain and neutral rather than in the
user's voice.

## Step 2: Run the slop checklist

Scan every line against these categories. Flag any line that trips one or more.

**1. Buzzword stacking.** Several hollow corporate words in one sentence.
- Slop: "Leveraged data-driven insights to drive strategic alignment across cross-functional stakeholders"
- Clean: "Built a pricing model that cut decision time from 3 days to 20 minutes"

**2. Outcome-free claims.** Action with no measurable result. Improved what, by how much, for whom?
- Slop: "Improved team efficiency and enhanced collaboration"
- Clean: "Cut the release cycle from 3 weeks to 2 by merging four request channels into one triage board"

**3. Passive or weak framing.** The writer hides behind the verb.
- Kill list: "was responsible for", "helped to", "contributed to", "assisted with", "supported",
  "played a role in", "was involved in"
- Fix: make the user the subject. They built it, shipped it, launched it, designed it.

**4. Corporate filler.** Sounds professional, says nothing.
- Kill list: "partnered with", "collaborated with", "worked closely with", "engaged stakeholders",
  "aligned teams", "drove alignment", "fostered collaboration"
- Fix: say what the user actually did with those people. "Co-designed the scoring model with the
  data team" beats "collaborated with cross-functional stakeholders".

**5. Vague scope.** Big-sounding scope with no number.
- Kill list: "large-scale", "significant impact", "major initiative", "various projects",
  "numerous", "multiple stakeholders", "key metrics"
- Fix: use the real number from `profile/evidence.md`. "Large-scale system" → "system processing ~2M
  claims a month". No number? Use the best true proxy or cut the word. Never invent one.

**6. Adverb stuffing.** Adverbs propping up weak verbs.
- Kill list: "effectively", "strategically", "proactively", "seamlessly", "holistically",
  "successfully", "significantly", "substantially", "autonomously" (for AI agents, it is a given;
  say what the agent does)
- Fix: delete the adverb. If the sentence goes flat, the verb is the problem; replace the verb.

**7. Abstract nouns over concrete verbs.** Nominalizations that bury the action.
- Slop: "Facilitated the optimization of the month-end reconciliation process"
- Clean: "Rebuilt the month-end reconciliation script; close went from 5 days to 2"
- Pattern: "[weak verb] the [noun] of" → rewrite as a direct verb

**8. Template phrasing.** Could appear on anyone's resume unchanged.
- Test: cover the name and company. Could this line belong to anyone? Then it is slop.
- Slop: "Led cross-functional team to deliver high-impact initiatives"
- Clean: "Led 4 engineers and 2 designers to ship the first self-serve refund flow in 8 weeks"

**9. Missing "so what".** Says what was done, not why it mattered.
- Every bullet: **[what they did] → [by how much / at what scale] → [why it mattered]**
- Slop: "Built a policy lookup page for support teams"
- Clean: "Built a policy lookup page used by 300 support agents, cutting escalations 20%"

**10. Jargon without grounding.** Technical terms used to sound smart. Test: could a smart outsider
understand what the user did?
- Slop: "Implemented a microservices-based architecture leveraging event-driven paradigms"
- Clean: "Split the monolith into 6 services so teams could deploy independently; deploys went from weekly to daily"

**11. Bland verbs.** Verbs that describe a role, not an action.
- Kill list: "managed", "oversaw", "handled", "utilized", "ensured", "facilitated",
  "coordinated", "maintained"
- Prefer: built, shipped, launched, designed, led, created, defined, owned, scaled, diagnosed,
  proved, tested, found, automated, consolidated, restructured. Use the user's own preferred verbs
  from `profile/voice.md` or `profile/rules.md` if listed.

**12. Hedging achievements.** Softening that dilutes ownership.
- Kill list: "helped drive", "played a key role in", "was instrumental in", "contributed to the
  success of", "supported the launch of"
- Fix: if they did it, say so. If they did part of it, name their part precisely.
- Also flag representativeness hedges ("one example", "e.g.", "for instance") on a bullet that is
  the only entry for a role. Readers assume representativeness; the hedge signals under-confidence.

**13. Preposition imprecision.** A wrong small word misframes the claim.
- Slop: "collected $2M across 12 donors" (money comes *from* people)
- Clean: "collected $2M from 12 donors"
- Audit: money comes *from*; results land *across* surfaces; tools are *adopted by* teams; features
  *ship to* users.

**14. Named side projects plus jargon in a cold message.** In a cold DM to a senior reader, one
portfolio link beats listing projects with descriptors.
- Slop: "building side projects (most recently a solo-built recipe app with 40 integrations)"
- Clean: "building side projects (more here: example.com/projects)"

**15. Usage-frequency overclaims.** Never "used daily by X" unless telemetry backs it. Prefer reach
or adoption claims.
- Slop: "a macro library now used daily by 60 support agents" (daily use unverified)
- Clean: "a macro library adopted by a 60-person support team"

**16. Adjectives the number already implies.**
- Slop: "a **significant** $5M cost saving" → "a $5M cost saving"
- Rule: if the number is the proof, drop the adjective.

**17. Modifier-stacked nouns.** Three or more modifiers before a noun.
- Slop: "Built an award-winning cross-team internal shift-scheduling dashboard..."
- Clean: "Built a shift-scheduling dashboard that 4 nursing units share; it won the hospital's ops award"
- Test: count the modifiers. 3+ → rewrite as a clause.

**18. Misplaced modifiers that change the meaning.**
- Slop: "proposed to the principal an unasked-for new tutoring schedule" (the *proposing* was unasked-for)
- Clean: "proposed to the principal, unasked, a new tutoring schedule"
- Test: put the modifier next to what it actually modifies.

**19. Ungrounded rhetorical claims.** Punchy judgments about other people, companies or markets
that cannot be defended.
- Slop: "a designer who fixes products at companies that don't value design"
- Clean: "a designer who has redesigned intake forms at a clinic, a school district and a bank"
- Test: every adjective applied to a third party must be true or removed.

**20. Stock AI constructions.** Patterns readers now recognize as machine-written.
- "It's not X, it's Y" / "This isn't just X; it's Y" reframes
- "In today's fast-paced world", "at the intersection of" used as filler, "delve", "tapestry",
  "testament to", "navigate the complexities"
- Triplets of abstract nouns ("innovation, collaboration and excellence")
- A closing line that restates the paragraph

## Step 3: Report

For each flagged line:

```
LINE: [original text]
SLOP TYPE: [category, e.g. "Buzzword stacking + Outcome-free claim"]
WHY: [one sentence]
REWRITE: [corrected version in the user's voice]
```

If nothing is flagged: "Clean: no slop detected."

Rewrites never add facts. If a fix needs a number the draft does not have, grep
`profile/evidence.md`; if it is not there, ask the user or cut the claim, and say which you did.

## Step 4: Final gut check

Re-read the full draft after the rewrites:

1. **Could this belong to anyone in this role?** Every bullet should hold something only this user
   can claim (a specific tool, number, or context).
2. **Does it sound like the user or like a chatbot?** Cross-check against `profile/voice.md`.
3. **Is the "so what" real?** Specific and believable, not inflated. If the number is not real, cut
   it rather than inventing one.

## When called from the resume skill

Run the full checklist on all bullets after the verb scan and before the Google Doc update. Fix
every flag first.

## Quick kill list (scanning speed)

Almost always slop in a resume or outreach context; flag on sight. Add the user's banned list from
`profile/voice.md`.

> leveraged, utilized, spearheaded, orchestrated, synergized, operationalized, effectuated,
> facilitated, streamlined (without a number), optimized (without a number), enhanced (without a
> number), fostered, empowered, championed, endeavored, ensured, oversaw, managed (as a lead verb),
> aligned, partnered with, collaborated with, worked closely with, cross-functional (as filler),
> stakeholders (without naming who), significant, substantial, various, numerous, key, critical,
> robust, scalable (without context), end-to-end (without specifics), best-in-class, world-class,
> cutting-edge, innovative (without showing it), transformative, impactful, actionable, holistic,
> seamless, proactive, strategic (as an adjective), autonomously (for AI agents), superpower,
> entities (as in "partner entities"), delve, tapestry, testament to
