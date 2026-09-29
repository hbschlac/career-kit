#!/usr/bin/env bash
# cvcheck.sh DOC_ID_OR_URL [--over N]
#
# Export the resume's PDF to a FILE and print only linefit's summary: page count and any bullet
# over N lines (default 2). The PDF never enters the conversation: ~30 tokens of output instead of
# the tens of thousands a PDF costs in the chat.
#
# Exit codes: 0 fits · 1 over one page or a bullet too long · 3 export failed (doc not
# link-readable) · 2 usage.
#
# Needs only bash, curl and stdlib python3. The export is unauthenticated, so it reads only a doc
# already shared "anyone with the link"; a resume copy is normally private, and then it exits 3.
# Never change a doc's sharing to get round that: exit 3 names cvcheck_workbench.py, the same check
# run inside Composio's sandbox, which reads the user's Drive as the user.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
[[ $# -ge 1 ]] || { echo "usage: cvcheck.sh DOC_ID_OR_URL [--over N]" >&2; exit 2; }
id="$(sed -nE 's#.*/d/([A-Za-z0-9_-]+).*#\1#p' <<<"$1")"; [[ -n "$id" ]] || id="$1"; shift
over=2
if [[ "${1:-}" == "--over" && -n "${2:-}" ]]; then over="$2"; fi
[[ "$id" =~ ^[A-Za-z0-9_-]{20,}$ ]] || { echo "cvcheck: '$id' does not look like a Google Doc id" >&2; exit 2; }

out="${TMPDIR:-/tmp}/cv-$id.pdf"
if ! curl -sSL --max-time 60 "https://docs.google.com/document/d/$id/export?format=pdf" -o "$out" \
   || ! head -c 4 "$out" 2>/dev/null | grep -q '%PDF'; then
  rm -f "$out"
  args="\"$id\""; [[ "$over" == 2 ]] || args+=", over=$over"
  echo "cvcheck: export failed — the doc is not link-readable (a resume copy is normally private). Do not change its sharing. Run the same check inside Composio's sandbox, which reads the user's Drive as the user:"
  echo "  1. send $HERE/cvcheck_workbench.py, unchanged, as ONE COMPOSIO_REMOTE_WORKBENCH call; it prints the one name it binds, CVFIT_<id>"
  echo "  2. then, in the next call: CVFIT_<id>($args), with the <id> it printed"
  echo "It prints these same summary lines and keeps the PDF in the sandbox (step4-apply.md, After the round). No Composio connector in this session: tell the user the page fit is unchecked. Nothing was printed into the chat."
  exit 3
fi
echo "cvcheck: $(wc -c < "$out") bytes -> $out (file only; not shown)"
python3 "$HERE/linefit.py" "$out" --over "$over" | tail -n 12
exit "${PIPESTATUS[0]}"
