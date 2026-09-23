# Changelog

All notable changes to the Fluxline RCF Book Pipeline.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions are folders in this repository; each release keeps its predecessors intact so an in-flight book can finish on the version it started with.

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
