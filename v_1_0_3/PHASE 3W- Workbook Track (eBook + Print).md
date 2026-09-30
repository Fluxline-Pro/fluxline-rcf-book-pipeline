# PHASE 3W: Workbook Track (eBook + Full-Color Print) (v1.0)

> **Pipeline position:** a side track that runs **alongside PHASE 3 / 3.5** for each chapter, then once per book after PHASE 4 Part B step B0 · **Upstream gate:** `Governance/Trigger/GOVERNANCE_READY.md` (per chapter) · **Downstream:** PHASE 6.5 (workbook sub-certification), PHASE 7
> **Canonical paths, status ladder, triggers, and deliverables:** see `MASTER_PIPELINE_OVERVIEW.md`.

**New in v1.0.3 (2026-09-30).** The workbook ships in two formats only: an **eBook (PDF)** and a **full-color print book**, both laid out by <AUTHOR> in InDesign. It has **no Kindle edition, no audiobook, and no RAG ingestion**. Before this file, the workbook's steps were spread across PHASES 1–7, and several of them assumed an HTML-built eBook, a Kindle edition, and RAG ingestion.

---

## 1. What the workbook is, and what it isn't

| In scope | Out of scope |
|---|---|
| Workbook eBook PDF (RGB, bookmarks, links; fillable fields optional) | Kindle / KDP reflowable workbook |
| Full-color print workbook PDF (CMYK, print-ready) | Audiobook, narration, XTTS |
| Per-chapter exercise content (PHASE 1 Workbook Exercise Packet) | RAG ingestion (Local or Cloud), `RAG_Workbook.html` |
| The exercise registry (exercise IDs ↔ manuscript mentions) | A Claude Design `Workbook_Master.html` eBook build |

**Numbering:** workbook exercises are numbered by **Lesson**, not by chapter (for example, `Exercise 1.4` belongs to Lesson 1 and appears in Chapter 4). The manuscript points readers into the workbook ("Begin Exercise 1.4 in your workbook"), so the workbook and the manuscript must agree on every exercise ID.

**Where the InDesign files live:** <AUTHOR> keeps the workbook InDesign documents, the book file (INDB), linked assets, and fonts in `<WORKBOOK_INDESIGN_ROOT>`, outside `<BOOK_ROOT>`, so links and fonts don't break. No phase reads, copies, or checks `.indd`/`.indb` files. Phases check only the **exported PDFs** <AUTHOR> uploads.

---

## 2. Per chapter (during PHASE 3 / 3.5)

### W0. Content source (PHASE 1–2 output, unchanged)

| File | Location | Made in |
|---|---|---|
| Workbook Exercise Packet (Markdown) | `<CH_ROOT>/Workbook/<ChapterName>_WorkbookPacket.md` | PHASE 1 Step 2 |
| Workbook exercise DOCX | `<CH_ROOT>/Workbook/<ChapterName>_Exercise<L.N>_Workbook.docx` | PHASE 1 Step 2 |

The same rule as the manuscript applies: **the DOCX is canonical; the Markdown is its replica.** If <AUTHOR> edits the DOCX, the Markdown is regenerated from it (with a backup) before W2.

### W1. Layout (<AUTHOR>, manual in InDesign)

<AUTHOR> lays out the chapter's workbook pages in InDesign at the same time as the chapter's eBook and print work in PHASE 3. The Claude Design workbook layout (`DesignPacket/Ch<N>_Workbook_eBook_Print7x10.dc.html`) is an optional **reference** for components and styling, never the source of the eBook.

One layout serves both exports:

| Export | Spec |
|---|---|
| **Print** | Full color, CMYK, PDF/X-4, bleed and crop marks per the printer's spec, trim `<WORKBOOK_TRIM>`, a gutter wide enough to write near the spine, real write-in space (lines or boxes sized for handwriting) |
| **eBook** | RGB PDF, bookmarks for every exercise, working internal links, document title and language set; fillable form fields are optional |

### W2. Upload: the cue that the chapter's workbook is done

When both exports are final, <AUTHOR> uploads them to the chapter's `Workbook/` folder:

- `<CH_ROOT>/Workbook/<ChapterName>_Workbook_eBook.pdf`
- `<CH_ROOT>/Workbook/<ChapterName>_Workbook_Print.pdf`

**The upload is the trigger.** Nothing is uploaded until both files are final; a later re-upload (a file newer than `WORKBOOK_READY.md`) re-runs W3.

### W3. Workbook check (Claude, report-only)

Run when W2's files appear or change. Write `<CH_ROOT>/Governance/<ChapterName>_WorkbookQA_<YYYYMMDD_HHMM>.md`.

