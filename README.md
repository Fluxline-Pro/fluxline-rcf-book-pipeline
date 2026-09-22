# Fluxline RCF Book Pipeline

A phase-by-phase AI workflow for taking a finished book manuscript all the way to published formats — eBook, print, Kindle, audiobook, training materials, a RAG knowledge base, and grounded marketing — without losing control of the manuscript or the voice.

It is a set of Markdown prompts. You paste a phase into an AI assistant (these were written against Claude, Claude Design, and a local LLM, and read fine in most assistants), it produces that phase's outputs, and a gate decides whether the chapter moves on. Nothing here is code you install.

Built for *RCF: Resonance Core Framework* by Terence Waters at [Fluxline.pro](https://fluxline.pro), and shared for other authors who are building a real production pipeline rather than one-off prompts.

**Current version: [v1.0](./v1_0)** · See the [changelog](./CHANGELOG.md) for what changed and why.

---

## What problem this solves

A book that ships in six formats has the same content living in twenty places: manuscript, workbook, slides, reference guides, narration script, eBook HTML, print layout, Kindle file, vector store, marketing copy. Each one drifts. A term gets redefined in the slides. A figure gets renumbered in print but not in Kindle. A marketing post claims something the book never says.

This pipeline treats the manuscript as the only source of truth and makes every other artifact answer to it — with validation, correction, and a human sign-off at the end.

## The nine phases

| Phase | What it does | Ends with |
|---|---|---|
| **1 — Creation** | Generates every chapter artifact from the locked manuscript: review packet, workbook, training materials, reference guides, slide outline, eBook prep, print prep, narration script, RAG packet, and a grounded marketing intake packet | Production checklist |
| **2 — Governance** | Validates everything against the manuscript, fixes what is safely fixable, proposes the rest, and certifies the chapter | `GOVERNANCE_READY` |
| **3 — Design + Production** | Design-system-bound HTML for every asset, figure images, exports, manual print layout, audiobook render, and book-level assembly | Hand-off to QA |
| **3.5 — Design QA** | Reviews the design output against the design system, accessibility, instructional quality, and Kindle readiness | `DESIGN_READY` |
| **4 — Kindle** | Builds the Kindle files per chapter, then assembles the book-level Kindle package | Kindle package |
| **5 — RAG + Local LLM** | Rebuilds the chapter's ingestion surface, updates the vector store, writes the system prompt and query profiles | `RAG_READY` |
| **6 — Automation** | Activates the n8n and OpenClaw workflows that generate marketing and design drafts from the grounded RAG | Activation report |
| **6.5 — Publication QA** | Validates EPUB, Kindle, print, audiobook, metadata, and accessibility | Publishing Ready |
| **7 — Release** | Final verification, the assistant's recommendations, and the author's signature | **Published** |

```
Locked manuscript ─▶ 1 ─▶ 2 ─▶ 3 ─▶ 3.5 ─▶ 4 ─▶ 5 ─▶ 6 ─▶ 6.5 ─▶ 7 ─▶ Published
                            ▲       │
                            └───────┘ fix loop
```

Phases 1–5 run chapter by chapter. Book-level assembly happens once every chapter has cleared the relevant gate.

## Principles the phases enforce

- **The manuscript is locked.** No phase edits it. Suggested changes go into a proposals file that you accept or reject, and the version increments before governance runs.
- **One source of truth, ranked.** Manuscript → normalized glossary → learning metadata and figure registry → everything derived. Conflicts always resolve downward.
- **Gates, not vibes.** Each phase has an entry condition, an exit condition, and a trigger file that says it passed. A phase cannot start because it feels ready.
- **Fix with a paper trail.** The governance phase backs up before editing, logs every change with before-and-after, escalates anything ambiguous to you, and never deletes.
- **AI drafts, the author approves.** Marketing and design automation produce drafts only. Nothing publishes, schedules, or overwrites finished work on its own.
- **Claims are grounded.** Marketing copy is generated from a claims registry and a terminology lock built from the manuscript, with an explicit "do not claim" list, so the local model cannot invent statistics, testimonials, credentials, or outcome promises.
- **Voice is a spec, not a hope.** A voice kit with verbatim sample passages loads before every generation task.

## Repository layout

```
v1_0/
  MASTER_PIPELINE_OVERVIEW.md   the tie-breaker: phases, gates, folders, deliverables
  PLACEHOLDERS.md               every token to replace, and what to leave alone
  PHASE 1 … PHASE 7             the nine phase prompts
beta_0_9/                  previous version, kept intact for books mid-flight
archived-versions/
  alpha_0_5/               the original six-phase shape
CHANGELOG.md               what changed in each version, and why
LICENSE                    GPL-3.0
```

Start with **`v1_0/MASTER_PIPELINE_OVERVIEW.md`**. It carries the phase table, the status ladder, the folder map, the deliverable map, and the trigger map, and it is the tie-breaker whenever a phase file and the overview disagree.

## Getting started

1. **Read the overview.** Ten minutes there saves an afternoon later.
2. **Fill in the placeholders.** The phase files ship with tokens like `<BOOK_ROOT>`, `<BOOK>`, and `<AUTHOR>`. [`v1_0/PLACEHOLDERS.md`](./v1_0/PLACEHOLDERS.md) lists every one, with a find-and-replace script for PowerShell and bash, and says which concrete values (print trim, model names, "PASS 7") are examples rather than requirements.
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
- **Tools.** The defaults are Claude and Claude Design for generation, InDesign for print, XTTS for narration, Ollama plus ChromaDB for local RAG, and n8n plus OpenClaw for orchestration. Each is swappable; the gates and deliverables are what matter.
- **Optional deliverables.** Workbook, training materials, and audiobook are separable. Drop what your book does not have, and say so in the checklist rather than leaving the item silently blank.

## Contributing

Issues and pull requests are welcome, especially from authors who have run this on a different kind of book. If you adapt a phase for another toolchain, a PR adding it as a variant is more useful than a fork nobody finds.

## License

GPL-3.0. See [LICENSE](./LICENSE).

The pipeline is free to use and adapt. The book content it was built for is not part of this repository.
