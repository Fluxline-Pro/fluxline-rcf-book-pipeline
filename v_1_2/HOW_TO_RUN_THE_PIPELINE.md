# How to Run the Pipeline (v1.2)

**For:** <AUTHOR> · **Book:** *<BOOK_TITLE>* — <EDITION> · **Pipeline:** release v1.2 (phase files v3.3; PHASE 3W, 4, 6.5, and 7 at v3.4; PHASE 3.5A v1.0; new PHASE 3.5B v1.0)

This is the operating guide: what to do, in what order, one step at a time. The PHASE files hold the full rules; `MASTER_PIPELINE_OVERVIEW.md` holds every path, gate, and trigger, and wins if anything here disagrees.

**How each step is written:**
- 🤖 **Automatic:** what starts it, what it does, and whether you get an email.
- 🧑 **You:** what you do by hand, and where (Claude chat, Claude Design, InDesign, Audition, a file you create).
- ✅ **Done when:** the file or email that tells you the step is finished.

**The golden rules:**
1. **Your uploads are the switches.** The final **eBook PDF** locks a chapter's manuscript, and the final **workbook PDF** locks its workbook manuscript. Everything downstream starts from those two uploads, so upload only final exports.
2. **Email is your inbox for the pipeline.** You're only emailed when you're needed, or when something is ready for you. No email means it's still running, or nothing needs you.
3. **Nothing publishes itself.** Every generated item is a draft, and only you approve, sign off, and mark a chapter Published.
4. **To redo a step,** create `<CH_ROOT>/_Pipeline/RERUN_P<n>.md`, where `<n>` is 1, 2, 3W, 3.5A, 3.5B, 4, 5, 6, 6.5, or 7. Anything you write inside is passed to Claude.
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

📧 **Email:** "PHASE 2 done. Ready for PHASE 3 / 3.5", or "PHASE 2 needs you" with the blockers.

✅ `Governance/Trigger/GOVERNANCE_READY.md`.

If PHASE 2 needs you, resolve the listed items (Needs Author Review, Tier C proposals), then create `_Pipeline/RERUN_P2.md`.

**Revising the manuscript later (v1.1.3).** To change the manuscript after PHASE 1, but before you upload the final eBook PDF:
1. Edit the DOCX in `Manuscript/`, regenerate the MD from it, and bump the version.
2. Create `Manuscript/Trigger/MANUSCRIPT_REVISED.md` listing the changed sections and why.

PHASE 1 regenerates what those sections feed, and PHASE 2 re-validates. After the eBook upload, change wording in the eBook instead.

### Step 2b — Print build → PHASE 3.5A (automatic import, then your layout)

🤖 **Automatic, on request** (`_Pipeline/RERUN_P3.5A.md`, or run `idml_build.py` by hand): once the manuscript DOCX is in `Manuscript/`, the print build turns it into `InDesign/<ChapterName>_Import.txt`. Every paragraph and character style is set to the print template's style, through `<PRINT_DSM_ROOT>/style_map.json`. It also writes `_BuildManifest.json` and `_BuildReport.md` beside it. It never changes the manuscript or the template.

🧑 **You:**
1. Read `InDesign/<ChapterName>_BuildReport.md`. If anything is **unmapped**, add or confirm the entry in `<PRINT_DSM_ROOT>/style_map.json` (remove the `CONFIRM:` prefix once checked), then re-run. A missing figure needs its CMYK TIFF in `Figures/CMYK/` (the RGB PNG/JPG in `Figures/RGB/` is for the eBook only).
2. In InDesign, open a **copy** of the print template, and File → Place the import with **Show Import Options** → Use Tagged Text, **Load Styles**.
3. Replace each `[[FIGURE N …]]` placeholder with its image, set the running heads, and lay out the chapter.
4. Export the print PDF to `InDesign/<ChapterName>_Print7x10.pdf` (Step 5b).

✅ The build report says **PASS** and the chapter is laid out from it.

### Step 2c — eBook first, then the print IDMLs → PHASE 3.5B (v1.2, the default print build)

