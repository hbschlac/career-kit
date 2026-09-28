#!/usr/bin/env python3
"""LinkedIn Jobs MCP server for the career-kit skills.

Reads LinkedIn's PUBLIC guest job endpoints (the ones linkedin.com/jobs serves to
logged-out visitors). No login, no cookies, no LinkedIn account is ever touched.

Two ways to run the same code:

  python3 server.py                      # MCP server over stdio (Claude Code / Desktop)
  python3 server.py search --keywords "data analyst" --location "Chicago, IL"
  python3 server.py get 1234567890       # or a full linkedin.com/jobs/view/... URL
  python3 server.py track 1234567890 --notes "via referral"   # prints the Pipeline row

The CLI mode prints JSON to stdout, so a web session whose sandbox cannot reach
linkedin.com can run this file on Composio's remote bash instead (see
skills/linkedin-jobs/SKILL.md).

Stdlib only; Python 3.8+.
"""

import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

SERVER_NAME = "linkedin-jobs"
SERVER_VERSION = "1.0.0"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
SEARCH_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
JOB_URL = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{id}"
VIEW_URL = "https://www.linkedin.com/jobs/view/{id}/"

# Politeness: one request at a time, a pause between pages, a hard page cap.
PAGE_SIZE = 10
PAGE_PAUSE_S = 1.5
MAX_RESULTS = 100

POSTED = {"24h": "r86400", "day": "r86400", "week": "r604800",
          "month": "r2592000", "any": None}
EXPERIENCE = {"internship": "1", "entry": "2", "associate": "3",
              "mid-senior": "4", "director": "5", "executive": "6"}
JOB_TYPE = {"full-time": "F", "part-time": "P", "contract": "C",
            "temporary": "T", "internship": "I"}
WORKPLACE = {"onsite": "1", "remote": "2", "hybrid": "3"}


class LinkedInError(Exception):
    pass


# --------------------------------------------------------------------------- http

def _get(url, params=None):
    if params:
        url = url + "?" + urllib.parse.urlencode(
            {k: v for k, v in params.items() if v not in (None, "", [])}, doseq=True)
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise LinkedInError("LinkedIn rate-limited this IP (429). Wait a few minutes; "
                                "do not retry in a loop.")
        if e.code == 404:
            raise LinkedInError("LinkedIn returned 404: the posting is gone or the id is wrong.")
        raise LinkedInError("LinkedIn returned HTTP %d for %s" % (e.code, url))
    except urllib.error.URLError as e:
        raise LinkedInError("Could not reach linkedin.com (%s). On a web sandbox that "
                            "blocks it, run this script through Composio remote bash." % e.reason)


# ------------------------------------------------------------------------ parsing

