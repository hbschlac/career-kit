# Defining Your Search Targets

The user's actual targets live in **`profile/targets.md`**. This file is the guide to what a good
targets file contains, and the filters every search applies to it. Skills read targets from
`profile/targets.md` only; if it is missing or still has placeholders, say so and offer the
`setup` skill rather than guessing.

---

## What goes in `profile/targets.md`

A sharp targets file makes every Boolean string, X-Ray and scout better. Fill in each section; a
line or two each is enough.

### 1. Candidate snapshot
- **Function and level:** e.g. "Senior Software Engineer, backend", "Product Designer, mid-level",
  "Marketing Manager, lifecycle", "Senior PM", "Operations Manager"
- **Years of relevant experience**, and any adjacent experience that can count as "equivalent"
  (consulting, founding, a neighbouring function, a graduate degree)
- **Key qualifications** — the 5-8 skills that most roles in the search will ask for
- **Differentiator** — the one thing that sets them apart (a shipped side project, a domain, a
  scale of system)
- Point to `profile/resume.md` for the detail; don't copy it here

### 2. Target roles (titles)
List every title the role goes by — companies name the same job differently. Examples:
- Product: Product Manager, Senior Product Manager, Staff PM, Product Lead, Group PM
- Software engineering: Software Engineer, Senior Software Engineer, Backend Engineer, Full-Stack Engineer, Staff Engineer
- Design: Product Designer, Senior Product Designer, UX Designer, Design Lead
- Marketing: Product Marketing Manager, Growth Marketing Manager, Lifecycle Marketing Manager
- Operations: Operations Manager, Business Operations, Strategy & Operations, Program Manager

### 3. Target industries / verticals
3-6 verticals, most wanted first (e.g. developer tools, fintech, healthcare, climate, consumer, B2B SaaS).

### 4. Target company profile
- **Stage:** e.g. Seed-Series A, Series B through post-IPO, public
- **Size:** employee range and sweet spot
- **Location:** which offices qualify and which don't (see the Location Filter below) — be concrete
  about cities, not just "Bay Area" or "NYC area"
- **Remote:** remote OK / hybrid OK / on-site only
- **Comp floor:** base and/or total, if they have one
- **Culture signals:** what "good team" looks like to them

### 5. Active target companies
A short list the user is actively pursuing. Always `find()` these in Pipeline before searching —
some may already be tracked.

### 6. Experience rule
The maximum "years required" they qualify for, and which "or equivalent" phrasings count for them
(see the Experience Filter below).

### 7. Exclusions
- **Too junior** / **too senior** titles
- **Wrong domain** — areas they don't want (e.g. ads, crypto, defense)
- **Wrong role type** — neighbouring functions that pollute results
- **Visa / clearance** constraints, if any

### 8. What energizes them / what they're not pursuing
Plain-language lists used to score fit: the kind of work that lights them up, and the kind they'd
turn down even at a great company.

---

## Location Filter — apply to every search

**Read the JD body, not the job board's location field.** A card often shows one city while the
posting lists several offices or a remote option.

| JD body says | Verdict |
|---|---|
| One of the user's allowed offices is listed | **Qualifies** |
| Remote in the user's country ("or remote", "remotely in the United States", "open to remote candidates") and the user accepts remote | **Qualifies** |
| Only offices the user excluded | **Out**, even for a great role |
| Only other cities, with no allowed office or remote option | **Out** |
| No location in the body | Fall back to the card |

- Pay-by-location tables count as offices ("For <City>-based roles: $X" means that city is allowed).
- Boilerplate doesn't count: "remote roles are not eligible for visa sponsorship", a city's fair-chance
  ordinance, "we have distributed teams" say nothing about this role.
- "Other locations may be considered" is too weak to count. Treat the role as the named office.

## Experience Filter — apply to every search

Read the years-of-experience line in the **full JD**, not the title. Titles are unreliable: a
"Staff" role may ask for 4+ years and a "Senior" role for 8+.

Let `N` be the maximum years the user qualifies for (from `profile/targets.md`).

| JD says | Verdict |
|---------|---------|
| **≤ N years** required | **Qualifies** |
| **> N years, but with an "or equivalent" path**: "or equivalent", "or related technical role", "or related area", "or relevant experience (e.g. founder, engineer)", "X years of industry experience, including Y in <function>" (Y ≤ N) | **Qualifies. Rank these first** when the user's adjacent experience counts as the equivalent |
| **> N years in the function, full stop** | **Out.** Don't surface it |
| No number stated | Show separately as "unstated". Worth a look |

- Use the **hard requirement**, not a "preferred" line. A range counts by its low end ("5-10 years" → 5).
- "Degree or equivalent experience... with 8+ years in the role": the "equivalent" there is about
  the **degree**, so it doesn't rescue the years requirement.
- Multi-option JDs ("Option 1 / Option 2"): qualifies if any option does.
- Far below the user's level (e.g. < 3 years for a senior candidate): still qualifies, but flag it as
  possibly too junior and check level and comp.
- Ignore numbers that aren't about the candidate ("25+ years in business", "3/5 year planning").

Tooling: `linkedin_search_jobs` → `linkedin_get_job` for every hit, regex the years line, then
**read the quoted lines yourself** before trusting the verdict. A regex misses spelled-out numbers
("Five to ten years") and "or related area" phrasing.

## Seniority signals (include)
- Level words that match the user: e.g. senior, staff, lead, principal
- Level codes where companies use them (L4-L6, IC4-IC6, E5)
- "N+ years" counts at or below the user's maximum, or any count with an "or equivalent" path

## Exclusion keyword starter set
Adapt to the user's level and function:
- **Too junior:** intern, internship, new grad, entry level, junior, associate, trainee, apprentice, early career, university recruiting, campus recruiting
- **Too senior:** VP, director, head of, chief (unless the user targets these)
- **Wrong domain / role type:** whatever `profile/targets.md` lists
