# Changelog

All notable changes to the Fluxline RCF Book Pipeline.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions are folders in this repository; each release keeps its predecessors intact so an in-flight book can finish on the version it started with.

---

## [v1.0.3] — 2026-09-30

**Folder:** `v_1_0_3/` · **Previous:** `v_1_0_2/` (tag `v1_0_2_PROD`, unchanged, kept for books mid-flight)

The workbook gets its own track. It ships in two formats only: an **eBook PDF** (8.5×11 in) and a **full-color print book** (7×10 in). Claude Design builds the workbook from the workbook manuscript, and the author produces both formats in InDesign alongside PHASE 3 / 3.5. The workbook manuscript now follows the chapter manuscript's rule (the DOCX is canonical, the MD is its replica), and by the end the PDF, DOCX, and MD match word for word. Before this release, the workbook's steps were spread across seven phases, and several of them assumed things this workbook doesn't have: an HTML-built eBook, a Kindle edition, and RAG ingestion.

### Added

- **PHASE 3W — Workbook Track (eBook + Print) (new file).**
  - **W0:** the workbook manuscript, `<ChapterName>_Exercise<L.N>_Workbook.docx` (canonical) + `.md` (replica). At the end of PHASE 2, the **`WORKBOOK_MANUSCRIPT_READY.md`** gate confirms DOCX = MD and registers the exercise IDs. The PHASE 3 workbook design waits for it.
  - **W1:** Claude Design builds the workbook from the workbook manuscript; the author produces both formats from it in InDesign.
    - eBook: 8.5×11 in RGB PDF, printable at home but not meant for it.
    - Print: 7×10 in, full color, CMYK PDF/X-4, with bleed and write-in space.
  - **W2:** the author uploads `<ChapterName>_Workbook_eBook.pdf` and `_Workbook_Print.pdf` to `Workbook/`. **The upload is the cue** that the chapter's workbook is done.
  - **W3:** syncs layout-time wording from the eBook PDF back into the DOCX, then regenerates the MD (with a backup and a change log; uncertain items go to the author). It confirms **PDF = DOCX = MD**, then checks print/eBook match, the exercise registry, print preflight, and the eBook. The result is `WORKBOOK_READY.md` or `WORKBOOK_INCOMPLETE.md`.
  - **W4–W5:** the book-level workbook, assembled after PHASE 4 B0 (`AUDIT_FINAL_CLEAR.md`) so exercise IDs and wording are frozen, plus an assembly report.
- **Companion workbook manuscripts** (optional): `<ChapterName>_Exercise<L.N>_<Part>_Workbook.docx` + `.md` for extra pages of the same exercise, such as write-in journal pages. They follow the same DOCX = MD rule and gates.
- **Exercise registry** `_BookGovernance/Workbook/Workbook_ExerciseRegistry.json`. Exercises are numbered by Lesson (e.g. `Exercise 1.4` in Chapter 4). A manuscript mention with no matching exercise is blocking.
- **`WORKBOOK_MANUSCRIPT_READY.md`** (before PHASE 3) and **`WORKBOOK_READY.md`** (after the PDFs, PDF = DOCX = MD) triggers in `Workbook/Trigger/`, each with an `_INCOMPLETE` counterpart. `WORKBOOK_READY.md` doesn't block `DESIGN_READY.md` or PHASES 4–6; they're required for PHASE 6.5's new **Workbook** sub-certification and for PHASE 7.
- **Workbook triggers are bound to their files.** Each READY file records the SHA-256 hashes of what it certifies, and consumers treat it as stale if a hash differs. Every re-run renames the previous READY file to `_superseded_<timestamp>` before writing its result, so a failed re-upload can't leave an old READY standing.
- **PHASE 7:** a Workbook Approved sign-off, and PHASE 3W in the completion rule.
- **`<WORKBOOK_INDESIGN_ROOT>`** placeholder: the workbook InDesign files, INDB, links, and fonts stay outside `<BOOK_ROOT>` (for example, OneDrive), and no phase reads them.

### Changed

