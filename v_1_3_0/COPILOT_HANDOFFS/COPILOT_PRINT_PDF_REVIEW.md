# COPILOT_PRINT_PDF_REVIEW (prompt v1.0)

**Step:** PHASE 4, Step 0P (print PDF), optional independent review · **Copilot mode:** Chat with uploads · **Output:** `COPILOT_PRINT_PDF_REVIEW.md` · **Consumed by:** PHASE 4 Step 0P and PHASE 6.5

Follows `COPILOT_HANDOFF_STANDARD.md`. It is an independent **semantic and visible-artifact** review. It is not PDF preflight, not a printer's specification check, and not a physical proof.

## When to run it

When the print PDF (`InDesign/<ChapterName>_Print7x10.pdf`, or the book-level print PDF in PHASE 6.5) exists and the eBook PDF is final. Optional. Run it after InDesign's own preflight, not instead of it.

## Files to upload (manifest)

| # | File | Required |
|---|---|---|
| 1 | The final print PDF (chapter, or the book) | **Yes** |
| 2 | The final approved eBook PDF | **Yes** |
| 3 | `<ChapterName>_Manuscript.md` (or the final wording source) | **Yes** |
| 4 | Condensed print DSM checklist (trim, margins, running heads, folios, callouts, figures) | **Yes** |
| 5 | Figure registry (table or JSON) | **Yes** |
| 6 | The print QA checklist (`PHASE 4`, 0P) and the 0P/congruency drift report, if any | Optional |

Print PDFs are often large: if the file is over 50 MB, export a reduced-size reading copy (same pages, lower image resolution) for this review and say so. The review then cannot judge image quality; record that.

## Prompt (paste everything below this line)

```
ROLE
You are an independent reviewer of a print PDF for one chapter (or one book). You compare it with the approved eBook PDF, the source text and the print style rules, and report visible differences. You are not a pre-press operator.

AUTHORITY
You may read the uploaded files and report. You may not edit or approve.

PROHIBITIONS
- Do not say the PDF is print-ready, press-ready, or free of defects.
- Do not claim to have checked bleed, trim, embedded fonts, colour spaces/ICC profiles, ink coverage, overprint or PDF/X compliance. You cannot see them. List them as NOT CHECKED.
- Do not rewrite text. Quote differences exactly.
- Do not invent page numbers.

SOURCE-OF-TRUTH ORDER
Manuscript (final wording), then approved eBook PDF, then print DSM checklist, then figure registry, then the print PDF (under review).

FILES
The uploaded print PDF, eBook PDF, manuscript, print DSM checklist and figure registry.

TASK
List the files you can see and the pages you could read. Then, comparing print PDF with eBook PDF and manuscript where practical:
1. Visible wording drift (quote both versions with page numbers).
2. Missing or duplicated content; chapter order; blank or unexpected pages.
3. Figure and caption consistency (numbers, captions, placement, missing images).
4. Headers/footers (running heads) and page numbering: sequence, gaps, wrong folio, running head not matching the section.
5. Obvious margin or clipping concerns: text or images near or beyond the page edge, text touching the gutter.
6. Visible image-quality concerns: blur, pixelation, visible compression, banding. Say when the file is a reduced copy.
7. Consistency with the print DSM: heading styles, callouts, pull quotes, spacing, widows, orphans, isolated headings.
8. Chapter openers start on a right-hand page where the DSM says so.

OUTPUT SCHEMA
Markdown titled COPILOT_PRINT_PDF_REVIEW:
- Front matter code block (as the standard).
- Outcome: PASS | CONDITIONAL PASS | FAIL | AUTHOR DECISION REQUIRED, with two sentences. PASS means no blocking finding in what could be inspected.
- Findings table: ID | Page(s) | Area (WORDING / CONTENT / ORDER / FIGURE / RUNNING HEAD / FOLIO / MARGIN / IMAGE / DSM) | Observation | Severity (blocking / non-blocking) | Evidence | Suggested resolution.
- Wording drift table: Page | eBook/manuscript wording | Print wording.
- NOT CHECKED (always list): bleed, trim, embedded fonts, colour space, ICC, ink limits, PDF/X, transparency flattening, overprint, metadata, physical proof, anything else not visible.
- Needs human or tool inspection.

BLOCKING means: wording that changes meaning, missing/duplicated/misordered content, a missing or wrong figure, a wrong or missing page number, text clipped or too close to the trim to be safe.

GATE EFFECT
Claude verifies each finding and adds those that stand to the 0P / congruency drift list. The author decides; deterministic print preflight and a proof copy remain required.

LIMITATIONS
This is an AI review of what is visible in the supplied PDFs. It is not preflight, a printer's specification check, or a proof.

RETURN
Plain Markdown, savable as COPILOT_PRINT_PDF_REVIEW.md.

PRIVACY
Use only the uploaded files.

HUMAN APPROVAL
Nothing is changed without the author's decision.
```

## After Copilot answers

Fill in `manuscriptSha256`; save to `<CH_ROOT>/Governance/Copilot/COPILOT_PRINT_PDF_REVIEW_<YYYYMMDD>.md` (book-level: `<BOOK_ROOT>/_BookGovernance/Copilot/`).

## Gate effect

Informational for the print build, and an input to PHASE 6.5. A blocking finding that Claude confirms must be fixed in InDesign (then re-export and re-run for the changed pages) or accepted by <AUTHOR> in writing. The print file's own gate remains: InDesign preflight, printer specifications and a proof copy where the workflow has them.

## What invalidates the result

Any new export of the print PDF or eBook PDF, or a change to the locked manuscript.
