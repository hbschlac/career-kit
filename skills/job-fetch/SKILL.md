---
name: job-fetch
description: >
  Fetches and ingests a job description when the user shares a job-posting URL
  (Ashby / Greenhouse / Lever / Workday / Gem, or any company careers page), even when
  the sandbox egress proxy blocks the host (403). Routes the fetch out of the
  sandbox through the connected Composio MCP and the ATS public APIs, parses the
  role, ingests it into context, and acknowledges in one line. Activates on any
  jobs.ashbyhq.com / boards.greenhouse.io / jobs.lever.co / *.myworkdayjobs.com /
  jobs.gem.com / careers-page link, or when the user says "read this job", "here's a role/JD".
---

# job-fetch

Pull the real text of a job posting, even one the sandbox can't reach, ingest it, acknowledge it.
Built to avoid the dead end of "the job board is proxy-blocked, let me search an aggregator
instead."

## Works on desktop and web — try direct, fall back to Composio

The URL → API mapping is identical everywhere; only where the fetch runs changes:

- **Desktop / any environment with normal internet:** a direct fetch of the ATS public API works.
  Use `WebFetch` (or `curl` via Bash). No Composio needed.
- **Claude Code on the web:** the sandbox egress proxy is typically a **strict allowlist** — job
  boards (`jobs.ashbyhq.com`, `boards.greenhouse.io`, `jobs.lever.co`, careers sites) return
  **403 CONNECT** to every in-sandbox fetch (`WebFetch`, `curl`, `wget`, headless browsers). Do not
  try to route around the proxy. The fetch must happen **outside the sandbox**, via a connected
  remote-execution MCP.

**Algorithm:** try the public API directly first (`WebFetch`). If it succeeds, parse. If it fails
with a 403 / proxy block, retry the same URL through Composio. One try each — don't loop on a 403.

### The out-of-sandbox backend (web) — Composio remote execution

The Composio MCP runs bash on Composio's own machines, which have open internet. Tool:
`COMPOSIO_REMOTE_BASH_TOOL` (its full name is prefixed by whatever the connector is called in the
session, e.g. `mcp__<connector>__COMPOSIO_REMOTE_BASH_TOOL`; load it via ToolSearch with
`+composio remote bash`). Any other remote-exec or scrape MCP works the same way, because it
connects through the MCP gateway, not the egress proxy.

If none is available: say the host is blocked, name the missing connector (see README → "Connect
your tools"), and ask the user to paste the JD text.

### Step 1 — Identify the ATS from the URL, hit its PUBLIC API (primary path)

Raw ATS pages are client-rendered SPAs — `curl` returns markup with **zero JD text**. Don't scrape
the HTML. Use the ATS's public posting API, which returns clean JSON (title, location, comp,
description). Fetch it directly (desktop) or via `COMPOSIO_REMOTE_BASH_TOOL` (web):

| URL shape | Public API |
|-----------|------------|
| `jobs.ashbyhq.com/<org>` or `/<org>/<jobId>` | `https://api.ashbyhq.com/posting-api/job-board/<org>?includeCompensation=true` → array of jobs; pick the one whose `id` matches `<jobId>` (or the only listing / title match) |
| `boards.greenhouse.io/<org>/jobs/<id>`, `job-boards.greenhouse.io/<org>/jobs/<id>` | `https://boards-api.greenhouse.io/v1/boards/<org>/jobs/<id>?content=true` → `title`, `location.name`, `content` (HTML) |
| `jobs.lever.co/<org>/<id>` | `https://api.lever.co/v0/postings/<org>/<id>` → `text`, `descriptionPlain`, `categories` |
| `linkedin.com/jobs/view/<id>`, `...?currentJobId=<id>` | hand off to the **linkedin-jobs** skill (`skills/linkedin-jobs/SKILL.md`): `linkedin_get_job` MCP tool, or `python3 mcp/linkedin-jobs/server.py get <url> --markdown`. LinkedIn job pages are login-walled; its guest endpoint returns the full JD |
| `jobs.gem.com/<org>/<extId>` | GraphQL POST — see **Gem** below (no REST endpoint) |
| `*.myworkdayjobs.com/...` | the site's `/wday/cxs/<tenant>/<site>/jobs` JSON endpoint; if the tenant/site path isn't obvious, use the fallback in Step 2 |

