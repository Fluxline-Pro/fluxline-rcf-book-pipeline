# PHASE 5: RAG Rebuild — Local + Cloud Indexes, LLM Setup (Per Chapter) (v4)

> **Pipeline position:** PHASE 5 of 7 (Knowledge) · **Upstream gate:** PHASE 4 checklist `gateStatus: PASS` and `Manuscript/Trigger/MANUSCRIPT_SYNCED.md` · **Downstream:** PHASE 6 Automation Activation
> **Canonical paths, status ladder, triggers, and deliverables:** see `MASTER_PIPELINE_OVERVIEW.md`.

**v4 changes (2026-09-24 dual-RAG):**
- The book now keeps **two vector indexes** built from **one canonical chunk set**:
  - **Track L (local):** ChromaDB in Docker, with vectors from the local ONNX/TEI embedding container.
  - **Track C (cloud):** Azure AI Search, with vectors from an Azure OpenAI embedding deployment.
- The two tracks cannot share vectors: each embedding model produces its own vector space and dimensions. They share chunk text, chunk IDs, and metadata, so a result from either index traces back to the same chunk.
- Adds a book-level config (`_BookAutomation/RAG/RAG_Config.json`), per-track index manifests, per-track triggers (`RAG_LOCAL_READY.md`, `RAG_CLOUD_READY.md`), and a parity check. `RAG_READY.md` means every **enabled** track passed.
- Local embedding model changed from Ollama `nomic-embed-text` to **`nomic-ai/nomic-embed-text-v1.5` served by the ONNX/TEI container**. The container's default, `all-MiniLM-L6-v2`, truncates input at 256 tokens, which would drop most of a 500–1000-word chunk.

**v3 changes (2026-09-22 pipeline alignment):** paths moved to `<CH_ROOT>`; chunk rule aligned with PHASES 1–2; ChromaDB rebuild scoped by `chapterName`; checklist and `RAG_READY.md` trigger added; environment state is recorded, not assumed.

---

**Purpose:**
Rebuild the chapter's RAG ingestion surface from the *final, locked* PHASE 1–4 outputs, where the manuscript is the version synced to the final eBook PDF in PHASE 4 Part 0. Embed it into every enabled index, then prepare the local LLM environment (and the cloud environment, when enabled) for grounded generation, marketing automation, and the workflows activated in PHASE 6.

Run **per chapter**, after PHASE 4.

## The two tracks

