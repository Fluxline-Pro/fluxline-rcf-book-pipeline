# PHASE 6- RCF Chapter Publishing and Release Checklist

## Human Production Workflow (Post-Generation)

**Purpose:** This checklist is the final human-controlled quality gate before a chapter is considered complete, published, archived, and ready for long-term use.

### Instructions

Make a copy of this checklist and place it under “Finalized Releases” with the specific Chapter’s content being reviewed and added. This shows the Release is fully locked and ALL artifacts have been verified and went through all Phases of the process (PHASE 1-PHASE 5) including all checks and QA setup. 

---

# Chapter Information

| Item | Value |
| --- | --- |
| Chapter Number |  |
| Chapter Name |  |
| Version |  |
| Review Date |  |
| Status | Draft / Review Ready / Production Ready / Published |
| Reviewer |  |

---

# PHASE 1 — Content Production Verification

## PASS 7 Outputs

### Review Packet

- [ ]  Chapter Summary created
- [ ]  Key Takeaways included
- [ ]  Glossary Terms included
- [ ]  Definitions included
- [ ]  Frameworks identified
- [ ]  Metadata JSON included

### Workbook Packet

- [ ]  Primary Workbook Exercise included
- [ ]  Additional Exercises included
- [ ]  Reflection Questions included
- [ ]  Application Questions included
- [ ]  Workbook DOCX created

### Training Materials

- [ ]  Instructor Notes created
- [ ]  Teaching Objectives created
- [ ]  Facilitation Guide created
- [ ]  Discussion Questions created
- [ ]  Training Outline created

### Reference Guides

- [ ]  One-pager created for each major topic
- [ ]  Key Concepts included
- [ ]  Definitions included
- [ ]  Practical Checklists included
- [ ]  Visual descriptions included

### Slide Deck

- [ ]  Title Slide included
- [ ]  Slide count appropriate
- [ ]  Reflection slide included
- [ ]  Key concepts represented
- [ ]  Visual suggestions included
- [ ]  Speaker notes included

### Kindle Assets

- [ ]  EPUB HTML created
- [ ]  TOC entries created
- [ ]  Metadata created

### InDesign Assets

- [ ]  Layout notes created
- [ ]  Pull quotes selected
- [ ]  Sidebar summaries created
- [ ]  Figure suggestions created
- [ ]  Layout spread suggestions created

### Audiobook Assets

- [ ]  Narration script created
- [ ]  Pronunciation guide created
- [ ]  Segment markers added
- [ ]  Pacing notes added

### RAG Assets

- [ ]  Chunked text created
- [ ]  Metadata JSON created
- [ ]  Semantic tags created
- [ ]  Retrieval summaries created

---

# PHASE 2 — Governance Validation

## Artifact Manifest

- [ ]  ArtifactManifest.json exists
- [ ]  All generated files listed
- [ ]  Paths accurate
- [ ]  Versions recorded

## Cross Reference Audit

- [ ]  Chapter references validated
- [ ]  Figure references validated
- [ ]  Appendix references validated
- [ ]  Glossary references validated

## Figure Registry

- [ ]  FigureRegistry.json exists
- [ ]  Figures documented
- [ ]  Descriptions complete

## Learning Metadata

- [ ]  LearningMetadata.json exists
- [ ]  Objectives documented
- [ ]  Difficulty assigned
- [ ]  Estimated duration assigned

## Glossary Normalization

- [ ]  No duplicate definitions
- [ ]  Consistent terminology
- [ ]  Related term mapping completed

## Terminology Audit

- [ ]  No conflicting terminology
- [ ]  Consistent framework naming
- [ ]  Consistent concept naming

## Governance Assessment

- [ ]  Governance report reviewed
- [ ]  No critical findings
- [ ]  Remediation completed

## Chapter Certification

- [ ]  Status = Design Ready
- [ ]  Status = Production Ready

---

# PHASE 3 — Claude Design Review

## Design Inputs Provided

- [ ]  DSM provided
- [ ]  Design System Prompt provided
- [ ]  Design Handoff provided
- [ ]  Slide Deck Outline provided
- [ ]  Workbook provided
- [ ]  Training Materials provided
- [ ]  Reference Guides provided

## Design Deliverables Received

### HTML Slides

- [ ]  Complete
- [ ]  Styled correctly

### HTML Workbook

- [ ]  Complete
- [ ]  Styled correctly

### HTML Training Guide

- [ ]  Complete
- [ ]  Styled correctly

### HTML Reference Guides

- [ ]  Complete
- [ ]  Styled correctly

### Figure Layouts

- [ ]  Included

