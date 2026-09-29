# Build a question bank for any role

Only product management ships with a ready bank (`pm-question-bank.md`). For every other role
family, build a short one for this interview from the JD, the research brief, the family's section
of `profile/positioning.md`, and `profile/targets.md`. Twelve to twenty ranked questions the user
actually practices beat a hundred they skim. Don't build banks for families that aren't in play.

## Inputs

- **The JD:** must-haves, nice-to-haves, and the verbs it uses
- **The brief** from Mode 1, if it ran: recent moves and likely themes
- **The family's section** in `profile/positioning.md`: *What these teams hire to fix*, *Words
  they use*
- **Seniority** from `profile/targets.md`
- **What the recruiter said about the loop**: ask the user, or read the scheduling thread
  (read-only) if Gmail is connected

## Steps

1. **List the rounds.** From the recruiter or the brief. If unknown, use the family's typical loop
   below and mark it "assumed".
2. **Turn the JD into 4 to 6 competencies**, must-haves first, each a verb phrase in the JD's words
   ("ships to a monthly release train", "owns renewals for mid-market accounts").
3. **For each competency write three things:**
   - a behavioral question: "Tell me about a time you <competency>."
   - a craft question in the family's case shape (table below)
   - the follow-up probe an interviewer would ask next ("What was your part?", "What broke?")
4. **Add the core set** below. Every loop asks most of it.
5. **Add 2 to 3 company-specific questions** from the brief: "What would you change about
   <product>?", "How would you approach <a priority they announced>?", "Why us over <competitor>?"
6. **Adjust for seniority.** Senior and lead roles add scope and people questions: setting
   direction, a decision you reversed, hiring, managing up. Early-career roles trade scale for
   learning speed, and school or side projects count as stories.
7. **Rank and cap.** High (named in the JD, or asked in most loops), medium, stretch. Twenty at
   most. Tag each with its round.

## The core set: every role, every loop

**Openers and fit**
- Tell me about yourself. / Walk me through your background.
- Why this company? Why this role? Why now?
- Why are you leaving, or what are you looking for next? (Grep `profile/me.md` *Where I am right
  now* for how the user describes a gap or a departure, and what never to say about it.)
- What are you best at? What's a real weakness?

**Behavioral: have a story ready for each**
- Biggest impact, or the work you're proudest of
- A conflict or disagreement with a peer or manager
- A failure or mistake you owned
- Influencing people you had no authority over
- Ambiguity: a vague goal and no playbook
- Prioritizing when there was too much to do
- Hard feedback you received and what you changed
- A difficult stakeholder or customer

**Closers**
- What questions do you have for us?
- Recruiter screens also cover pay expectations, timeline, other processes, location and work
  authorization. Rehearse these so the answers are short and consistent with the resume.

## Typical loops and case shapes by role family

The craft round nearly always asks for a small version of the work the role does every day. If
the user's family isn't listed, derive its case shape from that.

| Family | Rounds beyond recruiter and behavioral | Craft case shape | Sample prompts |
|---|---|---|---|
| Product management | product sense, metrics, execution, strategy | see `pm-question-bank.md` | see `pm-question-bank.md` |
| Software engineering | coding, system design, project deep dive, debugging or code review | requirements → API and data model → high-level design → bottlenecks → tradeoffs | "Design a rate limiter for a public API." "Walk me through a production incident you owned." "This page takes 6 seconds to load. Find out why." |
| Design (product, UX, visual) | portfolio review, app critique, live design exercise | problem → constraints → options → decision and rationale → outcome → what you'd change | "Walk me through one project, start to finish." "Critique the checkout flow of an app you use." "Help new users find their first useful feature." |
| Data (analytics, science, engineering) | SQL or coding screen, statistics, product analytics case, take-home presentation | question → metric definition → data needed → method → caveats → recommendation | "Signups rose 10% but activation fell. What do you check first?" "Design an A/B test for a new pricing page." "Explain a model you built to a non-technical executive." |
| Marketing (product, growth, brand, content) | positioning or messaging exercise, launch plan, channel and funnel metrics, portfolio or writing sample | audience → insight → message → channels → metrics → budget tradeoffs | "Position our product against the market leader in three sentences." "Launch a feature with no paid budget." "Acquisition cost doubled last quarter. Walk me through it." |
| Sales, account management, customer success | role-play (discovery, demo, objection, negotiation), territory or account plan, deal walk-through | discovery questions → pain → value in the buyer's numbers → next step | "Sell me this product; I'm a skeptical finance lead." "Walk me through a deal you lost." "A top account says it will churn. What do you do this week?" |
| Operations, program management, bizops, strategy | process case, planning or prioritization case, spreadsheet or modeling exercise, cross-team execution | goal → current process → bottleneck → options → rollout → metric | "The support backlog doubled in a month. Diagnose it." "Plan a migration that touches five teams." "Build a quick model: should we open a second warehouse?" |
| Research (UX, market) | study design, method choice, synthesis walk-through | question → method and why → sample → risks to validity → how the findings changed a decision | "How would you learn why trial users don't convert?" "When would you not run a survey?" |
| People manager (any family) | hiring, performance, team building, managing up | situation → your call → how you communicated it → what happened to the person and the team | "Tell me about someone you had to let go." "How do you grow a strong individual contributor who doesn't want to manage?" |

**Live exercises.** Coding, whiteboard and design exercises are best practiced in a real editor or
on a real whiteboard with a timer. This skill runs the talk track around them: the clarifying
questions, narrating tradeoffs out loud, and the project deep dive.
