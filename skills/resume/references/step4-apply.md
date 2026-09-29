# Gate 4 — Apply the swap list as one round

**The round:** select and copy the base → read the copy's plaintext → apply every swap in one
batch → read back once → page fit: `CVFIT_<id>("<DOC_ID>")` in Composio's workbench (*After the
round*, step 1), or `cvcheck.sh` without Composio. Both return only the line-fit summary, never the
PDF → fix any over-long bullet → update the tracker. Run
this per **set**, never per bullet; running it per bullet is how a handful of bullets turn into
dozens of doc edits and PDF pulls.

If the repo's guard hook is installed, it enforces the wall on every doc call: it refuses
markdown/whole-doc imports, a replace without `match_case: true`, a `find_text` that matches 0 or
2+ times in the latest plaintext readback, and the first resume write before a Gate 0 grep. A
refusal names the rule: read it, re-read the doc, retry. Never insert or rewrite a paragraph to get
around it.

**Header and education lines come from the base, so check them.** The swap list covers the
tagline, bullets and skills line. Role header lines (titles, dates) and education lines usually
aren't in it, so a new copy silently keeps whatever its base had. When you read the copy's
plaintext, compare those lines against `profile/resume.md` and `profile/rules.md` (date format,
degree wording, honors wording, what is bold) and put any that differ in the swap list.

## Editing method

> **A resume the user has called final is read-only.** Sessions don't change the content of a
> finished doc, not to fix a typo, not to tighten a bullet. The moves below apply to a **fresh copy
> made this session**. If you spot a problem in a final doc, say so once and let the user decide.

> **Never a whole-doc or markdown import, any provider.** Banned: `import_to_google_doc`,
> `create_file` from HTML/markdown, `GOOGLEDOCS_UPDATE_DOCUMENT_SECTION_MARKDOWN`, and
> `GOOGLEDOCS_UPDATE_EXISTING_DOCUMENT` used as a rewrite. They rewrite the document and destroy
> native formatting: fonts, spacing, margins, bullet styles, heading levels, italic scope.
>
> **Allowed: targeted find→replace.** First-party `find_and_replace_doc`, or Composio
> `GOOGLEDOCS_REPLACE_ALL_TEXT`. Both issue the Docs API `replaceAllText` request, which never
> touches document structure: paragraph styles, bullets and run styles survive. Two gotchas:
> `match_case` defaults to `false` (always pass `true`), and it replaces *every* occurrence, so
> confirm each `find_text` is unique in the latest plaintext readback first.

**Preference order:** (1) first-party `find_and_replace_doc` → (2) Composio
`GOOGLEDOCS_REPLACE_ALL_TEXT` → (3) never a whole-doc import.

### Connector preflight: Drive alone is not enough

Google **Drive** (copy, search, read, export) and a Google **Docs edit** tool are separate
connectors. Before editing, confirm an edit tool is actually callable, not just that Drive
responds. Enabling a Docs option on the Drive connector does not add an edit tool; connectors
enabled mid-session usually need a fresh session to load.

**If only Drive is present:**
1. Never substitute a whole-doc import.
2. Copy the base with Drive `copy_file` (preserves formatting).
3. Hand the user the exact find → replace swap list to paste via Google Docs' own Edit → Find and
   replace (match case on). Formatting stays intact.
4. Tell them which connector is missing and "See README → Connect your tools". Don't keep asking
   them to re-toggle Drive.

## Base selection and the copy

1. **Use the base chosen at Gate 0**: the closest past version from `profile/tailored.md` (see
   `step0-facts.md` → *Start from the closest past version*), else `profile/config.json` →
   `base_cv_doc_id`. Still select final bullets fresh against the JD; a matched base is a starting
   point, not permission to skip tailoring. **Confirm the chosen base with the user before
   copying.** If neither `base_cv_doc_id` nor `cv_folder_id` is set, stop and offer the `setup`
   skill.
2. **Check for an existing tailored draft** for this company/role before starting from scratch. If
   one exists and was tailored in a prior session, diff-preview first: show the from/to swap list,
   wait for a go-ahead, then execute.
3. **Copy it** with Drive `copy_file` (or `GOOGLEDOCS_COPY_DOCUMENT`) into `cv_folder_id`, named
   `<Company>-<Role>_Resume-<config.name>`. All edits happen on the copy; never edit the base.
   The copy stays private: nothing in this gate needs it shared.

## Apply

**Checkpoint before the first write:** you have a list of individual replacements (not a
document); you will make one find→replace call per change; you have read the copy's plaintext
this round for exact `find_text` values. State this before proceeding.