- **PHASE 2 (v3.2):** writes the `WORKBOOK_MANUSCRIPT_READY.md` gate in the same run as `GOVERNANCE_READY.md`.
- **PHASE 3 (v3.2):** Claude Design builds the workbook from the workbook manuscript once `WORKBOOK_MANUSCRIPT_READY.md` exists, and the workbook's production track points to PHASE 3W. The book-level workbook deliverables are assembled in PHASE 3W, not in PHASE 3 book assembly.
- **PHASE 3.5 (v3.2):** still reviews the Claude Design workbook, and confirms its exercise text matches the workbook manuscript. The workbook PDFs are checked in PHASE 3W. The Kindle Readiness item covers only the exercise text the Kindle book carries.
- **PHASE 4 (v3.2):** the Part 0 downstream impact list checks exercise IDs against the registry.
- **PHASE 6.5 (v3.2):** certifies the workbook from the PHASE 3W reports, with new Workbook score, findings, and sub-certification lines.
- **PHASE 7 (v3.2):** gains a PHASE 3W section and the Workbook sub-certification.
- **PHASE 1 (v3.2):** Step 2 names the workbook files and creates the workbook manuscript's MD replica.
- **`MASTER_PIPELINE_OVERVIEW.md`:** 3W appears in the flow, phase table, deliverable map, folder map, trigger map, publishing map, and LLM map.
- **`PLACEHOLDERS.md`:** new token; the workbook eBook page size (8.5×11 in) is listed as a changeable example; the scripts point at `v_1_0_3/`. The bash script also gains the `<PASS7_SOURCE>` replacement it was missing.

### Removed

- **PHASE 4 B5 Kindle workbook.** There is no Kindle workbook.
- **The workbook as a RAG input** (PHASE 5 v4.1), and `RAG_Workbook.html`. The manuscript still carries each chapter's main exercise text.
- **The HTML-built workbook eBook** (`_Masters/Workbook_Master.html` → PDF/EPUB), and the workbook EPUB.

---

## [v1.0.2] — 2026-09-27

**Folder:** `v_1_0_2/` · **Previous:** `v1_0/` (tag `v1_0_1_PROD`, unchanged, kept for books mid-flight)

The RAG layer now supports two vector stores: a private local one and an optional cloud one. Both are built from the same chunks, and neither can drift from the manuscript unnoticed. Found while running PHASES 4–5 on a real chapter.

A new PHASE 0.9 audits the **whole book** for drift before PASS 7 and again at the end, because the RAG stores (and any product built on them) inherit every inconsistency between chapters.

### Added

- **PHASE 0.9 — Book-Wide Manuscript Audit (new file).** A report-only, chapter-by-chapter audit with a running ledger, so a local 8k-context model can run it. Pass 1 extracts, Pass 2 detects drift in eleven categories with a blocking/major/minor severity, Pass 3 writes evaluation questions, and a Consolidation pass produces the canonical decisions list and a glossary delta. It has three modes:
  - **F — Full:** runs on the draft before PASS 7 → `AUDIT_CLEAR.md`, which PHASE 1 now requires.
  - **P — Spot check:** re-runs Pass 2 on a chapter whose PASS 7 edits touch a canonical item, and runs Passes 1–2 after every PHASE 4 Part 0 sync (step 0.7).
  - **D — Final delta:** runs at PHASE 4 Part B, step B0, on the manuscripts synced to the final eBook PDFs. It re-checks only chapters changed since their spot check, then consolidates the whole book → `AUDIT_FINAL_CLEAR.md`.
- **`Audit_CanonicalTerms.json`** (author-resolved) becomes the book-wide terminology authority. PHASE 1 seeds each TerminologyLock from it, and PHASE 2 flags any glossary entry that differs from it as Tier C.
- **`Audit_Config.json`** holds the canonical-term seed list, the known corrections, and `glossaryStatus`. A `stale` glossary produces review items, never blockers.
- **Evaluation set** (Pass 3), versioned per edition in `_BookGovernance/Audit/EvalSet/<EDITION>/`. PHASE 5 adds an informational extended retrieval check from it.
- **Cloud release-ready flag.** The Blob `manifest.json` gets an `auditFinalClear` entry, set only after the final delta audit. External consumers serve the book only while it is set.
- PHASE 4 Part B, PHASE 6.5 book mode, and PHASE 7 now check `AUDIT_FINAL_CLEAR.md`.
- **`<DRAFT_SOURCE>`** placeholder token.
- **PHASE 4 Part C (Audiobook), after Part A.** The narration script is built from the Kindle output. XTTS renders an optional **draft** (a pacing guide, never published), and the author records the final narration in Adobe Audition. Part C then checks coverage, the technical spec (ACX as the example), and pronunciation, with a re-record rule for changed passages. Part B (B4b) assembles `<BOOK>_AUDIOBOOK` from the final recordings only.
- **The final eBook PDF is the trigger** for each chapter's final-wording chain: Part 0 → 0.7 → Part A Kindle → Part C audiobook → PHASE 5. It's documented in the overview's trigger map, and PHASE 6 gains an optional notify-only **3F eBook watcher**.
- **PHASE 4 Part 0 step 0.7.** A PHASE 0.9 spot check of each chapter's synced text, so drift is caught before Kindle is built and the audiobook is recorded. `MANUSCRIPT_SYNCED.md` requires that no blocking finding is open.
- **Dual RAG in PHASE 5 (v4).** One canonical, model-agnostic chunk set (`RAG/Chunks/`) feeds two tracks:
  - **Track L — Local (required):** ChromaDB in Docker, with vectors from an ONNX/TEI embedding container.
  - **Track C — Cloud (optional):** vector files in Azure Blob Storage, embedded with an Azure OpenAI `text-embedding-3-large` deployment (3,072 dims, multilingual) and searched in memory by cosine similarity. No search service, so the cloud track costs only the per-token embedding calls plus Blob storage.
  - The tracks share chunk text, IDs, and metadata; they never share vectors.
