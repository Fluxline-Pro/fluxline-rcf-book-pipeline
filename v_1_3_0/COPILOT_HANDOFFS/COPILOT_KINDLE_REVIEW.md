# COPILOT_KINDLE_REVIEW (prompt v1.0)

**Step:** PHASE 4, Part B (book level, after the Kindle package is built), optional independent review · **Copilot mode:** Chat with uploads · **Output:** `COPILOT_KINDLE_REVIEW.md` · **Consumed by:** PHASE 4 Part B (B6) and PHASE 6.5

Follows `COPILOT_HANDOFF_STANDARD.md`. It checks the content and structure of the Kindle files. It does **not** replace EPUB validation (EPUBCheck), Kindle Previewer, or review on representative devices; those stay in the workflow.

## When to run it

After `<BOOK>_Kindle.docx` (and the EPUB or KDP package, where built) exists at Part B. This is a book-level review (`chapter: book` in the front matter, with one manuscript hash per chapter, one line each). There is no chapter-level Kindle review: the chapter's Kindle build (Part A) is covered by congruency pass 2 and the final eBook review.

## Files to upload (manifest)

| # | File | Required |
|---|---|---|
| 1 | `<BOOK>_Kindle.docx` | **Yes** |
| 2 | A PDF export of the Kindle Previewer's view of the EPUB. **EPUB itself is not a documented upload type**, so do not upload the `.epub` or a zip of it; if a package must be reviewed, convert its HTML to PDF first | Optional |
| 3 | The canonical manuscript(s) for the chapters in the file (MD or DOCX) | **Yes** |
| 4 | The final eBook PDF(s) | Optional |
| 5 | The Kindle preparation checklist (PHASE 4 Part A/B) | Yes |
| 6 | Figure registry (table or JSON) | Yes |
| 7 | Metadata file (`Kindle/<BOOK>_metadata.*`) | Yes |
| 8 | Table of contents, and the reference list | Yes |

Upload one or a few chapters at a time if the book-level DOCX exceeds 50 MB or is truncated; say which part you uploaded.

## Prompt (paste everything below this line)

```
ROLE
You are an independent reviewer of a Kindle manuscript file. You compare it with the source text and the preparation checklist, and report content and structure problems. You are not a Kindle conversion tool.

AUTHORITY
You may read the uploaded files and report. You may not edit or approve.

PROHIBITIONS
- Do not say the file is valid, KDP-ready, or will display correctly on any device. You cannot run EPUBCheck, Kindle Previewer, or a device.
- Do not rewrite text. Quote differences.
- Do not invent chapters, headings or problems. If you can't tell, write CANNOT VERIFY.

SOURCE-OF-TRUTH ORDER
Manuscript text, then reference list and metadata, then the figure registry, then the preparation checklist, then the Kindle file (under review).

FILES
The uploaded Kindle DOCX (and Kindle Previewer PDF), manuscripts, checklist, registry, metadata, table of contents and reference list. List the files you can see before you start.

TASK
List the files you can see. Then check:
1. Text completeness: compare the Kindle text with the manuscript, section by section (missing, duplicated, truncated, wording drift; quote each).
2. Chapter sequence against the table of contents.
3. Heading hierarchy (Title, Heading 1 to 3): skipped levels, wrong levels, headings styled as body text.
4. Table of contents entries against the headings; any entry that has no heading, or a heading missing from the contents.
5. Figure and caption placement, figure numbering against the registry.
6. Missing alt text, as far as you can tell from the file (say if alt text can't be inspected).
7. Reference integrity: markers against the reference list; every cited reference present.
8. Formatting anomalies visible in the supplied artifacts: stray page numbers, manual page breaks, tab-indented paragraphs, fixed-layout leftovers, layout-only tables, empty paragraphs, odd characters.
9. Obvious conversion artifacts (smart-quote damage, broken characters, lost italics, lists turned into paragraphs).
10. Metadata discrepancies (title, subtitle, author, edition, language) against the manuscript.

OUTPUT SCHEMA
Markdown titled COPILOT_KINDLE_REVIEW:
- Front matter code block (as the standard).
- Outcome: PASS | CONDITIONAL PASS | FAIL | AUTHOR DECISION REQUIRED, with two sentences.
- Findings table: ID | Location (chapter / heading / page) | Area (TEXT / SEQUENCE / HEADINGS / TOC / FIGURE / ALT TEXT / REFERENCES / FORMATTING / CONVERSION / METADATA) | Observation | Severity (blocking / non-blocking) | Evidence | Suggested resolution.
- Wording parity table: Location | Manuscript | Kindle file.
- NOT CHECKED (always list): EPUB validity, Kindle Previewer rendering, device rendering, reflow behaviour, embedded fonts, image resolution, KDP upload checks.

GATE EFFECT
Claude verifies each finding; the author decides. Deterministic validation and device previews remain separate required checks.

LIMITATIONS
This is an AI review of the supplied files. It is not EPUB validation, Kindle Previewer, KDP checking or a device test.

RETURN
Plain Markdown, savable as COPILOT_KINDLE_REVIEW.md.

PRIVACY
Use only the uploaded files.

HUMAN APPROVAL
Nothing is changed without the author's decision.
```

## After Copilot answers

Save to `<BOOK_ROOT>/_BookGovernance/Copilot/COPILOT_KINDLE_REVIEW_<YYYYMMDD>.md`. Fill in `manuscriptSha256` as one `<ChapterName>: <hash>` line per chapter.

## Gate effect

Confirmed blocking findings must be fixed in the Kindle build (then rebuild and review the changed parts) or accepted by `<AUTHOR>` in writing before Part B is called done. EPUB validation, Kindle Previewer and device previews stay required where the workflow has them. The report feeds PHASE 6.5.

## What invalidates the result

A rebuilt Kindle DOCX/EPUB or a change to the locked manuscript.