1. **Content match.** Extract the text of the eBook PDF and compare it with the canonical workbook DOCX (W0): every exercise, prompt, and instruction is present, with the same wording. List any difference; <AUTHOR> decides whether the PDF or the DOCX is right. An intentional layout-time wording change is copied back to the DOCX (and the Markdown regenerated), the same way PHASE 4 Part 0 treats the manuscript.
2. **Print and eBook match.** The print PDF has the same pages, in the same order, with the same exercise IDs as the eBook PDF.
3. **Exercise registry.** Update `_BookGovernance/Workbook/Workbook_ExerciseRegistry.json` for this chapter: one entry per exercise with `exerciseId`, `lesson`, `chapter`, `title`, and `manuscriptMentions` (each place the manuscript names it). **Blocking:** an exercise the manuscript mentions that the workbook doesn't have, or a number that differs between them.
4. **Print preflight** (from the PDF): page size matches `<WORKBOOK_TRIM>` plus bleed, CMYK output intent (PDF/X-4), fonts embedded, images at 300 ppi or better at placed size, and no RGB-only or spot colors the printer doesn't accept.
5. **eBook checks:** bookmarks cover every exercise, internal links work, the title and language are set, and fillable fields (if used) tab in reading order.

**Result:**
- No blocking items → `<CH_ROOT>/Workbook/Trigger/WORKBOOK_READY.md` (lists the QA report, the two PDF file names and their dates, and any items <AUTHOR> accepted).
- Otherwise → `WORKBOOK_INCOMPLETE.md` with the blockers.

`WORKBOOK_READY.md` does **not** block `DESIGN_READY.md` or anything in PHASES 4–6; the workbook is not a Kindle, audiobook, or RAG input. It is required for PHASE 6.5's workbook sub-certification and for PHASE 7.

---

## 3. When the final wording changes (PHASE 4 Part 0)

PHASE 4 Part 0 syncs the manuscript to the final eBook PDF, and its downstream impact list already searches `Workbook/`. For the workbook, it also checks:

- every exercise ID the manuscript mentions still matches the registry;
- any changed wording that the workbook quotes or depends on.

Each hit is a follow-up for <AUTHOR>: revise the InDesign workbook, re-export, and re-upload (W2), which re-runs W3. A stale `WORKBOOK_READY.md` (older than a PHASE 4 Part 0 sync that flagged the workbook) is renamed `WORKBOOK_READY_superseded_<timestamp>.md`.

---

## 4. Per book: the two workbook deliverables

### W4. Book assembly (<AUTHOR>, InDesign book file)

**Entry gate:**
- every chapter has a current `WORKBOOK_READY.md`;
- `_BookGovernance/Audit/Trigger/AUDIT_FINAL_CLEAR.md` exists (PHASE 4 Part B step B0), so exercise IDs and manuscript wording are frozen.

<AUTHOR> assembles the workbook InDesign book (INDB in `<WORKBOOK_INDESIGN_ROOT>`) with its front matter (title page, copyright, how to use this workbook, contents) and back matter, then exports and uploads:

| Deliverable | Folder | Files |
|---|---|---|
| <BOOK>_WORKBOOK_EBOOK | `_BookPublication/<BOOK>_WORKBOOK_EBOOK/` | `<BOOK>_Workbook_eBook.pdf` |
| <BOOK>_WORKBOOK_PRINT_BOOK | `_BookPublication/<BOOK>_WORKBOOK_PRINT_BOOK/` | `<BOOK>_Workbook_Print.pdf` (interior); `<BOOK>_Workbook_Cover.pdf` (full-wrap cover, if printed separately) |

### W5. Book check (Claude, report-only)

Write `_BookPublication/<BOOK>_WORKBOOK_EBOOK/<BOOK>_Workbook_AssemblyReport.md`:

- every chapter's exercises appear, in Lesson order, and match the chapter PDFs that passed W3;
- the contents page and bookmarks match the exercise registry;
- the registry has no open blocking items against the synced manuscripts;
- the print interior passes the W3 step 4 preflight; page count and spine width are recorded for the cover;
- the eBook passes the W3 step 5 checks for the whole book.

PHASE 6.5 book mode certifies the workbook from this report; <AUTHOR> signs off in PHASE 7.

---

## 5. Exit gates

**Per chapter:** `WORKBOOK_READY.md` is present and newer than the chapter's latest PHASE 4 Part 0 sync that flagged the workbook.

**Per book:** both workbook deliverables are uploaded, the assembly report lists no blocking items, and PHASE 6.5 book mode certifies the workbook.

---

## 6. Rules

- **The DOCX is canonical** for workbook content; the Markdown is its replica.
- **Never edit the PDFs.** Fixes are made in InDesign by <AUTHOR>, then re-exported and re-uploaded.
- **Never read or copy `<WORKBOOK_INDESIGN_ROOT>`.** Its files stay where their links and fonts work.
- **No workbook content goes to Kindle, the audiobook, or RAG.** The Kindle book's per-chapter Practice Section (PHASE 4 Part A, 5B) carries only the main exercise text that the manuscript already includes; it isn't a workbook edition.
- **Back up before overwriting** any workbook DOCX or Markdown (`Governance/_Backups/<YYYYMMDD>_<reason>/`); never delete.
