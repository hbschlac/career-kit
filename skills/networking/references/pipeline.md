# Pipeline: the job-application tracker

The user tracks every active application in one Google Sheet. Its ID and live tab come from
`profile/config.json`:

```json
{ "pipeline_sheet_id": "<sheet id>", "pipeline_tab": "<tab name, e.g. Oct-2026>" }
```

If either value is missing or still a placeholder, say so and offer to run the `setup` skill (it
can create the sheet with the header row below). Do not guess a sheet.

Access is through the **Composio Google Sheets** toolkit, ideally via `COMPOSIO_REMOTE_WORKBENCH`
and `skills/networking/scripts/pipeline_workbench.py`. If no Composio connector is present, say so
and point to README "Connect your tools".

**No Sheets connector? Markdown fallback.** If the user chose to keep the tracker in the repo
during setup, `profile/pipeline.md` holds the same columns (A–L below) as a markdown table, newest
row at the bottom. Read it with `grep -n "<Company>" profile/pipeline.md`, edit the one row, and
commit. Everything else in this file (one flat list, free-text Status, dated Log lines) still applies.

---

## Why it's a flat sheet (do not "improve" this)

The design is one list the user can scan. Treat these as rules:

- **One flat list per tab.** No kanban, no per-stage tabs, no filtered streams.
- **Status is a free-text cell**, not a set of booleans. The user overwrites it with whatever word
  they want.
- **Do not add columns, tabs or sections without asking.** Every addition costs scannability, which
  is the reason the sheet exists.

## Tabs

Write only to the tab named in `pipeline_tab` (header in row 1, frozen; one row per role from row
2). Some users keep one tab per month. When a new period starts and no tab exists for it, **ask the
user** before creating one, then update `pipeline_tab` in `profile/config.json`. Always name the
tab in every range (`'<Tab>'!A70:L70`) because the first tab can change. Other tabs (people lists,
archived months) are not job lists; do not write roles there.

## Columns

| Col | Field | What goes in it |
|-----|-------|-----------------|
| A | Company | Company **and role** in one cell: `Acme Corp, Senior Analyst, Growth` |
| B | Job App | Canonical posting URL (a second URL or a short note may follow on a new line) |
| C | Status | Free text: `CV drafted`, `CV in progress`, `Applied`, `Rejected`, `No apply`, anything |
| D | Log | Dated history, newest first: `10/22 - submitted app` then `10/18 - CV built from base` |
| E | Notes | Location, comp band, req ID, what the role actually is, cover-letter doc link |
| F | CV for application | Link to the CV actually sent (often blank until the user applies) |
| G | Existing CV | An older CV already tailored to this exact req, if one exists |
| H | Base CV | Link to the CV the new one was copied from |
| I | CV for this app (new) | **Link to the tailored Google Doc you built** |
| J | Recruiter score | recruiter-filter score as a bare number (`84`). Blank if none was run; never self-grade to fill it |
| K | Gaps / to add | Fit read, gaps, what not to claim, trades made |
| L | Fit | `Strong` / `Medium` / `Low`. The user's call; leave blank unless they said it |

## Row colour follows Status

| Status (C) contains, any case | Row A to L |
|---|---|
| `reject` (`Rejected`, `applied - rejected`) | light red `#F4CCCC` |
| `no apply` / `not apply` / `didn't apply` / `did not apply` / `won't apply` | light grey `#D9D9D9` |
| the word `applied` | light green `#D9EAD3` |
| anything else (`CV drafted`, `Referral submitted`, `CV ready - not submitted`) | no colour |

- This is **conditional formatting on the tab**, not painted fills, so the colour follows the Status
  cell whoever edits it. **Never paint row colours by hand** or with `set_cells`; just write the
  status. First match wins, so a status that says both applied and rejected is red.
- **Every new tab needs it once:** after the user approves the tab, run
  `print(status_colors("<Tab>"))`. It is idempotent (replaces its own three rules, leaves others
  alone). The regexes and colours live in `STATUS_COLORS` in the workbench script.
- For a status that should count as applied but does not say "applied" (e.g. `Referral submitted`),
  write `Applied` in C and put the detail in the Log. Do not widen the regex without asking.

---

## Reading and writing it cheaply

**A full-tab read is expensive**: a tab with ~100 roles is roughly 77k characters (~19k tokens) per
read, and a Drive `read_file_content` returns every tab and is bigger still. Never read a whole tab
into the conversation.

**Use the workbench helpers.** `skills/networking/scripts/pipeline_workbench.py` runs inside
Composio's remote sandbox, so the sheet is read there and only what you print comes back.

1. Replace the placeholders `S = "<PIPELINE_SHEET_ID>"` and `TAB = "<PIPELINE_TAB>"` with the
   values from `profile/config.json`, then send the whole file as the `code_to_execute` of **one**
   `COMPOSIO_REMOTE_WORKBENCH` call (~1k tokens, once per session; the sandbox keeps the functions).
2. Then, in later workbench calls:

| Need | Call | Returns |
|------|------|---------|
| Is this role tracked? which row? | `print(find(["Acme"]))` | matching rows (A to E, trimmed) + next empty row |
| Everything in one row | `print(row(74))` | that row, labelled by column |
| Status change / log a step | `print(log(74, "10/25 - submitted app", status="Applied"))` | prepends to Log (D), never overwrites; sets C if given |
| Any other cell | `print(set_cells(74, {"J": "84", "I": "<doc url>"}))` | one write per cell |
| New role | `print(add_row(["<Company>, <Role>", "<url>", "CV drafted", "<M/D> - ...", "<notes>", "", "", "<base CV>", "<new CV>", "<score>", "<gaps>"]))` | refuses if column A already has that exact entry |
| New tab's colours | `print(status_colors("<Tab>"))` | installs the Status colour rules |

Pass `dry_run=True` to any write to see the exact range and values first.

**If the workbench is not available,** use a direct `GOOGLESHEETS_VALUES_GET` of **one column**
(`'<Tab>'!A:A`) to find the row, then **one row** (`'<Tab>'!A74:L74`). Write with
`GOOGLESHEETS_VALUES_UPDATE`, one row's cells at a time, `value_input_option: "USER_ENTERED"`.
Prepend to Log (D); never overwrite earlier entries.

**Every CV you build gets a row.** If the role is not in the tracker yet, add it. Only updating an
existing row is how applications go missing.

> **Composio scope:** the resume skill's rule against whole-document imports applies to Google
> Docs editing. The tracker is a spreadsheet, and Composio Sheets is the right tool for it.

---

## Your responsibility as a session

- **`find()` the role at the start** of any application work, so you do not duplicate another
  session
- **Add or update the row** when you finish something real: a CV built, an application sent
- **Do not mark "Applied"** unless it was actually submitted
- **Do not invent a status** for a role whose state you do not know; ask the user
- **Notes are for humans:** comp, fit read, what is blocking, applied date
