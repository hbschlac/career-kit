# Pipeline sheet helpers. Paste this whole file as ONE COMPOSIO_REMOTE_WORKBENCH call, then call
# the functions in later workbench calls. The sheet is read inside Composio's sandbox and only the
# lines you print come back into the conversation.
#
# BEFORE SENDING: Claude substitutes the two placeholders below with the values from
# profile/config.json ("pipeline_sheet_id" and "pipeline_tab"). Never commit real values into this
# file; it lives in skills/ and must stay generic. If config.json has no values yet, stop and offer
# the setup skill instead of guessing.
#
# A full-tab VALUES_GET of a ~100-role tab is ~77k chars (~19k tokens) per read; find() returning
# a few matching rows is ~2k chars. Never read the whole tab into the chat.
#
#   print(find(["Acme"]))                 # matching rows with row numbers + next empty row
#   print(row(74))                        # one full row, all columns, labelled
#   print(log(74, "10/25 - applied", status="Applied", dry_run=True))  # prepend to Log (D)
#   print(add_row(["Co, Role", "url", "CV drafted", "10/25 - CV built from base", ...], dry_run=True))
#   print(set_cells(74, {"J": "84"}, dry_run=True))                   # any other cells
#   print(status_colors("<Tab>"))         # once per new tab: Status -> row colour rules
#
# Always dry_run=True first when unsure; the write returns the range it changed.
import os, time

S = "<PIPELINE_SHEET_ID>"   # from profile/config.json -> pipeline_sheet_id
TAB = "<PIPELINE_TAB>"      # from profile/config.json -> pipeline_tab; check tabs() when it turns over
COLS = "ABCDEFGHIJKL"
HEAD = ["Company", "Job App", "Status", "Log", "Notes", "CV for application", "Existing CV",
        "Base CV", "CV for this app (new)", "Recruiter score", "Gaps / to add", "Fit"]

if S.startswith("<") or TAB.startswith("<"):
    raise RuntimeError("Fill S and TAB from profile/config.json before loading these helpers.")


def _get(rng):
    r, e = run_composio_tool("GOOGLESHEETS_VALUES_GET", {"spreadsheet_id": S, "range": rng})
    if e: raise RuntimeError(e)
    return r["data"].get("values", [])


def _put(rng, values, dry_run):
    if dry_run: return f"DRY RUN - would write {rng}: {values}"
    r, e = run_composio_tool("GOOGLESHEETS_VALUES_UPDATE", {"spreadsheet_id": S, "range": rng,
                             "value_input_option": "USER_ENTERED", "values": values})
    if e: raise RuntimeError(e)
    return f"wrote {rng}"


def tabs():
    r, e = run_composio_tool("GOOGLESHEETS_GET_SPREADSHEET_INFO", {"spreadsheet_id": S})
    return [s["properties"]["title"] for s in r["data"]["sheets"]]


def _next_empty(tab=TAB):
    a = _get(f"'{tab}'!A:A")
    return max((i + 1 for i, v in enumerate(a) if v and v[0].strip()), default=1) + 1


def find(terms, tab=TAB, width=160):
    v = _get(f"'{tab}'!A:L")
    last = max((i + 1 for i, r in enumerate(v) if r and r[0].strip()), default=1)
    out = [f"{tab}: {last - 1} roles, next empty row {last + 1}"]
    for i, r in enumerate(v[1:], start=2):
        if any(t.lower() in " ".join(r).lower() for t in terms):
            out.append(f"row {i}: " + " | ".join(c.replace("\n", " / ")[:width] for c in r[:5]))
    return "\n".join(out) if len(out) > 1 else out[0] + f"\nno row matches {terms}"


def row(n, tab=TAB):
    v = (_get(f"'{tab}'!A{n}:L{n}") or [[]])[0]
    return "\n".join(f"{COLS[i]} {HEAD[i]}: {c}" for i, c in enumerate(v) if c)


def log(n, entry, status=None, tab=TAB, dry_run=False):
    """Prepend a dated line to Log (D); never overwrites earlier entries."""
    old = (_get(f"'{tab}'!D{n}") or [[""]])[0]
    new = entry + ("\n" + old[0] if old and old[0] else "")
    if status is None: return _put(f"'{tab}'!D{n}", [[new]], dry_run)
    return _put(f"'{tab}'!C{n}:D{n}", [[status, new]], dry_run)


def set_cells(n, cells, tab=TAB, dry_run=False):
    return "\n".join(_put(f"'{tab}'!{c}{n}", [[v]], dry_run) for c, v in cells.items())


def add_row(values, tab=TAB, dry_run=False):
    """Append one role at the first empty row. values = A..K (L only if the user gave the fit)."""
    key = values[0].strip().lower()
    if any(r and r[0].strip().lower() == key for r in _get(f"'{tab}'!A:A")):
        return f"'{values[0]}' already has a row - use find() and log() instead"
    n = _next_empty(tab)
    return _put(f"'{tab}'!A{n}:{COLS[len(values) - 1]}{n}", [values], dry_run)