### Visual Specifications

- [ ]  Included

---

# PHASE 3.5 — Design QA

## Quality Review

- [ ]  DesignQA.md created
- [ ]  Reviewed manually

## DSM Compliance

- [ ]  No critical violations
- [ ]  Typography compliant
- [ ]  Colors compliant
- [ ]  Components compliant

## Accessibility

- [ ]  Semantic HTML present
- [ ]  Accessibility review passed
- [ ]  Responsive design passed

## Instructional Design

- [ ]  Learning objectives aligned
- [ ]  Activities aligned
- [ ]  Knowledge checks aligned

## HTML Review

- [ ]  Structure clean
- [ ]  Content hierarchy logical
- [ ]  Components reusable

## Design QA Status

- [ ]  Publishing Ready
- [ ]  Production Ready

---

# PHASE 4 — Local AI Pipeline

## ChromaDB

- [ ]  Chapter imported
- [ ]  Metadata imported
- [ ]  Retrieval tested

### Notes

---

---

---

## RAG

- [ ]  Embeddings generated
- [ ]  Search tested
- [ ]  Retrieval tested
- [ ]  Responses validated

### Notes

---

---

---

## XTTS

- [ ]  Narration generated
- [ ]  Pronunciation reviewed
- [ ]  Audio quality reviewed

### Notes

---

---

---

## Local LLM Testing

- [ ]  Chapter loaded
- [ ]  Reference guide loaded
- [ ]  Metadata loaded
- [ ]  Retrieval tested

### Notes

---

---

---

# PHASE 5 — Copilot Publishing

## Kindle DOCX

- [ ]  DOCX generated
- [ ]  Chapter formatting validated
- [ ]  Styles validated

## EPUB

- [ ]  EPUB generated
- [ ]  Navigation tested
- [ ]  TOC tested

## Final Export Validation

- [ ]  Headers correct
- [ ]  Images correct
- [ ]  Metadata correct
- [ ]  Links correct

---

# PHASE 6 — Release & Archive

## Chapter Folder Audit

Verify final structure:

/RCF/Chapters/<ChapterName>/

├── Manuscript/

├── ReviewPacket/

├── Workbook/

├── Training/

├── ReferenceGuides/

├── Slides/

├── Equations/

├── Kindle/

├── InDesign/

├── Audiobook/

├── RAG/

├── Governance/

└── Published/

### Folder Verification

- [ ]  Manuscript
- [ ]  ReviewPacket
- [ ]  Workbook
- [ ]  Training
- [ ]  ReferenceGuides
- [ ]  Slides
- [ ]  Equations
- [ ]  Kindle
- [ ]  InDesign
- [ ]  Audiobook
- [ ]  RAG
- [ ]  Governance
- [ ]  Published

---

## Final Published Package

### Files Verified

- [ ]  Final Manuscript
- [ ]  Workbook
- [ ]  Training Guide
- [ ]  Slides
- [ ]  Reference Guides
- [ ]  EPUB
- [ ]  Audio
- [ ]  Metadata
- [ ]  Manifest

### Published Folder Complete

- [ ]  Yes

---

## Archive Process

Move drafts to archive.

- [ ]  PASS7 Drafts archived
- [ ]  HTML Drafts archived
- [ ]  QA Drafts archived
- [ ]  Working Notes archived

Archive Path:

/RCF/Archive/<ChapterName>/

---

## Master Asset Updates

### Glossary

- [ ]  Master Glossary updated

### Figure Registry

- [ ]  Master Figure Registry updated

### Metadata Catalog

- [ ]  Global Metadata updated

### Chapter Index

- [ ]  Master Chapter Catalog updated

---

# Release Certification

## Final Verification

- [ ]  Content Approved
- [ ]  Governance Approved
- [ ]  Design Approved
- [ ]  Accessibility Approved
- [ ]  RAG Approved
- [ ]  Audio Approved
- [ ]  Kindle Approved
- [ ]  Archive Complete

---

# Chapter Status

Choose One:

- [ ]  Draft
- [ ]  Review Ready
- [ ]  Design Ready
- [ ]  Production Ready
- [ ]  Published

---

# Final Sign-Off

**Chapter:** _______________________

**Version:** _______________________

**Date:** _______________________

**Reviewer:** _______________________

**Signature/Approval:** _______________________

---

# Completion Rule

The chapter is considered **Published** only when:

✅ All six phases are complete

✅ Published package exists

✅ Archive package exists

✅ Metadata is updated

✅ Knowledge systems are updated

✅ Human review is completed

✅ Final sign-off is recorded

**Only then may the chapter be marked COMPLETE.**