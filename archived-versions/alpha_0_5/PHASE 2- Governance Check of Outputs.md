# PHASE 2: GOVERNANCE CHECK

# POST-PASS7 PUBLISHING PIPELINE STANDARDIZATION PROMPT
## Chapter Production Governance, Metadata, Validation, and Design Handoff

---

# PURPOSE

You are operating on a chapter that has already completed the PASS 7 manuscript workflow and has had all primary production artifacts generated.
Your responsibility is NOT to recreate existing artifacts.
Your responsibility is to perform publication governance, validation, metadata creation, standardization, production readiness review, and downstream asset preparation.
Use all previously generated chapter outputs as source material.

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
- Kindle Assets
- InDesign Assets
- Audiobook Assets
- RAG Assets

as the authoritative chapter ecosystem.

---

# OUTPUT LOCATION

Save all outputs into:

```text
/Documents/Books/RCF_FIRST_EDITION/RCF/Chapters/<ChapterName>/Governance/
```

If the folder does not exist:

Create it.

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
      "status": ""
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

This file serves as the master registry for all chapter assets.

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

Provide remediation recommendations.

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

Use instructional design best practices.

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
- Flag potential conflicts with existing glossary entries.

---

# DESIGN HANDOFF PACKET

Create:

```text
<ChapterName>_DesignHandoff.md
```

For future Claude Design processing.

Include:

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

Most visually impactful quotes.

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

Recommend remediation.

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

Recommend improved chunking when appropriate.

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

Prepare the chapter for future edition tracking.

---

# TERMINOLOGY CONSISTENCY AUDIT

Create:

```text
<ChapterName>_TerminologyAudit.md
```

Review all generated artifacts.

Identify:

- Term variations
- Conflicting definitions
- Duplicate frameworks
- Inconsistent naming patterns
- Different explanations of identical concepts

Recommend standardized wording.

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
- Metadata Completeness
- Publishing Readiness

Provide rationale for every score.

Provide recommendations for any score below 5.

---

# CHAPTER PACKAGING AUDIT

Create:

```text
<ChapterName>_PackagingAudit.md
```

Verify:

- Required folders exist
- Required files exist
- File naming conventions comply
- Metadata files exist
- References are valid

List:

## Complete

Items successfully generated.

## Missing

Required items not found.

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

## Readiness Scores

---

## Outstanding Issues

---

## Recommended Next Actions

---

## Certification Statement

State whether the chapter is:

- Draft
- Review Ready
- Production Ready
- Design Ready
- Publishing Ready

with supporting rationale.

---

# FINAL RULE

Do not regenerate existing chapter assets unless required for consistency.

Focus on:

- Governance
- Standardization
- Validation
- Metadata
- Readiness
- Reusability
- Future automation

The objective is to transform a completed PASS 7 chapter into a fully governed, searchable, design-ready, publishing-ready knowledge asset suitable for book production, training development, RAG systems, LMS deployment, web delivery, and future edition management.