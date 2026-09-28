# Platform Guide — Job Sites, ATS Tricks, and Automation

---

## ATS Platform URL Patterns

When X-Raying a specific company:

| ATS | Career Page Pattern | Google X-Ray Prefix |
|-----|-------------------|-------------------|
| Greenhouse | `boards.greenhouse.io/[company]` | `site:boards.greenhouse.io` |
| Lever | `jobs.lever.co/[company]` | `site:jobs.lever.co` |
| Ashby | `jobs.ashbyhq.com/[company]` | `site:jobs.ashbyhq.com` |
| Workday | `[company].wd5.myworkdayjobs.com` | `site:myworkdayjobs.com` |
| iCIMS | `careers-[company].icims.com` | `site:icims.com "[company]"` |
| SmartRecruiters | `careers.smartrecruiters.com/[Company]` | `site:careers.smartrecruiters.com` |

**Tip:** native company career pages often post roles 24-48 hours before aggregators index them. Check the source.

---

## LinkedIn URL Filters

After running a search on LinkedIn, append these to the URL and press Enter.

### Time
| Filter | URL Parameter | Value |
|--------|--------------|-------|
| Last 1 hour | `&f_TPR=r3600` | 3,600 seconds — roles with almost no applicants yet |
| Last 24 hours | `&f_TPR=r86400` | 86,400 seconds |
| Last 7 days | `&f_TPR=r604800` | 604,800 seconds |
| Last 30 days | `&f_TPR=r2592000` | 2,592,000 seconds |

### Experience level
| Level | URL Parameter |
|-------|--------------|
| Internship | `&f_E=1` |
| Entry | `&f_E=2` |
| Associate | `&f_E=3` |
| Mid-Senior | `&f_E=4` |
| Director | `&f_E=5` |
| Executive | `&f_E=6` |

Pick the level(s) that match `profile/targets.md`; most experienced individual contributors want `&f_E=4`. Combine with commas: `&f_E=3,4`.

### Work type
| Type | URL Parameter |
|------|--------------|
| On-site | `&f_WT=1` |
| Remote | `&f_WT=2` |
| Hybrid | `&f_WT=3` |

### Combined example
```
&f_TPR=r86400&f_E=4&f_WT=2
```
Remote, mid-senior roles posted in the last 24 hours.

---

## LinkedIn Tips

- **"Open to Work" for recruiters only:** Settings > Job seeking preferences > Let recruiters know you're open. Visible in LinkedIn Recruiter, not on the public profile. No green banner.
- **Resume vs JD gap check:** LinkedIn's built-in tools can compare a resume to a JD to find keyword gaps. Use them for gap analysis, then edit by hand (don't let them rewrite).
- **Engage for visibility:** before applying, connect with the hiring manager or a team member with a personalized note, and engage with the company's recent posts, so the name is familiar when the application lands.
- **Alumni tool:** any company's LinkedIn page > People > filter by the user's school(s) or past employers (from `profile/me.md`) to find warm connections.

---

## Top Job Sites (general, ranked)

| Rank | Site | URL | Best For | Boolean Support |
|------|------|-----|----------|----------------|
| 1 | **Native company sites** | careers.[company].com | Freshest listings, direct to ATS | Varies by ATS |
| 2 | **LinkedIn** | linkedin.com/jobs | Networking + search, recruiter visibility | AND/OR/NOT, no wildcards, 3-4 nesting levels |
| 3 | **Google for Jobs** | google.com (any job query) | Aggregates company career pages | Space=AND, OR, minus for NOT, wildcards |
| 4 | **Wellfound** | wellfound.com | Startups, salary/equity transparency, founder access | Basic keyword + filters |
| 5 | **Indeed** | indeed.com | Volume | AND/OR/NOT, wildcards, 5+ nesting levels |
| 6 | **Otta / Welcome to the Jungle** | otta.com | Curated tech roles, salary shown | Filter-based |
| 7 | **YC Work at a Startup** | workatastartup.com | YC portfolio companies, one application to many | Filter-based |
| 8 | **ZipRecruiter** | ziprecruiter.com | AI matching that pitches the profile to recruiters | AND/OR/NOT, wildcards |
| 9 | **Glassdoor** | glassdoor.com | Culture research, interview questions, salary data | AND/OR/NOT, basic nesting |
| 10 | **Built In** | builtin.com | Tech roles by city | Filter-based |

**Google for Jobs:** not a separate site — a module Google shows for job queries, aggregating company career pages, LinkedIn and Glassdoor. It generally does not include Indeed.

Less relevant for experienced candidates: Handshake and College Recruiter (campus / early career). Include USAJOBS only if the user targets government roles.

---

## Niche Sites by Function / Vertical

Pick the rows that match `profile/targets.md`.

| Area | Sites |
|------|-------|
| Product management | Lenny's Job Board, Mind the Product jobs, Product Hunt jobs |
| Software engineering | Hacker News "Who is hiring?" (monthly thread), Wellfound, Stack Overflow-style dev boards |
| Design | Dribbble jobs, Behance jobs, Authentic Jobs |
| Marketing | Built In marketing filters, marketing community job boards |
| Operations / strategy | Built In ops filters, VC portfolio job boards |
| AI / ML | ai-jobs.net, Hugging Face jobs |
| Startups | Wellfound, YC Work at a Startup, VC portfolio boards (many VCs host one) |
| Climate | Climatebase, Work on Climate |
| Nonprofit / mission | Idealist |

---

## ATS / Resume Tips

- **Match keywords exactly:** if the JD says "Product Designer", don't write only "UX" — many filters do literal matching. Mirror the JD's terminology.
- **Accomplishments, not duties:** "Cut onboarding time 30% by redesigning the setup flow" beats "Responsible for onboarding."
- **Apply AND network:** find the hiring manager (Discover flow), send a personalized note (networking skill), and apply through the ATS. Both channels raise the odds.

---

## Automation — Set Up Alerts

### LinkedIn job alerts
1. Paste the Boolean string into LinkedIn Jobs search
2. Apply filters (date posted, experience level, remote)
3. Turn on the "Set alert" toggle at the top of the results
4. Set frequency to daily

### Google Alerts
1. Go to google.com/alerts
2. Paste a string like: `"<Title>" "<industry>" (hiring OR careers OR jobs)`
3. "How often": as-it-happens or once a day; "Sources": automatic
4. Good for press releases about new teams and hiring announcements

### Distill Web Monitor (browser extension)
For career pages without RSS:
1. Install Distill Web Monitor
2. Open the company's career page
3. Select the job-listing section to monitor
4. Set a check interval (e.g. every 6 hours)
5. Get notified when new roles appear

---

## The 30-Minute Method (networking + search combined)

1. Run the Boolean search → 10-15 results
2. Pick the top 3 matches
3. For each, find the hiring manager (Discover flow)
4. Send a targeted message on why the user fits (networking skill)
5. ALSO apply through the ATS, and log it in Pipeline

About 30 minutes, and far more effective than mass-applying.
