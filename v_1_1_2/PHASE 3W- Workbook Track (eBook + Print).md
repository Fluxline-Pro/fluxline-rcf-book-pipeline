# PHASE 3W: Workbook Track (eBook + Full-Color Print) (v3.4)

**v3.4 changes (2026-10-03, release v1.1.2):**
- **Print QA on upload (W2b):** when the book ships a print workbook, each print PDF uploaded to `<WORKBOOK_BOOK_ROOT>/InDesign/` is checked automatically against its eBook PDF: text drift plus print layout. This is the workbook variant of PHASE 4 Part 0P. With `formats: ["ebook"]` it is N/A.
- **Book-root print location:** in the `book-root` layout, print PDFs now go to `<WORKBOOK_BOOK_ROOT>/InDesign/<eBook stem>_Print7x10.pdf`, not next to the eBook PDF.
- W3 steps 3 and 5 cite the print QA report as evidence, rather than repeating its checks.

**v1.1 changes (2026-10-02):**
- **W2 upload location:** the final workbook PDFs may go to the chapter's `Workbook/` folder (as before), **or** to the book's workbook folder `<WORKBOOK_BOOK_ROOT>`, named `<NN>_Ex_<L>_<N>_Chapter<C>.pdf` (e.g. `01_Ex_1_1_Chapter1.pdf`). The chapter number in the name ties it to the chapter.
- **Print PDF optional per book:** a book that ships only the workbook eBook records print as *n/a*; W3 doesn't fail on it.
- **The upload completes PHASE 3.5 for the workbook and starts W3 automatically** (after 30 quiet minutes).
- **Uncertain sync items** go to `<CH_ROOT>/_Pipeline/P3W_DECISIONS.md`, a table with a blank **Decision** column. W3 applies the decisions on its next run, the same way PHASE 4 Part 0 handles S3 items.
- **W0 includes only the exercises <AUTHOR> selected** (PHASE 1 Step 2 / PHASE 2 workbook selection).

> **Pipeline position:** a side track that runs from the end of **PHASE 2** through **PHASE 3 / 3.5** for each chapter, then once per book after PHASE 4 Part B step B0 · **Upstream gate:** `Governance/Trigger/GOVERNANCE_READY.md` (per chapter) · **Downstream:** PHASE 6.5 (workbook sub-certification), PHASE 7
> **Canonical paths, status ladder, triggers, and deliverables:** see `MASTER_PIPELINE_OVERVIEW.md`.

**New in v1.0.3 (2026-09-30).** The workbook ships in two formats only: an **eBook (PDF)** and a **full-color print book**. Claude Design builds the workbook from the workbook manuscript, and <AUTHOR> produces both formats from that in InDesign. It has **no Kindle edition, no audiobook, and no RAG ingestion**. Before this file, the workbook's steps were spread across PHASES 1–7, and several of them assumed an HTML-built eBook, a Kindle edition, and RAG ingestion.

**The alignment rule:** the workbook manuscript follows the same rule as the chapter manuscript. **The DOCX is canonical and the Markdown is its replica.** By the end of the track, the three forms say the same thing, word for word: **PDF = DOCX = MD**.

---

## 1. What the workbook is, and what it isn't

| In scope | Out of scope |
|---|---|
| Workbook manuscript: DOCX (canonical) + MD (replica) | Kindle / KDP reflowable workbook |
| Claude Design workbook, built from the workbook manuscript | Audiobook, narration, XTTS |
| Workbook eBook PDF (8.5×11 in, RGB) | RAG ingestion (Local or Cloud), `RAG_Workbook.html` |
| Full-color print workbook PDF (7×10 in, CMYK) | Workbook EPUB, or an eBook built from `Workbook_Master.html` |
| The exercise registry (exercise IDs ↔ manuscript mentions) | |

**Numbering:** workbook exercises are numbered by **Lesson**, not by chapter (for example, `Exercise 1.4` belongs to Lesson 1 and appears in Chapter 4). The manuscript points readers into the workbook ("Begin Exercise 1.4 in your workbook"), so the workbook and the manuscript must agree on every exercise ID.

**Where the InDesign files live:** <AUTHOR> keeps the workbook InDesign documents, the book file (INDB), linked assets, and fonts in `<WORKBOOK_INDESIGN_ROOT>`, outside `<BOOK_ROOT>`, so links and fonts don't break. No phase reads, copies, or checks `.indd`/`.indb` files. Phases check only the **exported PDFs** <AUTHOR> uploads.

---

## 2. Per chapter