Example (Ashby):
`curl -sSL -A "Mozilla/5.0" "https://api.ashbyhq.com/posting-api/job-board/<org>?includeCompensation=true"`
returns all postings; pick the one whose `id` matches the `<jobId>` in the URL, then use its
`title`, `location`, `compensationTierSummary` and `descriptionHtml`.

### Gem (`jobs.gem.com`) — GraphQL, and the two IDs are easy to get wrong

Gem boards are a pure SPA with no REST posting API. POST to the public GraphQL endpoint:

```
POST https://jobs.gem.com/api/public/graphql        # /api/graphql is 403, /graphql is 404
Content-Type: application/json
Origin: https://jobs.gem.com
{"operationName":"ExternalJobPosting",
 "variables":{"boardId":"<org-slug>","extId":"<last URL segment>"},
 "query":"query ExternalJobPosting($boardId: String!, $extId: String!) { oatsExternalJobPosting(boardId: $boardId, extId: $extId) { title descriptionHtml firstPublishedTsSec locations { name city isRemote } job { locationType employmentType department { name } } jobPostSectionHtml { introHtml outroHtml } compensationHtml } }"}
```

**Two gotchas, both of which return `null` rather than an error:**

- **`boardId` is the vanity slug from the URL** (e.g. `acme-corp`) — *not* the UUID in the page's
  `window['__GEM_TRACKING_CONTEXT__']`. That UUID looks authoritative and silently fails.
- **`extId` is the last URL path segment verbatim.** It base64-decodes to `jobpost:<uuid>`, but the
  decoded UUID does **not** work. Pass the raw segment.

A `null` result with no `errors` array means one of those two is wrong, not that the job is gone.

**List the whole board** (feeds `recruiter-filter` Step 0.5) with the same endpoint:

```
query JobBoardList($boardId: String!) { oatsExternalJobPostings(boardId: $boardId) {
  jobPostings { id extId title locations { name city isRemote }
                job { department { name } locationType employmentType } } } }
```

Unlisted roles exist — some companies post a role only on their own careers page (or not on any
board), so check the company's own careers surface too, not just the ATS.

Parse the JSON, strip HTML from the description field (`sed 's/<[^>]*>//g'` or by reading it), keep
the visible text.

**Fetch gotchas (Composio remote bash):**
- **Send a real User-Agent.** Some ATS APIs (Ashby's included) return **403 to a bare Python/urllib
  UA** (bot filtering) but 200 to `curl` / `-A "Mozilla/5.0"`. A 403 from the ATS *API* with a
  default UA is a UA problem, not a proxy block — retry with a browser UA before concluding the host
  is unreachable.
- **Don't pipe curl into a `python3 - <<HEREDOC`** — the heredoc and the piped body collide on stdin.
  Write the response to a file first (`curl ... -o /tmp/board.json`), then parse the file.

### Step 2 — Fallback for an unknown ATS / a company's own careers page

1. `curl -sSL "<url>"` — directly on desktop, or via Composio remote bash on web — strip tags, check
   visible-text length. If it's real prose (hundreds of words of role text), use it.
2. If it's thin / SPA-shaped (lots of markup, no prose), escalate to a scrape-to-markdown tool. With
   Composio: discover one with `COMPOSIO_SEARCH_TOOLS` (use_case: "scrape a URL to clean markdown"),
   then run it via `COMPOSIO_MULTI_EXECUTE_TOOL`.
3. If every path fails, name the exact blocked host and ask the user to paste the text. Don't
   silently give up or substitute a web search.

## After fetching — ingest, don't echo

The user wants the JD **read, not read back**. Do NOT paste the description into the reply:

1. Parse into structured fields you hold in context: **title, company, location, remote/on-site,
   comp (if present), key responsibilities, must-have requirements, years of experience required,
   notable signals** (stage, team, tech).
2. Reply with **one short line** confirming it, e.g.:
   > Read the Senior Data Engineer role at Northwind — Chicago, hybrid, platform team. Got it — ready when you are.
3. Stop. Wait for the next instruction.

## Downstream (only when the user asks — not automatic)

- Tailor a resume → `skills/resume/SKILL.md`
- Score fit / ATS pass → `skills/recruiter-filter/SKILL.md`
- Recruiter or hiring-manager outreach → `skills/networking/SKILL.md`
- Track it → `skills/networking/references/pipeline.md` (`find()` first, then `add_row`)

Pass the structured JD you ingested. Don't do any of this unprompted — ingest-and-acknowledge is
the whole job unless asked.
