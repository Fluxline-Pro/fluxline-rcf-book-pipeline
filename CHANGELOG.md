# Changelog

All notable changes to the Fluxline RCF Book Pipeline.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions are folders in this repository; each release keeps its predecessors intact so an in-flight book can finish on the version it started with.

---

## [v1.3.0] — 2026-10-31

**Folder:** `v_1_3_0/` · **Previous:** `v_1_2_6/` (unchanged, kept for books mid-flight) · **Tag:** `v1_3_0.ALPHA` (then BETA, RC, PROD after the author's review)

Microsoft Copilot as a governed second opinion. Also publishes the working v1.2.7 changes (Pass 4, sidebars) that were never in a repository folder.

### Why

Research checks, final-artifact reads and figure generation all ran on one model family. A second, independent model catches different mistakes, and the author's Microsoft 365 Premium account can carry some of that work. The pipeline stays the authority: Copilot output is evidence and drafts, every Copilot step is started by the author, and nothing calls Copilot automatically.

### Added

- **`COPILOT_HANDOFFS/`**: the standard (`COPILOT_HANDOFF_STANDARD.md`: role, authority, prohibitions, source-of-truth order, upload manifest, task, output schema, gate effect, limitations, return path, privacy check, human approval; status labels; platform limits), a README, and seven prompts with upload lists and return formats: Phase 2.5 research review, Phase 3 image generation, Phase 3.5 design review, Phase 4 final eBook review, print PDF review, Kindle review, Phase 6.5 publication QA.
- **PHASE 2.5 §3.2b, research verification and reconciliation**: after Pass 4 (Claude), a Researcher review in Copilot; Claude validates the report (hash, file list), verifies every source Copilot names, writes `RESEARCH_RECONCILIATION.md` (claim, Pass 4 conclusion, Copilot conclusion, source disagreement, resolution, author decision) and adds SCIENCE rows to the decisions log. Blocking vs non-blocking findings are defined.
- **`copilotRequired: yes|no` and `pipelineRelease` in `MANUSCRIPT_LOCKED.md`**: one field that every Copilot gate reads. The first lock under v1.3.0 sets `yes`; a delta re-lock carries the old value forward (an ordinary revision of an older chapter does not make the steps mandatory); a research retrofit sets `yes`; locks from earlier releases count as `no`.
- **`RESEARCH_CLEAR.md`**, written just before `MANUSCRIPT_LOCKED.md` with the same hashes; the lock records it. The gate is inside PHASE 2.5 (not a new phase between 2 and 3) because 2.5 edits the DOCX and records the lock hashes, and PHASE 3 already requires the lock, so the runner needs no change. §7 defines what invalidates it (adding or strengthening a claim, a number, a causal or absolute statement, or changing a citation) and what doesn't (softening, spelling, narrative or framework wording). Chapters locked earlier can opt in through a `MANUSCRIPT_REVISED.md` "Copilot research retrofit".
- **`COPILOT_AGENT_INSTRUCTIONS.md` and `HOW_TO_USE_COPILOT.md`**: a standing role prompt for a dedicated Copilot agent (research, reviews, image generation, governance limits, labels; about 5,200 characters against Agent Builder's documented 8,000-character limit; Microsoft 365 Premium eligibility for Agent Builder and a Researcher toggle are not documented, so the file gives a paste-as-first-message fallback and says to run research in Researcher mode directly), and an author's guide to where Copilot is used in each PHASE.
- **Deep Researcher counts as Pass 4 evidence.** The local Deep Researcher workflow plus the author's claim-by-claim review of its results is the evidence and review record for Pass 4 (for example the first six chapters' 37 High claims); it does not replace the Copilot step, which is the independent second model. A retrofit of such a chapter reviews the whole chapter, including whether the approved replacement wording overstates anything. The research prompt carries an optional `BOOK_CONTEXT` line for the author (for example, a book that is the consumer form of a dissertation).
- **PHASE 4 Step 0V, author layout verification.** The order is now explicit: manuscript (DOCX and MD) → eBook and print book (chapter **and workbook**) verified by the author in InDesign → Kindle → audiobook (always last) → PHASE 5. The author creates `Manuscript/Trigger/LAYOUT_VERIFIED.md` after checking the layouts; Part A (Kindle) and everything after it wait for it, and for Part 0 synced, DOCX = MD, 0P closed, and the workbook ready (`WORKBOOK_READY.md`, workbook print QA closed). A later export makes it stale. Sections without a lock (the first book's Ch1 to Ch5) are not held. This also resolves an earlier inconsistency in which 0P was non-blocking while Step 0C required the print PDF. To make that order possible, the manuscript-to-narration-script comparison and the script's freshness check moved from congruency pass 1 to pass 2: the script is rebuilt from the Kindle output in Part C, so it cannot be current before Part A. `WORKBOOK_READY.md` must be current (hashes match) at Step 0V, and PHASE 3W's "does not block PHASES 4-6" now excepts it.
- **PHASE 3 A0**: Copilot Create as an optional figure generator (`Figures/Copilot/<FigureID>_CopilotHandoff.md`). The figure registry gains provenance fields (`generator`, `promptVersion`, `dsmVersion`, `aiGenerated`, `approval`, `colorMode`, `resolutionStatus`, `rights`, `revisionHistory`, …). Generated images are RGB concepts (Copilot offers three fixed sizes up to 1536 px) and never canonical.
- **PHASE 3.5 §15**: checks generated figures (complete provenance, `approval`, no invented text, not concept-only) and folds in an optional Copilot design review.
- **PHASE 4 Step 0F**: a Copilot review of the final eBook PDF before it becomes the manuscript's wording source (required for chapters locked under v1.3.0). Wording differences that change an empirical claim or citation go through `MANUSCRIPT_REVISED.md` and a PHASE 2.5 delta audit, not Part 0. Optional print-PDF review (0P) and Kindle review (Part B).
- **PHASE 6.5 §9b**: a Copilot cross-format review is one input to Publishing Ready, which also needs the deterministic checks, the human checks, resolved findings and the author's sign-off.
- **PHASE 7**: checklist items for the research clearance, Copilot reviews, and AI-generated figure disclosure.
- **HOW_TO_RUN "Copilot checkpoints"**: for each of the seven checkpoints: when, why, files to upload, prompt, output name, where to save it, pass/fail, what happens next, what needs the author, and what invalidates it.
- **MASTER_PIPELINE_OVERVIEW**: release notes, Copilot checkpoint table, status ladder, trigger map (`RESEARCH_CLEAR.md`, Copilot report files), folder map (`Governance/Research/`, `Governance/Copilot/`), and a tool-responsibility table (builds, reviews, validates, decides).

### Refinements before release (pre-release hardening of the Copilot handoffs)

- **Two-stage research review, with an explicit STOP.** `COPILOT_PHASE2_5_RESEARCH_REVIEW` (now v1.1) is split into **STAGE 1 UPLOADS** (DOCX, reference list, glossary) and **STAGE 2 UPLOADS** (`ScienceClaims`, Deep Researcher evidence, the audit report, the claims registry). Copilot lists the files, builds its own claim inventory, returns it, says "STAGE 1 COMPLETE. Waiting for the Stage 2 files." and stops until the author writes `STAGE 2 FILES ATTACHED`. A Stage 2 file already in the conversation is not opened. One conversation. The report records `stage1Completed`; Claude marks a report `not independent` if it says otherwise. PHASE 2.5, HOW_TO_RUN, HOW_TO_USE_COPILOT and the Ch1 to Ch6 packets follow.
- **One governed candidate per image generation.** The image prompt (now v1.1, so batch and single-candidate runs can be told apart in `promptVersion`) asks for Option 1 only; another composition is Option 2 as a separate request. Files are `<FigureID>_copilot_<date>_opt<n>.png`, each with its own text file and one `revisionHistory` entry (date, option, file, prompt version, DSM version, generator, outcome, reason).
- **The Copilot agent stays optional.** "The handoff contract is authoritative. Persistent agent instructions reduce repetition but are not required for correctness." is stated in the standard, the agent file, the handoffs README, HOW_TO_RUN and HOW_TO_USE_COPILOT; Researcher is always a separately started session.
- **Placeholders stay visible on GitHub.** The source files were intact: GitHub's Markdown view hides an unrecognised `<AUTHOR>` outside a code span as an HTML tag. The Copilot handoff files now wrap tokens in backticks (documented in PLACEHOLDERS). The README's handoff diagram is fenced as `text`.

### Changed (carried over from the working v1.2.7)

- **Pass 4, science and source verification** in PHASE 0.9 and PHASE 2.5 (category SCIENCE): claims are extracted and risk-rated, every source is opened and existence-checked, local models never rate a claim or source, and a High claim never closes on an AI verdict alone. Made generic (the book-specific counts are removed).
- **Sidebars are an optional per-book setting** (`sidebars: on`; default off) in PHASE 1, 2, 3.5, 4 and 7 and PLACEHOLDERS. The working files had hard-coded "no sidebars", which was one author's decision.
- **PHASE 2 FIGURE REGISTRY schema** now lists the fields later phases already read (`number`, `caption`, `spec`, `accents`, `status`, `imagePath`, `printImagePath`, `toolUsed`, `altText`).
- PLACEHOLDERS: the token-replacement scripts also cover `COPILOT_HANDOFFS/`.

### Compatibility

- A book mid-flight finishes on its starting version. Chapters whose lock has `copilotRequired: no` (or no such field) need neither `RESEARCH_CLEAR.md` nor any Copilot step; each can opt in.
- No runner change is needed: PHASE 3 and later keep requiring `MANUSCRIPT_LOCKED.md`. Step 0F stops PHASE 4 with `MANUSCRIPT_SYNC_INCOMPLETE.md` ("Waiting: Copilot final eBook review") until the review or a recorded waiver exists; a runner that reads that file as a blocker works as is. The runner, which lives outside this repository, must be pointed at the `v_1_3_0` phase files (its `instructions/` folder) before it applies Pass 4 or the Copilot steps; the author deploys that, with a backup, after reviewing.
- Every required Copilot step can be waived with a recorded reason, in one file (`Governance/Copilot/Copilot_Waivers.md`: `research`, `final-ebook`, `publication-qa`). Waivers are copied into the reports and the PHASE 7 checklist.
- Copilot report hashes: the research report carries the hash of the DOCX it reviewed (`reviewedSha256`, recorded when the handoff is written); a later hash difference does not invalidate it, only added or strengthened claims or changed citations do. Later reviews use the hash in `MANUSCRIPT_SYNCED.md` (or the lock before Part 0 has run).

### Known limitations

- **Copilot's behavior is the author's to confirm on first use.** Microsoft documents the Researcher agent for Microsoft 365 Premium and uploads of PDF, DOCX, XLSX, PPTX and MD (20 files, 50 MB each), but not EPUB or IDML, not whether Researcher reads uploaded files on a personal plan, not a PDF page limit, and not image resolution beyond three fixed sizes. The handoffs say so and give fallbacks (PDF/DOCX forms, splitting long PDFs, pasting the claim list). The consumer "Deep Research" mode was retired on 2026-08-18; the prompts use Researcher. A monthly query allowance may apply.
- **Copilot reads PDFs semantically.** It cannot check preflight, fonts, colour spaces, bleed, trim, metadata, tags or EPUB validity, and the prompts forbid it to claim so.
- Pre-existing PHASE 4 inconsistencies not changed in this release (the print-PDF one is resolved by Step 0V): the Part A exit gate requires the pass 2 congruency result, which only exists after Part C; PHASE 5 and 6.5 do not check the pass 2 result that PHASE 4 says gates them; HOW_TO_RUN lists the layout builds (2c) before the figures (2d).
- Two phase files (3.5B, 3W) changed line endings only (CRLF to LF) when copied from the working files, as in v1.2.6.
- The v1.2.7 label in the working files was never a repository release; v1.3.0 is the first published version with Pass 4.

---

## [v1.2.6] — 2026-10-26

**Folder:** `v_1_2_6/` · **Previous:** `v_1_2_5/` (unchanged, kept for books mid-flight) · **Tag:** `v1_2_6_PROD` (after the author's review)

One congruency check across every format.

### Why

Each pair of formats was already checked on its own: Part 0 (eBook against manuscript), 0P (print against eBook), Part C (audio against its script). Nothing combined them into one result, and three things were not checked at all: the narration script against the locked manuscript, the freshness of every file against `MANUSCRIPT_LOCKED.md`, and the book's exercise numbers and titles against the workbook.

### Added

- **PHASE 4 Step 0C, the congruency check** (`congruency_check.py <Section> [--pass 1|2]`, deterministic, no LLM, report-only), reusing the Part 0 text comparison, the 0P print QA result, and the audiobook QA text rules. The report (`_BookGovernance/CongruencyQA/<Section>_Congruency.md` + `.json`) has a status row for each format, every difference with its page or segment, a stale-file list, and a **PASS / HOLD** verdict.
- **Pass 1** (after Part 0 / 0R / 0G / 0P, before Part A) covers the manuscript DOCX and MD, the eBook PDF, the print PDF, the narration script, and the workbook's exercise numbers and titles. Part A starts only on PASS.
- **Pass 2** (after Part C) adds the Kindle DOCX and the audiobook QA. PHASE 5 and PHASE 6.5 start only on PASS.
- **Review loop:** differences are accepted with `--accept "<reason>"` (recorded in `<Section>_Accepted.json`), or fixed at the source.
- **Numeric comparison** in the DOCX/MD, manuscript/eBook, manuscript/script and Kindle checks: "three", "3" and "3rd" agree, "three" and "4" are reported as "number differs" with the words around them.
- **Triggers:** automatic (the local watcher, once every input exists and nothing has changed for 5 minutes; an email only on HOLD) or manual (`Manuscript/Trigger/RUN_CONGRUENCY.md`).
- Chapters without a lock (the first book's Ch1 to Ch5) are reported only and never held.
- Updated: PHASE 4, MASTER_PIPELINE_OVERVIEW, HOW_TO_RUN_THE_PIPELINE (new Step 5c), PLACEHOLDERS. All other phase files are unchanged from v1.2.5.

### Known limitations

- **Numbers outside the body text are not compared by value:** the reference list (left to `references_check.py`) and, in the narration script, numbers above 100 (years and page ranges are read aloud differently). Inside the body text, numbers are compared by value (see Added).
- **Pass 1 needs the print PDF,** so PHASE 4 now waits for it, where before print could arrive later.
- **Moved text is matched only when identical** (a footnote set at the page foot); a footnote reflowed with different wording shows as a missing and an extra passage.
- **`--accept` is by text, not by place.** The same wording difference elsewhere in the section is accepted with it.
- Two phase files (3.5B, 3W) changed line endings only (CRLF to LF) when copied.

---

## [v1.2.5] — 2026-10-24

**Folder:** `v_1_2_5/` · **Previous:** `v_1_2_4/` (unchanged, kept for books mid-flight) · **Tag:** `v1_2_5_PROD` (after the author's review)

The manuscript is now audited and locked **before** design.

### Why

Until now, the full content audit of each chapter (PHASE 0.9 Mode D) ran at the very end, in PHASE 4 Part B. By then the design packet, the eBook, the print IDMLs, and even an audiobook recording already existed. When the audit found something (a definition that disagreed with another chapter, a wrong cross-reference, a list count), the fix had to go back into the manuscript and then through every format again. Chapter 3's audio had already been recorded when its findings came in.

The audit belongs where a fix is still one edit in one file: after governance, before anything is designed, laid out, or recorded.

### Added

- **New PHASE 2.5, Manuscript Lock Audit** (`PHASE 2.5- Manuscript Lock Audit.md`), between PHASE 2 and PHASE 3. Per chapter, it:
  - runs PHASE 0.9's read-through passes (Pass 1 → Pass 2, Mode P) on the governed chapter against the book ledger, with the full content categories: definition conflicts, cross-references, term drift, list counts, glossary gaps, acronyms, heading anchors, and figures (plus equations, thresholds, and known corrections);
  - writes a findings report and a **decisions log** (`Manuscript/<ChapterName>_LockDecisions.md`), where the author decides every finding: `Fix`, `Fix: <wording>`, `Keep — <reason>`, `Canonical: …`, or `Defer — <chapter>` for a cross-chapter item whose other chapter isn't locked yet;
  - applies the approved fixes to the **DOCX first** (canonical), then brings the MD in line with `docx_md_sync.py`, re-checks the changed sections, and updates verbatim quotes of the old wording in the chapter's derived files;
  - writes **`Manuscript/Trigger/MANUSCRIPT_LOCKED.md`**, recording the DOCX and MD SHA-256 hashes, the run ID, and the decision counts, plus a locked snapshot in `Manuscript/_Locked/`.
- **A lock gate on every design and production phase:** PHASE 3 (A0 now starts from the lock), 3.5, 3.5A, 3.5B, 3W (W1 onward), and 4 (Part 0, Part A, and Part C). A lock is stale when a recorded hash no longer matches the file, or when `MANUSCRIPT_REVISED.md` has a newer section.
- **Status ladder:** a new **Locked** milestone, awarded by PHASE 2.5, between Design Ready and Production Ready.
- `docx_md_sync.py` is listed with the reference tools in `PLACEHOLDERS.md` (`<LOCAL_TOOLS_ROOT>`).

### Changed

- **After the lock, any change needs `MANUSCRIPT_REVISED.md` and the author's approval.** Each new section carries an `Approved: <initials> <date>` line. PHASE 1 then re-runs for the changed sections, PHASE 2 re-validates, and PHASE 2.5 runs a delta audit and writes a new lock (PHASE 1, PHASE 2.5 §7).
- **PHASE 4 Part 0** expects no differences from the locked manuscript. Any S1 or S2 difference is now a post-lock change and needs the author's decision in `_Pipeline/P4_DECISIONS.md`, like an S3 item. `MANUSCRIPT_SYNCED.md` records the new hashes.
- **PHASE 4 Part B, B0 (PHASE 0.9 Mode D) is reduced** to a cross-chapter consistency check plus a check of what changed in each chapter since its lock. It is no longer a full content audit, and it doesn't reopen a manuscript except for a genuine cross-chapter conflict, with the author's approval.
- **PHASE 4 Part C:** the audiobook is recorded only after the lock, so a re-recording should never be needed.
- `MASTER_PIPELINE_OVERVIEW.md` (phase table, flow, status ladder, deliverables, folder map, trigger table, automation events), `HOW_TO_RUN_THE_PIPELINE.md` (new Step 2a), PHASE 0.9 (Mode L and the reduced Mode D), PHASE 2, 6.5, and 7 updated to match.

### Documentation

- **README: choosing your path.** Running the pipeline AI-assisted, with AI only for checking, or with no AI (the phases as a checklist-and-gate system), with steps for each path, AI-disclosure guidance, and a short guide to adopting the pipeline for other publishing work.
- README updated for v1.2.5: current version, the phase table, and the flow.

---

## [v1.2.4] — 2026-10-22

**Folder:** `v_1_2_4/` · **Previous:** `v_1_2_3/` (unchanged, kept for books mid-flight) · **Tag:** `v1_2_4_PROD`

The author's review of the Chapter 4 and Exercise 1.4 builds, and the workbook eBook's structure.

### Added

- **Finish step: export the finished document as IDML into `_PrintDSM`** (the author, 2026-10-22; PHASE 3.5B §9), so the next build starts from it. Templates are refreshed there too.
- **Chapter builder:** callouts are separate frames copied from the template's master C (`idml_callouts.py`). The builder also:
  - adds keeps: headings stay with the next paragraph, and at least 2 lines stay at each end of a break;
  - sets 12 pt around figures, captions, and callouts, and 0 pt before pull quotes and centered italics;
  - reports figure/callout pairs.
- **In-text figure references** (PHASE 3.5B §2, §8). In "(see Figure N)", the "Figure N" takes the "Caption Figure Roboto Mono" character style in print, and `figure-text` in the eBook (now in the book eBook design system). The chapter builder applies it even when the eBook source has no span. Chapter 4's eBook references were wrapped.
- **Numbered question badges** (PHASE 3W W1c). Numbered questions (Reflection Questions) lead with a color circle: 1 green, 2 blue, 3 yellow, 4 orange, and so on.
  - Print: the exercise builder copies the template's numbered badge groups and indents the question and hint 25.6 pt beside each one.
  - eBook: `.wb-num` in the workbook eBook design system.
  - Exercise 1.4's eBook Reflection Questions were updated.
- **Workbook eBook page numbering and final PDFs** (PHASE 3W W1c).
  - Page numbers follow the assembled eBook, and each page file's own default page matches its place there.
  - Structure: front matter in roman (Contents now two pages; Values/Virtues/DRIVEs and the first journal set after the Prologue); Part I starts at 1; the nine remaining journal sets are in the back.
  - Finals are exported per section, tagged, with title, author, language, and bookmarks (`ebook_print.py --tagged`).
- **Chapters start on a right-hand page** (PHASE 3.5B §2, §8, §9). The chapter's page parity is checked in the finish.

### Changed

- **Workbook write-in questions are Montserrat bold** in the eBook, matching print's "Workbook Prompt" styles; hints stay Merriweather italic (PHASE 3W W1c; workbook eBook design system). Exercises 1.2–1.4 were re-exported.
- **Exercise openers show no page number** in the workbook eBook (Exercises 1.3 and 1.4 fixed; design system updated).

---

## [v1.2.3] — 2026-10-22

**Folder:** `v_1_2_3/` · **Previous:** `v_1_2_2/` (unchanged, kept for books mid-flight) · **Tag:** `v1_2_3_PROD`

Refinements from the author's review of the Chapter 3 and Exercise 1.3 print builds.

### Changed

- **Print callouts are separate objects** (the author, 2026-10-22; PHASE 3.5B §4). This covers the print book and the print workbook, not the eBook. Each callout is copied from the book template's Body Page Spread C master and edited in place, never built inline in the body story. The spacer after the eyebrow's line break is kept, and the text starts right after it. The book builder's callout code changes before the Chapter 4 print build.
- **How-to step emphasis:** parentheticals are italic, parentheses included, and a phrase the author marks may be bold italic (PHASE 3W W1c). Exercise 1.3's DOCX, MD, and eBook were updated.
- **Workbook how-to steps are roman** (the author, 2026-10-22; PHASE 3W W1c), matching Exercises 1.1 and 1.2. Italic is used only for quoted speech and deliberate emphasis. The print styles are named: "Workbook Subparagraph Under Heading" for the step text and "Numbering Roboto Mono Red" for the numbers. Exercise 1.3's DOCX, MD, and eBook were updated to match.

---

## [v1.2.2] — 2026-10-22

**Folder:** `v_1_2_2/` · **Previous:** `v_1_2_1/` (unchanged, kept for books mid-flight) · **Tag:** `v1_2_2_PROD`

### Added

- **Design systems are the source for every export** (the author, 2026-10-22). Three Design System artifacts:
  - the book eBook (`<EBOOK_DESIGN_SYSTEM>`);
  - the workbook eBook (`<WORKBOOK_EBOOK_DESIGN_SYSTEM>`);
  - the design packet (`<PACKET_DESIGN_SYSTEM>`, mirrored locally in `<PACKET_DSM_ROOT>`).

  New placeholders, with both replace scripts updated.
- **PHASE 3.5B §3a, design system alignment.** Each eBook page links its system's `dsm/<slug>/tokens.css` and `bundle.css` after its own styles and carries an `rcf:design-system` meta. The files come from `dsm_css.py` (new reference tool in `<LOCAL_TOOLS_ROOT>`), which turns the system's `tokens.json`, `bundle.css`, and fonts into a local stylesheet folder with a `DSM.json` record.
  - Re-export after any system change. Compare the renders before and after.
  - New components go into the system first, with the author's approval.
  - New §8 check, "Design system (eBook)".
  - First run: Chapter 3 and Exercise 1.3 re-exported pixel-identical.
- **PHASE 3W W1c** builds the exercise eBook pages from the workbook eBook system.
- **"How to work this exercise" = numbered steps** (the author, 2026-10-22; PHASE 3W W1c). Every workbook how-to box lists its instructions as steps 01, 02, 03 … in red, in two columns, as in Exercise 1.2, in the eBook and in print. A one-paragraph DOCX how-to is split at sentence ends only, with the wording verbatim. The workbook eBook design system's HowToBox component was updated (version 3). Exercise 1.3's three boxes (1.3a, 1.3b, 1.3c) were converted, with the 1.3b opener spacing tightened, and re-exported.
- **Codex "Exercise(s) completed" includes an unlettered main exercise** (PHASE 3W W1c). Exercise 1.3's Codex gained its missing 1.3 checkbox, in the eBook and in the workbook DOCX/MD. **PHASE 3 A2b**: the packet DSM is the Design System artifact.

---

## [v1.2.1] — 2026-10-22

**Folder:** `v_1_2_1/` · **Previous:** `v_1_2/` (unchanged, kept for books mid-flight) · **Tag:** `v1_2_1_PROD`

The author's feedback after the first eBook-first print build (Chapter 3 and Exercise 1.3, "about 95% of the way there"):
- print rules for the last 5%;
- PHASE 3 now starts on its own when PHASE 2 passes;
- figure prompts, with a checklist of what to make in Photoshop, are generated for every chapter.

### Added

- **PHASE 3 A0, automatic start** (release v1.2.1). `GOVERNANCE_READY.md` starts PHASE 3 for the chapter (protected chapters run it in chat):
  - **Step 1, figure prompts and checklist:** `Figures/<ChapterName>_FigurePrompts.md`, with `Figures/RGB/`, `CMYK/`, and `Drafts/` created. Each figure gets the manuscript lines and caption, a Google Gemini prompt (house style, manuscript-exact labels, at least 2400 px, no title in the image), a no-text fallback, a check against the manuscript, and save-as names.
    - **Figure checklist:** what the author must make in Photoshop. Each figure gets an RGB master (PNG or JPG) in `Figures/RGB/` and a CMYK TIFF (300 ppi at the placed width, LZW, flattened) in `Figures/CMYK/`, with the Photoshop steps.
    - **Figure suggestions** for figures the chapter could use. They are added only with the author's approval.
    - After the files are made: a check against the manuscript, then a FigureRegistry update (paths, tool used, alt text).
  - **Step 2, design packet:** built as artifacts from the packet DSM once `<PACKET_DSM_ROOT>/DSM_APPROVED.md` exists. They are published as private artifacts only with the runner config's `designPacket.publishArtifacts` standing permission; otherwise the packet is built locally and the author is emailed.
- **HOW_TO_RUN Step 2d**, two cheat-sheet rows (`<ChapterName>_FigurePrompts.md`, `DSM_APPROVED.md`), and the master overview's release note and trigger map.
- **Print pagination and spacing rules** (the author, 2026-10-22, after reviewing the Chapter 3 print build; PHASE 3.5B §2, §8, §9). Print only:
  - no widows or orphans, with white space accepted;
  - facing pages aligned top and bottom where possible, uneven pages accepted otherwise;
  - callouts and paragraphs never split into widowed or orphaned lines;
  - callouts and figures kept apart, preferably on different pages;
  - 1 pica before and after callouts, figures, and captions;
  - no space after the paragraph before a red callout or an italic paragraph.

  The builder applies what the styles carry (keeps, spacing) and reports figure/callout pairs. The author settles facing-page alignment in the finish.
- **Design packet as Claude artifacts** (the author, 2026-10-22; PHASE 3 A2b). Claude Design is no longer required. A design packet DSM (`<PACKET_DSM_ROOT>`, new placeholder) is extracted once from a finished chapter's DesignPacket (tokens, components, content patterns) and approved by the author. Every later chapter's packet is built from it, as individual private artifacts; the slide deck uses the Slides artifact type for PPTX and PDF export. The eBook, print, and workbook layout rows in A2 now point to `_eBookDSM` and PHASE 3.5B.
- **Styling rule: quoted speech is emphasized** (the author, 2026-10-22; PHASE 3.5B §2). Real or hypothetical quoted speech and self-talk ("I am experiencing chest tightening." "How might I do this action?") is always set in italics, in the eBook and print layouts of the book and the workbook. It is styling only; the DOCX wording is unchanged. Pull quotes, epigraphs, titles, scare quotes, and citations are excluded.

---

## [v1.2] — 2026-10-22

**Folder:** `v_1_2/` · **Previous:** `v_1_1_3/` (unchanged, kept for books mid-flight) · **Tag:** `v1_2_PROD`

eBook-first print build (IDML). v1.1.3 gave the print track a styled text import, but figures, callouts, and the layout itself were still placed by hand. In v1.2 the print documents are generated as InDesign IDML files that replicate the finished eBook:
- the chapter (7×10);
- the workbook exercise (7×10).

Each is built on the author's own finished print documents, so a new chapter opens looking like the ones already laid out. The order is fixed: the eBook first, then print. It is a minor release because it adds new functionality: the pipeline now writes IDML.

First run: Chapter 3 and Exercise 1.3 of *RCF*, built on Chapter 2 and Exercise 1.2, with structural proofs rendered through Adobe's InDesign service.

### Added

- **PHASE 3.5B, eBook-first print build**, new file `PHASE 3.5B- eBook-First Print Build (IDML).md`:
  - **Entry gate:**
    - the final DOCX;
    - finished figures (RGB in `Figures/RGB/`, CMYK TIFF in `Figures/CMYK/`);
    - the print template and the author's last finished chapter or exercise IDML;
    - the eBook page reviewed.
  - **eBook first (§3):** the chapter's `<EBOOK_DSM_ROOT>/Chapter<N>_eBook.dc.html` is built from the DOCX (and the Claude Design draft) and paginated to 8.5×11. A real-render pass checks it, and footnotes stay with their block. Then the contents page and the page numbers that follow are updated, a review PDF is printed, and the page is published as a private artifact with the author's permission. The workbook gets the same treatment, in its own `_eBookDSM/`.
  - **Chapter IDML (§4):** one main story through full-page 1-column frames, built on the author's last finished chapter IDML (its masters, styles, swatches, and opener). Paragraph styles follow the finished chapter. Callouts use the print template's Callout styles, with an anchored badge. Figures are anchored and link the CMYK TIFFs, with captions. Footnote and reference styles, running heads through text variables, and Smart Text Reflow (adds pages, deletes empty ones) complete it.
  - **Exercise IDML (§5):** cloned piece by piece from the previous exercise's IDML: the opener, ruled lines, tables, grids, badges, callouts, example panels, cards, Codex, and closing. The text is re-worded from the exercise DOCX, word for word, with text heights measured in the real fonts. The opener frames keep their ids, so the master's text stays overridden.
  - **Optional structural proof (§6)** through Adobe's InDesign rendering, with the author's permission (it uploads to their Creative Cloud). Fonts are substituted on the render server, so the proof checks structure and content, not line breaks.
  - **Placement (§7):**
    - `<CH_ROOT>/InDesign/<NNN>_Chapter<N>_<Title>.idml`;
    - `<CH_ROOT>/Workbook/<NN>-<n>_Exercise_<L>_<N>_<Name>.idml`;
    - proofs in `_Proofs/`.
  - **Checks (§8):** one column; complete text (pull quotes word for word); CMYK figures at ≥ 300 effective ppi or flagged; print callout styles; footnotes and references complete; opener correct; valid IDML.
  - **Manual finish (§9):** fonts, links, a final check, then the print PDF export as before.
- **Design rules (the author, 2026-10-22), PHASE 3.5B §2:**
  - **Sources:** print uses `_PrintDSM` only; `_eBookDSM` is read for content only.
  - **Image formats:** TIFF (CMYK) for print and PNG/JPG (RGB) for the eBook, never swapped.
  - **Columns:** one-column masters only, and never 2-column spreads.
  - **Look:** print matches the eBook's overall design without its heavy color, in black, white, and gold. Callouts keep their content and spacing.
  - **Motifs:** no eBook motifs, diamonds, or extra colors, except the quote callouts and the print template's own multi-color callouts (never the eBook versions).
  - **Margins and spacing:** margins are used end to end, and spacing is consistent.
  - **Figure size:** figures are resized to the column, and one too large or too small is flagged.
  - **Workbook only:** tables, ruled lines, and circular badges are copied from the templates or the previous exercise.
- **Reference implementations** in `<LOCAL_TOOLS_ROOT>`:
  - `ebook_paginate.py`;
  - `ebook_print.py` (waits for fonts, images, and a stable page count; checks the embedded fonts);
  - `idml_chapter_build.py`;
  - `idml_workbook_build.py`. Its page plan is per exercise; the component layer is shared.
- **PHASE 3.5 §13B, Print IDML (3.5B):** the QA reads the build report and the §8 checks.
  - Missing text, an RGB figure, or a 2-column page is Critical for the print track.
  - None of these blocks `DESIGN_READY.md`.
- **PHASE 3W W1c, exercise print IDML:** the workbook half of 3.5B: eBook pages first, then the cloned print IDML into `Workbook/`.
- **Placeholder `<EBOOK_DSM_ROOT>`** (= `<BOOK_ROOT>/_eBookDSM`), with both replace scripts updated. `<LOCAL_TOOLS_ROOT>` lists the four new tools. `<PRINT_DSM_ROOT>` also holds the author's finished chapter IDMLs.
- **`HOW_TO_RUN_THE_PIPELINE.md`:**
  - new Step 2c (eBook first, then the print IDMLs);
  - `3.5B` in the RERUN list;
  - a cheat-sheet row for `RERUN_P3.5B.md`.

### Changed

- **PHASE 3 A3 print layout:** the default is now the PHASE 3.5B generated IDML, then the author's finish. The 3.5A import remains the alternative. The workbook row names the 3.5B exercise IDML.
- **PHASE 3.5A:** a note that 3.5B is the default print build. 3.5A stays available for a chapter without an eBook yet, or for a plain styled import.
- **Master overview:**
  - the release note;
  - phase table row **3.5B**;
  - the flow;
  - the deliverable map;
  - the folder map: `_eBookDSM/`, the IDMLs in `InDesign/` and `Workbook/`, and `_Proofs/`;
  - the trigger map;
  - the local tools rows.
- **Master overview §4:** phases read `<PRINT_DSM_ROOT>` through 3.5A and 3.5B, and still never write to it.
- **README:**
  - current version v1.2, folder `v_1_2/`, with `v_1_1_3/` listed as previous;
  - a 3.5A / 3.5B row in the phase table;
  - a note on what the print build needs in `_PrintDSM`.

---

## [v1.1.3] — 2026-10-21

**Folder:** `v_1_1_3/` · **Previous:** `v_1_1_2/` (unchanged, kept for books mid-flight)

Print build. Print layout was the one format that started from nothing: the author placed the manuscript into an empty InDesign document and applied every style by hand, even though the print template already defines them all. PHASE 3.5A now generates a styled import from the manuscript DOCX, and the author's work starts at layout. The release also names the pre-PHASE 1 polish window and adds a trigger for revising the DOCX after PHASE 1.

### Added

- **PHASE 3.5A, print build (automated tagged text)**, new file `PHASE 3.5A- Print Build (Automated Tagged Text).md`:
  - **Entry gate:** the DOCX is in `Chapters/<ChapterName>/Final/Manuscript/` and is newer than `AUDIT_CLEAR.md`, and `<PRINT_TEMPLATE_BOOK>` exists. `DESIGN_READY.md` is not required.
  - **Inputs:** the manuscript DOCX (canonical), with the MD as a guard only (the MD is regenerated from the DOCX, never the reverse), plus the FigureRegistry, `<PRINT_DSM_ROOT>/style_map.json`, and the IDML template.
  - **Outputs** in `Chapters/<ChapterName>/Final/InDesign/`:
    - `<ChapterName>_Import.txt`: InDesign tagged text, UTF-16, with `<ParaStyle:…>`, `<CharStyle:…>`, and figure placeholder lines;
    - `_BuildManifest.json`: SHA-256 of the template, style map, and DOCX; styles used; unmapped items; figures with resolved paths; running heads;
    - `_BuildReport.md`.
  - **Checks:** every style exists in the template's `Styles.xml` (colon form); no DOCX paragraph or run is unmapped; every figure resolves to a TIFF in `DesignPacket/figures_export/` or to the FigureRegistry path; running heads are set; the template hash is recorded. A failure blocks the closure of 3.5A only.
  - **Manual finish:** place with Load Styles into a copy of the template, lay out, then export `InDesign/<ChapterName>_Print7x10.pdf` (checked by PHASE 4 Part 0P, as before).
  - **Rules:** never edit the DOCX or MD; never write to `<PRINT_DSM_ROOT>`; never call InDesign; never guess an unmapped style.
- **`idml_build.py`** in `<LOCAL_TOOLS_ROOT>` (reference implementation; `python-docx`, `zipfile`, `xml.etree` only):
  - Exit codes: 0 pass, 1 check fail, 2 bad input.
  - `--md` stops the build if the MD is newer than the DOCX.
  - It refuses an output folder inside the template's or the style map's folder.
  - Tests in `<LOCAL_TOOLS_ROOT>/tests/test_idml_build.py` (`unittest`; a synthetic IDML and DOCX built in a temp folder; no book files).
- **`v_1_1_3/templates/style_map.example.json`:**
  - paragraph and character maps, plus the direct-formatting keys (`direct:italic`, `direct:bold`, …) and a `figures` block (`path_pattern`, `tif_dir`, `placeholder_style`);
  - values derived from the print DSM, and every one checked to exist in the current book template;
  - every value marked `CONFIRM:` or `TODO:`, which the tool treats as unmapped until the author confirms it.
- **Polish window (PHASE 1):** between `AUDIT_CLEAR.md` and the PASS 7 drop, the author polishes in the DOCX and regenerates the MD.
- **Revision trigger, `Manuscript/Trigger/MANUSCRIPT_REVISED.md` (PHASE 1):** it lists the changed sections and the reason. It is valid after PHASE 1 and before the eBook lock. PHASE 1 re-runs from Step 1 onward for the changed sections only, and records the revision in the Production Checklist. PHASE 2 then re-validates, and 3.5A is re-run if print layout hasn't started.
- **PHASE 3.5 §13A, Print build (3.5A):** requires zero unmapped items, zero missing figures, and a template and DOCX matching the ones the import was built from. A failure that blocks layout is Critical for the print track.
- **PHASE 3W W1b, workbook print build:** one build per exercise, from `_BookGovernance/Workbook/Workbook_ExerciseRegistry.json` and `<PRINT_TEMPLATE_WORKBOOK>`. Outputs go to `<CH_ROOT>/Workbook/InDesign/`. It is a second step, gated by a new workbook-profile key, `"printBuild"` (default `false`).
- **PHASE 4 Part 0 (0.1):** a new stop. If `MANUSCRIPT_REVISED.md` is newer than the eBook PDF, Part 0 writes `MANUSCRIPT_SYNC_INCOMPLETE.md` and asks for a re-export instead of syncing.
- **Placeholders:** `<PRINT_DSM_ROOT>` (= `<BOOK_ROOT>/_PrintDSM`), `<PRINT_TEMPLATE_BOOK>`, `<PRINT_TEMPLATE_WORKBOOK>`; `idml_build.py` in the `<LOCAL_TOOLS_ROOT>` list. Both replace scripts are updated, with `<PRINT_DSM_ROOT>` replaced before the template tokens.
- **`HOW_TO_RUN_THE_PIPELINE.md`:**
  - the polish window in Step 1, and revising the manuscript after Step 2;
  - new Step 2b (read the build report, place, lay out, export);
  - `3.5A` in the RERUN list;
  - cheat-sheet rows for `MANUSCRIPT_REVISED.md`, `RERUN_P3.5A.md`, `style_map.json`, and `_Import.txt`.

### Changed

- **PHASE 3 A3:** the print layout track was "manual in InDesign". It is now **"PHASE 3.5A generated import, then manual finish"**, and its output is the print PDF at `InDesign/<ChapterName>_Print7x10.pdf`. `Ch<N>_Print7x10.dc.html` stays the design reference. The workbook row points to the optional W1b build.
- **Master overview:**
  - the release note;
  - phase table row **3.5A**;
  - the flow (polish window, 3.5A, the revision loop);
  - the deliverable map;
  - the folder map: `_PrintDSM/` (read-only), the `InDesign/` build outputs, and `Manuscript/Trigger/MANUSCRIPT_REVISED.md`;
  - the trigger map: `MANUSCRIPT_REVISED.md`, the 3.5A outputs, and `AUDIT_CLEAR.md` → 3.5A entry;
  - the local tools rows.
- **Master overview §4:** "No phase reads those folders" is replaced by "Phases read `<PRINT_DSM_ROOT>` only through PHASE 3.5A, and never write to it." The print InDesign book itself (INDB, links) may still live outside `<BOOK_ROOT>`.
- **README:** current version v1.1.3, folder `v_1_1_3/`; `v_1_1_2/` is listed as the previous release.
- **Author decisions folded in (2026-10-21, same release):**
  - **Figure formats.** RGB masters go in `Figures/RGB/` (PNG for illustrations, JPG for photos) for the eBook and Kindle. CMYK TIFFs go in `Figures/CMYK/` for print. The print build now requires a TIFF: an RGB-only figure fails with "RGB only; CMYK TIFF missing".
    - The FigureRegistry may carry `printImagePath`.
    - The style map's figure pattern takes `{short}` (= `Ch<N>`), and its example defaults to `{short}_Fig{n}_*.tif` in `Figures/CMYK`.
  - **Figures are finished before the eBook and print builds.** This is now part of the PHASE 3.5A gate.
  - **The manuscript is final before PHASE 1.** The layouts are built from the DOCX, not edited for wording. PHASE 4 Part 0 stays as the safety check and now expects no differences.
  - **Callouts are not in the manuscript.** PHASE 1 Step 8 writes `InDesign/<ChapterName>_CalloutRecommendations.md` (type, verbatim or derived text, source, placement, reason), and PHASE 2 validates it under new "Callout Candidates". The author places the approved callouts in the layouts. The callout `TODO` entries are dropped from the example style map.

### Fixed

- `PLACEHOLDERS.md` in the copied folder named `v_1_1_2/` in its intro and in both replace scripts. It now names `v_1_1_3/`.
- **Print export wording: bleed yes, printer's marks no.** Five places asked for a print PDF "with printer's marks and bleed", and the workbook print spec asked for "crop marks": HOW_TO_RUN Step 5b, PHASE 3.5A §6, PHASE 3W W1, PHASE 4 Part 0P, PHASE 7 Part A, and the master trigger map. KDP and IngramSpark want interiors with 0.125 in bleed on the top, bottom, and outside edge, none at the spine, and no printer's or crop marks. The author's exports already do this. All six files now say so, and Part 0P lists exported marks as a warning.
  - **`print_check.py`** (`<LOCAL_TOOLS_ROOT>`) now checks bleed on the top, bottom, and outside edge only. It had flagged every page of a correct export (91 false warnings on Ch1–Ch2). It also warns if printer's marks were exported, i.e. the page is larger than the bleed.

### Defaults chosen for this release

1. **Tagged text is the only output.** Generating an IDML document directly is deferred.
2. **`style_map.json` lives in `<PRINT_DSM_ROOT>`**, next to the template it maps to, not in `DesignPacket/_ds/`.
3. **The workbook build ships off by default** (`"printBuild": false`). The book build is tested first.

---

## [v1.1.2] — 2026-10-03

**Folder:** `v_1_1_2/` · **Previous:** `v_1_1/` (unchanged, kept for books mid-flight) · **Tag:** `v1_1_2_PROD`

Print vs. eBook QA. The print layout was the one deliverable no phase checked: PHASE 4 asked the author to confirm that the print InDesign book carried the same wording as the eBook, and PHASE 6.5 checked only that print PDFs existed. Wording can drift between the two layouts, and print has faults the eBook can't show (widows, trim, bleed, image resolution). The author now uploads the print PDF, and a deterministic check compares it with the eBook.

### Added

- **PHASE 4 Part 0P, print vs. eBook QA (report-only):**
  - **Input:** the author exports each finished section from the print InDesign book as a high-fidelity print PDF (7×10, printer's marks and bleed). It goes to `<CH_ROOT>/InDesign/<ChapterName>_Print7x10.pdf`; front matter goes to `FrontMatter/Final/<Section>/InDesign/<Section>_Print7x10.pdf`.
  - **Text drift:** a word-by-word comparison with the final eBook PDF. Line breaks, hyphenation, spacing, running heads, and folios are ignored, and print-only differences the author logs in `<Section>_PrintOnlyDifferences.md` are skipped.
  - **Layout:** widows, orphans, runts, stranded headings, 3+ stacked hyphens, doubled words, text in the 0.25 in safe zone or across the trim, trim and bleed size, unembedded or Type3 fonts, images under 300 ppi effective, RGB images, and blank pages.
  - **Report:** `_BookGovernance/PrintQA/<Section>_PrintQA.md` + `.json`, at book level, so protected chapters are covered too. Severities are text *check* (3+ words) or *minor*, and layout *error*, *warn*, or *info*.
  - **Runs automatically:** when the print or eBook PDF changes, after 5 quiet minutes. An email goes out when the findings change. Reference implementation: `print_check.py` in `<LOCAL_TOOLS_ROOT>`.
  - **Gate:** non-blocking for Part A, but closed before PHASE 6.5 and PHASE 7. Closed means 0 text differences to check, 0 layout errors, and every warning fixed or accepted by the author.
  - Nothing edits a layout or a manuscript. Wording that should reach the manuscript goes through Part 0 (fix the eBook, re-export).
- **PHASE 3W W2b, print workbook QA:** the same check for the print workbook, only when the workbook profile's `formats` includes `print` (otherwise N/A). It covers both workbook locations:
  - `location: book-root`: print PDFs go to `<WORKBOOK_BOOK_ROOT>/InDesign/`. `<eBook stem>_Print7x10.pdf` is checked against that section's eBook PDF; any other `*Print*.pdf` there is checked against the assembled workbook eBook PDF. Reports: `Workbook_<eBook stem>_PrintQA.md` or `Workbook_PrintQA.md`.
  - `location: chapter`: `<CH_ROOT>/Workbook/<ChapterName>_Workbook_Print*.pdf` is checked against `<CH_ROOT>/Workbook/<ChapterName>_Workbook_eBook.pdf`. Report: `<ChapterName>_Workbook_PrintQA.md`.
  - The 8.5×11 eBook vs. 7×10 print page size is expected, not drift.
- **PHASE 7 (v3.4):** Part A items for the print PDF upload, a closed 0P report, and reviewed warnings (plus the print workbook in the 3W section), a Part C **Print Approved**, and a completion-rule line.
- **`HOW_TO_RUN_THE_PIPELINE.md`:** Step 5b (export and upload the print PDF, read the report, fix and re-export), a running-checks row, and cheat-sheet rows.
- **Master overview:** the release note, phase table, deliverable map, folder map (`_BookGovernance/PrintQA/`), trigger map, and §9 event "print PDF uploaded / eBook re-exported → `print_check.py` → report → email".

### Changed

- **PHASE 7:** a PHASE 3W **workbook final check**: <AUTHOR> reviews the workbook eBook (8.5×11) and the full-color print (7×10) side by side (same exercises and order, usable write-in space, color and contrast, links), then signs off each format separately in Part C ("Workbook eBook Approved", "Workbook Print Approved"). "Audio Approved" notes that only the main book has an audiobook.
- **PHASE 4 (v3.4):**
  - **0.6 print cross-check:** now evidenced by the 0P report. the author still confirms print-only differences, and logs them in `<ChapterName>_PrintOnlyDifferences.md`.
  - **Print files in `InDesign/`:** PHASE 4 no longer says it never needs print files there. The print InDesign book still lives outside `<BOOK_ROOT>`, but its exported PDF is uploaded to `<CH_ROOT>/InDesign/`. It is never a sync source.
  - The checklist records the 0P counts.
- **PHASE 3W (v3.4):** in the `book-root` layout, print PDFs move from `<section>/<…>_Print.pdf` to `<WORKBOOK_BOOK_ROOT>/InDesign/<eBook stem>_Print7x10.pdf`. W3 steps 3 and 5 and the W5 preflight cite the print QA report.
- **PHASE 6.5 (v3.4):** print is validated from the print QA reports instead of being re-checked. An open text check or layout error is a Major issue, and blocks the Print sub-certification.
- **`PLACEHOLDERS.md`:** `print_check.py` is listed under `<LOCAL_TOOLS_ROOT>`, and the print trim row names the `_Print7x10.pdf` suffix.

### Fixed (review)

- **Workbook profile awareness:** the master overview's 3W entry gate, deliverable map, folder note, and trigger map, and PHASE 3's production-track row, now name only the profile's `formats` in its `location` (`chapter`: `Workbook/<ChapterName>_Workbook_eBook.pdf` + `_Workbook_Print.pdf`; `book-root`: `<section>/<NN>_Ex_<L>_<N>_Chapter<C>.pdf` + `InDesign/<eBook stem>_Print7x10.pdf`).
- **W2b covers both workbook locations:** `location: chapter` is checked (`<CH_ROOT>/Workbook/<ChapterName>_Workbook_Print*.pdf` vs `_Workbook_eBook.pdf`, report `<ChapterName>_Workbook_PrintQA.md`). The "not covered" note and the manual fallback are gone from PHASE 3W; PHASE 4, 6.5, 7, the master overview, and HOW_TO name both report forms. PHASE 6.5's book-root print name is `<WORKBOOK_BOOK_ROOT>/InDesign/<eBook stem>_Print7x10.pdf`.
- **Whole-workbook print QA input:** the assembled workbook eBook export at `<WORKBOOK_BOOK_ROOT>` if present, else W4's `<BOOK>_Workbook_eBook.pdf` (PHASE 3W W2b, W4, W5; PHASE 4).
- **`WORKBOOK_READY.md` evidence:** hashes every uploaded workbook PDF for the chapter's exercises in the profile's formats, not "the two PDFs"; W4 matches them in the profile's location.
- **PHASE 4 entry gate:** the final eBook PDF upload; `MANUSCRIPT_SYNCED.md` is Part 0's exit and the Step 0 / Part A entry (master overview).
- **PHASE 4 Part 0P:** names the front-matter eBook input, `FrontMatter/Final/<Section>/eBook/*.pdf`.
- **PHASE 1 exit gate:** `WORKBOOK_SELECTION.md` is required only when the workbook profile is enabled; otherwise N/A.
- **RAG `inputHash` is per track:** shared content inputs plus that track's own provider, model, and dimensions, so changing one track re-embeds that track only (PHASE 5 manifests and §5A; PHASE 6 §3G).

---

## [v1.1.1] — 2026-10-02

**Folder:** `v_1_1/` (unchanged) · **Tag:** `v1_1_1_PROD`

Documentation only. No phase file changed.

### Added

- **README: "Before the phases: the editing passes (PASS 0–7)".** What each editing pass settles, from the original draft (PASS 0) through PASS 6, the draft PHASE 0.9 audits. Also covers PASS 7, the semi-locked manuscript the phases take over, and the three ways it can still change.
- **README: current version** is labelled v1.1.1 (phase files in the unchanged `v_1_1/`). The pass count is stated as the original draft plus seven editing passes, and the PASS 7 note links to `v_1_1/PLACEHOLDERS.md`.

---

## [v1.1] — 2026-10-02

**Folder:** `v_1_1/` · **Previous:** `v_1_0_4/` (unchanged, kept for books mid-flight) · **Tag:** `v1_1_PROD`

Automation first. The author's two uploads (the final eBook PDF and the final workbook PDF) are now the switches that complete PHASE 3.5 and lock the text, and every step after them starts from an event, without anyone pasting a prompt. Three things were added along the way, each found while running the pipeline:
- Claude Design built every generated workbook sub-exercise into a chapter's workbook, including some that belonged to later chapters.
- Glossary definitions drifted between a chapter that primes a term and the chapter that defines it.
- References were never verified at all.

### Added

- **`HOW_TO_RUN_THE_PIPELINE.md`:** a step-by-step operating guide. For each step it says what runs automatically, what the author does by hand (and where), and what "done" looks like.
- **References check:**
  - **PHASE 1 Step 10b:** in-text citations ↔ reference list, numbering order, DOIs verified on Crossref (title, year, first author), DOIs found for entries without one, link checks, and APA 7 basics.
  - **Safe fixes go into the manuscript MD and DOCX before design:** DOI formatting, plus a DOI added when Crossref matches the entry unambiguously.
  - **Everything else goes to the author** as Editorial Suggestions.
  - **PHASE 4 Part 0R** re-checks report-only after the lock.
  - Report: `_BookGovernance/References/`.
- **Glossary lock and drift:**
  - **PHASE 4 Part 0G** finalises the chapter glossary from the locked manuscript and rebuilds `_BookGovernance/Glossary/Master_Glossary`, which holds **locked chapters only**. It also writes `Glossary_DriftReport.md`, an early warning across all chapters.
  - **New `Glossary_Canonical.json`,** where the author records which chapter *defines* a term (`definedIn`), which only *prime* it (`primedIn`), and which should not carry it at all (`removeFrom`).
- **The workbook exercise draft comes in with the manuscript:** `<ChapterName>_Exercise<L.N>_Workbook.docx`, reviewed against the same PHASE 0.9 notes, is dropped into `<PASS7_SOURCE>` with the manuscript. PHASE 1 adopts it as the workbook manuscript, without rewriting it.
- **Workbook candidate selection:** PHASE 1 writes extra exercises as candidates and lists them in `_Pipeline/WORKBOOK_SELECTION.md`. PHASE 2 adds only the ones the author ticks, renumbered without gaps, and stages a filtered packet for Claude Design.
- **PHASE 3W W2 upload location:** the workbook PDF may go to `<WORKBOOK_BOOK_ROOT>/<section>/<NN>_Ex_<L>_<N>_Chapter<C>.pdf` instead of each chapter's `Workbook/` folder. The print workbook is optional per book.
- **PHASE 3W uncertain sync items** go to `_Pipeline/P3W_DECISIONS.md` (a Decision column), mirroring PHASE 4's S3 handling.
- **Workbook profile:** a book-level `workbook` object in the exercise registry: `enabled`, `formats` (`["ebook"]` or `["ebook","print"]`), and `location` (`chapter` or `book-root`). Every phase reads it, so none assumes a format.
  - With no workbook, PHASE 2 writes `WORKBOOK_NOT_APPLICABLE.md`, which PHASE 6.5 and PHASE 7 accept.
  - In the book-root layout, print PDFs carry a `_Print` suffix, and W3 waits until every exercise has every required format, so a partial upload never yields a READY file.
- **PHASE 4 `_Pipeline/P4_DECISIONS.md`** is now specified: the table schema, how a re-run reads and applies it, and that it's archived once every row is decided.
- **PHASE 7 completion rule:** also requires no open critical or major reference finding, and every Part A item ticked or explicitly accepted by the author.
- **Master overview §9:** the automation map (event → automation → output → email), and what stays manual by design.
- **Placeholders:** `<WORKBOOK_BOOK_ROOT>` and `<LOCAL_TOOLS_ROOT>`.

### Changed

- **PHASE 3.5 (v3.3):** the author's upload of the final eBook PDF (book) or the final workbook PDF (workbook) completes the phase. If PHASE 3.5 didn't write `DESIGN_READY.md`, PHASE 4 writes it as attested by the upload.
- **PHASE 4 (v3.3):** the entry gate is the upload. The eBook PDF may be named `_eBook.pdf` or `_eBookPDF.pdf`. The checklist records 3.5 completion, 0R, and 0G.
- **PHASE 7 (v3.3):** runs locally and automatically after PHASE 6.5, with no Claude.
  - A deterministic check ticks every Part A item it can prove, with the evidence.
  - The local LLM drafts Part B from the unmet checks only.
  - The author gets an email with what's missing, or "ready for sign-off".
  - New Part A and C items: references, glossary, 3.5 completion by upload, and workbook selection.
- **PHASE 1 / PHASE 2 (v3.3):** workbook selection, references, and the glossary defining-chapter rule. Open critical or major reference findings block Design Ready.
- **`MASTER_PIPELINE_OVERVIEW.md`:** the release note, phase table, deliverable map, trigger map, and LLM map.

---

## [v1.0.4] — 2026-09-30

**Folder:** `v_1_0_4/` · **Previous:** `v_1_0_3/` (unchanged, kept for books mid-flight)

The cloud RAG track can now run behind a governance gateway, and a nightly refresh keeps the local and cloud stores in sync without anyone starting PHASE 5 by hand. Found while connecting a reader-facing companion to the cloud store: it needs every cloud AI call governed, smaller vectors, and a signal when a chapter changes.

### Added

- **Governance gateway mode for Track C (PHASE 5 v4.2).** `cloud.embeddingProvider: "governance-gateway"` sends every embedding call through a gateway flow (`cloud.gateway` in `RAG_Config.json`: `baseUrl`, `embedFlow`, `maxInputsPerCall`, `credentialEnv`). The gateway checks the request, then calls the embedding deployment, so PHASE 5 holds a gateway credential instead of model credentials. Direct Azure OpenAI (`azure-openai`) remains for setups without a gateway.
- **PHASE 6 §3G nightly RAG refresh** (book-level, time-triggered at `<RAG_REFRESH_TIME>`): detects chapters whose PHASE 5 inputs changed, re-runs PHASE 5 for them (Track L and Track C, validation and parity), then notifies each consumer in `cloud.consumers` and records its response. Nothing changed means nothing runs.
- **`cloud.consumers`** in `RAG_Config.json`: downstream products that build their own index from the cloud store, each with a `notifyUrl`, a `credentialEnv`, and any extra uploads it needs (for example figure images).
- **Cloud vector metadata:** `part` and `lesson` on every line; `figureId` and `altText` on FigureRegistry chunks.
- **Placeholders:** `<GATEWAY_URL>`, `<CLOUD_EMBED_FLOW>`, `<RAG_REFRESH_TIME>`.
- **PHASE 5 §5A: promote or roll back both tracks together.** Track C is staged (its `current.json` flips only after validation and parity pass), and Track L is snapshotted before the chapter's vectors are replaced. A failed run restores the snapshot and discards the staged cloud folder, so the stores can't drift apart.
- **`inputHash` in the index manifests:** a hash of every file PHASE 5 read for the chapter plus the track settings. The §3G refresh compares it to decide whether a chapter changed; the chunk-set hash alone can't see a changed input before PHASE 5 runs.
- **`cloud.gateway.chatFlow`:** the gateway flow PHASE 6 cloud chat uses. Empty means no cloud chat in gateway mode, never a direct fallback.

### Fixed

- **PHASE 4:** the Part 0 exit gate and the Step 0 heading now say plainly that Part 0 starts from the final eBook PDF and writes `MANUSCRIPT_SYNCED.md`, and that Step 0 runs right after it. (The sequence was right; the old heading, "do this before anything else", read as if Step 0 came first.)

### Changed

- **PHASE 5 (v4.2):** default `cloud.dimensions` is 1,024 (was 3,072). Existing cloud stores keep their dimensions until re-embedded, per the model-change rule. The environment check and data-handling rule cover gateway mode.
- **PHASE 6 (v4.1):** in gateway mode, cloud query embeddings and cloud chat go through the gateway (§4B). Test 5 allows the §3G refresh as the one workflow that writes to the vector stores; Test 6 checks gateway routing.
- **`MASTER_PIPELINE_OVERVIEW.md`:** release note, PHASE 6 row, cloud vector store row, and LLM map.
- **`PLACEHOLDERS.md`:** new tokens; the scripts point at `v_1_0_4/`; cloud-model defaults.

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
