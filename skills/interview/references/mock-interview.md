# Mock interview

A live practice round: Claude plays the interviewer, then switches to coach after each answer.
This is the highest-value mode; offer it early.

## Set up (one message)

- **The frame:** company, role, round, and interviewer persona (recruiter, hiring manager, peer,
  executive, or a panel). If the user doesn't say, default to the hiring manager in a mixed round.
- **The questions:** 3 to 5. Order: a warm-up opener → the round's core question → a behavioral →
  one on a JD must-have → an optional curveball. Take them from Mode 3's list if it ran; otherwise
  pick from `building-a-question-bank.md` (or `pm-question-bank.md` for product roles).
- **How to answer:** as they would out loud. Typing is fine; a pasted voice transcript is better.
  They can say "hint", "skip", or "stop" at any time.
- **The rubric:** state it once, in its short form (below). Don't repeat it mid-round.

## Rules

- **One question per turn.** The turn holds the question and nothing else (in a panel, also who
  is asking). No preamble, no tips.
- **Wait for the answer.** Never answer it first. Hints only when asked.
- **Stay in character for one follow-up** when the answer leaves an obvious hole ("What was your
  part, specifically?", "How did you know it worked?"). One probe per question, then switch to
  coach.
- **Coach with the format below**, quoting the user's words.
- **Offer a retry** ("Retry, or next question?"). Score the retry too, and name what changed.
- **Calibrate.** Scoring 3 or more on everything: raise the difficulty with sharper probes or a
  curveball. Stuck at 1 to 2: slow down; have them outline first, then answer.
- **Check every number they say.** After the feedback, grep the ledger for it. Not there: ask if
  it's accurate and, once confirmed, append it to `profile/evidence.md`
  (`source: user, <YYYY-MM-DD>, said in mock`). It contradicts the ledger: ask which is right and
  fix the ledger. Interviewers compare what you say against the resume.

## The rubric

Score each answer 1 to 4 on five dimensions, plus one for the round's craft when the question is a
case, technical, portfolio or role-play question.

| Dimension | What a 3 looks like |
|-----------|---------------------|
| **Answered it** | Addresses the question actually asked, in the first two sentences |
| **Structure** | A listener could retell it: clear start, middle and end |
| **Specific and owned** | One concrete example; "I" for the user's part; their role is clear |
| **Result** | An outcome with a number or a concrete change; for a failure, what changed after |
| **Length** | Behavioral about 2 minutes spoken (250–300 words); openers 60–90 seconds; short setup |
| **Craft** (when it applies) | Case: clarifies, structures, decides, names tradeoffs. Technical: requirements and tradeoffs stated. Portfolio: a reason for each decision. Role-play: asks before pitching. Recruiter screen: crisp and consistent with the resume |

Scale:
- **1: hurts.** Off the question, no example, or a claim they couldn't back up.
- **2: forgettable.** An example, but their role is vague or the result is missing.
- **3: strong.** Specific, owned, a real result, on time.
- **4: memorable.** A 3, plus an insight or tradeoff that fits this company's problem.

Overall is the average, rounded to the nearest half.

Short form to state at setup:

> I'll score each answer 1–4 on: answered the question, structure, specific and owned, result, and
> length (plus craft on case questions). 3 is strong; 4 is one they'd remember.

## Feedback after each answer

```
Score: 2.5/4 (answered 3 · structure 3 · owned 2 · result 2 · length 3)
What worked: <1–2 concrete things, quoting them>
Cut: <what to remove: long setup, hedges, "we", filler>
Add: <what's missing: their specific action, the number, the so-what>
Reframe (only when the angle is wrong): <a better story or angle from the cheat sheet>
```

Then: "Retry, or next question?"

## Delivery tells to call out

- **Hedging:** "I think", "maybe", "kind of", "sort of", "I guess"
- **Hiding the actor:** "we" where the interviewer needs "I"; passive voice ("it was decided")
- **No outcome:** the story ends at the action
- **Filler:** "drove alignment", "moved the needle", "synergies", "best-in-class", and anything on
  the kill list in `skills/aislop/SKILL.md`
- **Vague scope:** "worked on", "helped with", "was involved in" → owned, led, built, decided
- **Abstract impact:** "drove impact" → on what, and how much?
- **Long setup:** the situation runs past a fifth of the answer
- **The wrong question:** a prepared story that answers something else
- **Resume recital:** walking the roles in order instead of choosing
- **Numbers that don't match** the resume or the ledger

## Debrief (after 3 to 5 questions, or on "stop")

```
## Mock debrief: <Company>, <round> (<date>)

Scores: Q1 <n> · Q2 <n> · Q3 <n> · … → average <n>/4
Patterns: + <recurring strength>   − <recurring gap>
The one thing to fix before the real interview: <the single most important note>
Stories that landed: <story → question type, and why>
Stories that fell flat: <story → question type, and what to try instead>
Next: <retry the weakest / practice another round type / ready>
```

Say "that answer is ready" only when it scores 3 or more on every dimension.

## Write back after the debrief

- **`profile/positioning.md`:** one Log line per story with a clear signal (scored 4, or 2 and
  below), three at most, under the family's `- Log` list:
  `  - <YYYY-MM-DD> mock (<Company>, <round>): <question type> → <story>; <n>/4, <landed / fell flat: why in under 10 words>; outcome: practice`.
  The `practice` outcome tells `career-review` this is not an application result.
- **`profile/evidence.md`:** any number confirmed during the round, the same turn.
- **Tell the user** what you wrote, one line each.
- **Tracker:** only if the user asks (`<M/D> - mock for HM round, avg 3/4`).
