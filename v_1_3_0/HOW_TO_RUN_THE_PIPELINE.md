# How to Run the Pipeline (v1.3.0)

**For:** <AUTHOR> · **Book:** *<BOOK_TITLE>* — <EDITION> · **Pipeline:** release v1.3.0 (each phase file's own version is in the table in `MASTER_PIPELINE_OVERVIEW.md`, section 1)

**New in v1.2.5: the manuscript is locked before design.** After governance (PHASE 2), PHASE 2.5 reads the chapter for content problems and gives you a decisions log. You decide every finding, the fixes go into the DOCX (then the MD), and the chapter is locked. Design, print, the workbook, Kindle, and the audiobook all start from the locked text (Step 2a).

**New in v1.2.6: one congruency check across formats.** Before the Kindle build, `congruency_check.py` compares the manuscript, the eBook PDF, the print PDF and the workbook's exercise numbers and titles, and checks that every file is current against the lock. You get one report and a PASS or HOLD (Step 5c). A second pass after the audiobook adds the narration script, the Kindle file and the audio check.

**New in v1.3.0: Microsoft Copilot as a governed second opinion.** At seven points the pipeline hands you a list of files and a prompt (in `COPILOT_HANDOFFS/`); you open Microsoft Copilot yourself, upload the named files, paste the prompt, and save the answer where it says. Claude then checks the answer and the gate moves on only with your decision. Copilot checks research (before the lock), generates concept images, and gives independent reads of the design, the final eBook PDF, the print PDF, the Kindle files, and the whole publication. **Nothing in this pipeline calls or has access to your Copilot.** See "Copilot checkpoints" at the end of this guide. The same release also adds Pass 4 (science and source verification) and makes sidebars an optional per-book setting.

This is the operating guide: what to do, in what order, one step at a time. The PHASE files hold the full rules; `MASTER_PIPELINE_OVERVIEW.md` holds every path, gate, and trigger, and wins if anything here disagrees.

**How each step is written:**
- 🤖 **Automatic:** what starts it, what it does, and whether you get an email.
- 🧑 **You:** what you do by hand, and where (Claude chat, Claude Design, InDesign, Audition, a file you create).
- ✅ **Done when:** the file or email that tells you the step is finished.

**The golden rules:**
1. **The lock comes first, then your uploads are the switches.** PHASE 2.5 locks a chapter's manuscript before design (`MANUSCRIPT_LOCKED.md`, v1.2.5). After that, the final **eBook PDF** starts PHASE 4 (it does not create the lock), and the final **workbook PDF** starts the workbook sync. Upload only final exports.
2. **Email is your inbox for the pipeline.** You're only emailed when you're needed, or when something is ready for you. No email means it's still running, or nothing needs you.
3. **Nothing publishes itself.** Every generated item is a draft, and only you approve, sign off, and mark a chapter Published. A Copilot report is evidence, never a verdict or a gate on its own.
4. **To redo a step,** create `<CH_ROOT>/_Pipeline/RERUN_P<n>.md`, where `<n>` is 1, 2, 2.5, 3W, 3.5, 3.5A, 3.5B, 4, 5, 6, 6.5, or 7. Anything you write inside is passed to Claude.
5. **Where to look:** `<CH_ROOT>/_Pipeline/STATUS.md` shows a chapter's phase history.

---

## 0. Before you start (once, and after a restart)

🧑 **Check the services are running.** Each of these starts at login:

| Service | How it starts | Quick check |
|---|---|---|
| n8n | its scheduled task (or `n8n start`; the wrapper applies the right settings) | http://localhost:5678 opens |
| Chapter-pipeline runner | its scheduled task | the runner log updates each minute |
| Local orchestrator (local tools, chat) | its scheduled task | `GET /v1/localai/status` |
| Ollama (local LLM) | at login | `http://127.0.0.1:11434` answers |
| Docker Desktop (vector store, embeddings) | at login | containers are up |

🧑 **In n8n, these workflows are active:** Chapter Pipeline, Local AI Notifications, Error Alerts, Ask the Book, and Ask My Research.

✅ The status endpoint shows every service up.

---

## 1. Book level, before chapter work — PHASE 0.9 (book-wide audit)

🧑 **You, in Claude (chat):**
1. Run PHASE 0.9 **Mode F** on the full draft in `<DRAFT_SOURCE>`, before PASS 7.
2. Decide the canonical terms it asks about. They go to `_BookGovernance/Audit/Audit_CanonicalTerms.json`.
3. Write PASS 7, your voice pass, from the audited draft.

✅ `_BookGovernance/Audit/Trigger/AUDIT_CLEAR.md` exists.

---

## 2. Per chapter

Work one chapter at a time, or several in parallel; the pipeline keeps each chapter separate.

### Step 1 — Drop the manuscript → PHASE 1 (content production)

🧑 **You:**
1. Work through the chapter's **PHASE 0.9 author-review notes** in the manuscript, and save the result as PASS 7. **Polish window (v1.1.3):** polish as much as you like now, in the **DOCX**, then regenerate the MD from it. Don't edit the MD on its own.
2. Review the chapter's **workbook exercise** against the same notes.
3. When **both** are final, drop them into `<PASS7_SOURCE>` together:
   - `Ch<N>_<PascalCaseTitle>.md` + `.docx`: the manuscript, both formats with the same name. **This is the final wording** (v1.1.3): every later format is built from it.
   - The chapter's **finished figures** in `Figures/`: the RGB masters in `Figures/RGB/` (PNG for illustrations, JPG for photos) and the CMYK print TIFFs in `Figures/CMYK/`. They must be in place before the eBook and print builds.
   - `Ch<N>_<PascalCaseTitle>_Exercise<L.N>_Workbook.docx` (+ `.md` if you have one): the exercise, e.g. `Ch6_ValuesVirtues_Exercise2.2_Workbook.docx`. Name any companion pages `..._Exercise<L.N>_<Part>_Workbook.docx`.

   If a workbook draft lands first, it waits for its manuscript. The run starts about 2 minutes after the last file lands.

🤖 **Automatic:** PHASE 1 starts about 2 minutes later. Claude:
- copies the manuscript into the chapter folder
- builds every Step 1–11 artifact (review packet, workbook, training, reference guides, slides, eBook prep, InDesign prep, audiobook prep, RAG packet, marketing packet)
- checks the **references** (Step 10b), applying safe fixes such as verified DOIs to the MD and DOCX
- writes the **Editorial Suggestions**
- lists any extra workbook exercises as **candidates** in `_Pipeline/WORKBOOK_SELECTION.md`

📧 **Email:** "PHASE 1 done. Your editorial review is next."

✅ The email arrives.

### Step 2 — Review, select, approve → PHASE 2 (governance)

🧑 **You:**
1. Open `Manuscript/<ChapterName>_EditorialSuggestions.md`. Accept or reject each row; reference findings are rows too ("References #N").
2. Apply the edits you accept to the manuscript, **both MD and DOCX**, and bump its version.
3. Open `_Pipeline/WORKBOOK_SELECTION.md` and tick `[x]` only the extra exercises you want in the published workbook. Skip anything flagged as a later chapter's material.
4. Create `_Pipeline/APPROVE_EDITORIAL.md`. Any notes you put inside go to Claude.

🤖 **Automatic:** PHASE 2 governance:
- validates and fixes derived artifacts
- builds the chapter's glossary, following your defining-chapter rules
- adds the exercises you selected to the workbook manuscript
- runs the workbook manuscript gate (DOCX = MD)
- stages the design packet

📧 **Email:** only if PHASE 2 needs you, with the blockers. When it passes, PHASE 2.5 starts on its own (Step 2a).

✅ `Governance/Trigger/GOVERNANCE_READY.md`.

If PHASE 2 needs you, resolve the listed items (Needs Author Review, Tier C proposals), then create `_Pipeline/RERUN_P2.md`.

### Step 2a — Decide the findings, lock the manuscript → PHASE 2.5 (v1.2.5)

🤖 **Automatic:** when PHASE 2 writes `GOVERNANCE_READY.md`, PHASE 2.5 reads the whole chapter for content problems, against the rest of the book: definition conflicts, cross-references, term drift, list counts, glossary gaps, acronyms, heading anchors, and figures. It changes nothing. It writes:
- the findings report, `Governance/<ChapterName>_LockAudit_<YYYYMMDD_HHMM>.md`;
- the **decisions log**, `Manuscript/<ChapterName>_LockDecisions.md`: one row per finding, with a blank **Decision** column.

📧 **Email:** "PHASE 2.5: N findings to decide", with the decisions log path. (No findings: the chapter is locked straight away.)

🧑 **You, in parallel (Copilot checkpoint 1, when `copilotRequired: yes`):** run the Researcher review in Microsoft Copilot and save its report as `DeepResearch/COPILOT_RESEARCH_REPORT.md` (details in "Copilot checkpoints" below). On the next run Claude reconciles it with its own findings (`RESEARCH_RECONCILIATION.md`) and may add research rows to the decisions log for you to decide. `RESEARCH_CLEAR.md` is written just before the lock.

🧑 **You:**
1. Open the decisions log and fill in **every** Decision:
   - `Fix`: apply the suggestion;
   - `Fix: <your wording>`: apply your wording instead;
   - `Keep — <reason>`: the text is right as it is;
   - `Canonical: <form or definition>`: a book-wide choice, recorded in `Audit_CanonicalTerms.json`;
   - `Defer — <chapter>`: only when the other side of a cross-chapter finding is in a chapter that isn't locked yet.

   A group row at the end saves time, for example `All minor: Fix`.
2. Create `_Pipeline/RERUN_P2.5.md`.

🤖 **Automatic:** PHASE 2.5 applies your decisions to the **DOCX** first, then brings the MD in line with `docx_md_sync.py`, re-checks the changed sections, and updates any verbatim quotes of the old wording in the chapter's derived files. Then it writes `Manuscript/Trigger/MANUSCRIPT_LOCKED.md` with the DOCX and MD hashes.

📧 **Email:** "manuscript locked; PHASE 3 starts", or "PHASE 2.5 needs you" (a blank decision, a new finding a fix caused, or a derived file that needs PHASE 2 again: create `RERUN_P2.md`, and PHASE 2.5 confirms the lock after it).

✅ `Manuscript/Trigger/MANUSCRIPT_LOCKED.md`. Nothing is designed, laid out, or recorded before this file exists.

**Revising the manuscript after the lock (v1.2.5).** The lock is what keeps the eBook, print, workbook, Kindle, and audiobook from drifting, so a change after it needs your written approval:
1. Edit the DOCX in `Manuscript/`, bring the MD in line with `docx_md_sync.py`, and bump the version.
2. Add a dated section to `Manuscript/Trigger/MANUSCRIPT_REVISED.md`: the changed sections, the reason, and **`Approved: <initials> <date>`**. A section without that line is ignored.

PHASE 1 regenerates what those sections feed, PHASE 2 re-validates, and PHASE 2.5 runs a delta audit of the changed sections and writes a new lock. Saving the REVISED file starts nothing: create `RERUN_P1.md`, then `RERUN_P2.md`, then `RERUN_P2.5.md`, in that order. Anything already built from the old text (the eBook, the print IDMLs, the workbook) needs the change carried in by hand; PHASE 4 stops until the eBook PDF is re-exported.

### Step 2b — Print build → PHASE 3.5A (automatic import, then your layout)

🤖 **Automatic, on request** (`_Pipeline/RERUN_P3.5A.md`, or run `idml_build.py` by hand): once the manuscript DOCX is in `Manuscript/` and locked (`MANUSCRIPT_LOCKED.md`, v1.2.5), the print build turns it into `InDesign/<ChapterName>_Import.txt`. Every paragraph and character style is set to the print template's style, through `<PRINT_DSM_ROOT>/style_map.json`. It also writes `_BuildManifest.json` and `_BuildReport.md` beside it. It never changes the manuscript or the template.

🧑 **You:**
1. Read `InDesign/<ChapterName>_BuildReport.md`. If anything is **unmapped**, add or confirm the entry in `<PRINT_DSM_ROOT>/style_map.json` (remove the `CONFIRM:` prefix once checked), then re-run. A missing figure needs its CMYK TIFF in `Figures/CMYK/` (the RGB PNG/JPG in `Figures/RGB/` is for the eBook only).
2. In InDesign, open a **copy** of the print template, and File → Place the import with **Show Import Options** → Use Tagged Text, **Load Styles**.
3. Replace each `[[FIGURE N …]]` placeholder with its image, set the running heads, and lay out the chapter.
4. Export the print PDF to `InDesign/<ChapterName>_Print7x10.pdf` (Step 5b).

✅ The build report says **PASS** and the chapter is laid out from it.

### Step 2c — Training materials, figures and the design packet → PHASE 3 A0 (automatic after the lock, v1.2.5)

🤖 **Automatic:** when PHASE 2.5 issues `MANUSCRIPT_LOCKED.md` (before v1.2.5: when PHASE 2 issued `GOVERNANCE_READY.md`), PHASE 3 starts.
- It writes `Figures/<ChapterName>_FigurePrompts.md`, containing:
  - a **figure checklist**: what to make, in RGB and CMYK;
  - a **Gemini prompt** for each figure, with a no-text fallback;
  - **figure suggestions** for you to accept or decline.
- It builds the **design packet** (deck, guides, **training materials**, reference guides, workbook) as artifacts from the packet DSM.
- You get an email when both are ready.

🧑 **You:**
1. Make each figure with Gemini, Firefly, or Microsoft Copilot Create (Copilot checkpoint 2: the handoff for each figure is in `Figures/Copilot/`), then finish it in Photoshop (Copilot images are small RGB concepts, not print files):
   - the RGB master to `Figures/RGB/`;
   - the CMYK TIFF to `Figures/CMYK/`, following the file's Photoshop steps.
2. Accept or decline the figure suggestions. An accepted suggestion goes into the registry and the manuscript before the build.
3. Review the packet artifacts.

✅ Every checklist row says **final**, and the FigureRegistry records the tool used. The eBook pass and the print build (Step 2d) can then run.

### Step 2d — eBook pass, your notes, then the print IDMLs → PHASE 3.5B (v1.2, the default print build)

References and manuscript are already finished and locked (PHASE 2.5). Everything here is for the book **and** the workbook exercise. **Print is required:** you review it, edit it, and pass it off.

1. 🤖 **eBook pass (on request):** create `_Pipeline/RERUN_P3.5B.md` with `ebook` on the first line (or ask Claude). The chapter's eBook page, `<EBOOK_DSM_ROOT>/Chapter<N>_eBook.dc.html`, is built from the DOCX (and the Claude Design draft, if there is one), paginated to 8.5×11, and printed to a review PDF. With your permission it is published as a private artifact. The same happens for the exercise's workbook eBook page.
2. 🧑 **You review the eBook and write your notes.** Layout notes go back into the eBook page. A wording change is a **`MANUSCRIPT_REVISED.md` change** (DOCX first, then a new lock), made **before** the print build, so the print replicates locked text.
3. 🤖 **Print IDML (on request):** when your notes are applied (or you say there are none), create `_Pipeline/RERUN_P3.5B.md` with `idml` on the first line. The print IDMLs then replicate the eBook:
   - the chapter, built on your last finished chapter IDML in `<PRINT_DSM_ROOT>`, goes to `InDesign/<NNN>_Chapter<N>_<Title>.idml`;
   - the exercise, cloned from your previous exercise IDML, goes to `Workbook/<NN>-<n>_Exercise_<L>_<N>_<Name>.idml`.
   Optionally, with your permission, a structural proof is rendered through Adobe and saved in `_Proofs/`.
4. 🧑 **You, in InDesign:** open each IDML, re-apply fonts where needed (the proofs use substitutes), check the callout badges, figures, and page breaks, edit, and pass it off. You are the final print authority; 3.5B is the default route and 3.5A the fallback, and neither decides.
5. 🧑 Export the print PDFs (Step 5b).

The design rules are in PHASE 3.5B §2: one column only; black, white, and gold; the template's print callouts; CMYK TIFFs for print only.

✅ Both IDMLs are in place with the build report's flags addressed, and the print PDFs are exported.

### Step 3 — Design updates, then QA → PHASE 3 + 3.5 (manual)

This follows the order in Steps 2c and 2d: the packet and figures, your updates, the eBook pass and your notes, then the print pass-off.

🧑 **You, in Claude Design and InDesign:**
1. In **Claude Design**, use the PHASE 3 Part B prompt and the files in `DesignPacket/uploads/` to build or update the packet: deck, guides, **training materials**, reference guides, workbook, opener, figures, and the eBook / print 7×10 / workbook layouts.
2. Export the figure images to `DesignPacket/figures_export/`, plus the slides (PPTX + PDF) and the eBook exports.
3. Finish the eBook pass and the print book as in Step 2d (your notes, then the print IDML created from the eBook; you review, edit and pass off the print book and the workbook's). **The wording is locked** (v1.2.5): it was settled in the DOCX before PHASE 1 and audited in PHASE 2.5. A change you still need goes into the DOCX, with an approved `MANUSCRIPT_REVISED.md` section and a re-lock, not into a layout. Place the callouts you approved from the PHASE 1 recommendations. Lay out the **workbook** in InDesign.
4. Run the **PHASE 3.5 QA** (report-only) once the print pass-off is done, and fix the findings until it says Production Ready.

✅ Design is finished, and you're ready to export the final PDFs.

### Step 4 — Upload the final eBook PDF → PHASE 4 (sync, references, glossary lock, Kindle)

🧑 **You:** export the chapter's **final** eBook PDF and save it as `eBook/<ChapterName>_eBook.pdf`. This completes PHASE 3.5.

🤖 **Automatic**, after 30 minutes with no further changes in `eBook/`:
1. **3.5 closed:** writes `DESIGN_READY.md` as attested by your upload, if PHASE 3.5 hadn't already.
2. **Part 0, manuscript sync:** **first, Step 0F (when `copilotRequired: yes`)** pauses and gives you the handoff for Copilot checkpoint 4 (see below); the sync starts when you have saved the review or a `final-ebook` waiver and its findings are resolved. Then it checks the manuscript is still locked, then compares it with your eBook PDF. It expects no differences; any it finds is listed in `_Pipeline/P4_DECISIONS.md` for your decision, since it would change the locked text (v1.2.5). Writes `MANUSCRIPT_SYNCED.md`.
3. **0R, references re-check:** report-only, since the manuscript is now locked.
4. **0G, glossary lock:** refreshes the chapter glossary from the locked text and rebuilds the **official master glossary** and the drift report.
5. **Part A, Kindle:** DOCX, HTML, metadata, and figures. **From v1.3.0 it waits for Step 5v** (your InDesign verification of the eBook and print books, chapter and workbook); nothing is built for Kindle until you confirm the layouts are final.

📧 **Email:** only if it needs you, for example wording changes it couldn't decide. Fill in the **Decision** column in `_Pipeline/P4_DECISIONS.md` (*Accept PDF*, *Keep manuscript*, or *Defer* with initials), then create `_Pipeline/RERUN_P4.md`.

✅ The PHASE 4 checklist shows `gateStatus: PASS`, and PHASE 5 starts on its own.

**Reference or glossary findings** don't block Kindle; they reach you by email. References are finished and locked before any PHASE 3 build (PHASE 2.5), so a reference fix after the lock is a **`MANUSCRIPT_REVISED.md` change** (DOCX first, delta audit, new lock), not an edit made only in InDesign.

### Step 5 — Upload the final workbook PDF → PHASE 3W (workbook sync)

🧑 **You:** export the exercise's **final** workbook PDF to the workbook folder, in reading order and named so the chapter number appears. For example: `<WORKBOOK_BOOK_ROOT>/03_Part_I_The_Self/01_Ex_1_1_Chapter1.pdf`. This completes PHASE 3.5 for the workbook.

🤖 **Automatic**, after 30 quiet minutes:
- syncs your layout wording back into the workbook manuscript (DOCX, then MD)
- confirms **PDF = DOCX = MD**
- updates the exercise registry
- writes `Workbook/Trigger/WORKBOOK_READY.md`

📧 **Email:** "workbook synced and locked", or "needs you". If it needs you, fill in the **Decision** column in `_Pipeline/P3W_DECISIONS.md`, then create `_Pipeline/RERUN_P3W.md`.

✅ `WORKBOOK_READY.md`.

Steps 4 and 5 are independent, so do them in either order.

### Step 5b — Upload the print PDF → print QA (PHASE 4 Part 0P; report-only)

🧑 **You:** when the chapter's print layout is finished (after Step 4's eBook upload):
1. Export it from the print InDesign book as a high-fidelity print PDF: 7×10 in, with bleed on the top, bottom, and outside edge (0.125 in), no printer's marks (KDP and IngramSpark reject crop marks).
2. Save it as `InDesign/<ChapterName>_Print7x10.pdf`. Front matter: `FrontMatter/Final/<Section>/InDesign/<Section>_Print7x10.pdf`. Print workbook (only if the workbook ships print): `<WORKBOOK_BOOK_ROOT>/InDesign/<eBook stem>_Print7x10.pdf`, or `Workbook/<ChapterName>_Workbook_Print*.pdf` if the workbook profile's `location` is `chapter`.
   Keep one print PDF per section: rename an older export `*_superseded_<timestamp>.pdf`.

🤖 **Automatic**, after 5 quiet minutes, and again whenever the print or eBook PDF changes:
- compares the print wording with the final eBook PDF, word by word (line breaks, hyphenation, running heads, and folios ignored);
- flags print-layout problems: widows, orphans, runts, stranded headings, stacked hyphens, doubled words, the safe zone and trim, trim and bleed size, fonts, image resolution, RGB images, and blank pages.

It changes nothing; it writes `_BookGovernance/PrintQA/<ChapterName>_PrintQA.md`.

📧 **Email:** the print QA summary, whenever the findings change.

🧑 **Then:**
1. Read the report.
2. **Text differences:**
   - Print wrong → fix the print InDesign book.
   - Print right → fix the eBook InDesign book, and re-export the eBook PDF (Part 0 re-syncs the manuscript).
   - Print-only (e.g. a page reference) → log it as a quoted phrase in `<CH_ROOT>/<ChapterName>_PrintOnlyDifferences.md`.
3. **Layout errors:** fix them in the print InDesign book. **Warnings:** fix each one, or accept it.
4. Re-export the PDF. The report refreshes on its own.

✅ The report shows 0 text differences to check and 0 layout errors, and you've fixed or accepted every warning. For a chapter with a lock it must be closed before Kindle (Step 5v); PHASE 6.5 and PHASE 7 need it closed for every section.

### Step 5v — Verify the layouts in InDesign, then confirm → PHASE 4 Step 0V (v1.3.0)

**The order is: manuscript (DOCX and MD) → eBook and print book (chapter and workbook) → Kindle → audiobook (always last) → PHASE 5.** Kindle and the audiobook are made from the same words, so they wait until the layouts are final.

🧑 **You** (as the graphic designer):
1. Check the chapter's eBook and print books, and the workbook's eBook and print, in InDesign for final anomalies. Fix them there (wording that should reach the manuscript goes through the DOCX and `MANUSCRIPT_REVISED.md`, or Part 0's decision list).
2. Re-export the PDFs: the eBook PDF to `eBook/`, the print PDF to `InDesign/<ChapterName>_Print7x10.pdf`, the workbook PDFs as Step 5 says. Part 0 (Step 4) and 0P (Step 5b) re-run by themselves; for `copilotRequired: yes`, a new eBook PDF first re-opens Step 0F (a new Copilot review or a `final-ebook` waiver) for the changed pages. If you ran the optional Copilot print review, use its confirmed findings as a checklist.
3. Wait until the Part 0 and 0P results are closed (nothing left to check; warnings fixed or accepted).
4. **Create `Manuscript/Trigger/LAYOUT_VERIFIED.md` yourself** (the template is in PHASE 4, Step 0V). Claude never writes it. Then **create `_Pipeline/RERUN_P4.md`**: creating `LAYOUT_VERIFIED.md` alone wakes nothing.

🤖 **Automatic:** checks the file is newer than every PDF and the manuscript, Part 0 is synced, DOCX = MD, 0P is closed, and the workbook is ready (`WORKBOOK_READY.md`, and its print QA closed). If not, `LAYOUT_VERIFY_INCOMPLETE.md` lists what is open and Kindle does not start. A later export makes the confirmation stale; confirm again.

✅ `LAYOUT_VERIFIED.md` is accepted; the congruency check (5c, pass 1) runs and the Kindle build starts. A section without a lock (the first book's Ch1 to Ch5) is not held.

### Step 5c — Congruency check → PHASE 4 Step 0C (report-only; v1.2.6)

🤖 **Automatic:** when a section has all of its pass 1 inputs (manuscript DOCX and MD, final eBook PDF, print PDF; the narration script joins in pass 2) and none has changed for 5 minutes, the local watcher runs the check and writes `_BookGovernance/CongruencyQA/<ChapterName>_Congruency.md`. It emails you only when the verdict is **HOLD**, and again only if the open differences change.

🧑 **You** (also to run it on demand): create an empty `Manuscript/Trigger/RUN_CONGRUENCY.md` (Parts and Lessons: `Trigger/RUN_CONGRUENCY.md` in their folder), or ask Claude. Put `pass 2` on the first line for the second pass. The watcher runs it and renames the file `RUN_CONGRUENCY_done_<timestamp>.md`.

🧑 **Then:**
1. Open the report. The first table shows each format's status; each difference has its page or segment.
2. For each difference: fix the file that is wrong and re-export (the check re-runs by itself), or accept it as intended. Narration-only text (figure descriptions, the spoken pointer in place of the references) is accepted once.
3. To accept what the report shows: `python congruency_check.py <ChapterName> --accept "<reason>"` (add `--keys K1,K2`, from the report's Key column, to accept only some). Read each difference first; never accept a wording difference you haven't looked at.
4. A file listed as older than the manuscript needs re-exporting.

✅ **Done when:** the verdict is **PASS**. Part A (Kindle) starts only on PASS. For a chapter without a lock (the first book's Ch1 to Ch5) the report is for information and never holds anything.

**Pass 2.** After Step 6 (the recording) and its audio check, the same check adds the Kindle DOCX and the audiobook QA. PHASE 5 and PHASE 6.5 start only when pass 2 is PASS.

### Step 6 — Record the audiobook → PHASE 4 Part C (manual, with an automatic check; the last step before PHASE 5)

🧑 **You:** record the chapter in Adobe Audition from the narration script built from the Kindle output, and export `Audiobook/<NN>_<ChapterName>.mp3`. Record only after the lock (`MANUSCRIPT_LOCKED.md`) and the Kindle build: the content audit is already done, so you shouldn't have to re-record (v1.2.5).

🤖 **Automatic:** Audiobook QA transcribes the MP3 with Whisper and compares it with the text. It reports skipped lines, changed wording, retake leftovers, and framework terms heard differently, plus the ACX specs (RMS, peak, noise floor, room tone, 44.1 kHz/192 kbps).

📧 **Email:** the QA summary. The full report lands in the audiobook QA folder.

✅ The QA report has nothing open, or only items you accept.

### Step 7 — RAG, automation, publication QA → PHASES 5, 6, 6.5 (automatic)

**This comes last, after all of the chapter's files are finished:** the manuscript, the eBook and print books (chapter and workbook, verified by you), Kindle, and the audiobook. The RAG index is built from the final wording; automations follow.

🤖 **Automatic chain:** PHASE 5 builds the chapter's RAG index (local, and cloud if enabled) → PHASE 6 runs the automation and marketing activation tests → PHASE 6.5 runs publication QA.

📧 **Email:** only if a phase needs you. Fix the item, then create `RERUN_P5.md`, `RERUN_P6.md`, or `RERUN_P6.5.md`.

✅ PHASE 6.5 finishes, and PHASE 7 starts on its own.

### Step 8 — Final checklist and your sign-off → PHASE 7

🤖 **Automatic, local, no Claude:** the release check pre-fills `<ChapterName>_PHASE7_ReleaseChecklist.md`:
- **Part A:** every item it can prove from the files is ticked, with the evidence. Anything missing is unticked, with the reason. Judgment calls are marked 👤 for you.
- **Part B:** recommendations drafted by the local LLM from the gaps.

📧 **Email:** "N items missing", with the list, or "ready for your sign-off".

🧑 **You:**
1. Fix anything missing, then create `_Pipeline/RERUN_P7.md` to refresh the checklist. It takes seconds.
2. Confirm every 👤 item and decide each Part B row (Accept / Defer / Reject).
3. Sign **Part C**, and choose *Publishing Ready (hold)* or ***Published***.
4. Copy the signed checklist to `_FinalizedReleases/<ChapterName>_PHASE7_ReleaseChecklist_v<chapterVersion>.md`, create the chapter's `Published/` package, and move working drafts to `_Archive/<ChapterName>/`.

✅ The signed checklist is in `_FinalizedReleases/`. The chapter is **Published**.

---

## 3. Book level, at the end

Once every chapter has passed PHASE 4 Part A and Part C:

| Step | Who | What |
|---|---|---|
| B0 consistency + delta check | 🧑 Claude (PHASE 0.9 Mode D, reduced in v1.2.5) | Checks the book for conflicts **between** chapters, and checks what changed in each chapter since its lock (each change must be approved) → `AUDIT_FINAL_CLEAR.md`. Not a full content audit: it reopens a manuscript only for a genuine cross-chapter conflict, with your approval |
| Kindle + audiobook sets | 🧑 Claude (PHASE 4 Part B) | `<BOOK>_KINDLE_EBOOK` (KDP package) and `<BOOK>_AUDIOBOOK` |
| eBook + print books | 🧑 You (InDesign) + Claude (PHASE 3 book mode) | `<BOOK>_EBOOK`, `<BOOK>_PRINT_BOOK` |
| Workbook books | 🧑 You (InDesign) + Claude (PHASE 3W W4–W5) | `<BOOK>_WORKBOOK_EBOOK` (and print, if shipped), after B0 |
| Back-matter glossary | 🧑 You | Update the back-matter glossary from `_BookGovernance/Glossary/Glossary_DriftReport.md`, using the "Add to GLOSSARY" and "differs" sections |
| Book publication QA | 🧑 Claude (PHASE 6.5 book mode) | Book-level Publishing Ready |
| KDP upload, publishing | 🧑 You | After the PHASE 7 sign-offs |

---

## 4. Running checks (every chapter, report-only)

These run on their own whenever their inputs change, and email you when something new turns up. They never edit a chapter.

| Check | Report | What to do |
|---|---|---|
| **References** | `_BookGovernance/References/<ChapterName>_ReferencesCheck.md` | Before lock, fix it in the manuscript, or let PHASE 1 apply the safe fixes. After lock, fix it in InDesign and re-export. |
| **Glossary drift** | `_BookGovernance/Glossary/Glossary_DriftReport.md` | Decide which chapter **defines** each conflicting term, and record it in `_BookGovernance/Glossary/Glossary_Canonical.json` (`definedIn`, `primedIn`, `removeFrom`). The next run applies it. |
| **Print QA** (v1.1.2) | `_BookGovernance/PrintQA/<ChapterName>_PrintQA.md` (workbook: `Workbook_<eBook stem>_PrintQA.md`) | Fix in the print InDesign book and re-export. Wording that should reach the manuscript goes into the eBook, then re-export. Log print-only differences in `<ChapterName>_PrintOnlyDifferences.md`. |
| **Release readiness** (any chapter, on request) | `_BookGovernance/ReleaseChecks/` | Run the release check by hand to see where a chapter stands. |
| **Writing / voice** | next to the file you dropped in the writing-check folder | Drop any draft in (Book or PhD profile) to get a review. |

**The glossary rule in one line:** a term is defined by the chapter that fully teaches it. Earlier chapters may only prime it, and the official master glossary holds only locked chapters.

---

## 5. Cheat sheets

**Files you create:**

| File | Where | What it does |
|---|---|---|
| `Ch<N>_<Title>.md` + `.docx` | `<PASS7_SOURCE>` | Starts PHASE 1 |
| `Ch<N>_<Title>_Exercise<L.N>_Workbook.docx` | `<PASS7_SOURCE>` (with the manuscript) | Becomes the workbook manuscript in PHASE 1 |
| `[x]` ticks | `_Pipeline/WORKBOOK_SELECTION.md` | Chooses the published workbook exercises |
| `APPROVE_EDITORIAL.md` | `_Pipeline/` | Starts PHASE 2 |
| Decision column | `Manuscript/<ChapterName>_LockDecisions.md` | Your call on each lock-audit finding; then create `RERUN_P2.5.md` (v1.2.5) |
| `RERUN_P2.5.md` | `_Pipeline/` | Applies your lock-audit decisions (DOCX, then MD) and locks the manuscript: `Manuscript/Trigger/MANUSCRIPT_LOCKED.md` (v1.2.5) |
| `MANUSCRIPT_REVISED.md` (changed sections + reason; after the lock, `Approved: <initials> <date>`) | `Manuscript/Trigger/` | Records a change. You then create `RERUN_P1.md` (those sections), `RERUN_P2.md` (re-validates, v1.1.3), `RERUN_P2.5.md` (delta audit and a new lock, v1.2.5) in turn |
| `RERUN_P3.5A.md` | `_Pipeline/` | Runs the print build: `InDesign/<ChapterName>_Import.txt` + `_BuildManifest.json` + `_BuildReport.md` (v1.1.3) |
| `<ChapterName>_FigurePrompts.md` | `Figures/` | Not a trigger: written by PHASE 3 A0. Make the figures it lists (RGB + CMYK) and decide its suggestions (v1.2.1) |
| `DSM_APPROVED.md` | `<PACKET_DSM_ROOT>` | Created once by you after reviewing the packet DSM; lets PHASE 3 build packets automatically (v1.2.1) |
| `RERUN_P3.5B.md` | `_Pipeline/` | First line `ebook` (or anything else): builds only the eBook page and its review PDF. First line `idml`: builds `InDesign/<NNN>_Chapter<N>_<Title>.idml` and `Workbook/<NN>-<n>_Exercise_…idml`, and requires the eBook to be reviewed first (v1.2, two-step from v1.3.0) |
| `style_map.json` entries | `<PRINT_DSM_ROOT>` | Map DOCX styles to the print template's styles for the print build; remove `CONFIRM:` once checked (v1.1.3) |
| `<ChapterName>_Import.txt` | `InDesign/` | Not a trigger: place it into a copy of the print template (Show Import Options → Load Styles), then lay out |
| `<ChapterName>_eBook.pdf` | `eBook/` | Completes 3.5 and starts PHASE 4 (does not create the manuscript lock: PHASE 2.5 did) |
| `<NN>_Ex_<L>_<N>_Chapter<C>.pdf` | `<WORKBOOK_BOOK_ROOT>/…` | Completes 3.5 for the workbook and starts the 3W sync |
| `<ChapterName>_Print7x10.pdf` | `InDesign/` (workbook: `<WORKBOOK_BOOK_ROOT>/InDesign/`, or `Workbook/<ChapterName>_Workbook_Print*.pdf` in the `chapter` layout) | Starts the print QA (PHASE 4 Part 0P; workbook: PHASE 3W W2b) |
| `RUN_CONGRUENCY.md` (v1.2.6) | `Manuscript/Trigger/` (Parts: `Trigger/`) | Runs the congruency check now (`pass 2` on the first line for pass 2) |
| `<ChapterName>_PrintOnlyDifferences.md` | `<CH_ROOT>` | Print-only wording the print QA should skip |
| `<NN>_<ChapterName>.mp3` | `Audiobook/` | Starts audiobook QA |
| Decision column | `_Pipeline/P4_DECISIONS.md`, `P3W_DECISIONS.md` | Your call on uncertain wording; then create the matching RERUN file |
| `RERUN_P<n>.md` | `_Pipeline/` | Re-runs a phase (`<n>` includes `3.5`, v1.3.0) |
| `Glossary_Canonical.json` entries | `_BookGovernance/Glossary/` | Glossary defining-chapter decisions |

**Emails you'll get:** PHASE 1 done (review) · PHASE 2 needs you · PHASE 2.5 findings to decide · manuscript locked (start design) · PHASE 4/3W/5/6/6.5 needs you · workbook locked · PHASE 7 checklist · references, glossary, or print QA findings changed · audiobook QA · error alerts (any n8n workflow failing).

**Protected chapters:** chapters that existed before the automation (see the runner's `protectedChapterFolders`) are never *edited* by automation. Report-only checks still cover them, and you run their phases with Claude in chat.

**If something seems stuck:**
- Check `_Pipeline/STATUS.md` and the runner log.
- Confirm the services in section 0 are up. Uploads made while n8n was down aren't seen: re-save the file, or create the RERUN file.

---

## What wakes the runner (v1.3.0)

The phase runner watches only the events in the table below; anything else you create does nothing until you also create a `RERUN` file. Separate local watchers handle the print-PDF check (Step 5b), `RUN_CONGRUENCY.md` (Step 5c) and the nightly RAG refresh (PHASE 6). (Ch1 to Ch5 are protected: the runner ignores their files, and you run their phases with Claude in chat.)

| What you do | Wakes the runner? | Then do |
|---|---|---|
| Drop the manuscript in `<PASS7_SOURCE>` | Yes: PHASE 1 | none |
| Create `_Pipeline/APPROVE_EDITORIAL.md` | Yes: PHASE 2 | none |
| Upload the final eBook PDF to `eBook/`, or create `DesignPacket/Trigger/DESIGN_READY.md` | Yes: PHASE 4 (after 30 quiet minutes) | none; for `copilotRequired: yes` Step 0F pauses it |
| Upload the final workbook PDF | Yes: PHASE 3W W3 | none |
| Create `_Pipeline/RERUN_P<n>.md` | Yes: re-runs that phase | none |
| Save a Copilot report (research, final eBook, design, print, Kindle, publication) | **No** | create the `RERUN_P<n>.md` the handoff names (`2.5`, `4`, `3.5`, `6.5`) |
| Add a line to `Copilot_Waivers.md` | **No** | create the matching `RERUN_P<n>.md` |
| Create `LAYOUT_VERIFIED.md` | **No** | create `_Pipeline/RERUN_P4.md` |
| Create `MANUSCRIPT_REVISED.md` sections | **No** | create `RERUN_P1.md`, then `RERUN_P2.md`, then `RERUN_P2.5.md`, in that order |

## Copilot checkpoints (v1.3.0)

All of these are **you** using Microsoft Copilot (the Microsoft 365 Premium account), at your pace. The same workflow every time:

> pipeline writes the handoff list → you open Copilot → you upload the named files → you paste the prompt from the named file (the block under "Prompt") → Copilot answers → you fill in the front-matter block and save the answer at the named path → Claude validates it and checks every finding → differences are reconciled → you decide → the gate moves on.

A dedicated Copilot agent (`COPILOT_AGENT_INSTRUCTIONS.md`) is optional: the handoff files are authoritative and complete on their own, and Researcher is always started separately. Before you start, read `COPILOT_HANDOFFS/COPILOT_HANDOFF_STANDARD.md` once (status labels, upload limits, privacy check). Don't upload secrets or unrelated files. A report with the wrong manuscript hash, or listing other files, is rejected as stale. A Copilot `PASS` never certifies anything.

### 1. Research verification (PHASE 2.5; required when `copilotRequired: yes`)

| | |
|---|---|
| **When** | After the PHASE 2.5 audit run, while you fill in the decisions log |
| **Why** | A second, independent model checks externally verifiable claims and citations that Claude's Pass 4 also checked |
| **Upload** | Open the chapter's `DeepResearch\START_HERE.md`. **Stage 1:** drag `1_Upload_First` (the DOCX and glossary) into Copilot with the prompt from `PROMPT_PasteIntoCopilot.md`; Copilot returns its own claim list and stops. **Stage 2 (after you write `STAGE 2 FILES ATTACHED`):** drag `2_Upload_Second` (Claude's claim list, the Deep Researcher evidence, the claims registry). The reference list is inside the DOCX; the audit report is optional and not in the folder. One conversation |
| **Mode / prompt** | Researcher · `COPILOT_HANDOFFS/COPILOT_PHASE2_5_RESEARCH_REVIEW.md` |
| **Output / save to** | `COPILOT_RESEARCH_REPORT.md` → `<CH_ROOT>/DeepResearch/` |
| **Pass / fail** | Blocking findings (High claims unsupported/overstated, bad or fabricated citations, contradictions, undecided author-decision items) stop `RESEARCH_CLEAR.md`; non-blocking ones don't |
| **Next** | Re-run PHASE 2.5 (`RERUN_P2.5.md`): Claude writes `RESEARCH_RECONCILIATION.md`, adds rows to the decisions log, you decide, then `RESEARCH_CLEAR.md` and the lock |
| **You approve** | Every correction, and every High claim closed |
| **Invalidated by** | A later change that adds or strengthens an empirical claim, number, causal/absolute statement, or changes a citation (re-run for those sections). Softening, spelling and narrative edits don't |

*Chapters with `copilotRequired: no`:* optional, through a `MANUSCRIPT_REVISED.md` section "Copilot research retrofit".

### 2. Image generation (PHASE 3 A0; optional generator)

| | |
|---|---|
| **When** | After `Figures/<ChapterName>_FigurePrompts.md` is written, for each figure you want to make with Copilot |
| **Why** | A further generator, working from the approved passage and the Visual DSM |
| **Upload** | The passage, the condensed Visual DSM, the registry row, the terminology lock, 1 to 2 approved earlier images (at most 5 images) |
| **Mode / prompt** | Create · `Figures/Copilot/<FigureID>_CopilotHandoff.md` (from `COPILOT_PHASE3_IMAGE_GENERATION.md`) |
| **Output / save to** | One image per request (Option 1; ask for Option 2 as a separate request): `Figures/Drafts/<FigureID>_copilot_<date>_opt<n>.png`; alt text and rationale → `Figures/Copilot/<FigureID>_opt<n>_AltText_Rationale.md`; one `revisionHistory` entry per generation |
| **Pass / fail** | You keep or reject each candidate. Nothing is `approved` here |
| **Next** | Finish in Photoshop/Illustrator; PHASE 3 A0 updates the registry (provenance, `aiGenerated: true`); PHASE 3.5 §15 checks it |
| **You approve** | The image, the alt text, the rationale |
| **Invalidated by** | A change to the passage, the DSM, or the caption |

### 3. Design review (PHASE 3.5; optional)

| | |
|---|---|
| **When** | After the chapter PDF is exported and PHASE 3.5 has run, before PHASE 3.5 certifies Production Ready |
| **Why** | An independent read for DSM compliance, hierarchy, figure/caption mismatches, content drift |
| **Upload** | The exported PDF, condensed DSM checklist, the manuscript, the figure registry; optionally the accessibility checklist |
| **Mode / prompt** | Chat · `COPILOT_HANDOFFS/COPILOT_PHASE3_5_DESIGN_REVIEW.md` |
| **Output / save to** | `COPILOT_DESIGN_REVIEW.md` → `<CH_ROOT>/Governance/Copilot/COPILOT_DESIGN_REVIEW_<date>.md` |
| **Pass / fail** | `PASS`, `CONDITIONAL PASS`, `FAIL`, `AUTHOR DECISION REQUIRED`; none certifies the design |
| **Next** | Re-run PHASE 3.5 (`RERUN_P3.5.md`); Claude verifies and folds confirmed findings into the DesignQA report |
| **You approve** | Production Ready / `DESIGN_READY.md` (always yours) |
| **Invalidated by** | A new export, a manuscript or registry change |

### 4. Final eBook review (PHASE 4 Step 0F; required when `copilotRequired: yes`)

| | |
|---|---|
| **When** | After you upload the final eBook PDF; PHASE 4 pauses and writes `Governance/Copilot/Final_eBook_Handoff.md` |
| **Why** | An independent final read before the PDF becomes the manuscript's wording source |
| **Upload** | The eBook PDF, the manuscript MD (and DOCX), the reference list, figure registry, terminology lock, condensed DSM checklist, `RESEARCH_CLEAR.md` + `RESEARCH_RECONCILIATION.md`, the layout-wording log if any |
| **Mode / prompt** | Chat · `COPILOT_HANDOFFS/COPILOT_PHASE4_FINAL_EBOOK_REVIEW.md` |
| **Output / save to** | `COPILOT_FINAL_EBOOK_REVIEW.md` → `<CH_ROOT>/Governance/Copilot/COPILOT_FINAL_EBOOK_REVIEW_<date>.md` (or add a `final-ebook: waived — <reason> (<initials> <date>)` line to `Governance/Copilot/Copilot_Waivers.md`) |
| **Pass / fail** | `PASS` or accepted `CONDITIONAL PASS` lets Part 0 continue. `FAIL` / `AUTHOR DECISION REQUIRED` stop the chapter until you fix the eBook and re-upload, or accept the findings in writing |
| **Next** | Create `_Pipeline/RERUN_P4.md` (saving the report does not start anything): Claude verifies the findings, writes `Final_eBook_Gate_<date>.md`, and Part 0 runs (0.2 onward) |
| **You approve** | Each non-blocking finding you accept; any wording change that touches research (goes through `MANUSCRIPT_REVISED.md` and a re-lock) |
| **Invalidated by** | A new eBook PDF (the changed pages), or a manuscript change other than the Part 0 changes taken from the PDF that was reviewed |

### 5. Print PDF review (PHASE 4 0P; optional)

| | |
|---|---|
| **When** | After the print PDF is exported and 0P has run |
| **Why** | Independent read for wording drift, order, headers/footers, folios, visible clipping and image problems |
| **Upload** | The print PDF (a reduced reading copy if over 50 MB), the final eBook PDF, the manuscript, the print DSM checklist, the figure registry |
| **Mode / prompt** | Chat · `COPILOT_HANDOFFS/COPILOT_PRINT_PDF_REVIEW.md` |
| **Output / save to** | `COPILOT_PRINT_PDF_REVIEW.md` → `<CH_ROOT>/Governance/Copilot/` |
| **Pass / fail** | Informational for the build; confirmed blocking findings must be fixed in InDesign or accepted |
| **Next** | Create `_Pipeline/RERUN_P4.md`: Claude adds confirmed findings to the 0P drift list; feeds PHASE 6.5 |
| **You approve** | Fixes or acceptance |
| **Invalidated by** | A new print or eBook export |
| **Still required** | InDesign preflight, the printer's specification check, bleed/trim/fonts/colour inspection, and a proof copy |

### 6. Kindle review (PHASE 4 Part B; optional)

| | |
|---|---|
| **When** | After `<BOOK>_Kindle.docx` is built |
| **Why** | Independent check of text completeness, sequence, headings, TOC, figures, references, conversion artifacts |
| **Upload** | The Kindle DOCX (and a PDF of the Kindle Previewer view; EPUB is not an accepted upload), the manuscript, the checklist, the registry, the metadata, the TOC, the reference list |
| **Mode / prompt** | Chat · `COPILOT_HANDOFFS/COPILOT_KINDLE_REVIEW.md` |
| **Output / save to** | `COPILOT_KINDLE_REVIEW.md` → `<BOOK_ROOT>/_BookGovernance/Copilot/` (book level only) |
| **Pass / fail** | Confirmed blocking findings fixed or accepted before Part B passes |
| **Next** | Create `_Pipeline/RERUN_P4.md` (or ask Claude); rebuild if needed; feeds PHASE 6.5 |
| **You approve** | Fixes or acceptance |
| **Invalidated by** | A rebuilt Kindle file or manuscript change |
| **Still required** | EPUB validation (EPUBCheck), Kindle Previewer, and review on representative devices |

### 7. Publication QA (PHASE 6.5; required when `copilotRequired: yes`)

| | |
|---|---|
| **When** | After the deterministic checks in PHASE 6.5 have run |
| **Why** | A cross-format read: drift, missing sections, terminology, figure numbers, metadata, and earlier findings still open |
| **Upload** | The manuscript, eBook PDF, print PDF, Kindle DOCX, workbook files, narration script, metadata, reference list, registry, accessibility artifacts, the earlier Copilot and research reports, the latest congruency report |
| **Mode / prompt** | Chat · `COPILOT_HANDOFFS/COPILOT_PHASE6_5_PUBLICATION_QA.md` (split by chapter if the files are large) |
| **Output / save to** | `COPILOT_PUBLICATION_QA.md` → `<CH_ROOT>/Governance/Copilot/` (book: `_BookGovernance/Copilot/`) |
| **Pass / fail** | One input to Publishing Ready. It can never produce Publishing Ready alone |
| **Next** | Create `_Pipeline/RERUN_P6.5.md`: Claude merges confirmed findings into the PublicationQA report; PHASE 7 starts from Publishing Ready |
| **You approve** | Resolution or written acceptance of each finding; the PHASE 7 sign-off |
| **Invalidated by** | Any rebuilt format file or manuscript change |

### Waivers

Any required Copilot step can be waived by a line in `Governance/Copilot/Copilot_Waivers.md`: `research`, `final-ebook` or `publication-qa`, then `: waived — <reason> (<initials> <date>)`. Claude copies it into the report and the PHASE 7 checklist; it is never silent. If Copilot is unavailable (a usage limit is reached, the service or model changes), a waiver, a delay, or, for research only, a recorded Claude backup run is the correct response (see the backup path in `COPILOT_HANDOFFS/COPILOT_HANDOFF_STANDARD.md`); do not paper over it.
