# PHASE 0.9: Book-Wide Manuscript Audit (v1)

> **Pipeline position:** PHASE 0.9 (Consistency), between the tightening pass (PASS 6) and <AUTHOR>'s voice pass (PASS 7) · **Upstream gate:** PASS 6 is complete for **every** chapter in `<DRAFT_SOURCE>` · **Downstream:** PASS 7 → PHASE 1. Spot-checks each chapter again after its PHASE 4 Part 0 sync, and runs a **final delta audit** at the start of PHASE 4 Part B.
> **Canonical paths, status ladder, triggers, and deliverables:** see `MASTER_PIPELINE_OVERVIEW.md`.

**v1 (2026-09-27):** new phase. Every other phase checks one chapter at a time; PHASE 2 carries the glossary forward, but only against chapters already processed. Nothing checked the **whole book** for drift. That matters most in the RAG layer: the local and cloud vector stores (and any product built on them) inherit every inconsistency, and two chapters that disagree become one contradictory answer.

---

**Purpose:**
Find every place where the book disagrees with itself — terms, definitions, acronyms, equations, thresholds, lists, figures, cross-references, and citation-unfriendly headings — and hand <AUTHOR> one list of decisions to make. This phase is **report-only**: it never edits the manuscript.

## Where it sits in the manuscript passes

- **PASS 6: tightening.** Word counts come down and redundancy goes. Wording changes a lot here, so audit **after** PASS 6 is finished for every chapter, not during it.
- **PHASE 0.9, Mode F.** The book-wide audit, run on the tightened draft.
- **PASS 7: voice.** <AUTHOR> reads each chapter in full and edits it for voice, resolving the audit findings along the way. After PASS 7, the chapter is pseudo-locked: from then on, wording changes only through PHASE 1 Editorial Suggestions or the layout sync in PHASE 4 Part 0.
- **PHASES 1–3.** Production, governance, and design work from the PASS 7 text.
- **eBook and print InDesign books.** Built before PHASE 4. <AUTHOR> may refine wording in either one, and PHASE 4 Part 0 copies the final eBook wording back into the manuscript. Mode P checks each chapter at that point, and Mode D checks the whole book before the book-level builds.
- **Audiobook and the remaining phases.** They run from the final, synced wording.

## When it runs

| Mode | When | Chapters | Passes | Exit trigger |
|---|---|---|---|---|
| **F — Full** | Once, on the complete draft (PASS 6 or whichever pass is current), **before PASS 7** | all | 1 → 2 → 3 per chapter, then Consolidation | `AUDIT_CLEAR.md` |
| **P — Spot check** | (a) During PASS 7, whenever an edit touches a canonical term, equation, threshold, or named list · (b) **after every PHASE 4 Part 0 sync** that changes wording (Part 0 step 0.7), before the chapter's audiobook render and RAG rebuild | the one chapter | (a) 2 only · (b) 1 → 2 on the synced text, updating the ledger | (a) none; findings join the next Consolidation · (b) the result is recorded in the sync report; no open blocking finding allowed |
| **D — Final delta** | PHASE 4 Part B, step B0: every chapter has `MANUSCRIPT_SYNCED.md` | only chapters whose text changed **after** their last Mode P check (usually none, since each Part 0 sync already ran one) | 1 → 2 (→ 3 if anchors moved) for those chapters, then Consolidation over the whole book (catches conflicts *between* chapters synced at different times) | `AUDIT_FINAL_CLEAR.md` |

Why this order: before PASS 7, a fix is one edit in one draft file, and PASS 7 is where <AUTHOR> is already reading every line. After PHASE 1, the same fix touches every derived artifact, the design packet, and both vector stores. The Part 0 spot check exists because <AUTHOR> refines wording during InDesign layout, and that wording is what the eBook, Kindle build, audiobook, and RAG actually ship. Catching drift then, chapter by chapter, means a problem is fixed before its audio is rendered, and the final delta has little left to find.

## Inputs

- Mode F / P: the draft manuscripts in `<DRAFT_SOURCE>` (one file per chapter)
- Mode P (b) and Mode D: the synced manuscripts, `<CH_ROOT>/Manuscript/<ChapterName>_Manuscript.md`, and each chapter's `ManuscriptSync_*.md` reports (Mode D uses them to find chapters changed after their last spot check)
- The book glossary (export to plain text if it is a DOCX)
- `<BOOK_ROOT>/_BookGovernance/Audit/Audit_Config.json` (below)
- Mode D also reads the previous run's `ledger.json` and `Audit_CanonicalTerms.json`

