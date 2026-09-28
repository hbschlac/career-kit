---
name: project
description: >
  Builds a targeted project for a job application: a small, live piece of work product scoped to
  one team's real problem, so the hiring team sees the user already understands their world. Fits
  any role: a research dashboard or memo, a product or competitor teardown, a working prototype, a
  writing sample, a design case study, a sales or ops plan. Use when the user asks "what should I
  build for this application", "I want to do a project for X", or wants a live artifact for an
  application or interview. Sub-skill of networking.
---

# Project Skill

For a role the user really wants, a resume is not enough. Build something.

The goal: ship a focused piece of work in about 1 to 2 hours that makes the hiring team think
"this person already gets our problems" before they have talked. It is not a side project. It is
targeted work product: scoped to that team's actual problem, in the format that team uses, live or
shareable, with a clear "so what".

Before starting, check `profile/me.md` for the user's skills and tools, and `profile/targets.md`
for the role type. Scope to what the user can actually build and defend in an interview. Never
present Claude's work as a skill the user does not have; if Claude does most of the build, the
user should be able to explain every decision in it.

---

## The angles

Pick the one that matches how this team makes hiring decisions. Examples of each are fictional.

### Angle 1: Research / insight
**What:** find real signal on a problem the team owns. Analyze public feedback, reviews, forums,
job posts, pricing pages, public datasets, or filings; map the competitive landscape; surface
patterns they may not have quantified. Ship as a live page, dashboard, or one-page memo.

**Fits:** product, strategy, research, growth, marketing, analytics, UX research, investing,
consulting.

**So what:** you did their homework. You arrive knowing what their users complain about, what
competitors do, and where the opportunity is.

**Example (product analyst at Acme Corp):** 900 public app-store reviews and forum posts about
Acme's mobile app, clustered into 6 themes. Live page with each theme drillable to source quotes.
Thesis: "The top reason users leave is missed prescription-refill reminders."

**Memo vs dashboard.** Use a **one-page memo** when the reader is research-minded or will spend
under 60 seconds: one sharp, non-obvious finding, one stat, methodology one click away. Use a
**dashboard** when the reader wants to drill in themselves. A memo reads like an internal strategy
doc, which itself signals "already thinking like the team".

### Angle 2: Prototype
**What:** build a working slice of the product, or a convincing demo of where it could go.

**Fits:** software engineering, product, design engineering, developer relations, AI and platform
teams, any "builders welcome" culture.

**So what:** you shipped the thing. A live demo is worth several resume bullets.

**Example (frontend engineer at Northwind):** a working appointment-booking flow using Northwind's public API
and design tokens, deployed with a demo mode so no login is needed.

### Angle 3: Teardown or plan
**What:** a structured critique or plan for one surface or motion: an onboarding teardown with
redlines, a 30-60-90 plan for a territory, a support-ops audit of a public help center, a pricing
page teardown, a launch plan.

**Fits:** design, product marketing, sales, customer success, operations, program management.

**Example (account executive at Globex):** a one-page territory plan for mid-market retailers in
the region, with 20 named target accounts, the trigger event for each, and a first-touch message
for three.

### Angle 4: Writing or design sample in their format
**What:** produce a real example of the work the role does, for this company: a blog post in their
voice, a help-center article rewrite, a case study, a redesigned screen, an email sequence, a
policy brief.

**Fits:** content, communications, UX writing, design, policy, education.

**Example (content designer at Acme Corp):** rewrite of Acme's three most-visited help articles,
with before/after readability scores and a short note on the principles applied.

If two angles fit, pick one and go deep; two shallow projects are worse than one sharp one.

---

## Workflow

### Step 1: Understand the team's scope
From the JD and any context the user has:
- What problem does this team own?
- What is its biggest open question right now (from public sources)?
- Who are its users or customers, and what do they complain about?
- What does success look like for this role in 6 months?

### Step 2: Pick the angle
Match how the team decides: a growth team cares about data, a platform team about demos, a design
team about craft, a sales team about pipeline. State the angle and a one-paragraph rationale.

### Step 3: Scope it (completable in about 2 hours)

**Research:** one product area or surface; 3 to 5 public sources reachable without logins; 5 to 7
findings, not 20; one page; one thesis sentence.

**Prototype:** one user flow; demo mode (no real auth to see the value); the company's own stack
or public APIs where possible; a running URL, not a mockup.

**Teardown / plan:** one surface or one motion; concrete recommendations tied to evidence; fits on
one or two pages.

**Writing / design sample:** one to three pieces; matches the company's published style; shows
before and after where relevant.

Only use public data, and respect sites' terms. Do not scrape behind logins or collect personal
data about individuals.

### Step 4: Write the "so what" before building
> "I built [X] to show [team] that [insight or capability]. The so what: [what this proves about
> the user for this role]."

If it will not fill in cleanly, the scope is wrong. Revise until it is crisp.

### Step 5: Build and publish
- A real, shareable URL (a deployed site, a published doc, a public repo, a hosted PDF)
- Readable on a phone
- No login wall in front of the key demo
- Source or methodology available for anyone checking rigor
- Neutral framing: "independent analysis of public feedback", not branded as the company's own

### Step 6: Write the application hook
The CV line or cover-letter sentence must: name the thing in one sentence, say where to find it,
deliver the "so what" in one sentence, and not over-explain.

> I wanted to see what I could learn about [team's problem] before interviewing, so I built
> [project], [one-line description], at [URL]. The so what: [what it shows about the user for this
> role].

Run it through `skills/voice/SKILL.md` and `skills/aislop/SKILL.md`. Log the project link in the
role's tracker row (Notes, via `skills/networking/references/pipeline.md`).

---

## Gift framing (after meeting someone)

When the user has met someone at the target company, the same work can be a gift instead of an
application. Different rules:

- **No prescription, no resume, no ask.** Outsiders organize signal; they do not tell a team what
  to prioritize. Cut any "here's what you should do" section.
- **Utility beats portfolio.** If the recipient will actually use it, order it for them: a
  one-sentence description of what it is, when the data was last refreshed, definitions of any
  labels, then the content. Strip anything that reads as "here's what this proves about me".
- **Match claims to what is wired up.** If a source they mentioned is not actually covered, say
  what is covered. An honest scope reads better than an overclaim they will spot in seconds.
- **The message drops the "so what".** Warm opener naming something specific from the meeting, what
  the tool does in one sentence, the link, and a practical handoff ("open source if anyone wants to
  adapt it"). The project is the signal; explaining it turns the gift into an ask.
- **Plain words in the one-line description.** Re-read it with an outsider's ear.

---

## What to produce

1. **Angle recommendation** with a one-paragraph rationale
2. **Scoped brief:** what to build, sources or stack, the one-sentence thesis
3. **Pre-build check:** confirm it is achievable in about 2 hours with the user's tools
4. **Application hook draft:** the CV line or cover-letter sentence
5. **Offer to co-build:** stay in the session to scope, build and publish

## Hand-offs

- Outreach that leads with the finished project: `skills/networking/SKILL.md`
- Adding the project to the CV: `skills/resume/SKILL.md` (a project line must be as factual as any
  other bullet; add its facts to `profile/evidence.md` first)
- Voice for the hook: `skills/voice/SKILL.md`
