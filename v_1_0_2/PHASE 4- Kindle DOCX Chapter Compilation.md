# PHASE 4: Kindle DOCX Chapter Compilation (v3)

> **Pipeline position:** PHASE 4 of 7 (Kindle) · **Upstream gate:** `DesignPacket/Trigger/DESIGN_READY.md` exists (PHASE 3.5 certified Production Ready) **and** the final eBook PDF is uploaded (Part 0) · **Downstream:** PHASE 5 RAG Rebuild
> **Canonical paths, status ladder, triggers, and deliverables:** see `MASTER_PIPELINE_OVERVIEW.md`.

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

### Part A — per chapter (run chapter by chapter)

| Deliverable | Path |
|---|---|
| Kindle DOCX per chapter | `<CH_ROOT>/Kindle/<ChapterName>_Kindle.docx` |
| Kindle-ready HTML blocks | `<CH_ROOT>/Kindle/<ChapterName>_Kindle.html` |
| Kindle-ready metadata | `<CH_ROOT>/Kindle/<ChapterName>_KindleMetadata.json` |
| Kindle figure images (Kindle-sized copies) | `<CH_ROOT>/Kindle/figures/<ChapterName>_Fig<#>_<Name>.jpg` |
| PHASE 4 checklist | `<CH_ROOT>/<ChapterName>_PHASE4_KindleChecklist.md` |

### Part B — book level (once every chapter has passed Part A)

| Deliverable | Path |
|---|---|
| **<BOOK>_KINDLE_EBOOK** | `<BOOK_ROOT>/_BookPublication/<BOOK>_KINDLE_EBOOK/` |

---

# PART 0 — MANUSCRIPT SYNC FROM THE FINAL eBook PDF (run first)

**Why:** <AUTHOR> refines wording while laying out the eBook and the print InDesign books. Those edits land in the layouts, not in the manuscript. Everything from here on (Kindle, RAG, automation, marketing grounding) reads the manuscript, so it has to say what the published eBook says before any of it runs.

**Reference text:** the final eBook PDF. It is the one layout that lives inside the chapter folder. The print InDesign book is kept in <AUTHOR>'s separate print folders (INDB and template dependencies), outside `<BOOK_ROOT>`. PHASE 4 does not read those folders, and does not require print files in `InDesign/`.

**This is the one sanctioned manuscript edit after PHASE 2.** It records <AUTHOR>'s own layout-stage wording back into the manuscript. It never introduces new wording, and it follows the same paper trail as a governance fix: back up, log, version, and escalate anything uncertain.

## 0.1 Hard stop: the eBook PDF must be uploaded

Look for `<CH_ROOT>/eBook/<ChapterName>_eBook.pdf`, the final PDF exported from <AUTHOR>'s eBook InDesign book. (If the eBook is exported as one book-level PDF, save this chapter's pages under that name.)

If the file is **missing**, empty, cannot be opened, or has no extractable text (image-only export):

1. Do **not** continue Part 0, Step 0, Part A, or Part B for this chapter.
2. Write `Manuscript/Trigger/MANUSCRIPT_SYNC_INCOMPLETE.md` stating `Blocked: final eBook PDF not uploaded` (or the specific problem) and the exact path expected.
3. Write the PHASE 4 checklist with `gateStatus: FAIL` and the same blocker.
4. Tell <AUTHOR> the path to upload to, and stop.

PHASE 5, 6, 6.5, and 7 cannot start for a chapter without a PHASE 4 `PASS`, so a missing PDF halts the chapter from PHASE 4 onward. Part B cannot start while any chapter is blocked here.

Also stop, and ask, if:
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

If more than roughly 5% of paragraphs differ, or alignment fails for a whole section, stop and ask <AUTHOR> before applying anything. That usually means the wrong PDF, the wrong manuscript version, or a failed extraction.

## 0.4 Apply S1 and S2 changes

1. Back up both files to `<CH_ROOT>/Governance/_Backups/<YYYYMMDD_HHMM>/Manuscript/` before the first edit.
2. **Markdown:** edit the affected text in place. Keep headings, anchors, figure references, and front-matter fields intact.
3. **DOCX:** edit the same text in place, keeping the existing paragraph and character styles, comments, and section breaks. Change only the runs that differ. Do not regenerate the DOCX from the Markdown.
4. Re-run the comparison. The only remaining differences must be S3 items (pending) and S4 noise. The MD and the DOCX must also match each other.