## Book-level config (create once)

`<BOOK_ROOT>/_BookGovernance/Audit/Audit_Config.json`

```json
{
  "bookTitle": "<BOOK_TITLE>",
  "edition": "<EDITION>",
  "voiceNote": "The author writes in a deliberate voice; stylistic choices, metaphor, and capitalized framework terms are intentional.",
  "canonicalTerms": ["Framework Term One", "FTO"],
  "knownCorrections": [
    { "wrong": "Old Stage Name", "canonical": "Correct Stage Name", "scope": "where it applies, e.g. the name of stage 6 of the model" }
  ],
  "glossaryPath": "<BOOK_ROOT>/_BookGovernance/<BOOK>_Glossary.txt",
  "glossaryStatus": "current",
  "pass3": { "enabled": true, "answerable": 10, "notInBook": 3, "personalAdvice": 2 },
  "maxQuoteWords": 25
}
```

- The values above are examples; replace them with your book's terms. `canonicalTerms` starts as a seed list and grows from the glossary and every resolved canonical decision.
- `glossaryStatus: "stale"` (set it when the manuscript is ahead of the glossary): glossary conflicts become `needs_author_review` findings and never `blocking` ones, because the manuscript outranks a stale glossary.

## Folder layout and deliverables

```
<BOOK_ROOT>/_BookGovernance/Audit/
├── Audit_Config.json
├── Audit_CanonicalTerms.json                 current author-resolved canonical list (seeds PHASE 1 + PHASE 2)
├── EvalSet/<EDITION>/<ChapterName>_EvalSet.jsonl   current evaluation set (Pass 3), versioned by edition
├── <RUN_ID>/                                 e.g. 20260927_F, 20261101_D
│   ├── ledger.json
│   ├── pass1/<ChapterName>_Pass1.json
│   ├── pass2/<ChapterName>_Pass2.json
│   ├── pass3/<ChapterName>_EvalSet.jsonl
│   ├── <BOOK>_AuditReport.md                 Consolidation output
│   └── <BOOK>_CanonicalDecisions.md          the decisions list, with <AUTHOR>'s choice recorded per item
└── Trigger/
    ├── AUDIT_CLEAR.md | AUDIT_INCOMPLETE.md          (Mode F)
    └── AUDIT_FINAL_CLEAR.md | AUDIT_FINAL_INCOMPLETE.md   (Mode D)
```

---

# How to run

1. Split the manuscript into chapters. If a chapter exceeds the model's context, split it at H2 headings and carry the ledger between parts. This works on a local LLM or on Claude; no single call needs the whole book.
2. Start `ledger.json` as `{"terms": [], "equations": [], "thresholds": [], "lists": [], "figures": [], "crossrefs": []}` (Mode D starts from the previous run's ledger and replaces the changed chapters' entries).
3. For each chapter in reading order: Pass 1 → merge into the ledger, keeping every location → Pass 2 → Pass 3 (if enabled).
4. After the last chapter, run the Consolidation pass over all Pass 2 files and the glossary.
5. <AUTHOR> resolves the decisions list (see *After the audit*).

Fill the `{{...}}` tokens from `Audit_Config.json` before each call.

## Shared system prompt (every pass)

```
You are auditing the manuscript of "{{BOOK_TITLE}}, {{EDITION}}" for internal consistency before
publication. You are an auditor, not an editor.

Rules:
- Report only what the text supports. Never invent content, definitions, or page facts.
- Flag; never rewrite. Suggested fixes are one line and marked as suggestions.
- {{VOICE_NOTE}} Do not flag voice or style.
- Quote at most {{MAX_QUOTE_WORDS}} words from the manuscript per finding. Always give a location
  (chapter, section heading, and paragraph or figure number if present).
- When unsure, set "confidence": "low" and "needs_author_review": true rather than guessing.
- Output only the requested JSON. No commentary before or after it.

Canonical framework terms (spelling and capitalization as the book should use them):
{{CANONICAL_TERMS}}

Known terminology corrections to enforce:
{{KNOWN_CORRECTIONS}}
```