- **Book-level `_BookAutomation/RAG/RAG_Config.json`.** It names each track's store (ChromaDB collection or Blob container), embedding model, dimensions, task prefixes, and endpoint *environment variable names* (never keys), and `cloud.enabled` switches the cloud track on or off.
- **Per-track index manifests** (`RAG/Index/<ChapterName>_RAG_Index_{Local,Cloud}.json`): model, dimensions, chunk IDs, chunk-set hash, and before/after counts.
- **Per-track triggers** `RAG_LOCAL_READY.md` and `RAG_CLOUD_READY.md`. `RAG_READY.md` now means every *enabled* track passed.
- **Parity check** in the validation report: the cloud chunk IDs are a subset of the local ones, at the same version and chunk-set hash.
- **Cloud data rule:** chunks marked `cloudEligible: false` stay local. By default that covers draft marketing seeds and internal governance notes.
- **Blob vector layout** (PHASE 5 §4B): `<BOOK>/chapters/<ChapterName>/<chunkSetHash>/vectors.jsonl.gz`, published by swapping a `current.json` pointer only after the upload is verified, so readers never see a half-written file. One previous version is kept for rollback. A book-level `manifest.json` records the model and dimensions.
- **Multilingual smoke test** for the cloud track: translated AudienceMap questions (languages in `cloud.multilingualSmokeTest`) must retrieve the mapped section. PHASE 6 cloud answers may be written in the reader's language, but quotations come from the English chunk text.
- **Access model:** Entra ID preferred. PHASE 5 writes with Storage Blob Data Contributor, and consumers read with Storage Blob Data Reader. Keys and SAS tokens are allowed only through environment variables or the n8n credential store.
- **PHASE 6 (v4):**
  - Every workflow declares its track, and it embeds queries with that track's model.
  - AutomationIndex entries record both tracks.
  - New §4B (connect the cloud LLM), with credentials kept only in n8n's store or environment variables.
  - Governance automation gains an index drift check.
  - New **Test 6** covers index routing and parity. Tests 1 and 3 now run per track.
- **`<RAG_BLOB_CONTAINER>`** placeholder token.

### Changed

