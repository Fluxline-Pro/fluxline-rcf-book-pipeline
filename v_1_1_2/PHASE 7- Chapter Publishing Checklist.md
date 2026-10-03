# PHASE 7: Chapter Publishing & Release Checklist (v3.4)

## Final Validation, LLM Recommendations, and Human Sign-off

> **Pipeline position:** PHASE 7 of 7 (Release) · **Upstream gate:** latest PHASE 6.5 report certifies **Publishing Ready** · **Downstream:** none (chapter becomes **Published**)
> **Canonical paths, status ladder, triggers, and deliverables:** see `MASTER_PIPELINE_OVERVIEW.md`.

**v3.4 changes (2026-10-03, release v1.1.2): print QA.** New Part A items for PHASE 4 Part 0P: the print PDF is uploaded, and the latest `_BookGovernance/PrintQA/<ChapterName>_PrintQA.md` shows no open text difference to check and no layout error, with every warning fixed or accepted by <AUTHOR>. They replace the self-reported print cross-check. Part C gains **Print Approved**, and the completion rule requires a closed 0P report. The PHASE 3W section gains the same item for the print workbook (N/A when the workbook ships eBook only).

**v3.3 changes (2026-10-02, release v1.1): PHASE 7 runs locally and automatically.**
- **When it runs:** as soon as PHASE 6.5 finishes, whether or not it passed. A run that didn't pass simply lists what's missing.
- **No Claude:** a deterministic local check (reference implementation: `release_check.py` in `<LOCAL_TOOLS_ROOT>`) pre-fills the checklist.
- **Part A:** each item it can prove from the files is ticked, with its evidence path. Items it can't prove are left unticked, with the reason. Judgment calls are marked 👤 for <AUTHOR>.
- **Part B:** drafted by the local LLM (Ollama; e.g. phi4 14B) **from the unmet checks only**. If the model is down, a plain list of the gaps is used.
- **Part C:** left blank for <AUTHOR>.
- **Notification:** <AUTHOR> gets an email listing what's missing, or "ready for your sign-off".
- **New Part A items:** the references check (PHASE 1 10b / PHASE 4 0R), the glossary lock (PHASE 4 0G), and PHASE 3.5 completion by upload.
- **Where it's saved:** in `<CH_ROOT>`. A chapter the automation may not edit gets a report-only copy in `_BookGovernance/ReleaseChecks/` instead.

**v3.2 changes (2026-09-30 workbook track):** a PHASE 3W section verifies the workbook's eBook and full-color print PDFs, and the Workbook sub-certification.

**Book audit (2026-09-27):** the book-level section verifies the PHASE 0.9 final delta audit.

**v3.1 changes (2026-09-24 dual-RAG):** the PHASE 5 section verifies the Local and Cloud RAG tracks separately, plus their parity. The RAG sub-certification is split per track.

**v3 changes (2026-09-22 pipeline alignment):**
- Retitled from "PHASE 6". The internal phase sections now match the real phases (1, 2, 3, 3.5, 4, 5, 6, 6.5) instead of the old 1–6 numbering ("Local AI Pipeline", "Copilot Publishing").
- Absorbs the superseded stub `PHASE 4- Local LLM AI and Human Publishing Checklist.md` (editorial review, publishing prep, knowledge systems, version control).
- Adds Marketing, eBook, DesignPacket, triggers, and all book-level deliverables to the verification.
- Adds Part B, "LLM Recommendations", which Claude completes **before** <AUTHOR> signs.
- Folder audit matches the canonical `Final/` structure; the Published, Archive, and Finalized Releases paths are defined.

---

## How to use

1. The local release check (v3.3) writes this checklist to `<CH_ROOT>/<ChapterName>_PHASE7_ReleaseChecklist.md`.
   - It pre-fills Part A (evidence: file paths, report names, gate statuses) and Part B (local-LLM recommendations from the gaps).
   - It runs automatically after PHASE 6.5, and again whenever <AUTHOR> asks for a re-run.
   - Claude may still be used instead, following the same rules.
