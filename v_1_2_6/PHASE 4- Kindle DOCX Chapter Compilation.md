# PHASE 4: Final-Wording Builds — Manuscript Sync, Print QA, Kindle DOCX, Audiobook (v3.4)

> **Pipeline position:** PHASE 4 of 7 (Kindle) · **Upstream gate:** a current `Manuscript/Trigger/MANUSCRIPT_LOCKED.md` (PHASE 2.5, release v1.2.5) **and** the final eBook PDF is uploaded, which completes PHASE 3.5 (v3.3); `DESIGN_READY.md` is written by PHASE 3.5 or, if absent, attested by the upload · **Downstream:** PHASE 5 RAG Rebuild
> **Canonical paths, status ladder, triggers, and deliverables:** see `MASTER_PIPELINE_OVERVIEW.md`.

**Release v1.2.6 (2026-10-26): Step 0C, the congruency check.**
- **New Step 0C** (section 0C below), after Part 0, 0R, 0G and 0P and before Part A. One deterministic report says whether the manuscript, the eBook PDF, the print PDF, the narration script and the workbook say the same thing, and whether every file is current against `MANUSCRIPT_LOCKED.md`. Verdict **PASS** or **HOLD**. Part A starts only on PASS (pass 1).
- **Pass 2** runs after Part C. It adds the Kindle DOCX and the audiobook QA, and gates PHASE 5 and 6.5.
- **Why:** each pair of formats was already checked on its own (Part 0: eBook against manuscript; 0P: print against eBook; Part C: audio against script). Nothing put them in one result, and three things were not checked at all: the narration script against the locked manuscript, the freshness of every file against the lock, and the book's exercise numbers and titles against the workbook.
- Chapters that predate the lock (Ch1 to Ch5 of the first book) get the report only; it never gates them.

**Release v1.2.5 (2026-10-24): the manuscript is locked before design (PHASE 2.5), and B0 is reduced.**
- **The lock gates Part 0, Part A, and Part C.** Each needs `Manuscript/Trigger/MANUSCRIPT_LOCKED.md`. Part 0 checks it is current (0.1); Step 0 and Part C check the hashes again.
- **Part 0 expects no differences.** Any difference between the final eBook PDF and the locked manuscript is a post-lock change, so S1 and S2 differences now need <AUTHOR>'s decision too, in `_Pipeline/P4_DECISIONS.md` (0.3–0.5).
- **B0 (PHASE 0.9 Mode D) is a consistency and delta check,** not a full content audit: a cross-chapter consistency pass over the whole book, plus a check of what changed in each chapter since its lock. It doesn't reopen a manuscript except for a genuine cross-chapter conflict, and then only with <AUTHOR>'s approval.
- **Part C is recorded only after the lock,** so the audiobook is never recorded from text that the content audit could still change.

**Release v1.1.3 (2026-10-21):** Part 0 has a new stop in 0.1. If `Manuscript/Trigger/MANUSCRIPT_REVISED.md` is newer than the eBook PDF, Part 0 asks for a re-export instead of syncing, which would undo the revision. There is also a note on the PHASE 3.5A print build.

**v3.4 changes (2026-10-03, release v1.1.2):**
- **New Part 0P, print vs. eBook QA (report-only):** <AUTHOR> uploads each finished section's print PDF (7×10, exported from the print InDesign book) to `<CH_ROOT>/InDesign/<ChapterName>_Print7x10.pdf`. A deterministic check (no LLM) compares its text with the final eBook PDF and flags print-layout problems. It doesn't block Part A, but it must be closed before PHASE 6.5 and PHASE 7.
- **The print cross-check in 0.6 is now evidenced by the 0P report.** <AUTHOR> still confirms the print-only differences, and logs them in `<ChapterName>_PrintOnlyDifferences.md`.
- The print *InDesign book* still lives outside `<BOOK_ROOT>`; only its exported PDF is uploaded.
- The same check covers the print workbook (PHASE 3W W2b), when the book ships one.

**v3.3 changes (2026-10-02, release v1.1):**
- **The upload is the gate.** <AUTHOR>'s upload of the final eBook PDF completes PHASE 3.5 and starts PHASE 4, after 30 quiet minutes. If `DESIGN_READY.md` is missing, Part 0 writes it as attested by the upload.
  - The PDF may be named `<ChapterName>_eBook.pdf` (preferred) or `<ChapterName>_eBookPDF.pdf`.
- **New step 0R, references re-check (report-only):** after the sync, the chapter's citations and references are checked again. The manuscript is now locked to the eBook, so nothing is auto-fixed. Findings go to <AUTHOR>; a fix goes into the eBook InDesign book, then re-export, then Part 0 re-runs.
- **New step 0G, glossary lock:** the locked manuscript is the moment the chapter's glossary is finalised.
  - The chapter's `GlossaryNormalized.json` is refreshed from the synced text, applying the defining-chapter rules in `_BookGovernance/Glossary/Glossary_Canonical.json`.
  - The book-level master glossary and drift report are rebuilt. Only **locked** chapters enter the official master.
  - Both new steps come before Step 0 and Part A.

**v3.2 changes (2026-09-30 workbook track):** the Kindle workbook (B5) is removed; the workbook ships as an eBook PDF and a print book from `PHASE 3W- Workbook Track (eBook + Print).md`. The Part 0 downstream impact list also checks exercise IDs against the workbook exercise registry.

**v3.1 changes (2026-09-27 book audit + audiobook timing):**
- Part 0 gains step **0.7**, a PHASE 0.9 spot check (Mode P) of the chapter's synced text. `MANUSCRIPT_SYNCED.md` now requires that no blocking audit finding is open for the chapter.
- Part B opens with step **B0**, the PHASE 0.9 final delta audit, and waits for `AUDIT_FINAL_CLEAR.md`.
- **The final eBook PDF is the trigger** for the chapter's final-wording chain: Part 0 sync → 0.7 spot check → Part A Kindle build → Part C audiobook → PHASE 5 onward.
- **New Part C: Audiobook**, moved here from PHASE 3 and run **after Part A**, because the audiobook is recorded from the Kindle output. The narration script is rebuilt from the Kindle build. XTTS makes an optional draft for pacing, and <AUTHOR> records the final narration in Adobe Audition. The book-level `<BOOK>_AUDIOBOOK` set is now assembled in Part B.

**v3 changes (2026-09-22 pipeline alignment):**
- One path root: `<CH_ROOT>` = `<BOOK_ROOT>/Chapters/<ChapterName>/Final/` (the old file mixed three different roots).
- The three PHASE 4 deliverables are now separate files (DOCX, HTML blocks, metadata) instead of "HTML embedded in DOCX", matching the files already in Chapters 1–3.
- The eBook-folder section was merged into Step 1 and Step 2 so the steps are no longer duplicated.
- Optional sections (Instructor Notes, Further Exploration) now use a build profile. Marketing seeds may appear only if <AUTHOR> has approved them.
- Adds front matter, Part, and back matter handling, plus the exit gate.
- **Kindle decision (2026-09-22):** PHASE 4 is now the **only** place Kindle files are made. PHASE 3 no longer produces a Kindle edition. Adds Step 0 (dependency check), figure images from `DesignPacket/figures_export/`, and Part B (book-level `<BOOK>_KINDLE_EBOOK` assembly from the per-chapter builds).
- **Manuscript sync patch (2026-09-23):** adds **Part 0**, which runs before anything else in PHASE 4. <AUTHOR> makes small wording changes while laying out the eBook and print InDesign books, so the manuscript (MD and DOCX) is brought into line with the final eBook PDF before the Kindle build reads it. If the eBook PDF is not uploaded, PHASE 4 stops, and so does everything after it.

