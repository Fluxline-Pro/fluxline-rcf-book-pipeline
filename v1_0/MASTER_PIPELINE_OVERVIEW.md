# MASTER PIPELINE OVERVIEW

**Book:** *<BOOK_TITLE>* — <EDITION>
**Author:** <AUTHOR> · **Pipeline version:** v3 (aligned 2026-09-22)
**Kindle decision (2026-09-22):** all Kindle work lives in PHASE 4, chapter by chapter, after the DesignPacket, figures, and the manual print/eBook work are finished and QA'd. PHASE 3 no longer produces a Kindle edition; `<BOOK>_KINDLE_EBOOK` is assembled in PHASE 4 Part B from the per-chapter builds.
**Manuscript sync (2026-09-23):** PHASE 4 opens with Part 0, which brings the manuscript (MD and DOCX) into line with the final eBook PDF, because <AUTHOR> refines wording during InDesign layout. No eBook PDF, no PHASE 4, and nothing after it.

**Authority:** This file is the single reference for paths, gates, triggers, status, and deliverables. Each PHASE file points here. If a PHASE file disagrees with this overview, this overview wins, and the discrepancy is logged for correction.

---

## 1. PHASE 1–7 at a glance

| Phase | File | Role | Entry gate | Exit gate | Runs |
|---|---|---|---|---|---|
| **1** Creation | `PHASE 1- Claude PASS 7 Markdown Script.md` | Generate every chapter artifact from the locked PASS 7 manuscript (Mode A new, Mode B retrofit) | PASS 7 locked | ProductionChecklist + Editorial Suggestions resolved + Marketing trigger | per chapter |
| **2** Governance | `PHASE 2- Governance Check of Outputs.md` | Validate, fix (Tier A/B), propose (Tier C), certify, stage the design handoff | PHASE 1 exit | `GOVERNANCE_READY.md` (certified Design Ready) | per chapter + batch |
| **3** Design + Production | `PHASE 3- Claude Design Hand-off.md` | Claude Design HTML packet + exports + **figure image export**; manual InDesign print; XTTS audio; eBook/print book assembly | `GOVERNANCE_READY.md` | Handoff to 3.5 | per chapter + book assembly |
| **3.5** Design QA | `PHASE 3.5- Claude QA of Design Artifacts.md` | Report-only QA → fix loop; **Kindle Readiness check (§13)** | PHASE 3 exit | `DESIGN_READY.md` (Production Ready + Kindle Ready) | per chapter |
| **4** Kindle | `PHASE 4- Kindle DOCX Chapter Compilation.md` | **Part 0:** sync manuscript MD + DOCX to the final eBook PDF · **Part A:** Kindle DOCX + HTML + metadata + figures per chapter · **Part B:** book-level `<BOOK>_KINDLE_EBOOK` | `DESIGN_READY.md` + final eBook PDF uploaded + `MANUSCRIPT_SYNCED.md` + Step 0 dependency check | Part A checklist PASS; Part B package complete | per chapter / section, then once per book |
| **5** RAG + Local LLM | `PHASE 5- RAG Rebuild & Local LLM Setup (Per Chapter).md` | Final ingestion, ChromaDB rebuild, system prompt, query profiles | PHASE4 PASS | `RAG_READY.md` | per chapter |
| **6** Automation | `PHASE 6- Automation Activation (n8n + Local LLM + RAG).md` | n8n + OpenClaw activation, drafts-only | `RAG_READY.md` | PHASE6 checklist PASS, status `active` | per chapter + batch |
| **6.5** Publication QA | `PHASE 6.5- Claude Design Publication QA.md` | Report-only QA of EPUB/Kindle/print/audio/RAG | PHASE6 PASS | Publishing Ready report | per chapter + book |
| **7** Release | `PHASE 7- Chapter Publishing Checklist.md` | Validation, LLM recommendations, <AUTHOR>'s sign-off | Publishing Ready | **Published** | per chapter |

```
PASS 7 ─▶ 1 ─▶ 2 ─▶ 3 ─▶ 3.5 ─▶ 4 ─▶ 5 ─▶ 6 ─▶ 6.5 ─▶ 7 ─▶ Published
               ▲          │ fix loop
               └──────────┘ (3.5 → 3; 6.5 → owner phase after approval)
```

---

## 2. Milestone map (status ladder)

One ladder is used by every phase:

`Draft → Review Ready → Design Ready → Production Ready → Publishing Ready → Published`

