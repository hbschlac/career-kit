---
name: job-search
description: >
  Job search skill. Use whenever the user wants to find job openings, discover which companies are hiring, scan career pages, find growing companies, identify hiring managers, build Boolean search strings, or anything else about finding new opportunities. Trigger on: "find roles", "what's open", "who's hiring", "x-ray", "scan Greenhouse", "companies that raised", "who just fundraised", "growing companies", "find people at", "Boolean search", "job search", "LinkedIn tricks", "set up alerts", "niche job boards", "add to tracker", or any natural language about finding opportunities or companies to target. Works for any role (product, engineering, design, marketing, operations, sales...). A sub-skill of networking.
---

# Job Search Skill

Finds job openings, growing companies, and people to reach out to, without the user having to remember any search syntax. They say what they want in plain language; the skill does the rest.

**A sub-skill of networking.** It feeds into:
- **Pipeline sheet** (`skills/networking/references/pipeline.md`) — add discovered opportunities
- **networking** (`skills/networking/SKILL.md`) — hand off contacts for outreach drafting
- **resume** (`skills/resume/SKILL.md`) — tailoring for strong matches

---

## Before You Start

**Always read first:** `profile/targets.md` — the user's target roles, seniority, years of experience, industries, locations, comp, company criteria, exclusions, and active target companies. Every Boolean string, X-Ray query and scout filter pulls from it.

If `profile/targets.md` is missing, empty, or still has template placeholders (`<...>` / "TODO"), say so, and offer to run the `setup` skill (`skills/setup/SKILL.md`). `references/target-criteria.md` explains what a good targets file contains. Never guess the user's targets; if they want to search right now, ask for the three things that matter most (role titles, location / remote, years of experience) and use only those.

Then read what the task needs:

- **Searches / Boolean strings:** `references/boolean-templates.md` — platform templates and syntax rules
- **To actually run a LinkedIn Jobs search** (not just build the string): the **linkedin-jobs** skill / `linkedin_search_jobs` MCP tool returns real postings you can pull and track — `skills/linkedin-jobs/SKILL.md`
- **X-Ray / platform tricks / alerts:** `references/platform-guide.md` — ATS URLs, LinkedIn URL filters, top sites, automation
- **Scouting growing companies:** `references/growth-signals.md` — funding queries, signal types, fit scoring
- **How to define targets:** `references/target-criteria.md` — the guide, plus the location and experience filters applied to every search
- **Outreach context:** `profile/me.md` — background and story angles
- **Qualification matching:** `profile/resume.md` — experience and skills
- **Voice:** `profile/voice.md`

---

## Job Tracker Integration

This skill reads and writes the user's **Pipeline**, a single Google Sheet. The sheet ID and live tab come from `profile/config.json` (`pipeline_sheet_id`, `pipeline_tab`). If either is blank, say so and point to `setup`; you can still show results in chat.

Full column reference and the cheap workbench helpers (`find` / `log` / `add_row`): `skills/networking/references/pipeline.md`. Needs the Composio Google Sheets connector; if it is missing, say so and point to README → "Connect your tools". **Never read the whole tab** (a full-tab read costs tens of thousands of tokens).

### Before searching
Check what the user already tracks with `find(["<Company>", ...])`, or a one-column read of `'<pipeline_tab>'!A:A`. Don't resurface companies already in the pipeline.

### After any search / x-ray / scout result
Proactively offer: "Want me to add [Company | Role] to your tracker?"

If yes, `add_row` it (columns per `pipeline.md`: A = company and role in one cell, B = URL, C = Status, D = Log, E = Notes):

```
print(add_row(["<Company>, <Role>", "<job URL>", "Found", "<M/D> - found via <search>; next: <next action>", "<comp, location, fit read>"]))
```

### Display format
When showing tracker state: `Company, Role | Status | latest Log line`.

Keep it one flat list: no stage columns, no kanban. A single scannable list is the point of the sheet.

---

## How It Works — Natural Language, Not Subcommands

The user says what they want; route by intent.

### "Find roles at..." / "What's open in..." / "Search for jobs in..."
**→ Search flow**