---

**Purpose:**
Transform the governed, design-validated PHASE 1–3.5 chapter outputs into a **Kindle-ready DOCX** for *that chapter only*, plus its Kindle HTML blocks and Kindle metadata. The `Final/` folder is the only source of truth.

## Deliverables

### Part 0 — manuscript sync (per chapter, before Part A)

| Deliverable | Path |
|---|---|
| Updated manuscript (Markdown) | `<CH_ROOT>/Manuscript/<ChapterName>_Manuscript.md` |
| Updated manuscript (Word) | `<CH_ROOT>/Manuscript/<ChapterName>_Manuscript.docx` |
| Sync report (every difference, what was applied, what was flagged) | `<CH_ROOT>/Manuscript/<ChapterName>_ManuscriptSync_<YYYYMMDD_HHMM>.md` |
| Sync trigger | `<CH_ROOT>/Manuscript/Trigger/MANUSCRIPT_SYNCED.md` or `<CH_ROOT>/Manuscript/Trigger/MANUSCRIPT_SYNC_INCOMPLETE.md` |

### Part 0P — print vs. eBook QA (per chapter or section, whenever the print PDF is uploaded; v3.4)

| Deliverable | Path |
|---|---|
| Print PDF (<AUTHOR>'s upload, the input) | `<CH_ROOT>/InDesign/<ChapterName>_Print7x10.pdf` |
| Print-only differences (<AUTHOR>) | `<CH_ROOT>/<ChapterName>_PrintOnlyDifferences.md` |
| Print QA report | `<BOOK_ROOT>/_BookGovernance/PrintQA/<ChapterName>_PrintQA.md` + `.json` |

### Step 0C — congruency check (per chapter or section; v1.2.6)

| Deliverable | Path |
|---|---|
| Congruency report, pass 1 (before Part A) | `<BOOK_ROOT>/_BookGovernance/CongruencyQA/<ChapterName>_Congruency.md` + `.json` |
| Congruency report, pass 2 (after Part C) | `<BOOK_ROOT>/_BookGovernance/CongruencyQA/<ChapterName>_Congruency_Pass2.md` + `.json` |
| Differences <AUTHOR> has reviewed | `<BOOK_ROOT>/_BookGovernance/CongruencyQA/<ChapterName>_Accepted.json` |
| Manual trigger (optional) | `<CH_ROOT>/Manuscript/Trigger/RUN_CONGRUENCY.md` (Parts and Lessons: `<PART_DIR>/Trigger/RUN_CONGRUENCY.md`) |

### Part A — per chapter (run chapter by chapter)

| Deliverable | Path |
|---|---|
| Kindle DOCX per chapter | `<CH_ROOT>/Kindle/<ChapterName>_Kindle.docx` |
| Kindle-ready HTML blocks | `<CH_ROOT>/Kindle/<ChapterName>_Kindle.html` |
| Kindle-ready metadata | `<CH_ROOT>/Kindle/<ChapterName>_KindleMetadata.json` |
| Kindle figure images (Kindle-sized copies) | `<CH_ROOT>/Kindle/figures/<ChapterName>_Fig<#>_<Name>.jpg` |
| PHASE 4 checklist | `<CH_ROOT>/<ChapterName>_PHASE4_KindleChecklist.md` |

### Part C — per chapter, after Part A (the audiobook is recorded from the Kindle output)

| Deliverable | Path |
|---|---|
| Narration script built from the Kindle output | `<CH_ROOT>/Audiobook/<ChapterName>_NarrationScript.md` (pronunciation guide and segment markers kept) |
| XTTS draft (optional pacing guide; never published) | `<CH_ROOT>/Audiobook/Drafts/<NN>_<ChapterName>_XTTS_Draft.mp3` |
| **Final narration** (<AUTHOR>, Adobe Audition, manual) | `<CH_ROOT>/Audiobook/<NN>_<ChapterName>.mp3` (NN = book running order, matching FrontMatter numbering) |
| Audiobook check (in the PHASE 4 checklist) | `<CH_ROOT>/<ChapterName>_PHASE4_KindleChecklist.md` → `audiobookStatus` |

### Part B — book level (once every chapter has passed Part A and Part C)

| Deliverable | Path |
|---|---|
| Cross-chapter consistency + since-lock delta check (PHASE 0.9 Mode D, reduced in v1.2.5) | `<BOOK_ROOT>/_BookGovernance/Audit/<RUN_ID>/` + `Audit/Trigger/AUDIT_FINAL_CLEAR.md` |
| **<BOOK>_KINDLE_EBOOK** | `<BOOK_ROOT>/_BookPublication/<BOOK>_KINDLE_EBOOK/` |
| **<BOOK>_AUDIOBOOK** (ordered MP3 set + track list) | `<BOOK_ROOT>/_BookPublication/<BOOK>_AUDIOBOOK/` |

---

# PART 0 — MANUSCRIPT SYNC FROM THE FINAL eBook PDF (run first)

**Why:** <AUTHOR> refines wording while laying out the eBook and the print InDesign books. Those edits land in the layouts, not in the manuscript. Everything from here on (Kindle, RAG, automation, marketing grounding) reads the manuscript, so it has to say what the published eBook says before any of it runs.

**Reference text:** the final eBook PDF. Part 0 syncs the manuscript to it alone. The print InDesign book is kept in <AUTHOR>'s separate print folders (INDB and template dependencies), outside `<BOOK_ROOT>`, and PHASE 4 never reads those folders. Its exported print PDF is uploaded to `<CH_ROOT>/InDesign/<ChapterName>_Print7x10.pdf` (v3.4), where Part 0P compares it with the eBook PDF. The print PDF is never a sync source, and Part 0 and Part A don't wait for it.

**This is the one sanctioned manuscript edit after the lock (PHASE 2.5), besides an approved `MANUSCRIPT_REVISED.md` revision.** It records <AUTHOR>'s own layout-stage wording back into the manuscript. It never introduces new wording, and it follows the same paper trail as a governance fix: back up, log, version, and escalate anything uncertain.

**The manuscript is final before PHASE 1 (release v1.1.3).** <AUTHOR> settles the wording in the DOCX before PHASE 1, and the eBook (Claude Design) and print (InDesign, from the PHASE 3.5A import) are built from it. Part 0 therefore expects **no differences**. It still runs as the safety check, and any difference it finds is reported and classified as before, so a layout-time edit can't slip past unrecorded.

**Revisions and the print build (release v1.1.3).** Before the eBook lock, <AUTHOR> may revise the DOCX through `Manuscript/Trigger/MANUSCRIPT_REVISED.md` (PHASE 1, "Revision trigger"). The eBook PDF must already carry such a revision, so check it first (0.1). Part 0 still syncs the MD and the DOCX to the eBook PDF; that sync is the only time the pipeline writes to the manuscript, and the print build (PHASE 3.5A) never does. If Part 0 changes the DOCX after a 3.5A build, the build's manifest no longer matches: re-run 3.5A if print layout hasn't started, otherwise carry the change into the print document (Part 0P catches anything missed).

## 0.1 Hard stop: the eBook PDF must be uploaded

Look for `<CH_ROOT>/eBook/<ChapterName>_eBook.pdf` (or `<ChapterName>_eBookPDF.pdf`), the final PDF exported from <AUTHOR>'s eBook InDesign book. (If the eBook is exported as one book-level PDF, save this chapter's pages under that name.) Its upload completes PHASE 3.5: if `DesignPacket/Trigger/DESIGN_READY.md` is missing, write it now, stating "PHASE 3.5 complete: attested by <AUTHOR>'s upload of <file> on <date>" and citing the latest DesignQA report, if any.