def _text(fragment):
    """HTML fragment -> readable plain text (keeps list items and paragraphs)."""
    if fragment is None:
        return ""
    s = re.sub(r"(?is)<(script|style)\b.*?</\1>", "", fragment)
    s = re.sub(r"(?i)<br\s*/?>", "\n", s)
    s = re.sub(r"(?i)<li[^>]*>", "\n- ", s)
    s = re.sub(r"(?i)</(p|div|ul|ol|h[1-6])>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\r\f\v\xa0]+", " ", s)
    s = re.sub(r" *\n *", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def _first(pattern, s, flags=re.S):
    m = re.search(pattern, s, flags)
    return _text(m.group(1)) if m else ""


def job_id_from(value):
    """Accept a numeric id, a urn, or any linkedin.com/jobs URL (view/, currentJobId=...)."""
    value = str(value).strip()
    if value.isdigit():
        return value
    for pat in (r"currentJobId=(\d+)", r"jobPosting[:%3A]+(\d+)", r"/jobs/view/(?:[^/?#]*?-)?(\d{6,})",
                r"(\d{8,})"):
        m = re.search(pat, value)
        if m:
            return m.group(1)
    raise LinkedInError("Could not find a LinkedIn job id in %r" % value)


def parse_search(page):
    jobs = []
    for card in re.split(r"<li>", page)[1:]:
        m = re.search(r"urn:li:jobPosting:(\d+)", card)
        if not m:
            continue
        jid = m.group(1)
        dt = re.search(r'<time[^>]*datetime="([^"]+)"', card)
        jobs.append({
            "id": jid,
            "title": _first(r'<h3 class="base-search-card__title">(.*?)</h3>', card),
            "company": _first(r'<h4 class="base-search-card__subtitle">(.*?)</h4>', card),
            "location": _first(r'<span class="job-search-card__location">(.*?)</span>', card),
            "posted": dt.group(1) if dt else "",
            "posted_ago": _first(r"<time[^>]*>(.*?)</time>", card),
            "salary": _first(r'<span class="job-search-card__salary-info">(.*?)</span>', card),
            "signal": _first(r'<span class="job-posting-benefits__text">(.*?)</span>', card),
            "url": VIEW_URL.format(id=jid),
        })
    return jobs


def parse_job(page, jid):
    criteria = {}
    for item in re.findall(r'<li class="description__job-criteria-item">(.*?)</li>', page, re.S):
        k = _first(r"<h3[^>]*>(.*?)</h3>", item)
        v = _first(r"<span[^>]*>(.*?)</span>", item)
        if k:
            criteria[k] = v
    desc = _first(r'<div class="show-more-less-html__markup[^"]*"[^>]*>(.*?)</div>\s*'
                  r'(?:<button|</section>)', page)
    if not desc:
        desc = _first(r'<div class="show-more-less-html__markup[^"]*"[^>]*>(.*)</div>', page)
    apply_url = ""
    m = re.search(r'<code id="applyUrl"[^>]*><!--"(.*?)"--></code>', page, re.S)
    if m:
        apply_url = html.unescape(m.group(1))
        q = urllib.parse.parse_qs(urllib.parse.urlparse(apply_url).query)
        apply_url = q.get("url", [apply_url])[0]
    company_url = ""
    m = re.search(r'class="topcard__org-name-link[^"]*"[^>]*href="([^"?]+)', page)
    if m:
        company_url = m.group(1)
    title = _first(r'<h2[^>]*class="[^"]*top-card-layout__title[^"]*"[^>]*>(.*?)</h2>', page)
    if not title and not desc:
        raise LinkedInError("LinkedIn returned a page with no job on it (id %s). It may be "
                            "closed, or LinkedIn served a login wall." % jid)
    return {
        "id": jid,
        "title": title,
        "company": _first(r'class="topcard__org-name-link[^"]*"[^>]*>(.*?)</a>', page),
        "company_linkedin": company_url,
        "location": _first(r'<span class="topcard__flavor topcard__flavor--bullet">(.*?)</span>', page),
        "posted_ago": _first(r'<span class="posted-time-ago__text[^"]*">(.*?)</span>', page),
        "applicants": _first(r'class="num-applicants__caption[^"]*">(.*?)</(?:figcaption|span)>', page),
        "salary": _first(r'<div class="salary compensation__salary">(.*?)</div>', page),
        "seniority": criteria.get("Seniority level", ""),
        "employment_type": criteria.get("Employment type", ""),
        "job_function": criteria.get("Job function", ""),
        "industries": criteria.get("Industries", ""),
        "closed": bool(re.search(r"No longer accepting applications", page)),
        "apply_url": apply_url,
        "url": VIEW_URL.format(id=jid),
        "description": desc,
    }


# ------------------------------------------------------------------------- tools

def _pick(mapping, value, name):
    if value in (None, "", []):
        return None
    vals = value if isinstance(value, list) else [v.strip() for v in str(value).split(",")]
    out = []
    for v in vals:
        key = str(v).lower()
        if key not in mapping:
            raise LinkedInError("Unknown %s %r. Use one of: %s" % (name, v, ", ".join(mapping)))
        if mapping[key]:
            out.append(mapping[key])
    return ",".join(out) or None


def search_jobs(keywords="", location="", posted_within="week", experience=None,
                job_type=None, workplace=None, company_ids=None, sort="recent",
                limit=25, start=0):
    limit = max(1, min(int(limit or 25), MAX_RESULTS))
    params = {
        "keywords": keywords,
        "location": location,
        "f_TPR": _pick(POSTED, posted_within or "any", "posted_within"),
        "f_E": _pick(EXPERIENCE, experience, "experience"),
        "f_JT": _pick(JOB_TYPE, job_type, "job_type"),
        "f_WT": _pick(WORKPLACE, workplace, "workplace"),
        "f_C": ",".join(str(c) for c in company_ids) if isinstance(company_ids, list) else company_ids,
        "sortBy": {"recent": "DD", "relevant": "R"}.get(sort or "recent", "DD"),
    }
    jobs, seen, offset = [], set(), int(start or 0)
    while len(jobs) < limit:
        params["start"] = offset
        page_jobs = parse_search(_get(SEARCH_URL, params))
        fresh = [j for j in page_jobs if j["id"] not in seen]
        if not fresh:
            break
        for j in fresh:
            seen.add(j["id"])
        jobs.extend(fresh)
        offset += len(page_jobs)
        if len(jobs) < limit:
            time.sleep(PAGE_PAUSE_S)
    return {"count": len(jobs[:limit]), "next_start": offset, "jobs": jobs[:limit]}


def get_job(job):
    jid = job_id_from(job)
    return parse_job(_get(JOB_URL.format(id=jid)), jid)


def jd_markdown(j):
    """The ingest block the resume / recruiter-filter / networking skills take as a JD."""
    meta = [("Company", j.get("company")), ("Location", j.get("location")),
            ("Seniority", j.get("seniority")), ("Type", j.get("employment_type")),
            ("Function", j.get("job_function")), ("Industry", j.get("industries")),
            ("Comp", j.get("salary")), ("Posted", j.get("posted_ago")),
            ("Applicants", j.get("applicants")), ("LinkedIn", j.get("url")),
            ("Apply", j.get("apply_url"))]
    lines = ["# %s — %s" % (j.get("title", ""), j.get("company", ""))]
    if j.get("closed"):
        lines.append("\n> **Closed on LinkedIn — no longer accepting applications.**")
    lines.append("")
    lines += ["- **%s:** %s" % (k, v) for k, v in meta if v]
    lines += ["", "## Job description", "", j.get("description", "")]
    return "\n".join(lines)


def track_job(job, notes="", date=None):
    """The Pipeline row for this posting, ready for pipeline_workbench.add_row().

    Columns follow skills/networking/references/pipeline.md: A Company/role, B Job link,
    C Status (left blank), D Log, E Notes. F-L (CV links, recruiter score, gaps, fit) stay
    blank until those steps happen. The Pipeline Google Sheet can only be written with the
    user's own Google auth (Composio), so this returns the row and the exact call instead of
    writing. add_row() de-dupes on column A."""
    j = get_job(job) if not isinstance(job, dict) else job
    note_bits = [b for b in [notes, j.get("location"), j.get("salary"),
                             "LinkedIn %s" % (j.get("posted_ago") or "").strip(),
                             j.get("applicants"), "CLOSED on LinkedIn" if j.get("closed") else ""] if b]
    date = date or "%d/%d" % (time.localtime().tm_mon, time.localtime().tm_mday)
    row = ["%s, %s" % (j["company"], j["title"]), j.get("apply_url") or j["url"], "",
           "%s - found on LinkedIn" % date, " · ".join(note_bits)]
    return {"pipeline_row": row,
            "write_with": "add_row(%s)  # pipeline_workbench.py in COMPOSIO_REMOTE_WORKBENCH; "
                          "dry_run=True first" % json.dumps(row, ensure_ascii=False)}


# ---------------------------------------------------------------------- MCP stdio

_S = {"type": "string"}
TOOLS = [
    {
        "name": "linkedin_search_jobs",
        "description": ("Search LinkedIn job postings via LinkedIn's public guest endpoint (no login, "
                        "no account). Returns id, title, company, location, post date and URL per job. "
                        "Paginates politely; max 100 results per call."),
        "inputSchema": {"type": "object", "properties": {
            "keywords": dict(_S, description="Search keywords, e.g. 'data analyst'"),
            "location": dict(_S, description="e.g. 'Chicago, IL', 'United States', 'New York, NY'"),
            "posted_within": {"type": "string", "enum": ["24h", "week", "month", "any"],
                              "default": "week"},
            "experience": {"type": "array", "items": {"type": "string", "enum": list(EXPERIENCE)}},
            "job_type": {"type": "array", "items": {"type": "string", "enum": list(JOB_TYPE)}},
            "workplace": {"type": "array", "items": {"type": "string", "enum": list(WORKPLACE)}},
            "company_ids": {"type": "array", "items": {"type": "string"},
                            "description": "LinkedIn numeric company ids (f_C)"},
            "sort": {"type": "string", "enum": ["recent", "relevant"], "default": "recent"},
            "limit": {"type": "integer", "default": 25, "minimum": 1, "maximum": MAX_RESULTS},
            "start": {"type": "integer", "default": 0, "description": "Offset; pass next_start to page"},
        }},
    },
    {
        "name": "linkedin_get_job",
        "description": ("Fetch one LinkedIn posting's full job description and metadata (seniority, "
                        "type, function, applicants, salary if shown, off-site apply URL). Accepts a job "
                        "id or any linkedin.com/jobs URL. format='markdown' returns the JD block the "
                        "resume / recruiter-filter skills take as input."),
        "inputSchema": {"type": "object", "required": ["job"], "properties": {
            "job": dict(_S, description="Job id, or a linkedin.com/jobs/view/... or currentJobId= URL"),
            "format": {"type": "string", "enum": ["json", "markdown"], "default": "json"},
        }},
    },
    {
        "name": "linkedin_track_job",
        "description": ("Fetch a LinkedIn posting and return its row for the user's Pipeline sheet "
                        "(columns A-E) plus the pipeline_workbench add_row() call that writes it. "
                        "Does not write: the sheet needs the user's Google auth via Composio."),
        "inputSchema": {"type": "object", "required": ["job"], "properties": {
            "job": dict(_S, description="Job id or linkedin.com/jobs URL"),
            "notes": dict(_S, description="Extra notes for column E"),
        }},
    },
]


def call_tool(name, args):
    args = args or {}
    if name == "linkedin_search_jobs":
        return search_jobs(**{k: v for k, v in args.items() if k in (
            "keywords", "location", "posted_within", "experience", "job_type", "workplace",
            "company_ids", "sort", "limit", "start")})
    if name == "linkedin_get_job":
        j = get_job(args["job"])
        return jd_markdown(j) if args.get("format") == "markdown" else j
    if name == "linkedin_track_job":
        return track_job(args["job"], args.get("notes", ""))
    raise LinkedInError("Unknown tool %r" % name)


def _reply(msg_id, result=None, error=None):
    out = {"jsonrpc": "2.0", "id": msg_id}
    if error is not None:
        out["error"] = error
    else:
        out["result"] = result
    sys.stdout.write(json.dumps(out) + "\n")
    sys.stdout.flush()


def serve():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except ValueError:
            _reply(None, error={"code": -32700, "message": "Parse error"})
            continue
        method, msg_id = msg.get("method"), msg.get("id")
        if msg_id is None:  # notification (e.g. notifications/initialized)
            continue
        params = msg.get("params") or {}
        if method == "initialize":
            _reply(msg_id, {
                "protocolVersion": params.get("protocolVersion", "2025-06-18"),
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            })
        elif method == "ping":
            _reply(msg_id, {})
        elif method == "tools/list":
            _reply(msg_id, {"tools": TOOLS})
        elif method == "tools/call":
            try:
                res = call_tool(params.get("name"), params.get("arguments"))
                text = res if isinstance(res, str) else json.dumps(res, indent=2, ensure_ascii=False)
                _reply(msg_id, {"content": [{"type": "text", "text": text}], "isError": False})
            except (LinkedInError, KeyError, TypeError, ValueError) as e:
                _reply(msg_id, {"content": [{"type": "text", "text": "Error: %s" % e}], "isError": True})
        else:
            _reply(msg_id, error={"code": -32601, "message": "Method not found: %s" % method})


# ---------------------------------------------------------------------------- CLI

def main(argv):
    if not argv:
        return serve()
    p = argparse.ArgumentParser(prog="server.py", description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("--keywords", default="")
    s.add_argument("--location", default="")
    s.add_argument("--posted-within", default="week", choices=list(POSTED))
    s.add_argument("--experience", help="comma list: " + ",".join(EXPERIENCE))
    s.add_argument("--job-type", help="comma list: " + ",".join(JOB_TYPE))
    s.add_argument("--workplace", help="comma list: " + ",".join(WORKPLACE))
    s.add_argument("--company-ids", help="comma list of LinkedIn company ids")
    s.add_argument("--sort", default="recent", choices=["recent", "relevant"])
    s.add_argument("--limit", type=int, default=25)
    s.add_argument("--start", type=int, default=0)
    g = sub.add_parser("get")
    g.add_argument("job")
    g.add_argument("--markdown", action="store_true")
    t = sub.add_parser("track")
    t.add_argument("job")
    t.add_argument("--notes", default="")
    a = p.parse_args(argv)
    try:
        if a.cmd == "search":
            out = search_jobs(a.keywords, a.location, a.posted_within, a.experience, a.job_type,
                              a.workplace, a.company_ids, a.sort, a.limit, a.start)
        elif a.cmd == "get":
            j = get_job(a.job)
            out = jd_markdown(j) if a.markdown else j
        else:
            out = track_job(a.job, a.notes)
    except LinkedInError as e:
        print(json.dumps({"error": str(e)}))
        return 1
    print(out if isinstance(out, str) else json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