# Session meter (used by the career-review skill). Counts only - never a company, role, doc id
# or email text.
METER_TAB = "Meter"
METER_HEAD = ["date", "session", "kind", "doc_edits", "readbacks", "pdf_pulls", "rubric_runs",
              "markdown_imports", "cvcheck_runs", "sandbox_exports", "sheet_calls", "api_calls",
              "user_messages", "peak_context_k", "input_k", "output_k", "compactions", "note"]


def meter_row(m, kind=None, note="", dry_run=False):
    """Append one session's meter dict to the Meter tab. Creates the tab on first use.
    kind defaults to the session's first kit skill; the skills used go in the note column."""
    kind = kind or (m.get("skills") or ["session"])[0]
    note = note or ("skills: " + ", ".join(m.get("skills") or []) if m.get("skills") else "")
    if METER_TAB not in tabs():
        if dry_run: return f"DRY RUN - would create tab {METER_TAB}"
        run_composio_tool("GOOGLESHEETS_ADD_SHEET", {"spreadsheet_id": S, "title": METER_TAB,
                                                     "force_unique": False})
        _put(f"'{METER_TAB}'!A1:R1", [METER_HEAD], False)
    cv = m.get("cv", {})
    vals = [time.strftime("%Y-%m-%d"), os.path.basename(m.get("transcript", "?"))[:8], kind,
            *[cv.get(k, 0) for k in METER_HEAD[3:11]],
            m.get("api_calls", 0), m.get("user_messages", 0), m.get("peak_context_tokens", 0) // 1000,
            m.get("total_input_processed", 0) // 1000, m.get("output_tokens", 0) // 1000,
            m.get("compactions", 0), note]
    n = _next_empty(METER_TAB)
    return _put(f"'{METER_TAB}'!A{n}:R{n}", [vals], dry_run)


def meter_rows(last=20):
    """The last `last` sessions as compact lines, for the weekly career-review."""
    v = _get(f"'{METER_TAB}'!A:R")
    return "\n".join(" | ".join(map(str, r)) for r in [v[0]] + v[1:][-last:]) if v else "no Meter tab yet"


# Row colour follows the Status cell (C), via conditional formatting, so it updates itself whoever
# edits the cell. First matching rule wins, so order matters: a status that says both "applied"
# and "rejected" goes red. Free text is matched loosely (any case, any wording); "CV ready - not
# submitted" and "Referral submitted" stay uncoloured on purpose.
STATUS_COLORS = [  # (regex on lower(C), hex)  light red / light grey / light green
    ("reject", "#F4CCCC"),
    ("no apply|not apply|didn.?t apply|did not apply|won.?t apply", "#D9D9D9"),
    (r"\bapplied\b", "#D9EAD3"),
]


def status_colors(tab=TAB, dry_run=False):
    """Install the Status -> row-colour rules on a tab (A2:L). Idempotent: removes old ones first."""
    r, e = run_composio_tool("GOOGLESHEETS_GET_SPREADSHEET_INFO",
                             {"spreadsheet_id": S, "fields": "sheets(properties,conditionalFormats)"})
    if e: raise RuntimeError(e)
    sh = next(s for s in r["data"]["sheets"] if s["properties"]["title"] == tab)
    sid, rows = sh["properties"]["sheetId"], sh["properties"]["gridProperties"]["rowCount"]
    ours = {f'=REGEXMATCH(LOWER($C2),"{rx}")' for rx, _ in STATUS_COLORS}
    stale = [i for i, c in enumerate(sh.get("conditionalFormats", []))
             if (c.get("booleanRule", {}).get("condition", {}).get("values") or [{}])[0]
                .get("userEnteredValue") in ours]
    if dry_run: return f"DRY RUN - '{tab}': delete {len(stale)} old, add {len(STATUS_COLORS)} rules"
    for i in reversed(stale):
        _, e = run_composio_tool("GOOGLESHEETS_MUTATE_CONDITIONAL_FORMAT_RULES",
                                 {"spreadsheet_id": S, "sheet_id": sid, "operation": "DELETE", "index": i})
        if e: raise RuntimeError(e)
    rng = {"sheetId": sid, "startRowIndex": 1, "endRowIndex": rows, "startColumnIndex": 0, "endColumnIndex": 12}
    for i, (rx, hx) in enumerate(STATUS_COLORS):
        rgb = {k: int(hx[j:j + 2], 16) / 255 for k, j in (("red", 1), ("green", 3), ("blue", 5))}
        _, e = run_composio_tool("GOOGLESHEETS_MUTATE_CONDITIONAL_FORMAT_RULES", {
            "spreadsheet_id": S, "sheet_id": sid, "operation": "ADD", "index": i,
            "rule": {"ranges": [rng], "booleanRule": {
                "condition": {"type": "CUSTOM_FORMULA",
                              "values": [{"userEnteredValue": f'=REGEXMATCH(LOWER($C2),"{rx}")'}]},
                "format": {"backgroundColor": rgb}}}})
        if e: raise RuntimeError(e)
    return f"status colours set on '{tab}' ({len(STATUS_COLORS)} rules, {len(stale)} old removed)"


print("pipeline helpers loaded:", TAB)