## Pass 1 — Extract (per chapter)

```
Chapter: {{CHAPTER_NUMBER}} — {{CHAPTER_TITLE}}

Extract every item below from this chapter. Do not judge anything yet.

Return JSON:
{
  "chapter": "{{CHAPTER_NUMBER}}",
  "headings": [{"level": 2, "text": "...", "location": "..."}],
  "terms": [{"term": "...", "form_used": "...", "defined_here": true|false,
             "definition": "<=25 words or null", "location": "..."}],
  "acronyms": [{"acronym": "...", "expansion_given": "... or null", "location": "..."}],
  "equations": [{"name": "...", "expression": "...", "variables": {"X": "meaning"},
                 "location": "..."}],
  "thresholds": [{"measure": "...", "bands_or_values": "...", "location": "..."}],
  "lists": [{"name": "...", "stated_count": 5 or null, "items": ["..."], "location": "..."}],
  "figures": [{"id": "...", "caption": "...", "referenced_in_text": true|false,
               "location": "..."}],
  "crossrefs": [{"text": "see Chapter 7", "target": "...", "location": "..."}]
}

CHAPTER TEXT:
{{CHAPTER_TEXT}}
```

Save to `pass1/<ChapterName>_Pass1.json` and merge into `ledger.json`.

## Pass 2 — Detect (per chapter)

```
Chapter: {{CHAPTER_NUMBER}} — {{CHAPTER_TITLE}}

Compare this chapter's extraction against the ledger from the other chapters and the glossary.
Report discrepancies in these categories only:

- TERM_DRIFT: a framework term spelled, capitalized, or worded differently from canonical.
- DEFINITION_CONFLICT: a term defined differently here than elsewhere or in the glossary.
- GLOSSARY_GAP: a framework term defined in the text but missing from the glossary, or vice versa.
- ACRONYM: an acronym used before expansion, expanded two different ways, or never expanded.
- EQUATION: the same formula written differently, variables renamed, or a variable undefined.
- THRESHOLD: score bands or numeric cut-offs that disagree across chapters.
- LIST_COUNT: a stated count ("five steps") that doesn't match the items, or a named list
  whose items differ from another chapter.
- FIGURE: a figure referenced but missing, present but never referenced, or a caption that
  contradicts the text.
- CROSS_REF: a "see Chapter / Section / Figure" pointing to something that doesn't exist or
  doesn't contain what is claimed.
- HEADING_ANCHOR: headings that are duplicated, skipped levels, or too vague to serve as a
  citation anchor ("Overview" appearing in many chapters).
- KNOWN_CORRECTION: an instance of a term on the known-corrections list.

Severity:
- "blocking": a reader or a question-answering system would get a wrong or contradictory answer.
- "major": confusing or inconsistent, but the meaning survives.
- "minor": cosmetic consistency.
{{GLOSSARY_STALE_RULE}}

Return JSON:
{
  "chapter": "{{CHAPTER_NUMBER}}",
  "findings": [
    {"id": "{{CHAPTER_NUMBER}}-001", "category": "...", "severity": "...",
     "location": "...", "excerpt": "<=25 words",
     "conflicts_with": {"location": "...", "excerpt": "<=25 words"} or null,
     "issue": "one sentence",
     "suggestion": "one line, marked as a suggestion",
     "confidence": "high|medium|low", "needs_author_review": true|false}
  ]
}

GLOSSARY:
{{GLOSSARY_TEXT}}

LEDGER (other chapters):
{{LEDGER_JSON}}

THIS CHAPTER'S EXTRACTION:
{{PASS1_JSON}}

CHAPTER TEXT:
{{CHAPTER_TEXT}}
```

`{{GLOSSARY_STALE_RULE}}` is empty when `glossaryStatus` is `current`. When it is `stale`, use: *"The glossary is known to be out of date. A conflict with the glossary alone is never 'blocking'; mark it needs_author_review."*

Save to `pass2/<ChapterName>_Pass2.json`.

## Pass 3 — Evaluation questions (per chapter, if `pass3.enabled`)

These questions seed the quality checks for anything that answers from the book: PHASE 5 retrieval checks, and any downstream question-answering product built on the RAG stores. They are written from the book, never from readers.

