# Fluxline RCF Book Pipeline

A phase-by-phase AI workflow for taking a finished book manuscript all the way to published formats — eBook, print, Kindle, audiobook, training materials, a RAG knowledge base, and grounded marketing — without losing control of the manuscript or the voice.

It is a set of Markdown prompts. You paste a phase into an AI assistant (these were written against Claude, Claude Design, and a local LLM, and read fine in most assistants), it produces that phase's outputs, and a gate decides whether the chapter moves on. Nothing here is code you install. Where a phase relies on a deterministic script, such as the print builds that write InDesign IDML, the phase file specifies it as a reference implementation you run from your own tools folder.

Built for *RCF: Resonance Core Framework* by Terence Waters at [Fluxline.pro](https://fluxline.pro), and shared for other authors who are building a real production pipeline rather than one-off prompts.

**AI is optional.** You can run the pipeline AI-assisted, with AI only for checking, or entirely by hand as a checklist-and-gate system. See [Choosing your path](#choosing-your-path-with-ai-with-less-ai-or-without-it), and [Adopting it for your publishing work](#adopting-it-for-your-publishing-work) for what to tell someone who wants to use it.

**Current version: v1.3.0** (BETA; run `v_1_3_0/ROLLOUT_TEST_PLAN.md` on a sandbox chapter before relying on it) (phase files in [`v_1_3_0/`](./v_1_3_0)). v1.3.0 adds **Microsoft Copilot as a governed second opinion**, always human-initiated: independent research verification in PHASE 2.5 (`RESEARCH_CLEAR.md` before the lock), Copilot image generation as an optional figure source in PHASE 3, and independent reviews of the design, the final eBook PDF (before it becomes the wording source), the print PDF, the Kindle files, and the whole publication. The prompts and upload lists are in [`v_1_3_0/COPILOT_HANDOFFS/`](./v_1_3_0/COPILOT_HANDOFFS). Copilot never edits the manuscript, certifies anything, or replaces a deterministic check, and nothing in the pipeline calls it. The release also adds **Pass 4**, science and source verification (PHASE 0.9 and 2.5), and makes **sidebars an optional per-book setting**. v1.2.6 adds Step 0C in PHASE 4, the **congruency check**: one deterministic report (PASS or HOLD) that the manuscript, eBook, print PDF, narration script and workbook say the same thing and every file is current against the lock; pass 1 gates the Kindle build, pass 2 (after the audiobook) gates PHASE 5 and 6.5. v1.2.5 adds PHASE 2.5, the **manuscript lock audit**: each chapter's full content audit now runs after governance and before design, the author decides every finding, the fixes go into the DOCX, and the manuscript is locked (`MANUSCRIPT_LOCKED.md`). Every design and production phase requires the lock, and the end-of-book audit is reduced to a cross-chapter consistency check. v1.2.4 sets the workbook eBook's page numbering and final PDFs, makes write-in questions Montserrat, adds numbered badge circles, styles in-text figure references in print, and starts every chapter on a right-hand page. v1.2.3 refined print and the workbook: print callouts are separate frames copied from the template, and the workbook's how-to steps are roman with italic parentheticals. v1.2.2 made three Design System artifacts the source for every export: the book eBook, the workbook eBook, and the design packet. It also adds the workbook's numbered "How to work this exercise" steps. v1.2 added PHASE 3.5B, the **eBook-first print build**: the eBook is built first, then the print documents are generated as ready-to-open InDesign **IDML** files that replicate it, for both the chapter and its workbook exercise. v1.2.1 added:
- print pagination and spacing rules;
- an automatic PHASE 3 start once governance passes: Gemini figure prompts, a checklist of RGB and CMYK files to make, and the design packet built as Claude artifacts.

Previous versions: [v1.2.6](./v_1_2_6), [v1.2.5](./v_1_2_5), [v1.2.4](./v_1_2_4), [v1.2.3](./v_1_2_3), [v1.2.2](./v_1_2_2), [v1.2.1](./v_1_2_1), [v1.2](./v_1_2), [v1.1.3](./v_1_1_3), [v1.1.2](./v_1_1_2), [v1.1 / v1.1.1](./v_1_1), [v1.0.4](./v_1_0_4), [v1.0.3](./v_1_0_3), [v1.0.2](./v_1_0_2), [v1.0](./v1_0) · See the [changelog](./CHANGELOG.md) for what changed and why.

---

## What problem this solves

A book that ships in six formats has the same content living in twenty places: manuscript, workbook, slides, reference guides, narration script, eBook HTML, print layout, Kindle file, vector store, marketing copy. Each one drifts. A term gets redefined in the slides. A figure gets renumbered in print but not in Kindle. A marketing post claims something the book never says.

This pipeline treats the manuscript as the only source of truth and makes every other artifact answer to it — with validation, correction, and a human sign-off at the end.

## Before the phases: the editing passes (PASS 0–7)

The phases don't write the book. They start from a manuscript that has already been through seven editing passes on top of the original draft (PASS 0), eight stages in all, each with a single job, so a pass never has to fix structure, terminology, and commas all at once. Every pass kept its own folder, so any chapter can be traced back to the draft it came from.

| Pass | Focus | What it settles |
|---|---|---|
| **PASS 0 — Original draft** | The author's draft, as written | The raw material. Kept untouched as the reference point for every later pass. |
| **PASS 1 — Coherence & restructure** | Big-picture structure | Each chapter has one clear job, ideas sit in the chapter that owns them, and the argument flows from start to finish. Sections move, merge, or split here. |
| **PASS 2 — Term coherence** | The framework's vocabulary, chapter by chapter | Each core term means one thing wherever it's used, and is introduced before it's relied on. |
| **PASS 3 — Term consistency & book architecture** | The same vocabulary across the whole book, plus the book's skeleton | Terms are consistent book-wide, and the architecture (parts, lessons, chapter order, recurring sections) is fixed. |
| **PASS 4 — Voice, clarity & transitions** | How it reads | The author's voice holds throughout, dense passages are clarified, and chapters hand off to each other. |
| **PASS 5 — Transitions, editing, spelling, grammar & references** | Line-level correctness | Copy edit and proofread. Transitions are smoothed, and citations and the reference list are complete. |
| **PASS 6 — Tightening & automation** | Concision, and repeatable checks | The prose is tightened, and the checks a person shouldn't do by hand (term drift, repetition, formatting) are automated. This is the draft PHASE 0.9 audits. |
| **PASS 7 — Full systemic arc edit & cohesion** | The book as one arc | One full read for the through-line, callbacks, and cohesion, with the PHASE 0.9 audit decisions applied. The output is the **semi-locked manuscript** the phases take over. |

**Why "semi-locked":** after PASS 7, no phase rewrites the manuscript on its own. It changes only in three ways, each with a backup and a change log:
- edits the author accepts from a proposals file;
- safe reference fixes before design;
- fixes the author approves in the PHASE 2.5 lock audit, made in the DOCX first.

PHASE 2.5 then locks the chapter (`MANUSCRIPT_LOCKED.md`, v1.2.5). After the lock, a change needs a revision note with the author's written approval, and the chapter is re-locked.

You don't need seven passes, or these names. What matters is that the draft reaches a stage you won't rewrite before PHASE 1 starts (see [`v_1_1/PLACEHOLDERS.md`](./v_1_1/PLACEHOLDERS.md) → "PASS 7").

## The eleven phases, plus the workbook track

| Phase | What it does | Ends with |
|---|---|---|
| **0.9 — Book audit** | Audits the whole draft for drift (terms, definitions, acronyms, equations, thresholds, lists, figures, cross-references) **before PASS 7**. Its passes run again per chapter in PHASE 2.5, and at the end it checks the book for conflicts between chapters and for changes since each lock. Report-only; you resolve the canonical decisions | `AUDIT_CLEAR.md`, then `AUDIT_FINAL_CLEAR.md` |
| **1 — Creation** | Generates every chapter artifact from the locked manuscript: review packet, workbook, training materials, reference guides, slide outline, eBook prep, print prep, narration script, RAG packet, and a grounded marketing intake packet | Production checklist |
| **2 — Governance** | Validates everything against the manuscript, fixes what is safely fixable, proposes the rest, and certifies the chapter | `GOVERNANCE_READY.md` |
| **2.5 — Manuscript lock audit** (v1.2.5) | Reads the chapter in full for content problems (definition conflicts, cross-references, term drift, list counts, glossary gaps, acronyms, heading anchors, figures) **before design**. You decide every finding; the approved fixes go into the DOCX, then the MD; the chapter is locked, with its file hashes recorded. Everything after it requires the lock | `MANUSCRIPT_LOCKED.md` |
| **3 — Design + Production** | Design-system-bound HTML for every asset, figure images, exports, the manual eBook and print layouts, and book-level assembly | Hand-off to QA |
| **3W — Workbook track** | Runs from the end of 2 through 3.5.<br>• The workbook manuscript (DOCX canonical, MD replica) must match before Claude Design builds the workbook.<br>• The author produces the eBook PDF (8.5×11) and full-color print PDF (7×10) in InDesign. Uploading them is the cue that the workbook is done.<br>• Layout wording flows back so the PDF, DOCX, and MD match, and every exercise the manuscript mentions is checked.<br>• The book-level workbook is assembled after the final audit.<br>• No Kindle, audiobook, or RAG | `WORKBOOK_MANUSCRIPT_READY.md`, then `WORKBOOK_READY.md` |
| **3.5A / 3.5B — Print build** | Generates the print layout instead of starting InDesign from an empty page.<br>• **3.5B** (v1.2, default) builds the eBook first. It then writes the chapter's and the workbook exercise's 7×10 print IDMLs, which replicate the eBook, on the author's own finished print documents: one-column masters, CMYK TIFFs, and the print template's callouts.<br>• **3.5A** (v1.1.3) writes a styled tagged-text import from the DOCX.<br>• The author opens the result in InDesign, checks it, and exports the print PDF | Chapter + exercise IDMLs in the chapter's `InDesign/` and `Workbook/` folders |
| **3.5 — Design QA** | Reviews the design output against the design system, accessibility, instructional quality, and Kindle readiness | `DESIGN_READY.md` |
| **4 — Final-wording builds** | Syncs the manuscript (MD and DOCX) to the final eBook PDF and spot-checks it, checks the uploaded 7×10 print PDF against the eBook (wording drift and print layout; report-only, closed before 6.5), then builds the Kindle files and, from those, the audiobook per chapter (an XTTS draft as a guide, the final narration recorded by the author), and assembles the book-level Kindle package and audiobook set | Kindle package + audiobook |
| **5 — RAG (Local + Cloud)** | Rebuilds the chapter's canonical chunk set, re-embeds it into the local index (and the cloud index, if enabled, through a governance gateway when you have one), checks parity, writes the system prompt and query profiles | `RAG_READY.md` |
| **6 — Automation** | Activates the n8n and OpenClaw workflows that generate marketing and design drafts from the grounded RAG, plus a nightly refresh that keeps both vector stores in sync when chapters change | Activation report |
| **6.5 — Publication QA** | Validates EPUB, Kindle, print, the workbook, audiobook, metadata, and accessibility | Publishing Ready |
| **7 — Release** | Final verification, the assistant's recommendations, and the author's signature | **Published** |

```
Draft ─▶ 0.9 audit ─▶ Semi-locked manuscript ─▶ 1 ─▶ 2 ─▶ 2.5 lock ─▶ 3 ─▶ 3.5 ─▶ 4 ─▶ 5 ─▶ 6 ─▶ 6.5 ─▶ 7 ─▶ Published
                                                                (0.9 consistency check at 4 Part B)
                                 ▲       │
                                 └───────┘ fix loop
```

PHASE 0.9 is the exception: it audits the whole book at once, first on the draft before PASS 7 and again as a cross-chapter consistency check at PHASE 4 Part B. Its per-chapter passes run in PHASE 2.5. Every other phase runs chapter by chapter, including 6 and 6.5. Four of them add a book-level mode that runs once — PHASE 3 (eBook and print assembly), PHASE 3W (the workbook's eBook and print books, after the final audit), PHASE 4 Part B (the Kindle package and audiobook set), and PHASE 6.5 book mode (publication QA of the assembled files) — each waiting until every chapter has cleared the gate before it. PHASE 2 and PHASE 6 also offer a batch mode for running several chapters in one pass.

## Principles the phases enforce

- **The manuscript is locked before design.** No phase edits it on its own. Suggested changes go into a proposals file or a decisions log that you accept or reject, with a backup, a change log, and a version bump. PHASE 2.5 locks the chapter once you've decided every content finding, and every design and production phase checks the lock. After it, a change needs your written approval and a re-lock; PHASE 4 Part 0 only confirms the final eBook PDF still matches, and asks you about any difference.
- **One source of truth, ranked.** Manuscript → normalized glossary → learning metadata and figure registry → everything derived. Conflicts always resolve downward.
- **One vocabulary for "locked" (v1.3.0).** PASS 7 is *semi-locked*; PHASE 1 and 2 make the chapter *governed*; PHASE 2.5 makes it *research-cleared and locked* (references finished) before any build; PHASE 3 onward works from that *production source*; PHASE 4 Part 0 makes it *final-wording synced*. The eBook upload never creates the lock.
- **Finish the files, then index them.** The author verifies the eBook and print books (chapter and workbook) before Kindle; the audiobook comes last; RAG and automations come only after all of a chapter's files are finished.
- **Gates, not vibes.** Each phase has an entry condition, an exit condition, and a trigger file that says it passed. A phase cannot start because it feels ready.
- **Fix with a paper trail.** The governance phase backs up before editing, logs every change with before-and-after, escalates anything ambiguous to you, and never deletes.
- **AI drafts, the author approves.** Marketing and design automation produce drafts only. Nothing publishes, schedules, or overwrites finished work on its own.
- **A second model checks the first, and you check both (v1.3.0).** Research claims and finished artifacts get an independent read from Microsoft Copilot (Researcher, Chat, Create) through human-in-the-loop handoffs. Its output is evidence, not a verdict: it never edits the manuscript, never certifies, never opens a gate alone, and never replaces preflight, EPUB validation or a human check.
- **Claims are grounded.** Marketing copy is generated from a claims registry and a terminology lock built from the manuscript, with an explicit "do not claim" list, so the local model cannot invent statistics, testimonials, credentials, or outcome promises.
- **Voice is a spec, not a hope.** A voice kit with verbatim sample passages loads before every generation task.

## Repository layout

```
v_1_3_0/                   current release (Microsoft Copilot handoffs: research clearance, image generation, final-artifact reviews; Pass 4; optional sidebars)
  COPILOT_HANDOFFS/             the Copilot standard, prompts, upload lists, and return formats
v_1_2_6/                   previous release (PHASE 4 Step 0C congruency check; gates Part A and PHASE 5/6.5), kept for books mid-flight
v_1_2_5/                   previous release (PHASE 2.5 manuscript lock audit; the lock gates design and production; B0 reduced), kept for books mid-flight
v_1_2_4/                   previous release (workbook eBook numbering and finals; Montserrat questions; numbered badges; figure references), kept for books mid-flight
v_1_2_3/                   previous release (print callouts as separate template frames; roman how-to steps), kept for books mid-flight
v_1_2_2/                   previous release (design systems are the source for every export), kept for books mid-flight
v_1_2_1/                   previous release (print layout rules; automatic PHASE 3 start), kept for books mid-flight
  HOW_TO_RUN_THE_PIPELINE.md    the step-by-step operating guide (start here day to day)
  MASTER_PIPELINE_OVERVIEW.md   the tie-breaker: phases, gates, folders, deliverables, automation map
  PLACEHOLDERS.md               every token to replace, and what to leave alone
  PHASE 0.9 … PHASE 7           the phase prompts, plus PHASE 2.5 (lock audit, v1.2.5), PHASE 3W (workbook), PHASE 3.5A and 3.5B (print builds)
  templates/style_map.example.json   starting point for <PRINT_DSM_ROOT>/style_map.json (PHASE 3.5A)
v_1_2/                     previous release (eBook-first print build: PHASE 3.5B IDMLs), kept for books mid-flight
v_1_1_3/                   previous release (PHASE 3.5A tagged-text print import, polish window,
                           MANUSCRIPT_REVISED.md revision trigger), kept for books mid-flight
v_1_1_2/                   previous release (print vs. eBook QA: PHASE 4 Part 0P, PHASE 3W W2b), kept for books mid-flight
v_1_1/                     previous release (automation first: upload-triggered phases, references check,
                           glossary lock, local PHASE 7), kept for books mid-flight
v_1_0_4/                   previous release (governed cloud track, nightly RAG refresh), kept for books mid-flight
v_1_0_3/                   previous release (PHASE 3W workbook track), kept for books mid-flight
v_1_0_2/                   earlier release (dual local + cloud RAG), kept for books mid-flight
v1_0/                      earlier release, kept for books mid-flight
archived-versions/
  beta_0_9/                previous version, kept intact for books mid-flight
  alpha_0_5/               the original six-phase shape
CHANGELOG.md               what changed in each version, and why
LICENSE                    GPL-3.0
```

Start with **`v_1_3_0/MASTER_PIPELINE_OVERVIEW.md`** for the design, and **`v_1_3_0/HOW_TO_RUN_THE_PIPELINE.md`** for the day-to-day steps. It carries the phase table, the status ladder, the folder map, the deliverable map, and the trigger map, and it is the tie-breaker whenever a phase file and the overview disagree.

## Getting started

1. **Read the overview.** Ten minutes there saves an afternoon later.
2. **Fill in the placeholders.** The phase files ship with tokens like `<BOOK_ROOT>`, `<BOOK>`, and `<AUTHOR>`. [`v_1_3_0/PLACEHOLDERS.md`](./v_1_3_0/PLACEHOLDERS.md) lists every one, with a find-and-replace script for PowerShell and bash, and says which concrete values (print trim, model names, "PASS 7") are examples rather than requirements.
3. **Create the folder skeleton** from the overview's folder map — per chapter and at the book root.
4. **Run PHASE 1 on one chapter.** Paste the phase, give it the locked manuscript, let it generate.
5. **Run PHASE 2 on that same chapter** before generating a second one. It will find naming, metadata, and terminology problems while they are cheap to fix. Then run **PHASE 2.5** and lock the chapter before any design work.
6. **Keep going one chapter at a time** until you trust the output, then batch.

You do not need every phase. A pipeline that stops at PHASE 3.5 still gives you governed, design-consistent chapter assets.

**Print from the eBook (v1.2).** If you lay out print in InDesign, PHASE 3.5B needs three things in your print design folder (`_PrintDSM`):
- the print templates;
- one chapter you have already finished by hand;
- for the workbook, one finished exercise.

Each new chapter and exercise is then generated on those, so it opens looking like the ones you've already laid out. Fonts that load from Adobe Fonts may need re-activating when you open the file. Phases 5 and 6 only matter if you want a local RAG and automated drafting.

## Choosing your path: with AI, with less AI, or without it

The pipeline was built with AI doing much of the drafting, but **the gates are the product, not the AI**. Every phase says what has to exist and what has to be true before a chapter moves on. Whether a person or a model produces that work is your choice, phase by phase. Pick the path that fits your book, your budget, and your comfort, and you can change your mind later.

### Path 1 — AI-assisted (the way it was built)

An AI assistant drafts the derived material, and you review and approve every piece.

1. Fill in the placeholders and set up the folders ([Getting started](#getting-started)).
2. For each chapter, paste the phase file into your assistant (Claude was the reference), attach the locked manuscript, and let it produce the phase's outputs.
3. Read what it produced. Accept, reject, or edit; nothing in the manuscript changes without your say-so.
4. Let the gate decide: the next phase starts only when its trigger file exists (`GOVERNANCE_READY.md`, `DESIGN_READY.md`, and so on).
5. Optionally automate the hand-offs (n8n, a local runner), as described in `HOW_TO_RUN_THE_PIPELINE.md`. Automation only drafts; you still approve.

**Good for:** authors with many chapters, many formats, or a workbook and training materials to keep in sync.

### Path 2 — AI for checking only (you do the writing)

You write and design everything yourself, and use AI or scripts only to **check** your work.

- **You create** the review packet, guides, slide outline, workbook, eBook, print layout, narration script, and marketing copy, using each phase file as your checklist of what to make and where it goes.
- **The checks do the tedious part:** paste a finished chapter's files into PHASE 2 (governance) and ask only for the report. It tells you where a term drifted, a quote no longer matches the manuscript, or a figure number is wrong. Turn off any "fix" step and fix things yourself.
- **The deterministic tools need no AI at all:** the references check, glossary rollup, print-vs-eBook comparison, print checks, and the IDML print builders are plain scripts (see `MASTER_PIPELINE_OVERVIEW.md`, "Deterministic local tools").

**Good for:** authors who want their own hand on every word but don't want to proofread twenty files by eye.

### Path 3 — No AI (a manual production system)

Everything still works as a **checklist and gate system**, run by you (or your editor or team) with ordinary tools.

1. **Use each phase file as a written procedure.** Skip the "paste this into an assistant" lines; read the inputs, outputs, checks, and gate for each phase, and do them by hand.
2. **Keep the same files and folders.** The folder map, file names, and trigger files still tell you, and anyone helping you, exactly where a chapter stands.
3. **Do the governance check as a review.** PHASE 2's checklist (terminology, quotes, figures, metadata) becomes your editor's review sheet.
4. **Leave out what assumes a model:** PHASE 5 (the RAG knowledge base) and PHASE 6 (automated drafting) are optional; mark them N/A in the chapter checklist rather than leaving them blank.
5. **Keep the human sign-off.** PHASE 7's checklist and signature work the same way without AI.

**Good for:** authors, small presses, or publishers whose policies don't allow generative AI, or who simply want a disciplined, repeatable production process.

### Whichever path you choose

- **The manuscript stays the single source of truth.** Nothing else, AI-made or hand-made, overrides it.
- **You approve everything that ships.** The pipeline never publishes on its own.
- **Disclose AI use honestly.** If AI generated text, images, or other content in your book, say so in the front matter, and check each retailer's current rules before you publish. Amazon KDP, for example, asks you to disclose AI-generated content when you publish; content you wrote and only edited or brainstormed with AI tools is treated differently. Keep a record of which tool made what (the FigureRegistry has a "tool used" field for exactly this).
- **Mix freely.** Many authors use AI for checks and figures, and do the writing and layout themselves. Record your choice per phase in the chapter's production checklist so the rest of the pipeline knows what to expect.

## Adopting it for your publishing work

If someone asks you how to use this for their own books, here is the short version to share:

1. **Start with one chapter, not the whole book.** Run it end to end once (or as far as you need) before committing.
2. **Get your manuscript to a stage you won't rewrite.** The pipeline starts after editing; it doesn't replace an editor ([the editing passes](#before-the-phases-the-editing-passes-pass-07) show one way to get there).
3. **Choose your path above** (AI-assisted, AI for checks, or no AI), and write it down.
4. **Replace the placeholders** with your folders, title, and author name using `PLACEHOLDERS.md`; swap in your own terms, design system, and templates.
5. **Keep only the formats you need.** eBook only? Stop at PHASE 3.5 and PHASE 4's Kindle step. No workbook or audiobook? Mark them N/A.
6. **Respect the gates.** The value is in never moving a chapter on until its checks pass, whoever does the work.
7. **Use the latest version folder** (`v_1_3_0/` today) for new books; older folders are kept only so books already in progress can finish on the version they started with.
8. **Mind the license.** The pipeline is GPL-3.0: free to use and adapt, and changes you share keep the same license. Your book's content stays yours.
9. **Share what you learn.** If you adapt it for a different kind of book or toolchain, a pull request helps the next author ([Contributing](#contributing)).

## Adapting it to your book

These prompts are a working author's, not a sanitized template, so expect to change:

- **Paths and names.** `<BOOK_ROOT>`, `<BOOK>`, `<BOOK_TITLE>`, `<AUTHOR>`, and the rest — see `PLACEHOLDERS.md`. "PASS 7" means the seventh editing pass ([see the passes above](#before-the-phases-the-editing-passes-pass-07)); substitute your own final-draft stage. The phases are written in the author's first person ("my book", "I approve every piece"), which reads correctly whoever runs them.
- **The design system.** PHASE 3 expects a design system manual derived from your print layout — tokens, typography, components. Without one, the design phase has nothing authoritative to follow. From v1.2.1 the design packet is built as Claude artifacts from a packet DSM you extract once from a finished chapter (`<PACKET_DSM_ROOT>`), so no separate design tool is required.
- **Framework terminology.** The terminology lock names this book's concepts. Replace them with yours.
- **Tools.** The defaults are Claude and Claude Design for generation, InDesign for print (with the print IDMLs generated from the eBook since v1.2), XTTS for draft narration and Adobe Audition for the final recording, Ollama plus an ONNX/TEI embedder and ChromaDB for local RAG, optionally Azure OpenAI `text-embedding-3-large` with vectors in Azure Blob Storage for multilingual cloud RAG, and n8n plus OpenClaw for orchestration. Each is swappable; the gates and deliverables are what matter.
- **Optional deliverables.** Workbook, training materials, and audiobook are separable. Drop what your book does not have, and say so in the checklist rather than leaving the item silently blank.

## Contributing

Issues and pull requests are welcome, especially from authors who have run this on a different kind of book. If you adapt a phase for another toolchain, a PR adding it as a variant is more useful than a fork nobody finds.

## License

GPL-3.0. See [LICENSE](./LICENSE).

The pipeline is free to use and adapt. The book content it was built for is not part of this repository.
