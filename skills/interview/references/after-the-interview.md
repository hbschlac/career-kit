# After a real interview: debrief, write-backs, thank-you notes

Do this the same day. The exact questions fade within hours, and they are the best prep for the
next round.

## 1. Debrief: one numbered message

Ask all of these at once; short answers are fine.

1. Which round, with whom (names and roles), and how long?
2. What did they ask, as close to their words as you remember?
3. Which story or approach did you use for each?
4. What felt strong? Where did you stumble or run long?
5. What did they tell you about the team, its problems or its priorities?
6. What next steps and timeline did they give?
7. Did you promise anything: a work sample, references, a follow-up?
8. Did you mention any number or fact about your work that you haven't told me before?

If Gmail is connected, first read the scheduling thread (read-only) for names, roles and next
steps, and ask only for what it doesn't say.

If the user pastes feedback from the company (a recruiter's notes, reasons for a rejection),
record it as given. It's data, not something to argue with.

## 2. The debrief

```
## Debrief: <Company>, <round> (<date>)

Went well: <1–3, specific>
Fix before the next round: <1–2, each with the better story or structure>
What they care about: <from answer 5; feeds the thank-you note and the next round>
Likely next round: <what comes next and what it will probe, given what came up>
Promised: <each follow-up, with a date>
```

## 3. Write-backs, in the same turn

- **Tracker** (SKILL.md Mode 7):
  `print(log(N, "<M/D> - <round> with <interviewer role>: <how it went / next step>", status="Interviewing"))`.
  Put any promise in the same line ("sending work sample by 10/20").
- **`profile/positioning.md`:** one Log line per story the user flagged as landing or falling flat
  (four at most), under the family's `- Log` list:
  `  - <YYYY-MM-DD> <Company, Role> interview, <round>: <question type> → <story>; <landed / flat>; outcome: pending`.
  `career-review` fills in `pending` when the next outcome arrives.
- **`profile/evidence.md`:** each new fact from answer 8, with
  `(source: user, <YYYY-MM-DD>, said in interview)`. If a number they said contradicts the ledger,
  ask which is right and fix the ledger now; the next round may probe it.
- **Patterns:** if the same story has fallen flat twice for a question type in this family, or
  landed three times, propose changing the family's *Lead with* or *Downplay* line. Show the
  change and write it only when the user agrees: those lines also drive the resume tagline and
  outreach.
- **Coaching rules the user states** ("never open with my degree") are for `resume-learn` at the
  end of the session, which puts them in `profile/rules.md`.

## 4. Thank-you notes

One per interviewer, drafted in the chat. The user sends them. Never send, and never create a
Gmail draft.

- **When:** the same day or the next morning.
- **Length:** 3 to 5 sentences, under 120 words. Readable on a phone.
- **Structure:**
  1. Thanks, naming the topic or round, not just "your time".
  2. One specific thing from the conversation, in the interviewer's words (debrief answer 5).
  3. One line tying it to the user's matching experience, with a fact from the ledger. Or, instead,
     a short fix for a weak answer: "I undersold the rollout: onboarding went from ten days to
     three." One of these, not both.
  4. A forward close: looking forward to next steps, or the promised item and when it's coming.
- **Don't:** add any claim that isn't in the ledger, re-pitch the whole resume, flatter, or open
  with "I hope this finds you well".
- **Each interviewer gets a different note.** They compare.
- **Voice:** run `skills/voice/SKILL.md` (professional or warm-professional register), then the
  quick kill list in `skills/aislop/SKILL.md`. Use the sign-off from `profile/voice.md`.
- **Delivery:** email if the user has the address (reply on the scheduling thread when there is
  one, and give them a subject line); otherwise ask the recruiter to pass it on, or send a
  LinkedIn message.

Example (fictional names and numbers):

> **Subject:** Thanks for today's conversation on onboarding
>
> Hi Jordan, thank you for walking me through the onboarding redesign today. Your point that most
> new accounts stall at the data-import step stuck with me. It's the same drop-off I worked on in
> my last role, where moving import into the first session cut setup time from ten days to three.
> I'm looking forward to the next steps.
>
> <sign-off from profile/voice.md>

## 5. Waiting and following up

- **No word two business days after the date they gave:** a short check-in. Hand it to
  `skills/networking/SKILL.md` (follow-up), which reads the thread first.
- **A rejection after an interview** is not a resume problem, so don't reopen the CV. Log it only
  when the user tells you, in their word (`status="Rejected"`). Offer a two-line reply that thanks
  them and asks for one piece of feedback, and update the positioning Log line's outcome.
- **Next round:** start its prep from this debrief: the questions they asked, what they care
  about, and the fix list.
