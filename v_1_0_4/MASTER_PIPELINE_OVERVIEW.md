# MASTER PIPELINE OVERVIEW

**Book:** *<BOOK_TITLE>* — <EDITION>
**Author:** <AUTHOR> · **Pipeline version:** v3.2 (aligned 2026-09-30)
**Kindle decision (2026-09-22):** all Kindle work lives in PHASE 4, chapter by chapter, after the DesignPacket, figures, and the manual print/eBook work are finished and QA'd. PHASE 3 no longer produces a Kindle edition; `<BOOK>_KINDLE_EBOOK` is assembled in PHASE 4 Part B from the per-chapter builds.
**Dual RAG (2026-09-24):** PHASE 5 builds one canonical chunk set and embeds it into two vector stores: **Local** (ChromaDB + ONNX/TEI embeddings, Docker) and **Cloud** (vector files in Azure Blob Storage, embedded with Azure OpenAI `text-embedding-3-large` and searched in memory; multilingual). Each track has its own model, trigger, and index manifest; `RAG_READY.md` means every enabled track passed.
**The final eBook is the trigger (2026-09-27):** when <AUTHOR> finishes a chapter's eBook and exports its final PDF, the chapter is ready for everything that follows. PHASE 4 Part 0 syncs the manuscript to it, Part A builds Kindle from it, Part C records the audiobook from the Kindle output, and PHASE 5 onward read the synced text. The XTTS render is a draft; the final audiobook is <AUTHOR>'s own recording, made in Adobe Audition.
**Book audit (2026-09-27):** PHASE 0.9 audits the whole book for drift (terms, definitions, acronyms, equations, thresholds, lists, figures, cross-references, headings) on the draft **before PASS 7**, while wording is cheapest to change. Its author-resolved `Audit_CanonicalTerms.json` seeds PHASE 1 and PHASE 2. A **final delta audit** runs at PHASE 4 Part B (step B0) on the manuscripts synced to the final eBook PDFs, and gates the book's release-ready flag in the cloud RAG store.
**Workbook track (2026-09-30):** the workbook ships as an **eBook PDF** (8.5×11 in) and a **full-color print book** (7×10 in). **PHASE 3W** owns it end to end.
- The workbook manuscript follows the chapter manuscript's rule: the DOCX is canonical and the MD is its replica. `WORKBOOK_MANUSCRIPT_READY.md` (end of PHASE 2) confirms DOCX = MD before Claude Design builds the workbook in PHASE 3.
- <AUTHOR> then produces both formats in InDesign and uploads the two PDFs to `Workbook/`, which is the cue that they're done. The W3 check syncs layout-time wording back to the DOCX and MD, and writes `WORKBOOK_READY.md` once PDF = DOCX = MD.
- No Kindle edition, no audiobook, no RAG ingestion.
- The book-level workbook is assembled after the final delta audit (B0), once exercise IDs and wording are frozen.
**Manuscript sync (2026-09-23):** PHASE 4 opens with Part 0, which brings the manuscript (MD and DOCX) into line with the final eBook PDF, because <AUTHOR> refines wording during InDesign layout. No eBook PDF, no PHASE 4, and nothing after it.

