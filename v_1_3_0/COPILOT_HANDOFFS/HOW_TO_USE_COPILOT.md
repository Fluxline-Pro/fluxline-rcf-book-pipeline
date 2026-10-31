# How to use Copilot in the pipeline: your guide (v1.3.0)

**For:** `<AUTHOR>`. This is the short version. The full rules are in the handoff files; the full step-by-step pipeline guide is `HOW_TO_RUN_THE_PIPELINE.md`.

## The idea in four lines

1. **Claude** builds things and keeps the gates. **Local tools and the runner** do the automatic work.
2. **Copilot** is your second opinion: it checks research, makes concept images, and does independent final reads. **You start it, every time.**
3. Copilot's answer is advice. Claude checks it, and **you decide**. Nothing Copilot says changes a file by itself.
4. If Copilot isn't available, you can wait, skip with a written waiver, or (research only) use Claude as a backup.

## Who does what, by PHASE

🤖 = automatic (runner and local tools; you only get an email if you're needed) · 🧠 = Claude (builds, checks, reconciles) · 🧑 = you · 🧭 = Copilot, which **you** start · ✋ = a step-in only you can make

| PHASE | What happens | 🤖 / 🧠 | 🧑 Your part | 🧭 Copilot? |
|---|---|---|---|---|
| **0.9** Book audit | Checks the whole draft for drift | 🧠 report only | ✋ Decide the canonical terms | No |
| **1** Creation | Builds the chapter's files from your manuscript | 🤖 starts when you drop the manuscript; 🧠 writes them | Review the editorial suggestions | No |
| **2** Governance | Validates and certifies the chapter | 🤖 / 🧠 | ✋ Approve or reject proposed changes | No |
| **2.5** Lock audit | Reads the chapter in full, then locks the manuscript | 🤖 / 🧠 audit, reconcile, apply | ✋ **Decide every finding**, then ask for the re-run | **Yes: research review** (Researcher) |
| **3** Design + figures | Training materials, figures and the design packet; then the eBook pass, **your notes**, and the print IDML created from the eBook (book and workbook) | 🤖 / 🧠 | Make the figures (Photoshop); review the eBook and write notes; **review, edit and pass off the print book in InDesign** | **Optional: image generation** (Create) |
| **3.5** Design QA | Checks the design against the design system | 🧠 | ✋ Say it's Production Ready | Optional: design review |
| **3W** Workbook | Workbook manuscript and layouts | 🤖 / 🧠 checks | Produce the workbook eBook and print PDFs | No |
| **4** Part 0 | Compares the manuscript with your final eBook PDF | 🤖 / 🧠 | ✋ Decide any wording differences | **Yes: final eBook review** (Step 0F) |
| **4** 0P | Compares print with eBook | 🤖 report | Fix in InDesign | Optional: print review |
| **4** Step 0V | **You verify the eBook and print books, chapter and workbook, in InDesign** | 🤖 checks it | ✋ **Create `LAYOUT_VERIFIED.md` yourself** | Use Copilot's findings as a checklist, if you ran it |
| **4** Part A | Kindle build | 🤖 / 🧠 (starts after Step 0V) | Check in Kindle Previewer | No |
| **4** Part C | Audiobook (**always last**, before PHASE 5) | 🧠 script; 🤖 audio check | ✋ Record and master it | No |
| **4** Part B | Book-level Kindle eBook and audiobook set (after every chapter passes Part A and Part C) | 🤖 / 🧠 | Fix confirmed findings | Optional: Kindle review |
| **5, 6** | RAG index and automations | 🤖 | Fix only if emailed | No |
| **6.5** Publication QA | Checks every format | 🤖 / 🧠 | Fix findings | **Yes: cross-format review** |
| **7** Release | Final checklist | 🤖 pre-fills | ✋ **Sign it** | No |

**Order of work:** manuscript (DOCX and MD) → eBook and print book, chapter and workbook, verified by you → Kindle → audiobook → PHASE 5.

## When you use Copilot (a quick list)

| When | Mode | Prompt file | Required? |
|---|---|---|---|
| PHASE 2.5, research | **Researcher** | `COPILOT_PHASE2_5_RESEARCH_REVIEW.md` | Yes, for chapters marked `copilotRequired: yes` |
| PHASE 3, a figure | **Create** | `Figures/Copilot/<FigureID>_CopilotHandoff.md` (built from `COPILOT_PHASE3_IMAGE_GENERATION.md`) | Optional |
| PHASE 3.5, design | Chat | `COPILOT_PHASE3_5_DESIGN_REVIEW.md` | Optional |
| PHASE 4 Step 0F, your final eBook PDF | Chat | `COPILOT_PHASE4_FINAL_EBOOK_REVIEW.md` | Yes, when `copilotRequired: yes` |
| PHASE 4 0P, print PDF | Chat | `COPILOT_PRINT_PDF_REVIEW.md` | Optional |
| PHASE 4 Part B, Kindle (book level) | Chat | `COPILOT_KINDLE_REVIEW.md` | Optional |
| PHASE 6.5, whole publication | Chat | `COPILOT_PHASE6_5_PUBLICATION_QA.md` | Yes, when `copilotRequired: yes` |

Chapters with `copilotRequired: no` (Ch1 to Ch6 today) need none of these; you've chosen to run the research review on all six anyway.

## The routine (every Copilot step)

1. Open Copilot in the mode from the table. Upload **only** the files the handoff names.
2. Paste the prompt (the boxed block in the prompt file).
3. Copilot answers. Copy the whole answer into a new file at the path the handoff gives. Fill in the front matter.
4. Tell Claude, or create the `RERUN_P<n>.md` file the handoff names. **Saving the file does not start anything.**
5. Claude checks the report and every source it names, then brings you only what needs a decision.
6. You decide. Claude applies your decisions the normal way.

## Two special cases

**Research is two-stage, in one conversation.** Stage 1: upload the chapter, references and glossary. Copilot makes its own claim list and stops. You read it, then upload Claude's claim list and the Deep Researcher evidence and write `STAGE 2 FILES ATTACHED`. This stops Claude's findings from steering Copilot.

**Images are one per request.** Ask for Option 1. For another composition, ask for Option 2 as a new request. Each is saved and recorded separately (`<FigureID>_copilot_<date>_opt<n>.png`, one `revisionHistory` entry each). Copilot's images are small RGB concepts: finish them in Photoshop or Illustrator. You approve them, with PHASE 3.5.

## Optional: a dedicated Copilot agent

**The handoff contract is authoritative. Persistent agent instructions reduce repetition but are not required for correctness.** If you set up an agent, use `COPILOT_AGENT_INSTRUCTIONS.md` (it fits the 8,000-character Instructions field). Whether your Premium plan includes Agent Builder isn't documented; if not, paste the text as the first message of a session. **Research is always its own Researcher session**, not the agent.

## Limits and what to do when Copilot can't

- 20 files per conversation, 50 MB each. PDF, DOCX, XLSX, PPTX, MD, TXT, JSON, CSV and images work; **EPUB and IDML don't**.
- Researcher is included with Microsoft 365 Premium with extensive usage. Microsoft does not currently publish a fixed Researcher query count for Premium. Feature limits may vary by feature, entry point, system conditions, and service changes. Copilot provides in-product notifications when applicable limits are approached or reached. Batching a chapter into one Researcher run is a preference, not a quota.
- If Copilot can't do a required step (limit reached, outage, no access), you can: **wait**; **waive** it by adding a line to `Governance/Copilot/Copilot_Waivers.md`: `research: waived — <reason> (<initials> <date>)` (also `final-ebook`, `publication-qa`); or, for research only, **ask Claude to run it as a backup**. A Claude backup is less independent, is recorded as a backup, and is never counted as a Copilot review.

## Reading a Copilot report

- **PASS** means nothing blocking in what it could inspect. It is not approval.
- **CONDITIONAL PASS**: only small items. Accept each in writing or fix it.
- **FAIL / AUTHOR DECISION REQUIRED**: stop; fix the blocking items or accept them in writing.
- Copilot should never ask you to rewrite stories, metaphors, framework definitions or exercises just because they have no citation. Ignore that kind of item.
- Claude opens every source Copilot names, so you don't have to trust a citation because Copilot gave it.

## What makes a result out of date

- Research report: after it, the text gained or strengthened a claim, a number or a citation. Softening, spelling and story edits don't count.
- Final eBook review: a new eBook PDF.
- Design, print, Kindle and publication reviews: a new export or build, or a manuscript change.

When unsure, tell Claude; it re-runs only the changed parts.

## Ch1 to Ch6

Each chapter has its own **`DeepResearch\`** folder (reference only): open `START_HERE.md`, drag `1_Upload_First`, then `2_Upload_Second`, and save the results in the same folder. In one Researcher conversation, for each chapter: Stage 1 uploads → paste the prompt → read Copilot's claim list → Stage 2 uploads → write `STAGE 2 FILES ATTACHED` → save the report → tell Claude. Before any wording changes, add a "Copilot research retrofit" section (with your approval line) to the chapter's `MANUSCRIPT_REVISED.md`. No image handoffs are needed for these chapters.

## If Copilot behaves oddly

- It doesn't list files: ask "List the files you can see" and re-upload.
- It invents a citation: mark it CANNOT VERIFY in your notes; Claude checks everything anyway.
- It rewrites text: tell it "Do not rewrite. Quote and recommend only."
- It truncates a long PDF: split it by chapter and note "part 1 of 3" in the front matter.
- It disagrees with the pipeline files: the pipeline files win. Tell Claude.
