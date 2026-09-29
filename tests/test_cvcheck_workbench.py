#!/usr/bin/env python3
"""Tests for skills/resume/scripts/cvcheck_workbench.py — run: python3 tests/test_cvcheck_workbench.py

The file is sent as ONE COMPOSIO_REMOTE_WORKBENCH cell, so these tests exec it the way the
workbench does: into a kernel namespace other sessions' cells share, with run_composio_tool and
requests stubbed and a synthetic Google-Docs-style PDF standing in for the export. linefit.py runs
for real, as the subprocess the sandbox starts. The live sandbox is not reachable from a test.

After editing skills/resume/scripts/linefit.py, refresh the copy the cell carries:
    python3 tests/test_cvcheck_workbench.py --rebuild
"""
import base64
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import re
import stat
import subprocess
import sys
import tempfile
import types
import zlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "resume" / "scripts"
CELL = SCRIPTS / "cvcheck_workbench.py"
LINEFIT = SCRIPTS / "linefit.py"
CVCHECK = SCRIPTS / "cvcheck.sh"
PIPELINE = ROOT / "skills" / "networking" / "scripts" / "pipeline_workbench.py"
HOOK = ROOT / ".claude" / "hooks" / "cv_guard.py"
BLOB = re.compile(r'(_cvfit_build\(\s*run_composio_tool,\s*")([0-9a-f]{64})(",\s*""")([A-Za-z0-9+/=\s]*?)(""")')
DOC = "1TestResumeDocIdXXXXXXXXXXXXXXXXXXXXXXXXXXX"
S3URL = "https://files.example.com/export/cv.pdf?X-Amz-Signature=deadbeef"
WB = "mcp__Composio_Docs_Drive__COMPOSIO_REMOTE_WORKBENCH"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


leak_check = _load("leak_check", ROOT / "scripts" / "leak_check.py")


def leaks(text):
    """What scripts/leak_check.py flags in `text`. A run of base64 between '+' and '/' can look
    like a Google Drive id, so the blob is checked like any other file."""
    with tempfile.TemporaryDirectory() as t:
        pathlib.Path(t, "cell.py").write_text(text, encoding="utf-8")
        return leak_check.scan(pathlib.Path(t), [])


def embed(text, src):
    """`text` with the _cvfit_build(sha, blob) call carrying `src`. Tries a few line widths, since
    the line breaks decide which runs leak_check sees; the decoder ignores whitespace."""
    sha = hashlib.sha256(src).hexdigest()
    b64 = base64.b64encode(zlib.compress(src, 9)).decode()  # standard alphabet: no "_" possible
    new = text
    for width in (76, 72, 68, 64, 60, 56):
        blob = "".join(b64[i:i + width] + "\n" for i in range(0, len(b64), width))
        new, n = BLOB.subn(lambda m: m.group(1) + sha + m.group(3) + "\n" + blob + m.group(5), text, count=1)
        if n != 1:
            sys.exit(f"rebuild: no _cvfit_build(sha, blob) call found in {CELL}")
        if not leaks(new):
            break
    return new


def rebuild():
    src = LINEFIT.read_bytes()
    new = embed(CELL.read_text(encoding="utf-8"), src)
    CELL.write_text(new, encoding="utf-8")
    left = leaks(new)
    print(f"rebuilt {CELL.relative_to(ROOT)} from linefit.py {hashlib.sha256(src).hexdigest()[:12]}"
          + (f"; leak_check still flags {len(left)} run(s) in the blob" if left else ""))


if "--rebuild" in sys.argv[1:]:
    rebuild()
    sys.exit(0)

failures = []


def check(label, cond, detail=""):
    print(("  ok   " if cond else "  FAIL ") + label + ("" if cond else f"  — {detail}"))
    if not cond:
        failures.append(label)