1. Parse the request for: role focus, industry / vertical, specific companies, location
2. Merge with defaults from `profile/targets.md` (the user shouldn't have to repeat "not junior" every time)
3. Generate 3 platform-specific Boolean strings:
   - **LinkedIn** — ready to paste into the LinkedIn Jobs keyword field
   - **Indeed** — ready to paste into Indeed search
   - **Google** — ready to paste into Google, with minus-sign exclusions
4. Present all 3 formatted and copy-ready
5. Run WebSearch with the Google version to show immediate results
6. Include the LinkedIn URL filter reminder: append `&f_TPR=r86400` for the last 24 hours, and the `&f_E=` experience level that matches the user's seniority
7. Apply the **location filter** and **experience filter** (`references/target-criteria.md`) to every hit before showing it — read the JD body, not the card
8. **Proactively offer:** "Want me to add any of these to your tracker?" / "Want me to find the hiring manager at any of these companies?"

### "What's open at [Company]" / "X-Ray [Company]" / "Scan Greenhouse for..."
**→ X-Ray flow**

1. Read `boolean-templates.md` for X-Ray templates and `platform-guide.md` for ATS URL patterns
2. Build `site:` queries targeting the company's ATS
   - If the company's ATS is known, target it
   - If unknown, scan all the major ones: Greenhouse, Lever, Ashby, Workday
3. Run WebSearch with each X-Ray query
4. Present results as a table: Role | Platform | URL | Posted Date
5. **Proactively offer:** "Want me to add any to your tracker?" / "Want me to find who leads this team?" / "Want me to tailor your resume for any of these?"

### "Find companies that just fundraised" / "Who just raised?" / "Growing companies in X"
**→ Scout flow**

1. Read `growth-signals.md` for search queries and scoring criteria
2. Run WebSearch for recent funding rounds, hiring surges and product launches in the user's target verticals
3. Cross-reference against Pipeline with `find()` (skip companies already tracked)
4. Score each company High / Medium / Low against `profile/targets.md`
5. Present as a table: Company | Signal | Date | Fit | Notes
6. **Offer next steps:** "Want me to X-Ray any of these for open roles?" / "Want me to find who leads the team there?" / "Want me to add any to your tracker?"
7. If the user picks a company, chain into X-Ray or Discover

### "Find me people to reach out to at [Company]" / "Who runs [function] at [Company]"
**→ Discover flow**

1. For the given company, search for the people who hire for the user's target function — the likely hiring manager, their manager, a peer on the team, and the recruiter for that function. Examples:
   - Product: VP / Head of Product, Director of PM, Group PM
   - Engineering: Engineering Manager, Director of Engineering, Staff Engineer on the team
   - Design: Head of Design, Design Manager
   - Marketing: VP / Head of Marketing, Director of Growth / Product Marketing
   - Operations: VP / Director of Operations, Head of BizOps
   - Plus: the technical or functional recruiter for that area
2. WebSearch: `site:linkedin.com/in "[Company]" ("Head of <Function>" OR "Director of <Function>" OR "<Function> Manager")`
3. Present contacts in a table: Name | Title | Company | Potential Hook
4. **Offer:** "Want me to draft outreach to any of them?"
5. If yes, hand off to networking with full context:
   - How the user found this person (e.g., "found via X-Ray — they have an open senior role on Greenhouse")
   - What about the company is relevant (e.g., "just raised a Series C, building an AI product")
   - Which story angle from `profile/me.md` fits best
   - Any warm path in `profile/contacts.md` (shared school, former colleague, mutual connection)

### "What are the LinkedIn tricks?" / "Show me niche job boards" / "Set up alerts"
**→ Tips flow**

Read `platform-guide.md` and surface the relevant section: LinkedIn URL filters (time, experience level, remote), "Open to Work" for recruiters only, Google Alerts, niche sites for the user's function and verticals, top job sites, ATS keyword tips, Distill Web Monitor, the 30-Minute Method.

### "Add [Company] to my tracker" / "Track this"
**→ Tracker flow**

1. `find()` the company first, so you don't duplicate a row
2. If the user gives company + role: `add_row()` directly (`<Company>, <Role>` in column A, posting URL in B — see `skills/networking/references/pipeline.md`)
3. If only a company: ask for the role, then write it
4. Confirm by showing the new entry in the display format

### "Tailor my resume for this role" / "Match my resume to this JD"
**→ Resume handoff**

1. Capture the job URL and key themes from the search context
2. Say: "Handing off to the resume skill with this JD context"
3. Invoke `skills/resume/SKILL.md` with the JD details

---

## Output Formats

Examples below use fictional companies.

### Search Results
```
| # | Company | Role | Platform | Posted | Link |
|---|---------|------|----------|--------|------|
| 1 | Acme Corp | Senior Software Engineer, Payments | Greenhouse | 2d ago | [link] |
| 2 | Northwind | Product Designer, Growth | LinkedIn | 1d ago | [link] |
```

### Scout Results
```
| # | Company | Signal | Date | Fit | Notes |
|---|---------|--------|------|-----|-------|
| 1 | Globex | Series C, $120M | <Mon YYYY> | High | In target vertical, hiring in target function |
| 2 | Initech | New Head of Marketing | <Mon YYYY> | Medium | Team being built, no posting yet |
```

### Discover Results
```
| # | Name | Title | Company | Hook |
|---|------|-------|---------|------|
| 1 | Jordan Lee | Director of Engineering | Globex | Same school, 2 shared connections |
| 2 | Sam Rivera | Technical Recruiter | Globex | Posts about the team's hiring |
```

### Tracker Display
```
| Company, Role | Status | Latest log |
|---------------|--------|------------|
| Globex, Senior Software Engineer | Found | <M/D> - found via scout, Series C; next: find hiring manager |
```

---

## Chaining — Act Ahead

Chain actions when the next step is obvious:

- **Search → Tracker + Discover:** after search results, offer to add top matches AND find hiring contacts
- **Scout → X-Ray → Discover → Outreach:** after scouting, offer to scan for roles, then find people, then draft outreach
- **X-Ray → Resume + Tracker:** after finding a specific role, offer to tailor the resume and add it to the tracker
- **Discover → Outreach:** after finding contacts, offer to draft messages via networking

Don't wait for the user to ask for each step. Present the natural next action.
