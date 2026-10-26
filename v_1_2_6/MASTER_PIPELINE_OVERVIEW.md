# MASTER PIPELINE OVERVIEW

**Book:** *<BOOK_TITLE>* — <EDITION>
**Author:** <AUTHOR> · **Pipeline version:** v3.4 / release v1.2.6 (aligned 2026-10-26)
**Release v1.2.6 (2026-10-26): congruency check (PHASE 4 Step 0C).**
- **New Step 0C, pass 1**, after Part 0 / 0R / 0G / 0P and before Part A: `congruency_check.py <ChapterName> --pass 1` (deterministic, report-only). It puts the manuscript DOCX and MD, the eBook PDF, the print PDF, the narration script, the workbook's exercise numbers and titles, and every file's freshness against `MANUSCRIPT_LOCKED.md` into one report with a **PASS / HOLD** verdict. Part A starts only on PASS.
- **Pass 2**, after Part C, adds the Kindle DOCX and the audiobook QA, and gates PHASE 5 and 6.5.
- **Triggers:** automatic (the local watcher runs it when every input exists and nothing has changed for 5 minutes, and emails when the verdict is HOLD) or manual (`Manuscript/Trigger/RUN_CONGRUENCY.md`, or ask Claude).
- **Protected chapters** (the first book's Ch1 to Ch5, which have no lock) get the report only; it never holds them.
- Why: each pair of formats was checked alone; nothing combined them, and the script against the manuscript, file freshness, and the exercise numbers and titles were not checked at all.

**Release v1.2.5 (2026-10-24): the manuscript is locked before design (new PHASE 2.5).**
- **New PHASE 2.5, Manuscript Lock Audit** (`PHASE 2.5- Manuscript Lock Audit.md`), between PHASE 2 and PHASE 3. It runs PHASE 0.9's read-through passes on the governed chapter (Mode P, with the full content categories: definition conflicts, cross-references, term drift, list counts, glossary gaps, acronyms, heading anchors, figures).
  - <AUTHOR> decides every finding in the decisions log (`Manuscript/<ChapterName>_LockDecisions.md`).
  - Approved fixes go into the DOCX first; `docx_md_sync.py` then brings the MD in line.
  - It writes `Manuscript/Trigger/MANUSCRIPT_LOCKED.md`, recording the DOCX and MD hashes.
- **Every design and production phase requires the lock:** PHASE 3 (A0 included), 3.5, 3.5A, 3.5B, 3W, and 4 (Part 0, A, and C). A lock is stale if a hash no longer matches or `MANUSCRIPT_REVISED.md` is newer.
- **After the lock,** any change needs `MANUSCRIPT_REVISED.md` with <AUTHOR>'s approval line, then PHASE 1 (changed sections) → PHASE 2 → a PHASE 2.5 delta audit and a new lock.
- **PHASE 4 Part B, B0 (Mode D) is reduced** to a cross-chapter consistency check plus a check of what changed since each chapter's lock. It doesn't reopen a manuscript except for a genuine cross-chapter conflict, with <AUTHOR>'s approval.
- **The audiobook (Part C) is recorded only after the lock,** so no re-recording should be needed.
- Why: the full content audit used to run at B0, after the design packet, the eBook, the print IDMLs, and an audiobook recording already existed, so its fixes had to flow back through every format.

**Release v1.2.4 (2026-10-22): workbook eBook structure and print details.**
- The workbook eBook's page numbers follow the assembled eBook file; each page file's own default page matches it, and the final PDFs are exported tagged from it.
- Workbook write-in questions are Montserrat bold in the eBook, as in print. Hints stay Merriweather italic.
- Numbered questions lead with a color badge circle, in print and the eBook. Exercise openers show no page number.
- In "(see Figure N)", the "Figure N" takes the Caption Figure Roboto Mono character style in print (`figure-text` in the eBook).
- Every chapter starts on a right-hand page.

**Release v1.2.3 (2026-10-22): print and workbook refinements.**
- Print callouts, book and workbook, are separate objects copied from the book template's Body Page Spread C master. They are never inline in the body story, and the spacer after the eyebrow stays.
- Workbook how-to steps are roman, with parentheticals in italics.

**Release v1.2.2 (2026-10-22): design systems are the source.** Three Design System artifacts are the source for every export:
- the book eBook (`<EBOOK_DESIGN_SYSTEM>`);
- the workbook eBook (`<WORKBOOK_EBOOK_DESIGN_SYSTEM>`);
- the design packet (`<PACKET_DESIGN_SYSTEM>`).

Each eBook page links its system's tokens and components through `dsm_css.py` (PHASE 3.5B §3a). New components go into the system first, never into a page.

**Release v1.2.1 (2026-10-22): PHASE 3 starts automatically; print layout rules.**
- **PHASE 2 → PHASE 3 is automatic** (PHASE 3 A0). `GOVERNANCE_READY.md` starts:
  - the figure prompts file `Figures/<ChapterName>_FigurePrompts.md`: Gemini prompts, a figure checklist of RGB and CMYK files to make in Photoshop, and figure suggestions for the author;
  - the design packet, built as Claude artifacts from `<PACKET_DSM_ROOT>` (A2b; Claude Design is no longer required).
- **Print pagination and spacing rules** (PHASE 3.5B §2): no widows or orphans, facing pages aligned where possible, callouts and figures apart, 1 pica around callouts, figures, and captions.
- **Quoted speech is italic** in the eBook and print layouts.

**Release v1.2 (2026-10-22): eBook-first print build (IDML).**
- **New PHASE 3.5B.** The eBook is built first. The print documents are then generated as InDesign IDML files that replicate it:
  - the chapter (7×10), by `idml_chapter_build.py`, starting from <AUTHOR>'s last finished chapter IDML in `<PRINT_DSM_ROOT>`;
  - the workbook exercise (7×10), by `idml_workbook_build.py`, cloning the previous exercise's IDML.
- **Placement:** the chapter IDML goes to `<CH_ROOT>/InDesign/`, the exercise IDML to `<CH_ROOT>/Workbook/`. <AUTHOR> finishes them in InDesign (fonts, a final check) and exports the print PDFs as before.
- **Design rules (<AUTHOR>):**
  - one column only;
  - black, white, and gold;
  - no eBook motifs or extra colors, except the pull quotes and the print template's own multi-color callouts;
  - margins used end to end, and consistent spacing;
  - CMYK TIFF for print and RGB PNG/JPG for the eBook, never swapped;
  - `<PRINT_DSM_ROOT>` is the only print source, and `<EBOOK_DSM_ROOT>` is read on the print side for content only.
- **eBook tools:** `ebook_paginate.py` (fits blocks to 8.5×11 pages) and `ebook_print.py` (a print-ready PDF with a font check).
- **Proofs:** an optional structural proof through Adobe's InDesign rendering, with <AUTHOR>'s permission. Fonts are substituted on the render server.
- PHASE 3.5A (tagged text) stays available; 3.5B is the default print build.

**Release v1.1.3 (2026-10-21): print build.**
- **New PHASE 3.5A, print build (automated tagged text).** `idml_build.py` turns the chapter's manuscript DOCX into an InDesign tagged-text import, `<CH_ROOT>/InDesign/<ChapterName>_Import.txt`, styled with the print template's own styles through `<PRINT_DSM_ROOT>/style_map.json`. It also writes a build manifest (hashes of the template, style map, and DOCX) and a report. <AUTHOR> places the import into a copy of the template, finishes the layout by hand, and exports the print PDF as before.
- 3.5A never edits the manuscript, never writes to `<PRINT_DSM_ROOT>`, never calls InDesign, and never guesses an unmapped style. Its failures block only its own closure. PHASE 3.5 reads its report.
- **The manuscript is final before PHASE 1:** <AUTHOR> polishes in the DOCX before the PASS 7 drop (the polish window) and regenerates the MD. The layouts are built from it rather than edited for wording. PHASE 4 Part 0 stays as the safety check and expects no differences.
- **Figures:** finished before the eBook and print builds. RGB masters go in `Figures/RGB/` (PNG for illustrations, JPG for photos); CMYK print TIFFs go in `Figures/CMYK/`, which the print build requires.
- **Callouts** are not in the manuscript. PHASE 1 recommends them (`InDesign/<ChapterName>_CalloutRecommendations.md`), PHASE 2 validates them, and <AUTHOR> places the approved ones in the layouts.
- **Revision trigger:** `Manuscript/Trigger/MANUSCRIPT_REVISED.md` re-runs PHASE 1 for the changed sections, then PHASE 2 re-validates. PHASE 4 Part 0 stops if the trigger is newer than the eBook PDF.
- **Workbook print build** (PHASE 3W W1b): ships off by default.

**Release v1.1.2 (2026-10-03): print vs. eBook QA.** <AUTHOR> uploads each finished section's 7×10 print PDF to `<CH_ROOT>/InDesign/<ChapterName>_Print7x10.pdf` (workbook: `<WORKBOOK_BOOK_ROOT>/InDesign/`, or `<CH_ROOT>/Workbook/<ChapterName>_Workbook_Print*.pdf` in the `chapter` layout). A deterministic local check (PHASE 4 **Part 0P**; workbook: PHASE 3W **W2b**) compares its wording with the final eBook PDF and flags print-layout problems. It reports to `_BookGovernance/PrintQA/` and emails when the findings change. It is report-only and doesn't block Kindle, but it must be closed before PHASE 6.5 and PHASE 7. It replaces the self-reported print cross-check.

**Release v1.1 (2026-10-02): automation first.**
- **Uploads close PHASE 3.5.** <AUTHOR>'s uploads are what complete PHASE 3.5 and lock the text: the final eBook PDF locks the chapter manuscript, and the final workbook PDF locks the workbook manuscript.
- **Everything after an upload is triggered:**
  - manuscript sync and glossary lock (PHASE 4 Part 0 / 0G)
  - workbook sync (PHASE 3W W3)
  - Kindle build
  - RAG
  - automation
  - publication QA
  - a locally generated PHASE 7 release checklist, emailed to <AUTHOR> for the final human sign-off
- **References are verified.** PHASE 1 runs the check with safe auto-fixes before design; PHASE 4 Part 0R re-checks report-only after the lock.
- **The glossary follows a defining-chapter rule.** Its official master holds only locked chapters, and a drift report watches every chapter.
- **Extra workbook exercises are candidates** until <AUTHOR> selects them.
- **The step-by-step operating guide is `HOW_TO_RUN_THE_PIPELINE.md`.**
**Kindle decision (2026-09-22):** all Kindle work lives in PHASE 4, chapter by chapter, after the DesignPacket, figures, and the manual print/eBook work are finished and QA'd. PHASE 3 no longer produces a Kindle edition; `<BOOK>_KINDLE_EBOOK` is assembled in PHASE 4 Part B from the per-chapter builds.
**Dual RAG (2026-09-24):** PHASE 5 builds one canonical chunk set and embeds it into two vector stores: **Local** (ChromaDB + ONNX/TEI embeddings, Docker) and **Cloud** (vector files in Azure Blob Storage, embedded with Azure OpenAI `text-embedding-3-large` and searched in memory; multilingual). Each track has its own model, trigger, and index manifest; `RAG_READY.md` means every enabled track passed.
**The final eBook is the trigger (2026-09-27):** when <AUTHOR> finishes a chapter's eBook and exports its final PDF, the chapter is ready for everything that follows. PHASE 4 Part 0 syncs the manuscript to it, Part A builds Kindle from it, Part C records the audiobook from the Kindle output, and PHASE 5 onward read the synced text. The XTTS render is a draft; the final audiobook is <AUTHOR>'s own recording, made in Adobe Audition.
**Book audit (2026-09-27):** PHASE 0.9 audits the whole book for drift (terms, definitions, acronyms, equations, thresholds, lists, figures, cross-references, headings) on the draft **before PASS 7**, while wording is cheapest to change. Its author-resolved `Audit_CanonicalTerms.json` seeds PHASE 1 and PHASE 2. A **final delta audit** runs at PHASE 4 Part B (step B0) on the manuscripts synced to the final eBook PDFs, and gates the book's release-ready flag in the cloud RAG store.
**Workbook track (2026-09-30):** the workbook ships as an **eBook PDF** (8.5×11 in) and a **full-color print book** (7×10 in). **PHASE 3W** owns it end to end.
- The workbook manuscript follows the chapter manuscript's rule: the DOCX is canonical and the MD is its replica. `WORKBOOK_MANUSCRIPT_READY.md` (end of PHASE 2) confirms DOCX = MD before Claude Design builds the workbook in PHASE 3.
- <AUTHOR> then produces both formats in InDesign and uploads the PDFs in the profile's formats to its location (`Workbook/` or `<WORKBOOK_BOOK_ROOT>`), which is the cue that they're done. The W3 check syncs layout-time wording back to the DOCX and MD, and writes `WORKBOOK_READY.md` once PDF = DOCX = MD.
- No Kindle edition, no audiobook, no RAG ingestion.
- The book-level workbook is assembled after the final delta audit (B0), once exercise IDs and wording are frozen.
**Manuscript sync (2026-09-23):** PHASE 4 opens with Part 0, which brings the manuscript (MD and DOCX) into line with the final eBook PDF, because <AUTHOR> refines wording during InDesign layout. No eBook PDF, no PHASE 4, and nothing after it.

**Release v1.0.2 (2026-09-27):** dual RAG (PHASE 5 v4, PHASE 6 v4); the local embedding default is now `nomic-embed-text-v1.5` on an ONNX/TEI container, because the previous default truncated chunks at 256 tokens. The cloud track uses `text-embedding-3-large` with vectors stored in Azure Blob Storage (no search service), for multilingual retrieval at low cost. New PHASE 0.9 book-wide audit; the audiobook moved to PHASE 4 Part C (recorded from the Kindle output: XTTS draft, <AUTHOR>'s final narration in Adobe Audition); the final eBook PDF formally triggers each chapter's final-wording chain.

**Release v1.0.4 (2026-09-30):** governed cloud track. PHASE 5 v4.2 can embed Track C through a governance gateway (recommended), defaults cloud vectors to 1,024 dimensions, and adds `part`, `lesson`, `figureId`, and `altText` to the cloud vector lines. PHASE 6 v4.1 adds the §3G nightly RAG refresh, which re-ingests changed chapters into both stores and notifies cloud consumers.

**Release v1.0.3 (2026-09-30):** new PHASE 3W Workbook Track (eBook PDF + full-color print, InDesign only). The Kindle workbook (PHASE 4 B5), the workbook's RAG ingestion, and the HTML-built workbook eBook (`Workbook_Master.html`) are removed.

**Authority:** This file is the single reference for paths, gates, triggers, status, and deliverables. Each PHASE file points here. If a PHASE file disagrees with this overview, this overview wins, and the discrepancy is logged for correction.

---

## 1. PHASE 0.9–7 at a glance (with PHASE 2.5 from v1.2.5)

| Phase | File | Role | Entry gate | Exit gate | Runs |
|---|---|---|---|---|---|
| **0.9** Book audit | `PHASE 0.9- Book-Wide Manuscript Audit.md` | Report-only book-wide drift audit (extract → detect → eval questions → consolidation); canonical decisions for <AUTHOR>. **Mode F** before PASS 7; **Mode P** spot checks during PASS 7 and after a Part 0 sync; its passes run per chapter in **PHASE 2.5** (the lock audit); **Mode D** at PHASE 4 Part B is a cross-chapter consistency and since-lock delta check (v1.2.5) | Full draft in `<DRAFT_SOURCE>` (Mode F); every chapter `MANUSCRIPT_LOCKED.md` + `MANUSCRIPT_SYNCED.md` (Mode D) | `AUDIT_CLEAR.md` (F) · `AUDIT_FINAL_CLEAR.md` (D) | once per book, plus the final check |
| **1** Creation | `PHASE 1- Claude PASS 7 Markdown Script.md` | Generate every chapter artifact from the locked PASS 7 manuscript (Mode A new, Mode B retrofit) | PASS 7 locked + `AUDIT_CLEAR.md` | ProductionChecklist + Editorial Suggestions resolved + Marketing trigger | per chapter |
| **2** Governance | `PHASE 2- Governance Check of Outputs.md` | Validate, fix (Tier A/B), propose (Tier C), certify, stage the design handoff | PHASE 1 exit | `GOVERNANCE_READY.md` (certified Design Ready) | per chapter + batch |
| **2.5** Manuscript lock audit (v1.2.5) | `PHASE 2.5- Manuscript Lock Audit.md` | Full per-chapter content audit (PHASE 0.9 Pass 1 → Pass 2, Mode P with the full categories: definition conflicts, cross-references, term drift, list counts, glossary gaps, acronyms, heading anchors, figures) → decisions log → <AUTHOR> decides every finding → approved fixes applied to the DOCX, then the MD through `docx_md_sync.py` → delta re-check → lock with the DOCX/MD hashes | `GOVERNANCE_READY.md`; DOCX = MD; no pending `MANUSCRIPT_REVISED.md` section | `MANUSCRIPT_LOCKED.md` (Locked) | per chapter; again as a delta audit after an approved revision |
| **3** Design + Production | `PHASE 3- Claude Design Hand-off.md` | Claude Design HTML packet + exports + **figure image export**; manual eBook + print InDesign books; eBook/print book assembly (audiobook moved to PHASE 4) | `GOVERNANCE_READY.md` + **`MANUSCRIPT_LOCKED.md`** (v1.2.5; A0 starts from the lock) | Handoff to 3.5 | per chapter + book assembly |
| **3W** Workbook track | `PHASE 3W- Workbook Track (eBook + Print).md` | Workbook manuscript DOCX = MD gate (end of 2); Claude Design builds the workbook (3); <AUTHOR> produces the eBook (8.5×11) + print (7×10) PDFs in InDesign and uploads them; **W2b:** print QA on each print upload (v1.1.2; only if print ships); Claude syncs layout wording back (PDF = DOCX = MD) and checks the registry, preflight, and eBook. Book-level workbook assembled after B0. No Kindle, audiobook, or RAG | `GOVERNANCE_READY.md` + **`MANUSCRIPT_LOCKED.md`** (v1.2.5) → `WORKBOOK_MANUSCRIPT_READY.md`; the workbook PDFs in the profile's `formats` (eBook, plus print if listed) uploaded to the profile's `location` (`Workbook/` or `<WORKBOOK_BOOK_ROOT>`) | `WORKBOOK_READY.md` (per chapter); workbook assembly report (per book) | per chapter, then once per book |
| **3.5A** Print build (v1.1.3) | `PHASE 3.5A- Print Build (Automated Tagged Text).md` | Deterministic (`idml_build.py`): manuscript DOCX + `<PRINT_DSM_ROOT>/style_map.json` + `<PRINT_TEMPLATE_BOOK>` → styled InDesign tagged-text import, build manifest, report. Checks: styles exist, nothing unmapped, figures resolve, running heads set, template hash recorded. <AUTHOR> then places it, lays out, and exports the print PDF. Never edits the manuscript, writes to `<PRINT_DSM_ROOT>`, or calls InDesign | DOCX in `Manuscript/`, newer than `AUDIT_CLEAR.md`; **`MANUSCRIPT_LOCKED.md`** current (v1.2.5); `<PRINT_TEMPLATE_BOOK>` exists (`DESIGN_READY.md` not required) | `<ChapterName>_Import.txt` + `_BuildManifest.json` + `_BuildReport.md` with every check passing (failures block 3.5A closure only) | per chapter, on request; re-run when the DOCX, map, or template changes |
| **3.5B** eBook-first print build (v1.2) | `PHASE 3.5B- eBook-First Print Build (IDML).md` | The eBook page file is built and paginated first (`ebook_paginate.py`, `ebook_print.py`). Then the print IDMLs replicate it: the chapter (`idml_chapter_build.py`, from <AUTHOR>'s last finished chapter IDML) and the exercise (`idml_workbook_build.py`, cloning the previous exercise's IDML). It uses 1-column masters, CMYK TIFFs, and the print template's callouts, with an optional Adobe structural proof. It never edits the manuscript or writes to `<PRINT_DSM_ROOT>` | **`MANUSCRIPT_LOCKED.md`** current (v1.2.5); final DOCX; finished figures (RGB + CMYK); print template + last finished chapter/exercise IDML; the eBook page reviewed | `<CH_ROOT>/InDesign/<NNN>_Chapter<N>_<Title>.idml` and `<CH_ROOT>/Workbook/<NN>-<n>_Exercise_<L>_<N>_<Name>.idml` with every §8 check passing | per chapter / exercise |
| **3.5** Design QA | `PHASE 3.5- Claude QA of Design Artifacts.md` | Report-only QA → fix loop; **Kindle Readiness check (§13)** | PHASE 3 exit + **`MANUSCRIPT_LOCKED.md`** current (v1.2.5) | `DESIGN_READY.md` (Production Ready + Kindle Ready). **Completed by <AUTHOR>'s upload of the final eBook PDF** (book) / final workbook PDF (workbook) — v1.1 | per chapter |
| **4** Final-wording builds (Kindle + audiobook) | `PHASE 4- Kindle DOCX Chapter Compilation.md` | **Part 0:** sync check of the locked manuscript against the final eBook PDF (any difference needs <AUTHOR>'s decision, v1.2.5) · **0R:** references re-check (report-only) · **0G:** glossary lock + master glossary rebuild · **0P:** print vs. eBook QA on the uploaded print PDF (report-only, v1.1.2; closed before 6.5) · **Step 0C:** congruency check, pass 1 gates Part A, pass 2 gates PHASE 5 and 6.5 (v1.2.6) · **Part A:** Kindle DOCX + HTML + metadata + figures per chapter · **Part 0.7:** audit spot check (PHASE 0.9 Mode P) · **Part C:** narration refresh + XTTS audiobook per chapter, recorded only after the lock · **Part B:** B0 cross-chapter consistency + since-lock delta check (PHASE 0.9 Mode D, v1.2.5), then book-level `<BOOK>_KINDLE_EBOOK` and `<BOOK>_AUDIOBOOK` | **`MANUSCRIPT_LOCKED.md`** (Part 0, A, and C; v1.2.5) + `DESIGN_READY.md` + final eBook PDF uploaded (Part 0 writes `MANUSCRIPT_SYNCED.md`, which Step 0 / Part A then require) | Part A checklist PASS; Part B package complete | per chapter / section, then once per book |
| **5** RAG (Local + Cloud) + LLM | `PHASE 5- RAG Rebuild & Local LLM Setup (Per Chapter).md` | Canonical chunk set; Track L ChromaDB rebuild; Track C Blob vector file rewrite (if enabled); parity check; system prompt, query profiles | PHASE4 PASS + `MANUSCRIPT_SYNCED.md` | `RAG_LOCAL_READY.md` (+ `RAG_CLOUD_READY.md` if enabled) → `RAG_READY.md` | per chapter |
| **6** Automation | `PHASE 6- Automation Activation (n8n + Local LLM + RAG).md` | n8n + OpenClaw activation, drafts-only; each workflow grounded on the local or cloud index; §3G nightly RAG refresh keeps both stores in sync | `RAG_READY.md` | PHASE6 checklist PASS, status `active` | per chapter + batch |
| **6.5** Publication QA | `PHASE 6.5- Claude Design Publication QA.md` | Report-only QA of EPUB/Kindle/print/audio/RAG; print validated from the 0P / W2b print QA reports | PHASE6 PASS | Publishing Ready report | per chapter + book |
| **7** Release | `PHASE 7- Chapter Publishing Checklist.md` | **Local, automatic (v1.1):** deterministic validation of every Part A item with evidence, local-LLM recommendations from the gaps, emailed to <AUTHOR>; then <AUTHOR>'s sign-off | PHASE 6.5 finished (Publishing Ready to sign) | **Published** | per chapter |

```
PASS 6 (tighten) ─▶ 0.9 audit ─▶ PASS 7 (voice; pseudo-locked) ─▶ polish window (DOCX, then MD from it)
  ─▶ 1 ─▶ 2 ─▶ 2.5 lock audit (findings ─▶ <AUTHOR> decides ─▶ DOCX ─▶ docx_md_sync ─▶ MD) ─▶ MANUSCRIPT_LOCKED
  ─▶ 3 ─▶ 3.5 ─▶ eBook + print InDesign books (built from the locked text)
        ├─ 3.5B (v1.2, default): eBook page ─▶ print IDMLs (chapter + exercise) ─▶ InDesign finish ─▶ print PDF ─▶ 4 0P / 3W W2b
        ├─ 3.5A print build (after 1; DOCX + template ─▶ styled import) ─▶ manual print layout ─▶ print PDF ─▶ 4 0P
        └─ MANUSCRIPT_REVISED.md (after the lock: approved by <AUTHOR>) ─▶ 1 (changed sections) ─▶ 2 re-validates ─▶ 2.5 delta ─▶ new lock ─▶ 3.5A/3.5B re-run
        └─ 3W workbook: WORKBOOK_MANUSCRIPT_READY (end of 2) ─▶ Claude Design workbook (3) ─▶ InDesign eBook + print
                          ─▶ upload PDFs ─▶ W3 sync + check (PDF = DOCX = MD) ─▶ WORKBOOK_READY
  ─▶ 4: Part 0 sync + 0.7 spot check ─▶ Part A Kindle ─▶ Part C audiobook (script from the Kindle output; XTTS draft; <AUTHOR> records in Audition)
  ─▶ 5 ─▶ 6 ─▶ 6.5 ─▶ 7 ─▶ Published                               (per chapter)

  4 Part B, once every chapter has passed Part A and Part C:
  B0 cross-chapter consistency + since-lock delta ─▶ Kindle package + audiobook set ─▶ 6.5 book mode   (once per book)
                       └─▶ 3W W4–W5: workbook eBook + print books (after B0)

Fix loops: 2.5 finding → <AUTHOR>'s decision → DOCX → MD (before anything is designed); 0P / W2b print QA → print InDesign fix → re-export (wording that should reach the manuscript → MANUSCRIPT_REVISED.md + approval → eBook fix → Part 0 re-run); 3.5 → 3; 3W W3 → InDesign workbook fix (and DOCX → MD) → re-export → re-upload; 0.7 blocking finding → eBook (and print) InDesign fix → re-export → Part 0 re-run; B0 genuine cross-chapter conflict only → <AUTHOR> approves → MANUSCRIPT_REVISED.md → re-lock → eBook fix → Part 0 re-run; 6.5 → owner phase after approval.
```

---

## 2. Milestone map (status ladder)

One ladder is used by every phase:

`Draft → Review Ready → Design Ready → Locked → Production Ready → Publishing Ready → Published`

| Milestone | Awarded by | Evidence |
|---|---|---|
| Draft | PHASE 1 | Artifacts exist |
| Review Ready | PHASE 2 | Governance ran; blockers listed |
| **Design Ready** | PHASE 2 | ChapterCertification + `GOVERNANCE_READY.md` |
| **Locked** (v1.2.5) | PHASE 2.5 | Decisions log fully decided and applied + `MANUSCRIPT_LOCKED.md` (DOCX/MD hashes). Design and production start only from here |
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
| **PHASE 2.5 (per chapter; v1.2.5)** | Lock audit report (findings) | `<CH_ROOT>/Governance/<ChapterName>_LockAudit_<YYYYMMDD_HHMM>.md` + `.json` |
| | Decisions log (<AUTHOR>'s decision per finding, with what was applied) | `<CH_ROOT>/Manuscript/<ChapterName>_LockDecisions.md` |
| | Locked snapshot (DOCX + MD, for the B0 delta check) | `<CH_ROOT>/Manuscript/_Locked/<ChapterName>_Manuscript_v<chapterVersion>.docx` / `.md` |
| | Pass files + updated book ledger | `_BookGovernance/Audit/<YYYYMMDD>_L_<ChapterName>/` |
| | Lock trigger | `<CH_ROOT>/Manuscript/Trigger/MANUSCRIPT_LOCKED.md` |
| **PHASE 3** (+3.5) | <BOOK>_EBOOK_PDF&EPUB | `_BookPublication/<BOOK>_EBOOK/` |
| | <BOOK>_PRINT_BOOK (manual InDesign) | `_BookPublication/<BOOK>_PRINT_BOOK/` |
| | Exported figure images (PHASE 4 dependency) | `<CH_ROOT>/DesignPacket/figures_export/` |
| **PHASE 3.5A (per chapter; v1.1.3)** | Styled print import (InDesign tagged text) + build manifest + build report | `<CH_ROOT>/InDesign/<ChapterName>_Import.txt`, `_BuildManifest.json`, `_BuildReport.md` (workbook, if W1b is on: `<CH_ROOT>/Workbook/InDesign/<ChapterName>_Exercise<L.N>_*`) |
| **PHASE 3.5B (per chapter; v1.2)** | Chapter print IDML (7×10) + exercise print IDML (7×10), built from the eBook; optional structural proofs | `<CH_ROOT>/InDesign/<NNN>_Chapter<N>_<Title>.idml`; `<CH_ROOT>/Workbook/<NN>-<n>_Exercise_<L>_<N>_<Name>.idml`; `InDesign/_Proofs/`, `Workbook/_Proofs/` |
| **PHASE 3W (per chapter)** | Workbook manuscript: DOCX (canonical) + MD (replica), synced to the eBook PDF in W3 | `<CH_ROOT>/Workbook/<ChapterName>_Exercise<L.N>_Workbook.docx` / `.md` |
| | Workbook eBook PDF (8.5×11) + full-color print PDF (7×10, if `formats` lists print) (<AUTHOR>, InDesign), in the profile's `location` | `chapter`: `<CH_ROOT>/Workbook/<ChapterName>_Workbook_eBook.pdf` + `_Workbook_Print.pdf`; `book-root`: `<WORKBOOK_BOOK_ROOT>/<section>/<NN>_Ex_<L>_<N>_Chapter<C>.pdf` + `<WORKBOOK_BOOK_ROOT>/InDesign/<eBook stem>_Print7x10.pdf` |
| | Workbook QA report | `<CH_ROOT>/Governance/<ChapterName>_WorkbookQA_<YYYYMMDD_HHMM>.md` |
| | Exercise registry (book-wide, updated per chapter) | `_BookGovernance/Workbook/Workbook_ExerciseRegistry.json` |
| **PHASE 3W (per book, after B0)** | <BOOK>_WORKBOOK_EBOOK (PDF) + assembly report | `_BookPublication/<BOOK>_WORKBOOK_EBOOK/` |
| | <BOOK>_WORKBOOK_PRINT_BOOK (full-color print PDF + cover) | `_BookPublication/<BOOK>_WORKBOOK_PRINT_BOOK/` |
| **PHASE 4 (Part 0, per chapter)** | Manuscript MD + DOCX synced to the final eBook PDF | `<CH_ROOT>/Manuscript/<ChapterName>_Manuscript.md` / `.docx` |
| | Manuscript sync report | `<CH_ROOT>/Manuscript/<ChapterName>_ManuscriptSync_<YYYYMMDD_HHMM>.md` |
| **PHASE 4 (Part 0P, per chapter or section; v1.1.2)** | Print PDF (<AUTHOR>'s upload, the input) | `<CH_ROOT>/InDesign/<ChapterName>_Print7x10.pdf`; front matter `FrontMatter/Final/<Section>/InDesign/<Section>_Print7x10.pdf` |
| | Print QA report | `_BookGovernance/PrintQA/<ChapterName>_PrintQA.md` + `.json` |
| | Print-only differences (<AUTHOR>) | `<CH_ROOT>/<ChapterName>_PrintOnlyDifferences.md` |
| **PHASE 4 (Step 0C, per chapter or section; v1.2.6)** | Congruency report, pass 1 and pass 2 | `_BookGovernance/CongruencyQA/<ChapterName>_Congruency.md` + `.json`; pass 2: `<ChapterName>_Congruency_Pass2.md` + `.json` |
| | Reviewed differences (<AUTHOR>, via `--accept`) | `_BookGovernance/CongruencyQA/<ChapterName>_Accepted.json` |
| **PHASE 3W W2b (print workbook only; v1.1.2)** | Workbook print PDF + print QA report | `book-root`: `<WORKBOOK_BOOK_ROOT>/InDesign/<eBook stem>_Print7x10.pdf` → `_BookGovernance/PrintQA/Workbook_<eBook stem>_PrintQA.md` (whole workbook: `Workbook_PrintQA.md`); `chapter`: `<CH_ROOT>/Workbook/<ChapterName>_Workbook_Print*.pdf` → `<ChapterName>_Workbook_PrintQA.md` |
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
| **PHASE 7** | Validation of outputs · checklist of all content · <AUTHOR>'s sign-off with LLM recommendations | `<CH_ROOT>/<ChapterName>_PHASE7_ReleaseChecklist.md` → copy in `_FinalizedReleases/` (report-only copies for protected chapters: `_BookGovernance/ReleaseChecks/`) |
| **PHASE 1 10b / PHASE 4 0R (v1.1)** | References check report (per chapter) | `_BookGovernance/References/<ChapterName>_ReferencesCheck.md` + `.json` |
| **PHASE 4 0G (v1.1)** | Official master glossary (locked chapters only) + drift report | `_BookGovernance/Glossary/Master_Glossary.json` / `.md`, `Glossary_DriftReport.md` |
| | Glossary defining-chapter decisions (<AUTHOR>) | `_BookGovernance/Glossary/Glossary_Canonical.json` |
| **PHASE 1 Step 2 (v1.1)** | Workbook candidate selection (<AUTHOR> ticks) | `<CH_ROOT>/_Pipeline/WORKBOOK_SELECTION.md` |

The eBook and print deliverables are assembled in PHASE 3 *book assembly mode* once every chapter is Production Ready. **The workbook's two deliverables are assembled in PHASE 3W (W4)**, after the final delta audit (B0), so exercise IDs and manuscript wording can't move under them. **The audiobook is recorded per chapter in PHASE 4 Part C and assembled in Part B**: it is recorded from the Kindle output, which is built from the final eBook. **<BOOK>_KINDLE_EBOOK is assembled in PHASE 4 Part B**, after every chapter's Kindle build passes, because Kindle depends on the finished figures and the completed print/eBook work. PHASE 6.5 validates the package; <AUTHOR> approves the KDP upload in PHASE 7.

Per-chapter phase records (all at `<CH_ROOT>` root unless noted):
`_ProductionChecklist.md` (P1) · `Governance/_ChapterCertification.md` (P2) · `Governance/_LockAudit_<ts>.md` + `Manuscript/_LockDecisions.md` (P2.5) · `Governance/_DesignQA_<ts>.md` (P3.5) · `Governance/_WorkbookQA_<ts>.md` (P3W) · `_PHASE4_KindleChecklist.md` · `_PHASE5_RAGChecklist.md` · `_PHASE6_AutomationChecklist.md` · `Governance/_PublicationQA_<ts>.md` (P6.5) · `_PHASE7_ReleaseChecklist.md`

---

## 4. Folder map

**Book root:** `<BOOK_ROOT>` — your book's root folder, e.g. `D:\Books\<BOOK_SLUG>`. Every path below is relative to it.
**Chapter root:** `<CH_ROOT>` = `<BOOK_ROOT>/Chapters/<ChapterName>/Final/`
**Chapter name:** `Ch<N>_<PascalCaseTitle>` (e.g. `Ch1_YourChapterTitle`)
**Print InDesign book:** <AUTHOR> may keep the print InDesign book (INDB, linked assets) in separate print folders outside `<BOOK_ROOT>`. The print templates (IDML), the print DSM, and `style_map.json` live in `<PRINT_DSM_ROOT>` (`<BOOK_ROOT>/_PrintDSM`). Phases read `<PRINT_DSM_ROOT>` only through PHASE 3.5A and 3.5B, and never write to it. The eBook design system lives in `<EBOOK_DSM_ROOT>` (`<BOOK_ROOT>/_eBookDSM`); the print build reads it for content only (v1.2). From v1.1.2, the exported print PDF is uploaded to `<CH_ROOT>/InDesign/<ChapterName>_Print7x10.pdf`, and PHASE 4 Part 0P checks it against the eBook PDF. The final **eBook** PDF stays the only layout text PHASE 4 Part 0 syncs the manuscript to.
**Workbook InDesign files:** <AUTHOR> keeps them (documents, INDB, links, fonts) in `<WORKBOOK_INDESIGN_ROOT>`, outside `<BOOK_ROOT>` (for example, OneDrive). No phase reads them; PHASE 3W checks only the exported PDFs uploaded to the workbook profile's location, `Workbook/` or `<WORKBOOK_BOOK_ROOT>` (eBook 8.5×11 in; print 7×10 in, if the profile lists it).
**File names:** `<ChapterName>_<ArtifactType>.<ext>`; Marketing: `<ChapterName>_MKT_<Type>.<ext>`; Claude Design project files: `Ch<N>_<Type>.dc.html` (accepted exception)

```
<BOOK_ROOT>/
├── _ClaudeInstructions/          PHASE prompts, this overview, _Backups/, _Superseded/
├── _BookMarketing/               VoiceKit.md (book-level voice)                    [P1]
├── _BookGovernance/              cross-chapter reports, master glossary, book QA   [P2, P6.5]
│   ├── Audit/                    config, canonical terms, EvalSet/, <RUN_ID>/ (incl. <date>_L_<ChapterName>/ lock runs), Trigger/ [P0.9, P2.5]
│   ├── PrintQA/                  <Section>_PrintQA.md + .json, Workbook_*_PrintQA.md [P4 0P, P3W W2b]
│   ├── CongruencyQA/             <Section>_Congruency.md + .json (+ _Pass2), <Section>_Accepted.json [P4 Step 0C, v1.2.6]
│   └── Workbook/                 Workbook_ExerciseRegistry.json                    [P3W]
├── _PrintDSM/                    <PRINT_DSM_ROOT>: print templates (IDML), finished chapter IDMLs, print DSM, style_map.json — READ-ONLY [read by P3.5A, P3.5B]
├── _eBookDSM/                    <EBOOK_DSM_ROOT>: eBook design system + Chapter<N>_eBook.dc.html pages [P3, P3.5B]
├── _BookPublication/             six book deliverables + _Masters/                 [P3 assembly, P3W, P4 Part B, P6.5]
├── _BookAutomation/              AutomationIndex.json, n8n/, OpenClaw/, Notices/   [P6]
├── _FinalizedReleases/           signed PHASE 7 checklists                         [P7]
├── _Archive/<ChapterName>/       drafts moved at release                           [P7]
├── FrontMatter/Final/<Section>/  {Audiobook, eBook, Kindle}/                       [P3, P4]
├── Parts/<NNN>_<Part>/Kindle/                                                      [P4]
├── BackMatter/<Section>/         {Audiobook, eBook, Kindle}/                       [P3, P4]
└── Chapters/<ChapterName>/
    ├── Final/
    │   ├── Manuscript/           PASS 7 copy, EditorialSuggestions [P1]; LockDecisions, _Locked/ snapshot, Trigger/MANUSCRIPT_LOCKED.md [P2.5]; Trigger/MANUSCRIPT_REVISED.md (<AUTHOR>, v1.1.3); synced to eBook PDF, ManuscriptSync report, Trigger/ [P4 Part 0]
    │   ├── ReviewPacket/  Training/  ReferenceGuides/  Slides/                     [P1; exports P3]
    │   ├── Workbook/             packet, workbook manuscript DOCX (canonical) + MD [P1]; Trigger/ [P2 → P3W]; exercise print IDML, _Proofs/ [P3.5B]; eBook + print PDFs [P3W]
    │   ├── Equations/                                                              [P1]
    │   ├── eBook/                HTML blocks + metadata [P1]; PDF/EPUB exports [P3]; final eBook PDF (required by P4 Part 0)
    │   ├── Kindle/               DOCX, HTML, metadata, figures/                    [P4]
    │   ├── InDesign/             prep [P1]; _Import.txt, _BuildManifest.json, _BuildReport.md [P3.5A]; chapter print IDML, _Proofs/ [P3.5B]; print PDF <ChapterName>_Print7x10.pdf (<AUTHOR>) [P3 → P4 0P]
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
| **Final eBook PDF** `<ChapterName>_eBook.pdf` (or `_eBookPDF.pdf`; newer than `MANUSCRIPT_SYNCED.md`) — **completes PHASE 3.5 (v1.1)** | `eBook/` | <AUTHOR> (final export) | P4 Part 0 (after 30 quiet minutes); P6 3F watcher (notify only) |
| **Final workbook PDF** `<NN>_Ex_<L>_<N>_Chapter<C>.pdf` (v1.1 option) — completes PHASE 3.5 for the workbook | `<WORKBOOK_BOOK_ROOT>/<section>/` | <AUTHOR> (final export) | P3W W3 (after 30 quiet minutes) |
| `WORKBOOK_SELECTION.md` (ticked) | `_Pipeline/` | P1 (candidates) → <AUTHOR> | P2 workbook selection |
| `Glossary_Canonical.json` | `_BookGovernance/Glossary/` | <AUTHOR> | P2 glossary; P4 0G; glossary rollup |
| `AUDIT_CLEAR.md` / `AUDIT_INCOMPLETE.md` | `_BookGovernance/Audit/Trigger/` | P0.9 Mode F | P1 entry; P3.5A entry (the DOCX must be newer) |
| `RUN_CONGRUENCY.md` (v1.2.6): optional first line `pass 2`; renamed `RUN_CONGRUENCY_done_<timestamp>.md` after the run | `Manuscript/Trigger/` (Parts: `Trigger/`) | <AUTHOR> | The watcher runs the congruency check now |
| `MANUSCRIPT_LOCKED.md` / `MANUSCRIPT_LOCK_INCOMPLETE.md` (v1.2.5): run ID, chapter version, DOCX and MD SHA-256 hashes, finding and decision counts, decisions log, snapshot | `Manuscript/Trigger/` | P2.5 (once every finding is decided and applied, DOCX = MD) | Entry gates of P3 (A0 starts from it), P3.5, P3.5A, P3.5B, P3W, P4 Part 0/A/C; P4 B0 (since-lock delta). **Stale** when a hash no longer matches the files or `MANUSCRIPT_REVISED.md` is newer |
| `<ChapterName>_LockDecisions.md` (v1.2.5): one row per finding, blank **Decision** column | `Manuscript/` | P2.5 (rows) → <AUTHOR> (decisions), then `_Pipeline/RERUN_P2.5.md` | P2.5 apply run |
| `MANUSCRIPT_REVISED.md` (v1.1.3): changed sections + reason, one dated section per revision; **after the lock, each section carries <AUTHOR>'s `Approved: <initials> <date>` line** (v1.2.5) | `Manuscript/Trigger/` | <AUTHOR> (after PHASE 1; DOCX edited, MD brought in line with `docx_md_sync.py`) | P1 re-run from Step 1 for the changed sections → P2 re-validation → P2.5 delta audit + new lock; P3.5A / 3.5B re-run; P4 Part 0 stop (if newer than the eBook PDF: re-export) |
| `<ChapterName>_Import.txt` + `_BuildManifest.json` + `_BuildReport.md` (v1.1.3) | `InDesign/` | P3.5A (`idml_build.py`) | <AUTHOR> (place into a copy of the template; manual layout); P3.5 §13A print-build review |
| `<NNN>_Chapter<N>_<Title>.idml` / `<NN>-<n>_Exercise_<L>_<N>_<Name>.idml` (v1.2) | `InDesign/` / `Workbook/` | P3.5B (`idml_chapter_build.py`, `idml_workbook_build.py`) | <AUTHOR> (open in InDesign, fonts, finish, export the print PDF → P4 0P / P3W W2b) |
| `AUDIT_FINAL_CLEAR.md` / `AUDIT_FINAL_INCOMPLETE.md` | `_BookGovernance/Audit/Trigger/` | P0.9 Mode D (P4 B0: cross-chapter consistency + since-lock delta, v1.2.5) | P4 Part B; P5 cloud release-ready flag; P6.5 book mode; P7 |
| `MARKETING_READY.md` / `_INCOMPLETE` | `Marketing/Trigger/` | P1, re-validated P2 | P6 3A marketing workflows |
| `GOVERNANCE_READY.md` / `_INCOMPLETE` | `Governance/Trigger/` | P2 | **P2.5 entry (automatic, v1.2.5)**; P3 entry together with `MANUSCRIPT_LOCKED.md`: A0 figure prompts + checklist → `Figures/<ChapterName>_FigurePrompts.md`, then the design packet (needs `<PACKET_DSM_ROOT>/DSM_APPROVED.md`), automatic from v1.2.1 and started by the lock from v1.2.5; P6 3C |
| `WORKBOOK_MANUSCRIPT_READY.md` / `WORKBOOK_MANUSCRIPT_INCOMPLETE.md` | `Workbook/Trigger/` | P3W W0 gate (end of P2) | P3 workbook design |
| **Workbook PDFs** in the profile's `formats` (`chapter`: `<ChapterName>_Workbook_eBook.pdf` + `_Workbook_Print.pdf`; `book-root`: `<NN>_Ex_<L>_<N>_Chapter<C>.pdf` + `InDesign/<eBook stem>_Print7x10.pdf`) (newer than `WORKBOOK_READY.md`) | `Workbook/` or `<WORKBOOK_BOOK_ROOT>` (profile `location`) | <AUTHOR> (final exports from InDesign) | P3W W3 |
| `WORKBOOK_READY.md` / `WORKBOOK_INCOMPLETE.md` | `Workbook/Trigger/` | P3W W3 | P3W W4 (every chapter); P6.5 workbook sub-cert; P7 |
| `DESIGN_READY.md` / `_INCOMPLETE` | `DesignPacket/Trigger/` | P3.5 | P4 entry; P6 3B/3D |
| `MANUSCRIPT_SYNCED.md` / `MANUSCRIPT_SYNC_INCOMPLETE.md` | `Manuscript/Trigger/` | P4 Part 0 | P4 Step 0; P4 Part B; P5 entry |
| **Print PDF** `<ChapterName>_Print7x10.pdf` (v1.1.2; workbook: `<WORKBOOK_BOOK_ROOT>/InDesign/<eBook stem>_Print7x10.pdf`, or `Workbook/<ChapterName>_Workbook_Print*.pdf` in the `chapter` layout) | `InDesign/` | <AUTHOR> (print export: 7×10, bleed, no printer's marks) | P4 0P / P3W W2b print QA (after 5 quiet minutes; re-runs when the print or eBook PDF changes); P6.5; P7 |
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
| Claude (Cowork) | Book audit, artifact generation, governance fixes, lock audit, QA reports, Kindle compile, RAG build, recommendations | 0.9, 1, 2, 2.5, 3.5, 3W (checks), 4, 5, 6.5, 7 (Part B) |
| Local LLM (Ollama) for the audit (optional) | PHASE 0.9 passes run chapter by chapter with a running ledger, so an 8k-context model can run them | 0.9 |
| Local LLM (Ollama, e.g. phi4 14B) — v1.1 | PHASE 7 Part B recommendations (from the unmet checks only); writing/voice checks; grounded chat over the book | 7 (+ tools) |
| Deterministic local tools (no LLM) — v1.1 | References check (Crossref), glossary rollup + drift, print vs. eBook QA (v1.1.2), print build to tagged text (`idml_build.py`, v1.1.3), eBook pagination and print (`ebook_paginate.py`, `ebook_print.py`, v1.2), print IDML builds (`idml_chapter_build.py`, `idml_workbook_build.py`, v1.2), DOCX → MD replica sync (`docx_md_sync.py`, v1.2.5), PHASE 7 Part A evidence | 1, 2.5, 3W, 3.5A, 3.5B, 4, 7 |
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

---

## 9. Automation layer (v1.1)

Every step after one of <AUTHOR>'s uploads is started by an event, not by pasting a prompt. Three pieces do the work:

| Piece | What it does |
|---|---|
| **Orchestrator: n8n** (the "Chapter Pipeline" workflow) | Watches for files and runner events, decides what runs next, and emails <AUTHOR>. It never edits book files. |
| **Runner** (a scheduled script) | Runs one job at a time: Claude headless for the generative phases (1, 2, 2.5, 3W, 4, 5, 6, 6.5), or a local tool (PHASE 7). It re-checks each entry gate, enforces protected chapters, and reports results back to n8n. |
| **Local tools** (`<LOCAL_TOOLS_ROOT>`, run on a schedule by the local orchestrator) | Deterministic checks plus the local LLM: references check, glossary rollup and drift, print QA (`print_check.py`, v1.1.2), release check, audiobook QA, writing/voice check. These are report-only, so they may cover every chapter. The PHASE 3.5A print build (`idml_build.py`, v1.1.3) also runs here, on request; it writes only to the chapter's `InDesign/` folder. So do the PHASE 3.5B builds (v1.2), on request; they write only to the chapter's `InDesign/` and `Workbook/` folders and the eBook page files. |

| Event (made by) | Automation | Output · email |
|---|---|---|
| `Ch<N>_<Title>.md/.docx` in `<PASS7_SOURCE>` (<AUTHOR>) | PHASE 1, incl. Step 10b references check with safe fixes | Artifacts, Editorial Suggestions, `WORKBOOK_SELECTION.md` · "review, select, approve" |
| `_Pipeline/APPROVE_EDITORIAL.md` (<AUTHOR>) | PHASE 2, incl. workbook selection, W0 gate, design staging | `GOVERNANCE_READY.md` · only if it needs <AUTHOR> |
| PHASE 2 PASS (`GOVERNANCE_READY.md`) — v1.2.5 | PHASE 2.5 audit run | `<ChapterName>_LockDecisions.md` · "decide the lock-audit findings" (or the lock, if there are none) |
| `_Pipeline/RERUN_P2.5.md` after the decisions (<AUTHOR>) — v1.2.5 | PHASE 2.5 apply run: DOCX, `docx_md_sync.py`, delta re-check, lock | `MANUSCRIPT_LOCKED.md` · "manuscript locked; start PHASE 3 / 3.5", or what is open |
| Final eBook PDF in `eBook/` (<AUTHOR>; completes 3.5; needs a current `MANUSCRIPT_LOCKED.md`, v1.2.5) | PHASE 4: Part 0 sync → 0R references → 0G glossary lock → Part A Kindle | `MANUSCRIPT_SYNCED.md`, Kindle files, master glossary · only if it needs <AUTHOR> (`_Pipeline/P4_DECISIONS.md`) |
| Every input of a section present (manuscript DOCX + MD, eBook PDF, print PDF, narration script) and unchanged for 5 minutes, or `RUN_CONGRUENCY.md` — v1.2.6 | PHASE 4 Step 0C congruency check, pass 1 (local `congruency_check.py`, report-only); pass 2 once the Kindle DOCX and the MP3 QA exist | `_BookGovernance/CongruencyQA/<ChapterName>_Congruency.md` · email only on HOLD |
| Final workbook PDF (<AUTHOR>; completes 3.5 for the workbook) | PHASE 3W W3 sync + check | `WORKBOOK_READY.md` · "workbook locked", or `_Pipeline/P3W_DECISIONS.md` |
| PHASE 4 PASS → PHASE 5 PASS → PHASE 6 PASS | PHASE 5 → 6 → 6.5, chained | Each phase emails only when <AUTHOR> is needed |
| PHASE 6.5 finished | PHASE 7 local release check | Pre-filled checklist · "what's missing" or "ready for sign-off" |
| Print PDF uploaded to `InDesign/` (chapter, front matter, or `<WORKBOOK_BOOK_ROOT>/InDesign/`) or as `Workbook/<ChapterName>_Workbook_Print*.pdf`, or the matching eBook PDF re-exported (<AUTHOR>) — v1.1.2 | Print QA, `print_check.py` (PHASE 4 0P / 3W W2b; report-only; after 5 quiet minutes) | `_BookGovernance/PrintQA/<Section>_PrintQA.md` + `.json` · email when the findings change, or if the check fails |
| Any manuscript, glossary, or `GLOSSARY.docx` change | References re-check (report-only) · glossary rollup | Reports in `_BookGovernance/` · email when the findings change |
| `_Pipeline/RERUN_P<n>.md` (<AUTHOR>; `<n>` = 1, 2, 2.5, 3W, 4, 5, 6, 6.5, 7) | Re-runs that phase; notes inside go to Claude | As for that phase |

Manual by design: PHASE 0.9; PHASE 3 and 3.5 (Claude Design, InDesign); the audiobook recording (PHASE 4 Part C); book assembly (PHASE 3 book mode, 3W W4–W5, PHASE 4 Part B); every approval; and the PHASE 7 sign-off.