def fake_pdf(bullets, pages=1):
    """What linefit reads in a Google Docs export: Identity-H glyph runs placed with Tm, decoded
    through a ToUnicode CMap, and /Count pages. `bullets` = lines per bullet; a wrapped line sits
    one 12.2pt leading lower and indents 14pt."""
    runs, y = [], 700.0
    for n in bullets:
        for i in range(n):
            x, glyphs = (72, "0001" + "0002" * 40) if i == 0 else (86, "0002" * 40)
            runs.append(f"BT /F1 10 Tf 1 0 0 1 {x} {y:.1f} Tm <{glyphs}> Tj ET")
            y -= 12.2
        y -= 6.0
    content = "\n".join(runs).encode()
    cmap = b"begincmap\n2 beginbfchar\n<0001> <25CF>\n<0002> <0078>\nendbfchar\nendcmap"
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [3 0 R] /Count %d >>" % pages,
            b"<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /Contents 6 0 R >>",
            b"<< /Type /Font /Subtype /Type0 /Encoding /Identity-H /ToUnicode 5 0 R >>",
            b"<< /Length %d >>\nstream\n%s\nendstream" % (len(cmap), cmap),
            b"<< /Length %d >>\nstream\n%s\nendstream" % (len(content), content)]
    body = b"".join(b"%d 0 obj\n%s\nendobj\n" % (i + 1, o) for i, o in enumerate(objs))
    return b"%PDF-1.4\n" + body + b"%%EOF\n"


class Drive:
    """What the sandbox's run_composio_tool and requests.get return for one export."""

    def __init__(self, pdf=b"", status=200, err=None, response=None, fail=None):
        self.pdf, self.status, self.err, self.response, self.fail = pdf, status, err, response, fail
        self.calls = []

    def run_composio_tool(self, tool_slug, arguments, print_schema_for_tool=True):
        self.calls.append((tool_slug, dict(arguments), print_schema_for_tool))
        print(f"PREVIEW {tool_slug} s3url={S3URL}")  # the real helper prints one unless told not to
        if self.fail == "tool":
            raise RuntimeError(f"upstream 502 for {S3URL}")
        if self.response is not None:
            return self.response, self.err
        return {"data": {"file_id": arguments.get("file_id"), "mime_type": "application/pdf",
                         "download_url": {"name": "cv.pdf", "mimetype": "application/pdf", "s3url": S3URL}},
                "successful": True, "error": None}, self.err

    def get(self, url, timeout=None):
        if self.fail == "fetch":
            raise ConnectionError("HTTPSConnectionPool(host='files.example.com', port=443): Max retries "
                                  "exceeded with url: /export/cv.pdf?X-Amz-Signature=deadbeef")
        return types.SimpleNamespace(status_code=self.status, content=self.pdf)


class Sandbox:
    """One kernel namespace shared by every session's cells. Its run_composio_tool has the real
    helper's signature and answers from whichever Drive is set."""

    def __init__(self, **preset):
        self.ns, self.drive = dict(preset), Drive()

    def run_composio_tool(self, tool_slug, arguments, retry_params=None, print_schema_for_tool=True,
                          *, account=None):
        return self.drive.run_composio_tool(tool_slug, arguments, print_schema_for_tool)

    @contextlib.contextmanager
    def turn(self, drive, tmp, out):
        self.drive = drive
        old_req, old_tmp = sys.modules.get("requests"), tempfile.tempdir
        sys.modules["requests"] = types.SimpleNamespace(get=drive.get)
        tempfile.tempdir = str(tmp)
        try:
            with contextlib.redirect_stdout(out):
                yield
        finally:
            tempfile.tempdir = old_tmp
            if old_req is None:
                sys.modules.pop("requests", None)
            else:
                sys.modules["requests"] = old_req

    def cell(self, code, tmp, tool=None):
        """One workbench call: exec `code` in the kernel; what it printed."""
        self.ns["run_composio_tool"] = tool or self.run_composio_tool
        out = io.StringIO()
        with self.turn(Drive(), tmp, out):
            exec(compile(code, "<cell>", "exec"), self.ns)
        return out.getvalue()

    def names(self):
        return sorted(k for k in self.ns if re.fullmatch(r"CVFIT_[0-9a-f]{6}", k))

    def call(self, name, drive, tmp, *args, **kw):
        """name(*args, **kw) in this kernel: (return code, what it printed)."""
        out = io.StringIO()
        with self.turn(drive, tmp, out):
            rc = self.ns[name](*args, **kw)
        return rc, out.getvalue()


PASTE = CELL.read_text(encoding="utf-8")
SRC = LINEFIT.read_bytes()
OURS = {"__builtins__", "run_composio_tool"}

print("cvcheck_workbench — the cell")
m = BLOB.search(PASTE)
try:
    carried = zlib.decompress(base64.b64decode("".join(m.group(4).split()), validate=True)) if m else b""
except Exception:
    carried = b""
check("the cell carries the kit's current linefit.py, byte for byte",
      carried == SRC and m.group(2) == hashlib.sha256(SRC).hexdigest(),
      "linefit.py changed since the cell was built: python3 tests/test_cvcheck_workbench.py --rebuild")
