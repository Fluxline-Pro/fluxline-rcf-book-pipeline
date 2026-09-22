# PHASE 5: RAG Rebuild & Local LLM Setup (Per Chapter) (v3)

> **Pipeline position:** PHASE 5 of 7 (Knowledge) · **Upstream gate:** PHASE 4 checklist `gateStatus: PASS` · **Downstream:** PHASE 6 Automation Activation
> **Canonical paths, status ladder, triggers, and deliverables:** see `MASTER_PIPELINE_OVERVIEW.md`.

**v3 changes (2026-09-22 pipeline alignment):**
- Paths moved to `<CH_ROOT>` = `<BOOK_ROOT>/Chapters/<ChapterName>/Final/`.
- Chunk rule aligned with PHASE 1 and PHASE 2 (500–1000 words, 100-word overlap, 80–120 tolerated).
- ChromaDB rebuild scoped by `chapterName` metadata so one chapter's vectors are replaced without touching others.
- Checklist moved next to the other phase checklists; adds the `RAG_READY.md` trigger PHASE 6 needs.
- Local LLM "system prompt" steps now write files only. Model installation and server checks are recorded, not assumed.

---

**Purpose:**
Rebuild the chapter's RAG ingestion surface from the *final, locked* PHASE 1–4 outputs, then prepare the local LLM environment (Ollama / LM Studio) to use it for grounded generation, marketing automation, and the n8n workflows activated in PHASE 6.

Run **per chapter**, after PHASE 4.

## Deliverables (PHASE 5)

| Deliverable | Path |
|---|---|
| RAG_INGESTION | `<CH_ROOT>/RAG/<ChapterName>_RAG_Ingestion.json` + `<CH_ROOT>/RAG/Chunks/<ChapterName>_RAG_Chunks.jsonl` |
| RAG_ValidationReport | `<CH_ROOT>/RAG/<ChapterName>_RAG_ValidationReport.md` |
| LLM_SystemPrompt | `<CH_ROOT>/RAG/<ChapterName>_LLM_SystemPrompt.md` |
| RAG_QueryProfiles | `<CH_ROOT>/RAG/<ChapterName>_RAG_QueryProfiles.md` |
| Checklist | `<CH_ROOT>/<ChapterName>_PHASE5_RAGChecklist.md` |
| Trigger | `<CH_ROOT>/RAG/Trigger/RAG_READY.md` (or `RAG_INCOMPLETE.md`) |

The PHASE 1 files `<ChapterName>_RAG_chunks.jsonl` and `_RAG_metadata.json` stay in place. Mark them `superseded` in the ArtifactManifest; never delete them.

---

# 1. Gather all final, locked chapter outputs

Pull ONLY from `<CH_ROOT>`:

- Manuscript
- ReviewPacket
- Workbook
- Training
- ReferenceGuides
- Slides
- Audiobook
- eBook
- Kindle (PHASE 4 DOCX + HTML + metadata)
- InDesign
- DesignPacket (HTML text content and figure metadata, not scripts)
- Marketing (Intake + Seeds; Seeds carry their `status` into metadata)
- Governance (GlossaryNormalized, LearningMetadata, FigureRegistry, VersionMetadata, ArtifactManifest)
- RAG (PHASE 1 packet, for comparison only)
- Book-level: `/_BookMarketing/VoiceKit.md`

# 2. Build the chapter's RAG ingestion schema

Generate `<ChapterName>_RAG_Ingestion.json` using the unified schema. It must include:

- chunk definitions (IDs pointing into `Chunks/`)
- semantic tags
- metadata (chapterName, chapterNumber, part, lesson, coreValue, section, sourceArtifact, version)
- glossary terms (from GlossaryNormalized)
- framework terms (from TerminologyLock)
- claims registry
- voice constraints (VoiceKit + VoiceNotes)
- terminology lock
- marketing intake fields
- marketing seed fields (with `status`)
- design metadata (figure IDs, DSM component types)
- governance flags (certification level, open Needs Author Review items)
- authority hierarchy (Manuscript > Glossary > Learning Metadata/Figure Registry > derived artifacts, as in PHASE 2)
- version metadata
- artifact manifest reference

