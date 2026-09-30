# Fluxline RCF Book Pipeline

A phase-by-phase AI workflow for taking a finished book manuscript all the way to published formats — eBook, print, Kindle, audiobook, training materials, a RAG knowledge base, and grounded marketing — without losing control of the manuscript or the voice.

It is a set of Markdown prompts. You paste a phase into an AI assistant (these were written against Claude, Claude Design, and a local LLM, and read fine in most assistants), it produces that phase's outputs, and a gate decides whether the chapter moves on. Nothing here is code you install.

Built for *RCF: Resonance Core Framework* by Terence Waters at [Fluxline.pro](https://fluxline.pro), and shared for other authors who are building a real production pipeline rather than one-off prompts.

**Current version: [v1.0.4](./v_1_0_4)** (previous: [v1.0.3](./v_1_0_3), [v1.0.2](./v_1_0_2), [v1.0](./v1_0)) · See the [changelog](./CHANGELOG.md) for what changed and why.

---

## What problem this solves

A book that ships in six formats has the same content living in twenty places: manuscript, workbook, slides, reference guides, narration script, eBook HTML, print layout, Kindle file, vector store, marketing copy. Each one drifts. A term gets redefined in the slides. A figure gets renumbered in print but not in Kindle. A marketing post claims something the book never says.

This pipeline treats the manuscript as the only source of truth and makes every other artifact answer to it — with validation, correction, and a human sign-off at the end.

## The ten phases, plus the workbook track

| Phase | What it does | Ends with |
|---|---|---|
| **0.9 — Book audit** | Audits the whole draft for drift (terms, definitions, acronyms, equations, thresholds, lists, figures, cross-references) **before PASS 7**, and again as a final delta once every chapter is synced to its final eBook PDF. Report-only; you resolve the canonical decisions | `AUDIT_CLEAR.md`, then `AUDIT_FINAL_CLEAR.md` |
| **1 — Creation** | Generates every chapter artifact from the locked manuscript: review packet, workbook, training materials, reference guides, slide outline, eBook prep, print prep, narration script, RAG packet, and a grounded marketing intake packet | Production checklist |
| **2 — Governance** | Validates everything against the manuscript, fixes what is safely fixable, proposes the rest, and certifies the chapter | `GOVERNANCE_READY.md` |
| **3 — Design + Production** | Design-system-bound HTML for every asset, figure images, exports, the manual eBook and print layouts, and book-level assembly | Hand-off to QA |
| **3W — Workbook track** | Runs from the end of 2 through 3.5.<br>• The workbook manuscript (DOCX canonical, MD replica) must match before Claude Design builds the workbook.<br>• The author produces the eBook PDF (8.5×11) and full-color print PDF (7×10) in InDesign. Uploading them is the cue that the workbook is done.<br>• Layout wording flows back so the PDF, DOCX, and MD match, and every exercise the manuscript mentions is checked.<br>• The book-level workbook is assembled after the final audit.<br>• No Kindle, audiobook, or RAG | `WORKBOOK_MANUSCRIPT_READY.md`, then `WORKBOOK_READY.md` |
| **3.5 — Design QA** | Reviews the design output against the design system, accessibility, instructional quality, and Kindle readiness | `DESIGN_READY.md` |
| **4 — Final-wording builds** | Syncs the manuscript (MD and DOCX) to the final eBook PDF and spot-checks it, then builds the Kindle files and, from those, the audiobook per chapter (an XTTS draft as a guide, the final narration recorded by the author), and assembles the book-level Kindle package and audiobook set | Kindle package + audiobook |
| **5 — RAG (Local + Cloud)** | Rebuilds the chapter's canonical chunk set, re-embeds it into the local index (and the cloud index, if enabled, through a governance gateway when you have one), checks parity, writes the system prompt and query profiles | `RAG_READY.md` |
| **6 — Automation** | Activates the n8n and OpenClaw workflows that generate marketing and design drafts from the grounded RAG, plus a nightly refresh that keeps both vector stores in sync when chapters change | Activation report |
| **6.5 — Publication QA** | Validates EPUB, Kindle, print, the workbook, audiobook, metadata, and accessibility | Publishing Ready |
| **7 — Release** | Final verification, the assistant's recommendations, and the author's signature | **Published** |

```
Draft ─▶ 0.9 audit ─▶ Locked manuscript ─▶ 1 ─▶ 2 ─▶ 3 ─▶ 3.5 ─▶ 4 ─▶ 5 ─▶ 6 ─▶ 6.5 ─▶ 7 ─▶ Published
                                                                (0.9 final delta at 4 Part B)
                            ▲       │
                            └───────┘ fix loop
```

PHASE 0.9 is the exception: it audits the whole book at once, first on the draft before PASS 7 and again as a final delta at PHASE 4 Part B. Every other phase runs chapter by chapter, including 6 and 6.5. Four of them add a book-level mode that runs once — PHASE 3 (eBook and print assembly), PHASE 3W (the workbook's eBook and print books, after the final audit), PHASE 4 Part B (the Kindle package and audiobook set), and PHASE 6.5 book mode (publication QA of the assembled files) — each waiting until every chapter has cleared the gate before it. PHASE 2 and PHASE 6 also offer a batch mode for running several chapters in one pass.

## Principles the phases enforce

- **The manuscript is locked.** No phase edits it. Suggested changes go into a proposals file that you accept or reject, and the version increments before governance runs. The one exception is PHASE 4 Part 0: wording you changed while laying out the eBook is copied back from the final eBook PDF, with a backup, a change log, a version bump, and anything uncertain left for you to decide. Without that PDF, PHASE 4 does not start.
- **One source of truth, ranked.** Manuscript → normalized glossary → learning metadata and figure registry → everything derived. Conflicts always resolve downward.
- **Gates, not vibes.** Each phase has an entry condition, an exit condition, and a trigger file that says it passed. A phase cannot start because it feels ready.
- **Fix with a paper trail.** The governance phase backs up before editing, logs every change with before-and-after, escalates anything ambiguous to you, and never deletes.
- **AI drafts, the author approves.** Marketing and design automation produce drafts only. Nothing publishes, schedules, or overwrites finished work on its own.
- **Claims are grounded.** Marketing copy is generated from a claims registry and a terminology lock built from the manuscript, with an explicit "do not claim" list, so the local model cannot invent statistics, testimonials, credentials, or outcome promises.
- **Voice is a spec, not a hope.** A voice kit with verbatim sample passages loads before every generation task.

## Repository layout

```
v_1_0_4/                   current release (governed cloud track, nightly RAG refresh)
  MASTER_PIPELINE_OVERVIEW.md   the tie-breaker: phases, gates, folders, deliverables
  PLACEHOLDERS.md               every token to replace, and what to leave alone
  PHASE 0.9 … PHASE 7           the ten phase prompts, plus PHASE 3W (workbook)
v_1_0_3/                   previous release (PHASE 3W workbook track), kept for books mid-flight
v_1_0_2/                   earlier release (dual local + cloud RAG), kept for books mid-flight
v1_0/                      earlier release, kept for books mid-flight
archived-versions/
  beta_0_9/                previous version, kept intact for books mid-flight
  alpha_0_5/               the original six-phase shape
CHANGELOG.md               what changed in each version, and why
LICENSE                    GPL-3.0
```

Start with **`v_1_0_4/MASTER_PIPELINE_OVERVIEW.md`**. It carries the phase table, the status ladder, the folder map, the deliverable map, and the trigger map, and it is the tie-breaker whenever a phase file and the overview disagree.

## Getting started

1. **Read the overview.** Ten minutes there saves an afternoon later.
2. **Fill in the placeholders.** The phase files ship with tokens like `<BOOK_ROOT>`, `<BOOK>`, and `<AUTHOR>`. [`v_1_0_4/PLACEHOLDERS.md`](./v_1_0_4/PLACEHOLDERS.md) lists every one, with a find-and-replace script for PowerShell and bash, and says which concrete values (print trim, model names, "PASS 7") are examples rather than requirements.
3. **Create the folder skeleton** from the overview's folder map — per chapter and at the book root.
4. **Run PHASE 1 on one chapter.** Paste the phase, give it the locked manuscript, let it generate.
5. **Run PHASE 2 on that same chapter** before generating a second one. It will find naming, metadata, and terminology problems while they are cheap to fix.
6. **Keep going one chapter at a time** until you trust the output, then batch.

You do not need every phase. A pipeline that stops at PHASE 3.5 still gives you governed, design-consistent chapter assets. Phases 5 and 6 only matter if you want a local RAG and automated drafting.

## Adapting it to your book

These prompts are a working author's, not a sanitized template, so expect to change:

- **Paths and names.** `<BOOK_ROOT>`, `<BOOK>`, `<BOOK_TITLE>`, `<AUTHOR>`, and the rest — see `PLACEHOLDERS.md`. "PASS 7" means the seventh editing pass in the pipeline this came from; substitute your own final-draft stage. The phases are written in the author's first person ("my book", "I approve every piece"), which reads correctly whoever runs them.
- **The design system.** PHASE 3 expects a design system manual derived from your print layout — tokens, typography, components. Without one, the design phase has nothing authoritative to follow.
- **Framework terminology.** The terminology lock names this book's concepts. Replace them with yours.
- **Tools.** The defaults are Claude and Claude Design for generation, InDesign for print, XTTS for draft narration and Adobe Audition for the final recording, Ollama plus an ONNX/TEI embedder and ChromaDB for local RAG, optionally Azure OpenAI `text-embedding-3-large` with vectors in Azure Blob Storage for multilingual cloud RAG, and n8n plus OpenClaw for orchestration. Each is swappable; the gates and deliverables are what matter.
- **Optional deliverables.** Workbook, training materials, and audiobook are separable. Drop what your book does not have, and say so in the checklist rather than leaving the item silently blank.

## Contributing

Issues and pull requests are welcome, especially from authors who have run this on a different kind of book. If you adapt a phase for another toolchain, a PR adding it as a variant is more useful than a fork nobody finds.

## License

GPL-3.0. See [LICENSE](./LICENSE).

The pipeline is free to use and adapt. The book content it was built for is not part of this repository.