check("the blob is standard base64 (no '_'), so it can never spell a Composio tool slug",
      m and "_" not in m.group(4))
check("the cell passes scripts/leak_check.py, blob included", not leaks(PASTE), leaks(PASTE))
with tempfile.TemporaryDirectory() as t:
    got = [subprocess.run([sys.executable, str(HOOK)], capture_output=True, text=True,
                          input=json.dumps({"hook_event_name": "PreToolUse", "tool_input": {"code_to_execute": PASTE},
                                            "tool_name": f"mcp__{s}__COMPOSIO_REMOTE_WORKBENCH"}),
                          env={**os.environ, "CV_GUARD_DIR": t}).stdout.strip()
           for s in ("Composio_Docs_Drive", "claude_ai_Composio_Docs_Drive", "0f0e0d0c-1111-2222-3333-444455556666")]
check("cv_guard lets the cell through as workbench code, under every server name", got == [""] * 3, got)

with tempfile.TemporaryDirectory() as t:
    tmp = pathlib.Path(t)
    box = Sandbox(cvfit="another session's bare cvfit")
    out = box.cell(PASTE, tmp)
    names = box.names()
    NAME = names[0] if names else "CVFIT_??????"
    check("it binds ONE name, CVFIT_<6 hex>, and prints it with the verified linefit hash",
          set(box.ns) - OURS - {"cvfit"} == {NAME} and f"cvfit loaded as {NAME} (linefit.py "
          f"{hashlib.sha256(SRC).hexdigest()[:12]} verified)" in out, (sorted(box.ns), out))
    check("a bare cvfit another session left in the kernel is not touched",
          box.ns["cvfit"] == "another session's bare cvfit")
    check("sending the same file again binds the same name, not a second one",
          (box.cell(PASTE, tmp), box.names())[1] == [NAME])
    check("sending it calls no tool", box.drive.calls == [])

    bad = Sandbox()
    blob_line = m.group(4).strip().splitlines()[3]
    mangled = PASTE.replace(blob_line, blob_line[:20] + ("A" if blob_line[20] != "A" else "B") + blob_line[21:], 1)
    try:
        bad.cell(mangled, tmp)
        raised = ""
    except ValueError as exc:
        raised = str(exc)
    check("a blob garbled in the paste is refused, and nothing is bound",
          "arrived altered" in raised and set(bad.ns) - OURS == set(), raised or sorted(bad.ns))

    print("cvcheck_workbench — the name follows the code")
    other = Sandbox()
    other.cell(PASTE.replace("# PRIVATE resume, run inside", "# PRIVATE resume (a comment edit), run inside", 1), tmp)
    check("a comment edit keeps the name", other.names() == [NAME], other.names())
    variant = PASTE.replace('print("cvfit: " + msg[:400])', 'print("cvfit! " + msg[:400])', 1)
    box.cell(variant, tmp)
    two = box.names()
    check("a code change gets a new name, and both copies live side by side", len(two) == 2 and NAME in two, two)
    third = Sandbox()
    third.cell(embed(PASTE, SRC + b"\n# a later linefit.py\n"), tmp)
    check("a different linefit.py gets a new name too", third.names() and third.names() != [NAME], third.names())
    rc, out = box.call([n for n in two if n != NAME][0], Drive(pdf=fake_pdf([2])), tmp, DOC)
    rc0, out0 = box.call(NAME, Drive(pdf=fake_pdf([2])), tmp, DOC)
    check("... and each copy runs its own code", "cvfit! " not in out0 and rc == rc0 == 0, (out, out0))

    print("cvcheck_workbench — the check, run the way the workbench runs it")
    drive = Drive(pdf=fake_pdf([2, 3, 1]))
    rc, out = box.call(NAME, drive, tmp, DOC)
    check("a 3-line bullet: linefit's summary and exit 1",
          rc == 1 and "pages: 1" in out and "1 bullet(s) exceed 2 lines." in out, out)
    check("the detected leading is reported, the temp path is not",
          "leading 12.2pt (deleted; not shown)" in out and "cvfit-" not in out, out)
    check("it exported the doc with GOOGLEDOCS_EXPORT_DOCUMENT_AS_PDF, the helper's preview turned off",
          drive.calls == [("GOOGLEDOCS_EXPORT_DOCUMENT_AS_PDF", {"file_id": DOC}, False)], drive.calls)
    check("neither the PDF, its link nor the helper's preview reaches the output",
          not any(s in out for s in ("%PDF", "PREVIEW", "X-Amz", "deadbeef", "files.example")), out)
    check("the PDF is deleted after measuring", list(tmp.iterdir()) == [], list(tmp.iterdir()))
    rc, out = box.call(NAME, drive, tmp, DOC, over=3)
    check("a one-line re-check reuses the loaded cell: over=3 fits, exit 0",
          rc == 0 and "All 3 bullets within 3 lines." in out, out)
    rc, out = box.call(NAME, Drive(pdf=fake_pdf([2, 2, 1])), tmp, f"https://docs.google.com/document/d/{DOC}/edit?tab=t.0")
    check("a doc URL works, and a resume that fits exits 0", rc == 0 and "All 3 bullets within 2 lines." in out, out)
    rc, out = box.call(NAME, Drive(pdf=fake_pdf([1], pages=2)), tmp, DOC)
    check("two pages: OVER ONE PAGE, exit 1", rc == 1 and "OVER ONE PAGE" in out, out)
    rc, out = box.call(NAME, Drive(pdf=fake_pdf([3] * 12)), tmp, DOC)
    check("12 long bullets: the list is capped and the pages line kept",
          rc == 1 and "pages: 1" in out and "12 bullet(s) exceed 2 lines." in out and len(out.splitlines()) <= 13,
          f"{len(out.splitlines())} lines")
    plain = Sandbox()
    d = Drive(pdf=fake_pdf([2]))
    plain.cell(PASTE, tmp, tool=lambda tool_slug, arguments: d.run_composio_tool(tool_slug, arguments))
    rc, out = plain.call(plain.names()[0], d, tmp, DOC)
    check("a run_composio_tool without print_schema_for_tool still works",
          rc == 0 and "pages: 1" in out and len(d.calls) == 1, out)

    print("cvcheck_workbench — a kernel other sessions share")
    shared = Sandbox()
    helpers = PIPELINE.read_text(encoding="utf-8").replace("<PIPELINE_SHEET_ID>", "sheet-under-test") \
        .replace("<PIPELINE_TAB>", "Tab-under-test")
    shared.cell(helpers, tmp)
    before = {k: v for k, v in shared.ns.items() if k != "run_composio_tool"}
    shared.cell(PASTE, tmp)
    mine = shared.names()
    check("sent after the Pipeline helpers, it changes none of their names (find, log, S, TAB, ...)",
          {"find", "log", "S", "TAB"} <= set(before) and all(shared.ns[k] is v for k, v in before.items())
          and set(shared.ns) - set(before) - {"run_composio_tool"} == set(mine))
    shared.cell("import os, re, sys, subprocess, tempfile\n"
                "os = re = sys = subprocess = tempfile = requests = inspect = contextlib = None\n"
                "linefit = fit = check = cvfit = lambda *a, **k: 1 / 0\n"
                "run_composio_tool = lambda *a, **k: 1 / 0\n", tmp)
    rc, out = shared.call(mine[0], Drive(pdf=fake_pdf([2, 2])), tmp, DOC)
    check("other cells rebinding os/re/sys/linefit/cvfit, even run_composio_tool, cannot break it",
          rc == 0 and "All 2 bullets within 2 lines." in out, out)

    print("cvcheck_workbench — failures: one line, a code, never the link")
    for label, d, want, text in [
        ("an export error is reported, exit 3", Drive(err="403 The caller does not have permission"), 3,
         "export failed: 403 The caller does not have permission"),
        ("a response without download_url.s3url, exit 3", Drive(response={"data": {}, "successful": False}), 3,
         "no download_url.s3url in the response"),
        ("an HTML sign-in page instead of a PDF, exit 3", Drive(pdf=b"<html>Sign in</html>"), 3,
         "the export is not a PDF (HTTP 200, 20 bytes)"),
        ("a failed fetch, exit 3, and the signed link masked", Drive(fail="fetch"), 3, "ConnectionError"),
        ("a tool that raises, exit 3, and its URL masked", Drive(fail="tool"), 3, "RuntimeError: upstream 502 for <link>"),
        ("a PDF with no content, exit 4 with linefit's reason (not 1: that is no verdict)",
         Drive(pdf=b"%PDF-1.4\n%%EOF\n"), 4, "linefit failed (exit 3): linefit: the PDF has no content streams"),
        ("a PDF that crashes linefit, exit 4 with the exception", Drive(pdf=b"%PDF-1.4\nstream\nBT 1 0 0 1 72 - Tm ET\nendstream\n"), 4,
         "linefit failed (exit 1): ValueError: could not convert string to float: b'-'"),
    ]:
        rc, out = box.call(NAME, d, tmp, DOC)
        check(label, rc == want and text in out and len(out.splitlines()) == 1
              and not any(s in out for s in ("deadbeef", "X-Amz", "https://", "PREVIEW", "cvfit-")), f"rc={rc} {out!r}")
    for bad_id, kw in (("nope", {}), (DOC, {"over": "two"})):
        d = Drive(pdf=fake_pdf([2]))
        rc, out = box.call(NAME, d, tmp, bad_id, **kw)
        check(f"({bad_id[:6]!r}, {kw}) is refused before any export, exit 2", rc == 2 and d.calls == [], f"rc={rc} {out!r}")
    check("no temp file is left behind by any of them", list(tmp.iterdir()) == [], list(tmp.iterdir()))
    check("after all those calls the kernel holds only what was sent (nothing written at call time)",
          set(box.ns) - OURS - {"cvfit"} == set(two), sorted(box.ns))

