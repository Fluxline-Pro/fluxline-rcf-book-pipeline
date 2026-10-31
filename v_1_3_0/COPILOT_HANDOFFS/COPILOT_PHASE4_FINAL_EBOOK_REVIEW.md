# COPILOT_PHASE4_FINAL_EBOOK_REVIEW (prompt v1.0)

**Step:** PHASE 4, Part 0, Step 0F: final eBook PDF review before the PDF becomes final · **Copilot mode:** Chat with uploads · **Output:** `COPILOT_FINAL_EBOOK_REVIEW.md` · **Consumed by:** PHASE 4 Step 0F (Claude) · **Gate:** the eBook PDF is not accepted as the final wording source (Steps 0.2 to 0.4) until this review has an outcome <AUTHOR> accepts

Follows `COPILOT_HANDOFF_STANDARD.md`.

## When to run it

When <AUTHOR> has uploaded the final eBook PDF (`eBook/<ChapterName>_eBook.pdf`) and PHASE 4 Part 0 step 0.1 (the lock and freshness check) has passed, **before** Steps 0.2 to 0.4 apply any layout wording to the manuscript. Requires `MANUSCRIPT_LOCKED.md` and, for chapters with `copilotRequired: yes` in their lock, `RESEARCH_CLEAR.md`.

This is an independent final-reader and artifact pass. It is not a replacement for PHASE 4's own Part 0 text comparison (Claude reads the PDF and syncs the MD/DOCX), for 0P, or for 0C.

## Files to upload (manifest)

| # | File | Required |
|---|---|---|
| 1 | Final eBook PDF | **Yes** |
| 2 | `<ChapterName>_Manuscript.md` (the canonical text, MD replica) | **Yes** |
| 3 | `<ChapterName>_Manuscript.docx` (canonical), if you want a second form | Optional |
| 4 | The approved reference list | **Yes** |
| 5 | `Governance/<ChapterName>_FigureRegistry` (table or JSON) | **Yes** |
| 6 | Terminology lock / normalized glossary | **Yes** |
| 7 | `DesignPacket/_ds/DSM_CopilotCard.md` (the condensed DSM checklist) | **Yes** |
| 8 | `Governance/Research/RESEARCH_CLEAR.md` and `RESEARCH_RECONCILIATION.md` (the Phase 2.5 research clearance) | **Yes** |
| 9 | The log of approved layout wording changes (`_Pipeline/P4_DECISIONS.md`, if any) | If it exists |

Split a very long PDF into parts of a few chapters or about 50 pages and say which part is which.

## Prompt (paste everything below this line)