If the file is **missing**, empty, cannot be opened, or has no extractable text (image-only export):

1. Do **not** continue Part 0, Step 0, Part A, or Part B for this chapter.
2. Write `Manuscript/Trigger/MANUSCRIPT_SYNC_INCOMPLETE.md` stating `Blocked: final eBook PDF not uploaded` (or the specific problem) and the exact path expected.
3. Write the PHASE 4 checklist with `gateStatus: FAIL` and the same blocker.
4. Tell <AUTHOR> the path to upload to, and stop.

PHASE 5, 6, 6.5, and 7 cannot start for a chapter without a PHASE 4 `PASS`, so a missing PDF halts the chapter from PHASE 4 onward. Part B cannot start while any chapter is blocked here.

**Also a hard stop: the manuscript must be locked (release v1.2.5).** `Manuscript/Trigger/MANUSCRIPT_LOCKED.md` must exist, the DOCX and MD SHA-256 hashes it records must match the files, and no `MANUSCRIPT_REVISED.md` section may be newer than it. If any of these fails, write `MANUSCRIPT_SYNC_INCOMPLETE.md` stating `Blocked: manuscript not locked (PHASE 2.5)` or `Blocked: manuscript changed after its lock`, with the hashes found, set `gateStatus: FAIL`, and stop. The fix is PHASE 2.5 (or its delta audit after an approved revision), never a hand edit here.

Also stop, and ask, if:
- **`Manuscript/Trigger/MANUSCRIPT_REVISED.md` is newer than the eBook PDF** (v1.1.3). The manuscript was revised after this eBook was exported, so the PDF doesn't carry the revision, and syncing to it would undo the revision. Write `MANUSCRIPT_SYNC_INCOMPLETE.md` with `Blocked: manuscript revised after the eBook export (<revision date>) — re-export the eBook PDF`, list the revised sections from the trigger file, and ask <AUTHOR> to bring them into the eBook InDesign book and re-export. Part 0 runs again when the new PDF lands.
- `<CH_ROOT>/Manuscript/<ChapterName>_Manuscript.md` or `_Manuscript.docx` is missing. Both are kept in sync; do not create the DOCX from scratch without <AUTHOR>'s go-ahead.
- The PDF looks like a draft rather than the final layout: a Claude Design export, a watermark, placeholder figures, or a chapter title or number that does not match.

Record in the sync report: the PDF path, file size, modified date, page count, and <AUTHOR>'s confirmation that it is the final eBook export.

## 0.2 Extract and normalize

Extract the PDF's reading-order text, then drop layout artifacts **before** comparing, so they never show up as changes:

- running headers and footers, page numbers, folios, crop and bleed marks
- end-of-line hyphenation (rejoin `trans-` + `formation`; keep real hyphens such as `self-aware`)
- line breaks and column breaks inside a paragraph
- ligatures (`ﬁ` `ﬂ`), soft hyphens, non-breaking and thin spaces, discretionary breaks
- smart versus straight quotes and apostrophes, en/em dash spacing; follow the manuscript's convention
- figure images, figure labels, and captions (captions are checked against `Governance/<ChapterName>_FigureRegistry.json` in 0.3, not as body text)
- pull quotes and sidebars repeated from the body (compare those against `InDesign/` prep, not as body text)

Normalize the manuscript the same way (strip Markdown syntax for comparison only). Keep a map from each normalized paragraph back to its source location in the MD and the DOCX.

## 0.3 Compare and classify

Align paragraph by paragraph using headings as anchors, then diff at the word level. Classify every difference:

| Class | What it is | Action |
|---|---|---|
| **S1 — Wording** | Changed, added, or removed words, punctuation, or sentence order inside an existing paragraph | Apply to MD and DOCX |
| **S2 — Structure** | Paragraph split or merged, heading reworded, list re-itemized, emphasis (italic/bold) changed | Apply, matching the PDF, if unambiguous; otherwise flag |
| **S3 — Needs <AUTHOR>** | Changes a term in `GlossaryNormalized` or the TerminologyLock, a figure or chapter number, a quotation or citation, a factual claim, statistic, or credential; adds or removes a whole paragraph or section; or looks like a layout error (new typo, doubled word, text cut off at a frame edge, overset text) | **Do not apply.** List for <AUTHOR> with both versions and a recommendation |
| **S4 — Extraction noise** | Anything that survives 0.2 but is not a real change | Ignore; list in an appendix so it can be spot-checked |

Figure captions: compare PDF captions with `Governance/<ChapterName>_FigureRegistry.json`. A caption difference is S3; the FigureRegistry is updated only after <AUTHOR> confirms.

**After the lock (release v1.2.5), every S1 and S2 difference needs <AUTHOR> too.** The manuscript was locked in PHASE 2.5 and the eBook was built from it, so a difference is a post-lock change. Keep the class (S1, S2, S3) in the report, but list every S1 and S2 item in `_Pipeline/P4_DECISIONS.md` alongside the S3 items (0.5), and apply it only when <AUTHOR> writes `Accept PDF`. <AUTHOR> may decide the S1 rows as a group (`All S1: Accept PDF`). The decision file is the approval; Part 0 doesn't write `MANUSCRIPT_REVISED.md` (that would trip the 0.1 stop).

If more than roughly 5% of paragraphs differ, or alignment fails for a whole section, stop and ask <AUTHOR> before applying anything. That usually means the wrong PDF, the wrong manuscript version, or a failed extraction.

## 0.4 Apply S1 and S2 changes

From release v1.2.5, apply only the S1 and S2 rows <AUTHOR> accepted in `_Pipeline/P4_DECISIONS.md` (0.3).

1. Back up both files to `<CH_ROOT>/Governance/_Backups/<YYYYMMDD_HHMM>/Manuscript/` before the first edit.
2. **Markdown:** edit the affected text in place. Keep headings, anchors, figure references, and front-matter fields intact.
3. **DOCX:** edit the same text in place, keeping the existing paragraph and character styles, comments, and section breaks. Change only the runs that differ. Do not regenerate the DOCX from the Markdown.
4. Re-run the comparison. The only remaining differences must be S3 items (pending) and S4 noise. The MD and the DOCX must also match each other.

## 0.5 Resolve S3 items with <AUTHOR>

Present the S3 list (location, manuscript text, PDF text, why it is flagged, recommendation).

**The decision file (v1.1).** When <AUTHOR> isn't present, which is always the case in automated runs, write the list to `<CH_ROOT>/_Pipeline/P4_DECISIONS.md` as a table:

| # | Location (heading › paragraph) | Manuscript text | eBook PDF text | Why flagged | Recommendation | **Decision** |
|---|---|---|---|---|---|---|

- Leave **Decision** blank. <AUTHOR> writes `Accept PDF`, `Keep manuscript`, or `Defer — <initials>`, then requests a re-run.
- On every run, read this file first if it exists:
  - Apply each decided row as below, and carry blank rows forward.
  - Rename the file to `P4_DECISIONS_applied_<YYYYMMDD_HHMM>.md` once every row is decided and applied.
  - Rows whose PDF text no longer matches (because the PDF was re-exported) are re-evaluated, not applied.
- `MANUSCRIPT_SYNCED.md` can't be written while a row is blank.

