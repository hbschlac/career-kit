---
name: linkedin-jobs
description: >
  LinkedIn jobs connector. Searches LinkedIn job postings and pulls full job descriptions through
  LinkedIn's public guest endpoints (no login, no account), then moves a job into the rest of the
  user's career pipeline: the Pipeline sheet, a recruiter-filter score, a tailored resume, outreach.
  Trigger on any linkedin.com/jobs URL (jobs/view/<id>, currentJobId=<id>), or "search LinkedIn
  jobs", "find on LinkedIn", "LinkedIn roles for", "pull this LinkedIn job", "track this LinkedIn
  job", "add these LinkedIn jobs to my tracker", "what's new on LinkedIn for".
---

# linkedin-jobs

One path from "I found it on LinkedIn" to a tracked role with a tailored CV. The fetch lives in
`mcp/linkedin-jobs/server.py` (stdlib Python, no installs). It is both an **MCP server** and a
**CLI**, same code.

## What it touches (and what it doesn't)

It reads the pages LinkedIn serves to **logged-out** visitors
(`linkedin.com/jobs-guest/jobs/api/...`). No cookies, no login, no LinkedIn account — nothing it
does is tied to the user's profile. The one real limit is rate: LinkedIn answers bursts with
**429**. The server pauses 1.5s between pages and 2.5s between postings it reads to filter, and
caps a call at 100 results. On a 429 a filtered search returns what it kept so far with
`screened.stopped` saying why; stop and tell the user. Don't retry in a loop, and don't scrape
people or profiles with it. Job postings only.

## Step 0 — pick the backend (first one that works, one try each)

1. **MCP tools are loaded** (`mcp__linkedin-jobs__linkedin_search_jobs`, `..._get_job`,
   `..._track_job`): use them. Any Claude Code session opened in this repo gets them from `.mcp.json`.
2. **No MCP, but Bash can reach linkedin.com:** run the CLI from the repo root:
   `python3 mcp/linkedin-jobs/server.py search|get|track ...` (JSON on stdout).
3. **The sandbox blocks linkedin.com (403 / proxy error):** run the same CLI on Composio's remote
   bash (`COMPOSIO_REMOTE_BASH_TOOL`; load via ToolSearch `+composio remote bash`). Upload the
   script once per Composio sandbox, then call it:
   ```bash
   test -f ~/li/server.py || echo MISSING
   # if MISSING: mkdir -p ~/li && cat > ~/li/server.py <<'PYEOF'
   #   <paste mcp/linkedin-jobs/server.py verbatim>
   # PYEOF
   python3 ~/li/server.py get <job id> --markdown
   ```
   `track` works there too: it only prints the Pipeline row (see **Track** below).
4. Nothing works → name the blocked host, point to README → "Connect your tools", and ask the user
   to paste the JD. Never swap in a web search.

## Commands

### Search — "find X roles on LinkedIn"

`linkedin_search_jobs` / `server.py search`. When the user doesn't say, default to their usual cut
from `profile/targets.md`: target titles as keywords, allowed locations, their years of experience
as `years` (and the most a posting can ask for as `max_years_asked`), their target industries as
`industries`, their compensation floor as `min_salary`, plus `posted_within: week`, `sort: recent`,
`limit: 25`. If `profile/targets.md` is empty, ask for keywords and location rather than guessing.

**LinkedIn's public search only honors keywords, location and posted-within** (checked 2026-09-29:
the same jobs come back with or without its experience, remote, industry, function and pay
filters). So every other filter below is applied by the server itself: it reads each posting and
keeps the ones that match. That costs about 3 seconds a posting, so a filtered search reads at most
`check_limit` postings (15 by default, 40 max) and says so in `screened.stopped` when it hits that.

| Arg | Values | How it's applied |
|-----|--------|------------------|
| `keywords` | free text; LinkedIn Boolean works (`"product designer" AND (fintech OR payments)`) — see `skills/job-search/references/boolean-templates.md` | by LinkedIn |
| `location` | `United States`, `New York, NY`, `London, England`, `Chicago, IL`, ... | by LinkedIn |
| `posted_within` | `24h` `week` `month` `any` | by LinkedIn |
| `years` | the user's years of relevant experience, e.g. `6`. Picks the seniority levels that usually fit (6 → mid-senior; 12 → mid-senior + director) unless `experience` is given | posting's seniority |
| `max_years_asked` | drop postings that ask for more years than this. Set it a year or two above `years`: "5+ years" postings often hire at 4 | read from the description |
| `experience` | `internship` `entry` `associate` `mid-senior` `director` `executive` (list or comma string) | posting's seniority |
| `industries` | words to match in the posting's LinkedIn industry, e.g. `["software", "financial", "health"]` | posting's industry |
| `functions` | words to match in its job function, e.g. `["product management"]` | posting's function |
| `min_salary` | yearly pay floor. Drops postings whose posted range tops out below it; hourly is counted at 2,080 hours | posted pay |
| `workplace` | `onsite` `remote` `hybrid` | guessed from location, title and description |
| `job_type` | `full-time` `part-time` `contract` `temporary` `internship` | posting's employment type |
| `company_ids` | LinkedIn numeric company ids | by LinkedIn |
| `check_limit` | most postings to read when filtering | — |
| `start` | pass `next_start` from the last call for the next page. It starts at the first posting this call didn't read, so paging never skips one | — |

