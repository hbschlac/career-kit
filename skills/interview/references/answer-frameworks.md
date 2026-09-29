# Answer frameworks

Match the structure to the question type, then fill it with one of the user's real stories or
with live reasoning. A framework recited in the abstract scores low; interviewers want the
example, not the scaffolding. Never name the framework out loud ("Using STAR…").

| Question type | Structure |
|---------------|-----------|
| "Tell me about a time…" (any behavioral) | STAR |
| Failure, mistake, weakness | STAR + what changed after; the weakness frame |
| "Tell me about yourself" | Present → throughline → proof → why this |
| "Why us / why this role / why now" | Their problem → your match → why now |
| "How would you measure…" | North Star + supporting metrics |
| "X dropped, walk me through it" | Driver tree |
| "Design / improve a product" | CIRCLES |
| "How do you prioritize…" | 2x2 |
| "How many / how big…" | Estimation |
| "Should we… / where is this going" | First principles |
| A craft round outside product | The family's case shape in `building-a-question-bank.md`, plus *Thinking out loud* below |
| A JD requirement the user lacks | Honest bridge |

---

## STAR: behavioral questions

1. **Situation:** the context in one or two sentences. Only what the listener needs.
2. **Task:** the user's own responsibility or goal.
3. **Action:** what the user did, specifically. The longest part. "I", not "we".
4. **Result:** the outcome, with a number from the ledger or a concrete change. Then, in one
   line, what it meant for the team or the business.

Rough split: Situation and Task 20%, Action 60%, Result 20%. About two minutes spoken (250 to 300
words).

Common mistakes:
- A long Situation. The interviewer doesn't need the whole backstory.
- "We" all through the Action, so the user's part is invisible.
- No Result, or a vague one ("it went well").
- A "the team won" story instead of an "I did X" story.

## Failures and weaknesses

- **Failure:** a real one with stakes, not a disguised success. STAR, then add what the user
  changed afterwards and the evidence it stuck. Own it without blaming others.
- **Weakness:** real, relevant but not disqualifying for this role, what the user does about it,
  and a sign it's improving. "I'm a perfectionist" loses points.

## "Tell me about yourself"

60 to 90 seconds. A conversation starter, not a resume read-out.

1. **Present:** who the user is now, in one line. Start from the family's *Why me* line in
   `profile/positioning.md`.
2. **Throughline:** what connects the past roles. One sentence, not a tour.
3. **Proof:** the *Lead with* story in one or two sentences, with its number.
4. **Why this:** why this role at this company, now. One specific sentence.

Practice it out loud; it sets the tone for everything after.

## "Why us / why this role / why now"

1. **Their problem:** what this team is trying to do, from the JD or the brief, in their words.
2. **Your match:** the thing the user has already done that answers it, with one number.
3. **Why now:** a true, specific reason: a launch, a stage the company is at, a turn in the user's
   own path. No generic praise ("I love your mission").

## North Star: "How would you measure success?"

1. **The value exchange:** what value does the product deliver, and to whom?
2. **The moment of value:** the user action that shows value was received. Not an input, not
   activity for its own sake.
3. **The North Star:** one metric that counts that moment at scale.
4. **Two or three supporting metrics:** a leading indicator, a quality measure, and a guardrail.

Example, a team chat app: value is getting work unblocked through a conversation; the North Star
could be weekly active teams where at least three people send messages; supporting metrics are
time to first reply, the 4-week retention of new teams, and a guardrail on notification opt-outs.

Always name a counter-metric so the main one can't be gamed (engagement bought at the cost of
trust is a loss).

## Driver tree: "The metric dropped. Walk me through it."

1. **Clarify** the metric, how it's calculated, and when the drop started.
2. **Rule out the boring causes:** a tracking change, a holiday, a data pipeline delay.
3. **Segment to isolate:** platform, app version, new vs. returning users, region, traffic source,
   product area.
4. **Build the driver tree:** the inputs that make up the metric (visitors × click-through ×
   add-to-cart × checkout).
5. **Form a hypothesis** from where the segmentation points. "Only the newest app version:
   probably the release."
6. **Say what data you'd pull and who you'd talk to, then a fix direction.**

Isolate before diagnosing; a theory stated before segmenting is the most common miss.

## CIRCLES: "Design / improve a product"

1. **Clarify:** one or two questions about the user, the goal and the constraints.
2. **Identify the customer:** one specific user, not "everyone".
3. **Report their needs:** the jobs they're trying to get done, and where it hurts.
4. **Cut through prioritization:** which need matters most, and why.
5. **List solutions:** at least three before committing to one.
6. **Evaluate tradeoffs:** risks of the top option, and what it gives up.
7. **Summarize:** the pick and the reason, in two sentences.

Don't skip step 5. Interviewers want breadth before depth.

## 2x2: "How do you prioritize?"

1. List the options.
2. Pick the two axes that matter for this context: impact vs. effort, user value vs. strategic
   value, or revenue vs. user trust.
3. Place each option, recommend the top-right, and say why the others lose.

Impact vs. effort alone is the common trap; show strategic fit too.

## Estimation: "How many / how big?"

1. **Clarify** the scope: region, time period, paying users only?
2. **Choose top-down or bottom-up** and say why.
3. **Segment** the population into groups that behave differently.
4. **Estimate each segment** with round numbers, stating assumptions out loud.
5. **Add up, then sanity-check** against something known.

Example, rideshare trips per day in a city of one million: 25% of residents use rideshare (250k);
each averages one trip a week (about 36k trips a day); visitors and business travel add about a
quarter (about 45k). Check: at $18 a trip that's about $800k a day, plausible for a city that size.

## First principles: "Should we…?" / "Where is this going?"

1. **Strip the question down** to what's really being asked: moat, timing, or where to spend.
2. **State assumptions.**
3. **Reason from what's true** about users, costs and technology.
4. **Commit to a point of view,** not a list of considerations.
5. **Name what would prove you wrong.**

## Thinking out loud: any case, design or technical round

- Ask one or two clarifying questions before solving. Then say your assumptions.
- Give the structure before the detail: "I'll look at three things: …"
- Pick and commit. A defended choice beats a list of options.
- Name the risk or tradeoff of your choice before they ask.
- End with a two-sentence summary.
- "I don't know" is fine when followed by how you'd reason about it or find out.

## Honest bridge: a requirement the user lacks

Never stretch a claim to cover a gap. Name it and bridge to the closest real thing:

> "I haven't <done X> directly. The closest is <Y>, where I <specific action> and <result>. The
> part that carries over is <skill>."

Check the family's *Downplay* line and `profile/me.md` *Never say* before writing any bridge.
