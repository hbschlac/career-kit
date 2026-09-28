# Building a voice profile from writing samples

The method for turning 3 to 5 of the user's own writing samples into `profile/voice.md`. The
`setup` skill uses it on first run; the voice skill uses it to add rules later. The output is a set
of **checkable rules with short examples**, not a personality description.

---

## 1. Collect the samples

Ask for 3 to 5 pieces the user wrote themselves, without AI help, ideally across registers:

| Want | Why |
|------|-----|
| 1 to 2 professional emails or LinkedIn messages they were happy with | the register outreach will use most |
| 1 longer piece (cover letter, essay, blog post, long doc) | sentence rhythm and structure at length |
| 1 casual message (Slack, text to a colleague) | where rules relax, and how |
| Optional: something they wrote when frustrated or saying no | tone under pressure |

Rules for samples:
- **Their words only.** Skip anything heavily edited by someone else or drafted by an AI.
- **Recent beats old.** Voices change; weight the last year or two.
- **More is better, up to a point.** Past ~8,000 words, extra samples rarely add new rules.
- Store the samples (or excerpts) in `profile/voice.md` under a Samples heading. They stay in
  `profile/`, never in `skills/`.

If the user has no samples, interview them instead: ask how they would open a cold email to a
stranger, sign off to a recruiter, and say no to a meeting. Treat those answers as samples.

## 2. Measure these dimensions

Read every sample and record what you see for each dimension. Count where you can; a rough
percentage beats an adjective.

**A. Core identity**: 3 to 5 lines on what the voice *is* (e.g. "short sentences, plain words",
"context first, then the point", "formal but friendly"). Pull the words they reach for most.

**B. Sentence structure**
- Median sentence length and the spread (short / medium / long shares)
- Recurring rhythms (e.g. one short sentence per paragraph; questions as openers)
- How often sentences start with "I" or "My"; favorite transitions
- Active vs passive share
- Whether the main point comes first or after context
- How they ask for things (direct question vs "I'm wondering if...")

**C. Grammar by register**: when capitalization, contractions and periods relax, and whether the
switch is gradual or binary. Note any consistent micro-habits (e.g. always writing "OK" in caps, or numerals for every number).

**D. Punctuation fingerprint**: dashes (which kind, how often, what for), parentheticals,
colons vs semicolons, exclamation marks (how many per message), ellipses, symbols like "&" for
"and". Cap anything heavy: "max one exclamation mark per email".

**E. Emoji and emoticons**: the complete list they actually use and where; the zones where none
appear (usually cover letters, subject lines, professional body text).

**F. Vocabulary**: plain vs formal defaults ("built" vs "constructed"), top content words,
intensifiers they use and never use ("really" vs "very"), hedges they use and never use.

**G. Tone by situation**: outreach, following up, saying no, apologizing, when excited, when
frustrated. One line each.

**H. Greetings**: each greeting they use and when (stranger, peer, group, close contact).

**I. Sign-offs**: each sign-off and when; the sign-offs they never use.

**J. Signature phrases**: recurring phrasings that are recognizably theirs (a way of asking, a way
of framing a hypothesis, a thread-reviver line). Five to fifteen is typical.

**K. Structure patterns**: email architecture (e.g. greeting → context → ask → thanks), paragraph size,
lists vs prose, how long-form pieces are shaped.

**L. The never list**: see section 4.

## 3. Write rules, not descriptions

Each finding becomes a rule a reviewer can check against a draft.

| Weak (description) | Strong (rule) |
|--------------------|---------------|
| "Writes warmly" | "Open with one line of genuine thanks before the ask in follow-ups." |
| "Likes parentheses" | "Use parentheses for asides; at most one per email." |
| "Casual with friends" | "Level 5 (close friends): emoji allowed, first name only as sign-off." |
| "Uses simple words" | "Prefer 'use', 'help', 'plan' over 'utilize', 'facilitate', 'roadmap'." |

Guidelines:
- **One rule, one example.** Quote a short phrase from the samples as evidence, or a fictional
  illustration if the sample is private.
- **Give numbers where you counted** (sentence length, exclamation cap, share of first-person
  openers). They make the checklist testable.
- **Mark the register** a rule applies to. Many rules flip between professional and casual.
- **Note exceptions explicitly** (e.g. "sign off 'Cheers' with peers, 'Best' with strangers").
- **Do not over-fit.** A habit seen once is a note, not a rule. Promote it after it appears in 2+
  samples or the user confirms it.

## 4. The banned list

A short list of words, phrases and moves the user never uses or has explicitly rejected. It is the
highest-value part of the profile, because it is the easiest to check. Typical entries:

- Sign-offs the user never uses (whatever they are for this user; ask)
- Openers: "Hope this message finds you well", "I hope you're doing well" at the top
- Networking cliches: "pick your brain", "compare notes", "touch base", "circle back"
- Intensifiers and hedges: "very", "extremely", "kind of", "sort of", "perhaps"
- Corporate filler: "leverage", "synergy", "spearheaded", "stakeholders" (unnamed)
- Formatting: emoji in professional email, ALL CAPS for emphasis, scattered exclamation marks

Build it from three sources: words absent from the samples that AI drafts tend to use, words the
user reacts against when shown a draft, and the generic kill list in `skills/aislop/SKILL.md`.
Keep it to the items that actually matter to this user; 10 to 25 is typical.

## 5. Check the profile with the user

Before saving, show a short summary: the 5 strongest rules, the greetings and sign-offs, and the
banned list. Then write one short fictional message using the profile and ask "does this sound
like you?" Adjust from their answer. Save to `profile/voice.md` with sections matching A to L
above plus Samples.

## 6. Keep it current

When the user corrects a draft's voice, add or adjust one rule (with its register and one example)
in `profile/voice.md`. Remove rules the user contradicts. Note the change with a date in a short
changelog at the bottom of the file so later sessions know which rule is newest.
