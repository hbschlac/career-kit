# Gate 0 — Facts, before a single bullet is written

**This gate is blocking.** Nothing below it runs until the JD is parsed, the ledger is grepped per
requirement, and the remaining gaps have gone to the user in ONE message.

**Get the JD first.** If it is not in the conversation, ask for it; never tailor from a doc title.
A job-posting URL goes through the `job-fetch` skill; a LinkedIn job URL through `linkedin-jobs`.

## Start from the closest past version

Tailoring the same kind of role from scratch twice wastes a session. Right after parsing the JD,
check what the user already has:

1. `grep -i -E "<company>|<role family>|<top theme>|<top theme>" profile/tailored.md`. That's the
   registry: one line per tailored resume, newest last. If it has no rows yet, search
   `cv_folder_id` in Drive for titles with the company or role instead.
2. **Same company and role, or the same job reposted** → offer it as is: "You made a resume for
   this exact job on <date>. Reuse it (I'll make a fresh copy), or tailor again?"
3. **Close match** (same role family, and at least half of this JD's top themes appear in its
   themes column) → offer it as the starting point: "Your <Company> <Role> version (<date>,
   scored <n>) already covers <themes>. Start from it instead of your main resume?" The swap list
   then covers only what this JD needs differently.
4. **The user names one** ("use the one I made for Acme") → find it in the registry by company.
5. Ask this in Gate 0's one batched message, never in a turn of its own. If they don't mind, use
   the closest match, else `base_cv_doc_id`.

A past version is final: never edit it. Gate 4 copies it like any base, and its claims still go
through the ledger grep like any other fact.

**Grep, don't read.** The ledger (`profile/evidence.md`) and the story bank (`profile/me.md`) grow
long and are never read whole. Per JD requirement:

```
bash skills/resume/scripts/ledger_grep.sh security "threat model" compliance   # any terms
```

It prints each matching entry with its heading context from `profile/evidence.md`,
`profile/me.md`, `profile/resume.md` and `profile/voice.md`, at a few dozen tokens a hit. Search
the JD's nouns **and their synonyms** before deciding a gap exists. Never tell the user something
"has never been on a resume" or "isn't in your background" until the grep has run on every
synonym you can think of.

Running it also **records Gate 0** for the guard hook (`$CV_GUARD_DIR/facts-grepped`, default
`~/.claude/cv-guard/facts-grepped`): if the hook is installed, the session's first resume write is
refused until a grep has run. That is the enforcement, not a reminder.

## Gather the evidence BEFORE you write (blocking)

Most wasted resume sessions are sequencing failures, not writing failures: facts the user had but
Claude did not arrive *after* a bullet was written, scored, exported and reviewed, so every one
triggers a full rewrite cycle. Discovery must precede production. In order:

1. **Parse the JD into its requirement list.** Write down the 2–3 themes the role cares about most
   before touching anything.
2. **Grep the ledger for each requirement** (and synonyms). What you find is evidence you already
   have; use it without asking.
3. **Never declare a gap unfixable before grepping.** "This gap can't be closed without
   fabricating" is often wrong: the user did adjacent work that is recorded under a different noun.
4. **Cross-check all available material, not just the base resume.** The base resume is a
   one-page snapshot, not the full record. `profile/me.md` (story bank) and `profile/evidence.md`
   hold work that may have been cut from the base and is exactly what this role wants.
5. **Read project-specific source docs before any technical claim.** When the user points to a
   spec, impact doc or README for a project, read it before writing numbers, dimensions or scope.
   A number written from memory is how close-but-wrong claims ship.
6. **Batch every remaining gap into ONE message.** Not one question per turn.
7. **Append the user's answers to `profile/evidence.md` in the same turn**, with source ("user,
   this session") and any hedge they gave, before writing the bullet. Not at the end of the
   session; sessions run out of context and the end never comes.

## Corrections are facts too; record them in the same turn

When the user corrects a fact mid-session ("that was 38, not 45", "I led it, I didn't support
it"), fix `profile/evidence.md` in the same turn, before replying. When they correct wording or a
rule ("don't say leveraged", "never call it X"), note it for `resume-learn`, which routes it to
`profile/rules.md` or `profile/voice.md` at the end of the session. Same-turn is the point: a
correction "to be captured at the end" is a correction lost.