For each item <AUTHOR> chooses:
- **Accept the PDF wording** → apply it to MD and DOCX (and the Glossary or FigureRegistry, if affected).
- **Keep the manuscript wording** → the eBook layout is wrong; list it as a layout fix for the eBook InDesign book (and the print book, if it carries the same text). The PDF must be re-exported and Part 0 re-run for the chapter before the gate passes.
- **Defer** → allowed only for non-substantive items, recorded with <AUTHOR>'s initials. A deferred item blocks nothing, but it is carried into the PHASE 7 release checklist.

## 0.6 Version and impact

- Increment `chapterVersion` in `Governance/<ChapterName>_VersionMetadata.json` (patch level: e.g. `1.0` → `1.0.1`), set `revisionDate`, and add a `majorChanges` entry: `"Manuscript synced to final eBook PDF: <n> wording changes, <n> structural"`. If nothing changed, leave the version alone and record `no differences`.
- Update the manuscript entries in `Governance/<ChapterName>_ArtifactManifest.json`.
- **Downstream impact list.** Search the chapter's derived artifacts for the old wording of every applied change and list each hit in the sync report: ReviewPacket, ReferenceGuides, Workbook (the exercise DOCX, and every exercise ID the manuscript mentions against `_BookGovernance/Workbook/Workbook_ExerciseRegistry.json`; see PHASE 3W §3. If the registry, or this chapter's entries, don't exist yet, record **"exercise-ID check pending (no registry)"** in the sync report. That is non-blocking here, because PHASE 3W W3 must create the entries and run the check before `WORKBOOK_READY.md` is written), Training, Slides, InDesign prep (pull quotes, sidebars), Audiobook narration script and recorded MP3 (and any re-record passages), eBook HTML blocks, Marketing Intake (claims registry, terminology lock, voice samples), and the PHASE 1 RAG packet. Do **not** edit them here. PHASE 4 Part A reads the updated manuscript, and PHASE 5 rebuilds RAG from it; the others go to <AUTHOR> as proposed follow-ups. Mark verbatim quotations (pull quotes, voice samples, claims) and narration as **must fix before release**; they are checked again in PHASE 6.5 and PHASE 7.
- **Print cross-check (<AUTHOR>, evidenced by Part 0P; v3.4).** Cite the latest `_BookGovernance/PrintQA/<ChapterName>_PrintQA.md`. Its text drift section shows whether the print PDF carries the same wording as the eBook PDF. <AUTHOR> confirms each remaining difference as print-only, and logs it in `<CH_ROOT>/<ChapterName>_PrintOnlyDifferences.md`, or has it fixed in the print InDesign book. If no print PDF is uploaded yet, record "print cross-check pending (no print PDF)". PHASE 4 does not block on print, but the answer is recorded.

## 0.7 Chapter audit spot check (PHASE 0.9, Mode P)

Run this before writing the sync report. If Part 0 changed any wording, run PHASE 0.9 Pass 1 → Pass 2 on the synced manuscript against the book ledger and `Audit_CanonicalTerms.json`, update the ledger with this chapter's entries, and add the result to the sync report (counts by severity, run ID). If nothing changed, record "spot check not needed".

A **blocking** finding is handled like an S3 item: <AUTHOR> decides, the fix goes into the eBook (and print) InDesign book, the PDF is re-exported, and Part 0 re-runs. Major and minor findings are carried into the Mode D final delta.

## 0.8 Sync report and trigger

Save `<CH_ROOT>/Manuscript/<ChapterName>_ManuscriptSync_<YYYYMMDD_HHMM>.md`:

- PDF source details and <AUTHOR>'s confirmation that it is final
- Counts by class (S1 / S2 / S3 / S4)
- Change log table: `# | Class | Location (heading › paragraph) | Manuscript (before) | eBook PDF (after) | Applied to MD | Applied to DOCX | Decision`
- S3 decisions, with any layout fixes sent back to the eBook (and print) InDesign book
- Version before → after, backup path
- Downstream impact list
- Print cross-check answer: the 0P report used (date, counts), and the print-only differences <AUTHOR> confirmed
- Audit spot check (0.7): run ID and counts by severity, or "not needed"
- `syncStatus: SYNCED | NO_DIFFERENCES | BLOCKED`

Then write the trigger (renaming any older one to `*_superseded_<timestamp>.md`):
- `Manuscript/Trigger/MANUSCRIPT_SYNCED.md` when `syncStatus` is `SYNCED` or `NO_DIFFERENCES`: no S3 item is pending, no blocking step-0.7 audit finding is open, MD and DOCX match the PDF and each other, and the version is recorded. From release v1.2.5 it also records the DOCX and MD SHA-256 hashes after the sync, the `MANUSCRIPT_LOCKED.md` it started from, and the post-lock changes <AUTHOR> accepted (count and decision file). With `NO_DIFFERENCES`, the hashes equal the lock's. Step 0 and Part C accept hashes that match either the lock or this file.
- `Manuscript/Trigger/MANUSCRIPT_SYNC_INCOMPLETE.md` otherwise, listing what is blocking.

**Re-run rule:** if <AUTHOR> re-exports the eBook PDF after further edits, at any point up to PHASE 7, Part 0 runs again for that chapter, PHASE 4 Part A is rebuilt from the updated manuscript, and the Part C re-record rule applies.

## 0R. References re-check (report-only, v3.3)

Right after `MANUSCRIPT_SYNCED.md` is written, re-run the references check (PHASE 1 Step 10b) **without fixes**.
- **Output:** `_BookGovernance/References/<ChapterName>_ReferencesCheck.md`.
- **Findings:** each critical or major finding goes to <AUTHOR>.
  - The fix is made in the eBook (and print) InDesign book, the PDF is re-exported, and Part 0 re-runs.
  - Findings don't block Part A. They are carried to PHASE 6.5 and PHASE 7.
  - Record the counts in the sync report.

## 0G. Glossary lock (v3.3)

The chapter's manuscript is now locked to its final eBook, so its glossary is finalised here, before Step 0:

1. **Back up** `Governance/<ChapterName>_GlossaryNormalized.json` to `Governance/_Backups/<YYYYMMDD_HHMM>/`.
2. **Refresh it from the synced manuscript:**
   - add terms the locked text now defines
   - update definitions whose wording changed
   - drop terms the manuscript no longer uses
   - keep the PHASE 2 fields (aliases, relatedTerms, References: Ch N)
   - add `"lockedFrom": "MANUSCRIPT_SYNCED <date>, version <chapterVersion>"`
3. **Apply the author's defining-chapter rules** in `_BookGovernance/Glossary/Glossary_Canonical.json` (`definedIn` / `primedIn` / `removeFrom`). See PHASE 2, Glossary Normalization. Never edit that file; <AUTHOR> owns it.
4. **Rebuild the book-level glossary** in `_BookGovernance/Glossary/` (reference implementation: `glossary_rollup.py` in `<LOCAL_TOOLS_ROOT>`):
   - `Master_Glossary.json` / `.md`: the **official** glossary. It holds only **locked** chapters (`MANUSCRIPT_SYNCED.md` newer than the eBook PDF), each term with its defining chapter's definition.
   - `Glossary_DriftReport.md`: an early warning across *all* chapters, covering:
     - the same term defined differently
     - name variants
     - alias collisions
     - terms to remove
     - terms not yet in the back-matter glossary, and back-matter definitions that differ
5. **Send every new conflict involving this chapter to <AUTHOR>,** with a recommendation of which chapter should define the term. These don't block Part A.
6. **Record the glossary lock in the PHASE 4 checklist:** terms added, changed, and removed, plus conflicts raised.

The back-matter glossary (e.g. `BackMatter/Glossary/GLOSSARY.docx`) is <AUTHOR>'s document. The drift report lists what it is missing or where it differs; nothing writes to it automatically.

