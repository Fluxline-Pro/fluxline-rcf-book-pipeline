# Copilot Handoff Standard (v1.3.0)

Every Microsoft Copilot step in the pipeline follows this contract. The per-step prompt files in this folder add only what is specific to that step.

## What a handoff is

**The handoff contract is authoritative. Persistent agent instructions reduce repetition but are not required for correctness.** A dedicated Copilot agent or saved custom instructions (`COPILOT_AGENT_INSTRUCTIONS.md`) are optional: every handoff file is complete enough to run in a plain Copilot conversation. Researcher is always a separately started specialist session.

A handoff is a **human-in-the-loop** step. The pipeline prepares a list of files and a prompt; `<AUTHOR>` opens Microsoft Copilot (the personal Microsoft 365 Premium account), uploads the named files, pastes the prompt, and saves what comes back to the named location. Nothing in this pipeline (Claude, the runner, n8n, Microsoft Graph, or any script) calls, drives, or has access to `<AUTHOR>`'s personal Copilot. If a phase file ever appears to say otherwise, this standard wins.

Copilot is an **independent reviewer and artifact producer, not a source of truth.** Its output is evidence and drafts. Nothing it produces becomes canonical until `<AUTHOR>` accepts it and it enters the pipeline through the normal governed path (the decisions log, `MANUSCRIPT_REVISED.md`, the figure registry, or a phase gate).

## Source-of-truth order (all handoffs)

1. Canonical manuscript (DOCX; the MD is its replica)
2. Normalized glossary / terminology lock
3. Approved metadata and registries (figure registry, claims registry, reference list)
4. Derived artifacts (eBook, print, Kindle, workbook, audiobook script)
5. Publication builds (PDF, EPUB, DOCX exports)

When two sources disagree, the higher one wins. Copilot's own knowledge ranks below all of them.

## The twelve parts of every handoff

Parts A to D, F to I, K and L are written inside the prompt block that the author pastes. Part E (the upload manifest) and part J (return-to-pipeline) sit in the handoff file around the block, and the prompt also lists the files it expects ("list the files you can see"). Every prompt block has a FILES line and a LIMITATIONS line.

| | Part | Content |
|---|---|---|
| A | **Role** | What Copilot is asked to do |
| B | **Authority** | What it may inspect, recommend, or generate |
| C | **Prohibitions** | What it must not change, infer, invent, certify, or publish |
| D | **Source-of-truth order** | The precedence above, restated for this step |
| E | **File upload manifest** | Exact required and optional files, in a table |
| F | **Task** | Step-by-step |
| G | **Output schema** | Exact headings, tables, status labels, artifact name |
| H | **Gate effect** | How the output changes the pipeline |
| I | **Limitations** | What still needs deterministic tools or a human |
| J | **Return-to-pipeline** | Where `<AUTHOR>` saves the output, and which phase reads it |
| K | **Privacy / source check** | Nothing secret in the uploads |
| L | **Human approval** | Nothing is canonical without `<AUTHOR>`'s acceptance |

## Common rules (copied into every prompt as parts C, K and L)

**C. Prohibitions.** Do not edit, rewrite, or "correct" the canonical manuscript. Do not invent sources, page numbers, DOIs, quotes, figures, labels, or constructs of the author's framework. Do not certify that anything is production-ready, print-ready, accessible, or publication-ready. Do not publish or share anything. If you cannot verify something, say `CANNOT VERIFY`; do not guess.

**K. Privacy / source check.** Before uploading, confirm the files contain no secrets, credentials, API keys, private keys, signing files, tokens, bank or tax data, customer lists, or unrelated personal or business data. Upload only the files in the manifest. Manuscripts you have not published are your own unreleased work: uploading them to your own Copilot account is your decision, and you should know that your Microsoft account's data and privacy settings apply.

**L. Human approval.** Every finding is a recommendation. `<AUTHOR>` accepts, changes, or rejects each one. A finding that changes the manuscript goes through PHASE 2.5 (before the lock) or `MANUSCRIPT_REVISED.md` (after it).

## Status labels

**Evidence labels (research and claims):** `VERIFIED` · `PARTIALLY SUPPORTED` · `UNSUPPORTED` · `OVERSTATED` · `NEEDS CITATION` · `CANNOT VERIFY` · `AUTHOR DECISION REQUIRED`

**Gate outcomes (QA reviews):** `PASS` · `CONDITIONAL PASS` · `FAIL` · `AUTHOR DECISION REQUIRED`

- `PASS`: no blocking findings; limitations stated.
- `CONDITIONAL PASS`: only non-blocking findings remain, each listed with an owner. `<AUTHOR>` must accept them in writing.
- `FAIL`: at least one blocking finding is open.
- A Copilot `PASS` is **never** a certification. It means "this reviewer found nothing blocking in what it could inspect". `<AUTHOR>` signs off separately.

## What Copilot reviews and what it does not

Copilot reviews: externally verifiable empirical, historical, medical, psychological, technical, legal, quantitative, or academic claims; visible content parity; visible layout and reading experience.

Copilot does **not** review, and must not rewrite: personal narrative, lived experience, metaphor, framework definitions, or the author's interpretation, merely because they lack an outside citation. It classifies such passages (`NARRATIVE`, `FRAMEWORK`, `METAPHOR`, `INTERPRETATION`, `EXERCISE`) and moves on.