A posting that doesn't say (no pay listed, seniority "Not Applicable", no years in the text) is
**kept** and marked `unknown: [...]`: missing is not a no. Mention those marks in the table. Every
dropped posting comes back in `screened.dropped` with the reason ("asks for 10+ years",
"industries is Banking"); offer that list in one line ("dropped 7: 4 too senior, 2 other
industries, 1 closed") rather than hiding it, since a wrong filter is how good roles get missed.

Show results as a compact table (# · Title · Company · Location · Posted · id, plus Level · Years
asked · Pay when the search was filtered). Flag roles already
in Pipeline (`find([...])` with the workbench helpers) and anything that matches the user's target
in `profile/targets.md`. Apply the location and experience filters in
`skills/job-search/references/target-criteria.md` once you have pulled the JD — the card's
location is not the whole story. Then ask which ones to pull or track. Don't pull every JD unasked.

### Pull a JD — a LinkedIn URL, or "pull #3"

`linkedin_get_job` with `format: "markdown"` (CLI: `get <id|url> --markdown`). Any LinkedIn job
URL works, including search URLs with `currentJobId=`. Then do what **job-fetch** does: ingest,
don't echo. Reply with one line (title, company, location, comp if shown, applicants) and wait.
If it comes back `closed`, say so before anything else.

### Track — "add these to my tracker"

`linkedin_track_job` (MCP) or `track <id>` (CLI) returns the Pipeline row and the exact
`add_row([...])` call. The row fills the first five Pipeline columns
(`skills/networking/references/pipeline.md`):

| Col | Field | From the posting |
|-----|-------|------------------|
| A | Company / role | `<Company>, <Title>` |
| B | Job link | off-site apply URL if LinkedIn has one, else the LinkedIn job URL |
| C | Status | blank — the user sets it |
| D | Log | `<M/D> - found on LinkedIn` |
| E | Notes | notes · location · comp · posted · applicants · `CLOSED on LinkedIn` if closed |
| F-L | CV for application, Existing CV, Base CV, CV for this app (new), Recruiter score, Gaps / to add, Fit | left blank; filled later by the resume and recruiter-filter steps (and Fit only by the user) |

It does not write — the sheet needs the user's Google auth. Run the returned call with the
workbench helpers in `skills/networking/references/pipeline.md` (`dry_run=True` first); `add_row`
refuses a role already in column A. Sheet ID and tab come from `profile/config.json`.

### Hand-off — "make a CV for this" / "score me" / "who do I reach out to"

The markdown JD block is the input every downstream skill takes. Pass it as-is:

| The user says | Route to |
|---------------|----------|
| "score me", "will I pass the ATS" | `skills/recruiter-filter/SKILL.md` with the JD block. Record the score in column J |
| "tailor / make a CV" | `skills/resume/SKILL.md` with the JD block. After the CV exists, `log()` it in Pipeline and set column I |
| "who's the hiring manager", "draft outreach" | `skills/job-search/SKILL.md` (Discover flow) → `skills/networking/SKILL.md` (draft). `log()` the outreach once sent |

Batch flow: **search → pick → track (`add_row`, dry-run first) → recruiter-filter each → tailor the
best-scoring ones.** Stop between steps for the user's picks. Never auto-apply.

## Setup (once per surface)

- **This repo, any Claude Code session (cloud or local):** nothing to do. `.mcp.json` registers
  `linkedin-jobs`. If Claude Code asks to approve a project MCP server the first time, approve
  `linkedin-jobs` (or run `/mcp`).
- **Local machine, every repo:**
  `claude mcp add --scope user linkedin-jobs -- python3 /path/to/your-kit-clone/mcp/linkedin-jobs/server.py`
- **Claude Desktop app:** add to `claude_desktop_config.json`:
  `{"mcpServers": {"linkedin-jobs": {"command": "python3", "args": ["/path/to/your-kit-clone/mcp/linkedin-jobs/server.py"]}}}`
- **claude.ai web / mobile chat (not Claude Code):** these need a hosted HTTPS MCP server, which
  this kit doesn't include. Use a Claude Code session with this repo, or step 3 above.

## If LinkedIn changes its markup

Parsing is regex over known class names (`base-search-card__title`,
`show-more-less-html__markup`, `description__job-criteria-item`, ...) in `parse_search` /
`parse_job`. When results come back with empty titles or descriptions, fetch one raw page
(`curl -A "Mozilla/5.0" https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/<id>`), find the
new class names, and fix the regex.
