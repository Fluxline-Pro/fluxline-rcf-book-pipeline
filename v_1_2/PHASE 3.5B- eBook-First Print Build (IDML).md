# PHASE 3.5B: eBook-First Print Build (IDML) (v1.0)

> **Pipeline position:** per chapter, after PHASE 3 has produced the chapter's eBook page and before <AUTHOR>'s print finish in InDesign · **Upstream gate:** §1 below · **Downstream:** <AUTHOR>'s print finish in InDesign → the print PDF → PHASE 4 Part 0P print QA; workbook → PHASE 3W W2 / W2b
> **Canonical paths, status ladder, triggers, and deliverables:** see `MASTER_PIPELINE_OVERVIEW.md`. If this file and the Overview disagree, the Overview wins and the discrepancy is logged.

**New in release v1.2 (2026-10-22).** PHASE 3.5A (v1.1.3) gave the print track a styled text import, but layout, figures, and callouts were still placed by hand. PHASE 3.5B builds the print documents themselves:
- the **chapter's print IDML** (7×10, the book);
- the **exercise's print IDML** (7×10, the workbook).

Both are built from the finished **eBook** pages, so print copies the eBook's design: the same blocks in the same order, the same callouts and pull quotes, the same figures and captions. The print styling comes from the print templates and <AUTHOR>'s own finished print documents. <AUTHOR> opens the IDML in InDesign, checks fonts and layout, and exports the print PDF.

**Order: the eBook comes first, then print.** The eBook is built and reviewed first (§3). The print IDMLs then replicate it (§4, §5), for this chapter and every chapter after it.

**Relationship to 3.5A.** 3.5B is the default print build from v1.2. PHASE 3.5A still works and stays available:
- for a chapter whose eBook isn't built yet;
- when <AUTHOR> wants a plain styled import to lay out from scratch.

Neither phase blocks the other.

**Reference implementations** (in `<LOCAL_TOOLS_ROOT>`; deterministic; no LLM):

| Tool | Does |
|---|---|
| `ebook_paginate.py` | Fits the eBook's content blocks into fixed 8.5×11 `<doc-page>` pages, measured in headless Edge |
| `ebook_print.py` | Prints an eBook page file to PDF once fonts, images, and pages are ready, and checks the fonts |
| `idml_chapter_build.py` | Builds the chapter's print IDML from the eBook page file |
| `idml_workbook_build.py` | Builds the exercise's print IDML by cloning the previous exercise's IDML |

The IDML tools need the Python standard library, plus Pillow and the fonts' TTF files for text measurement. The eBook tools also need `websocket-client` and Edge or Chrome.

---

## 1. Entry gate

All of these must hold. If any fails, write nothing and tell <AUTHOR> which one.

1. **The manuscript is final.** The chapter DOCX is in `<CH_ROOT>/Manuscript/` and the MD isn't newer than it (as in 3.5A §1). For the workbook, the exercise DOCX is in `<CH_ROOT>/Workbook/`, and `WORKBOOK_MANUSCRIPT_READY.md` exists.
2. **The figures are finished:**
   - the RGB masters (PNG or JPG) are in `Figures/RGB/`, for the eBook only;
   - the CMYK TIFFs are in `Figures/CMYK/`, for print only.
3. **The print sources exist** in `<PRINT_DSM_ROOT>` (book) and the workbook's own `_PrintDSM/`:
   - the template IDML;
   - <AUTHOR>'s most recent finished chapter IDML, or exercise IDML, which the build starts from (§4, §5).
4. **The eBook page is built and reviewed** (§3) before the print build starts.

## 2. Design rules (<AUTHOR>, 2026-10-22)

These rules apply to every print build from this release on.

