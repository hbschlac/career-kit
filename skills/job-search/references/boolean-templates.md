# Boolean Search Templates

Build every string from the user's `profile/targets.md`: role titles, industries, seniority and
exclusions. The examples below show several functions; swap in the user's own terms.

---

## Template Structure

Every search string follows this 4-block structure, with NOT at the end (best compatibility across platforms):

```
(ROLE KEYWORDS) AND (INDUSTRY KEYWORDS) AND (SENIORITY/FUNCTION KEYWORDS) NOT (EXCLUSION KEYWORDS)
```

The AND blocks create a strict intersection: a result must match ALL blocks. This trades volume for precision.

---

## LinkedIn / Indeed

**Syntax rules:**
- Operators MUST be UPPERCASE: `AND`, `OR`, `NOT`
- Exact phrases in straight double quotes: `"Product Designer"`
- Group with parentheses: `(A OR B)`
- LinkedIn: ~1,000 char limit (free), ~2,000 (Recruiter); max 3-4 nesting levels; NO wildcards
- Indeed: no strict char limit; supports wildcards `*`; NOT can be inconsistent — keep the NOT block at the end
- Do NOT use the minus sign (-) on LinkedIn or Indeed
- Do NOT use AND NOT — just NOT (saves characters, same result)

### Generic pattern

```
("<Title 1>" OR "<Title 2>" OR "<Title 3>" OR "<Title 4>") AND ("<industry 1>" OR "<industry 2>" OR "<industry 3>") NOT (intern OR internship OR "new grad" OR "entry level" OR junior OR <too-senior titles> OR <wrong-domain terms>)
```

### Role examples

**Product manager:**
```
("Senior Product Manager" OR "Product Manager" OR "Staff Product Manager" OR "Product Lead") AND ("SaaS" OR "fintech" OR "marketplace" OR "developer tools") NOT (intern OR internship OR "new grad" OR junior OR associate OR director OR VP)
```

**Software engineer:**
```
("Senior Software Engineer" OR "Software Engineer" OR "Backend Engineer" OR "Full Stack Engineer" OR "Staff Engineer") AND ("Python" OR "Go" OR "distributed systems" OR "APIs") NOT (intern OR internship OR "new grad" OR junior OR manager OR director OR "QA")
```

**Designer:**
```
("Product Designer" OR "Senior Product Designer" OR "UX Designer" OR "Design Lead") AND ("SaaS" OR "consumer" OR "mobile" OR "design systems") NOT (intern OR internship OR junior OR "graphic designer" OR "interior" OR director)
```

**Marketing:**
```
("Product Marketing Manager" OR "Growth Marketing Manager" OR "Lifecycle Marketing Manager" OR "Senior Marketing Manager") AND ("B2B" OR "SaaS" OR "demand generation" OR "go-to-market") NOT (intern OR internship OR coordinator OR junior OR VP OR "field marketing")
```

**Operations:**
```
("Operations Manager" OR "Business Operations" OR "Strategy and Operations" OR "BizOps" OR "Program Manager") AND ("startup" OR "SaaS" OR "marketplace" OR "fintech") NOT (intern OR internship OR "warehouse" OR "shift" OR junior OR VP)
```

### Focus variations
Narrow a string by swapping the industry block for a theme block:

- **AI-focused:** `AND ("artificial intelligence" OR "machine learning" OR "generative AI" OR "LLM" OR "AI agent")`
- **Growth-focused:** `AND ("growth" OR "adoption" OR "activation" OR "engagement" OR "retention" OR "onboarding")`
- **Commerce-focused:** `AND ("ecommerce" OR "marketplace" OR "retail tech" OR "checkout" OR "conversion")`

---

## Google

**Syntax rules:**
- Space between terms = AND (do NOT write "AND")
- `OR` must be UPPERCASE
- Minus sign `-` for exclusion (NOT is ignored by Google)
- No space between `-` and the word: `-intern`
- Supports wildcards `*`
- Supports `site:` for X-Ray
- ~2,000 chars practical limit; unlimited nesting

### Generic pattern