**Release v1.0.2 (2026-09-27):** dual RAG (PHASE 5 v4, PHASE 6 v4); the local embedding default is now `nomic-embed-text-v1.5` on an ONNX/TEI container, because the previous default truncated chunks at 256 tokens. The cloud track uses `text-embedding-3-large` with vectors stored in Azure Blob Storage (no search service), for multilingual retrieval at low cost. New PHASE 0.9 book-wide audit; the audiobook moved to PHASE 4 Part C (recorded from the Kindle output: XTTS draft, <AUTHOR>'s final narration in Adobe Audition); the final eBook PDF formally triggers each chapter's final-wording chain.

**Release v1.0.4 (2026-09-30):** governed cloud track. PHASE 5 v4.2 can embed Track C through a governance gateway (recommended), defaults cloud vectors to 1,024 dimensions, and adds `part`, `lesson`, `figureId`, and `altText` to the cloud vector lines. PHASE 6 v4.1 adds the §3G nightly RAG refresh, which re-ingests changed chapters into both stores and notifies cloud consumers.

**Release v1.0.3 (2026-09-30):** new PHASE 3W Workbook Track (eBook PDF + full-color print, InDesign only). The Kindle workbook (PHASE 4 B5), the workbook's RAG ingestion, and the HTML-built workbook eBook (`Workbook_Master.html`) are removed.

**Authority:** This file is the single reference for paths, gates, triggers, status, and deliverables. Each PHASE file points here. If a PHASE file disagrees with this overview, this overview wins, and the discrepancy is logged for correction.

---

## 1. PHASE 0.9–7 at a glance

| Phase | File | Role | Entry gate | Exit gate | Runs |
|---|---|---|---|---|---|
| **0.9** Book audit | `PHASE 0.9- Book-Wide Manuscript Audit.md` | Report-only book-wide drift audit (extract → detect → eval questions → consolidation); canonical decisions for <AUTHOR>. **Mode F** before PASS 7; **Mode P** spot checks during PASS 7; **Mode D** final delta at PHASE 4 Part B | Full draft in `<DRAFT_SOURCE>` (Mode F); every chapter `MANUSCRIPT_SYNCED.md` (Mode D) | `AUDIT_CLEAR.md` (F) · `AUDIT_FINAL_CLEAR.md` (D) | once per book, plus the final delta |
| **1** Creation | `PHASE 1- Claude PASS 7 Markdown Script.md` | Generate every chapter artifact from the locked PASS 7 manuscript (Mode A new, Mode B retrofit) | PASS 7 locked + `AUDIT_CLEAR.md` | ProductionChecklist + Editorial Suggestions resolved + Marketing trigger | per chapter |
| **2** Governance | `PHASE 2- Governance Check of Outputs.md` | Validate, fix (Tier A/B), propose (Tier C), certify, stage the design handoff | PHASE 1 exit | `GOVERNANCE_READY.md` (certified Design Ready) | per chapter + batch |
| **3** Design + Production | `PHASE 3- Claude Design Hand-off.md` | Claude Design HTML packet + exports + **figure image export**; manual eBook + print InDesign books; eBook/print book assembly (audiobook moved to PHASE 4) | `GOVERNANCE_READY.md` | Handoff to 3.5 | per chapter + book assembly |
| **3W** Workbook track | `PHASE 3W- Workbook Track (eBook + Print).md` | Workbook manuscript DOCX = MD gate (end of 2); Claude Design builds the workbook (3); <AUTHOR> produces the eBook (8.5×11) + print (7×10) PDFs in InDesign and uploads them; Claude syncs layout wording back (PDF = DOCX = MD) and checks the registry, preflight, and eBook. Book-level workbook assembled after B0. No Kindle, audiobook, or RAG | `GOVERNANCE_READY.md` → `WORKBOOK_MANUSCRIPT_READY.md`; both workbook PDFs uploaded to `Workbook/` | `WORKBOOK_READY.md` (per chapter); workbook assembly report (per book) | per chapter, then once per book |
| **3.5** Design QA | `PHASE 3.5- Claude QA of Design Artifacts.md` | Report-only QA → fix loop; **Kindle Readiness check (§13)** | PHASE 3 exit | `DESIGN_READY.md` (Production Ready + Kindle Ready) | per chapter |
| **4** Final-wording builds (Kindle + audiobook) | `PHASE 4- Kindle DOCX Chapter Compilation.md` | **Part 0:** sync manuscript MD + DOCX to the final eBook PDF · **Part A:** Kindle DOCX + HTML + metadata + figures per chapter · **Part 0.7:** audit spot check (PHASE 0.9 Mode P) · **Part C:** narration refresh + XTTS audiobook per chapter · **Part B:** B0 final delta audit (PHASE 0.9 Mode D), then book-level `<BOOK>_KINDLE_EBOOK` and `<BOOK>_AUDIOBOOK` | `DESIGN_READY.md` + final eBook PDF uploaded + `MANUSCRIPT_SYNCED.md` + Step 0 dependency check | Part A checklist PASS; Part B package complete | per chapter / section, then once per book |
| **5** RAG (Local + Cloud) + LLM | `PHASE 5- RAG Rebuild & Local LLM Setup (Per Chapter).md` | Canonical chunk set; Track L ChromaDB rebuild; Track C Blob vector file rewrite (if enabled); parity check; system prompt, query profiles | PHASE4 PASS + `MANUSCRIPT_SYNCED.md` | `RAG_LOCAL_READY.md` (+ `RAG_CLOUD_READY.md` if enabled) → `RAG_READY.md` | per chapter |
| **6** Automation | `PHASE 6- Automation Activation (n8n + Local LLM + RAG).md` | n8n + OpenClaw activation, drafts-only; each workflow grounded on the local or cloud index; §3G nightly RAG refresh keeps both stores in sync | `RAG_READY.md` | PHASE6 checklist PASS, status `active` | per chapter + batch |
| **6.5** Publication QA | `PHASE 6.5- Claude Design Publication QA.md` | Report-only QA of EPUB/Kindle/print/audio/RAG | PHASE6 PASS | Publishing Ready report | per chapter + book |
| **7** Release | `PHASE 7- Chapter Publishing Checklist.md` | Validation, LLM recommendations, <AUTHOR>'s sign-off | Publishing Ready | **Published** | per chapter |

```
PASS 6 (tighten) ─▶ 0.9 audit ─▶ PASS 7 (voice; pseudo-locked)
  ─▶ 1 ─▶ 2 ─▶ 3 ─▶ 3.5 ─▶ eBook + print InDesign books (final wording edits)
        └─ 3W workbook: WORKBOOK_MANUSCRIPT_READY (end of 2) ─▶ Claude Design workbook (3) ─▶ InDesign eBook + print
                          ─▶ upload PDFs ─▶ W3 sync + check (PDF = DOCX = MD) ─▶ WORKBOOK_READY
  ─▶ 4: Part 0 sync + 0.7 spot check ─▶ Part A Kindle ─▶ Part C audiobook (script from the Kindle output; XTTS draft; <AUTHOR> records in Audition)
  ─▶ 5 ─▶ 6 ─▶ 6.5 ─▶ 7 ─▶ Published                               (per chapter)

  4 Part B, once every chapter has passed Part A and Part C:
  B0 final delta audit ─▶ Kindle package + audiobook set ─▶ 6.5 book mode   (once per book)
                       └─▶ 3W W4–W5: workbook eBook + print books (after B0)

Fix loops: 3.5 → 3; 3W W3 → InDesign workbook fix (and DOCX → MD) → re-export → re-upload; 0.7 / B0 blocking finding → eBook (and print) InDesign fix → re-export → Part 0 re-run; 6.5 → owner phase after approval.
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
| **PHASE 0.9 (per book)** | Audit report, canonical decisions, ledger, per-chapter pass files | `_BookGovernance/Audit/<RUN_ID>/` |
| | Canonical terms (author-resolved) | `_BookGovernance/Audit/Audit_CanonicalTerms.json` |
| | Evaluation set (Pass 3) | `_BookGovernance/Audit/EvalSet/<EDITION>/` |
| **PHASE 3** (+3.5) | <BOOK>_EBOOK_PDF&EPUB | `_BookPublication/<BOOK>_EBOOK/` |
| | <BOOK>_PRINT_BOOK (manual InDesign) | `_BookPublication/<BOOK>_PRINT_BOOK/` |
| | Exported figure images (PHASE 4 dependency) | `<CH_ROOT>/DesignPacket/figures_export/` |
| **PHASE 3W (per chapter)** | Workbook manuscript: DOCX (canonical) + MD (replica), synced to the eBook PDF in W3 | `<CH_ROOT>/Workbook/<ChapterName>_Exercise<L.N>_Workbook.docx` / `.md` |
| | Workbook eBook PDF (8.5×11) + full-color print PDF (7×10) (<AUTHOR>, InDesign) | `<CH_ROOT>/Workbook/<ChapterName>_Workbook_eBook.pdf`, `_Workbook_Print.pdf` |
| | Workbook QA report | `<CH_ROOT>/Governance/<ChapterName>_WorkbookQA_<YYYYMMDD_HHMM>.md` |
| | Exercise registry (book-wide, updated per chapter) | `_BookGovernance/Workbook/Workbook_ExerciseRegistry.json` |
| **PHASE 3W (per book, after B0)** | <BOOK>_WORKBOOK_EBOOK (PDF) + assembly report | `_BookPublication/<BOOK>_WORKBOOK_EBOOK/` |
| | <BOOK>_WORKBOOK_PRINT_BOOK (full-color print PDF + cover) | `_BookPublication/<BOOK>_WORKBOOK_PRINT_BOOK/` |
| **PHASE 4 (Part 0, per chapter)** | Manuscript MD + DOCX synced to the final eBook PDF | `<CH_ROOT>/Manuscript/<ChapterName>_Manuscript.md` / `.docx` |
| | Manuscript sync report | `<CH_ROOT>/Manuscript/<ChapterName>_ManuscriptSync_<YYYYMMDD_HHMM>.md` |
| **PHASE 4 (Part A, per chapter)** | Kindle DOCX per chapter | `<CH_ROOT>/Kindle/<ChapterName>_Kindle.docx` |
| | Kindle-ready HTML blocks | `<CH_ROOT>/Kindle/<ChapterName>_Kindle.html` |
| | Kindle-ready metadata | `<CH_ROOT>/Kindle/<ChapterName>_KindleMetadata.json` |
| | Kindle figure images | `<CH_ROOT>/Kindle/figures/` |
| **PHASE 4 (Part C, per chapter)** | Narration script (from the Kindle output); XTTS draft (optional); <AUTHOR>'s final narration MP3 (Adobe Audition) | `<CH_ROOT>/Audiobook/` (drafts in `Audiobook/Drafts/`) |
| **PHASE 4 (Part B, per book)** | <BOOK>_AUDIOBOOK (ordered MP3 set + track list) | `_BookPublication/<BOOK>_AUDIOBOOK/` |
| | <BOOK>_KINDLE_EBOOK: `<BOOK>_Kindle.docx` (KDP source), `.epub`, `.azw3` proof, metadata, cover, assembly report | `_BookPublication/<BOOK>_KINDLE_EBOOK/` |
| **PHASE 5** | RAG_INGESTION | `<CH_ROOT>/RAG/<ChapterName>_RAG_Ingestion.json` + `RAG/Chunks/` |
| | Index manifests (per track) | `<CH_ROOT>/RAG/Index/<ChapterName>_RAG_Index_Local.json`, `_RAG_Index_Cloud.json` |
| | RAG_ValidationReport (both tracks + parity) | `<CH_ROOT>/RAG/<ChapterName>_RAG_ValidationReport.md` |
| | Book RAG config (once) | `_BookAutomation/RAG/RAG_Config.json` |
| | LLM_SystemPrompt | `<CH_ROOT>/RAG/<ChapterName>_LLM_SystemPrompt.md` |
| | RAG_QueryProfiles | `<CH_ROOT>/RAG/<ChapterName>_RAG_QueryProfiles.md` |
| **PHASE 6** | N8N_AUTOMATIONS | `_BookAutomation/n8n/` |
| | OpenClaw pipelines | `_BookAutomation/OpenClaw/` |
| | AutomationIndex.json | `_BookAutomation/AutomationIndex.json` |
| | ActivationReport | `<CH_ROOT>/<ChapterName>_PHASE6_ActivationReport.md` |
| **PHASE 7** | Validation of outputs · checklist of all content · <AUTHOR>'s sign-off with LLM recommendations | `<CH_ROOT>/<ChapterName>_PHASE7_ReleaseChecklist.md` → copy in `_FinalizedReleases/` |

The eBook and print deliverables are assembled in PHASE 3 *book assembly mode* once every chapter is Production Ready. **The workbook's two deliverables are assembled in PHASE 3W (W4)**, after the final delta audit (B0), so exercise IDs and manuscript wording can't move under them. **The audiobook is recorded per chapter in PHASE 4 Part C and assembled in Part B**: it is recorded from the Kindle output, which is built from the final eBook. **<BOOK>_KINDLE_EBOOK is assembled in PHASE 4 Part B**, after every chapter's Kindle build passes, because Kindle depends on the finished figures and the completed print/eBook work. PHASE 6.5 validates the package; <AUTHOR> approves the KDP upload in PHASE 7.

Per-chapter phase records (all at `<CH_ROOT>` root unless noted):
`_ProductionChecklist.md` (P1) · `Governance/_ChapterCertification.md` (P2) · `Governance/_DesignQA_<ts>.md` (P3.5) · `Governance/_WorkbookQA_<ts>.md` (P3W) · `_PHASE4_KindleChecklist.md` · `_PHASE5_RAGChecklist.md` · `_PHASE6_AutomationChecklist.md` · `Governance/_PublicationQA_<ts>.md` (P6.5) · `_PHASE7_ReleaseChecklist.md`

---

## 4. Folder map

**Book root:** `<BOOK_ROOT>` — your book's root folder, e.g. `D:\Books\<BOOK_SLUG>`. Every path below is relative to it.
**Chapter root:** `<CH_ROOT>` = `<BOOK_ROOT>/Chapters/<ChapterName>/Final/`
**Chapter name:** `Ch<N>_<PascalCaseTitle>` (e.g. `Ch1_YourChapterTitle`)
**Print InDesign book:** <AUTHOR> may keep the print InDesign book (INDB, templates, linked assets) in separate print folders outside `<BOOK_ROOT>`. Phases then treat print as <AUTHOR>-confirmed rather than checking `InDesign/` for files; the final **eBook** PDF is the layout text PHASE 4 Part 0 syncs the manuscript to.
**Workbook InDesign files:** <AUTHOR> keeps them (documents, INDB, links, fonts) in `<WORKBOOK_INDESIGN_ROOT>`, outside `<BOOK_ROOT>` (for example, OneDrive). No phase reads them; PHASE 3W checks only the exported PDFs uploaded to `Workbook/` (eBook 8.5×11 in, print 7×10 in).
**File names:** `<ChapterName>_<ArtifactType>.<ext>`; Marketing: `<ChapterName>_MKT_<Type>.<ext>`; Claude Design project files: `Ch<N>_<Type>.dc.html` (accepted exception)

```
<BOOK_ROOT>/
├── _ClaudeInstructions/          PHASE prompts, this overview, _Backups/, _Superseded/
├── _BookMarketing/               VoiceKit.md (book-level voice)                    [P1]
├── _BookGovernance/              cross-chapter reports, master glossary, book QA   [P2, P6.5]
│   ├── Audit/                    config, canonical terms, EvalSet/, <RUN_ID>/, Trigger/ [P0.9]
│   └── Workbook/                 Workbook_ExerciseRegistry.json                    [P3W]
├── _BookPublication/             six book deliverables + _Masters/                 [P3 assembly, P3W, P4 Part B, P6.5]
├── _BookAutomation/              AutomationIndex.json, n8n/, OpenClaw/, Notices/   [P6]
├── _FinalizedReleases/           signed PHASE 7 checklists                         [P7]
├── _Archive/<ChapterName>/       drafts moved at release                           [P7]
├── FrontMatter/Final/<Section>/  {Audiobook, eBook, Kindle}/                       [P3, P4]
├── Parts/<NNN>_<Part>/Kindle/                                                      [P4]
├── BackMatter/<Section>/         {Audiobook, eBook, Kindle}/                       [P3, P4]
└── Chapters/<ChapterName>/
    ├── Final/
    │   ├── Manuscript/           PASS 7 copy, EditorialSuggestions [P1]; synced to eBook PDF, ManuscriptSync report, Trigger/ [P4 Part 0]
    │   ├── ReviewPacket/  Training/  ReferenceGuides/  Slides/                     [P1; exports P3]
    │   ├── Workbook/             packet, workbook manuscript DOCX (canonical) + MD [P1]; Trigger/ [P2 → P3W]; eBook + print PDFs [P3W]
    │   ├── Equations/                                                              [P1]
    │   ├── eBook/                HTML blocks + metadata [P1]; PDF/EPUB exports [P3]; final eBook PDF (required by P4 Part 0)
    │   ├── Kindle/               DOCX, HTML, metadata, figures/                    [P4]
    │   ├── InDesign/             prep [P1]; .indd + print PDF (manual, optional)   [P3]
    │   ├── Audiobook/            script, markers [P1]; script from Kindle, Drafts/ (XTTS), final MP3 [P4 Part C]
    │   ├── RAG/                  PHASE 1 packet; Ingestion, Chunks/, Index/, Trigger/ [P1, P5]
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
| **Final eBook PDF** `<ChapterName>_eBook.pdf` (newer than `MANUSCRIPT_SYNCED.md`) | `eBook/` | <AUTHOR> (final export) | P4 Part 0; P6 3F watcher (notify only) |
| `AUDIT_CLEAR.md` / `AUDIT_INCOMPLETE.md` | `_BookGovernance/Audit/Trigger/` | P0.9 Mode F | P1 entry |
| `AUDIT_FINAL_CLEAR.md` / `AUDIT_FINAL_INCOMPLETE.md` | `_BookGovernance/Audit/Trigger/` | P0.9 Mode D (P4 B0) | P4 Part B; P5 cloud release-ready flag; P6.5 book mode; P7 |
| `MARKETING_READY.md` / `_INCOMPLETE` | `Marketing/Trigger/` | P1, re-validated P2 | P6 3A marketing workflows |
| `GOVERNANCE_READY.md` / `_INCOMPLETE` | `Governance/Trigger/` | P2 | P3 entry; P6 3C |
| `WORKBOOK_MANUSCRIPT_READY.md` / `WORKBOOK_MANUSCRIPT_INCOMPLETE.md` | `Workbook/Trigger/` | P3W W0 gate (end of P2) | P3 workbook design |
| **Workbook PDFs** `<ChapterName>_Workbook_eBook.pdf` + `_Workbook_Print.pdf` (newer than `WORKBOOK_READY.md`) | `Workbook/` | <AUTHOR> (final exports from InDesign) | P3W W3 |
| `WORKBOOK_READY.md` / `WORKBOOK_INCOMPLETE.md` | `Workbook/Trigger/` | P3W W3 | P3W W4 (every chapter); P6.5 workbook sub-cert; P7 |
| `DESIGN_READY.md` / `_INCOMPLETE` | `DesignPacket/Trigger/` | P3.5 | P4 entry; P6 3B/3D |
| `MANUSCRIPT_SYNCED.md` / `MANUSCRIPT_SYNC_INCOMPLETE.md` | `Manuscript/Trigger/` | P4 Part 0 | P4 Step 0; P4 Part B; P5 entry |
| `RAG_LOCAL_READY.md` | `RAG/Trigger/` | P5 Track L | P6 local workflows; local 3E |
| `RAG_CLOUD_READY.md` | `RAG/Trigger/` | P5 Track C | P6 cloud workflows; cloud 3E |
| `RAG_READY.md` / `_INCOMPLETE` | `RAG/Trigger/` | P5 (all enabled tracks) | P6 entry; batch mode |

Rules: triggers only fire workflows for chapters whose `automationStatus` is `active` or `batch-ready`. Never leave a stale READY file; an older one is renamed `*_superseded_<timestamp>.md`.

| Automation layer | Definitions | Grounding | Output |
|---|---|---|---|
| n8n workflows (3A–3E) | `_BookAutomation/n8n/` | RAG_Ingestion + LLM_SystemPrompt + QueryProfiles; local index by default, cloud index for Azure-hosted consumers | `Marketing/Generated/<date>/` drafts; reports |
| OpenClaw pipelines (5A–5D) | `_BookAutomation/OpenClaw/` | same | drafts; reports |

**Approval rule:** every generated item is `status: draft`. Only <AUTHOR> approves. Nothing publishes, schedules, edits the manuscript, or overwrites `Final/` automatically.

---

## 6. RAG map

| Stage | Phase | Files | Status |
|---|---|---|---|
| Pre-governance packet | P1 Step 10 | `RAG/<ChapterName>_RAG_chunks.jsonl`, `_RAG_metadata.json` | superseded after P5 (kept) |
| Chunk validation / re-chunk | P2 | `Governance/_ChunkingValidation.md` | Tier A fixes |
| Final ingestion | P5 | `_RAG_Ingestion.json`, `RAG/Chunks/_RAG_Chunks.jsonl` | authoritative |
| Vector store — Local (Track L) | P5 | ChromaDB (Docker) collection `<RAG_COLLECTION>`; ONNX/TEI embeddings (`nomic-embed-text-v1.5`, 768d); filtered by `chapterName` | rebuilt per chapter |
| Vector store — Cloud (Track C) | P5 | Azure Blob Storage container `<RAG_BLOB_CONTAINER>`: `<BOOK>/chapters/<ChapterName>/current.json` → `vectors.jsonl.gz`; `text-embedding-3-large` (1024d by default, multilingual), through the governance gateway when configured; in-memory cosine retrieval filtered by metadata; cloud-eligible chunks only | rebuilt per chapter, when enabled |
| Index manifests + parity | P5 | `RAG/Index/*_RAG_Index_{Local,Cloud}.json`; same chunk IDs and chunk-set hash in both | gate |
| Validation | P5 | `_RAG_ValidationReport.md` (incl. retrieval smoke test) | gate |
| Evaluation set | P0.9 Pass 3 → P5 | `_BookGovernance/Audit/EvalSet/<EDITION>/`; extended retrieval check (informational) | versioned per edition |
| Release-ready flag (cloud) | P5 | `<BOOK>/manifest.json` → `auditFinalClear`, set only after `AUDIT_FINAL_CLEAR.md` | gate for external consumers |
| Publication check | P6.5 | RAG sub-certification per track (Local · Cloud) | gate |

**One chunk set, two vector spaces:** the tracks share chunk text, IDs, and metadata, never vectors. Changing a track's embedding model re-embeds every chapter for that track only.
**Chunk rule (all phases):** 500–1000 words · 100-word overlap (80–120 tolerated) · section name in metadata · never split a concept.
**Canonical terminology:** `_BookGovernance/Audit/Audit_CanonicalTerms.json` (PHASE 0.9, author-resolved) is the book-wide source for term forms and definitions; the TerminologyLock and GlossaryNormalized files follow it.
**Authority hierarchy (embedded in metadata):** PASS 7 Manuscript > GlossaryNormalized > LearningMetadata / FigureRegistry > derived artifacts. From PHASE 4 Part 0 on, "Manuscript" means the manuscript as synced to the final eBook PDF.

---

## 7. LLM map

| Model / tool | Role | Phases |
|---|---|---|
| Claude (Cowork) | Book audit, artifact generation, governance fixes, QA reports, Kindle compile, RAG build, recommendations | 0.9, 1, 2, 3.5, 3W (checks), 4, 5, 6.5, 7 (Part B) |
| Local LLM (Ollama) for the audit (optional) | PHASE 0.9 passes run chapter by chapter with a running ledger, so an 8k-context model can run them | 0.9 |
| Claude Design | DSM-bound HTML packet, layouts, exports; applies HTML fixes | 3 (and fixes from 3.5 / 6.5) |
| Ollama: drafting model (default Qwen2.5 14B Instruct) | Grounded marketing/design drafts | 5 (configure), 6 (run) |
| ONNX/TEI embedding container (default `nomic-ai/nomic-embed-text-v1.5`) | Local embeddings for `<RAG_COLLECTION>` (Track L); one model for all chapters | 5, 6 (query embeddings) |
| Governance gateway (optional, recommended; `<GATEWAY_URL>`) | Runs checks, then calls the embedding (and chat) deployments for Track C and cloud workflows | 5, 6 |
| Azure OpenAI (embedding deployment `text-embedding-3-large`; optional chat deployment) | Cloud embeddings for `<RAG_BLOB_CONTAINER>` (Track C) and query vectors; cloud-grounded drafting; reached through the gateway when one is configured | 5, 6 |
| Azure Blob Storage | Cloud vector store (private container; Entra ID, read-only for consumers) | 5, 6 |
| LM Studio (optional) | OpenAI-compatible endpoint for n8n | 5, 6 |
| XTTS (local) | **Draft** narration render: a pacing and timing guide, never published | 4 (Part C) |
| Adobe Audition (<AUTHOR>, manual) | Final audiobook narration: recording, editing, and mastering | 4 (Part C) |
| n8n / OpenClaw | Orchestration | 6 |

**Local-LLM context load order (8k window):** VoiceKit → TerminologyLock → Claims + Do-Not-Claim → Marketing rules → Design rules → Governance rules → RAG query rules → task.

---

## 8. Publishing map

| Channel | Source | Built in | Validated in | Released in |
|---|---|---|---|---|
| eBook PDF & EPUB | `_Masters/Manuscript_Master.html` ← chapter `eBook/` + DesignPacket | P3 | P3.5, P6.5 | P7 |
| Workbook eBook (PDF, 8.5×11) | Workbook manuscript → Claude Design workbook → <AUTHOR>'s InDesign workbook (in `<WORKBOOK_INDESIGN_ROOT>`) → uploaded PDF | P3 (design), P3W (<AUTHOR>; book: W4) | P3.5 (design), P3W W3/W5, P6.5 | P7 |
| Print book | Manual InDesign from Print 7×10 layouts + InDesign prep | P3 (<AUTHOR>) | P6.5 (package) | P7 |
| Workbook print (7×10, full color) | Same source, CMYK print export | P3W (<AUTHOR>; book: W4) | P3W W3/W5, P6.5 | P7 |
| Audiobook | <AUTHOR>'s narration (Adobe Audition) from the script built from the Kindle output; XTTS draft as a guide | P4 Part C (set: Part B) | P4 Part C, P6.5 | P7 |
| Kindle / KDP | Per-chapter Kindle build (P4 Part A) → book assembly (P4 Part B) | P4 | P6.5 | P7 (<AUTHOR> approves upload) |
| RAG (Local + Cloud) | Canonical chunk set → ChromaDB and Azure Blob Storage | P5 | P5, P6.5 | P7 |
| Marketing | Intake + Seeds → n8n/OpenClaw drafts | P1, P6 | P2, P6 tests | Per item, <AUTHOR> approval |
| Training / LMS / CMS | DesignPacket HTML + exports | P3, P6 (drafts) | P3.5 | P7 |