## 0P. Print vs. eBook QA (report-only, v3.4)

**Why:** <AUTHOR> lays out the print book in its own InDesign book. Wording can drift between the print and eBook layouts, and print has layout problems the eBook doesn't. This check catches both before release. It is deterministic (no LLM), and the reference implementation is `print_check.py` in `<LOCAL_TOOLS_ROOT>`.

**Hard input: the print PDF.** When a section's print layout is finished, <AUTHOR> exports it from the print InDesign book as a high-fidelity print PDF: 7×10 in trim, with bleed on the top, bottom, and outside edge (0.125 in), no printer's marks. Upload it to:
- **Chapters:** `<CH_ROOT>/InDesign/<ChapterName>_Print7x10.pdf`
- **Front matter:** `<BOOK_ROOT>/FrontMatter/Final/<Section>/InDesign/<Section>_Print7x10.pdf`

Keep one print PDF per folder. Rename an older export to `*_superseded_<timestamp>.pdf`, which the check skips. The matching final eBook PDF must also be present: for chapters `<CH_ROOT>/eBook/<ChapterName>_eBook.pdf` (or `_eBookPDF.pdf`; 0.1), for front matter the section-local `<BOOK_ROOT>/FrontMatter/Final/<Section>/eBook/*.pdf`. Without both PDFs, 0P doesn't run. Without a print PDF, 0P is **pending**, not failed.

**What is checked:**

