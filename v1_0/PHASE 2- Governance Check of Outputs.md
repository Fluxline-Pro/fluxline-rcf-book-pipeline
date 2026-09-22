# PHASE 2: GOVERNANCE CHECK + AUTO-REMEDIATION (v3)

> **Pipeline position:** PHASE 2 of 7 (Governance) · **Upstream gate:** PHASE 1 Exit Gate passed · **Downstream:** PHASE 3 Claude Design
> **Canonical paths, status ladder, triggers, and deliverables:** see `MASTER_PIPELINE_OVERVIEW.md`.

**v3 changes (2026-09-22 pipeline alignment):**
- Paths moved to the canonical chapter root `<BOOK_ROOT>/Chapters/<ChapterName>/Final/` (`<CH_ROOT>`).
- Adds the `/eBook/` prep files to the inputs and validations.
- Certification now uses the pipeline-wide status ladder; PHASE 2 may certify up to **Design Ready** only.
- NEW: Design Handoff staging into `/DesignPacket/uploads/` and a `GOVERNANCE_READY.md` trigger (consumed by PHASE 3 and PHASE 6).
- Batch Mode report moved to the book-level `/_BookGovernance/` folder (sibling of `/_BookMarketing/`).
- File-naming checks now catch non-standard prefixes (e.g. `Chapter5_`, `TheWindowOfChoice_`).


# POST-PASS7 PUBLISHING PIPELINE STANDARDIZATION PROMPT
## Chapter Production Governance, Metadata, Validation, Fixing, and Design Handoff

**v2 changes:**
- The prompt now **detects AND fixes** issues (previously report-only), under a tiered remediation policy with backups, a fix log, and re-validation.
- Adds validation of the new `/Marketing/` packet from Phase 1 (Step 11).
- Adds a Source-of-Truth Hierarchy, a Manuscript Change Proposals file (the manuscript is never edited here), and a Batch Mode for Chapters 1–5 with a cross-chapter consistency report.
- Production Readiness, Packaging Audit, Manifest, and Certification updated to include Marketing.

---

# PURPOSE

You are operating on a chapter that has already completed the PASS 7 manuscript workflow and has had all primary production artifacts generated.
Your responsibility is NOT to recreate existing artifacts.
Your responsibility is to perform publication governance, validation, metadata creation, standardization, **correction of defects you find**, production readiness review, and downstream asset preparation.
Use all previously generated chapter outputs as source material.

---

# SOURCE-OF-TRUTH HIERARCHY

When artifacts disagree, resolve conflicts in this order:

1. **PASS 7 Manuscript** (locked; highest authority)
2. **Normalized Glossary** (`<ChapterName>_GlossaryNormalized.json`)
3. **Learning Metadata and Figure Registry**
4. **All derived artifacts** (Review Packet, Workbook, Training, Reference Guides, Slides, Equation Sheet, Kindle, InDesign, Audiobook, RAG, Marketing)

Derived artifacts are corrected to match higher-ranked sources, never the reverse.

---

# GLOBAL STANDARDIZATION RULE

All chapter artifacts must represent a single authoritative source of truth.

When concepts, terminology, frameworks, glossary entries, definitions, examples, or learning objectives appear in multiple artifacts, they must remain semantically consistent.

Do not rewrite concepts differently across:

- Manuscript
- Review Packet
- Workbook
- Training Materials
- Reference Guides
- Slide Decks
- Audiobook Files
- Kindle Files
- InDesign Files
- RAG Files
- Marketing Files
- Future LMS Assets

Differences are allowed only when required by the delivery format.

---

# INPUTS

Use:

- PASS 7 Chapter Manuscript
- Review Packet
- Workbook Packet
- Training Materials
- One-Page References
- Slide Deck Outline
- Equation Sheet (if present)
- eBook Prep Assets (`/eBook/`: HTML blocks, eBook metadata, TOC)
- Kindle Assets (legacy PHASE 1 files only, if present; PHASE 4 owns `/Kindle/`)
- InDesign Assets
- Audiobook Assets
- RAG Assets
- **Marketing & Local LLM Intake Packet** (`/Marketing/Intake/`, `/Marketing/Seeds/`, `/Marketing/Trigger/`)

as the authoritative chapter ecosystem.

---

# OUTPUT LOCATION

Save all outputs into:

```text
<BOOK_ROOT>/Chapters/<ChapterName>/Final/Governance/
```