**Sources: print uses `_PrintDSM`, the eBook uses `_eBookDSM`:**
- Print styling, masters, swatches, callouts, tables, and ruled lines come only from `<PRINT_DSM_ROOT>` (and the workbook's `_PrintDSM/`).
- `<EBOOK_DSM_ROOT>` is read for content and structure only: which blocks, in which order, with which callouts. Its colors, components, and CSS are never copied into print.

**Image formats:**
- Print uses only the CMYK TIFFs from `Figures/CMYK/`.
- The eBook uses only the RGB PNG or JPG files from `Figures/RGB/`.
- A format is never substituted for the other, in either direction.

**One column only.** The templates contain 1-column and 2-column designs. Use only the 1-column masters and frames, in both the book and the workbook. Never create 2-column spreads.

**Print replicates the eBook:**
- It matches the eBook's overall design, without its heavy use of color. Black, white, and gold are preferred.
- Callouts are kept as they are in the eBook, including their content and spacing.

**Motifs and color:**
- Leave out the eBook's motifs, diamonds, ornaments, and extra colors.
- **Quote callouts** (pull quotes) are the exception: they are kept, in the print template's pull-quote style.
- **Multi-color callouts** are also kept, using the **print template's** versions (for example Green Insight, Blue Coherence, Violet Expansion). The eBook versions are never used.

**Margins and spacing:**
- Use the page from margin to margin. Text frames span the full live area, and nothing is narrowed or inset without a reason.
- Spacing above and below headings, callouts, figures, and captions is the same everywhere. It comes from the paragraph styles, not from manual nudges.

**Figures and captions:**
- Figures are anchored in the text, full column width, and link the CMYK TIFF. Each caption uses the template's caption styles.
- A figure is resized to fit the column when necessary.
- Compute each figure's **effective ppi** at its placed size. Below 300 ppi, flag it as too small for print. A figure taller than the live area also gets a flag. Never upscale silently.

**Workbook pieces:**
- Tables, ruled lines (writing lines), and the circular badges and markers may be copied as they are from the workbook template or the previous exercise's IDML.
- Callouts and their content may also be copied and re-worded.
- These copying rules apply **only to the workbook**. The book builds its callouts from the print styles.

**Never write to `_PrintDSM`.** The templates and <AUTHOR>'s finished documents there are read-only. The builders open them as zips and write somewhere else (§7).

## 3. eBook first (8.5×11, Claude Design)

**Goal:** the chapter's eBook page file, `<EBOOK_DSM_ROOT>/Chapter<N>_eBook.dc.html` (one `<doc-page>` per page), and the exercise's page file in the workbook's `_eBookDSM/`. Both follow the eBook DSM and use the RGB figures.

1. **Content.** Start from the manuscript DOCX. If PHASE 3 produced a Claude Design draft, start from it, but update its wording from the DOCX. Keep the callouts and pull quotes <AUTHOR> approved (PHASE 1 recommendations, validated in PHASE 2).
   - Check every pull quote word for word against the DOCX.
   - Back up the draft to `<EBOOK_DSM_ROOT>/_Backups/` before replacing it.
2. **Paginate** with `ebook_paginate.py`. The rules:
   - pages fill from top to bottom, using the page end to end;
   - a block never splits;
   - a heading never ends a page;
   - footnotes stay on the page of the block they belong to.

   Then check the paginated file in a real render and fix the first overflow on each pass, until no page overflows.
3. **Book-level pages.** Update the eBook's contents page and the page numbers of the pages that follow:
   - the book's `startPage` values;
   - for the workbook, `WB - Contents` and the master workbook file's imports, with the later pages renumbered.

   A contents page that is nearly full gets a flag before the next chapter is added.
4. **Review copy.**
   - Print a PDF with `ebook_print.py`. Its check confirms the brand fonts are embedded.
   - With <AUTHOR>'s permission, publish the page as a **private** artifact for review.
   - Compare the eBook's words with the DOCX: the only differences allowed are design elements (running heads, callout eyebrows, captions).

## 4. Book: chapter print IDML (`idml_chapter_build.py`)

**Base:** <AUTHOR>'s most recent **finished** chapter IDML in `<PRINT_DSM_ROOT>` (for example `004_Chapter2_<Title>.idml` for Chapter 3). The build keeps its:
- masters, styles, swatches, and fonts;
- preferences and the chapter-opener page.

So the result opens exactly like the chapters already laid out. Use the template IDML only when no chapter has been finished yet.

**What it writes:**
- **Opener page:** the chapter number word, title, and epigraph.
- **Body:** **one main story** threaded through full-page, 1-column body frames. Everything is in the text flow:
  - **Paragraphs, headings, lists, and pull quotes** get the paragraph styles <AUTHOR>'s finished chapter uses.
  - **Callouts** become inline paragraphs in the print template's Callout styles. The eyebrow line and the circular badge are an anchored group.
  - **Figures** are anchored frames (above the line, full column width) linking the CMYK TIFF, with the caption in the caption style. Alt text comes from the eBook.
  - **Footnotes and references** use the footnote and reference styles: the red footnote marker, the hanging-indent reference list, and the footnote paragraph.
- **Running heads:** set through the document's text variables (chapter number and title).
- **Smart Text Reflow:** adds pages at the end of the story and deletes empty pages, so the page count follows <AUTHOR>'s edits.

```
python <LOCAL_TOOLS_ROOT>/idml_chapter_build.py ^
  --base "<PRINT_DSM_ROOT>/<NNN>_Chapter<N-1>_<Title>.idml" ^
  --ebook "<EBOOK_DSM_ROOT>/Chapter<N>_eBook.dc.html" ^
  --out "<CH_ROOT>/InDesign/<NNN>_Chapter<N>_<Title>.idml" ^
  --chapter-number <N> --chapter-word <WORD> --title "<Chapter Title>" ^
  --epigraph "<epigraph>" [--attribution "<name>"] ^
  --figures-dir "<CH_ROOT>/Figures/CMYK" --body-pages <estimate> --first-page-number <first body page>
```

It prints a JSON report covering:
- pages;
- paragraphs by style;
- figures, with their effective ppi;
- callouts;
- warnings.

## 5. Workbook: exercise print IDML (`idml_workbook_build.py`)

**Base:** <AUTHOR>'s previous finished **exercise** IDML in the workbook's `_PrintDSM/` (for example `02-2_Exercise_1_2_<Name>.idml` for Exercise 1.3). The build clones its page designs piece by piece:
- the opener and the PART tab;
- the title and running header;
- field labels, body text, and prompts with ruled lines;
- step heads and step chips;
- the safety callout and gray example panels;
- the how-to box and the self-reflection box;
- log grids and field cards;
- the Codex and closing pages.

Each piece is positioned to mirror the exercise's eBook pages.

**Wording:**
- The wording comes from the exercise's workbook DOCX (canonical), word for word.
- Text heights are measured with the real fonts, so ruled lines and cards never overrun a page.
- The opener's frames keep their ids, so the master's text stays overridden.

**Per-exercise page plan.** The page plan (which pieces go on which page) is specific to each exercise:
- it lives in the builder;
- it is updated from the previous exercise's plan each time, matching the new exercise's eBook pages.

The component layer (cloning, measurement, callouts, cards, grids) is shared.

```
python <LOCAL_TOOLS_ROOT>/idml_workbook_build.py ^
  --base "<workbook _PrintDSM>/<NN>-<n>_Exercise_<L>_<n>_<Name>.idml" ^
  --docx "<CH_ROOT>/Workbook/<ChapterName>_Exercise<L.N>_Workbook.docx" ^
  --out "<CH_ROOT>/Workbook/<NN>-<n+1>_Exercise_<L>_<N>_<Name>.idml"
```

**Page count.** Print may run a few pages longer than the eBook, because writing lines and cards need room at 7×10. Report the difference.

## 6. Proof (optional, with <AUTHOR>'s permission)

A structural proof can be rendered through Adobe's InDesign rendering service. That service uploads the IDML to <AUTHOR>'s Creative Cloud storage, so ask first, once per session.

**What the proof checks:**
- the structure and the content;
- that no text is missing.

**Fonts.** The render server substitutes fonts it doesn't have (Myriad Pro for Merriweather and Montserrat). Line breaks and the page count will differ from <AUTHOR>'s InDesign, where the fonts load from Adobe Fonts and Creative Cloud Desktop. Linked TIFFs render as gray boxes, because the server can't reach the local links.

**Look for:**
- overset or cut-off text;
- callout eyebrows that overlap their badges;
- crowded field labels;
- a complete reference list;
- footnotes on the right page.

**Where proofs go:** save them as `<CH_ROOT>/InDesign/_Proofs/<stem>_AdobeProof_<YYYYMMDD>.pdf` and `<CH_ROOT>/Workbook/_Proofs/…`.

## 7. Outputs and placement

| File | Location |
|---|---|
| Chapter print IDML | `<CH_ROOT>/InDesign/<NNN>_Chapter<N>_<Title_Words>.idml`. `<NNN>` continues the print book's document order (Chapter 2 = `004`, Chapter 3 = `005`) |
| Exercise print IDML | `<CH_ROOT>/Workbook/<NN>-<n>_Exercise_<L>_<N>_<PascalName>.idml`. The prefix continues the workbook's document order (Exercise 1.2 = `02-2`, Exercise 1.3 = `02-3`) |
| Structural proofs (optional) | `InDesign/_Proofs/` and `Workbook/_Proofs/` |
| eBook page files | `<EBOOK_DSM_ROOT>/Chapter<N>_eBook.dc.html`; the workbook's `_eBookDSM/WB - Chapter <N> Exercises.dc.html` |

**Report to <AUTHOR>:**
- the artifact links;
- the page counts (eBook against print);
- each figure's effective ppi, flagging any below 300 or too tall;
- anything left to check by hand.

## 8. Checks

| Check | Pass when |
|---|---|
| One column | No 2-column master, frame, or spread is used |
| Text complete | Every eBook block (book) or DOCX paragraph (workbook) is in the IDML, word for word. Pull quotes match the DOCX |
| Figures | Every figure links a CMYK TIFF in `Figures/CMYK/`; no RGB file is linked; effective ppi ≥ 300 or flagged |
| Callouts | Each callout uses the print template's style for its kind; no eBook color or motif is used |
| Footnotes and references | Every footnote is in the text; the reference list ends with the manuscript's last reference |
| Opener | The chapter or exercise title and epigraph are correct; the master's text is overridden, not showing through |
| Valid IDML | Every XML part parses; the IDML opens in InDesign (or renders in the proof) |

## 9. Manual finish (<AUTHOR>, InDesign)

1. Open the IDML. Re-apply or activate fonts where InDesign reports missing ones (Adobe Fonts).
2. Relink the figures if the links moved, then check the anchored figures and captions.
3. Check the callout badges, opener, spacing, and page breaks. Smart Text Reflow adds or removes pages at the end.
4. Save as INDD in the print book (INDB), and export the print PDF to:
   - the book: `<CH_ROOT>/InDesign/<ChapterName>_Print7x10.pdf`;
   - the workbook: the W2 location.

   Both are 7×10 in, with 0.125 in bleed and no printer's marks. PHASE 4 Part 0P (book) and PHASE 3W W2b (workbook) check the PDFs as before.

## 10. Rules

- **Never edit the DOCX or the MD.** The builds only read them.
- **Never write to `<PRINT_DSM_ROOT>`** or the workbook's `_PrintDSM/`. They are read-only.
- **`_eBookDSM` is for reference only on the print side.** Its styling never reaches print.
- **TIFF for print, RGB for the eBook.** Never one for the other.
- **One column only.** Never create 2-column spreads.
- **Ask before uploading anything** (proofs, artifacts). Artifacts are private.
- **Flag instead of guessing.** Flag a figure that is too small or too large, a page that runs over, or a callout with no print style.