2. <AUTHOR> reviews, ticks, and signs Part C. Only <AUTHOR> can mark a chapter **Published**.
3. After sign-off, a copy is placed in `<BOOK_ROOT>/_FinalizedReleases/<ChapterName>_PHASE7_ReleaseChecklist_v<chapterVersion>.md`, where `<chapterVersion>` is the `chapterVersion` value from `Governance/<ChapterName>_VersionMetadata.json` (e.g. `..._ReleaseChecklist_v1.0.md`). Re-releasing a chapter writes a new file at its new version rather than replacing the signed one.

`<CH_ROOT>` = `<BOOK_ROOT>/Chapters/<ChapterName>/Final/`

---

# Chapter Information

| Item | Value |
| --- | --- |
| Chapter Number |  |
| Chapter Name |  |
| Version (VersionMetadata) |  |
| Review Date |  |
| Current Status | Draft / Review Ready / Design Ready / Production Ready / Publishing Ready / Published |
| Reviewer | <AUTHOR> |

---

# PART A — VALIDATION OF OUTPUTS (the local release check pre-fills evidence; <AUTHOR> confirms)

## PHASE 1 — Content Production

### Review Packet
- [ ] Chapter Summary · Key Takeaways · Glossary Terms · Definitions · Frameworks · Metadata JSON

### Workbook Packet
- [ ] Primary Exercise · Additional Exercises · Reflection Questions · Application Questions · Workbook DOCX (canonical) + Markdown replica

### Training Materials
- [ ] Instructor Notes · Teaching Objectives · Facilitation Guide · Discussion Questions · Training Outline

### Reference Guides
- [ ] One per major topic · Key Concepts · Definitions · Practical Checklists · Visual descriptions

### Slide Deck Outline
- [ ] Title slide · 8–20 slides · Reflection slide · Key concepts · Visual suggestions · Speaker notes

### Equations
- [ ] Equation sheet (XLSX), or README stating not applicable

### eBook Prep (`/eBook/`)
- [ ] HTML blocks · eBook metadata · TOC entries

### InDesign Prep
- [ ] Layout notes · Pull quotes · Sidebar summaries · Figure suggestions · Spread suggestions

### Audiobook Prep
- [ ] Narration script · Pronunciation guide · Segment markers · Pacing notes · MD transcript

### RAG Packet (PHASE 1)
- [ ] Chunks · Metadata JSON · Semantic tags · Retrieval summaries

### Marketing & Local LLM Intake
- [ ] 6 Intake files · Seed files · VoiceKit (book-level) present
- [ ] `MARKETING_READY.md` present (no `MARKETING_INCOMPLETE.md`)

### Editorial
- [ ] `EditorialSuggestions.md` resolved; accepted edits applied and versioned
- [ ] Final wording review · voice consistency · technical validation

### References / bibliography (v3.3)
- [ ] `_BookGovernance/References/<ChapterName>_ReferencesCheck.md`: every citation ↔ entry; DOIs verified; links open; no open critical/major finding (PHASE 1 10b fixes applied; PHASE 4 0R report clean)

## PHASE 2 — Governance

- [ ] ArtifactManifest.json complete; paths and versions accurate
- [ ] CrossReferenceReport: no open Critical items
- [ ] FigureRegistry.json complete
- [ ] LearningMetadata.json complete
- [ ] GlossaryNormalized.json: no duplicates; References: Ch N present
- [ ] TerminologyAudit: no conflicting terms
- [ ] MarketingIntakeValidation passed
- [ ] RemediationLog: no `Open` items; all `Needs Author Review` resolved
- [ ] ManuscriptChangeProposals reviewed by <AUTHOR>
- [ ] ChapterCertification = **Design Ready**
- [ ] `GOVERNANCE_READY.md` present

## PHASE 3 — Claude Design

