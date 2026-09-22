# PHASE 7: Chapter Publishing & Release Checklist (v3)

## Final Validation, LLM Recommendations, and Human Sign-off

> **Pipeline position:** PHASE 7 of 7 (Release) · **Upstream gate:** latest PHASE 6.5 report certifies **Publishing Ready** · **Downstream:** none (chapter becomes **Published**)
> **Canonical paths, status ladder, triggers, and deliverables:** see `MASTER_PIPELINE_OVERVIEW.md`.

**v3 changes (2026-09-22 pipeline alignment):**
- Retitled from "PHASE 6". The internal phase sections now match the real phases (1, 2, 3, 3.5, 4, 5, 6, 6.5) instead of the old 1–6 numbering ("Local AI Pipeline", "Copilot Publishing").
- Absorbs the superseded stub `PHASE 4- Local LLM AI and Human Publishing Checklist.md` (editorial review, publishing prep, knowledge systems, version control).
- Adds Marketing, eBook, DesignPacket, triggers, and all book-level deliverables to the verification.
- Adds Part B, "LLM Recommendations", which Claude completes **before** <AUTHOR> signs.
- Folder audit matches the canonical `Final/` structure; the Published, Archive, and Finalized Releases paths are defined.

---

## How to use

1. Claude copies this template to `<CH_ROOT>/<ChapterName>_PHASE7_ReleaseChecklist.md` and pre-fills Part A (evidence: file paths, report names, gate statuses) and Part B (recommendations).
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

# PART A — VALIDATION OF OUTPUTS (Claude pre-fills evidence; <AUTHOR> confirms)

## PHASE 1 — Content Production

### Review Packet
- [ ] Chapter Summary · Key Takeaways · Glossary Terms · Definitions · Frameworks · Metadata JSON

### Workbook Packet
- [ ] Primary Exercise · Additional Exercises · Reflection Questions · Application Questions · Workbook DOCX

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
- [ ] Exports: Slides PPTX + PDF · eBook PDF + EPUB · Workbook eBook PDF
- [ ] InDesign print files (manual) present
- [ ] Audiobook MP3 rendered (XTTS) and pronunciation reviewed

## PHASE 3.5 — Design QA

- [ ] Latest `DesignQA_<timestamp>.md` certifies **Production Ready**
- [ ] No Critical issues; accepted Major issues listed
- [ ] `DESIGN_READY.md` present

## PHASE 4 — Kindle

- [ ] Step 0 dependency check passed (figures exported, manual print/eBook work finished)
- [ ] `<ChapterName>_Kindle.docx` · `_Kindle.html` · `_KindleMetadata.json` · `Kindle/figures/`
- [ ] Every figure is a real image (no placeholders, or an approval is recorded)
- [ ] Build profile recorded; no draft marketing seeds included
- [ ] PHASE 4 Part A checklist `gateStatus: PASS`
- [ ] Part B book assembly: this chapter appears in `<BOOK>_Kindle.docx` at the correct version and reading position

## PHASE 5 — RAG & Local LLM

- [ ] `RAG_Ingestion.json` + `Chunks/` · `RAG_ValidationReport.md` · `LLM_SystemPrompt.md` · `RAG_QueryProfiles.md`
- [ ] ChromaDB `<RAG_COLLECTION>` updated for this chapter; retrieval smoke test passed
- [ ] `RAG_READY.md` present

## PHASE 6 — Automation

- [ ] Chapter in `AutomationIndex.json` with `automationStatus: active`
- [ ] n8n workflows exported to `_BookAutomation/n8n/`
- [ ] OpenClaw pipelines defined in `_BookAutomation/OpenClaw/`
- [ ] ActivationReport: Tests 1–5 passed (including the approval rule)
- [ ] CMS / LMS imports staged as drafts (if in scope)

## PHASE 6.5 — Publication QA

- [ ] Latest `PublicationQA_<timestamp>.md` certifies **Publishing Ready**
- [ ] Sub-certifications: EPUB · Kindle · Print · Audiobook · RAG
- [ ] Kindle package confirmed ready for KDP upload (`_BookPublication/<BOOK>_KINDLE_EBOOK/<BOOK>_Kindle.docx`)

## Book-level deliverables (tick when this chapter is included in the assembled build)

- [ ] <BOOK>_EBOOK (PDF & EPUB)
- [ ] <BOOK>_WORKBOOK_EBOOK
- [ ] <BOOK>_PRINT_BOOK (manual InDesign)
- [ ] <BOOK>_WORKBOOK_PRINT_BOOK (manual InDesign)
- [ ] <BOOK>_AUDIOBOOK
- [ ] <BOOK>_KINDLE_EBOOK (PHASE 4 Part B)

---

## Chapter folder audit

```
<BOOK_ROOT>/Chapters/<ChapterName>/
├── Final/
│   ├── Manuscript/        ├── ReviewPacket/     ├── Workbook/
│   ├── Training/          ├── ReferenceGuides/  ├── Slides/
│   ├── Equations/         ├── eBook/            ├── Kindle/ (figures/)
│   ├── InDesign/          ├── Audiobook/        ├── RAG/ (Chunks/, Trigger/)
│   ├── Marketing/ (Intake/, Seeds/, Trigger/, Generated/)
│   ├── Governance/ (Trigger/, _Backups/)
│   └── DesignPacket/ (_ds/, packet/, figures_export/, templates/, uploads/, Trigger/)
└── Published/
```

- [ ] All `Final/` folders present and populated (or documented not-applicable)
- [ ] `Published/` created

## Final published package (`Chapters/<ChapterName>/Published/`)

Copies of the approved release versions only:
- [ ] Final Manuscript · Workbook · Training Guide · Slides (PPTX/PDF) · Reference Guides · eBook (PDF/EPUB) · Kindle DOCX · Audio · Metadata · Manifest

## Archive (`<BOOK_ROOT>/_Archive/<ChapterName>/`)

Move (never delete) working material:
- [ ] PASS 7 drafts · HTML drafts · superseded QA reports · `Marketing/Generated/` drafts not approved · working notes

## Master asset updates

- [ ] Master Glossary (`_BookGovernance/`) updated
- [ ] Master Figure Registry updated
- [ ] Global metadata catalog updated
- [ ] Master Chapter Catalog updated
- [ ] VersionMetadata incremented; ArtifactManifest updated

---

# PART B — LLM RECOMMENDATIONS (Claude completes before sign-off)

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
- [ ] Audio Approved
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
✅ The published package exists
✅ The archive package exists
✅ Master metadata is updated
✅ Knowledge systems are updated
✅ Part B recommendations have a decision
✅ <AUTHOR>'s sign-off is recorded

**Only then may the chapter be marked COMPLETE.**