| | Track L — Local | Track C — Cloud |
|---|---|---|
| Purpose | Offline/private grounding for n8n + Ollama drafting, local tools, the orchestrator | Grounding for Azure-hosted consumers (Azure OpenAI chat, agents, web/CMS search, Copilot-style assistants) |
| Vector store | ChromaDB (Docker), collection `<RAG_COLLECTION>` | Azure AI Search, index `<RAG_INDEX_CLOUD>` |
| Embedding model | `nomic-ai/nomic-embed-text-v1.5` via the ONNX/TEI container (768 dims; model context 8k, served input usually capped lower by the container's token budget, e.g. 2048) | Azure OpenAI deployment of `text-embedding-3-small` (1536 dims; 8191-token input) |
| Access path | Orchestrator `/v1/rag` (ingest with `"chunking": "none"`, admin) or direct ChromaDB + TEI | Azure OpenAI Embeddings API + Azure AI Search REST/SDK |
| Secrets | none | `AZURE_OPENAI_*`, `AZURE_SEARCH_*` from environment variables only — never written to a file, report, or workflow export |
| Content allowed | Everything in the canonical chunk set | Canonical chunks **except** items marked `cloudEligible: false` (default: draft marketing seeds and internal governance notes) |
| Can be disabled | No (Track L is required) | Yes: `cloud.enabled: false` in `RAG_Config.json` |

Rule: **one embedding model per track, for every chapter.** If a track's model or dimensions change in `RAG_Config.json`, every chapter is re-embedded **for that track only**. The other track is untouched.

## Book-level config (create once; PHASE 5 reads it every run)

`<BOOK_ROOT>/_BookAutomation/RAG/RAG_Config.json`

```json
{
  "chunkSetVersion": "v4",
  "local": {
    "enabled": true,
    "store": "chromadb",
    "collection": "<RAG_COLLECTION>",
    "embeddingProvider": "tei-onnx",
    "embeddingModel": "nomic-ai/nomic-embed-text-v1.5",
    "dimensions": 768,
    "maxInputTokens": 2048,
    "prefixesAppliedBy": "ingestion-path",
    "taskPrefixes": { "document": "search_document: ", "query": "search_query: " },
    "endpoints": { "orchestrator": "http://127.0.0.1:3200/v1/rag", "chroma": "http://127.0.0.1:8000", "embedder": "http://127.0.0.1:8001" }
  },
  "cloud": {
    "enabled": false,
    "store": "azure-ai-search",
    "index": "<RAG_INDEX_CLOUD>",
    "embeddingProvider": "azure-openai",
    "embeddingModel": "text-embedding-3-small",
    "embeddingDeployment": "<deployment name>",
    "dimensions": 1536,
    "endpointEnv": { "openai": "AZURE_OPENAI_ENDPOINT", "openaiKey": "AZURE_OPENAI_API_KEY", "search": "AZURE_SEARCH_ENDPOINT", "searchKey": "AZURE_SEARCH_API_KEY" },
    "excludeWhere": { "cloudEligible": false }
  }
}
```

## Deliverables (PHASE 5)

| Deliverable | Path | Track |
|---|---|---|
| RAG_INGESTION (canonical, model-agnostic) | `<CH_ROOT>/RAG/<ChapterName>_RAG_Ingestion.json` + `<CH_ROOT>/RAG/Chunks/<ChapterName>_RAG_Chunks.jsonl` | shared |
| Local index manifest | `<CH_ROOT>/RAG/Index/<ChapterName>_RAG_Index_Local.json` | L |
| Cloud index manifest | `<CH_ROOT>/RAG/Index/<ChapterName>_RAG_Index_Cloud.json` | C |
| RAG_ValidationReport (both tracks + parity) | `<CH_ROOT>/RAG/<ChapterName>_RAG_ValidationReport.md` | both |
| LLM_SystemPrompt | `<CH_ROOT>/RAG/<ChapterName>_LLM_SystemPrompt.md` | both |
| RAG_QueryProfiles | `<CH_ROOT>/RAG/<ChapterName>_RAG_QueryProfiles.md` | both |
| Checklist | `<CH_ROOT>/<ChapterName>_PHASE5_RAGChecklist.md` | both |
| Triggers | `<CH_ROOT>/RAG/Trigger/RAG_LOCAL_READY.md`, `RAG_CLOUD_READY.md`, `RAG_READY.md` (or `RAG_INCOMPLETE.md`) | per track / combined |

Each index manifest records: track, store, collection/index name, embedding provider, model, dimensions, chunk count, chunk IDs, content hash of the chunk file, vector count for this chapter before and after, total index count before and after, timestamp, and the smoke-test result.

The PHASE 1 files `<ChapterName>_RAG_chunks.jsonl` and `_RAG_metadata.json` stay in place. Mark them `superseded` in the ArtifactManifest; never delete them.

---

# 1. Gather all final, locked chapter outputs

Pull ONLY from `<CH_ROOT>`:

- Manuscript (synced to the final eBook PDF in PHASE 4 Part 0; the authority)
- ReviewPacket
- Workbook
- Training
- ReferenceGuides
- Slides
- Audiobook (script only; skip if it predates the latest manuscript sync)
- eBook
- Kindle (PHASE 4 DOCX + HTML + metadata)
- InDesign
- DesignPacket (HTML text content and figure metadata, not scripts)
- Marketing (Intake + Seeds; Seeds carry their `status` into metadata)
- Governance (GlossaryNormalized, LearningMetadata, FigureRegistry, VersionMetadata, ArtifactManifest)
- RAG (PHASE 1 packet, for comparison only)
- Book-level: `/_BookMarketing/VoiceKit.md`, `/_BookAutomation/RAG/RAG_Config.json`

Any derived artifact that the PHASE 4 sync report lists as carrying pre-sync wording is either left out of the chunk set or tagged `stale: true` (never higher authority than the manuscript). The checklist says which.

# 2. Build the canonical ingestion schema (shared)

Generate `<ChapterName>_RAG_Ingestion.json`, the unified schema, **independent of any embedding model**. It must include:

- chunk definitions (IDs pointing into `Chunks/`)
- semantic tags
- metadata (chapterName, chapterNumber, part, lesson, coreValue, section, sourceArtifact, version, authorityLevel, `cloudEligible`)
- glossary terms (from GlossaryNormalized)
- framework terms (from TerminologyLock)
- claims registry
- voice constraints (VoiceKit + VoiceNotes)
- terminology lock
- marketing intake fields
- marketing seed fields (with `status`; `status: draft` ⇒ `cloudEligible: false` unless <AUTHOR> says otherwise)
- design metadata (figure IDs, DSM component types)
- governance flags (certification level, open Needs Author Review items)
- authority hierarchy (synced Manuscript > Glossary > Learning Metadata/Figure Registry > derived artifacts, as in PHASE 2)
- version metadata
- artifact manifest reference
- `targets`: which tracks the chunk set is embedded into this run, with the model and dimensions from `RAG_Config.json`

# 3. Chunk the chapter (shared)

- 500–1000 word chunks
- 100-word overlap (80–120 tolerated)
- semantic boundaries preserved; never split a concept mid-explanation
- section name and `sourceArtifact` in every chunk's metadata
- chunk ID format: `<ChapterName>::<sourceArtifact>::c<NNN>` (extends the PHASE 1 format)
- every chunk fits every enabled track's **served** input limit (1000 words ≈ 1,350 tokens; check `local.maxInputTokens`, since a container may serve less than the model's full context; Azure `text-embedding-3-small` accepts 8191). An embedder that silently truncates is a Track failure, not a warning.