### W0. Workbook manuscript (PHASE 1–2)

| File | Location | Role |
|---|---|---|
| Workbook manuscript, DOCX | `<CH_ROOT>/Workbook/<ChapterName>_Exercise<L.N>_Workbook.docx` | **Canonical.** The exercise text the workbook publishes |
| Workbook manuscript, MD | `<CH_ROOT>/Workbook/<ChapterName>_Exercise<L.N>_Workbook.md` | **Replica** of the DOCX, same base name |
| Companion workbook manuscript (optional) | `<CH_ROOT>/Workbook/<ChapterName>_Exercise<L.N>_<Part>_Workbook.docx` + `.md` | Extra workbook pages for the same exercise, such as write-in journal pages (e.g. `Ch5_…_Exercise2.1_DailyJournal_Workbook.docx`). The same DOCX = MD rule and the same gates apply, and the registry lists them under `companionFiles` |
| Workbook Exercise Packet | `<CH_ROOT>/Workbook/<ChapterName>_WorkbookPacket.md` | PHASE 1 working material (anchor + companion exercises, prompts). Not the manuscript; content reaches the workbook only once it's in the DOCX |

PHASE 1 Step 2 creates the DOCX and its MD replica. PHASE 2 governs the content like any derived artifact. If <AUTHOR> edits the DOCX, the MD is regenerated from it, with a backup in `Governance/_Backups/<YYYYMMDD>_<reason>/`.

### W0 gate: `WORKBOOK_MANUSCRIPT_READY.md` (end of PHASE 2, before PHASE 3)

Run at the end of PHASE 2, alongside `GOVERNANCE_READY.md`:

1. **DOCX = MD** (the workbook manuscript and every companion file). Extract the text of both and compare them word for word, ignoring only Markdown syntax. The expected result is 0 differences. A difference means the MD is regenerated from the DOCX (with a backup), never hand-patched.
2. **Exercise registry.** Add this chapter's entries to `_BookGovernance/Workbook/Workbook_ExerciseRegistry.json`: one per exercise, with `exerciseId`, `lesson`, `chapter`, `title`, `docx`, and `manuscriptMentions` (each place the chapter manuscript names it). **Blocking:** an exercise the manuscript mentions that the workbook manuscript doesn't have, or a number that differs between them.

**Result:** before writing either file, rename any existing `WORKBOOK_MANUSCRIPT_READY.md` to `WORKBOOK_MANUSCRIPT_READY_superseded_<YYYYMMDD_HHMM>.md`, so a failed re-run never leaves an old READY file in place. Then:
- Both pass → `<CH_ROOT>/Workbook/Trigger/WORKBOOK_MANUSCRIPT_READY.md`, listing the DOCX and MD file names, their modified dates and SHA-256 hashes, the parity result, and the registry entries.
- Otherwise → `WORKBOOK_MANUSCRIPT_INCOMPLETE.md` with the blockers.

PHASE 3 does not start the workbook design without `WORKBOOK_MANUSCRIPT_READY.md`. Everything else in PHASE 3 may run without it.

### W1. Design (Claude Design, PHASE 3) and layout (<AUTHOR>, InDesign)

1. **Claude Design builds the workbook** from the workbook manuscript (the MD staged from W0, with the DOCX as the authority):
   - `DesignPacket/packet/workbook/Ch<N>_Workbook.dc.html`
   - `DesignPacket/Ch<N>_Workbook_eBook_Print7x10.dc.html` (the eBook and print layout)

   PHASE 3.5 reviews it with the rest of the DesignPacket.
2. **<AUTHOR> produces both formats in InDesign** from the Claude Design workbook, at the same time as the chapter's eBook and print work:

| Export | Spec |
|---|---|
| **eBook** | **8.5×11 in** (US Letter) pages, RGB PDF. Bookmarks for every exercise, working internal links, document title and language set; fillable form fields are optional. Readers are encouraged to work on screen. If they print it anyway, it prints normally on a home printer: no bleed or crop marks, and margins wide enough (about 0.5 in or more) that nothing is clipped |
| **Print** | **7×10 in**, full color, CMYK, PDF/X-4, bleed and crop marks per the printer's spec, a gutter wide enough to write near the spine, real write-in space (lines or boxes sized for handwriting) |

### W2. Upload: the cue that the chapter's workbook is done

**The book's workbook profile (set once, v1.1).** `_BookGovernance/Workbook/Workbook_ExerciseRegistry.json` carries a book-level `workbook` object. Every phase reads it, so no phase assumes a format:

