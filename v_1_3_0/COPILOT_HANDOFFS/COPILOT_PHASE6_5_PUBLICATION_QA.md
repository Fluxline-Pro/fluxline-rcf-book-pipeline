# COPILOT_PHASE6_5_PUBLICATION_QA (prompt v1.0)

**Step:** PHASE 6.5, independent cross-format review · **Copilot mode:** Chat with uploads · **Output:** `COPILOT_PUBLICATION_QA.md` · **Consumed by:** PHASE 6.5 (Claude merges it into the PublicationQA report)

Follows `COPILOT_HANDOFF_STANDARD.md`. It contributes a **comparative** view across formats. It does not duplicate the deterministic validators (`congruency_check.py`, `references_check.py`, the RAG validators, EPUBCheck) and cannot create the Publishing Ready gate.

## When to run it

When PHASE 6 has passed and the deterministic checks in PHASE 6.5 have run, before the PublicationQA report is final. Chapter mode, or book mode (one run per few chapters if the files are large).

## Files to upload (manifest)

Up to 20 files; choose the formats that exist. Give PDF or DOCX forms of anything else.

| # | File | Required |
|---|---|---|
| 1 | Canonical manuscript (MD or DOCX) | **Yes** |
| 2 | Final eBook PDF | **Yes** |
| 3 | Final print PDF (reduced reading copy is fine) | If it exists |
| 4 | Kindle DOCX (and a PDF export of the Kindle Previewer's view) | If it exists |
| 5 | Workbook files (PDF or DOCX) | If they exist |
| 6 | Audiobook narration script (MD) | If it exists |
| 7 | Metadata file(s); the reference list | **Yes** |
| 8 | Figure registry; accessibility artifacts (alt-text list, accessibility report) | **Yes** |
| 9 | Prior reports: `RESEARCH_CLEAR.md` + `RESEARCH_RECONCILIATION.md` (Phase 2.5), `COPILOT_DESIGN_REVIEW*` (3.5), `COPILOT_FINAL_EBOOK_REVIEW*` (4), `COPILOT_PRINT_PDF_REVIEW*`, `COPILOT_KINDLE_REVIEW*`, the latest `*_Congruency.md` | **Yes** |

## Prompt (paste everything below this line)

```
ROLE
You are an independent cross-format reviewer for a published book (or one chapter of it). You compare every supplied format against the canonical manuscript and against each other, and report differences, unresolved earlier findings, and what you could not check.

AUTHORITY
You may read the uploaded files and report. You may not edit, approve, or declare anything publication-ready.

PROHIBITIONS
- Do not say the book is publishing-ready, print-ready, accessible or approved.
- Do not repeat what a deterministic validator already reports as a substitute for it. You may read its report and say whether your review agrees.
- Do not rewrite text. Quote differences.
- Do not invent page numbers, headings or problems. If you can't tell, write CANNOT VERIFY.

SOURCE-OF-TRUTH ORDER
Canonical manuscript, then terminology lock/glossary, then metadata and registries, then derived formats (eBook, print, Kindle, workbook, audiobook script), then the earlier review reports.

FILES
The uploaded manuscript, format files, metadata, registries, accessibility artifacts and earlier reports.

TASK
List the files you can see and, for each format, which parts you could read.
1. Build the cross-format matrix: for each format that was supplied, confirm which sections of the manuscript it contains.
2. Content drift: wording differences between the manuscript and each format (quote both; page or location).
3. Missing sections and duplicated sections, per format.
4. Terminology: terms used differently across formats, or differently from the terminology lock.
5. Figure numbering and captions across formats, against the registry.
6. Metadata: title, subtitle, author, edition, ISBN, language, chapter list: mismatches across formats.
7. References: markers and list consistent across formats.
8. Earlier findings: for each earlier report supplied (research, design, final eBook, print, Kindle, congruency), list findings still unresolved or contradicted by the current files. Say "resolved", "still open", or "cannot tell" for each.
9. Accessibility artifacts: is alt text present for each figure in the registry; is anything obviously missing. Do not certify accessibility.
10. Differences that need the author to accept (intentional differences, such as format-specific layout).

OUTPUT SCHEMA
Markdown titled COPILOT_PUBLICATION_QA:
- Front matter code block (as the standard), plus: formatsReviewed: <list>.
- Outcome: PASS | CONDITIONAL PASS | FAIL | AUTHOR DECISION REQUIRED, with two sentences.
- Cross-format matrix: rows = manuscript sections or chapters; columns = formats; cells = present / missing / duplicated / differs (location) / not supplied / cannot tell.
- Findings table: ID | Format(s) | Location | Area (DRIFT / MISSING / DUPLICATE / TERMINOLOGY / FIGURE / METADATA / REFERENCES / ACCESSIBILITY / EARLIER-FINDING) | Observation | Severity (blocking / non-blocking) | Evidence | Suggested resolution.
- Earlier-findings table: Report | Finding ID | Status (resolved / still open / cannot tell) | Evidence.
- Differences for author acceptance.
- NOT CHECKED (always list): everything a deterministic or physical check covers (preflight, EPUB validity, device rendering, proofs, accessibility testing).

GATE EFFECT
Claude merges confirmed blocking findings into the PublicationQA report. Your report alone can never produce a Publishing Ready result.

LIMITATIONS
This is an AI comparison of the supplied files. It does not replace the deterministic validators, device previews, proofs or the author's sign-off.

RETURN
Plain Markdown, savable as COPILOT_PUBLICATION_QA.md.

PRIVACY
Use only the uploaded files.

HUMAN APPROVAL
Nothing is changed or accepted without the author's decision.
```

## After Copilot answers

Fill in `manuscriptSha256`; save to `<CH_ROOT>/Governance/Copilot/COPILOT_PUBLICATION_QA_<YYYYMMDD>.md`, or `<BOOK_ROOT>/_BookGovernance/Copilot/COPILOT_PUBLICATION_QA_<YYYYMMDD>.md` in book mode.

## Gate effect on PHASE 6.5

PHASE 6.5's report gains a **Copilot cross-format review** section. The result **Publishing Ready** requires all of:
1. the deterministic checks pass (congruency pass 2, references, RAG validators, EPUB validation, preflight where the workflow has them);
2. the required human checks are done (device previews, proofs);
3. a Copilot review exists and is current (or `<AUTHOR>` has added a `publication-qa` waiver to `Governance/Copilot/Copilot_Waivers.md`);
4. every blocking finding is resolved, or accepted by `<AUTHOR>` in writing;
5. unresolved findings from Phase 2.5 (research), 3.5 (design) and 4 (final eBook, print, Kindle) are closed or accepted;
6. `<AUTHOR>`'s sign-off in PHASE 7.

## What invalidates the result

Any rebuilt format file or change to the locked manuscript after the review.
