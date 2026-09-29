#!/usr/bin/env python3
"""Offline tests for mcp/linkedin-jobs/server.py — run: python3 tests/test_linkedin_jobs.py

No network: LinkedIn is replaced by canned pages. Covers the filters LinkedIn's public search
ignores (seniority, years, industry, function, pay, remote), which the server applies itself by
reading each posting.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mcp" / "linkedin-jobs"))
import server as s  # noqa: E402

failures = []


def check(name, ok):
    print(("ok   " if ok else "FAIL ") + name)
    if not ok:
        failures.append(name)


# --- parsers
check("years: '5+ years of experience' -> 5", s.years_asked("5+ years of experience in product") == 5)
check("years: a range counts its low end", s.years_asked("3-5 years experience") == 3)
check("years: 'minimum of 7 years of relevant experience' -> 7",
      s.years_asked("Minimum of 7 years of relevant experience") == 7)
check("years: 'founded 10 years ago' is not a requirement", s.years_asked("founded 10 years ago") is None)
check("years: required beats preferred (smallest wins)",
      s.years_asked("2+ years exp required; 8+ years of experience preferred") == 2)
check("pay: top of an annual range", s.salary_top("$150,000.00/yr - $200,000.00/yr") == 200000)
check("pay: hourly becomes yearly", s.salary_top("$60/hr - $80/hr") == 166400)
check("pay: K amounts", s.salary_top("$120K–$150K") == 150000)
check("pay: none listed", s.salary_top("") is None)
check("levels: 6 years -> mid-senior", s.levels_for_years(6) == ["mid-senior"])
check("levels: 12 years -> mid-senior + director", s.levels_for_years(12) == ["mid-senior", "director"])
check("workplace: remote from the location", s.workplace_of({"location": "United States (Remote)"}) == ["remote"])

# --- one posting against the criteria
want = {"levels": ["mid-senior"], "max_years_asked": 8, "industries": ["software"], "functions": [],
        "job_types": [], "min_salary": 150000, "workplace": ["remote"]}
good = {"seniority": "Mid-Senior level", "years_asked": 5, "industries": "Software Development",
        "salary_top": 180000, "workplace_guess": ["remote"]}
ok, why, unknown = s.check_job(good, want)
check("a matching posting is kept", ok and not why and not unknown)
ok, why, _ = s.check_job(dict(good, years_asked=10), want)
check("too many years asked -> dropped with the reason", not ok and why == ["asks for 10+ years"])
ok, why, _ = s.check_job(dict(good, industries="Hospitals and Health Care"), want)
check("wrong industry -> dropped", not ok and "industries is Hospitals and Health Care" in why)
ok, why, unknown = s.check_job(dict(good, salary_top=None), want)
check("no pay listed -> kept, marked unknown", ok and unknown == ["salary"])
ok, why, _ = s.check_job(dict(good, seniority="Director"), want)
check("wrong seniority -> dropped", not ok and why == ["seniority is Director"])
ok, _, unknown = s.check_job(dict(good, seniority="Not Applicable"), want)
check("'Not Applicable' seniority -> kept, marked unknown", ok and "seniority" in unknown)

# --- the whole search, with LinkedIn replaced by canned pages
CARD = ('<li><div data-entity-urn="urn:li:jobPosting:{id}"><h3 class="base-search-card__title">{t}</h3>'
        '<h4 class="base-search-card__subtitle">Acme</h4><span class="job-search-card__location">'
        'New York, NY</span><time datetime="2026-09-28">1 day ago</time></div></li>')
PAGE = "".join(CARD.format(id=1000000 + i, t="Product Manager %d" % i) for i in range(4))
DETAILS = {
    "1000000": {"seniority": "Mid-Senior level", "industries": "Software Development",
                "description": "Remote. 5+ years of experience. $160,000 - $190,000"},
    "1000001": {"seniority": "Mid-Senior level", "industries": "Software Development",
                "description": "Remote. 12+ years of experience required."},
    "1000002": {"seniority": "Entry level", "industries": "Software Development",
                "description": "Remote role. 1+ years of experience."},
    "1000003": {"seniority": "Mid-Senior level", "industries": "Banking",
                "description": "Remote. 4+ years of experience."},
}
calls = {"search": 0, "get": 0}


def fake_get(url, params=None):
    calls["search"] += 1
    return PAGE if params and params.get("start", 0) == 0 else ""


def fake_job(job):
    calls["get"] += 1
    jid = s.job_id_from(job)
    d = {"id": jid, "title": "PM", "company": "Acme", "location": "New York, NY", "salary": "",
         "job_function": "Product Management", "employment_type": "Full-time", "closed": False}
    d.update(DETAILS[jid])
    return d


s._get, s.get_job = fake_get, fake_job
s.PAGE_PAUSE_S = s.SCREEN_PAUSE_S = 0
plain = s.search_jobs(keywords="product manager", limit=4)
check("no filters -> no postings read", calls["get"] == 0 and plain["count"] == 4 and "screened" not in plain)
out = s.call_tool("linkedin_search_jobs", {"keywords": "product manager", "years": 6,
                                           "max_years_asked": 8, "industries": ["software"],
                                           "workplace": ["remote"], "limit": 4})
ids = [j["id"] for j in out["jobs"]]
check("screened search keeps only the matching posting", ids == ["1000000"])
why = {d["id"]: d["why"] for d in out["screened"]["dropped"]}
check("each dropped posting says why", why == {"1000001": ["asks for 12+ years"],
                                               "1000002": ["seniority is Entry level"],
                                               "1000003": ["industries is Banking"]})
check("years picked the seniority levels", out["screened"]["levels_from_years"] == ["mid-senior"])
check("kept rows carry the checked fields", out["jobs"][0]["years_asked"] == 5
      and out["jobs"][0]["salary_top"] == 190000 and out["jobs"][0]["workplace_guess"] == ["remote"])

calls["get"] = 0
capped = s.search_jobs(keywords="pm", workplace="remote", check_limit=2, limit=4)
check("check_limit caps the postings read", calls["get"] == 2 and "check_limit" in capped["screened"]["stopped"])
check("next_start resumes at the first posting not read", capped["next_start"] == 2)
check("an unscreened page resumes after the last card shown",
      s.search_jobs(keywords="pm", limit=3)["next_start"] == 3)
calls["get"] = 0
exact = s.search_jobs(keywords="pm", workplace="remote", check_limit=4, limit=5)
check("reading every card fetched still says the check_limit was hit",
      calls["get"] == 4 and "check_limit" in exact["screened"].get("stopped", ""))


def limited(job):
    raise s.LinkedInError("LinkedIn rate-limited this IP (429).")


s.get_job = limited
stopped = s.search_jobs(keywords="pm", industries="software", limit=4)
check("a rate limit stops screening politely instead of failing",
      stopped["count"] == 0 and "429" in stopped["screened"]["stopped"])

try:
    s.search_jobs(keywords="pm", experience="senior-ish")
    check("an unknown experience label is refused", False)
except s.LinkedInError:
    check("an unknown experience label is refused", True)

print()
if failures:
    print(f"{len(failures)} FAILED: " + ", ".join(failures))
    sys.exit(1)
print("all linkedin-jobs tests passed")