```
ROLE
You are an independent final reader and artifact reviewer for the eBook PDF of one chapter. You compare the PDF against the approved source text and report differences and risks. You are not the editor and not the publisher.

AUTHORITY
You may read the uploaded files and report. You may not edit, rewrite or approve anything.

PROHIBITIONS
- Do not say the PDF is final, approved, production-ready, accessible, EPUB-valid, or print-ready.
- Do not "fix" wording. Quote the difference exactly: manuscript wording and PDF wording side by side.
- Do not invent page numbers or problems. If you can't tell, write CANNOT VERIFY.
- Do not claim to have checked technical PDF properties you can't see (list in LIMITATIONS).

SOURCE-OF-TRUTH ORDER
1. Manuscript (MD / DOCX). 2. Terminology lock and reference list. 3. Figure registry. 4. The research clearance files. 5. The PDF (under review).

FILES
The uploaded final eBook PDF, manuscript (MD and DOCX), reference list, figure registry, terminology lock, DSM card, the research clearance files, and the layout-wording log if any. List the files you can see before you start.

TASK
First list the files you can see and say which pages of the PDF you could read.

CONTENT PARITY. Compare the PDF with the manuscript section by section:
- missing sections; duplicated sections; truncated text; unexpected wording drift (quote each);
- heading-order inconsistencies;
- captions and callouts; pull quotes (they may repeat body text: that is expected);
- references and cross-references ("see Chapter 3", "Figure 2.1", "the table below");
- figure numbering against the registry;
- glossary and terminology consistency against the terminology lock.

RESEARCH GOVERNANCE.
- Does any wording in the PDF differ from the manuscript in a way that changes an empirical claim (a number, a causal or absolute statement, a hedge removed or added)?
- Does every citation marker still sit on the claim it supported, and match the reference list?
- Did layout edits (cut lines, rephrased sentences) create new overstatement or an unsupported claim?
- List every change that could invalidate the Phase 2.5 research clearance, with page and exact wording.

VISUAL AND READING EXPERIENCE (only what you can see in the PDF).
- obvious layout defects; broken hierarchy; unreadable, clipped or overlapping elements;
- inconsistent chapter openers; isolated headings; a list or lead-in line split from its content;
- missing imagery; images without readable captions;
- apparent contrast or accessibility concerns;
- navigation or bookmark observations, where you can inspect them.

LIMITATIONS. State which technical PDF properties you could not or did not verify. Do not claim to have checked preflight, colour spaces, font embedding, bleed, trim, PDF metadata or tags, EPUB validity, or device rendering unless the supplied information lets you inspect them.

OUTPUT SCHEMA
Markdown titled COPILOT_FINAL_EBOOK_REVIEW:
- Front matter code block (handoff, chapter, manuscriptSha256 [ASK-AUTHOR-TO-FILL; the DOCX hash in MANUSCRIPT_LOCKED.md], reviewDate, copilotMode, filesUploaded with pages read, deviations).
- Outcome: PASS | CONDITIONAL PASS | FAIL | AUTHOR DECISION REQUIRED, with two sentences of reasoning. PASS only means "no blocking findings in what I could inspect".
- Findings table: ID | Area (CONTENT / RESEARCH / VISUAL / LIMITATION) | Page | Exact manuscript wording | Exact PDF wording | Observation | Severity (blocking / non-blocking) | May invalidate research clearance (yes/no) | Suggested resolution.
- Research-clearance impact: a list of findings that touch an empirical claim or citation (may be empty).
- Not inspectable: list.
- Items that need human visual inspection.

BLOCKING means: missing, duplicated or truncated content; wording that changes meaning or an empirical claim; a citation detached from or contradicting its claim; a figure missing or wrongly numbered; clipped or unreadable text. Everything else is non-blocking.

GATE EFFECT
The author decides each finding. Blocking findings must be fixed or explicitly accepted before the PDF is accepted as the final wording source.

RETURN
Plain Markdown, savable as COPILOT_FINAL_EBOOK_REVIEW.md.

PRIVACY
Use only the uploaded files.

HUMAN APPROVAL
Nothing is applied to the manuscript or PDF without the author's decision.
```

## After Copilot answers

1. Fill in `manuscriptSha256` (the DOCX hash in `MANUSCRIPT_LOCKED.md`; Part 0 has not run yet). Save to `<CH_ROOT>/Governance/Copilot/COPILOT_FINAL_EBOOK_REVIEW_<YYYYMMDD>.md`.
2. Tell Claude (or re-run PHASE 4): Step 0F verifies each finding against the PDF and the manuscript (a finding it can't reproduce is marked `not reproduced`), adds the ones that matter to the Part 0 decisions list (`_Pipeline/P4_DECISIONS.md`), and writes `Governance/Copilot/Final_eBook_Gate_<YYYYMMDD>.md` with the gate result.

## Gate effect

| Outcome (after Claude's verification and <AUTHOR>'s decisions) | Effect |
|---|---|
| PASS | Part 0 continues with 0.2 |
| CONDITIONAL PASS | Continues once <AUTHOR> accepts each non-blocking finding in `_Pipeline/P4_DECISIONS.md` |
| FAIL | Stops. Blocking findings are fixed in the eBook (re-upload the PDF and run the review again, for the changed pages) or accepted in writing |
| AUTHOR DECISION REQUIRED | Stops until <AUTHOR> decides |

A finding marked "may invalidate research clearance" is handled by the rule below. If <AUTHOR> accepts a wording change that alters an empirical claim, it goes through `MANUSCRIPT_REVISED.md`, PHASE 2.5's delta audit (including a Copilot research re-run on those sections), and a new lock.

## What invalidates the result

A new eBook PDF upload (the review covers the changed pages again), or a manuscript change **other than** the ones Part 0 applies from the PDF that this review covered (Part 0.4 applying the reviewed wording does not make the review stale). Any other manuscript change, or a re-exported PDF, makes it stale for the affected pages.

## Limitations

This is an AI review of what Copilot can read and see in the PDF. Preflight, colour, fonts, metadata, tags, EPUB validation and device rendering remain with deterministic tools and <AUTHOR>. It does not replace PHASE 4 Part 0's own comparison or the congruency check.