```
Chapter: {{CHAPTER_NUMBER}} — {{CHAPTER_TITLE}}

Write evaluation items for a question-answering system that must answer only from this book.

Return JSON Lines, one object per line:
- {{N_ANSWERABLE}} "answerable" items: a question a reader might ask, answered in this chapter.
  {"type": "answerable", "question": "...", "expected_anchor": "chapter + section heading",
   "key_points": ["...", "..."]}
- {{N_NOT_IN_BOOK}} "not_in_book" items: plausible adjacent questions this book does not answer.
  {"type": "not_in_book", "question": "...", "why_not_covered": "..."}
- {{N_PERSONAL_ADVICE}} "personal_advice" items: questions asking what the reader should do in
  their own life about a topic this chapter covers (the system must explain the book and add a
  referral, not advise).
  {"type": "personal_advice", "question": "...", "topic_anchor": "..."}

Do not write crisis or self-harm phrasings; those come only from a clinician-reviewed list
maintained by the product that uses this set.

CHAPTER TEXT:
{{CHAPTER_TEXT}}
```

Save to `pass3/<ChapterName>_EvalSet.jsonl`. When the run's gate passes, copy it to `EvalSet/<EDITION>/`.

## Consolidation pass (once per run)

```
You have every chapter's Pass 2 findings and the glossary.

1. Merge duplicates (the same conflict reported from both sides).
2. Group by category, then by severity.
3. Produce a "canonical decisions needed" list: every term, equation, threshold, or list where
   the author must choose one version. For each, show the competing versions with locations.
4. Produce a glossary delta: terms to add, terms whose glossary definition disagrees with the
   text, and terms in the glossary never used in the text.

Return Markdown with these sections:
## Summary (counts by category and severity)
## Blocking findings
## Canonical decisions needed
## Glossary delta
## Major findings
## Minor findings (table)

FINDINGS:
{{ALL_PASS2_JSON}}

GLOSSARY:
{{GLOSSARY_TEXT}}
```

Save as `<BOOK>_AuditReport.md`, and copy the *Canonical decisions needed* section into `<BOOK>_CanonicalDecisions.md` with an empty **Decision** line under each item.

---

# After the audit

1. **<AUTHOR> resolves the canonical decisions first.** Each chosen version goes into `Audit_CanonicalTerms.json` (term, canonical form, canonical definition or expression, source location) and into `Audit_Config.json` → `canonicalTerms` / `knownCorrections` for the next run.
2. **Fix the manuscript.**
   - Mode F / P: <AUTHOR> edits the draft (this is what PASS 7 is for).
   - Mode P (b) and Mode D: a blocking wording fix goes into the eBook InDesign book (and the print book, if it carries the same text) → re-export the eBook PDF → PHASE 4 Part 0 re-sync → Part A / Part C → PHASE 5 re-run for that chapter (the existing re-sync rule). Never patch the synced manuscript by hand.
3. **Update the glossary** from the glossary delta.
4. **Re-run Pass 2 on the changed chapters only**, then Consolidation, until the gate passes.

`Audit_CanonicalTerms.json` is the canonical terminology authority from here on. PHASE 1 seeds each chapter's TerminologyLock from it, and PHASE 2 normalizes glossaries against it.

## PHASE 0.9 exit gates

**Mode F → `Trigger/AUDIT_CLEAR.md`** when:
- [ ] every chapter has Pass 1 and Pass 2 files (and Pass 3, if enabled)
- [ ] no **blocking** finding is open (each is fixed in the draft, or <AUTHOR> accepted it with a note)
- [ ] every canonical decision has a recorded Decision and is in `Audit_CanonicalTerms.json`
- [ ] the trigger lists the run ID, counts by severity, and the open major/minor findings carried into PASS 7

Otherwise write `AUDIT_INCOMPLETE.md` listing what is open. PHASE 1 does not start without `AUDIT_CLEAR.md`.

**Mode D → `Trigger/AUDIT_FINAL_CLEAR.md`** when the same conditions hold for the synced manuscripts, and every canonical term in the final text matches `Audit_CanonicalTerms.json`. Otherwise write `AUDIT_FINAL_INCOMPLETE.md`. PHASE 4 Part B, PHASE 6.5 book mode, and the release-ready flag on the cloud RAG store all wait for `AUDIT_FINAL_CLEAR.md`.

Rename any older trigger to `*_superseded_<timestamp>.md`.