```
# 1. Read the copy's plaintext for exact matching
get_doc_content({ document_id: "<copy-id>" })            # or GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT

# 2. One call per change, match_case true
find_and_replace_doc({ document_id: "<copy-id>",
                       find_text: "<exact text from the readback>",
                       replace_text: "<new text>", match_case: true })
# Composio: GOOGLEDOCS_REPLACE_ALL_TEXT with the same find/replace and match_case: true

# 3. Read back once; confirm every old text is gone and every new text is present
```

- Match `find_text` exactly as in the readback: punctuation, spaces, special characters.
- One bullet per call; never replace a whole section at once.
- Structural changes (add/remove a bullet, fix indent) use a batched structural update, not an
  import.

**Placeholder scan is a blocker.** On every read, scan first for `X`, `XX`, `XYZ`, `TODO`,
`[BRACKET NOTES]`, `<…>`. Flag each at the top of the review; block shipping until every one is
resolved or deleted.

**Re-run the verb scan after every batch.** Each swap can reintroduce a repeated opening verb.

## Known Google Docs API pitfalls

### Replaced text inherits the style of its first character
`replaceAllText` gives the new text the style of the first character it replaces. A line that
opens with a **bold** label (`Skills:`, `Interests:`) followed by plain items goes all-bold if
`find_text` starts at the label. Likewise a header line where a bold title is followed by a plain
span (dates, a location in parentheses) makes the span bold if the replace starts at the title.
1. **Prevent it:** start `find_text` after the label (the first plain item), never at the bold part.
2. **Fix it:** read the doc structure, find the paragraph, and send one targeted `updateTextStyle`
   with `{bold: false}`, `fields: "bold"`, over the range that should be plain (e.g. from
   paragraph start + `len("Skills: ")` to just before the paragraph's newline). That is a style
   patch on one range, not a rewrite, so the import ban doesn't apply.
Check it on every copy after the round: in the structure read, the label run is bold and the rest
is its own non-bold run. The bold/italic conventions themselves are in `profile/rules.md`.

### Empty replace leaves an orphan bullet marker
`replace_text: ""` removes the text but leaves the bullet paragraph: an empty `●` line. To remove a
bullet, delete the paragraph (a `deleteContentRange` spanning it, including its trailing newline,
using indices from the structure read). If the index math is fiddly, tell the user to delete the
orphan line manually and list it in the hand-off.

### Creating bullets resets indentation
A new bullet list defaults to a wide indent that wraps content onto extra lines. Always follow
`createParagraphBullets` with an `updateParagraphStyle` that restores the base doc's
`indentFirstLine` / `indentStart` (read them from an existing bullet in the structure).

### Zero-width borders error
`borderBottom` / `borderTop` with `width: {magnitude: 0}` returns `UNIT_UNSPECIFIED`. To hide a
border, set its color to white with `width: 0.75pt`.

### `tabStops` is not a valid `updateParagraphStyle` field
Including it in `fields` causes a 400.

## After the round

1. **Page fit: one page, no bullet over 2 lines.** Never pull the PDF into the chat. The copy is
   private, so run the check inside Composio's workbench, which reads the user's Drive as the user
   and needs no link sharing.
   - Send `skills/resume/scripts/cvcheck_workbench.py`, unchanged (nothing to fill in), as the
     `code_to_execute` of ONE `COMPOSIO_REMOTE_WORKBENCH` call, once per session. It prints
     `cvfit loaded as CVFIT_<id>`: the one name it binds, hashed from its code, so other sessions
     sharing the sandbox can't replace it. Never call a bare `cvfit()`.
   - Next call: `CVFIT_<id>("<COPY_DOC_ID>")` (a doc URL works; `over=3` allows 3-line bullets).
     It exports the doc in the sandbox, runs `linefit.py`, deletes the PDF and prints only the
     summary. Exit 0 fits, 1 over one page or a bullet too long, 2 bad doc id, 3 export failed,
     4 linefit failed. A `NameError` means the sandbox restarted: send the file again.
   - Exit 1 → tighten the flagged bullets (wording only) and run one more round, then re-check
     with the same one-liner.
   - No Composio connector: `bash skills/resume/scripts/cvcheck.sh <COPY_DOC_ID>` works only on a
     doc already shared by link (exit 3 otherwise). Never change the doc's sharing to make it
     work; tell the user the page fit is unchecked.
2. **Update the tracker** with the Pipeline workbench helpers
   (`skills/networking/references/pipeline.md`; sheet from `profile/config.json` →
   `pipeline_sheet_id`): `find()` the row, `log(N, "<M/D> - resume built from the <base> base",
   status="CV drafted")`, record the base and new doc URLs. **No row → `add_row()` it.** Never read
   the whole tab. No sheet configured → skip and say so.