1. **Text drift (eBook → print):** the print text inside the trim is compared word by word with the final eBook PDF.
   - Ignored: line breaks, hyphenation, and spacing (wording falls differently on print spreads), plus running heads and folios.
   - Skipped: print-only differences <AUTHOR> has logged in `<ChapterName>_PrintOnlyDifferences.md` (next to the section's folders, e.g. `<CH_ROOT>/<ChapterName>_PrintOnlyDifferences.md`). Log each one as a quoted phrase, e.g. `"see the facing page"`.
2. **Layout (print PDF only):**
   - widows, orphans, runts (one-word last lines), and headings stranded at a page bottom
   - 3+ stacked hyphens, and doubled words
   - text inside the 0.25 in safe zone or across the trim
   - trim size (7×10 in) and bleed (at least 0.125 in at the top, bottom, and outside edge; none is needed at the spine), and no printer's marks (the page must not be larger than the bleed)
   - fonts that aren't embedded, or are Type3
   - images under 300 ppi effective, and RGB images
   - blank pages

**Report:** `<BOOK_ROOT>/_BookGovernance/PrintQA/<ChapterName>_PrintQA.md` + `.json`: counts, text similarity, the text drift table (eBook page, print page, both texts), and the layout findings by page. It is written at book level, so it covers protected chapters too.

**Severity:**

| Severity | Meaning | Examples |
|---|---|---|
| **Text: check** | A difference of 3+ words | Reworded sentence, added or dropped line |
| **Text: minor** | A difference of 1–2 words | One changed, added, or dropped word |
| **Layout: error** | A print blocker | Wrong trim size, text across the trim, font not embedded, image under 200 ppi |
| **Layout: warn** | Look at it, then fix or accept | Widow, orphan, runt, stranded heading, stacked hyphens, doubled word, safe zone, bleed under 0.125 in at the top, bottom, or outside edge, printer's marks exported, Type3 font, image at 200–299 ppi |
| **Layout: info** | Observation only | RGB image (check the printer's spec), blank page (intentional?) |

The layout checks are heuristics: they point at places to look, not at certain faults.

**What to do with findings:**
- **Text difference, print is wrong:** fix the print InDesign book and re-export the print PDF.
- **Text difference, print is right** (the wording should reach the manuscript): fix the eBook InDesign book and re-export the eBook PDF. Part 0 re-syncs the manuscript (0.5's "Accept the PDF wording" path), and 0P re-runs.
- **Text difference that belongs only in print** (e.g. a page reference): <AUTHOR> logs it in `<ChapterName>_PrintOnlyDifferences.md`, and the next run skips it.
- **Layout error or warning:** fix it in the print InDesign book and re-export, or, for a warning, <AUTHOR> accepts it in writing (in the PHASE 7 checklist, beside the item).

Nothing in 0P edits a layout or a manuscript.

**Re-run rule:** 0P re-runs automatically whenever the print PDF or the eBook PDF changes, once both have been quiet for 5 minutes. <AUTHOR> is emailed when the findings change (and if the check fails to run). Run it by hand with `print_check.py <ChapterName>` (or `--all`).

**Workbook variant:** the same check covers the print workbook, when the workbook profile ships print (PHASE 3W W2b), in either profile location:
- `book-root`: print PDFs go to `<WORKBOOK_BOOK_ROOT>/InDesign/`. `<eBook stem>_Print7x10.pdf` is checked against that section's workbook eBook PDF; any other `*Print*.pdf` there is checked against the assembled workbook eBook (the assembled export at `<WORKBOOK_BOOK_ROOT>` if present, else `_BookPublication/<BOOK>_WORKBOOK_EBOOK/<BOOK>_Workbook_eBook.pdf`).
- `chapter`: `<CH_ROOT>/Workbook/<ChapterName>_Workbook_Print*.pdf` is checked against `<CH_ROOT>/Workbook/<ChapterName>_Workbook_eBook.pdf`.

Reports: `_BookGovernance/PrintQA/Workbook_<eBook stem>_PrintQA.md` or `Workbook_PrintQA.md` (`book-root`), `<ChapterName>_Workbook_PrintQA.md` (`chapter`). The workbook eBook is 8.5×11 in and its print is 7×10 in; that is expected, not drift. Workbook findings are closed in PHASE 3W, not here.

**Gate:** 0P is non-blocking for Part 0, Step 0, and Part A. It must be **closed** before PHASE 6.5 and PHASE 7:
- the latest report is newer than both PDFs;
- it shows **0** text differences to check and **0** layout errors;
- every minor text difference and every warning is fixed, logged as print-only, or accepted by <AUTHOR>.

Record the latest 0P counts in the PHASE 4 checklist.

## Part 0 exit gate

Part 0 itself needs only the final eBook PDF and the manuscript (MD and DOCX); it writes `MANUSCRIPT_SYNCED.md` above, then runs 0R and 0G. 0P runs on its own trigger (the print PDF, paired with the chapter's eBook PDF or, for front matter, `FrontMatter/Final/<Section>/eBook/*.pdf`) and doesn't gate Step 0. Step 0 may begin only when that trigger exists and is newer than the eBook PDF (`eBook/<ChapterName>_eBook.pdf`, or `_eBookPDF.pdf`).

---

## 0C. Congruency check (Step 0C, pass 1; report-only; v1.2.6)

**When:** after Part 0 (with 0R, 0G and 0P) has finished and before Part A. It needs the sections' inputs to exist: the manuscript (DOCX and MD), the final eBook PDF, the print PDF, and the narration script.

**What it does** (deterministic, no LLM; `<LOCAL_TOOLS_ROOT>/congruency_check.py <ChapterName> --pass 1`). It reuses the Part 0 text comparison, the 0P print QA result, and the audiobook QA text rules:

| Check | Compares | Reported as |
|---|---|---|
| Manuscript DOCX ↔ MD | the canonical DOCX with its replica | differences with the text on each side, and changed numbers |
| Manuscript ↔ eBook PDF | the same wording as Part 0, normalised | differences with the page |
| eBook PDF ↔ print PDF | the latest 0P result (0P is re-run if it is older than either PDF) | differences with both page numbers, and the layout error count |
| Manuscript ↔ narration script | what the narrator is told to read | differences with the segment id; narration-only descriptions (figures, the spoken pointer in place of references) show up here and are accepted once |
| Manuscript ↔ workbook | exercise number and title in the manuscript heading, the exercise registry, the workbook DOCX/MD and the print IDML | any number or title that disagrees |
| Freshness | every file against `MANUSCRIPT_LOCKED.md` (both hashes and the revision date), or against `MANUSCRIPT_SYNCED.md` when Part 0 changed the manuscript after the lock with <AUTHOR>'s decision and nothing was edited since; a derived file older than the manuscript is listed | the stale-file list |

Folios, footnote numbers, figure labels, pull quotes that repeat body text, and text that only moved are not differences.

**Output:** `<BOOK_ROOT>/_BookGovernance/CongruencyQA/<ChapterName>_Congruency.md` and `.json`: a status row for each format, every difference with its page or segment, the stale-file list, and the verdict:
- **PASS:** no stale file, no missing input, and every difference is either gone or accepted.
- **HOLD:** anything else. The report says why.

**Deciding a HOLD.** <AUTHOR> reads the report and, for each difference, either fixes the file that is wrong (the manuscript through `MANUSCRIPT_REVISED.md`; a layout in InDesign; the script in the Audiobook folder) and re-exports, or accepts it as intended. Accepting is `congruency_check.py <ChapterName> --accept "<reason>"`, which records the currently reported differences in `CongruencyQA/<ChapterName>_Accepted.json`; it applies only to the differences shown in the report, never with `--all`. To accept only some, add `--keys K1,K2` (the Key column of the report). Read each difference first: a wording difference between formats is a real error until you have decided otherwise.

**Numbers.** Each text check also compares numbers by value ("three", "3" and "3rd" agree; "three" and "4" do not). A number that differs while the words around it match is reported as "number differs", with the words before and after. Numbers in the reference list are left to the references check, and in the narration script numbers above 100 (years, page ranges) are skipped, because they are read aloud differently. The check re-runs on its own when an input changes (HOW_TO_RUN, Step 5c).

**Gate:** Part A starts only when the latest pass 1 report for the chapter is PASS and is newer than every input. A chapter without a lock (the first book's Ch1 to Ch5) is checked and reported, and is never held by it.

**Pass 2** (after Part C, Part C step 6) is the same check plus the Kindle DOCX against the manuscript and the audiobook QA result (text match, the lines the transcript flagged, ACX failures, an MP3 older than the script). PHASE 5 and PHASE 6.5 start only on a pass 2 PASS.

---

## 0. Dependency check (right after Step 0C, before anything else in Part A)

PHASE 4 depends on finished design work, because Kindle content is built from the eBook structure and the exported figures — not from the design HTML. Confirm, and stop if any item fails:

| Dependency | Source | Produced by |
|---|---|---|
| **`MANUSCRIPT_LOCKED.md` exists, and the DOCX and MD hashes match it or the newer `MANUSCRIPT_SYNCED.md`** (release v1.2.5) | `Manuscript/Trigger/` | PHASE 2.5 / PHASE 4 Part 0 |
| **Step 0C (congruency check, pass 1) is PASS and newer than every input** (v1.2.6; not required for chapters without a lock) | `_BookGovernance/CongruencyQA/` | PHASE 4 Step 0C |
| **`MANUSCRIPT_SYNCED.md` exists and is newer than the eBook PDF** | `Manuscript/Trigger/` | PHASE 4 Part 0 |
| `DESIGN_READY.md` exists: written by PHASE 3.5 with its Kindle Readiness section checked, or attested by the final eBook upload (v3.3), in which case confirm the §13 items here | `DesignPacket/Trigger/` | PHASE 3.5 §13 / upload |
| Final manuscript text and version (synced to the eBook PDF) | `Manuscript/`, `Governance/<ChapterName>_VersionMetadata.json` | PHASE 1 / 2, updated in Part 0 |
| Final eBook HTML + metadata (structural backbone) | `eBook/` | PHASE 1, designed in PHASE 3 |
| Final FigureRegistry (numbering, captions, alt text) | `Governance/` | PHASE 2, reconciled in PHASE 3 |
| **Exported figure images, no placeholders** | `DesignPacket/figures_export/` | PHASE 3 (Claude Design + <AUTHOR>'s manual work) |
| Pull quotes, sidebar summaries | `InDesign/` | PHASE 1, final after PHASE 3 |
| eBook layout complete; final eBook PDF uploaded | `DesignPacket/`, `eBook/` | PHASE 3 (manual) |
| Print layout complete (<AUTHOR> confirms; the print InDesign book lives in separate print folders. The uploaded print PDF and its 0P report are evidence, but not required here) | <AUTHOR>'s print folders; `InDesign/<ChapterName>_Print7x10.pdf` | PHASE 3 (manual) |
| Glossary, Learning Metadata, Manifest | `Governance/` | PHASE 2 |

If a figure is still a placeholder, or the print/eBook work for the chapter is not finished, **do not build the Kindle files**. Record the blocker in the checklist with `gateStatus: FAIL` and return the chapter to PHASE 3.

## Build profile (declare before starting)

| Toggle | Default | Notes |
|---|---|---|
| `includeConceptCards` (Reference Guides) | on | |
| `includePracticeSection` (Workbook exercise) | on | Exercise text only. The workbook itself is an eBook PDF + print book with no Kindle edition (PHASE 3W). |
| `includeInstructorNotes` | **off** | Reader edition. Turn on only for a facilitator edition. |
| `includeFurtherExploration` (Marketing seeds) | **off** | Allowed only for seeds whose frontmatter shows `status: approved` and `voiceCheck: passed`. Seeds with `status: draft` are never published. |

---

## 1. Gather all final chapter assets (PHASE 1–3.5)

Pull ONLY from `<CH_ROOT>`:

- `Manuscript/` (authoritative text)
- `eBook/` (**structural backbone**: HTML blocks, EPUB formatting, TOC entries, section anchors, eBook metadata. For legacy chapters whose PHASE 1 HTML sits in `Kindle/`, use that file and note it in the checklist.)
- `ReviewPacket/` (summary, definitions, glossary terms)
- `ReferenceGuides/` (concept breakdowns)
- `Workbook/` (exercise text only, no DOCX formatting)
- `Training/` (only if `includeInstructorNotes` is on)
- `Slides/` (semantic outline, not images)
- `Audiobook/` (segment markers, used for anchor cross-check only)
- `InDesign/` (pull quotes, section headers, sidebar summaries; not the print PDF)
- `DesignPacket/` (figure files, figure prompts, layout notes, DSM-derived components)
- `Marketing/Seeds/` (only if `includeFurtherExploration` is on and the seeds are approved)
- `Governance/` (GlossaryNormalized, LearningMetadata, FigureRegistry, VersionMetadata)

These are the **final, locked** assets. Do not edit them.

## 2. Map eBook HTML to DOCX styles (global style map)

| HTML | DOCX style |
|---|---|
| `<h1>` | Heading 1 (Chapter Title) |
| `<h2>` | Heading 2 (Major Section) |
| `<h3>` | Heading 3 (Subsection) |
| `<p>` | Body |
| `<blockquote>` | Quote |
| `<figure>` / `<figcaption>` | Figure placeholder or image + Caption |
| `<aside>` | Sidebar or Callout |
| DSM callouts (`callout-info`, `tip-card`, `summary-box`, …) | Callout |

Preserve semantic hierarchy, inline emphasis, paragraph spacing, indentation, lists, and section breaks. Everything must be EPUB-safe and Kindle-friendly (no fixed widths, no floating text boxes, no tables used for layout).

## 3. Insert chapter front matter

- Chapter title and number
- Part / Lesson / Core Value
- Short chapter summary (ReviewPacket)
- Optional: 1–2 pull quotes (InDesign prep; verbatim)

## 4. Insert main manuscript body

- The manuscript text is authoritative (after Part 0, it matches the final eBook PDF); the eBook HTML supplies structure only. If they differ, the manuscript wins, and the difference is logged in the checklist for PHASE 2's owner.
- Insert figure placeholders or images wherever the FigureRegistry places a figure.
- Captions come from the Governance FigureRegistry (titles, descriptions).

## 5. Insert supporting materials (per build profile)

- **5A. Concept Cards:** Reference Guides as end-of-chapter cards.
- **5B. Practice Section:** the chapter's main workbook exercise.
- **5C. Instructor Notes:** appendix, only if toggled on.
- **5D. Further Exploration:** 1–2 pull-lines, 1 framework card, and a shortened newsletter excerpt, only if toggled on and approved.

## 6. Insert figures and images

Figures come from `DesignPacket/figures_export/` (PHASE 3), never from the `.dc.html` design files:

1. For each FigureRegistry entry, take `<ChapterName>_Fig<#>_<Name>.png`.
2. Convert to a Kindle-safe copy in `<CH_ROOT>/Kindle/figures/`: JPEG (or PNG where transparency matters), long edge 1600–2560 px, sRGB, under ~5 MB, no text smaller than roughly 9 pt at final size.
3. Insert it at the figure anchor from the eBook HTML, with the caption and alt text from the FigureRegistry.
4. Keep figure numbering identical to the FigureRegistry and the print edition.

A placeholder may be inserted **only** with <AUTHOR>'s explicit approval for that figure; record the approval in the checklist. Otherwise a missing figure is a `gateStatus: FAIL` (see Step 0).

## 7. Apply global DOCX styles

Title · Heading 1 · Heading 2 · Heading 3 · Body · Quote · Caption · Callout · Sidebar. Styles must be Kindle-friendly.

## 8. Generate the Kindle HTML and metadata files

- `<ChapterName>_Kindle.html`: clean Kindle-safe HTML of the compiled chapter (same content and order as the DOCX)
- `<ChapterName>_KindleMetadata.json`: chapterNumber, chapterTitle, part, lesson, coreValue, TOC entries, section anchors, figure anchors, alt text, language, version (from VersionMetadata), buildProfile

## 9. Save outputs

Save all three deliverables to `<CH_ROOT>/Kindle/`. If a file of the same name exists, back it up to `<CH_ROOT>/Governance/_Backups/<YYYYMMDD_HHMM>/Kindle/` first, and increment the version in `Governance/<ChapterName>_ArtifactManifest.json`.

## 10. Produce PHASE 4 checklist

Save as `<CH_ROOT>/<ChapterName>_PHASE4_KindleChecklist.md`. Include:

- Part 0 manuscript sync: eBook PDF used, `syncStatus`, change counts, version before → after, link to the sync report (a missing PDF is recorded here as the blocker, with `gateStatus: FAIL`)
- PHASE 3.5 completion: `DESIGN_READY.md` from PHASE 3.5, or attested by the upload (v3.3)
- 0R references re-check: counts by severity, open critical/major findings (non-blocking)
- 0G glossary lock: terms added / changed / removed; conflicts raised for <AUTHOR> (non-blocking)
- 0P print QA: print PDF used, report date, counts (text check / minor, layout error / warn), or "pending (no print PDF)" (non-blocking here; must be closed before PHASE 6.5)
- All assets gathered (list any legacy-path substitutions)
- Build profile used
- All sections included
- Step 0 dependency check result (list anything missing)
- Figures inserted, with the source image for each (list any approved placeholder)
- Styles applied
- TOC generated
- Metadata added
- Deliverables saved (DOCX, HTML, metadata, `Kindle/figures/`) and manifest updated
- Any missing elements
- Recommendations for PHASE 5 (RAG rebuild)
- Part 0 step 0.7 audit spot check result
- Part C: `audiobookStatus: RECORDED | DRAFT_ONLY | PENDING | N/A`, narration-script date (from the Kindle build), final recording file and date, coverage result, measured technical-spec values, pronunciation review by <AUTHOR>, passages to re-record (if any)
- `gateStatus: PASS | FAIL`

---

# PART C — AUDIOBOOK (per chapter, after Part A)

**The chain:** the final eBook PDF is the trigger, the Kindle build is made from it, and the audiobook is recorded from the Kindle output. Part C therefore waits for Part A `PASS`, which in turn waits for `MANUSCRIPT_SYNCED.md` and the step 0.7 spot check.

**Recorded only after the lock (release v1.2.5).** Part C needs a current `Manuscript/Trigger/MANUSCRIPT_LOCKED.md`, with the manuscript hashes matching it or the newer `MANUSCRIPT_SYNCED.md`. The content audit now runs before design (PHASE 2.5), and B0 no longer audits content, so a recording made from the locked text should never need re-recording. Re-recording (step 5) is left for an approved post-lock revision or an accepted Part 0 change.

**XTTS is a draft only:** a pacing and timing guide. The published audiobook is <AUTHOR>'s own narration, recorded and edited manually in Adobe Audition.

1. **Build the narration script from the Kindle output.** Update `Audiobook/<ChapterName>_NarrationScript.md` (first created in PHASE 1 Step 9) from `Kindle/<ChapterName>_Kindle.docx`: same reading order, headings, and text as the Kindle build. Keep the pronunciation guide and segment markers, and move any marker whose text moved. Narration-only adaptations are marked notes, never silent text changes: figure and table references, URLs, and visual-only callouts get a spoken alternative or a skip note. This clears the "narration" items in the Part 0 downstream impact list.
2. **XTTS draft (optional).** Render the script with local XTTS to `Audiobook/Drafts/<NN>_<ChapterName>_XTTS_Draft.mp3` as a timing and pacing reference. Drafts are never published and never go into the book set.
3. **<AUTHOR> records the final narration** in Adobe Audition from the narration script (a manual track; the Audition session may live outside `<BOOK_ROOT>`, like the print InDesign book) and exports the chapter master to `Audiobook/<NN>_<ChapterName>.mp3`.
4. **Check the final recording** and record the result in the PHASE 4 checklist:
   - It is <AUTHOR>'s recording (not a file from `Drafts/`) and newer than the chapter's Kindle build.
   - **Coverage:** every narration segment is present and in order. Optionally, transcribe the MP3 and diff it against the script to list skipped or changed lines. List them; never judge delivery or voice.
   - **Technical spec** from the distributor. ACX, for example, asks for RMS between −23 and −18 dB, peaks no higher than −3 dB, a noise floor below −60 dB, 44.1 kHz constant-bit-rate MP3 at 192 kbps or higher, and room tone at the head and tail. Check the distributor's current requirements, and record the measured values.
   - Framework terms are pronounced as the pronunciation guide says (<AUTHOR> confirms).
   - `audiobookStatus: RECORDED | DRAFT_ONLY | PENDING | N/A`
5. **Re-record rule:** if Part 0 re-runs and changes narrated text, Part A rebuilds the Kindle output and step 1 refreshes the script. List the changed passages (from the sync change log) with their segment markers, so <AUTHOR> can re-record only those passages. For those passages, a recording older than the chapter's Kindle build is stale.

6. **Congruency check, pass 2 (v1.2.6).** After the recording passes its checks, run `congruency_check.py <ChapterName> --pass 2`. It repeats the pass 1 checks and adds the Kindle DOCX against the manuscript and the audiobook QA result. PHASE 5 and PHASE 6.5 start only on PASS. Record the verdict in the checklist.

Front matter, Part openers, and back matter sections that are narrated follow the same steps in their `Audiobook/` folders.

## Front matter, Parts, and back matter

Sections outside `/Chapters/` follow the same process with fewer inputs (manuscript + eBook only), writing to their existing folders:
- `/FrontMatter/Final/<Section>/Kindle/<Section>_Kindle.docx`
- `/Parts/<NNN>_<PartName>/Kindle/<PartName>_Kindle.docx`
- `/BackMatter/<Section>/Kindle/<Section>_Kindle.docx`

They must exist before Part B, since the book Kindle file needs front matter, Part openers, and back matter in reading order.

## PHASE 4 Part A exit gate

PHASE 5 may start for the chapter when `Manuscript/Trigger/MANUSCRIPT_SYNCED.md` exists, the pass 2 congruency report is PASS (v1.2.6; not required without a lock), the PHASE 4 checklist shows `gateStatus: PASS`, and the chapter's Kindle deliverables exist.

---

# PART B — BOOK-LEVEL ASSEMBLY (<BOOK>_KINDLE_EBOOK + <BOOK>_AUDIOBOOK)

Run once, when every chapter, front matter section, Part opener, and back matter section has a PHASE 4 Part A `PASS`. Output folder: `<BOOK_ROOT>/_BookPublication/<BOOK>_KINDLE_EBOOK/`.

## B0. Cross-chapter consistency and since-lock delta check (PHASE 0.9, Mode D; reduced in release v1.2.5)

**What B0 is now.** Each chapter's full content audit ran before design, in PHASE 2.5, and <AUTHOR> decided every finding. B0 doesn't repeat it. It checks two things only:

1. **Cross-chapter consistency.** Once every chapter has `MANUSCRIPT_LOCKED.md` and `MANUSCRIPT_SYNCED.md`, run PHASE 0.9's Consolidation over the whole book, using the latest ledger (the newest lock-audit run folder) and `Audit_CanonicalTerms.json`. It looks only for conflicts **between** chapters that were locked at different times: a definition, term form, list, threshold, equation, or figure number that two chapters now state differently, and cross-references between chapters that no longer resolve. Findings `Defer`red in a lock audit are closed here.
2. **What changed since each chapter's lock.** Compare each chapter's current DOCX and MD with its lock snapshot (`Manuscript/_Locked/`, hashes in `MANUSCRIPT_LOCKED.md`). For a chapter with no change, record "unchanged since lock". For a chapter that changed (an accepted Part 0 change, or an approved `MANUSCRIPT_REVISED.md` revision with its delta lock), run Pass 1 → Pass 2 on the changed paragraphs only, and confirm each change has its approval (the `P4_DECISIONS` row or the revision's approval line). An unapproved change is a blocking finding.

**B0 doesn't reopen the manuscript.** It is not a content audit, so a single-chapter finding (a style point, a minor term variant inside one chapter) is recorded, not fixed. A manuscript change is allowed only for a **genuine cross-chapter conflict**, and only with <AUTHOR>'s approval: <AUTHOR> chooses the version, the chapter that changes gets a `MANUSCRIPT_REVISED.md` section with the approval line, PHASE 2.5 re-locks it (delta audit), and the change goes through the eBook (re-export → Part 0 → Part A → PHASE 5 for that chapter). Then re-run B0. Never patch a synced manuscript by hand.

- Continue to B1 only when `_BookGovernance/Audit/Trigger/AUDIT_FINAL_CLEAR.md` exists and is newer than every chapter's `MANUSCRIPT_SYNCED.md`. It records the run ID, the chapters checked for consistency, and, per chapter, "unchanged since lock" or the approved changes checked.

## B1. Confirm the assembly inputs

- [ ] Every chapter has `Manuscript/Trigger/MANUSCRIPT_SYNCED.md`, still newer than its eBook PDF (re-run Part 0 and Part A for any chapter whose PDF was re-exported)
- [ ] Every chapter has `Kindle/<ChapterName>_Kindle.docx`, `_Kindle.html`, `_KindleMetadata.json`, and `Kindle/figures/`
- [ ] FrontMatter, Parts, and BackMatter Kindle DOCX files exist
- [ ] Reading order confirmed against the book TOC (front matter → Part I → its chapters → Part II → … → back matter)
- [ ] Every chapter is at the same edition version (VersionMetadata)
- [ ] `AUDIT_FINAL_CLEAR.md` exists and is newer than every chapter's `MANUSCRIPT_SYNCED.md` (B0)
- [ ] Every chapter has `MANUSCRIPT_LOCKED.md`, and every change since its lock is approved (B0, v1.2.5)

## B2. Build the manuscript

1. Concatenate in reading order into `<BOOK>_Kindle.docx`, keeping one consistent style set (Title, Heading 1–3, Body, Quote, Caption, Callout, Sidebar).
2. Rebuild a single book-level TOC from the chapter TOC entries; heading levels drive the Kindle navigation.
3. Renumber nothing: chapter and figure numbers stay as governed. Flag any collision instead of fixing it silently.
4. Resolve cross-chapter links to the book-level anchors.

## B3. Build the book metadata

`<BOOK>_KindleMetadata.json`: title, subtitle, author (<AUTHOR>), publisher, language, edition, version, ISBN (if assigned), categories, keywords, description, cover file, reading order, and the full anchor map.

## B4. Produce the upload package

- `<BOOK>_Kindle.docx` — the KDP upload source
- `<BOOK>_Kindle.epub` — reflowable EPUB converted from the same DOCX, for validation and as an alternate upload
- `<BOOK>_Kindle.azw3` — Kindle Previewer proof copy
- `<BOOK>_KindleMetadata.json`
- `cover/<BOOK>_Kindle_Cover.jpg` (1600 × 2560 recommended)
- `<BOOK>_Kindle_AssemblyReport.md` — source files used, per-chapter versions, TOC depth, figure count, warnings

## B4b. Audiobook set (<BOOK>_AUDIOBOOK)

Once every narrated section has `audiobookStatus: RECORDED` with no stale passages (no final recording older than its Kindle build for changed text), assemble `_BookPublication/<BOOK>_AUDIOBOOK/` from the **final recordings only** (never `Drafts/`): the ordered MP3 set (running order matches the book TOC and the Kindle reading order) and `<BOOK>_Audiobook_TrackList.md` (track number, section, file, duration). This set was assembled in PHASE 3 before v1.0.2.

## B5. Workbook (not built here)

There is no Kindle workbook. Once B0 writes `AUDIT_FINAL_CLEAR.md`, the workbook's book-level eBook and print deliverables are assembled in PHASE 3W (W4–W5).

## B6. Hand off

PHASE 6.5 validates this package (EPUB, Kindle, metadata, figures, accessibility). Nothing is uploaded to KDP until <AUTHOR> signs off in PHASE 7.

## PHASE 4 Part B exit gate

- [ ] `<BOOK>_Kindle.docx`, `.epub`, `.azw3`, metadata, cover, and assembly report exist
- [ ] Kindle Previewer opens the proof with a working TOC and correct reflow
- [ ] Assembly report lists no unresolved warnings
- [ ] Assembly report records the final audit run ID
- [ ] `<BOOK>_AUDIOBOOK` set and track list exist, built only from <AUTHOR>'s final recordings, with no stale passages
