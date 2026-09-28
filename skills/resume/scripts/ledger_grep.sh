#!/usr/bin/env bash
# ledger_grep.sh TERM [TERM...] — print profile entries matching any term, each with its heading
# context (# / ## / ###) so the hit can be cited. Case-insensitive; terms are OR'ed regexes.
# A few dozen tokens per hit instead of reading the files whole. Never read them whole.
#
# Searches (repo-root relative): profile/evidence.md (the fact ledger), profile/me.md (story
# bank), profile/resume.md (master resume), profile/voice.md (writing samples). A real, sourced
# number often lives in only one of them, so all four are scanned before a gap is declared.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PROFILE_DIR="${CAREER_PROFILE_DIR:-$ROOT/profile}"
FILES=("$PROFILE_DIR/evidence.md" "$PROFILE_DIR/me.md" "$PROFILE_DIR/resume.md" "$PROFILE_DIR/voice.md")
[[ $# -ge 1 ]] || { echo "usage: ledger_grep.sh TERM [TERM...]" >&2; exit 2; }
pat="$(printf '%s|' "$@")"; pat="${pat%|}"

scan() {  # $1 file  $2 label
  awk -v pat="$pat" -v label="$2" '
    BEGIN { IGNORECASE = 1; hits = 0; pl = tolower(pat) }
    function m(s) { return tolower(s) ~ pl }
    /^# /   { flush(); h1 = substr($0, 3); next }
    /^### / { flush(); h3 = substr($0, 5); next }
    /^## /  { flush(); h2 = substr($0, 4); h3 = ""; next }
    # an entry is a "- " line plus its continuation / "> " lines until the next entry or header
    /^- /   { flush(); block = $0; next }
    /^#/    { flush(); next }
    block != "" && $0 !~ /^[[:space:]]*$/ { block = block "\n" $0; next }
    { flush(); if (m($0) && $0 !~ /^[[:space:]]*$/) { printf "%s | %s | %s\n%s\n\n", label, h2 ? h2 : h1, h3, $0; hits++ } }
    function flush() {
      if (block != "" && m(block)) { printf "%s | %s | %s\n%s\n\n", label, h2 ? h2 : h1, h3, block; hits++ }
      block = ""
    }
    END { flush(); printf "-- %s: %d hit(s) for /%s/\n", label, hits, pat }
  ' "$1"
}
found=0
for f in "${FILES[@]}"; do
  if [[ -f "$f" ]]; then scan "$f" "profile/$(basename "$f")"; found=1
  else echo "-- profile/$(basename "$f"): MISSING — run the setup skill to create it"; fi
done
[[ $found -eq 1 ]] || { echo "ledger_grep: no profile files under $PROFILE_DIR" >&2; exit 1; }
if grep -qsE '<[^>]+>|TODO' "$PROFILE_DIR/evidence.md" 2>/dev/null; then
  echo "-- note: profile/evidence.md still has template placeholders (<…> / TODO); fill them via the setup skill"
fi

# Record Gate 0 for the guard hook: it refuses a session's first resume write until a grep has
# run. It checks this file's mtime; the terms are kept as the audit trail of what was searched.
G="${CV_GUARD_DIR:-$HOME/.claude/cv-guard}"
{ mkdir -p "$G" && printf '%s  %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$pat" >> "$G/facts-grepped" \
  && echo "-- Gate 0 recorded for the guard hook ($G/facts-grepped)"; } 2>/dev/null || true