🤖 **Automatic, on request** (`_Pipeline/RERUN_P3.5B.md`, or ask Claude):
1. The chapter's eBook page, `<EBOOK_DSM_ROOT>/Chapter<N>_eBook.dc.html`, is built from the DOCX (and the Claude Design draft, if there is one). It is paginated to 8.5×11 and printed to a review PDF. With your permission, it is published as a private artifact. The same happens for the exercise's workbook eBook page.
2. The print IDMLs then replicate the eBook:
   - the chapter, built on your last finished chapter IDML in `<PRINT_DSM_ROOT>`, goes to `InDesign/<NNN>_Chapter<N>_<Title>.idml`;
   - the exercise, cloned from your previous exercise IDML, goes to `Workbook/<NN>-<n>_Exercise_<L>_<N>_<Name>.idml`.
3. Optionally, with your permission, a structural proof is rendered through Adobe and saved in `_Proofs/`.

🧑 **You:**
1. Review the eBook artifact or PDF.
2. Open each IDML in InDesign. Re-apply fonts where needed (the proofs use substitutes), and check the callout badges, figures, and page breaks.
3. Export the print PDFs (Step 5b).

The design rules are in PHASE 3.5B §2: one column only; black, white, and gold; the template's print callouts; CMYK TIFFs for print only.

✅ Both IDMLs are in place with the build report's flags addressed, and the print PDFs are exported.

### Step 3 — Design and layout → PHASE 3 + 3.5 (manual)

🧑 **You, in Claude Design and InDesign:**
1. In **Claude Design**, use the PHASE 3 Part B prompt and the files in `DesignPacket/uploads/` to build the packet: deck, guides, reference guides, workbook, opener, figures, and the eBook / print 7×10 / workbook layouts.
2. Export the figure images to `DesignPacket/figures_export/`, plus the slides (PPTX + PDF) and the eBook exports.
3. Run the **PHASE 3.5 QA** (report-only), and fix the findings in Claude Design until it says Production Ready.
4. Finish the **print** book in InDesign from the PHASE 3.5B IDML (Step 2c), or lay it out from the PHASE 3.5A import (Step 2b). The eBook is built in Claude Design. **The wording is already final** (v1.1.3): it was settled in the DOCX before PHASE 1. A change you still need goes into the DOCX, with `MANUSCRIPT_REVISED.md`, not into a layout. Place the callouts you approved from the PHASE 1 recommendations.
5. Lay out the **workbook** in InDesign.

✅ Design is finished, and you're ready to export the final PDFs.

### Step 4 — Upload the final eBook PDF → PHASE 4 (sync, references, glossary lock, Kindle)

🧑 **You:** export the chapter's **final** eBook PDF and save it as `eBook/<ChapterName>_eBook.pdf`. This completes PHASE 3.5.

🤖 **Automatic**, after 30 minutes with no further changes in `eBook/`:
1. **3.5 closed:** writes `DESIGN_READY.md` as attested by your upload, if PHASE 3.5 hadn't already.
2. **Part 0, manuscript sync:** brings your InDesign wording back into the manuscript MD and DOCX (the manuscript is now **locked**). Writes `MANUSCRIPT_SYNCED.md`.
3. **0R, references re-check:** report-only, since the manuscript is now locked.
4. **0G, glossary lock:** refreshes the chapter glossary from the locked text and rebuilds the **official master glossary** and the drift report.
5. **Part A, Kindle:** DOCX, HTML, metadata, and figures.

📧 **Email:** only if it needs you, for example wording changes it couldn't decide. Fill in the **Decision** column in `_Pipeline/P4_DECISIONS.md` (*Accept PDF*, *Keep manuscript*, or *Defer* with initials), then create `_Pipeline/RERUN_P4.md`.

✅ The PHASE 4 checklist shows `gateStatus: PASS`, and PHASE 5 starts on its own.

**Reference or glossary findings** don't block Kindle; they reach you by email. A reference fix after lock goes into InDesign: re-export the eBook PDF, and Part 0 re-syncs automatically.

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

✅ The report shows 0 text differences to check and 0 layout errors, and you've fixed or accepted every warning. It doesn't block Kindle, but PHASE 6.5 and PHASE 7 need it closed.