print("session_meter — a CVFIT_<id> call is a page-fit run")
meter = _load("session_meter", ROOT / "scripts" / "session_meter.py")
C = "CVFIT_3f9a2c"


def counted(code):
    c = meter.classify(WB, {"code_to_execute": code})
    return c.count("cvcheck_runs"), c.count("sandbox_exports")


check("sending the cell counts 0 runs, 0 hand exports", counted(PASTE) == (0, 0), counted(PASTE))
check("CVFIT_<id>(<doc>) counts 1", counted(f'{C}("{DOC}")') == (1, 0))
check("two calls count 2; the cell with a call appended counts 1",
      counted(f'{C}("{DOC}")\nprint({C}("{DOC}", over=3))') == (2, 0) and counted(PASTE + f'{C}("{DOC}")\n') == (1, 0))
check("comments, a bare cvfit() (another session's) and other helpers do not count",
      counted(f'# {C}("{DOC}")\ncvfit("{DOC}")\nmy_cvfit("{DOC}")\nx.{C}("{DOC}")') == (0, 0))
check("cvcheck.sh still counts", meter.classify("Bash", {"command": f"bash {CVCHECK} {DOC}"}) == ["cvcheck_runs"])

print("cvcheck.sh — exit 3 hands over to the sandbox check, never to link sharing")
with tempfile.TemporaryDirectory() as t:
    fake = pathlib.Path(t, "bin")
    fake.mkdir()
    for label, body in (("curl cannot connect", "exit 7"),
                        ("curl gets a sign-in page", 'for a; do [ "$p" = -o ] && o="$a"; p="$a"; done; '
                                                      'echo "<html>Sign in</html>" > "$o"')):
        (fake / "curl").write_text("#!/bin/sh\n" + body + "\n")
        (fake / "curl").chmod(stat.S_IRWXU)
        p = subprocess.run(["bash", str(CVCHECK), f"https://docs.google.com/document/d/{DOC}/edit"],
                           capture_output=True, text=True, cwd=t,
                           env={**os.environ, "PATH": f"{fake}:{os.environ['PATH']}", "TMPDIR": t})
        check(f"{label}: exit 3, naming the cell by path and the call to make, not 'share it'",
              p.returncode == 3 and str(CELL) in p.stdout and f'CVFIT_<id>("{DOC}")' in p.stdout
              and "Do not change its sharing" in p.stdout and "anyone with the link: viewer" not in p.stdout.lower(),
              f"rc={p.returncode} {p.stdout[-300:]!r}")
    check("... and leaves no half-written PDF", not list(pathlib.Path(t).glob("cv-*.pdf")))
    p = subprocess.run(["bash", str(CVCHECK), DOC, "--over", "3"], capture_output=True, text=True, cwd=t,
                       env={**os.environ, "PATH": f"{fake}:{os.environ['PATH']}", "TMPDIR": t})
    check("--over 3 carries over to the call", p.returncode == 3 and f'CVFIT_<id>("{DOC}", over=3)' in p.stdout,
          p.stdout[-200:])

print()
if failures:
    print(f"{len(failures)} FAILED: " + ", ".join(failures))
    sys.exit(1)
print("all cvcheck_workbench tests passed")