## 0.5 Resolve S3 items with <AUTHOR>

Present the S3 list (location, manuscript text, PDF text, why it is flagged, recommendation). For each one <AUTHOR> chooses:
- **Accept the PDF wording** → apply it to MD and DOCX (and the Glossary or FigureRegistry, if affected).
- **Keep the manuscript wording** → the eBook layout is wrong; list it as a layout fix for the eBook InDesign book (and the print book, if it carries the same text). The PDF must be re-exported and Part 0 re-run for the chapter before the gate passes.
- **Defer** → allowed only for non-substantive items, recorded with <AUTHOR>'s initials. A deferred item blocks nothing, but it is carried into the PHASE 7 release checklist.

## 0.6 Version and impact

- Increment `chapterVersion` in `Governance/<ChapterName>_VersionMetadata.json` (patch level: e.g. `1.0` → `1.0.1`), set `revisionDate`, and add a `majorChanges` entry: `"Manuscript synced to final eBook PDF: <n> wording changes, <n> structural"`. If nothing changed, leave the version alone and record `no differences`.
- Update the manuscript entries in `Governance/<ChapterName>_ArtifactManifest.json`.
- **Downstream impact list.** Search the chapter's derived artifacts for the old wording of every applied change and list each hit in the sync report: ReviewPacket, ReferenceGuides, Workbook, Training, Slides, InDesign prep (pull quotes, sidebars), Audiobook narration script and rendered MP3, eBook HTML blocks, Marketing Intake (claims registry, terminology lock, voice samples), and the PHASE 1 RAG packet. Do **not** edit them here. PHASE 4 Part A reads the updated manuscript, and PHASE 5 rebuilds RAG from it; the others go to <AUTHOR> as proposed follow-ups. Mark verbatim quotations (pull quotes, voice samples, claims) and narration as **must fix before release**; they are checked again in PHASE 6.5 and PHASE 7.
- **Print cross-check (<AUTHOR>).** The print book is outside this pipeline's folders, so <AUTHOR> confirms one of: the print InDesign book carries the same wording changes, or the print-only differences are listed in the sync report. PHASE 4 does not block on print, but the answer is recorded.

## 0.7 Sync report and trigger

Save `<CH_ROOT>/Manuscript/<ChapterName>_ManuscriptSync_<YYYYMMDD_HHMM>.md`:

- PDF source details and <AUTHOR>'s confirmation that it is final
- Counts by class (S1 / S2 / S3 / S4)
- Change log table: `# | Class | Location (heading › paragraph) | Manuscript (before) | eBook PDF (after) | Applied to MD | Applied to DOCX | Decision`
- S3 decisions, with any layout fixes sent back to the eBook (and print) InDesign book
- Version before → after, backup path
- Downstream impact list
- Print cross-check answer
- `syncStatus: SYNCED | NO_DIFFERENCES | BLOCKED`

Then write the trigger (renaming any older one to `*_superseded_<timestamp>.md`):
- `Manuscript/Trigger/MANUSCRIPT_SYNCED.md` when `syncStatus` is `SYNCED` or `NO_DIFFERENCES`: no S3 item is pending, MD and DOCX match the PDF and each other, and the version is recorded.
- `Manuscript/Trigger/MANUSCRIPT_SYNC_INCOMPLETE.md` otherwise, listing what is blocking.

**Re-run rule:** if <AUTHOR> re-exports the eBook PDF after further edits, at any point up to PHASE 7, Part 0 runs again for that chapter, and PHASE 4 Part A is rebuilt from the updated manuscript.

## Part 0 exit gate

Step 0 may begin only when `Manuscript/Trigger/MANUSCRIPT_SYNCED.md` exists and is newer than `eBook/<ChapterName>_eBook.pdf`.

---

## 0. Dependency check (do this before anything else)

PHASE 4 depends on finished design work, because Kindle content is built from the eBook structure and the exported figures — not from the design HTML. Confirm, and stop if any item fails:

| Dependency | Source | Produced by |
|---|---|---|
| **`MANUSCRIPT_SYNCED.md` exists and is newer than the eBook PDF** | `Manuscript/Trigger/` | PHASE 4 Part 0 |
| `DESIGN_READY.md` exists, with the Kindle Readiness section checked | `DesignPacket/Trigger/` | PHASE 3.5 §13 |
| Final manuscript text and version (synced to the eBook PDF) | `Manuscript/`, `Governance/<ChapterName>_VersionMetadata.json` | PHASE 1 / 2, updated in Part 0 |
| Final eBook HTML + metadata (structural backbone) | `eBook/` | PHASE 1, designed in PHASE 3 |
| Final FigureRegistry (numbering, captions, alt text) | `Governance/` | PHASE 2, reconciled in PHASE 3 |
| **Exported figure images, no placeholders** | `DesignPacket/figures_export/` | PHASE 3 (Claude Design + <AUTHOR>'s manual work) |
| Pull quotes, sidebar summaries | `InDesign/` | PHASE 1, final after PHASE 3 |
| eBook layout complete; final eBook PDF uploaded | `DesignPacket/`, `eBook/` | PHASE 3 (manual) |
| Print layout complete (<AUTHOR> confirms; the print InDesign book lives in separate print folders, not `InDesign/`) | <AUTHOR>'s print folders | PHASE 3 (manual) |
| Glossary, Learning Metadata, Manifest | `Governance/` | PHASE 2 |

If a figure is still a placeholder, or the print/eBook work for the chapter is not finished, **do not build the Kindle files**. Record the blocker in the checklist with `gateStatus: FAIL` and return the chapter to PHASE 3.

## Build profile (declare before starting)

| Toggle | Default | Notes |
|---|---|---|
| `includeConceptCards` (Reference Guides) | on | |
| `includePracticeSection` (Workbook exercise) | on | Exercise text only. The full workbook is a separate deliverable. |
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
- `InDesign/` (pull quotes, section headers, sidebar summaries)
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
- `gateStatus: PASS | FAIL`

---

## Front matter, Parts, and back matter

Sections outside `/Chapters/` follow the same process with fewer inputs (manuscript + eBook only), writing to their existing folders:
- `/FrontMatter/Final/<Section>/Kindle/<Section>_Kindle.docx`
- `/Parts/<NNN>_<PartName>/Kindle/<PartName>_Kindle.docx`
- `/BackMatter/<Section>/Kindle/<Section>_Kindle.docx`

They must exist before Part B, since the book Kindle file needs front matter, Part openers, and back matter in reading order.

## PHASE 4 Part A exit gate

PHASE 5 may start for the chapter when `Manuscript/Trigger/MANUSCRIPT_SYNCED.md` exists, the PHASE 4 checklist shows `gateStatus: PASS`, and the chapter's Kindle deliverables exist.

---

# PART B — BOOK-LEVEL KINDLE ASSEMBLY (<BOOK>_KINDLE_EBOOK)

Run once, when every chapter, front matter section, Part opener, and back matter section has a PHASE 4 Part A `PASS`. Output folder: `<BOOK_ROOT>/_BookPublication/<BOOK>_KINDLE_EBOOK/`.

## B1. Confirm the assembly inputs

- [ ] Every chapter has `Manuscript/Trigger/MANUSCRIPT_SYNCED.md`, still newer than its eBook PDF (re-run Part 0 and Part A for any chapter whose PDF was re-exported)
- [ ] Every chapter has `Kindle/<ChapterName>_Kindle.docx`, `_Kindle.html`, `_KindleMetadata.json`, and `Kindle/figures/`
- [ ] FrontMatter, Parts, and BackMatter Kindle DOCX files exist
- [ ] Reading order confirmed against the book TOC (front matter → Part I → its chapters → Part II → … → back matter)
- [ ] Every chapter is at the same edition version (VersionMetadata)

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

## B5. Workbook Kindle edition (optional)

If a Kindle workbook is in scope, repeat B1–B4 using the chapters' workbook content into `_BookPublication/<BOOK>_WORKBOOK_EBOOK/<BOOK>_Workbook_Kindle.docx`. Otherwise record "not in scope" in the assembly report.

## B6. Hand off

PHASE 6.5 validates this package (EPUB, Kindle, metadata, figures, accessibility). Nothing is uploaded to KDP until <AUTHOR> signs off in PHASE 7.

## PHASE 4 Part B exit gate

- [ ] `<BOOK>_Kindle.docx`, `.epub`, `.azw3`, metadata, cover, and assembly report exist
- [ ] Kindle Previewer opens the proof with a working TOC and correct reflow
- [ ] Assembly report lists no unresolved warnings
