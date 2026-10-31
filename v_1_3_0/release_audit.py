#!/usr/bin/env python3
"""Release audit for a pipeline version folder (documentation only; no network).

Usage: python release_audit.py [version_folder]   (default: this file's folder)

Checks, and exits 1 if any fails:
  1. phase file versions: the table in MASTER_PIPELINE_OVERVIEW.md matches each file's title
  2. no older version-folder paths (v_1_x_x) are used as current paths
  3. every handoff file named anywhere exists in COPILOT_HANDOFFS/ (author-saved outputs are exempt)
  4. headings cited by other files exist (PHASE 2.5 section 0 / 3.2b, PHASE 3.5 section 15, PHASE 6.5 section 9b, PHASE 4 Step 0V / 0F)
  5. every trigger file named in a phase file or HOW_TO appears in the overview's trigger map or is a documented output
  6. no raw <TOKEN> outside code in COPILOT_HANDOFFS (GitHub would hide it)
  7. old lock wording is gone ("pseudo-locked", "fully locked and ready", "locks the chapter/workbook manuscript", "final eBook PDF locks", "locked to the eBook", "locks the manuscript and glossary", "wording changes go through the eBook instead")
"""
import pathlib
import re
import sys

V = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent
bad = 0


def chk(name, ok, detail=""):
    global bad
    print(("ok   " if ok else "FAIL ") + name + (" " + detail if detail else ""))
    bad += (not ok)


txt = {f: f.read_text(encoding="utf-8") for f in V.rglob("*.md")}
overview = (V / "MASTER_PIPELINE_OVERVIEW.md").read_text(encoding="utf-8")

# 1 versions
titles = {}
for f in sorted(V.glob("PHASE*.md")):
    h1 = txt[f].split("\n")[0]
    m = re.search(r"\((v[\d.]+)\)\s*$", h1)
    titles[f.name] = m.group(1) if m else "?"
rows = dict((m.group(3), m.group(2)) for m in re.finditer(r"^\| (PHASE [\d.A-Z]+) \| (v[\d.]+|\?) \| [^|]+ \| `([^`]+)` \|$", overview, re.M))
chk("1 version table lists every phase file", set(rows) == set(titles), str(set(titles) ^ set(rows)) if set(rows) != set(titles) else "")
chk("1 version table matches the titles", all(rows.get(k) == v for k, v in titles.items()))
chk("1 no phase file has an unreadable version", "?" not in titles.values())
howto = txt[V / "HOW_TO_RUN_THE_PIPELINE.md"]
chk("1 HOW_TO header points at the table (no hand-kept list)", "phase files v3" not in "\n".join(howto.split("\n")[:6]))
# "Since v1.2.6" column against the older folder, when it is present
old = V.parent / "v_1_2_6"
if old.is_dir():
    bad_since = []
    since = [(m.group(2), m.group(1)) for m in re.finditer(r"^\| PHASE [\d.A-Z]+ \| v[\d.]+ \| ([^|]+) \| `([^`]+)` \|$", overview, re.M)]
    for fn, claim in since:
        o = old / fn
        changed = (not o.exists()) or o.read_bytes().replace(b"\r\n", b"\n") != (V / fn).read_bytes().replace(b"\r\n", b"\n")
        if changed != claim.strip().startswith("changed"):
            bad_since.append(fn)
    chk("1 Since-v1.2.6 column matches v_1_2_6", not bad_since, str(bad_since))

# 2 stale folder paths
stale = [f.name for f, t in txt.items() if re.search(r"\bv_?1_(?:[0-2](?:_\d+)?|3_[1-9]\d*)\b", t) and "ROLLOUT" not in f.name]
chk("2 no older version-folder paths", not stale, str(stale))

# 3 handoff files
out = {"COPILOT_RESEARCH_REPORT.md", "COPILOT_RESEARCH_STAGE1.md", "COPILOT_DESIGN_REVIEW.md", "COPILOT_FINAL_EBOOK_REVIEW.md",
       "COPILOT_PUBLICATION_QA.md"}
allt = "\n".join(txt.values())
named = set(re.findall(r"COPILOT_[A-Z0-9_]+\.md", allt)) - out
missing = [n for n in sorted(named) if not (V / "COPILOT_HANDOFFS" / n).exists()]
chk("3 handoff files exist", not missing, str(missing))

# 4 headings
def has(file, pat):
    t = txt.get(V / file)
    return t is not None and re.search(pat, t, re.M) is not None
for label, f, pat in [("PHASE 2.5 section 0", "PHASE 2.5- Manuscript Lock Audit.md", r"^## 0\. The lock state machine"),
                      ("PHASE 2.5 section 3.2b", "PHASE 2.5- Manuscript Lock Audit.md", r"^### 3\.2b"),
                      ("PHASE 3.5 section 15", "PHASE 3.5- Claude QA of Design Artifacts.md", r"^# 15\."),
                      ("PHASE 6.5 section 9b", "PHASE 6.5- Claude Design Publication QA.md", r"^## 9b\."),
                      ("PHASE 4 Step 0F", "PHASE 4- Kindle DOCX Chapter Compilation.md", r"^## 0F "),
                      ("PHASE 4 Step 0V", "PHASE 4- Kindle DOCX Chapter Compilation.md", r"^## 0V\.")]:
    chk("4 " + label, has(f, pat))

# 5 triggers
trig = set(re.findall(r"\b([A-Z][A-Z0-9_.]{5,}\.md)\b", "\n".join(t for f, t in txt.items() if f.name.startswith(("PHASE", "HOW_TO")))))
doc_ok = {"README.md", "CHANGELOG.md", "PLACEHOLDERS.md", "MANUSCRIPT_SYNCED.md", "MASTER_PIPELINE_OVERVIEW.md", "STATUS.md"}
# the overview writes "X_READY.md / _INCOMPLETE" as shorthand for the pair
short = {n for n in trig if n.endswith("_INCOMPLETE.md") and n.replace("_INCOMPLETE", "_READY") in overview}
unknown = sorted(n for n in trig if n not in overview and n not in doc_ok and n not in short and not n.startswith(("COPILOT_", "PHASE_", "RAG_", "BOOK_", "RERUN_P")))
chk("5 trigger files named in phases/HOW_TO appear in the overview", not unknown, str(unknown))

# 6 raw tokens in handoffs
raw = 0
for f, t in txt.items():
    if "COPILOT_HANDOFFS" not in str(f):
        continue
    fence = False
    for line in t.split("\n"):
        if line.startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        raw += len(re.findall(r"<[A-Za-z_][A-Za-z0-9_]*>", re.sub(r"`[^`]*`", "", line)))
chk("6 no raw tokens outside code in COPILOT_HANDOFFS", raw == 0, str(raw))

# 7 old wording
for pat in ("pseudo-locked", "fully locked and ready", "locks the chapter manuscript", "locks the workbook manuscript", "final eBook PDF locks", "locked to the eBook", "locks the manuscript and glossary", "wording changes go through the eBook instead"):
    hit = [f.name for f, t in txt.items() if pat in t]
    chk(f"7 wording gone: {pat}", not hit, str(hit))

sys.exit(1 if bad else 0)
