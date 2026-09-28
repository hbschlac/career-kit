# Resume rules — the generic core

These hold for every resume the kit writes, for any role (engineer, designer, PM, marketer, ops,
sales…). The user's own rules live in `profile/rules.md` and are applied on top; where they
conflict, the user's rule wins. The user's content (roles, bullets, tagline options, contact line)
lives in `profile/resume.md`; this file never holds content.

## The rules (non-negotiable on every version)

1. **Every bullet earns its place against the JD.** Before editing, name the 2–3 things this
   company cares about most (e.g. "reliability at scale", "0-to-1 product", "enterprise sales
   motion"). Every bullet that survives connects to at least one. Cut or move back the rest.

2. **Show someone who builds, not someone who attends.** Favor verbs that show the user did the
   work: built, shipped, launched, designed, closed, cut, grew. Not "supported", "partnered on",
   "contributed to", "helped drive".

3. **Every bullet = action verb + measurable outcome + why it mattered.**
   *[What they did] → [by how much / at what scale] → [why it mattered].* The "why it mattered" is
   the piece most resumes skip. If there is no number, find the best real proxy (team size, scope,
   time saved, adoption, users, revenue) or cut the bullet. Never invent a number; sharpen what is
   real.
   - Weak: "Built internal analytics dashboard"
   - Strong: "Built self-serve analytics dashboard adopted by 6 sales teams, cutting weekly
     reporting from 2 days to 2 hours"

4. **No repeated opening verbs.** Every bullet across the whole resume opens with a different
   verb. Scan the full list before finalizing, and again after every batch of edits. When two
   collide, rethink the framing of one; don't just swap in a synonym.

5. **Exactly one page.** If content doesn't fit, cut or shorten content. **Never** change font
   size, font style, spacing, margins or any other formatting to make it fit; only the words
   change.

6. **Every bullet fits within 2 lines** in the rendered doc. Tighten the language, keeping the
   action + outcome + why structure. Measure it with `skills/resume/scripts/cvcheck.sh`; don't estimate from
   character count and don't ask the user to eyeball it.

7. **The italic role/company descriptor fits on exactly 1 line.** Shorten it; don't let it wrap.

8. **The tagline fits on exactly 1 line** and passes match + metric + why-you (rule 8 of
   `SKILL.md`). A tagline that only describes what kind of professional the user is fails,
   however well it echoes the JD.

9. **No jargon.** Role keywords are fine when they match the JD, but no line should leave a reader
   asking "what does this actually mean?" Test: could a smart non-specialist read the bullet and
   say what the user did and why it mattered? If not, rewrite in plain, specific language. Also:
   replace any employer-internal name (a codename, an internal tool name) with what the thing
   *is*; the reader cannot decode it.

10. **Never add a bullet that isn't grounded in real work.** Sharpen and reframe; don't invent.
    Every fact traces to `profile/evidence.md`, `profile/me.md`, `profile/resume.md` or the
    user's words this session.

11. **The user's rules.** Apply every rule in `profile/rules.md`: naming bans, section order,
    skills-line ordering, header/contact line format, date formats, education line format, tense,
    bold/italic conventions.

## Bullet patterns that work

- **Lead with total scope, then one proof point.** The number that states the user's altitude
  (the budget, revenue line, org size or user base they were accountable for) beats a single win.
  Use at most one feature-level win as a concrete example inside that scope; never stack several
  single-win numbers as a headline.
- **"Features" beats "experiments" for shipping roles.** When the JD is about launching product,
  "shipped features" reads delivered; "ran experiments" reads exploratory. Use "experiments" when
  the role explicitly values experimentation rigor.
- **Integrate advocacy into a launch bullet, never standalone.** "Championed [customer need] by
  launching [specific thing] that [measurable outcome]" beats an abstract advocacy bullet plus a
  neutral launch bullet.
- **Name the audience precisely.** If a role served several distinct audiences (customers,
  investors, internal teams, partners), pick the specific label; never use "clients" or
  "stakeholders" loosely, and separate bullets by audience rather than merging them.
- **Frame tools and systems as standing mechanisms.** "Became the default planning layer for 4
  teams" signals durable impact; "saved 40 hours" is a one-off.

## Verb bank (to avoid repetition)

Built, Shipped, Launched, Designed, Led, Owned, Created, Developed, Defined, Identified, Mapped,
Scaled, Drove, Accelerated, Reduced, Cut, Increased, Grew, Expanded, Established, Architected,
Deployed, Pioneered, Negotiated, Closed, Streamlined, Rebuilt, Directed, Delivered, Enabled,
Automated, Migrated, Instrumented, Analyzed, Trained, Hired, Won, Secured.

Avoid as openers (they read as filler; see the `aislop` skill): Leveraged, Spearheaded,
Orchestrated, Utilized, Facilitated, Assisted, Helped.

## Tagline options

`profile/resume.md` may hold a few stock taglines by audience. **They are vocabulary, not finished
taglines**: none names a specific JD requirement, so none passes match + metric + why-you as-is.
Build from them; never paste one.