Deterministic tools keep their jobs: `references_check.py`, `docx_md_sync.py`, `congruency_check.py`, PDF preflight, embedded-font and colour-space inspection, bleed and trim checks, EPUB validation, Kindle Previewer, device previews, physical proofs. A Copilot report never replaces them.

## Platform notes (checked against Microsoft's documentation, October 2026; re-check, they change)

- **Uploads:** up to 20 files per conversation, 50 MB each. Documented types include PDF, DOCX, XLSX, PPTX, MD, TXT, JSON, CSV, and PNG/JPEG. **EPUB and IDML are not documented as accepted**; give Copilot a PDF or DOCX of the same content instead. If a long PDF is truncated or only partly read, split it by chapter and say so in the report.
- **Researcher:** documented for Microsoft 365 Premium. The consumer "Deep Research" mode was retired on 2026-08-18, so these prompts say *Researcher*. Whether Researcher reads files you upload on a personal plan is not documented: on the first run, ask Copilot to list the files it can see, and if it cannot see them, paste the claim list into the prompt instead. Researcher is included with Microsoft 365 Premium with extensive usage. Microsoft does not currently publish a fixed Researcher query count for Premium. Feature limits may vary by feature, entry point, system conditions, and service changes. Copilot provides in-product notifications when applicable limits are approached or reached. Batching a chapter's claims into one efficient Researcher run is a design preference of this pipeline, not a response to a published quota.

**If Researcher is unavailable or a limit is reached (backup path).** Retain the waiver route, and the author may use Claude as a backup: (1) wait and retry later; or (2) have Claude run the same two-stage verification (an independent claim inventory from the chapter alone first, then the ScienceClaims and Deep Researcher evidence, with web search, every source opened and checked) and record it as `research: waived — Researcher unavailable or limit reached (<date>); Claude backup run <file> (<initials> <date>)` in `Copilot_Waivers.md`. A Claude backup is **less independent** than Copilot (the same model family as Pass 4), and `RESEARCH_CLEAR.md` records it as a backup, never as a Copilot review. It does not change any rule about High claims, which still never close on an AI verdict alone.
- **Images:** the Create tool offers three sizes: 1024×1024, 1024×1536, 1536×1024 pixels. Resolution beyond that is not documented. Treat every generated image as an **RGB concept**, not a print-ready file (a 7×10 in page at 300 ppi needs 2100×3000 px). Record the resolution status in the figure registry and finish or upscale in Photoshop/Illustrator.
- Copilot may change names, limits and modes. When a handoff cannot be followed as written, record what you did in the return file's "Deviations" section.

## Return-file front matter (every Copilot output)

Every file saved back into the pipeline starts with:

```
handoff: <handoff file name and version>
chapter: <ChapterName or "book">
manuscriptSha256: <hash of the manuscript file reviewed; see the table below>
reviewDate: <YYYY-MM-DD>
copilotMode: <Researcher | Chat | Create | other>
filesUploaded: <list, with each file's modified date>
deviations: <none | what differed from the handoff>
```

Claude checks this block before using a report. A report that lists files other than the manifest, or whose hash is not the one expected for its step, is rejected. Which hash goes in the block:

| Step | `manuscriptSha256` is | Where to read it |
|---|---|---|
| Research review (PHASE 2.5) | The DOCX uploaded (before any fixes), `reviewedSha256` | `Governance/Research/Copilot_Research_Handoff.md` |
| Design, final eBook, print, Kindle, publication reviews | The DOCX hash in `MANUSCRIPT_SYNCED.md` if it exists (PHASE 4 Part 0 has run), otherwise in `MANUSCRIPT_LOCKED.md` | `Manuscript/Trigger/` |
| Book-level review (`chapter: book`) | One line per chapter: `<ChapterName>: <hash>` | each chapter's trigger file |
| Image generation | `n/a` | |

"Stale" is decided by each gate's own invalidation rule, not by a hash difference alone: the research report stays valid after softening-only fixes, and the final eBook review stays valid after Part 0 applies the very PDF wording it reviewed.

## Waivers

A required Copilot step may be waived by the author, with a reason. One file holds them: `<CH_ROOT>/Governance/Copilot/Copilot_Waivers.md` (book-level steps: `<BOOK_ROOT>/_BookGovernance/Copilot/Copilot_Waivers.md`), one line per waiver:

`<step>: waived — <reason> (<initials> <date>)`

| Step key | Phase | Required for |
|---|---|---|
| `research` | PHASE 2.5 | chapters with `copilotRequired: yes` in their lock |
| `final-ebook` | PHASE 4 Step 0F | chapters with `copilotRequired: yes` in their lock |
| `publication-qa` | PHASE 6.5 §9b | chapters with `copilotRequired: yes` in their lock |

The optional steps (design, print, Kindle, image generation) need no waiver. Claude copies each waiver into the report that would have used the Copilot output and into the PHASE 7 checklist. A waiver written by anyone but the author, or without a reason, is ignored.

## Version

Handoff prompt files carry their own version in the first line. A prompt change is recorded in the CHANGELOG. The figure registry and the research report record the prompt version used.
