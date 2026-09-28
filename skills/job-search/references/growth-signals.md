# Growth Signal Detection

Use these patterns to find companies that are growing and likely to hire in the user's function —
often before a JD is posted. Replace `<year>` with the current year and `<function>` with the
user's function (product, engineering, design, marketing, operations...).

---

## Signal Types

### 1. Funding rounds
Companies that just raised are about to hire.

**Search queries (WebSearch):**
- `"Series B" OR "Series C" OR "Series D" <industry> startup funding <year>`
- `"raised" "million" <industry> company <year>`
- `[company name] funding round <year>`
- `site:techcrunch.com "raises" <industry> <year>`
- `site:crunchbase.com "[company]" funding`

**Why it matters:** post-funding companies need people to build and ship what they raised money
for. They hire fast and often haven't posted every role yet — reaching out early gets ahead of the
crowd.

### 2. IPO / pre-IPO signals
Companies preparing to go public invest in product, engineering and go-to-market.

- `"IPO filing" OR "S-1" tech company <year>`
- `"confidentially filed" IPO <year>`
- `[company name] IPO rumors`

### 3. Hiring surges
Visible headcount growth = active hiring.

- `[company name] hiring <function> <year>`
- `[company name] "growing team" OR "building team" <function>`
- `site:linkedin.com/posts "[company] hiring" <function>`

**LinkedIn headcount trick:** on a company's LinkedIn page, the "Insights" tab shows headcount
growth. Companies growing >20% year over year are actively hiring.

### 4. Product launches / expansions
New products, new markets or new offices need people to own them.

- `[company name] launches OR announces product <year>`
- `[company name] "new office" OR "expands to" <year>`
- `site:producthunt.com [company name]`

### 5. Executive hires
A new leader in the user's function means the team is being built or restructured.

- `[company name] "hires" OR "appoints" "VP <Function>" OR "Head of <Function>"`
- `site:linkedin.com/posts "[company]" "excited to announce" "<function>"`

---

## Sources (ranked by signal quality)

| Source | URL | Best For |
|--------|-----|----------|
| TechCrunch | techcrunch.com | Funding rounds, product launches |
| Crunchbase | crunchbase.com | Funding data, company profiles |
| The Information | theinformation.com | Insider scoops, pre-IPO signals |
| Bloomberg | bloomberg.com/technology | IPO filings, major deals |
| Business Wire / PR Newswire | businesswire.com, prnewswire.com | Press releases, exec hires |
| LinkedIn posts | linkedin.com/feed | Hiring announcements, team growth |
| Product Hunt | producthunt.com | Product and startup launches |
| Y Combinator | ycombinator.com/companies | New YC startups |

---

## Fit Scoring

Score each signal against `profile/targets.md`.

### High fit
- In a target industry / vertical
- A role in the user's function likely open (or soon)
- Stage and size inside the user's target range
- An allowed location, or remote-friendly if the user accepts remote
- Two or more signals (e.g. funding + hiring + launch)

### Medium fit
- Adjacent vertical
- Adjacent role (e.g. a neighbouring function the user would consider)
- Established company with a new initiative in the user's area
- Only one signal (e.g. funding but no hiring posts yet)

### Low fit
- A vertical the user excluded
- Wrong seniority for the user
- No allowed location and no remote option
- Size outside the user's range

---

## Scout Workflow

1. **WebSearch** for recent funding rounds in the user's target verticals
2. **WebSearch** for hiring surges and product launches
3. **Cross-reference** against the active target list in `profile/targets.md` and against Pipeline (`find()`), so you don't surface what they already know
4. **Present** as a table: Company | Signal | Date | Fit | Notes
5. **Offer next steps:**
   - "Want me to X-Ray [company] for open roles?"
   - "Want me to find who leads the team there?"
   - "Want me to add any of these to your tracker?"
6. If the user picks a company, chain into X-Ray or Discover