If the folder does not exist:

Create it.

---

# REMEDIATION POLICY (NEW)

Every issue you find is classified into one of three tiers.

## Tier A: Fix automatically, then log

Apply the fix directly to the affected file:

- JSON schema errors, missing metadata fields, or malformed frontmatter
- Manifest mismatches (files listed but missing, or present but unlisted)
- File naming violations (`<ChapterName>_<ArtifactType>.<ext>`, where `<ChapterName>` = `Ch<N>_<PascalCaseTitle>`) and missing required folders. Exception: Claude Design project files in `/DesignPacket/` (`*.dc.html`) keep the names Claude Design assigns; list them in the manifest instead of renaming.
- Broken, missing, or duplicate cross-references inside derived artifacts
- Terminology drift in derived artifacts (align to manuscript and glossary)
- Duplicate or conflicting glossary entries; missing "References: Ch N" markers
- RAG chunking violations (re-chunk to 500–1000 words with 100-word overlap; keep section names as metadata; never split a concept mid-explanation)
- Audiobook script text that differs from the manuscript (sync to the manuscript; pronunciation guides and segment markers stay intact)
- Missing semantic structure, callout boundaries, component boundaries, or visual placeholders in Slides, Workbook, Training, and One-Pagers (add structure without changing meaning)
- **Marketing packet defects:** non-verbatim pull-lines (replace with exact manuscript text), claims outside the ClaimsRegistry (remove or rewrite to a supported claim), forbidden claims (outcome promises, medical or therapeutic claims, invented stats, testimonials, credentials), missing frontmatter, terminology not matching the TerminologyLock, ChapterContext over 2,000 words (compress), and missing required Marketing files (generate them from the manuscript)

## Tier B: Fix, then flag "Needs Author Review"

Apply the most conservative fix, but mark it in the log for my review:

- Definitions that differ across artifacts where the manuscript itself is ambiguous
- Substantive changes to workbook exercises or reflection prompts
- Equation Sheet corrections (always check against the manuscript's fixed equations and scoring scales; never alter a scale)
- Any fix that changes the meaning, emphasis, or teaching intent of a passage

## Tier C: Never change; propose only

Record in `<ChapterName>_ManuscriptChangeProposals.md` and do not edit:

- The PASS 7 manuscript text
- Footnotes and bibliography
- Author-stated framework decisions, terminology decisions, or fixed scoring rubrics
- Anything where fixing would require choosing between two defensible authorial intentions

For each proposal give: location, the issue, a suggested wording, and why. Voice must be preserved in any suggested wording.

---

# SAFETY RULES FOR FIXING (NEW)

1. **Back up before editing.** Before modifying any file, copy the original into `/Governance/_Backups/<YYYYMMDD_HHMM>/` preserving its relative path.
2. **Never delete** any file. If a file is obsolete, list it in the log for my decision.
3. **Edit in place** and keep original filenames. Increment the artifact version in the manifest.
4. **Smallest effective change.** Fix the defect and leave surrounding content alone.
5. **When in doubt, escalate a tier** (A → B → C).
6. **Every change is logged** in the Remediation Log.

---

# WORKFLOW (NEW)

Run in this order:

1. **Detect:** perform all validations below.
2. **Classify:** assign each issue an ID, severity (Critical / Major / Minor), and tier (A / B / C).
3. **Back up** the files to be changed.
4. **Fix** Tier A and Tier B items; write Tier C items to the proposals file.
5. **Log** every change in the Remediation Log.
6. **Re-validate:** re-run the affected checks on the corrected files. Perform at most **2 fix passes**. Anything still failing goes to Outstanding Issues.
7. **Certify:** produce the reports and certification based on the post-fix state.

---

# ARTIFACT MANIFEST

Create:

```text
<ChapterName>_ArtifactManifest.json
```

Include:

```json
{
  "chapterName": "",
  "chapterNumber": "",
  "sourceManuscript": "",
  "createdDate": "",
  "artifacts": [
    {
      "artifactType": "",
      "fileName": "",
      "filePath": "",
      "format": "",
      "version": "",
      "status": "",
      "dependencies": []
    }
  ]
}
```

Track:

- Artifact Type
- Filename
- Extension
- Folder Path
- Version
- Completion Status
- Dependencies

**Include every file in `/Marketing/`** (Intake, Seeds, Trigger).

This file serves as the master registry for all chapter assets. Fix any mismatch between the manifest and the actual files.

---

# CROSS-REFERENCE VALIDATION REPORT

Create:

```text
<ChapterName>_CrossReferenceReport.md
```

Validate all:

- Chapter references
- Section references
- Figure references
- Sidebar references
- Glossary references
- Appendix references
- Workbook references

Identify:

- Broken references
- Missing references
- Duplicate references
- Inconsistent references

Fix Tier A items in derived artifacts. Record any manuscript-side reference or footnote issue in the Manuscript Change Proposals. List what was fixed and what remains.

---

# FIGURE REGISTRY

Create:

```text
<ChapterName>_FigureRegistry.json
```

For every proposed or existing figure:

```json
{
  "figureId": "",
  "title": "",
  "description": "",
  "figureType": "",
  "complexity": "",
  "relatedTopics": [],
  "relatedGlossaryTerms": [],
  "designNotes": ""
}
```

Figure types may include:

- Infographic
- Process Flow
- Diagram
- Concept Model
- Comparison Chart
- Decision Tree
- Framework Visualization
- Data Illustration

Reconcile figure references across InDesign, Slides, and Reference Guides so numbering and titles match.

---

# LEARNING METADATA

Create:

```text
<ChapterName>_LearningMetadata.json
```

Include:

```json
{
  "learningObjectives": [],
  "bloomTaxonomyLevel": [],
  "difficulty": "",
  "estimatedCompletionTime": "",
  "prerequisiteChapters": [],
  "knowledgeDomains": [],
  "skillsDeveloped": [],
  "instructionalModality": []
}
```

Use instructional design best practices. Where Workbook, Training, or Slide objectives do not match these objectives, align the derived artifacts to the learning objectives (Tier A, or Tier B if the wording changes teaching intent).

---

# GLOSSARY NORMALIZATION PACKET

Create:

```text
<ChapterName>_GlossaryNormalized.json
```

For every glossary term:

```json
{
  "term": "",
  "definition": "",
  "chapter": "",
  "aliases": [],
  "relatedTerms": []
}
```

Requirements:

- Eliminate duplicate definitions.
- Normalize terminology.
- Maintain consistency across all artifacts.
- **Compare against the `<ChapterName>_GlossaryNormalized.json` files of previously processed chapters** (sibling folders under `/Chapters/`) and resolve or flag conflicts.
- Mark each term with its chapter reference (References: Ch N).

---

# DESIGN HANDOFF PACKET

Create:

```text
<ChapterName>_DesignHandoff.md
```

For future Claude Design processing.

Include:

**Staging:** after writing this file, copy it together with `FigureRegistry.json`, `GlossaryNormalized.json`, `LearningMetadata.json`, and `HTMLReadinessReport.md`, plus the Manuscript, ReviewPacket, Workbook, Training, ReferenceGuides, SlideDeck, and InDesign Markdown, into `<CH_ROOT>/DesignPacket/uploads/`. Claude Design (PHASE 3) reads only from that folder. The Governance copies remain the source of truth.

## Chapter Theme

Primary chapter message.

---

## Key Concepts

Major concepts requiring visual support.

---

## Visual Metaphors

Suggested metaphorical approaches.

---

## Suggested Infographics

Potential infographic concepts.

---

## Suggested Illustrations

Illustration opportunities.

---

## Process Diagrams

Workflow opportunities.

---

## Pull Quote Candidates

Most visually impactful quotes (verbatim from the manuscript).

---

## Chapter Opening Concepts

Hero page suggestions.

---

## Chapter Closing Concepts

Summary page suggestions.

---

## Figure Prioritization

Rank figures by importance.

---

# HTML TRANSFORMATION READINESS

Create:

```text
<ChapterName>_HTMLReadinessReport.md
```

Evaluate whether existing:

- Slides
- Workbook
- Training Materials
- One-Pagers
- Job Aids

are optimized for future HTML conversion.

Identify:

- Missing semantic structure
- Weak content hierarchy
- Missing callout types
- Missing component boundaries
- Missing visual placeholders

**Fix these directly** in the source Markdown or outline files (Tier A), keeping meaning unchanged, and record what was changed.

---

# SEMANTIC CHUNKING VALIDATION

Create:

```text
<ChapterName>_ChunkingValidation.md
```

Review RAG outputs.

Validate:

- Concept boundaries
- Learning objective boundaries
- Section boundaries

Chunk requirements:

- Preferred chunk size: 500–1000 words
- Recommended overlap: 100 words
- Preserve section names as metadata

Do not split concepts mid-explanation.

**Re-chunk any non-compliant output** (Tier A) and report before/after chunk counts.

---

# MARKETING INTAKE VALIDATION (NEW)

Create:

```text
<ChapterName>_MarketingIntakeValidation.md
```

Validate the `/Marketing/` packet against these checks, and fix failures under the Tier A policy:

1. **Completeness:** all 6 Intake files and all required Seed files exist (LeadMagnetCandidate may be a one-line "none fits" note).
2. **Frontmatter:** present and complete on every file, with `status: draft`.
3. **Verbatim check:** every pull-line and verbatim support quote matches the manuscript exactly. Report the count checked and the count corrected.
4. **Claims discipline:** every claim in the Seeds traces to the ClaimsRegistry or a verbatim manuscript line. No outcome promises, medical or therapeutic claims, invented statistics, testimonials, reviews, credentials, or endorsements.
5. **Terminology:** all framework terms match `TerminologyLock.json` and the manuscript's exact casing. Scoring scales and equations appear only verbatim.
6. **Local-LLM fitness:** `ChapterContext.md` is 2,000 words or fewer; each Intake file is usable standalone within an 8k context window; the Intake set stays within roughly 6,000 words.
7. **Voice:** flag content containing corporate softening, filler, generic self-help phrasing, or over-explanation, and rewrite in the voice shown in `VoiceNotes.md`.
8. **Length limits:** pull-lines under 40 words each; no large reproduction of the chapter in any marketing asset.
9. **Audiobook teasers:** segment references match the Audiobook prep files.
10. **Trigger file:** `MARKETING_READY.md` exists only if all checks above pass. If checks still fail after 2 fix passes, replace it with `MARKETING_INCOMPLETE.md` listing the open items. Never leave a stale `MARKETING_READY.md`.

---

# VERSION CONTROL METADATA

Create:

```text
<ChapterName>_VersionMetadata.json
```

Structure:

```json
{
  "edition": "",
  "chapterVersion": "",
  "sourceVersion": "",
  "revisionDate": "",
  "reviewDate": "",
  "reviewerNotes": [],
  "majorChanges": []
}
```

Prepare the chapter for future edition tracking. Record the governance fixes applied in `majorChanges`.

---

# TERMINOLOGY CONSISTENCY AUDIT

Create:

```text
<ChapterName>_TerminologyAudit.md
```

Review all generated artifacts, including Marketing.

Identify:

- Term variations
- Conflicting definitions
- Duplicate frameworks
- Inconsistent naming patterns
- Different explanations of identical concepts

Recommend standardized wording, then **apply it to derived artifacts** (Tier A/B). Standardization always follows the manuscript.

---

# REMEDIATION LOG (NEW)

Create:

```text
<ChapterName>_RemediationLog.md
```

For every issue found:

| Issue ID | Severity | Tier | Artifact / Location | Problem | Fix Applied (before → after) | Status |
|---|---|---|---|---|---|---|

Statuses: `Fixed`, `Fixed – Needs Author Review`, `Proposed (Tier C)`, `Open`.

Also include:
- Backup folder path
- Total issues found, fixed, flagged, and open
- Results of each re-validation pass

---

# MANUSCRIPT CHANGE PROPOSALS (NEW)

Create:

```text
<ChapterName>_ManuscriptChangeProposals.md
```

All Tier C items: manuscript wording, footnotes, bibliography, and authorial-intent conflicts. **Do not edit the manuscript.** Each entry gives location, issue, suggested wording (voice-preserving), and rationale. If there are none, state that explicitly.

---

# PRODUCTION READINESS REPORT

Create:

```text
<ChapterName>_ProductionReadinessReport.md
```

Score each category from:

```text
1 = Major Work Required
2 = Significant Gaps
3 = Adequate
4 = Strong
5 = Production Ready
```

Categories:

- Manuscript Quality
- Editorial Readiness
- Technical Accuracy
- Learning Quality
- Training Readiness
- Workbook Readiness
- Slide Readiness
- Kindle Readiness
- InDesign Readiness
- Audiobook Readiness
- Accessibility Readiness
- HTML Transformation Readiness
- RAG Readiness
- **Marketing Intake Readiness (NEW)**
- **Local LLM Readiness (NEW)** (context size, structure, grounding quality)
- Metadata Completeness
- Publishing Readiness

Provide rationale for every score.
Report scores **before and after** remediation.
Provide recommendations for any score below 5.

---

# CHAPTER PACKAGING AUDIT

Create:

```text
<ChapterName>_PackagingAudit.md
```

Verify:

- Required folders exist, per the PHASE 1 Step 13 map, including `/eBook/`, `/Kindle/`, `/Governance/`, `/DesignPacket/`, `/Marketing/Intake/`, `/Marketing/Seeds/`, and `/Marketing/Trigger/`
- Chapter content sits under `/Chapters/<ChapterName>/Final/` (flag chapters whose folders sit directly under `/Chapters/<ChapterName>/` as a Major packaging issue; Tier C proposal, since moving folders is <AUTHOR>'s call)
- Required files exist
- File naming conventions comply
- Metadata files exist
- References are valid

List:

## Complete

Items successfully generated.

## Missing

Required items not found (and whether they were generated during remediation).

## Recommended

Optional assets worth creating.

---

# ENTERPRISE CONTENT GOVERNANCE CHECK

Review chapter outputs for:

- Consistency
- Reusability
- AI-readiness
- Searchability
- Future LMS integration
- Future CMS integration
- Future knowledge base usage
- Future RAG ingestion
- Future web publication
- Future marketing automation (local LLM / n8n intake)

Generate:

```text
<ChapterName>_GovernanceAssessment.md
```

---

# MASTER CHAPTER CERTIFICATION REPORT

Create:

```text
<ChapterName>_ChapterCertification.md
```

Include:

## Executive Summary

---

## Production Status

---

## Artifact Inventory

---

## Metadata Inventory

---

## Readiness Scores (before and after remediation)

---

## Remediation Summary

Counts of issues found, fixed, flagged for author review, proposed, and open.

---

## Outstanding Issues

---

## Recommended Next Actions

---

## Certification Statement

Use the pipeline-wide status ladder:

`Draft → Review Ready → Design Ready → Production Ready → Publishing Ready → Published`

PHASE 2 may certify **Draft**, **Review Ready**, or **Design Ready** (the entry gate for PHASE 3). Higher levels are awarded by later gates: Production Ready by PHASE 3.5, Publishing Ready by PHASE 6.5, Published by <AUTHOR> in PHASE 7.

**A chapter may not be certified Design Ready while any Critical issue is open or any `Needs Author Review` item is unresolved.** In those cases, certify at the highest level the evidence supports and list what blocks the next level.

---

# GOVERNANCE TRIGGER (NEW)

After certification:

- If the chapter is certified **Design Ready**, create `<CH_ROOT>/Governance/Trigger/GOVERNANCE_READY.md` listing the certification level, the date, the manifest version, and the Design Handoff staging confirmation.
- Otherwise create `GOVERNANCE_INCOMPLETE.md` in the same folder listing the blockers, and remove nothing else. Never leave a stale `GOVERNANCE_READY.md`: if one exists from an earlier run and this run does not certify Design Ready, rename the old one to `GOVERNANCE_READY_superseded_<YYYYMMDD_HHMM>.md`.

PHASE 3 does not start without `GOVERNANCE_READY.md`.

---

# BATCH MODE: CHAPTERS 1–5 (NEW)

When running multiple chapters:

1. Process one chapter at a time, in chapter order.
2. Carry the glossary forward, so each chapter is validated against the previous chapters' normalized glossaries.
3. After the last chapter, create:

```text
<BOOK_ROOT>/_BookGovernance/Ch<first>-<last>_CrossChapterConsistencyReport.md
```

covering:
- Glossary conflicts across chapters, and how they were resolved or flagged
- Terminology drift across chapters
- Forward and backward chapter references that do not resolve
- Marketing voice or claims inconsistencies across the chapters' Marketing packets
- A list of all `Needs Author Review` and Tier C items across the batch in one place

---

# FINAL RULE

Do not regenerate existing chapter assets unless required for consistency or to correct a defect under the Remediation Policy.

Focus on:

- Governance
- Standardization
- Validation
- **Correction, with backups and a full log**
- Metadata
- Readiness
- Reusability
- Future automation

The manuscript is never edited by this phase. The objective is to transform a completed PASS 7 chapter into a fully governed, searchable, design-ready, publishing-ready knowledge asset suitable for book production, training development, RAG systems, LMS deployment, web delivery, marketing automation, and future edition management.