| Milestone | Awarded by | Evidence |
|---|---|---|
| Draft | PHASE 1 | Artifacts exist |
| Review Ready | PHASE 2 | Governance ran; blockers listed |
| **Design Ready** | PHASE 2 | ChapterCertification + `GOVERNANCE_READY.md` |
| **Production Ready** | PHASE 3.5 | DesignQA report + `DESIGN_READY.md` |
| **Publishing Ready** | PHASE 6.5 | PublicationQA report (+ per-format sub-certs) |
| **Published** | PHASE 7, **<AUTHOR> only** | Signed release checklist |

PHASES 4, 5, and 6 don't change the status; they gate by checklist (`gateStatus`) and trigger.

---

## 3. Deliverable map

| After | Deliverable | Location |
|---|---|---|
| **PHASE 3** (+3.5) | <BOOK>_EBOOK_PDF&EPUB | `_BookPublication/<BOOK>_EBOOK/` |
| | <BOOK>_WORKBOOK_EBOOK | `_BookPublication/<BOOK>_WORKBOOK_EBOOK/` |
| | <BOOK>_PRINT_BOOK (manual InDesign) | `_BookPublication/<BOOK>_PRINT_BOOK/` |
| | <BOOK>_WORKBOOK_PRINT_BOOK (manual InDesign) | `_BookPublication/<BOOK>_WORKBOOK_PRINT_BOOK/` |
| | <BOOK>_AUDIOBOOK | `_BookPublication/<BOOK>_AUDIOBOOK/` |
| | Exported figure images (PHASE 4 dependency) | `<CH_ROOT>/DesignPacket/figures_export/` |
| **PHASE 4 (Part 0, per chapter)** | Manuscript MD + DOCX synced to the final eBook PDF | `<CH_ROOT>/Manuscript/<ChapterName>_Manuscript.md` / `.docx` |
| | Manuscript sync report | `<CH_ROOT>/Manuscript/<ChapterName>_ManuscriptSync_<YYYYMMDD_HHMM>.md` |
| **PHASE 4 (Part A, per chapter)** | Kindle DOCX per chapter | `<CH_ROOT>/Kindle/<ChapterName>_Kindle.docx` |
| | Kindle-ready HTML blocks | `<CH_ROOT>/Kindle/<ChapterName>_Kindle.html` |
| | Kindle-ready metadata | `<CH_ROOT>/Kindle/<ChapterName>_KindleMetadata.json` |
| | Kindle figure images | `<CH_ROOT>/Kindle/figures/` |
| **PHASE 4 (Part B, per book)** | <BOOK>_KINDLE_EBOOK: `<BOOK>_Kindle.docx` (KDP source), `.epub`, `.azw3` proof, metadata, cover, assembly report | `_BookPublication/<BOOK>_KINDLE_EBOOK/` |
| **PHASE 5** | RAG_INGESTION | `<CH_ROOT>/RAG/<ChapterName>_RAG_Ingestion.json` + `RAG/Chunks/` |
| | RAG_ValidationReport | `<CH_ROOT>/RAG/<ChapterName>_RAG_ValidationReport.md` |
| | LLM_SystemPrompt | `<CH_ROOT>/RAG/<ChapterName>_LLM_SystemPrompt.md` |
| | RAG_QueryProfiles | `<CH_ROOT>/RAG/<ChapterName>_RAG_QueryProfiles.md` |
| **PHASE 6** | N8N_AUTOMATIONS | `_BookAutomation/n8n/` |
| | OpenClaw pipelines | `_BookAutomation/OpenClaw/` |
| | AutomationIndex.json | `_BookAutomation/AutomationIndex.json` |
| | ActivationReport | `<CH_ROOT>/<ChapterName>_PHASE6_ActivationReport.md` |
| **PHASE 7** | Validation of outputs · checklist of all content · <AUTHOR>'s sign-off with LLM recommendations | `<CH_ROOT>/<ChapterName>_PHASE7_ReleaseChecklist.md` → copy in `_FinalizedReleases/` |

The eBook, workbook, print, and audiobook deliverables are assembled in PHASE 3 *book assembly mode* once every chapter is Production Ready. **<BOOK>_KINDLE_EBOOK is assembled in PHASE 4 Part B**, after every chapter's Kindle build passes, because Kindle depends on the finished figures and the completed print/eBook work. PHASE 6.5 validates the package; <AUTHOR> approves the KDP upload in PHASE 7.