Output: `<CH_ROOT>/RAG/Chunks/<ChapterName>_RAG_Chunks.jsonl`. **This one file feeds both tracks.** Nothing downstream may re-split it. If an ingestion path would re-chunk (for example an orchestrator that splits documents before embedding), use its no-split option (the fluxline orchestrator: `"chunking": "none"` on `/v1/rag` ingest) or send pre-computed vectors directly to the store, and record which in the index manifest.

# 4A. Track L — rebuild the local ChromaDB collection

Collection: `<RAG_COLLECTION>` (one collection for the whole book; chapters separated by metadata).

1. Confirm the embedder serves the model named in `RAG_Config.json` (`local.embeddingModel`), returns `local.dimensions`-length vectors, and accepts at least `local.maxInputTokens` tokens (TEI reports `model_id` and `max_input_length` at `/info`). If it serves anything else, stop Track L and record the blocker. Never write vectors of another size into the collection. If the collection already holds vectors of another size (built with an earlier model), it must be deleted and rebuilt for **every** chapter; ask <AUTHOR> before deleting.
2. Record the collection count and this chapter's vector count **before**.
3. Delete existing vectors where `chapterName == <ChapterName>` (this chapter only).
4. Embed each chunk with the document prefix (`search_document: `) prepended **for embedding only**; the stored text stays clean. If the ingestion path applies the prefix itself (`prefixesAppliedBy: "ingestion-path"`; the fluxline orchestrator does), send clean text and do not prefix twice. Ingest with the chunk ID, text, and all metadata (semantic tags, authority level, marketing fields, design fields, governance flags). Non-scalar metadata is stored as JSON strings.
5. Record the counts **after** (the chapter count must equal the chunk count) and write `RAG/Index/<ChapterName>_RAG_Index_Local.json`.

# 4B. Track C — rebuild the Azure AI Search index (skip if `cloud.enabled` is false)

Index: `<RAG_INDEX_CLOUD>`, same layout for every chapter:

| Field | Type | Notes |
|---|---|---|
| `id` | key (string) | Azure keys allow only letters, digits, `_`, `-`, `=`: use URL-safe Base64 of the chunk ID |
| `chunkId` | string, filterable | original `<ChapterName>::<sourceArtifact>::c<NNN>` |
| `content` | string, searchable | chunk text |
| `contentVector` | Collection(Edm.Single), `cloud.dimensions`, HNSW, cosine | from the Azure OpenAI embedding deployment |
| `chapterName`, `chapterNumber`, `section`, `sourceArtifact`, `version`, `authorityLevel`, `status` | filterable | from the ingestion schema |
| `tags`, `glossaryTerms` | Collection(Edm.String), filterable | |

