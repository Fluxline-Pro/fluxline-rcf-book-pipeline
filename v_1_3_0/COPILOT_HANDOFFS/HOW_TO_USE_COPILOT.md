# How to use Copilot in the pipeline (author's guide, v1.3.0)

**For:** <AUTHOR> · **Short version:** Copilot is your second reviewer and an extra image maker. Claude builds and keeps the gates. You start every Copilot step, and nothing Copilot says changes a file until you decide.

## One-time setup

1. Create the Copilot agent (or saved instructions) from `COPILOT_AGENT_INSTRUCTIONS.md` (paste the fenced block; the Instructions field allows 8,000 characters and the block is about 5,200). Whether your Premium plan includes Agent Builder is not documented: if it doesn't, paste the block as the first message of each session. **Research verification must be run in Researcher mode directly** (an agent can't be switched to Researcher), so paste the block there, then the handoff prompt.
2. Keep these open in a folder you can reach from Copilot's upload dialog: the `COPILOT_HANDOFFS/` prompt files, and the chapter's `Governance/Research/Copilot_Research_Handoff.md` packet where one exists.
3. First run only: ask Copilot "List the files you can see" after uploading. If Researcher cannot see uploaded files on your plan, paste the text into the chat instead, and tell Claude so the handoff can be updated.
4. Copilot's limits (checked October 2026; they change): 20 files per conversation, 50 MB each; PDF, DOCX, XLSX, PPTX, MD, TXT, JSON, CSV and images are accepted, **EPUB and IDML are not**. Images come in three sizes (1024×1024, 1024×1536, 1536×1024) and are RGB concepts, never print files. Researcher may have a monthly query allowance.

## The routine (every time)

1. The pipeline (Claude) writes a handoff packet: which files, which prompt.
2. You open Copilot (the agent), choose the mode in the table below, upload **only** the named files.
3. You paste the prompt from the handoff file (the fenced block).
4. Copilot answers. Copy the whole answer into a new file at the path the handoff names. Fill in the front-matter block (hash, date, files).
5. Tell Claude, or create the `RERUN_P<n>.md` file the handoff names. **Saving the file does not start anything by itself.**
6. Claude checks the report (hash, file list, every source named) and brings you only the items that need your decision.
7. You decide. Claude applies decisions through the normal route (the PHASE 2.5 decisions log, or `MANUSCRIPT_REVISED.md`).

If a required Copilot step isn't possible (allowance used up, no access), add a line to `Governance/Copilot/Copilot_Waivers.md`: `research: waived — <reason> (<initials> <date>)` (also `final-ebook`, `publication-qa`). Waivers are copied into the reports; they are never silent.

## Where Copilot appears, by PHASE

| PHASE | Step | Use Copilot to | Mode | Upload | Prompt file | Save as (under `<CH_ROOT>/`) | Required? | Then |
|---|---|---|---|---|---|---|---|---|
| 0.9, 1, 2 | none | (nothing: Claude and the local tools do these) | | | | | | |
| **2.5** | §3.2b | Verify the chapter's claims and citations independently of Claude | **Researcher** | chapter DOCX, glossary; later the ScienceClaims file and Deep Researcher results | `COPILOT_PHASE2_5_RESEARCH_REVIEW.md` | `Governance/Research/COPILOT_RESEARCH_REPORT.md` | When the lock has `copilotRequired: yes` | `RERUN_P2.5.md` → reconciliation → you decide → `RESEARCH_CLEAR.md` → lock |
| 3 | A0 (figures) | Make a concept image for a figure (extra to Gemini/Firefly) | **Create** | passage, `DSM_CopilotCard.md`, registry row, 1–2 approved images | `COPILOT_PHASE3_IMAGE_GENERATION.md` (one handoff per figure in `Figures/Copilot/`) | images → `Figures/Drafts/`; text → `Figures/Copilot/<FigureID>_AltText_Rationale.md` | Optional | finish in Photoshop; Claude updates the registry (`aiGenerated: true`); PHASE 3.5 checks |
| 3.5 | §15 | Second look at the exported chapter for DSM, hierarchy, captions, drift | Chat | chapter PDF (a copy outside `eBook/`), DSM card, manuscript, registry | `COPILOT_PHASE3_5_DESIGN_REVIEW.md` | `Governance/Copilot/COPILOT_DESIGN_REVIEW_<date>.md` | Optional | `RERUN_P3.5.md` |
| **4** | Step 0F | Final read of the eBook PDF before it becomes the wording source | Chat | eBook PDF, manuscript MD (+DOCX), reference list, registry, terminology lock, DSM card, research clearance files | `COPILOT_PHASE4_FINAL_EBOOK_REVIEW.md` | `Governance/Copilot/COPILOT_FINAL_EBOOK_REVIEW_<date>.md` | When `copilotRequired: yes` | `RERUN_P4.md` → `Final_eBook_Gate_<date>.md` → Part 0 |
| 4 | 0P (before your InDesign verification, Step 0V) | Check the print PDF for drift, order, folios, clipping | Chat | print PDF (reduced copy if > 50 MB), eBook PDF, manuscript, print DSM card, registry | `COPILOT_PRINT_PDF_REVIEW.md` | `Governance/Copilot/COPILOT_PRINT_PDF_REVIEW_<date>.md` | Optional | `RERUN_P4.md` |
| 4 | Part B (book) | Check the Kindle package's text, TOC, headings, references | Chat | Kindle DOCX, Previewer PDF, manuscripts, checklist, registry, metadata | `COPILOT_KINDLE_REVIEW.md` | `_BookGovernance/Copilot/COPILOT_KINDLE_REVIEW_<date>.md` | Optional | `RERUN_P4.md` |
| 5, 6 | none | (nothing) | | | | | | |
| **6.5** | §9b | Cross-format read of everything, plus earlier findings still open | Chat | manuscript, eBook, print, Kindle, workbook, narration script, metadata, registry, earlier reports, congruency report | `COPILOT_PHASE6_5_PUBLICATION_QA.md` | `Governance/Copilot/COPILOT_PUBLICATION_QA_<date>.md` | When `copilotRequired: yes` | `RERUN_P6.5.md` |
| 7 | none | (nothing; your sign-off) | | | | | | |

