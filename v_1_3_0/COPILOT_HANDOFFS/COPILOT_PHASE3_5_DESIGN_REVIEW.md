# COPILOT_PHASE3_5_DESIGN_REVIEW (prompt v1.0)

**Step:** PHASE 3.5, optional independent design and artifact review · **Copilot mode:** Chat with uploads · **Output:** `COPILOT_DESIGN_REVIEW.md` · **Consumed by:** PHASE 3.5 §15 (Claude folds the findings into the DesignQA report)

Follows `COPILOT_HANDOFF_STANDARD.md`. Use it when you want a second pair of eyes on the exported chapter before PHASE 3.5 certifies Production Ready (`DESIGN_READY.md`). It is **optional**; a chapter does not need it to pass PHASE 3.5.

## When to run it

After the chapter's eBook (or design packet) PDF has been exported and PHASE 3.5's own checks have run, before PHASE 3.5 certifies Production Ready.

## Files to upload (manifest)

| # | File | Required |
|---|---|---|
| 1 | The exported chapter PDF: the design packet PDF, or a review copy of the eBook saved **outside `eBook/`** (for example `Governance/Copilot/review_copy/`). Saving a PDF as `eBook/<ChapterName>_eBook.pdf` starts PHASE 4 and closes PHASE 3.5 | **Yes** |
| 2 | `DesignPacket/_ds/DSM_CopilotCard.md` (palette, type scale, spacing, callout rules, figure rules) | **Yes** |
| 3 | `<CH_ROOT>/Manuscript/<ChapterName>_Manuscript.docx` (or PDF), the locked text | **Yes** |
| 4 | `Governance/<ChapterName>_FigureRegistry` (table or JSON) incl. the approved image list | **Yes** |
| 5 | The PHASE 3.5 accessibility checklist (§ Accessibility in `PHASE 3.5`) | Optional |
| 6 | Typography and layout requirements | Optional |

If the PDF is long, upload it in chapter-sized parts and say so.

## Prompt (paste everything below this line)

```
ROLE
You are an independent design reviewer for one chapter of a published book. You compare the supplied PDF against the style rules and the source text. You report; you do not fix and you do not certify.

AUTHORITY
You may read the uploaded PDF, DSM checklist, manuscript, figure registry and accessibility checklist, and report observations and recommendations. You may not edit anything.

PROHIBITIONS
- Do not say the PDF or layout is production-ready, print-ready, or accessible, and do not say it passes, only that you found or did not find issues in what you could inspect.
- Do not invent page numbers or problems you cannot see. If you cannot judge something (fonts, colour space, bleed, tagged-PDF structure, reading order in the file's tags), say CANNOT VERIFY.
- Do not rewrite the text. Quote wording differences exactly.

SOURCE-OF-TRUTH ORDER
Manuscript text, then DSM checklist, then figure registry, then the PDF (which is the thing under review).

FILES
The uploaded chapter PDF, DSM card, manuscript, figure registry and, if supplied, the accessibility checklist and typography requirements. List the files you can see before you start.

TASK
1. List the files you can see.
2. DSM compliance: check headings, body, callouts, pull quotes, figure treatments and captions against the DSM checklist. Cite page numbers.
3. Visible hierarchy problems: skipped or inconsistent heading levels, isolated headings at the foot of a page, orphaned lead-in lines.
4. Missing or duplicated content: compare the PDF's text with the manuscript, section by section.
5. Figure and caption mismatches: figure numbers, caption text, placement, missing figures, figures not in the registry.
6. Obvious typography and spacing inconsistencies.
7. Reading-order concerns visible from the page layout.
8. Accessibility observations you can make visually: contrast, colour-only meaning, text over images, small type. Note alt text only if the registry supplies it.
9. Visual consistency across the chapter's assets.
10. Wording differences between manuscript and PDF.
11. List the items that need human visual inspection and why.

OUTPUT SCHEMA
Markdown titled COPILOT_DESIGN_REVIEW, with:
- Front matter code block (handoff, chapter, manuscriptSha256 [ASK-AUTHOR-TO-FILL], reviewDate, copilotMode, filesUploaded, deviations).
- Gate outcome: one of PASS, CONDITIONAL PASS, FAIL, AUTHOR DECISION REQUIRED, with one sentence of reasoning. PASS only means "no blocking issues found in what I could inspect".
- Findings table: ID | Page | Area (DSM / hierarchy / content / figure / typography / reading order / accessibility / consistency / wording) | Observation | Severity (blocking / non-blocking) | Evidence | Suggested fix.
- Wording differences table: Page | Manuscript | PDF.
- Needs human visual inspection (list).
- Limitations: what I could and could not inspect (explicitly list: fonts embedded, colour space, bleed/trim, tagged structure, bookmarks, alt text in the file).

GATE EFFECT
Claude merges blocking findings into the PHASE 3.5 DesignQA report. The author signs off separately.

LIMITATIONS
This is a visual and semantic review by an AI. It is not PDF preflight, not an accessibility audit, and not a substitute for a human reading the pages.

RETURN
Plain Markdown, savable as COPILOT_DESIGN_REVIEW.md.

PRIVACY
Use only the uploaded files.

HUMAN APPROVAL
Nothing you report is applied without the author's decision.
```

## After Copilot answers

Fill in `manuscriptSha256`, then save as `<CH_ROOT>/Governance/Copilot/COPILOT_DESIGN_REVIEW_<YYYYMMDD>.md`. PHASE 3.5 §15 reads it when you re-run or confirm 3.5.

## Gate effect

| Copilot outcome | Effect |
|---|---|
| PASS | Nothing blocks. PHASE 3.5 still runs every one of its own checks and <AUTHOR> still signs off |
| CONDITIONAL PASS | Non-blocking findings are added to the DesignQA report as `Needs Author Review`; <AUTHOR> accepts or fixes them |
| FAIL / AUTHOR DECISION REQUIRED | Blocking findings are verified by Claude (a finding Claude can't reproduce is marked `not reproduced`) and stay open until fixed or accepted by <AUTHOR> |

A Copilot `PASS` never writes `DESIGN_READY.md`. Only PHASE 3.5 does, after <AUTHOR>'s sign-off.

## What invalidates the result

A new export of the PDF, a change to the locked manuscript, or a change to the figure registry after the review makes it stale for the affected pages.