# 3. Chunk the chapter for RAG ingestion

- 500–1000 word chunks
- 100-word overlap (80–120 tolerated)
- semantic boundaries preserved; never split a concept mid-explanation
- section name and `sourceArtifact` in every chunk's metadata
- chunk ID format: `<ChapterName>::<sourceArtifact>::c<NNN>` (extends the PHASE 1 format)

Output: `<CH_ROOT>/RAG/Chunks/<ChapterName>_RAG_Chunks.jsonl`

# 4. Rebuild the ChromaDB collection

Collection: `<RAG_COLLECTION>` (one collection for the whole book; chapters are separated by metadata).

1. Delete existing vectors where `chapterName == <ChapterName>` (this chapter only).
2. Embed and ingest the new chunks with their metadata, semantic tags, authority level, marketing fields, design fields, and governance flags.
3. Record the collection count before and after.

Embedding model: the one named in the book-level config (default `nomic-embed-text` via Ollama). Use the same model for every chapter; if it changes, all chapters must be re-embedded.

# 5. Validate RAG integrity

Check:

- chunk count and size distribution
- metadata completeness
- semantic tag coverage
- glossary normalization
- terminology lock alignment
- claims registry alignment
- voice constraints present
- marketing safety (draft seeds flagged, Do-Not-Claim list present)
- design metadata and figure registry alignment
- authority hierarchy
- version metadata
- **retrieval smoke test:** 5 questions from the AudienceMap search questions; each must retrieve a chunk from the mapped manuscript section

Output: `<CH_ROOT>/RAG/<ChapterName>_RAG_ValidationReport.md`

# 6. Local LLM environment

### Record (do not assume) the environment state

- Ollama drafting model installed (default: Qwen2.5 14B Instruct)
- Ollama embedding model installed (default: nomic-embed-text)
- Ollama server reachable
- LM Studio (optional): same model loaded, local server started for n8n

If anything is missing, list it in the checklist as a blocker for PHASE 6. Do not mark it done.

### Write the chapter system prompt

`<CH_ROOT>/RAG/<ChapterName>_LLM_SystemPrompt.md`, assembled in this load order (fits an 8k window):
1. VoiceKit (book-level)
2. TerminologyLock (chapter)
3. Claims discipline + Do-Not-Claim list
4. Marketing rules (PHASE 1 Step 11F)
5. Design rules (DSM is authoritative; local-LLM design output is draft only)
6. Governance rules (manuscript never edited; everything is a draft until <AUTHOR> approves)
7. RAG query rules (cite chunk IDs; refuse when retrieval returns nothing relevant)

# 7. Create chapter-level RAG query profiles

`<CH_ROOT>/RAG/<ChapterName>_RAG_QueryProfiles.md`, with reusable templates (retrieval filter, top-k, prompt, output format, safety checks) for:

- Explain this concept
- Generate social posts
- Generate Reddit drafts
- Generate newsletter excerpts
- Generate podcast kits
- Generate scripts
- Generate design prompts
- Generate HTML blocks
- Generate SEO articles

# 8. Produce PHASE 5 checklist and trigger

Save `<CH_ROOT>/<ChapterName>_PHASE5_RAGChecklist.md`:

- All ingestion files created
- All chunks generated (count)
- All metadata validated
- All semantic tags applied
- All governance flags applied
- All marketing fields applied
- All design fields applied
- ChromaDB updated (before/after counts)
- Local LLM environment state recorded
- Query profiles created
- Any missing elements
- Recommendations for PHASE 6 (automation activation)
- `gateStatus: PASS | FAIL`

If `PASS`, create `<CH_ROOT>/RAG/Trigger/RAG_READY.md` (paths of the four deliverables + timestamp). Otherwise create `RAG_INCOMPLETE.md` listing the blockers.

## PHASE 5 exit gate

PHASE 6 may start when `RAG_READY.md` exists.
