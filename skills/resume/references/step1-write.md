# Gate 1 — Write the whole set in the conversation

Draft **every** bullet, the tagline and the skills line here as a from→to swap list, before any
doc call. Load now, in full: `references/resume-rules.md` (the generic rules and verb bank),
`profile/resume.md` (the user's base content) and `profile/rules.md` (the user's own rules). Facts
come only from Gate 0's grep results and the user's words this session.

## The core premise

The resume has one job: make it obvious, for *this* role, that the user has already done the work
the job needs, and that it moved numbers. Every decision (which bullets lead, which verb, which
number) serves that.

If the resume could belong to anyone with the same title, it's wrong. If it reads as a list of job
duties, it's wrong. If it leans on "partnered with stakeholders" or "drove alignment," it's wrong.

## Writing rules beyond the core

**Surface "I already do this" explicitly, never in subtext.** When the user says they already do X
(playbooks, dashboards, automation, code review, customer research), the bullet names X in the
JD's keywords. Implying it through adjacent work is not enough; the recruiter won't connect the
dots.

**Echo JD language directly where natural.** If the JD uses a load-bearing phrase ("durable
mechanisms", "developer experience", "pipeline generation"), mirror it verbatim in at least one
bullet. Verbatim JD language is a stronger signal than a paraphrase.

**Preserve domain nouns when adding a "why it mattered" tail.** Appending an impact clause must not
rename or collapse the original nouns. "claims-processing pipeline" stays "claims-processing
pipeline", not "pipeline". Restore the original phrase exactly, then append.

**Tailor titles to the JD.** When a past title has suffixes that point away from this role (e.g.
"& Programs" for a product role, or "Engineering" for a program role), prune them if
`profile/evidence.md` shows the user actually held the relevant scope. The title should signal the
same shape as the JD. Never invent a title.

**Faithfulness when pulling from old resumes.** When reusing content from an older version,
preserve the original meaning; never paraphrase into something different. Show provenance
("from the 2022 resume, verbatim: …") so the user can verify nothing was invented or
misattributed.

**Domain-specific integration claims: cite or ask, never infer.** A bullet that says "integrated X
into Y" or "fed X into Y's Z layer" either quotes the user's own wording from the ledger or asks
"what did X actually integrate into?" first. Don't infer the target from adjacent facts; the
ledger says what was owned, not every system-to-system wire. Close-but-wrong reads as a bluff.

**Superlatives need verification.** "Largest / first / only in X history" needs an external
source before it lands. Narrow to what's verifiable; a smaller accurate superlative beats a bigger
unverifiable one.

**Protect the strongest lines.** When a replacement the user dictates weakens an existing strong
line, flag the regression explicitly ("this is weaker than what it replaces; here is what you'd
lose") instead of silently accepting it.

**"Own [system]" is a sub-header, not a bullet.** "Own the billing platform" describes the job,
not the work. Lead with what they *did* (launched, rebuilt, cut). Static ownership belongs in the
italic role descriptor.

**For senior roles, every bullet answers "how did this go beyond the job?"** The reader assumes the
user did their job. Show scope expansion, scale beyond expectation, a new structure created, or an
outcome that exceeded the mandate.

**Frame systems as compounding.** For a tool or dashboard, ask: did it become the standing way the
team works? If yes, say that.

## Content steps

1. **Classify the JD**: its 2–3 themes, its #1 requirement, and which role family in
   `profile/positioning.md` it belongs to. Grep that section and use its lead story, proof points
   and words. If no family fits, say so and draft from the story bank; after the session, offer to
   add the new family to the file.
2. **Draft the tagline** (see *Tagline* below), starting from that family's "why me" line.
3. **Start with the most recent / most relevant role**; this is where most tailoring happens.
   Reorder to front-load the most relevant bullets; rewrite verbs or "why it mattered" clauses to
   connect to the themes.
4. **Review the other roles**: usually kept or lightly adjusted; cut clearly off-angle bullets.
5. **Projects section, if it adds.** Include a projects section only when it is additive for this
   JD (0-to-1 building, a portfolio the role values, a skill the experience section doesn't prove).
   If the experience bullets already prove the skill, a project dilutes; use the space for
   experience instead. Title it in the JD's vocabulary ("Applied ML Projects", "Open Source",
   "Design Work"), not a generic "Projects". Prefer one consolidated breadth bullet over a
   headline-project bullet plus a breadth bullet that re-mentions it.
6. **Skills line last.** Order it per `profile/rules.md`; within that, surface the skills the JD
   emphasizes first.
7. **Verb scan**: list every opening verb across every bullet; rewrite any repeat.

## Formatting defaults (the user's `profile/rules.md` overrides any of these)

**Page:** exactly one page; content changes, formatting never does.

**Header:** name, then the contact line exactly as in `profile/resume.md` (built from
`profile/config.json`: phone, email, LinkedIn, website), then the one-line tagline.

**Section ownership:** anything paid with a formal title goes in EXPERIENCE. Projects, community
work, skills and interests go in the additional section. Never demote a paid role.

**Experience entries:**
- `Company | Role | Location — Dates`
- Months on every role's outer date range (`Jan 2021 – May 2023`, not `2021 – 2023`); take them
  from `profile/evidence.md` and never invent a missing month.
- One-line italic descriptor of what the company/team does; 1 line max.
- 3–5 bullets for the primary role, 1–3 for older ones.
- **Secondary-role compression:** under one-page pressure, an older role can collapse to one
  bullet with a triple-action structure: "[Verb1] X; [Verb2] Y; [Verb3] Z."
- **Descriptor/bullet redundancy:** a number or distinctive noun in the descriptor never repeats in
  a bullet beneath it.

**Bullets:**
- No periods at line end; consistent `%` and `$`; tilde for approximations (`~30%`).
- No em dashes inside bullets; join clauses with a semicolon. The em dash stays in the date range.
- No `+` or `/` as shorthand for "and"; it reads informal.
- Past tense for roles that ended. Present tense only for things the user still personally runs.
- Never "fix" a deliberate style from `profile/rules.md` (e.g. dropped articles) as a typo.

## Tagline

**Rule 8 in `SKILL.md` governs: match + metric + why you, all three, in one line.** Build it:

1. **Match (a):** the JD's #1 requirement, in its words.
2. **Metric (b):** the ONE ledger number that proves the user has done that at scale; total scope,
   not a single win. Grep it; never invent or round up.
3. **Why you (c):** the thing the user already did that *is* this job.
4. When one line is too tight, cut in this order: adjectives → employer names → extra list items.
   Never cut the match or the metric.

Shape: `<JD role identity> who <did the JD's #1 need> — <metric>`. Print it in the swap list as
`tagline: "…"  (a) <JD words> (b) <number + ledger source> (c) <their proof>`.

What a tagline is for: it gets about a second of the recruiter's skim. It (1) positions the user
in the right bucket ("Backend engineer", not "Technology professional"), (2) lands the JD's
keywords, (3) makes only defensible claims, and (4) sets the lens for the bullets below.

- Passes: JD words for the role + the number that proves it + what they did that is the job.
- Fails: a list of employers instead of the match ("Engineer with experience at Acme, Globex and
  Northwind"); could head any resume.
- Fails: stacked identities ("Designer, researcher, and builder across agencies and startups").
- Fails: an adjective with no proof ("Customer-obsessed marketer").
- Fails: a rhetorical claim about third parties ("PM who ships where others can't").
- Fails: a number the reader can't decode cold ("27 tools shipped").
- Fails: a bare accomplishment with no role identity; it makes the whole page read as one win.

**Check tagline nouns against the target company's world.** Industry-native terms from a past
employer ("GMV", "ranking", "tickets") read narrow elsewhere. Would this noun appear in the target
company's product reviews? If not, swap for a transferable abstraction.

## Output of this gate

A swap list in the conversation: `find → replace` for the tagline, every changed bullet, the
skills line, and any header/date/education line that differs from `profile/resume.md` /
`profile/rules.md`. No doc calls yet.