```
("<Title 1>" OR "<Title 2>" OR "<Title 3>") ("<industry 1>" OR "<industry 2>") ("careers" OR "jobs" OR "hiring" OR "apply") -intern -internship -"new grad" -"entry level" -junior
```

### Example (software engineer)
```
("Senior Software Engineer" OR "Backend Engineer" OR "Staff Engineer") ("fintech" OR "payments") ("careers" OR "jobs" OR "hiring" OR "apply") -intern -internship -"new grad" -junior -manager
```

### With a company filter
Append the company name in quotes:
```
("Product Designer" OR "Senior Product Designer") ("careers" OR "jobs" OR "hiring") "Acme Corp" -intern -junior
```

---

## Google X-Ray Templates

X-Ray finds jobs directly on ATS platforms before aggregators index them. Company career pages
often post 24-48 hours before LinkedIn / Indeed pick the role up.

### By ATS platform

Replace the title block with the user's titles.

**Greenhouse:**
```
site:boards.greenhouse.io ("<Title 1>" OR "<Title 2>") -intern -junior
```

**Lever:**
```
site:jobs.lever.co ("<Title 1>" OR "<Title 2>") -intern -junior
```

**Ashby:**
```
site:jobs.ashbyhq.com ("<Title 1>" OR "<Title 2>") -intern -junior
```

**Workday:**
```
site:myworkdayjobs.com ("<Title 1>" OR "<Title 2>") -intern -junior
```

### Company-specific X-Ray
Replace `[COMPANY]`:
```
site:boards.greenhouse.io "[COMPANY]" ("<Title 1>" OR "<Title 2>")
```
```
site:jobs.lever.co "[COMPANY]" ("<Title 1>" OR "<Title 2>")
```

### Multi-ATS scan
```
(site:boards.greenhouse.io OR site:jobs.lever.co OR site:jobs.ashbyhq.com) ("<Title 1>" OR "<Title 2>") ("<industry 1>" OR "<industry 2>") -intern -junior
```

Example (marketing):
```
(site:boards.greenhouse.io OR site:jobs.lever.co OR site:jobs.ashbyhq.com) ("Product Marketing Manager" OR "Growth Marketing Manager") ("SaaS" OR "B2B") -intern -coordinator
```

---

## Platform Comparison

| Feature | LinkedIn | Indeed | Google |
|---------|----------|--------|--------|
| **AND syntax** | `AND` (UPPERCASE) | `AND` (UPPERCASE) | space (implicit) |
| **OR syntax** | `OR` (UPPERCASE) | `OR` (UPPERCASE) | `OR` (UPPERCASE) |
| **NOT syntax** | `NOT` (UPPERCASE) | `NOT` (UPPERCASE) | `-` (minus, no space) |
| **Wildcard** | Not supported | `*` supported | `*` supported |
| **Exact phrase** | `"straight quotes"` | `"straight quotes"` | `"straight quotes"` |
| **Nesting `()`** | 3-4 levels max | 5+ levels | Unlimited |
| **Char limit** | ~1,000 (free) / ~2,000 (Recruiter) | No strict limit | ~2,000 practical |
| **site: operator** | No | No | Yes |
| **AND NOT vs NOT** | Both work; `NOT` preferred | Both work; `NOT` preferred | Only `-` works |

---

## Best Practices

1. **Always put the NOT block at the end** — better compatibility on Indeed, cleaner logic
2. **Keep LinkedIn strings under 800 chars** to leave room for platform additions
3. **Use OR generously for titles** — companies name the same role inconsistently
4. **Keep industry terms in the keyword/body block**, not the title search — they appear in the JD body
5. **For Google, always include `("careers" OR "jobs" OR "hiring")`** to filter out news articles
6. **Too narrow?** Drop the industry AND block and use the platform's industry filter instead
7. **Too broad?** Add seniority terms, e.g. `AND ("senior" OR "staff" OR "lead")`
8. **Exclude neighbouring functions** that share keywords (an engineer search may want `NOT "sales engineer"`; a designer search `NOT "graphic designer"`)
