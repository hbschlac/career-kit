# Company research brief

The goal is one screen the user can read in two minutes before walking in. It answers five
things: what the company sells and to whom, what changed recently, what this team owns, how they
interview, and which of the user's stories fits their problem. Skip history and trivia; keep only
what changes an answer.

## Sources, in this order

1. **The JD.** Tracker column B through `skills/job-fetch/SKILL.md` (or `skills/linkedin-jobs/`),
   or pasted by the user. Pull out what the team owns, the must-haves, and the words it repeats.
   Those words go into answers.
2. **The company's own pages.** Product, pricing, customers or case studies, blog, changelog or
   release notes, the about or leadership page, and the careers page: other open roles show where
   they are investing.
3. **The last 12 months of news.** Launches, funding, acquisitions, layoffs, leadership changes.
   For a public company, the latest earnings call or annual report: the priorities leadership
   named out loud.
4. **The interview process.** Review sites and forums (Glassdoor, Levels.fyi, Blind, Reddit).
   These are secondhand and often stale: label them "reported" and turn each into a question for
   the recruiter.
5. **The interviewers, if named.** Public professional work only: role, team, talks, posts,
   published writing. The point is to learn what they care about. Nothing personal, and never
   bring up anything that isn't both professional and public.
6. **The user's own history with the company.** The tracker row (Log, Notes),
   `grep -n -i "<company>" profile/contacts.md` for a warm contact, and
   `grep -n -i "<company>" profile/positioning.md` for what was pitched before.

Searches that tend to work:

- `"<Company>" launches OR announces <product or team>` (last year)
- `"<Company>" raises OR funding OR acquires`
- `"<Company>" <role title> interview process` (then check review sites)
- `"<Company>" engineering blog` / `"<Company>" changelog`
- `"<Interviewer name>" "<Company>" talk OR podcast OR post`

The sandbox proxy blocks some hosts (403). Use search snippets, route job postings through
`job-fetch`, or ask the user to paste the page. Don't retry a host that already refused.

## Rules

- **Date and source every fact that can change:** "Series C (press release, March)", "about 400
  people (company careers page, June)". Older than six months: hedge it in answers.
- **Unknown stays unknown.** Never fill in a number, a headcount, or a round format.
- **Recent and sensitive news** (layoffs, a failed launch, a lawsuit) goes under *Watch out for*,
  so the user can handle it with care, not raise it by accident.

## Brief template

```
## <Company>: interview brief (<role>, <round>, <date>)

What they do: <1–2 sentences: product, customer, how they make money>
Stage and scale: <public or funding stage, headcount, revenue if public; each with source and month>
Recent moves: <2–4 dated items>
What this team owns: <the problem this hire fixes, in the JD's words>
Words they use: <5–8 terms from the JD and their site to mirror>
How they interview (reported, confirm with the recruiter): <rounds, formats, known case prompts>
Interviewers: <name, role, one professional hook each>, or "not shared yet"

Your angle: <the family's "why me" line from profile/positioning.md, tuned to this team's problem>
Likely themes: <3–4, each tied to a JD line or a recent move>
Watch out for: <a JD must-have the user lacks, with its honest bridge; sensitive recent news>

Questions to ask them: <3, from the list below, made specific>
Ask the recruiter: <what is still unknown about the loop>
```

## Questions to ask them

Pick three and make each specific. A question that names a real launch or a JD line beats a
generic one; a question the website already answers costs points.

- **The work:** "What does success look like for this role at six months? What would tell you the
  hire wasn't working?"
- **The problem:** "The posting mentions <X>. What's the hardest part of that right now?"
- **How decisions get made:** "When <function A> and <function B> disagree on priorities, how does
  it get resolved?"
- **Recent change:** "Since <launch or reorg>, what has changed about how the team works?"
- **For the interviewer:** "What's something you've changed your mind about since joining?"
- **Closing, with the hiring manager or final round:** "Is there anything in my background you'd
  want me to address before you decide?"

Avoid perks and pay before the offer stage (unless the recruiter raises it), and anything that
assumes a problem you can't see from outside.

## Questions for the recruiter

Confirming the loop is free and most candidates skip it.

- How many rounds, what format each, and who is on the panel?
- Is there a case, take-home, presentation or live exercise? What does the prompt look like, how
  long is it, and can I use my own tools?
- What does the team most want to see in this round?
- What's the timeline to a decision?
