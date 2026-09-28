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
# Uses Google Docs' unauthenticated export, so the doc must be shared "Anyone with the link:
# Viewer". If it can't be, export it with the Drive connector (download_file_content,
# application/pdf) to a file and run: python3 linefit.py <file.pdf> --over 2
#
# Needs only bash, curl and stdlib python3.
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
  echo "cvcheck: export failed — the doc is not link-readable. Share it as 'Anyone with the link: Viewer' and retry, or export it via the Drive connector to a file and run linefit.py on that file. Nothing was printed into the chat."
  exit 3
fi
echo "cvcheck: $(wc -c < "$out") bytes -> $out (file only; not shown)"
python3 "$HERE/linefit.py" "$out" --over "$over" | tail -n 12
exit "${PIPESTATUS[0]}"