Per-chapter phase records (all at `<CH_ROOT>` root unless noted):
`_ProductionChecklist.md` (P1) · `Governance/_ChapterCertification.md` (P2) · `Governance/_DesignQA_<ts>.md` (P3.5) · `_PHASE4_KindleChecklist.md` · `_PHASE5_RAGChecklist.md` · `_PHASE6_AutomationChecklist.md` · `Governance/_PublicationQA_<ts>.md` (P6.5) · `_PHASE7_ReleaseChecklist.md`

---

## 4. Folder map

**Book root:** `<BOOK_ROOT>` — your book's root folder, e.g. `D:\Books\<BOOK_SLUG>`. Every path below is relative to it.
**Chapter root:** `<CH_ROOT>` = `<BOOK_ROOT>/Chapters/<ChapterName>/Final/`
**Chapter name:** `Ch<N>_<PascalCaseTitle>` (e.g. `Ch1_YourChapterTitle`)
**Print InDesign book:** <AUTHOR> may keep the print InDesign book (INDB, templates, linked assets) in separate print folders outside `<BOOK_ROOT>`. Phases then treat print as <AUTHOR>-confirmed rather than checking `InDesign/` for files; the final **eBook** PDF is the layout text PHASE 4 Part 0 syncs the manuscript to.
**File names:** `<ChapterName>_<ArtifactType>.<ext>`; Marketing: `<ChapterName>_MKT_<Type>.<ext>`; Claude Design project files: `Ch<N>_<Type>.dc.html` (accepted exception)

```
<BOOK_ROOT>/
├── _ClaudeInstructions/          PHASE prompts, this overview, _Backups/, _Superseded/
├── _BookMarketing/               VoiceKit.md (book-level voice)                    [P1]
├── _BookGovernance/              cross-chapter reports, master glossary, book QA   [P2, P6.5]
├── _BookPublication/             six book deliverables + _Masters/                 [P3 assembly, P6.5]
├── _BookAutomation/              AutomationIndex.json, n8n/, OpenClaw/             [P6]
├── _FinalizedReleases/           signed PHASE 7 checklists                         [P7]
├── _Archive/<ChapterName>/       drafts moved at release                           [P7]
├── FrontMatter/Final/<Section>/  {Audiobook, eBook, Kindle}/                       [P3, P4]
├── Parts/<NNN>_<Part>/Kindle/                                                      [P4]
├── BackMatter/<Section>/         {Audiobook, eBook, Kindle}/                       [P3, P4]
└── Chapters/<ChapterName>/
    ├── Final/
    │   ├── Manuscript/           PASS 7 copy, EditorialSuggestions [P1]; synced to eBook PDF, ManuscriptSync report, Trigger/ [P4 Part 0]
    │   ├── ReviewPacket/  Workbook/  Training/  ReferenceGuides/  Slides/          [P1; exports P3]
    │   ├── Equations/                                                              [P1]
    │   ├── eBook/                HTML blocks + metadata [P1]; PDF/EPUB exports [P3]; final eBook PDF (required by P4 Part 0)
    │   ├── Kindle/               DOCX, HTML, metadata, figures/                    [P4]
    │   ├── InDesign/             prep [P1]; .indd + print PDF (manual, optional)   [P3]
    │   ├── Audiobook/            script, markers [P1]; MP3                         [P3]
    │   ├── RAG/                  PHASE 1 packet; Ingestion, Chunks/, Trigger/      [P1, P5]
    │   ├── Marketing/            Intake/, Seeds/, Trigger/ [P1]; Generated/        [P6]
    │   ├── Governance/           reports, Trigger/, _Backups/, QA reports          [P2, P3.5, P6.5]
    │   ├── DesignPacket/         _ds/ (DSM), packet/, figures_export/, templates/, uploads/, Trigger/ [P2 staging, P3]
    │   └── <ChapterName>_*Checklist / _Report files
    └── Published/                approved release copies                           [P7]
```

---

## 5. Trigger & automation map

| Trigger file | Location | Created by | Consumed by |
|---|---|---|---|
| `MARKETING_READY.md` / `_INCOMPLETE` | `Marketing/Trigger/` | P1, re-validated P2 | P6 3A marketing workflows |
| `GOVERNANCE_READY.md` / `_INCOMPLETE` | `Governance/Trigger/` | P2 | P3 entry; P6 3C |
| `DESIGN_READY.md` / `_INCOMPLETE` | `DesignPacket/Trigger/` | P3.5 | P4 entry; P6 3B/3D |
| `MANUSCRIPT_SYNCED.md` / `MANUSCRIPT_SYNC_INCOMPLETE.md` | `Manuscript/Trigger/` | P4 Part 0 | P4 Step 0; P4 Part B; P5 entry |
| `RAG_READY.md` / `_INCOMPLETE` | `RAG/Trigger/` | P5 | P6 entry; P6 3E |

