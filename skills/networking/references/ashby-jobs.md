# Ashby jobs: connect and pull an Ashby posting

Read this the moment the user shares an **Ashby** job link (`jobs.ashbyhq.com/<org>` or
`jobs.ashbyhq.com/<org>/<jobId>`), with or without the JD text pasted alongside. Its job: **pull
the full posting cleanly, ingest it, and hand the structured JD to the outreach or resume flow,
with no dead ends on a sandbox egress block.** Do not search for an aggregator summary, and do not
ask the user to paste before you have tried the real path.

For Greenhouse, Lever, Workday or a company careers page, use `skills/job-fetch/SKILL.md`, which
carries those API mappings. If job-fetch already ingested this JD earlier in the session, do not
fetch again.

---

## The one rule

**Ashby job pages are client-rendered single-page apps. Fetching the page HTML returns markup with
no JD text. Never scrape the page.** Use Ashby's **public posting API**, which returns clean JSON:
`title`, `location`, `employmentType`, `isRemote`, `compensation`, and both `descriptionHtml` and a
ready-to-use `descriptionPlain`. The public job board is unauthenticated, so no API key or
employer-side Ashby account is needed to read a published posting.

---

## Connection ladder: try in order, one try each, do not loop on a 403

1. **Dedicated Ashby MCP, if one is connected** → use it (Path A). Check first.
2. **Ashby public API via the Composio MCP** → the reliable default in web sessions (Path B).
3. **Direct fetch** (desktop, or any session with open internet) → same API, no Composio (Path C).
4. **Paste fallback** → name the blocked host and ask the user to paste (Path D). Last resort.

If neither Composio nor open internet is available, say which connector is missing and point to
README "Connect your tools".

---

## Step 1: Parse the URL

| URL | `<org>` | `<jobId>` |
|-----|---------|-----------|
| `jobs.ashbyhq.com/acme/0f3c...-uuid` | `acme` | the UUID |
| `jobs.ashbyhq.com/acme/0f3c.../application` | `acme` | the UUID (drop `/application`) |
| `jobs.ashbyhq.com/acme` (board root) | `acme` | none; pick by title match, or list roles for the user |

`<org>` is the first path segment after the host and is usually case-sensitive; copy it verbatim.

---

## Step 2: Pull the posting

### Path A: dedicated Ashby MCP

If the session has an Ashby tool (named like `mcp__*ashby*`), call its posting-fetch tool with the
`<org>` (and `<jobId>` if known), then go to Step 3. If there is none, go to Path B without
stalling.

### Path B: Composio → public API

Web sandboxes often block job boards at the egress proxy, so run the fetch **outside** the sandbox
on Composio's machines, with `COMPOSIO_REMOTE_BASH_TOOL` (load it with ToolSearch if deferred).

Send a real browser User-Agent, and write to a file before parsing:

```bash
org="acme"                        # from Step 1
url="https://api.ashbyhq.com/posting-api/job-board/${org}?includeCompensation=true"
curl -sSL -A "Mozilla/5.0" -o /tmp/board.json "$url"
jq '.jobs | length' /tmp/board.json      # >0 means you got the board
```

Then select one posting and print only what you need:

```bash
jobId="<uuid from Step 1>"        # omit to pick by title
jq -r --arg id "$jobId" '
  (.jobs[] | select(.id == $id)) // .jobs[0]
  | "TITLE: \(.title)\nLOCATION: \(.location)  (remote=\(.isRemote), \(.workplaceType))\nTYPE: \(.employmentType)   TEAM: \(.department) / \(.team)\nCOMP: \(.compensation // "not shown")\nURL: \(.jobUrl)\n---\n\(.descriptionPlain)"
' /tmp/board.json
```

If the org returns 200 but `.jobs` is empty, re-check the slug casing. If the call fails through
Composio, go to Path D; do not retry a hard 403 in a loop.

### Path C: direct fetch

Same URL, no Composio: fetch it (or `curl -sSL -A "Mozilla/5.0" "<url>"`) and parse the same way.

### Path D: paste fallback

Only after A to C are unavailable: tell the user the exact blocked host (`api.ashbyhq.com` /
`jobs.ashbyhq.com`) and ask them to paste the JD. Do not fall back to a web-search summary; that
loses the requirements language the resume needs.

---

## Step 3: Which posting, which fields

**Pick the posting:** match `.id == <jobId>`. Each job's `.jobUrl` is
`https://jobs.ashbyhq.com/<org>/<id>`, so the UUID in the link is the job's `id`. Without a job id,
match on title, or list open roles and ask.

| Field | Use |
|-------|-----|
| `title`, `department`, `team` | role identity; drives the resume tagline and outreach frame |
| `location`, `secondaryLocations`, `isRemote`, `workplaceType` | where / remote or on-site |
| `employmentType` | FullTime, Contract, etc. |
| `compensation` | comp if published (often `null`) |
| **`descriptionPlain`** | **the JD text, already clean; use this** |
| `descriptionHtml` | fallback only; strip tags with `sed 's/<[^>]*>//g'` |
| `jobUrl`, `applyUrl` | canonical links for tracker column B |

The envelope is `{ apiVersion, jobs: [ ... ] }`.

**Fetch gotchas:**
- **Real User-Agent required.** The API rejects a bare `python`/`urllib` UA but accepts `curl` or
  `-A "Mozilla/5.0"`. A 403 from the API with a default UA is a UA problem, not the proxy; retry
  with a browser UA before concluding the host is unreachable.
- **Do not pipe `curl` into a `python3 - <<HEREDOC`**; the heredoc and the piped body collide on
  stdin. Write to a file first, then parse the file.

---

## Step 4: Ingest, don't echo; then continue

Read the JD; do not read it back. Do not paste the description into the reply.

1. Hold in context: title, company, team, location, remote/on-site, comp (if shown), key
   responsibilities, must-have requirements, notable signals (stage, stack, load-bearing phrases).
2. Reply with **one short line**, for example:
   > Read the *Senior Analyst, Growth* role at Acme Corp: remote US, full-time. Want a tailored
   > resume, outreach, or both?
3. Continue with the JD in hand:
   - **Resume** → `skills/resume/SKILL.md`
   - **Outreach** → the networking flow in `skills/networking/SKILL.md`
   - **Tracker** → add the role via `references/pipeline.md` with `jobUrl` in column B

Pulling the JD is setup, not the deliverable. Do not stop after the acknowledgement unless the user
only asked you to read it.

---

## Adding a dedicated Ashby MCP (optional)

Path B already works with no setup. A dedicated Ashby connector is only worth adding for
employer-side data. Enable it in the connector settings, then start a fresh session (connectors
enabled mid-session do not load into the running one). Path A then picks it up automatically.