1. Confirm the embedding deployment exists and returns `cloud.dimensions`-length vectors, and that the index exists with this schema. Create the index if missing; never change an existing field's type or dimension (a model change means a new index plus a full re-embed).
2. Record the index document count and this chapter's count **before** (`$filter=chapterName eq '<ChapterName>'`).
3. Delete this chapter's documents (query IDs by filter, then delete by key).
4. Embed every `cloudEligible` chunk with the Azure OpenAI deployment (no task prefix; batch within the deployment's rate limits, retrying on 429 with backoff) and upload with `mergeOrUpload`.
5. Record the counts **after** (the chapter count must equal the number of cloud-eligible chunks) and write `RAG/Index/<ChapterName>_RAG_Index_Cloud.json`.

Data-handling rule: only cloud-eligible, manuscript-derived text leaves the machine. Keys come from environment variables and are never echoed into files, logs, or reports.

# 5. Validate RAG integrity

**Shared checks:** chunk count and size distribution · metadata completeness · semantic tag coverage · glossary normalization · terminology lock alignment · claims registry alignment · voice constraints present · marketing safety (draft seeds flagged, Do-Not-Claim list present) · design metadata and figure registry alignment · authority hierarchy · version metadata · no chunk sourced from a stale derived artifact without its `stale` tag.

**Per enabled track:**
- model and dimensions match `RAG_Config.json`
- chapter vector count equals the chunks sent to that track
- **retrieval smoke test:** the same 5 questions from the AudienceMap search questions (queries use the query prefix `search_query: ` on Track L). Each must retrieve, in the top 5, a chunk from the mapped manuscript section.

**Parity (when both tracks are enabled):**
- every cloud chunk ID exists in the local collection with the same `version`
- the local-only chunk IDs are exactly the `cloudEligible: false` set
- informational: top-3 overlap per smoke-test question across the two tracks (low overlap is worth a look, not a failure)

Output: `<CH_ROOT>/RAG/<ChapterName>_RAG_ValidationReport.md`, with a **Shared**, **Track L**, **Track C**, and **Parity** section, each with PASS/FAIL.

# 6. LLM environments

### Record (do not assume) the environment state

**Local (required):**
- Ollama drafting model installed (default: Qwen2.5 14B Instruct)
- ONNX/TEI embedding container running `local.embeddingModel`, reachable at `local.endpoints.embedder`
- ChromaDB container reachable; orchestrator `/v1/rag` reachable (if used)
- Ollama server reachable
- LM Studio (optional): same model loaded, local server started for n8n

**Cloud (only if `cloud.enabled`):**
- Azure OpenAI endpoint reachable; embedding deployment present (and a chat deployment, if PHASE 6 cloud workflows will use one)
- Azure AI Search service reachable; index `<RAG_INDEX_CLOUD>` present with the §4B schema
- Required environment variables set (names only in the report, never values)

If anything is missing, list it in the checklist as a blocker for the affected track. Do not mark it done.

### Write the chapter system prompt

`<CH_ROOT>/RAG/<ChapterName>_LLM_SystemPrompt.md`, assembled in this load order (fits an 8k window; the same prompt serves local and cloud models):
1. VoiceKit (book-level)
2. TerminologyLock (chapter)
3. Claims discipline + Do-Not-Claim list
4. Marketing rules (PHASE 1 Step 11F)
5. Design rules (DSM is authoritative; LLM design output is draft only)
6. Governance rules (manuscript never edited; everything is a draft until <AUTHOR> approves)
7. RAG query rules (cite chunk IDs; refuse when retrieval returns nothing relevant; never mix results from the two indexes in one answer without labelling their source)

# 7. Create chapter-level RAG query profiles

`<CH_ROOT>/RAG/<ChapterName>_RAG_QueryProfiles.md`, with reusable templates. Each profile names its **track** (`local`, `cloud`, or `either`), retrieval filter, top-k, prompt, output format, and safety checks:

- Explain this concept
- Generate social posts
- Generate Reddit drafts
- Generate newsletter excerpts
- Generate podcast kits
- Generate scripts
- Generate design prompts
- Generate HTML blocks
- Generate SEO articles

Default: n8n/Ollama drafting profiles use `local`; web, CMS, and Azure-hosted assistant profiles use `cloud`.

# 8. Produce PHASE 5 checklist and triggers

Save `<CH_ROOT>/<ChapterName>_PHASE5_RAGChecklist.md`:

- Canonical ingestion files created; chunk count; cloud-eligible count
- All metadata validated; semantic tags, governance, marketing, and design fields applied
- **Track L:** model/dimensions, ChromaDB before/after counts, smoke test, `gateStatus: PASS | FAIL`
- **Track C:** enabled/disabled; model/dimensions, Azure AI Search before/after counts, smoke test, `gateStatus: PASS | FAIL | DISABLED`
- Parity result (if both enabled)
- LLM environment state recorded (local and cloud)
- Query profiles created
- Any missing elements
- Recommendations for PHASE 6 (automation activation)
- Overall `gateStatus: PASS | FAIL`: PASS when Track L passes **and** Track C is PASS or DISABLED

Triggers (rename any older one to `*_superseded_<timestamp>.md`):
- `RAG/Trigger/RAG_LOCAL_READY.md` when Track L passes: collection, model, dims, counts, timestamp.
- `RAG/Trigger/RAG_CLOUD_READY.md` when Track C passes: index, model, dims, counts, timestamp.
- `RAG/Trigger/RAG_READY.md` when the overall gate passes: paths of the deliverables, each track's status, timestamp.
- Otherwise `RAG/Trigger/RAG_INCOMPLETE.md` listing the blockers per track.

Re-run rule: when PHASE 4 Part 0 re-syncs the manuscript (eBook re-export), PHASE 5 re-runs for that chapter, and **both** enabled tracks are rebuilt from the new chunk set. An index built from an older chunk set is stale.

## PHASE 5 exit gate

PHASE 6 may start when `RAG_READY.md` exists. Local-only workflows need `RAG_LOCAL_READY.md`; cloud-grounded workflows also need `RAG_CLOUD_READY.md`.