- **The default local embedder is now `nomic-ai/nomic-embed-text-v1.5` (768 dims, 8k context), served by the ONNX/TEI container.** Common container defaults such as `all-MiniLM-L6-v2` truncate input at 256 tokens, which silently drops most of a 500–1000-word chunk. Ingest uses the `search_document: ` prefix and queries use `search_query: `.
- PHASE 5 checks each track's *served* input limit, not just the model's nominal context. A container can serve less than the model's full window: nomic's 8k window, for example, is typically capped at 2048 tokens on an ~8 GB Docker host so warmup doesn't run out of memory. The config gains `maxInputTokens` and `prefixesAppliedBy`, which prevents double-prefixing.
- PHASE 5 no longer lets an ingestion path re-split the canonical chunks. If a tool would re-chunk them, send pre-computed vectors to the store directly.
- PHASE 5 runs again after every PHASE 4 Part 0 manuscript re-sync; an index built from an older chunk set counts as stale.
- PHASE 6.5 (v3.1) and PHASE 7 (v3.1) certify and verify RAG per track: RAG (Local) · RAG (Cloud / N/A).
- `MASTER_PIPELINE_OVERVIEW.md`: phase table, deliverable map, trigger map, RAG map, and LLM map updated for both tracks.
- `PLACEHOLDERS.md`: new token and example values; scripts point at `v_1_0_2/`.
- **The audiobook moved from PHASE 3 to PHASE 4.** The author refines wording in the eBook and print InDesign books up to PHASE 4, so audio rendered in PHASE 3 would narrate pre-final text. PHASE 3.5 no longer checks audio, and PHASE 4 Part C and PHASE 6.5 do. PHASE 4 is retitled "Final-Wording Builds" (the file name is unchanged).
- PHASE 0.9 documents the manuscript passes: PASS 6 is tightening (audit when it's complete), and PASS 7 is the author's voice pass, after which the chapter is pseudo-locked.

### Unchanged

PHASES 1 and 2 differ from `v1_0/` only by the PHASE 0.9 hooks (the entry gate, the TerminologyLock seed, and glossary normalization) and a PHASE 1 Step 9 note about the audiobook. PHASES 3 and 3.5 differ only by the audiobook moving to PHASE 4.

---

## [v1.0] — 2026-09-22

**Folder:** `v1_0/` · **Previous:** `archived-versions/beta_0_9/` (unchanged, kept for reference)

The first release where the phases actually connect. Beta 0.9 was a set of strong individual prompts that disagreed with each other about paths, phase numbers, certification levels, and who produces what. v1.0 is a consistency and alignment pass: every phase now has one entry gate, one exit gate, one set of deliverables, and one place to write them.

Prompt text that was working was kept. The changes below are about making the pipeline hold together end to end.

### Added

- **`MASTER_PIPELINE_OVERVIEW.md`** — the single reference for the whole pipeline: phase table, milestone map, deliverable map, folder map, trigger/automation map, RAG map, LLM map, publishing map. Every phase file points to it, and it wins any disagreement.
- **Phase headers.** Every phase file opens with its position, entry gate, downstream phase, and a version-change list.
- **Exit gates.** Every phase ends with an explicit gate. No phase begins on a guess about whether the previous one finished.
- **Trigger files that someone actually creates.** Beta 0.9's automation phase listened for `DESIGN_READY.md` and `GOVERNANCE_READY.md`, but no phase wrote them. Now:
  - `Governance/Trigger/GOVERNANCE_READY.md` — written by PHASE 2
  - `DesignPacket/Trigger/DESIGN_READY.md` — written by PHASE 3.5
  - `RAG/Trigger/RAG_READY.md` — written by PHASE 5 (new; automation had no signal that RAG was rebuilt)
  - each with an `*_INCOMPLETE.md` counterpart, and a rule against leaving a stale READY file behind
- **PHASE 1:** a paths-and-conventions table, an eBook prep destination, RAG file names, and an exit gate.
- **PHASE 2:** Design Handoff staging into `DesignPacket/uploads/` (it was happening in practice but no phase said to do it); a governance trigger; a packaging check for chapters that aren't under `Final/`.
- **PHASE 3:** a whole operator section (Part A) in front of the Claude Design system prompt — inputs with paths, the DesignPacket layout, export names, production tracks for manual InDesign print work and XTTS audio, book assembly mode for the book-level deliverables, and an exit gate. The system prompt itself (Part B) is unchanged apart from one clarification.
- **PHASE 3:** figure image export (`DesignPacket/figures_export/`) as a required output, covering both generated figures and ones the author draws by hand.
- **PHASE 3.5:** a Kindle Readiness check (§13) that gates the Kindle build, a fix → re-QA loop, and a Kindle Readiness row in the score table.
- **PHASE 4 Part 0 — manuscript sync.** Wording often changes during InDesign layout, and nothing carried it back. PHASE 4 now starts by comparing the manuscript (MD and DOCX) with the final eBook PDF, applying the author's layout-stage wording changes, flagging anything that touches terminology, numbers, quotations, claims, or looks like a layout error, bumping the chapter version, and listing derived artifacts that still carry the old wording. It writes `Manuscript/Trigger/MANUSCRIPT_SYNCED.md`. If the eBook PDF is not in `eBook/`, the chapter stops at PHASE 4 and nothing downstream runs. The print InDesign book may live outside the book root; the author confirms print wording instead.
- **PHASE 4:** a Step 0 dependency check; Kindle-sized figure images in `Kindle/figures/`; a build profile with toggles; front matter, Part opener, and back matter handling; and **Part B**, the book-level Kindle assembly (`<BOOK>_Kindle.docx` for KDP, EPUB, AZW3 proof, metadata, cover, assembly report).
- **PHASE 5:** a deliverable table, a chunk ID format, a retrieval smoke test, a system-prompt load order sized for an 8k context window, and the RAG trigger.
- **PHASE 6:** homes for the required deliverables (`_BookAutomation/n8n/`, `_BookAutomation/OpenClaw/`), a trigger table mapping each trigger to the phase that creates it, and an activation test for the approval rule.
- **PHASE 6.5:** chapter mode and book mode, paths for every input, print and audiobook package checks, and per-format sub-certifications.
- **PHASE 7:** Part B "LLM Recommendations", which the assistant fills in before the author signs; verification of the marketing, eBook, trigger, and book-level deliverables; and defined Published, Archive, and Finalized Releases paths.
- **`PLACEHOLDERS.md`** — every token the phase files use (`<BOOK_ROOT>`, `<BOOK>`, `<AUTHOR>`, `<DSM_NAME>`, `<RAG_COLLECTION>` and the rest), with find-and-replace scripts and a list of the values that are examples rather than requirements.
- **`.gitattributes`** normalizing line endings to LF.

### Changed

- **One path root.** Beta 0.9 mixed three: a OneDrive path, a local book root, and a `RCF_KnowledgeBase` path for the automation index. Everything now resolves from one book root and one chapter root (`Chapters/<ChapterName>/Final/`).
- **Phase numbering fixed.** Two files were both numbered PHASE 4; the publication QA file called itself "PHASE 5.5"; the final checklist called itself "PHASE 6" and its internal sections numbered the phases differently again. The sequence now reads 1, 2, 3, 3.5, 4, 5, 6, 6.5, 7 everywhere.
- **One status ladder.** Four different certification lists became `Draft → Review Ready → Design Ready → Production Ready → Publishing Ready → Published`, with one phase owning each level: PHASE 2 up to Design Ready, PHASE 3.5 Production Ready, PHASE 6.5 Publishing Ready, PHASE 7 Published (author only).
- **Kindle moved to one place.** Beta 0.9 implied a Kindle edition during design *and* a Kindle DOCX compile later. All Kindle work now happens in PHASE 4 — per chapter (Part A), then assembled for the book (Part B) — after the design packet, figures, and the manual print/eBook work are finished and QA'd, because that is what Kindle content is built from.
- **Book-level outputs re-homed.** Alpha 0.5 had a "PHASE 5 — Claude Design Publications" step that produced the HTML masters and EPUB/Kindle packages; beta 0.9 dropped it, which left the publication QA phase reviewing files no phase produced. Those outputs now come from PHASE 3 book assembly (eBook, workbook, print, audiobook) and PHASE 4 Part B (Kindle), all landing in `_BookPublication/`.
- **Chunk rule aligned.** Creation and governance said 500–1000 words with 100-word overlap; the RAG phase said 550–1000 with 80–120. Now 500–1000 / 100 (80–120 tolerated) in all three.
- **The manuscript is never silently edited.** PHASE 1's accuracy step said "make suggested wording edits in the chapter" while PHASE 2 declared the manuscript locked. It now writes an Editorial Suggestions file; the author accepts the edits, and the manuscript version is incremented before governance runs.
- **Publication QA is report-only.** That file said both "you MAY modify files" and "you do not modify files". It reports; fixes are applied by the design and scripting steps after the author approves them.
- **Design QA output has one name.** `<ChapterName>_DesignQA.md` and `DesignQA_<DATE>.md` became `Governance/<ChapterName>_DesignQA_<YYYYMMDD_HHMM>.md`, timestamped so runs accumulate as history.
- **Kindle deliverables are separate files.** "Clean HTML blocks embedded in DOCX" became `_Kindle.docx`, `_Kindle.html`, and `_KindleMetadata.json`, which is what the phase's own checklist expected.
- **Export formats unblocked.** The design system prompt banned PDF and PowerPoint output while the deliverable list required both. It now states that those are exported *from* the HTML the prompt produces.
- **Automation index** moved to the book root, under `_BookAutomation/`.
- **OpenClaw pipelines** are required rather than "optional but recommended", since they are a listed deliverable.
- **Book-level governance report** moved out of `Chapters/_BookGovernance/` to a book-root `_BookGovernance/`, matching the existing `_BookMarketing/` pattern.
- **Naming convention enforced.** `<ChapterName>` is `Ch<N>_<PascalCaseTitle>`; governance now flags prefixes that drift from it. Design-tool project files keep the names their tool assigns, as a documented exception.

### Fixed

- **Draft marketing copy could reach readers.** The Kindle compile pulled in "Further Exploration" marketing seeds that are generated as drafts pending author approval. That section is now off by default and accepts only approved items. Instructor notes are off by default too, since the default build is a reader edition.
- **Nothing publishes itself.** The automation phase listed content scheduling and auto-fixing governance checks, which contradicted the creation phase's rule that the author approves every piece. Automations now produce drafts into a dedicated `Marketing/Generated/` folder, governance automations report rather than fix, and an activation test verifies it.
- **Figure placeholders could survive into a published file.** Placeholders are now a gate failure at PHASE 3.5 and PHASE 4, allowed only with a recorded author approval.
- **Manuscript-versus-structure conflicts** during the Kindle build now resolve to the manuscript, and the difference is logged.
- **Vector deletions scoped.** The ChromaDB rebuild deletes vectors for the chapter being rebuilt instead of implying a wider wipe, and the embedding model is fixed book-wide so chapters stay comparable.
- **Environment state is recorded, not assumed.** The local LLM setup step no longer marks model installs and servers as done; missing pieces become blockers.
- **Superseded files retired.** The duplicate PHASE 4 placeholder ("Local LLM AI and Human Publishing Checklist") was merged into PHASE 7, and the old publication QA file was replaced by the renamed 6.5. Neither is carried into `v1_0/`; both remain in `archived-versions/beta_0_9/`.

### Migration from beta 0.9

1. Copy `v1_0/` into your instructions folder and keep `archived-versions/beta_0_9/` for reference. Chapters mid-flight can finish on 0.9.
2. Fill in the placeholders (see `v1_0/PLACEHOLDERS.md`) and confirm your chapter-name convention against the folder map in `MASTER_PIPELINE_OVERVIEW.md` §4.
3. Create the folders phases now expect: `eBook/`, `Governance/`, `DesignPacket/` per chapter, and `_BookGovernance/`, `_BookPublication/`, `_BookAutomation/`, `_FinalizedReleases/`, `_Archive/` at the book root.
4. Re-run PHASE 2 on chapters processed under 0.9 to produce the governance files and triggers they never had.
5. Export figure images for any chapter already designed, so PHASE 4 has them.
6. Expect the first PHASE 3.5 run on an older chapter to fail Kindle Readiness. That is the point: it lists what is missing.

---

## [beta 0.9] — 2026-09

**Folder:** `archived-versions/beta_0_9/`

### Added
- Marketing & Local LLM Intake Packet in PHASE 1 (intake, seeds, trigger, claims registry, terminology lock, voice notes) with a retrofit run mode for chapters already built.
- Auto-remediation in PHASE 2: tiered fix policy with backups, remediation log, manuscript change proposals, re-validation passes, and a batch mode for multiple chapters.
- PHASE 4 Kindle DOCX chapter compilation.
- PHASE 5 RAG rebuild and local LLM setup, per chapter.
- PHASE 6 automation activation (n8n, local LLM, RAG, OpenClaw).
- PHASE 6.5 publication QA and PHASE 7 chapter publishing checklist.

### Changed
- Governance became detect-and-fix rather than report-only.
- Publishing checklists expanded across design QA, local AI, and release.

### Known issues (addressed in v1.0)
- Conflicting path roots, duplicate phase numbers, and four different certification vocabularies.
- Triggers consumed but never produced.
- The alpha publication phase was dropped without re-homing the book-level outputs it used to produce.

---

## [alpha 0.5] — 2026-08

**Folder:** `archived-versions/alpha_0_5/`

### Added
- The original six-phase shape: chapter artifact generation (PHASE 1), governance check (PHASE 2), design hand-off (PHASE 3), design QA (PHASE 3.5), a local-AI and human publishing checklist (PHASE 4), a Claude Design publication pipeline producing EPUB/Kindle/HTML masters (PHASE 5) with its QA (PHASE 5.5), and a chapter publishing checklist (PHASE 6).

---

[v1.0]: ./v1_0
[beta 0.9]: ./archived-versions/beta_0_9
[alpha 0.5]: ./archived-versions/alpha_0_5