- [ ] DesignPacket complete (deck, facilitator, learner, ref guides, review, workbook, opener, figures)
- [ ] Exported figure images in `DesignPacket/figures_export/` for every FigureRegistry entry
- [ ] eBook, Print 7×10, and Workbook eBook/Print layouts present
- [ ] Exports: Slides PPTX + PDF · eBook PDF + EPUB
- [ ] InDesign print files (manual) present

## PHASE 3W — Workbook

*If the book's workbook profile says `enabled: false`, tick only "`WORKBOOK_NOT_APPLICABLE.md` present" and skip the rest of this section. Only the formats the profile lists are required.*

- [ ] `Workbook/Trigger/WORKBOOK_MANUSCRIPT_READY.md` was present before the workbook design (DOCX = MD, exercise IDs registered)
- [ ] Final workbook PDF(s) uploaded by <AUTHOR>, to `Workbook/<ChapterName>_Workbook_eBook.pdf` (8.5×11) [+ `_Workbook_Print.pdf` (7×10) if the book ships print] or to `<WORKBOOK_BOOK_ROOT>/…/<NN>_Ex_<L>_<N>_Chapter<C>.pdf` [+ `<WORKBOOK_BOOK_ROOT>/InDesign/<eBook stem>_Print7x10.pdf` if the book ships print] (InDesign files stay in `<WORKBOOK_INDESIGN_ROOT>`)
- [ ] Only <AUTHOR>-selected sub-exercises are in the workbook (`_Pipeline/WORKBOOK_SELECTION.md`; registry `subExercises` / `notSelected`)
- [ ] Workbook PDF = DOCX = MD (latest WorkbookQA report, after the W3 sync)
- [ ] Workbook print QA (v3.4; only if the profile ships print, otherwise N/A): latest `_BookGovernance/PrintQA/Workbook_<eBook stem>_PrintQA.md` for each of this chapter's exercises is newer than both PDFs, shows **0** text differences to check and **0** layout errors, and every warning is fixed, logged as print-only, or accepted by <AUTHOR>
- [ ] Latest `Governance/<ChapterName>_WorkbookQA_<timestamp>.md` has no open blocking items
- [ ] `Workbook/Trigger/WORKBOOK_READY.md` present, and newer than any PHASE 4 Part 0 sync that flagged the workbook
- [ ] This chapter's exercises are in `_BookGovernance/Workbook/Workbook_ExerciseRegistry.json`, and every manuscript mention matches

## PHASE 3.5 — Design QA

- [ ] Latest `DesignQA_<timestamp>.md` certifies **Production Ready**
- [ ] No Critical issues; accepted Major issues listed
- [ ] `DESIGN_READY.md` present

## PHASE 4 — Kindle

