# Quick mode: a resume from your phone

For when the message is just a job link, or a link plus "make me a resume for this", usually from
the Claude app on a phone. The user wants a resume they can send in minutes, with as few replies
from them as possible. The wall in `SKILL.md` holds exactly as usual. What changes is how often
you stop to ask.

1. **Fetch the job** (`job-fetch`, or `linkedin-jobs` for a LinkedIn link). Reply in one line:
   role, company, and the role family it matches in `profile/positioning.md`.
2. **Gate 0 in one pass.** Grep the ledger for every requirement and check `profile/tailored.md`
   for a close past version (`step0-facts.md`). Stop to ask only if something blocks: a knockout
   (years, location, work authorization, a required credential) or a must-have with no evidence at
   all. Ask it in one message. Every other gap: go ahead with what the ledger has and list the gaps
   at the end.
3. **Gates 1–3 without stopping.** Write the swap list, run the voice pass, score before and after.
   Don't show the full swap list on a phone; show a short summary: the new tagline, how many
   bullets changed, score before → after. The full list is there if they ask.
4. **Gate 4 on a fresh copy** of the base (or of the closest past version). Nothing is edited in
   place, so it's safe to apply without a go-ahead: the user reviews the finished doc and can
   ask for changes. Check page fit with `CVFIT_<id>("<copy id>")` (send
   `skills/resume/scripts/cvcheck_workbench.py` once first; `step4-apply.md` → *After the round*).
   It needs no link sharing. Without Composio, `cvcheck.sh` works only on a doc already shared by
   link; never share the doc to run it, say the page fit is unchecked.
5. **Deliver it somewhere a phone can use.** A file saved inside this session is no use on a
   phone, so the PDF goes to their Drive:
   - `GOOGLEDOCS_EXPORT_DOCUMENT_AS_PDF` with `file_id` = the copy and
     `filename` = `<config.name> - Resume - <Company>.pdf`. It returns `download_url.s3url`.
   - `GOOGLEDRIVE_UPLOAD_FROM_URL` with `source_url` = that s3url, the same `name`,
     `mime_type: "application/pdf"`, `parent_folder_id` = `cv_folder_id`. The PDF lands next to
     the doc and can be attached from the phone's Files or Drive app.
   - Without Composio: give the doc link and say "In the Google Docs app: ⋯ → Share & export →
     Save as → PDF."
6. **Only if they want a link to share** (for example, a contact will forward it with a referral):
   ask once, "Make the PDF viewable by anyone with the link?" On yes,
   `GOOGLEDRIVE_CREATE_PERMISSION` with `type: "anyone"`, `role: "reader"` on the **PDF**, never on
   the editable doc. Confirm it took with `GOOGLEDRIVE_LIST_PERMISSIONS`, then hand over the link.
   Offer a two-line blurb for the contact to send with it: the third-person "why me" from the
   `networking` skill.
7. **Log it**: the line in `profile/tailored.md`, the role family's log in
   `profile/positioning.md`, a tracker row with status `CV ready`, and the meter.

Keep replies short: phone screens are small. Lead with the links, then the soft gaps worth fixing
before an interview.
