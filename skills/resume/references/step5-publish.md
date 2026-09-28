# Gate 5 — Export (only when the user asks)

The finished copy becomes a PDF the user can attach, plus (optionally) a link.

## Step 1 — Export the PDF to a file

Use Google Drive `download_file_content` on the copy with `exportMimeType: "application/pdf"`, and
save the result to a **file**. Never render or paste the PDF into the conversation; a PDF in the
chat costs tens of thousands of tokens per export.

The guard hook blocks `download_file_content` by default. This is the sanctioned export path, so
open it for this one export and close it straight after:

```
touch ~/.claude/cv-guard/allow-download      # 1. permit the export
# 2. download_file_content → write the PDF to a file (never into the chat)
rm ~/.claude/cv-guard/allow-download         # 3. close it again
```

- Name it `<config.name> - Resume - <Company>.pdf` (e.g. `Jordan Lee - Resume - Acme Corp.pdf`),
  using `name` from `profile/config.json`. Recruiters see the filename; keep it clean, no
  "v3-final".
- Run the line check on that file before handing it over:
  `python3 skills/resume/scripts/linefit.py "<file.pdf>" --over 2`. Exit 0 = one page and no
  bullet over two lines.
- Hand the user the file path (or the Drive download, depending on the session) and say it's
  ready to attach.

If Drive is not connected, name the missing connector ("See README → Connect your tools") and
tell the user to use File → Download → PDF in Google Docs.

## Step 2 — Optional: a shareable link

Only if the user wants a link (for outreach, a referral, a character-capped note).

**A direct Google Doc link.** Use the `/preview` view, not `/edit`:
`https://docs.google.com/document/d/<DOC_ID>/preview`, read-only with no editor chrome. The doc
must be shared *Anyone with the link: Viewer*, or every click lands on a request-access screen.

**Verify rather than trusting the share dialog.** Don't use `get_file_permissions` for this: it
returns only permissions set on the file itself, so a doc that is public because its parent folder
is shared comes back looking private. Fetch the link unauthenticated instead:

```
curl -sSL -o /tmp/p.html -w "%{http_code}\n" "https://docs.google.com/document/d/<DOC_ID>/preview"
# want: 200, the user's name in the body, and no "Request access" / "Sign in"
```

**On the user's website** (only if `profile/config.json` → `website` is set and the user asks).
How to add a link depends on their site; ask how they manage it. Useful rules whatever the stack:
- One path per tailored resume (`/resume-<company>-<role>`); keep `/resume` for the general one,
  since that link is already out in the world.
- If the site uses redirects, make them temporary (307/302), never permanent (308/301): browsers
  cache permanent redirects hard, so repointing later silently fails for anyone who already
  clicked.
- For character-capped contexts (a connection note), a short alias on the user's own domain beats
  a URL shortener, which reads as spam. If the long path is ever repointed, repoint the alias too.
- Never hand over a link until you've fetched it and seen it resolve to the resume.

## Step 3 — Update the tracker

Once the PDF exists (or the doc is confirmed complete), update the role's row with the Pipeline
workbench helpers in `skills/networking/references/pipeline.md` (sheet: `pipeline_sheet_id` in
`profile/config.json`). Never read a whole tab.

```
find(["<Company>"])                                   # row N, or "next empty row"
log(N, "<M/D> - resume exported", status="CV drafted")
set_cells(N, {"<base col>": "<base doc URL>", "<CV col>": "<new doc URL>", "<score col>": "<score>"})
```

No row → `add_row([...])`; don't skip the update because the role is missing. Put a one-line
summary of the angle emphasized in the notes column so future sessions know which version this is.
Don't set status to "CV drafted" until the doc is actually created and edited.

Using Composio for Sheets is fine; the whole-doc import ban is about resume Docs only.
