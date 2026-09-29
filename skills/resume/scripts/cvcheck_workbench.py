# cvcheck_workbench.py — cvcheck.sh's page-fit check (1 page, no bullet over 2 lines) for a
# PRIVATE resume, run inside Composio's sandbox. Send this whole file, unchanged, as the code of
# ONE COMPOSIO_REMOTE_WORKBENCH call per session. It prints the one name it binds, CVFIT_<id>;
# call that name in later workbench calls:
#
#   CVFIT_<id>("<DOC_ID or doc URL>")          # over=3 allows 3-line bullets
#
# cvcheck.sh exports with an unauthenticated curl, so it exits 3 on any doc not shared "anyone
# with the link", and a resume copy is normally private. Never change a doc's sharing to get round
# that. Composio reads the user's Drive as the user, so this exports the doc here
# (GOOGLEDOCS_EXPORT_DOCUMENT_AS_PDF), fetches the PDF into a temp dir, runs linefit.py on it in a
# subprocess and prints only the lines cvcheck.sh prints. The PDF is deleted; neither it nor its
# signed link reaches the chat. Returns cvcheck.sh's exit codes: 0 fits, 1 over one page or a
# bullet over `over` lines, 2 not a doc id, 3 export failed; plus 4, linefit failed.
#
# The sandbox is shared by every session on the user's Composio account, so nothing here is a
# global another session could replace. <id> hashes this code and the linefit.py it carries: any
# change gives a new name, the same copy the same name. run_composio_tool is passed in, so a later
# rebinding in the sandbox changes nothing. Never call a bare cvfit(): in this sandbox that is
# whatever another session defined.
#
# The blob is skills/resume/scripts/linefit.py (zlib, then base64), checked against its sha256
# when sent. After editing linefit.py: python3 tests/test_cvcheck_workbench.py --rebuild


def _cvfit_build(run_composio_tool, sha256, blob):
    """Check linefit.py, build the check, bind it to CVFIT_<id> and print that name."""
    import base64, binascii, hashlib, types, zlib
    try:
        linefit = zlib.decompress(base64.b64decode("".join(blob.split()), validate=True))
    except (binascii.Error, zlib.error):
        linefit = b""
    if hashlib.sha256(linefit).hexdigest() != sha256:
        raise ValueError("cvfit not loaded: the embedded linefit.py arrived altered. Send "
                         "skills/resume/scripts/cvcheck_workbench.py again, unchanged.")

    def cvfit(doc_id, over=2):
        """Page fit of one Google Doc, measured in this sandbox. Prints linefit's summary, never
        the PDF or its link. Returns 0 fits, 1 does not fit, 2 not a doc id, 3 export failed,
        4 linefit failed."""
        import contextlib, inspect, io, os, re, subprocess, sys, tempfile

        def say(msg):  # one line, links masked: the export's signed URL is a key to the PDF
            msg = re.sub(r"\S*(?:https?://|[?&][\w.-]+=)\S*", "<link>", " ".join(str(msg).split()))
            print("cvfit: " + msg[:400])

        m = re.search(r"/d/([A-Za-z0-9_-]+)", str(doc_id))
        doc = m.group(1) if m else str(doc_id).strip()
        if not re.fullmatch(r"[A-Za-z0-9_-]{20,}", doc):
            say(f"{doc!r} does not look like a Google Doc id")
            return 2
        try:
            over = int(over)
        except (TypeError, ValueError):
            say(f"over={over!r} is not a number of lines")
            return 2
        with tempfile.TemporaryDirectory(prefix="cvfit-") as tmp:
            pdf_path = os.path.join(tmp, "cv.pdf")
            try:
                tool = run_composio_tool
                try:  # off, the helper prints a response preview with the signed link in it
                    kw = {"print_schema_for_tool": False} \
                        if "print_schema_for_tool" in inspect.signature(tool).parameters else {}
                except (TypeError, ValueError):
                    kw = {}
                with contextlib.redirect_stdout(io.StringIO()):
                    res, err = tool("GOOGLEDOCS_EXPORT_DOCUMENT_AS_PDF", {"file_id": doc}, **kw)
                dl = ((res or {}).get("data") or {}).get("download_url")
                url = dl.get("s3url") if isinstance(dl, dict) else dl
                if err or not isinstance(url, str) or not url:
                    say(f"{doc}: export failed: {err or 'no download_url.s3url in the response'}")
                    return 3
                import requests
                got = requests.get(url, timeout=60)
                pdf = got.content
                if got.status_code != 200 or not pdf.startswith(b"%PDF"):
                    say(f"{doc}: the export is not a PDF (HTTP {got.status_code}, {len(pdf)} bytes)")
                    return 3
                with open(pdf_path, "wb") as fh:
                    fh.write(pdf)
            except Exception as exc:
                say(f"{doc}: export failed: {type(exc).__name__}: {exc}")
                return 3
            try:
                p = subprocess.run([sys.executable or "python3", "-", pdf_path, "--over", str(over)],
                                   input=linefit, capture_output=True, timeout=60,
                                   env={**os.environ, "PYTHONIOENCODING": "utf-8"})
            except Exception as exc:
                say(f"{doc}: linefit did not run: {type(exc).__name__}: {exc}")
                return 4
        lines = p.stdout.decode("utf-8", "replace").replace(pdf_path, "the PDF").splitlines()
        out = lines[1:]  # [0] is the temp path and the detected leading
        if p.returncode not in (0, 1) or not out[:1] or not out[0].startswith("pages:"):
            why = (p.stderr.decode("utf-8", "replace").replace(pdf_path, "the PDF").strip().splitlines()
                   or [s for s in lines if s.strip()] or ["no output"])[-1]
            say(f"{doc}: linefit failed (exit {p.returncode}): {why}")
            return 4
        if len(out) > 12:
            out = out[:1] + out[-11:]  # keep the pages line; the tail holds the verdict
        lead = re.search(r"leading: (\S+)pt", lines[0])
        print(f"cvfit: {doc}: {len(pdf)}-byte PDF measured in the sandbox"
              + (f", leading {lead.group(1)}pt" if lead else "") + " (deleted; not shown)")
        print("\n".join(out))
        return p.returncode

    def fingerprint(code, h):
        """Hash the compiled code, not the text: comments leave the name alone, any change to
        what runs gives a new one."""
        h.update(code.co_code)
        h.update(repr((code.co_names, code.co_varnames)).encode())
        for c in code.co_consts:
            if isinstance(c, types.CodeType):
                fingerprint(c, h)
            else:  # a set literal's order differs between processes; sort it
                h.update(repr(sorted(map(repr, c)) if isinstance(c, frozenset) else c).encode())
        return h

    name = "CVFIT_" + fingerprint(_cvfit_build.__code__, hashlib.sha256(sha256.encode())).hexdigest()[:6]
    cvfit.linefit_sha256 = sha256
    globals()[name] = cvfit
    print(f"cvfit loaded as {name} (linefit.py {sha256[:12]} verified). Call it by that name in "
          f"every later workbench call, e.g. {name}(\"<DOC_ID>\"). Never a bare cvfit(): other "
          "sessions share this sandbox.")


try:
    _cvfit_build(
        run_composio_tool,
        "e0ef036650ad3c0c70e13f4e55c566212de67cb3a620487e7b0f75a3edb2fb91",
        """
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
mdg2/ge+d+o9
""")
finally:
    del _cvfit_build
