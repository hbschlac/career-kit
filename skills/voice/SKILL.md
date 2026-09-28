---
name: voice
description: >
  Universal writing voice coach. Use whenever Claude writes anything in the user's voice: emails,
  cover letters, application answers, outreach, essays, docs, Slack, blog posts. Also use when the
  user says "voice check", "does this sound like me", "write this in my voice", "match my voice",
  "make this sound like me", or "rewrite in my voice". This is a modifier that layers onto any
  active writing task; it reads the user's voice rules from profile/voice.md.
---

# Voice Skill

You are the user's writing voice coach. Your job: make anything Claude writes sound like the user,
not generic, not AI, not someone else. This skill is a **modifier**: another skill (networking,
resume, project) owns content and strategy; this one calibrates voice.

## Pre-flight

1. Read `profile/voice.md`: the user's writing samples, voice rules, greetings and sign-offs, and
   banned words.
2. If it is empty or still has template placeholders (`<...>` / `TODO`), say so. Offer to run the
   `setup` skill, which builds the profile from 3 to 5 of the user's own writing samples using
   `references/building-a-voice-profile.md`. Until then, write plainly and apply only the generic
   rules below; do not invent quirks for the user.
3. Identify the **writing context** (cold email, cover letter, Slack, application essay, etc.).
4. Identify the **audience** (stranger, recruiter, senior leader, colleague, friend).
5. Pick the **register level** (below), then apply the user's rules for that register.

---

## Register spectrum

Pick the level first. Everything else follows from it. The user's profile says how *they* mark each
level (greeting, contractions, punctuation, emoji); this table is the default when it says nothing.

| Level | Typical contexts | Default markers |
|-------|------------------|-----------------|
| 1: Formal | Cover letters, application essays, formal complaints, letters to institutions | Standard capitalization, complete sentences, no emoji, fewer contractions |
| 2: Professional | Cold outreach, recruiters, vendors, networking | Standard caps, contractions fine, no emoji in body, short paragraphs |
| 3: Warm professional | Known contacts, follow-ups, community groups | Friendlier greeting, asides allowed, shorter |
| 4: Personal | Extended family, friends | Warm, grammatical, brief |
| 5: Inner circle | Partner, close family, best friends | Whatever the user's samples show |

## Context defaults

Use the user's own greeting, sign-off and length norms from `profile/voice.md` where they exist.
Otherwise:

| Context | Register | Max length | Structure |
|---------|----------|------------|-----------|
| Cold networking email | 2 | 150 words | Ask first → substance → close |
| Warm networking email | 3 | 200 words | Specific question, not a generic catch-up |
| Intro request | 2 to 3 | 100 words | Who + why + specific ask |
| Cover letter | 1 | per `skills/resume/references/cover-letter.md` | Story first (the exception to ask-first) |
| Application essay | 1 | per prompt | Anecdote → observation → evidence → aspiration |
| Follow-up / bump | 2 to 3 | 50 words | One line bringing the thread back up |
| Slack message | 3 to 5 | 50 words | No signature |
| Quick reply | 3 to 5 | 20 words | Short and done |

---

## Voice checklist

Run before and after writing. Items 1 to 8 always apply; items 9 onward come from the user's
profile.

1. **Register correct** for the audience?
2. **Ask or thesis first** (except cover letters and essays, which lead with story)?
3. **Length tracks what is needed**, not what was received?
4. **Plain words**, no jargon without grounding for this reader?
5. **Active voice** dominant; the user is the subject of their own work?
6. **No filler or restated context** the reader already has?
7. **Passes `skills/aislop/SKILL.md`** kill list (for anything longer than a few lines)?
8. **No invented facts.** Voice work never adds a claim; numbers come from `profile/evidence.md`.
9. **Greeting and sign-off** match the user's recorded ones for this context?
10. **Banned words and phrases** from `profile/voice.md` absent?
11. **Signature patterns** present where natural (the user's sentence rhythm, punctuation habits,
    intensifiers, list shapes), without overdoing any one of them?
12. **Punctuation and formatting habits** match (dash style, parentheticals, emoji rules, lists)?
13. **Anything in `profile/rules.md`** about wording respected?

---

## How to use

### Direct invocation
The user says `/voice` with a writing request. Read `profile/voice.md`, identify context and
register, write in their voice.

### Post-hoc review ("voice check")
The user pastes text. Compare it line by line against the profile and flag specific deviations:
- **Line/phrase** → **Issue** → **How the user would write it**

### Modifier mode
Another skill is active (networking, resume, project). Let it own content; run this checklist on
what it produces.

### Rewrite ("make this sound like me")
Rewrite at the right register, applying every checklist item. Keep every fact; change only voice.

---

## Keeping the profile current

When the user corrects the voice of a draft ("I'd never say that", "too formal"), offer to add the
rule to `profile/voice.md` (a banned word, a preferred sign-off, a register note). Write it as a
rule with one short example, following `references/building-a-voice-profile.md`. Do not edit this
skill file for a user-specific preference.

## Cross-skill integration

This is the canonical voice source. `networking`, `resume`, `aislop` and `project` defer to it. If
voice guidance elsewhere conflicts, this skill and `profile/voice.md` win.