### Step 6 — Record the audiobook → PHASE 4 Part C (manual, with an automatic check)

🧑 **You:** record the chapter in Adobe Audition from the narration script built from the Kindle output, and export `Audiobook/<NN>_<ChapterName>.mp3`.

🤖 **Automatic:** Audiobook QA transcribes the MP3 with Whisper and compares it with the text. It reports skipped lines, changed wording, retake leftovers, and framework terms heard differently, plus the ACX specs (RMS, peak, noise floor, room tone, 44.1 kHz/192 kbps).

📧 **Email:** the QA summary. The full report lands in the audiobook QA folder.

✅ The QA report has nothing open, or only items you accept.

### Step 7 — RAG, automation, publication QA → PHASES 5, 6, 6.5 (automatic)

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
| B0 final delta audit | 🧑 Claude (PHASE 0.9 Mode D) | Re-audits the chapters whose wording changed after their last check → `AUDIT_FINAL_CLEAR.md` |
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
| `MANUSCRIPT_REVISED.md` (changed sections + reason) | `Manuscript/Trigger/` | After PHASE 1 and before the eBook upload: re-runs PHASE 1 for those sections, then PHASE 2 re-validates (v1.1.3) |
| `RERUN_P3.5A.md` | `_Pipeline/` | Runs the print build: `InDesign/<ChapterName>_Import.txt` + `_BuildManifest.json` + `_BuildReport.md` (v1.1.3) |
| `RERUN_P3.5B.md` | `_Pipeline/` | Runs the eBook-first print build: the eBook page, then `InDesign/<NNN>_Chapter<N>_<Title>.idml` and `Workbook/<NN>-<n>_Exercise_…idml` (v1.2) |
| `style_map.json` entries | `<PRINT_DSM_ROOT>` | Map DOCX styles to the print template's styles for the print build; remove `CONFIRM:` once checked (v1.1.3) |
| `<ChapterName>_Import.txt` | `InDesign/` | Not a trigger: place it into a copy of the print template (Show Import Options → Load Styles), then lay out |
| `<ChapterName>_eBook.pdf` | `eBook/` | Completes 3.5 and starts PHASE 4 (locks the manuscript and glossary) |
| `<NN>_Ex_<L>_<N>_Chapter<C>.pdf` | `<WORKBOOK_BOOK_ROOT>/…` | Completes 3.5 for the workbook and starts the 3W sync |
| `<ChapterName>_Print7x10.pdf` | `InDesign/` (workbook: `<WORKBOOK_BOOK_ROOT>/InDesign/`, or `Workbook/<ChapterName>_Workbook_Print*.pdf` in the `chapter` layout) | Starts the print QA (PHASE 4 Part 0P; workbook: PHASE 3W W2b) |
| `<ChapterName>_PrintOnlyDifferences.md` | `<CH_ROOT>` | Print-only wording the print QA should skip |
| `<NN>_<ChapterName>.mp3` | `Audiobook/` | Starts audiobook QA |
| Decision column | `_Pipeline/P4_DECISIONS.md`, `P3W_DECISIONS.md` | Your call on uncertain wording; then create the matching RERUN file |
| `RERUN_P<n>.md` | `_Pipeline/` | Re-runs a phase |
| `Glossary_Canonical.json` entries | `_BookGovernance/Glossary/` | Glossary defining-chapter decisions |

**Emails you'll get:** PHASE 1 done (review) · PHASE 2 done (start design) or needs you · PHASE 4/3W/5/6/6.5 needs you · workbook locked · PHASE 7 checklist · references, glossary, or print QA findings changed · audiobook QA · error alerts (any n8n workflow failing).

**Protected chapters:** chapters that existed before the automation (see the runner's `protectedChapterFolders`) are never *edited* by automation. Report-only checks still cover them, and you run their phases with Claude in chat.

**If something seems stuck:**
- Check `_Pipeline/STATUS.md` and the runner log.
- Confirm the services in section 0 are up. Uploads made while n8n was down aren't seen: re-save the file, or create the RERUN file.