```json
"workbook": { "enabled": true, "formats": ["ebook"], "location": "book-root" }
```

- `enabled: false`: the book has no workbook.
  - PHASE 2 writes `<CH_ROOT>/Workbook/Trigger/WORKBOOK_NOT_APPLICABLE.md` in place of the W0 gate, and 3W doesn't run.
  - PHASE 6.5 and PHASE 7 accept that file in place of `WORKBOOK_READY.md`.
- `formats`: `["ebook"]` or `["ebook", "print"]`. Only the listed formats are required, uploaded, hashed, and checked. A missing format is never a defect.
- `location`: `chapter` (each chapter's `Workbook/`) or `book-root` (`<WORKBOOK_BOOK_ROOT>`; see below).

When the exports are final, <AUTHOR> uploads them to the location the profile names:

- **The chapter's `Workbook/` folder:**
  - `<CH_ROOT>/Workbook/<ChapterName>_Workbook_eBook.pdf`
  - `<CH_ROOT>/Workbook/<ChapterName>_Workbook_Print.pdf` (if the book ships a print workbook)
- **The book's workbook folder (v1.1):** `<WORKBOOK_BOOK_ROOT>/<section folder>/`, laid out in reading order the same way as the assembled workbook.
  - **eBook:** `<NN>_Ex_<L>_<N>_Chapter<C>.pdf` (e.g. `03_Part_I_The_Self/01_Ex_1_1_Chapter1.pdf`).
  - **Print** (only if `formats` includes it; v3.4): in `<WORKBOOK_BOOK_ROOT>/InDesign/`, named after the section's eBook PDF plus `_Print7x10`, i.e. `<WORKBOOK_BOOK_ROOT>/InDesign/<NN>_Ex_<L>_<N>_Chapter<C>_Print7x10.pdf`. The eBook stem is what pairs the two files (W2b).
  - `Chapter<C>` ties the PDF to its chapter, and `Ex_<L>_<N>` to its exercise.
  - Front matter and opener pages have no `Chapter<C>`, so they don't start a sync.

**The upload is the trigger, and it completes PHASE 3.5 for the workbook.** Nothing is uploaded until it's final.
- **W3 starts only when the upload is complete:** every exercise the registry assigns to the chapter has a PDF in every format the profile lists, and nothing has changed for 30 minutes.
  - A partial upload (one exercise of two, or the eBook without a required print file) waits, and never produces a READY file.
  - `WORKBOOK_READY.md` records the hash of every one of those files.
- A later re-upload (a file newer than `WORKBOOK_READY.md`) re-runs W3.

### W2b. Print QA on upload (report-only, v3.4)

**Only when the profile's `formats` includes `print`.** With `["ebook"]` there is no print workbook: record **print QA: N/A** and skip this step.

The workbook print PDF gets the same deterministic check as the book's print PDF (PHASE 4 Part 0P; reference implementation `print_check.py` in `<LOCAL_TOOLS_ROOT>`). It runs automatically when a print PDF or its eBook PDF changes, after 5 quiet minutes, and emails <AUTHOR> when the findings change.

| Mode | Print PDF in `<WORKBOOK_BOOK_ROOT>/InDesign/` | Compared with | Report in `<BOOK_ROOT>/_BookGovernance/PrintQA/` |
|---|---|---|---|
| **Per section** | `<eBook stem>_Print7x10.pdf` | the section's eBook PDF with that stem, anywhere in the workbook tree (e.g. `<section folder>/<eBook stem>.pdf`) | `Workbook_<eBook stem>_PrintQA.md` + `.json` |
| **Whole workbook** | any other `*Print*.pdf` | the assembled workbook eBook PDF at `<WORKBOOK_BOOK_ROOT>` | `Workbook_PrintQA.md` + `.json` |

- **Checked:** text drift against the eBook PDF (line breaks, hyphenation, spacing, running heads, and folios ignored), and the print layout checks: widows, orphans, runts, stranded headings, stacked hyphens, doubled words, safe zone and trim, 7×10 trim and bleed, embedded and Type3 fonts, images under 300 ppi, RGB images, blank pages. See PHASE 4 Part 0P for the severities.
- **Page size:** the eBook is 8.5×11 in and the print is 7×10 in. That difference is expected; only wording is compared between them.
- **Print-only differences:** <AUTHOR> logs them as quoted phrases in a `*PrintOnlyDifferences*.md` file at `<WORKBOOK_BOOK_ROOT>` (e.g. `Workbook_PrintOnlyDifferences.md`). The next run skips them.
- **Fixes:** layout and print wording go into the print InDesign workbook, then re-export. Wording that should reach the workbook manuscript goes into the eBook InDesign workbook, then re-export and re-upload, which re-runs W3.
- Keep one print PDF per section; rename an older export `*_superseded_<timestamp>.pdf`.

The `location: chapter` layout (`Workbook/<ChapterName>_Workbook_Print.pdf`) isn't covered by this check; W3 steps 3 and 5 are done by hand there.

### W3. Workbook sync and check (Claude)

Run when W2's files appear or change. Write `<CH_ROOT>/Governance/<ChapterName>_WorkbookQA_<YYYYMMDD_HHMM>.md`.

1. **Sync the manuscript to the eBook PDF** (the same model as PHASE 4 Part 0 for the chapter manuscript). Extract the eBook PDF's text and compare it with the workbook DOCX.
   - Wording <AUTHOR> changed during layout is copied back into the DOCX, and the MD is regenerated from the DOCX.
   - Back up both first to `Governance/_Backups/<YYYYMMDD>_WorkbookSync/`.
   - Record each change (location, before, after) in the QA report.
   - Anything uncertain (a possible typo in the PDF, a change that alters an exercise's meaning, an exercise ID change) is **not** applied.
     - It goes to `<CH_ROOT>/_Pipeline/P3W_DECISIONS.md` as a table (# · Location · DOCX text · PDF text · Why flagged · Recommendation · **Decision**, left blank).
     - <AUTHOR> writes *Accept PDF*, *Keep DOCX*, or *Defer* (with initials) in the Decision column. The next W3 run applies those decisions.
     - *Keep DOCX* means the PDF is wrong: fix it in InDesign and re-upload.
2. **Confirm PDF = DOCX = MD.** After the sync, all three give 0 word differences (ignoring page furniture: running heads, page numbers, and write-in lines).
3. **Print and eBook match.** The print PDF has the same exercises, in the same order, with the same wording and exercise IDs as the eBook PDF. Page breaks may differ, since the page sizes differ. Evidence (v3.4): the W2b print QA report shows 0 text differences to check, and any remaining difference is logged as print-only. (Skip this, and step 5, when the book ships no print workbook; record "print: n/a".)
4. **Exercise registry.** Re-check the chapter's entries against the synced workbook and the chapter manuscript (blocking rules as in the W0 gate). If the registry file, or this chapter's entries, don't exist yet (for example, a chapter built before v1.0.3 that skipped the W0 gate), create them now. **W3 never skips this step**, and `WORKBOOK_READY.md` can't be written without it.
5. **Print preflight** (from the print PDF): 7×10 in trim plus bleed, CMYK output intent (PDF/X-4), fonts embedded, images at 300 ppi or better at placed size, and no RGB-only or spot colors the printer doesn't accept. Use the W2b report for trim, bleed, fonts, image resolution, and RGB images (0 layout errors; warnings fixed or accepted by <AUTHOR>). The CMYK output intent and spot colors are still checked here.
6. **eBook checks:**
   - 8.5×11 in pages;
   - bookmarks cover every exercise, and internal links work;
   - the title and language are set;
   - fillable fields (if used) tab in reading order;
   - a test print to Letter at 100% clips nothing.

**Result:** before writing either file, rename any existing `WORKBOOK_READY.md` to `WORKBOOK_READY_superseded_<YYYYMMDD_HHMM>.md`. A re-upload that fails W3 must never leave the previous READY file standing for the new PDFs. Then:
- No blocking items, and <AUTHOR> has decided every uncertain sync item → `<CH_ROOT>/Workbook/Trigger/WORKBOOK_READY.md`. It lists:
  - the QA report;
  - the two PDF file names, dates, and **SHA-256 hashes**;
  - the synced DOCX/MD versions and hashes;
  - the number of sync changes;
  - any items <AUTHOR> accepted.
- Otherwise → `WORKBOOK_INCOMPLETE.md` with the blockers.

**Readiness is bound to the files.** Every consumer of `WORKBOOK_READY.md` (W4, PHASE 6.5, PHASE 7) recomputes the hashes of the uploaded PDFs (in `Workbook/` or `<WORKBOOK_BOOK_ROOT>`) and treats the trigger as stale if any hash differs from the recorded one.

`WORKBOOK_READY.md` does **not** block `DESIGN_READY.md` or anything in PHASES 4–6; the workbook is not a Kindle, audiobook, or RAG input. It is required for PHASE 6.5's workbook sub-certification and for PHASE 7.

---

## 3. When the chapter's final wording changes (PHASE 4 Part 0)

PHASE 4 Part 0 syncs the chapter manuscript to the final eBook PDF, and its downstream impact list already searches `Workbook/`. For the workbook, it also checks:

- every exercise ID the chapter manuscript mentions still matches the registry;
- any changed wording that the workbook quotes or depends on.

Each hit is a follow-up for <AUTHOR>. If the fix belongs in the workbook:
1. Edit the workbook DOCX and regenerate the MD.
2. Revise the InDesign workbook to match.
3. Re-export and re-upload (W2), which re-runs W3.

A stale `WORKBOOK_READY.md` (older than a PHASE 4 Part 0 sync that flagged the workbook) is renamed `WORKBOOK_READY_superseded_<timestamp>.md`.

---

## 4. Per book: the two workbook deliverables

### W4. Book assembly (<AUTHOR>, InDesign book file)

**Entry gate:**
- every chapter has a current `WORKBOOK_READY.md` (not superseded, and its recorded PDF hashes match the files in `Workbook/`);
- `_BookGovernance/Audit/Trigger/AUDIT_FINAL_CLEAR.md` exists (PHASE 4 Part B step B0), so exercise IDs and manuscript wording are frozen.

<AUTHOR> assembles the workbook InDesign book (INDB in `<WORKBOOK_INDESIGN_ROOT>`) with its front matter (title page, copyright, how to use this workbook, contents) and back matter, then exports and uploads:

| Deliverable | Folder | Files |
|---|---|---|
| <BOOK>_WORKBOOK_EBOOK | `_BookPublication/<BOOK>_WORKBOOK_EBOOK/` | `<BOOK>_Workbook_eBook.pdf` (8.5×11 in) |
| <BOOK>_WORKBOOK_PRINT_BOOK | `_BookPublication/<BOOK>_WORKBOOK_PRINT_BOOK/` | `<BOOK>_Workbook_Print.pdf` (7×10 in interior); `<BOOK>_Workbook_Cover.pdf` (full-wrap cover, if printed separately) |

### W5. Book check (Claude, report-only)

Write `_BookPublication/<BOOK>_WORKBOOK_EBOOK/<BOOK>_Workbook_AssemblyReport.md`:

- every chapter's exercises appear, in Lesson order, and match that chapter's synced workbook DOCX/MD (so the book PDFs = the chapter DOCX = the chapter MD);
- if the front and back matter have their own DOCX, they match the book PDFs too;
- the contents page and bookmarks match the exercise registry;
- the registry has no open blocking items against the synced chapter manuscripts;
- the print interior passes the W3 step 5 preflight (with a whole-workbook print PDF in `<WORKBOOK_BOOK_ROOT>/InDesign/`, cite `Workbook_PrintQA.md` from W2b), and the page count and spine width are recorded for the cover;
- the eBook passes the W3 step 6 checks for the whole book.

PHASE 6.5 book mode certifies the workbook from this report; <AUTHOR> signs off in PHASE 7.

---

## 5. Gates at a glance

| Gate | When | Means |
|---|---|---|
| `WORKBOOK_MANUSCRIPT_READY.md` | End of PHASE 2, before the PHASE 3 workbook design | DOCX = MD; exercise IDs registered and matching the chapter manuscript |
| Workbook print QA report (v3.4; print only) | After each print PDF upload (W2b) | Print wording = eBook wording; no layout errors; report-only |
| `WORKBOOK_READY.md` | After the W2 upload and the W3 sync | PDF = DOCX = MD; print and eBook match; preflight and eBook checks pass |
| Workbook assembly report | After W4, once per book | Book PDFs match every chapter's workbook manuscript; no blocking items |

---

## 6. Rules

- **The DOCX is canonical** for workbook content; the Markdown is its replica, regenerated from the DOCX and never hand-edited on its own.
- **Never edit the PDFs.** Fixes are made in InDesign by <AUTHOR>, then re-exported and re-uploaded. Wording changes made in InDesign flow back to the DOCX and MD through W3.
- **Never read or copy `<WORKBOOK_INDESIGN_ROOT>`.** Its files stay where their links and fonts work.
- **No workbook content goes to Kindle, the audiobook, or RAG.** The Kindle book's per-chapter Practice Section (PHASE 4 Part A, 5B) carries only the main exercise text that the chapter manuscript already includes; it isn't a workbook edition.
- **Back up before overwriting** any workbook DOCX or Markdown (`Governance/_Backups/<YYYYMMDD>_<reason>/`); never delete.
