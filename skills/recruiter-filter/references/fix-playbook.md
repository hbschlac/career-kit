# Fix playbook

Loaded at Step 5, when converting a score into edits. Work from the user's real material —
`profile/resume.md` for what's on the page, `profile/evidence.md` for facts and numbers
(grep it for the claim you need; never read it whole), `profile/me.md` for projects and story
angles. The before/afters below are fictional examples of each pattern, across several
functions.

## The truth rule, restated

Three legal moves: **surface**, **reframe**, **quantify**. If a fix is none of those, it is
a gap — report it. The test: *could the user defend this line under five minutes of
questioning from someone who does the job?* If not, cut it. A CV that scores 90 and falls
apart on the screening call is worse than one that scores 70 and holds.

**Quantify never means invent.** If the number isn't on the page and isn't in
`profile/evidence.md`, ask the user. An estimated metric on a resume is a fabricated metric.

## Pattern 1 — Top-third takeover (highest yield, almost always available)

The 6-second skim reads headline + current title + first two bullets. If the JD's core
requirement isn't in that block, nothing else you fix matters as much.

The move is not to add — it is to **reorder**. Promote the bullet that covers the JD's top
must-have into position one of the current role, and demote the one covering its
lowest-priority ask. Same content, different order, big rank delta.

For a platform / infrastructure req (engineer):
> before (bullet 3): "Worked on the payroll service's reliability."
> after (bullet 1):  "Own the payroll service — 99.99% uptime across 40K employer runs a month;
>                     cut p95 latency 40% by caching tax tables."

For a 0→1 / founding req, the strongest shipped project belongs above older role bullets or
in the headline rather than filed on page 2 — see *Which project to lead with* below.

## Pattern 2 — Vocabulary reframe (cheap, safe, moves Dimensions 1 and 4 together)

Companies name the same work differently. Use the req's noun, keep the user's work.

| The user's word | Req's word (use the req's) |
|-----------------|----------------------------|
| Help desk | IT service management, end-user support |
| Experiments | A/B testing, experimentation platform, causal measurement |
| Charge nurse | clinical operations, shift leadership |
| Reporting dashboards | analytics platform, BI, data infrastructure |
| Lesson plans | curriculum design, instructional design |
| Style guide | design system, component library |
| Email campaigns | lifecycle marketing, CRM, retention |
| Side project | built and shipped, 0→1, prototype to production |

Two rules. **Mirror, don't stack** — one term per concept, the req's term, not a slash
pile. And **only where the work matches**: calling reporting dashboards "analytics
platform" may be fair; calling them "data engineering" is not.

## Pattern 3 — Title bridging (Dimension 1, 20 points)

Recruiter boolean search runs on titles. When the user's title isn't one they'd search:

- Add a **parenthetical scope line**, never a false title:
  `Accountant II (Revenue Recognition)`, or
  `Software Engineer II (Payments Platform)` — accurate, and now matches a search.
- For a pivot req, a **target-title headline** above the experience block does the work
  legitimately: `Product Designer — B2B workflows · design systems at 500-customer scale`.
- Never restyle the employer-of-record title. Scope qualifiers are fair; a promotion the
  user didn't get is not.

## Pattern 4 — Evidence upgrade (Dimension 3, 20 points)

Duty verbs score low; outcomes with scope score high. Match the JD's *own* metric — if the
req is measured on conversion, lead with conversion; if on activation, lead with activation.

> before: "Ran experiments to improve onboarding."
> after:  "Redesigned onboarding for 50K monthly sign-ups; lifted 7-day activation 18%."

> before (marketing): "Managed lifecycle emails."
> after:              "Rebuilt the lifecycle program (12 journeys); cut 90-day churn 9%."

Prefer, in order: outcome + scope + timeframe > outcome > scope alone > activity. An
unquantifiable bullet can still carry **scope** — org size, volume, surface area, budget.
`Managed a $2M annual vendor budget across 14 contracts` is scope without an attribution
claim.

## Pattern 5 — Recency rescue (Dimension 5, 10 points)

A must-have last touched six years ago scores badly. Two honest routes:

1. **Find it in current work.** Often the skill is live and unlabeled — an internal tool
   the user built is current evidence whether or not it's in their job description.
2. **Use projects.** A current, dated, shipped side project is legitimate recency evidence
   and the fastest truthful fix for a stale skill — provided the user would still defend it
   today.

If neither works, it's a gap. Say so.

## Pattern 6 — Parse and skim safety (Dimension 6, 10 points)

Actual failure modes, in order of how often they bite:

- Contact details inside a header/footer or a graphic → often dropped by the parser.
- Multi-column layouts → columns interleave; bullets get attached to the wrong employer.
- Skills rendered as icons, ratings, or bar charts → no text, no match, no citation.
- Inconsistent date formats (`2024–present` vs `Jan 2024 - Now`) → broken tenure math,
  which then breaks a "5+ years" screen.
- Image-only PDF → parses to nothing. Text-layer PDFs are fine; the myth is that PDFs as a
  format fail.
- Non-standard section headers ("My Journey") → the parser can't map the section. Use
  Experience / Education / Skills / Projects.

Skim-safety is the other half: if page one is a wall, the human bails before the parser
ever mattered.

## Which project to lead with

Do not lead with the biggest-sounding project. Lead with the one that survives the
follow-up question. Rank by, in order:

1. **Is it running now?**
2. **Can the user defend how it works in detail?**
3. **Does it evidence this req's load-bearing requirement?**
4. Only then: how impressive the description sounds.

A project that shipped but never got users is **built scope, not traction**. Describe it as
what was built ("digitized 12 intake forms, 3 clinics"), never as adoption — the
first screener question ("how many people used it?") collapses an adoption claim it can't
back. Use it only where its *specific* content matches the req. The truth rule applies to
the user's own portfolio first.

Reliability details are often the strongest part of a project and the part people leave
off: "backs itself up nightly and emails a summary if a job fails" is the difference
between a script and a product.

Match project to req type: automation / agent / platform reqs want the project that runs
unattended; consumer / community reqs want the one with real users; developer-experience
reqs want the tooling or docs work. If `profile/me.md` lists which project fits which kind
of role, follow it.

If the user wants a number on a project, **ask them** — unless it's already in
`profile/evidence.md`, an estimated metric is a fabricated one.

## Application questions (Layer 1 — where the actual rejects live)

Check these before polishing prose. On Ashby and Greenhouse the custom questions are the
real auto-reject surface.

- **Gating questions** (work auth, sponsorship, onsite days, years, licensure) — answer
  accurately. A false answer here is the one unrecoverable move; it surfaces at offer.
- **Free-text boxes** ("why this company," "tell us about a project") are increasingly
  LLM-read. Treat each as a scored short answer: name the company's actual product, one
  specific piece of evidence, under 150 words, in the user's voice (`profile/voice.md`).
  Route drafts through `aislop`.
- **Salary expectations** — a number outside the band is a silent knockout. If the posting
  shows a range, stay inside it.

## When the honest answer is "don't apply cold"

Under 55 after the top fixes, or a hard-gate fail: say it plainly. The highest-EV move is a
referral or a targeted project, not another resume pass. Route to `job-search` (better-
fitting reqs at the same company), `networking` (outreach to a human who can bypass the
stack entirely — check `profile/contacts.md` for a warm path), or `project` (build something
for that team). One warm intro outranks every point on this rubric.
