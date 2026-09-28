# Gate 3 — Score twice

Run `recruiter-filter` (`skills/recruiter-filter/SKILL.md`) exactly twice:

1. **Baseline**: on the current doc's plaintext, before any swap.
2. **Final**: on the swap list applied to that plaintext, after Gate 2.

Its own *score freeze* rule is the law here: a rubric re-run after every edit produces
movement that is noise, and the user loses track of their own number.

- Re-score only when **new evidence lands on the page**: a fact the user supplied that wasn't
  there.
- **Never re-score after a rewording.** Rewording does not move the score; reporting that it does
  is noise dressed as progress.
- State the number once. If the remaining gaps are structural (seniority band, recency, a hard
  requirement the user doesn't meet), say so and stop. Points that can only be moved by a lie are
  not a fix list.

**Tagline check (part of the final, not a re-score):** read the tagline against rule 8 of
`SKILL.md` and print `(a) match ✓/✗ (b) metric ✓/✗ (c) why you ✓/✗`. Any ✗ → fix the tagline from
the ledger before Gate 4. A tagline with no number, or one that could head any company's resume,
does not ship.

Output of this gate: the final swap list, unchanged unless the score found a *content* gap that
the ledger can fill. If it can't, the gap goes to the user, not into a bullet.