Rules: triggers only fire workflows for chapters whose `automationStatus` is `active` or `batch-ready`. Never leave a stale READY file; an older one is renamed `*_superseded_<timestamp>.md`.

| Automation layer | Definitions | Grounding | Output |
|---|---|---|---|
| n8n workflows (3A–3E) | `_BookAutomation/n8n/` | RAG_Ingestion + LLM_SystemPrompt + QueryProfiles | `Marketing/Generated/<date>/` drafts; reports |
| OpenClaw pipelines (5A–5D) | `_BookAutomation/OpenClaw/` | same | drafts; reports |

**Approval rule:** every generated item is `status: draft`. Only <AUTHOR> approves. Nothing publishes, schedules, edits the manuscript, or overwrites `Final/` automatically.

---

## 6. RAG map

| Stage | Phase | Files | Status |
|---|---|---|---|
| Pre-governance packet | P1 Step 10 | `RAG/<ChapterName>_RAG_chunks.jsonl`, `_RAG_metadata.json` | superseded after P5 (kept) |
| Chunk validation / re-chunk | P2 | `Governance/_ChunkingValidation.md` | Tier A fixes |
| Final ingestion | P5 | `_RAG_Ingestion.json`, `RAG/Chunks/_RAG_Chunks.jsonl` | authoritative |
| Vector store | P5 | ChromaDB collection `<RAG_COLLECTION>`, filtered by `chapterName` | rebuilt per chapter |
| Validation | P5 | `_RAG_ValidationReport.md` (incl. retrieval smoke test) | gate |
| Publication check | P6.5 | RAG sub-certification | gate |

**Chunk rule (all phases):** 500–1000 words · 100-word overlap (80–120 tolerated) · section name in metadata · never split a concept.
**Authority hierarchy (embedded in metadata):** PASS 7 Manuscript > GlossaryNormalized > LearningMetadata / FigureRegistry > derived artifacts. From PHASE 4 Part 0 on, "Manuscript" means the manuscript as synced to the final eBook PDF.

---

## 7. LLM map

| Model / tool | Role | Phases |
|---|---|---|
| Claude (Cowork) | Artifact generation, governance fixes, QA reports, Kindle compile, RAG build, recommendations | 1, 2, 3.5, 4, 5, 6.5, 7 (Part B) |
| Claude Design | DSM-bound HTML packet, layouts, exports; applies HTML fixes | 3 (and fixes from 3.5 / 6.5) |
| Ollama: drafting model (default Qwen2.5 14B Instruct) | Grounded marketing/design drafts | 5 (configure), 6 (run) |
| Ollama: embedding model (default nomic-embed-text) | Embeddings for `<RAG_COLLECTION>`; one model for all chapters | 5 |
| LM Studio (optional) | OpenAI-compatible endpoint for n8n | 5, 6 |
| XTTS (local) | Audiobook narration render | 3 |
| n8n / OpenClaw | Orchestration | 6 |

**Local-LLM context load order (8k window):** VoiceKit → TerminologyLock → Claims + Do-Not-Claim → Marketing rules → Design rules → Governance rules → RAG query rules → task.

---

## 8. Publishing map

| Channel | Source | Built in | Validated in | Released in |
|---|---|---|---|---|
| eBook PDF & EPUB | `_Masters/Manuscript_Master.html` ← chapter `eBook/` + DesignPacket | P3 | P3.5, P6.5 | P7 |
| Workbook eBook | `_Masters/Workbook_Master.html` ← chapter Workbook + DesignPacket | P3 | P3.5, P6.5 | P7 |
| Print book | Manual InDesign from Print 7×10 layouts + InDesign prep | P3 (<AUTHOR>) | P6.5 (package) | P7 |
| Workbook print | Manual InDesign | P3 (<AUTHOR>) | P6.5 | P7 |
| Audiobook | XTTS from narration scripts | P3 | P3.5, P6.5 | P7 |
| Kindle / KDP | Per-chapter Kindle build (P4 Part A) → book assembly (P4 Part B) | P4 | P6.5 | P7 (<AUTHOR> approves upload) |
| RAG / local LLM | Final ingestion | P5 | P5, P6.5 | P7 |
| Marketing | Intake + Seeds → n8n/OpenClaw drafts | P1, P6 | P2, P6 tests | Per item, <AUTHOR> approval |
| Training / LMS / CMS | DesignPacket HTML + exports | P3, P6 (drafts) | P3.5 | P7 |