`<CH_ROOT>` is `Chapters/<ChapterName>/Final/`. Book-level reviews go to `_BookGovernance/Copilot/`.

## What Copilot does NOT replace

| Copilot | Still required |
|---|---|
| Final eBook / print / Kindle review | Part 0 text comparison, congruency check, InDesign preflight, printer specs, EPUBCheck, Kindle Previewer, device previews, a proof copy |
| Research review | Claude's Pass 4, Deep Researcher plus your review, `references_check.py`, your decision on every High claim |
| Publication review | The deterministic checks, human checks and your PHASE 7 sign-off |
| Images | Your approval, PHASE 3.5, Photoshop/Illustrator finishing |

## How to read a Copilot report

- **PASS** means "nothing blocking in what it could inspect". It is not approval.
- **CONDITIONAL PASS**: only non-blocking items; accept each in writing or fix.
- **FAIL / AUTHOR DECISION REQUIRED**: stop; blocking items must be fixed or accepted by you.
- Evidence labels: VERIFIED, PARTIALLY SUPPORTED, UNSUPPORTED, OVERSTATED, NEEDS CITATION, CANNOT VERIFY. Claude opens every source Copilot names, so you do not have to trust a citation because Copilot gave it.
- Copilot should never suggest rewriting stories, metaphors, framework definitions or exercises just because they lack citations. If it does, ignore that item.

## What makes a result stale

- Research report: the text gained or strengthened a claim, a number or a citation after the report. Softening and spelling fixes do not stale it.
- Final eBook review: a new eBook PDF, or any manuscript change other than the Part 0 changes taken from the PDF it reviewed.
- Print, Kindle, design, publication reviews: a new export or build, or a manuscript change.
When unsure, tell Claude; it re-runs only the changed sections.

## Your six Ch1–6 packets

Each chapter already has `Governance/Research/Copilot_Research_Handoff.md` and `ChN_DeepResearcher_Evidence_Bundle.md`. For each: Step 1 uploads → paste the prompt → wait for Copilot's own claim list → Step 2 uploads → save the report → tell Claude. Add a "Copilot research retrofit" section (with your approval line) to the chapter's `MANUSCRIPT_REVISED.md` before any wording change is made. No image handoffs are needed for Ch1–6.

## If Copilot behaves oddly

- It answers without listing files: ask "List the files you can see" and re-upload.
- It invents a citation: say so in the chat, and mark that item CANNOT VERIFY in your notes. Claude will check it anyway.
- It rewrites text: tell it "Do not rewrite. Quote and recommend only." and keep the report only if the findings table is intact.
- It refuses or truncates a long PDF: split by chapter and note "part 1 of 3" in the front matter.
- Anything it says conflicts with the pipeline files: the pipeline files win. Tell Claude.