- [ ] PHASE 3.5 completed: final eBook PDF uploaded; `DESIGN_READY.md` present (from PHASE 3.5, or attested by the upload)
- [ ] Part 0: manuscript MD and DOCX synced to the final eBook PDF (`Manuscript/Trigger/MANUSCRIPT_SYNCED.md` newer than the PDF); sync report reviewed
- [ ] Part 0G: glossary locked; the chapter is in the official `_BookGovernance/Glossary/Master_Glossary`; no open drift for it in `Glossary_DriftReport.md`
- [ ] Part 0 follow-ups closed: every "must fix before release" item in the downstream impact list (pull quotes, voice samples, claims, narration) is fixed; deferred items listed here
- [ ] Part 0 print cross-check recorded, citing the 0P report (print-only differences confirmed by <AUTHOR> and logged in `<ChapterName>_PrintOnlyDifferences.md`)
- [ ] Part 0P: print PDF uploaded to `InDesign/<ChapterName>_Print7x10.pdf` (7×10, printer's marks and bleed)
- [ ] Part 0P: latest `_BookGovernance/PrintQA/<ChapterName>_PrintQA.md` is newer than both the print and eBook PDFs, and shows **0** text differences to check and **0** layout errors
- [ ] Part 0P: every minor text difference and layout warning reviewed, and each one fixed, logged as print-only, or accepted by <AUTHOR> (acceptance written beside this item)
- [ ] Step 0 dependency check passed (figures exported, manual print/eBook work finished)
- [ ] `<ChapterName>_Kindle.docx` · `_Kindle.html` · `_KindleMetadata.json` · `Kindle/figures/`
- [ ] Every figure is a real image (no placeholders, or an approval is recorded)
- [ ] Build profile recorded; no draft marketing seeds included
- [ ] Part 0 step 0.7 audit spot check recorded; no blocking finding open
- [ ] Part C: narration script built from the Kindle output; final narration recorded by <AUTHOR> (Adobe Audition), not an XTTS draft; coverage and technical-spec checks recorded; pronunciation reviewed; no stale passages
- [ ] PHASE 4 Part A checklist `gateStatus: PASS`
- [ ] Part B book assembly: this chapter appears in `<BOOK>_Kindle.docx` at the correct version and reading position

## PHASE 5 — RAG (Local + Cloud) & LLM

- [ ] `RAG_Ingestion.json` + `Chunks/` · `Index/` manifests · `RAG_ValidationReport.md` · `LLM_SystemPrompt.md` · `RAG_QueryProfiles.md`
- [ ] Local: ChromaDB `<RAG_COLLECTION>` updated for this chapter; smoke test passed; `RAG_LOCAL_READY.md` present
- [ ] Cloud: Blob `<RAG_BLOB_CONTAINER>` `current.json` points at this chapter's current vector file (`text-embedding-3-large`); smoke test and multilingual smoke test passed; `RAG_CLOUD_READY.md` present (or cloud track disabled in `RAG_Config.json`)
- [ ] Parity: both indexes built from the same chunk set (same hash and chapter version)
- [ ] `RAG_READY.md` present

## PHASE 6 — Automation

- [ ] Chapter in `AutomationIndex.json` with `automationStatus: active`
- [ ] n8n workflows exported to `_BookAutomation/n8n/`
- [ ] OpenClaw pipelines defined in `_BookAutomation/OpenClaw/`
- [ ] ActivationReport: Tests 1–5 passed (including the approval rule)
- [ ] CMS / LMS imports staged as drafts (if in scope)

## PHASE 6.5 — Publication QA

- [ ] Latest `PublicationQA_<timestamp>.md` certifies **Publishing Ready**
- [ ] Sub-certifications: EPUB · Kindle · Print · Audiobook · Workbook · RAG (Local) · RAG (Cloud / N/A)
- [ ] Kindle package confirmed ready for KDP upload (`_BookPublication/<BOOK>_KINDLE_EBOOK/<BOOK>_Kindle.docx`)

## Book-level deliverables (tick when this chapter is included in the assembled build)

- [ ] <BOOK>_EBOOK (PDF & EPUB)
- [ ] <BOOK>_WORKBOOK_EBOOK (PDF; PHASE 3W W4)
- [ ] <BOOK>_PRINT_BOOK (manual InDesign)
- [ ] <BOOK>_WORKBOOK_PRINT_BOOK (full-color print PDF; manual InDesign, PHASE 3W W4)
- [ ] <BOOK>_AUDIOBOOK (PHASE 4 Part B)
- [ ] <BOOK>_KINDLE_EBOOK (PHASE 4 Part B)
- [ ] Book-wide audit: `_BookGovernance/Audit/Trigger/AUDIT_FINAL_CLEAR.md` present, and this chapter's final wording was part of that run (PHASE 0.9 Mode D)

---

## Chapter folder audit

```
<BOOK_ROOT>/Chapters/<ChapterName>/
├── Final/
│   ├── Manuscript/        ├── ReviewPacket/     ├── Workbook/
│   ├── Training/          ├── ReferenceGuides/  ├── Slides/
│   ├── Equations/         ├── eBook/            ├── Kindle/ (figures/)
│   ├── InDesign/          ├── Audiobook/        ├── RAG/ (Chunks/, Index/, Trigger/)
│   ├── Marketing/ (Intake/, Seeds/, Trigger/, Generated/)
│   ├── Governance/ (Trigger/, _Backups/)
│   └── DesignPacket/ (_ds/, packet/, figures_export/, templates/, uploads/, Trigger/)
└── Published/
```

- [ ] All `Final/` folders present and populated (or documented not-applicable)
- [ ] `Published/` created

## Final published package (`Chapters/<ChapterName>/Published/`)

Copies of the approved release versions only:
- [ ] Final Manuscript · Workbook (manuscript DOCX + MD, eBook + print PDFs) · Training Guide · Slides (PPTX/PDF) · Reference Guides · eBook (PDF/EPUB) · Kindle DOCX · Audio · Metadata · Manifest

## Archive (`<BOOK_ROOT>/_Archive/<ChapterName>/`)

Move (never delete) working material:
- [ ] PASS 7 drafts · HTML drafts · superseded QA reports · `Marketing/Generated/` drafts not approved · working notes

## Master asset updates

- [ ] Master Glossary (`_BookGovernance/Glossary/Master_Glossary`) includes this chapter (done automatically in PHASE 4 0G); back-matter glossary updated from `Glossary_DriftReport.md` (<AUTHOR>)
- [ ] Master Figure Registry updated
- [ ] Global metadata catalog updated
- [ ] Master Chapter Catalog updated
- [ ] VersionMetadata incremented; ArtifactManifest updated

---

# PART B — LLM RECOMMENDATIONS (drafted by the local LLM from the unmet checks, before sign-off)

| # | Area | Observation (with evidence path) | Recommendation | Risk if ignored | <AUTHOR> decision (Accept / Defer / Reject) |
|---|---|---|---|---|---|
| 1 | | | | | |

Also state:
- Open items carried into the next edition
- Anything Claude could not verify, and why

---

# PART C — HUMAN SIGN-OFF (<AUTHOR>)

## Release approvals
- [ ] Content Approved
- [ ] Governance Approved
- [ ] Design Approved
- [ ] Accessibility Approved
- [ ] Kindle Approved
- [ ] Print Approved (PHASE 4 Part 0P report closed; print-only differences logged)
- [ ] Audio Approved
- [ ] Workbook Approved (eBook + print PDFs; PDF = DOCX = MD)
- [ ] References / Bibliography Approved
- [ ] Glossary Approved (defining-chapter definitions; back-matter glossary updated)
- [ ] RAG Approved
- [ ] Automation Approved (drafts-only rule verified)
- [ ] Archive Complete
- [ ] Part B recommendations decided

## Chapter status (choose one)
- [ ] Publishing Ready (hold)
- [ ] **Published**

**Chapter:** _______________________
**Version:** _______________________
**Date:** _______________________
**Signed:** <AUTHOR> _______________________

---

# Completion rule

The chapter is **Published** only when:

✅ PHASES 1, 2, 3, 3.5, 4, 5, 6, and 6.5 have passed their exit gates
✅ The workbook is settled per the book's workbook profile (PHASE 3W W2): a current `WORKBOOK_READY.md` whose recorded hashes match the uploaded PDFs (in `Workbook/` or `<WORKBOOK_BOOK_ROOT>`, only the profile's formats), **or** `WORKBOOK_NOT_APPLICABLE.md` for a book without a workbook
✅ References: no open critical or major finding in `_BookGovernance/References/<ChapterName>_ReferencesCheck.md` (PHASE 4 0R lets Kindle proceed with open findings; publication does not)
✅ Print QA: the latest PHASE 4 Part 0P report is newer than both PDFs, with no text difference to check and no layout error open, and every warning fixed or accepted by <AUTHOR>
✅ Every Part A item is ticked, or is unticked with <AUTHOR>'s written acceptance beside it
✅ The published package exists
✅ The archive package exists
✅ Master metadata is updated
✅ Knowledge systems are updated
✅ Part B recommendations have a decision
✅ <AUTHOR>'s sign-off is recorded

**Only then may the chapter be marked COMPLETE.**
