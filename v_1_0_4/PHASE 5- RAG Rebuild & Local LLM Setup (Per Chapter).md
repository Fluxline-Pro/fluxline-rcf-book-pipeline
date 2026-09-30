# PHASE 5: RAG Rebuild — Local + Cloud Vectors, LLM Setup (Per Chapter) (v4.2)

> **Pipeline position:** PHASE 5 of 7 (Knowledge) · **Upstream gate:** PHASE 4 checklist `gateStatus: PASS` and `Manuscript/Trigger/MANUSCRIPT_SYNCED.md` · **Downstream:** PHASE 6 Automation Activation
> **Canonical paths, status ladder, triggers, and deliverables:** see `MASTER_PIPELINE_OVERVIEW.md`.

**v4.2 changes (2026-09-30 governed cloud track):**
- **Track C can embed through a governance gateway** (`cloud.embeddingProvider: "governance-gateway"`, recommended). PHASE 5 then holds a gateway credential instead of model credentials, and the gateway runs its checks before calling the embedding deployment. Direct Azure OpenAI stays available for setups without a gateway.
- **Default cloud dimensions are 1,024** (was 3,072): smaller vector files, and the size downstream products built on this store expect. Existing cloud stores keep their dimensions until re-embedded (the §4B model-change rule applies).
- **Vector lines carry more metadata:** `part` and `lesson` on every chunk, and `figureId` and `altText` on FigureRegistry chunks, so consumers can filter by lesson and show figure cards.
- **Consumers are notified, not written to.** A cloud consumer (for example a reader-facing companion) builds its own index from these files. PHASE 6 §3G tells it when a chapter changed.

**v4.1 changes (2026-09-30 workbook track):** the workbook is no longer a RAG input. The manuscript still carries each chapter's main exercise text.

**v4 changes (2026-09-24 dual-RAG):**
- The book now keeps **two vector stores** built from **one canonical chunk set**:
  - **Track L (local):** ChromaDB in Docker, with vectors from the local ONNX/TEI embedding container.
  - **Track C (cloud):** vector files in **Azure Blob Storage**, with vectors from an Azure OpenAI **`text-embedding-3-large`** deployment (3,072 dimensions, multilingual). There is no search service: cloud consumers load a chapter's vector file and rank chunks by cosine similarity in memory, which is fast at book scale and costs only the per-token embedding calls plus Blob storage.
- The two tracks cannot share vectors: each embedding model produces its own vector space and dimensions. They share chunk text, chunk IDs, and metadata, so a result from either index traces back to the same chunk.
- Adds a book-level config (`_BookAutomation/RAG/RAG_Config.json`), per-track index manifests, per-track triggers (`RAG_LOCAL_READY.md`, `RAG_CLOUD_READY.md`), and a parity check. `RAG_READY.md` means every **enabled** track passed.
- **Book audit (2026-09-27):** the cloud store's `manifest.json` records the PHASE 0.9 final audit, and consumers treat the book as release-ready only once it passes. The PHASE 0.9 evaluation set adds an extended retrieval check.
- Local embedding model changed from Ollama `nomic-embed-text` to **`nomic-ai/nomic-embed-text-v1.5` served by the ONNX/TEI container**. The container's default, `all-MiniLM-L6-v2`, truncates input at 256 tokens, which would drop most of a 500–1000-word chunk.

**v3 changes (2026-09-22 pipeline alignment):** paths moved to `<CH_ROOT>`; chunk rule aligned with PHASES 1–2; ChromaDB rebuild scoped by `chapterName`; checklist and `RAG_READY.md` trigger added; environment state is recorded, not assumed.

---

**Purpose:**
Rebuild the chapter's RAG ingestion surface from the *final, locked* PHASE 1–4 outputs, where the manuscript is the version synced to the final eBook PDF in PHASE 4 Part 0. Embed it into every enabled index, then prepare the local LLM environment (and the cloud environment, when enabled) for grounded generation, marketing automation, and the workflows activated in PHASE 6.

Run **per chapter**, after PHASE 4.

## The two tracks

| | Track L — Local | Track C — Cloud |
|---|---|---|
| Purpose | Offline/private grounding for n8n + Ollama drafting, local tools, the orchestrator | Grounding for Azure-hosted and multilingual consumers (Azure OpenAI chat, agents, web/CMS search, Copilot-style assistants) |
| Vector store | ChromaDB (Docker), collection `<RAG_COLLECTION>` | Azure Blob Storage, private container `<RAG_BLOB_CONTAINER>`: one gzipped JSONL vector file per chapter plus a `current.json` pointer (layout in §4B) |
| Embedding model | `nomic-ai/nomic-embed-text-v1.5` via the ONNX/TEI container (768 dims; model context 8k, served input usually capped lower by the container's token budget, e.g. 2048) | Azure OpenAI deployment of `text-embedding-3-large` (1,024 dims by default, up to 3,072; 8,192-token input; multilingual: a query in another language retrieves the English chunks) |
| Access path | Orchestrator `/v1/rag` (ingest with `"chunking": "none"`, admin) or direct ChromaDB + TEI | A **governance gateway** flow that calls the embedding deployment (recommended), or the Azure OpenAI Embeddings API directly; Azure Blob Storage SDK/REST for the files; retrieval is in-memory cosine similarity over the chapter's vector file |
| Secrets | none | The gateway's client credentials (gateway mode) or Microsoft Entra ID / `AZURE_OPENAI_*` (direct mode), plus Entra ID or `AZURE_STORAGE_*` for Blob — from a credential store or environment variables, never written to a file, report, or workflow export |
| Content allowed | Everything in the canonical chunk set | Canonical chunks **except** items marked `cloudEligible: false` (default: draft marketing seeds and internal governance notes) |
| Can be disabled | No (Track L is required) | Yes: `cloud.enabled: false` in `RAG_Config.json` |

`cloud.embeddingProvider` is `governance-gateway` (recommended: every embedding call goes through a gateway flow at `cloud.gateway.baseUrl` that checks the request first, then calls the embedding deployment; the gateway credential comes from `cloud.gateway.credentialEnv`) or `azure-openai` (direct). `cloud.auth` is `entra-id` (preferred; `openaiKey` and `storageSas` are then unused) or `keys` (the named environment variables); in gateway mode it covers Blob only. `cloud.dimensions` defaults to 1024 and can be raised to 3072; whatever value is set is sent on every ingest **and** query call. `multilingualSmokeTest` lists the extra languages the §5 smoke test uses.

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
    "store": "azure-blob",
    "container": "<RAG_BLOB_CONTAINER>",
    "blobPrefix": "<BOOK>/",
    "retrieval": "in-memory-cosine",
    "embeddingProvider": "governance-gateway",
    "gateway": {
      "baseUrl": "<GATEWAY_URL>",
      "embedFlow": "<CLOUD_EMBED_FLOW>",
      "maxInputsPerCall": 256,
      "credentialEnv": { "clientId": "GATEWAY_CLIENT_ID", "clientSecret": "GATEWAY_CLIENT_SECRET" }
    },
    "embeddingModel": "text-embedding-3-large",
    "embeddingDeployment": "<deployment name>",
    "dimensions": 1024,
    "maxInputTokens": 8192,
    "multilingualSmokeTest": ["es"],
    "auth": "entra-id",
    "endpointEnv": { "openai": "AZURE_OPENAI_ENDPOINT", "openaiKey": "AZURE_OPENAI_API_KEY", "storageAccountUrl": "AZURE_STORAGE_ACCOUNT_URL", "storageSas": "AZURE_STORAGE_SAS_TOKEN" },
    "excludeWhere": { "cloudEligible": false },
    "consumers": []
  }
}
```

## Deliverables (PHASE 5)

| Deliverable | Path | Track |
|---|---|---|
| RAG_INGESTION (canonical, model-agnostic) | `<CH_ROOT>/RAG/<ChapterName>_RAG_Ingestion.json` + `<CH_ROOT>/RAG/Chunks/<ChapterName>_RAG_Chunks.jsonl` | shared |
| Local index manifest | `<CH_ROOT>/RAG/Index/<ChapterName>_RAG_Index_Local.json` | L |
| Cloud index manifest | `<CH_ROOT>/RAG/Index/<ChapterName>_RAG_Index_Cloud.json` | C |
| Cloud vector file (in Blob) | `<RAG_BLOB_CONTAINER>/<BOOK>/chapters/<ChapterName>/<chunkSetHash>/vectors.jsonl.gz` + `current.json` pointer | C |
| RAG_ValidationReport (both tracks + parity) | `<CH_ROOT>/RAG/<ChapterName>_RAG_ValidationReport.md` | both |
| LLM_SystemPrompt | `<CH_ROOT>/RAG/<ChapterName>_LLM_SystemPrompt.md` | both |
| RAG_QueryProfiles | `<CH_ROOT>/RAG/<ChapterName>_RAG_QueryProfiles.md` | both |
| Checklist | `<CH_ROOT>/<ChapterName>_PHASE5_RAGChecklist.md` | both |
| Triggers | `<CH_ROOT>/RAG/Trigger/RAG_LOCAL_READY.md`, `RAG_CLOUD_READY.md`, `RAG_READY.md` (or `RAG_INCOMPLETE.md`) | per track / combined |

Each index manifest records: track, store, collection name (local) or container and blob paths (cloud), embedding provider, model, dimensions, chunk count, chunk IDs, content hash of the chunk file, vector count for this chapter before and after, total index count before and after, timestamp, and the smoke-test result.

The PHASE 1 files `<ChapterName>_RAG_chunks.jsonl` and `_RAG_metadata.json` stay in place. Mark them `superseded` in the ArtifactManifest; never delete them.

---

# 1. Gather all final, locked chapter outputs

Pull ONLY from `<CH_ROOT>`:

- Manuscript (synced to the final eBook PDF in PHASE 4 Part 0; the authority)
- ReviewPacket
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
- metadata (chapterName, chapterNumber, part, lesson, coreValue, section, sourceArtifact, version, authorityLevel, `cloudEligible`; on FigureRegistry chunks also `figureId` and `altText`, the figure's alt text from the registry or the PHASE 4 Kindle metadata)
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
- every chunk fits every enabled track's **served** input limit (1000 words ≈ 1,350 tokens; check `local.maxInputTokens`, since a container may serve less than the model's full context; Azure `text-embedding-3-large` accepts 8,192). An embedder that silently truncates is a Track failure, not a warning.

Output: `<CH_ROOT>/RAG/Chunks/<ChapterName>_RAG_Chunks.jsonl`. **This one file feeds both tracks.** Nothing downstream may re-split it. If an ingestion path would re-chunk (for example an orchestrator that splits documents before embedding), use its no-split option (the fluxline orchestrator: `"chunking": "none"` on `/v1/rag` ingest) or send pre-computed vectors directly to the store, and record which in the index manifest.

# 4A. Track L — rebuild the local ChromaDB collection

Collection: `<RAG_COLLECTION>` (one collection for the whole book; chapters separated by metadata).

1. Confirm the embedder serves the model named in `RAG_Config.json` (`local.embeddingModel`), returns `local.dimensions`-length vectors, and accepts at least `local.maxInputTokens` tokens (TEI reports `model_id` and `max_input_length` at `/info`). If it serves anything else, stop Track L and record the blocker. Never write vectors of another size into the collection. If the collection already holds vectors of another size (built with an earlier model), it must be deleted and rebuilt for **every** chapter; ask <AUTHOR> before deleting.
2. Record the collection count and this chapter's vector count **before**.
3. Delete existing vectors where `chapterName == <ChapterName>` (this chapter only).
4. Embed each chunk with the document prefix (`search_document: `) prepended **for embedding only**; the stored text stays clean. If the ingestion path applies the prefix itself (`prefixesAppliedBy: "ingestion-path"`; the fluxline orchestrator does), send clean text and do not prefix twice. Ingest with the chunk ID, text, and all metadata (semantic tags, authority level, marketing fields, design fields, governance flags). Non-scalar metadata is stored as JSON strings.
5. Record the counts **after** (the chapter count must equal the chunk count) and write `RAG/Index/<ChapterName>_RAG_Index_Local.json`.

# 4B. Track C — write the chapter's vectors to Azure Blob Storage (skip if `cloud.enabled` is false)

Container: `<RAG_BLOB_CONTAINER>` (private: no anonymous access). Same layout for every chapter:

```
<RAG_BLOB_CONTAINER>/
  <BOOK>/manifest.json                                   book-level: model, dimensions, each chapter's current pointer, and the final audit status
  <BOOK>/chapters/<ChapterName>/current.json             pointer: chunkSetHash, version, vector file path, count, model, dims, updated
  <BOOK>/chapters/<ChapterName>/<chunkSetHash>/vectors.jsonl.gz
```

Each line of `vectors.jsonl.gz` is one cloud-eligible chunk: `{ "chunkId", "content", "metadata": { chapterName, chapterNumber, part, lesson, section, sourceArtifact, version, authorityLevel, status, tags, glossaryTerms, figureId?, altText? }, "vector": [cloud.dimensions floats] }`. `figureId` and `altText` are present on FigureRegistry chunks only. The chunk ID is stored as-is; Blob has no key-format limits.

1. Confirm the embedding path (the gateway flow in gateway mode, or the deployment directly) runs `cloud.embeddingModel` and returns `cloud.dimensions`-length vectors (send `dimensions` on every call). In gateway mode, confirm the gateway credential can execute `cloud.gateway.embedFlow` and nothing else it doesn't need. Confirm the container exists, is private, and PHASE 5's identity can write to it (Entra role **Storage Blob Data Contributor**). If `<BOOK>/manifest.json` names a different model or dimensions, stop Track C and record the blocker: a model or dimension change means re-embedding **every** chapter under a new `blobPrefix`; ask <AUTHOR> first.
2. Record **before**: this chapter's `current.json` (chunk count and `chunkSetHash`), or "none".
3. Embed every `cloudEligible` chunk (no task prefix). Gateway mode: at most `cloud.gateway.maxInputsPerCall` inputs per flow call. Direct mode: at most 2,048 inputs and 300,000 tokens per request. Retry 429s with backoff, and check that every returned vector has `cloud.dimensions` values. A request the gateway blocks is a Track C failure for that chunk; record the gateway's reason (never the chunk text) and stop Track C.
4. Upload `vectors.jsonl.gz` to a **new** `<chunkSetHash>/` folder and verify it (line count equals the cloud-eligible chunk count). Only then overwrite `current.json`, and update the chapter's entry in `<BOOK>/manifest.json`. Readers follow `current.json`, so they never see a half-written file.
5. Keep the previous `<chunkSetHash>/` folder until the §5 smoke test passes (for rollback), then delete older folders, keeping one prior version.
6. Record **after** (the count in `current.json` must equal the number of cloud-eligible chunks) and write `RAG/Index/<ChapterName>_RAG_Index_Cloud.json` with the blob paths, `chunkSetHash`, ETag, model, and dimensions.

**Release-ready flag:** `<BOOK>/manifest.json` carries `"auditFinalClear": { "runId": "", "timestamp": "" }`. Set it only when `_BookGovernance/Audit/Trigger/AUDIT_FINAL_CLEAR.md` exists and every chapter's `current.json` was written from the synced manuscript that the audit checked; clear it whenever a chapter is rebuilt after that audit. Chapters can be ingested and tested before then. External products (for example a reader-facing companion) should serve the book only while the flag is set.

Retrieval (used by the §5 smoke test and every PHASE 6 cloud consumer): read `current.json` → load the vector file (cache it by `chunkSetHash`) → filter by metadata → embed the query through the same path (gateway flow or deployment) and `dimensions` → rank by cosine similarity (`text-embedding-3` vectors are unit-length, so a dot product is enough) → top-k. At book scale (a few thousand chunks), this runs in milliseconds and needs no search service. If a consumer later needs keyword/hybrid search or a much larger corpus, add a search index that reads these same Blob files. That's a consumer change, not a PHASE 5 change.

Data-handling rule: only cloud-eligible, manuscript-derived text leaves the machine, and in gateway mode it leaves only through the gateway. No reader or customer data is ever part of an ingestion call. Prefer Entra ID; if keys or a SAS are used, they come from environment variables, are short-lived where possible, and are never echoed into files, logs, or reports. Consumers get read-only access (**Storage Blob Data Reader**).

# 5. Validate RAG integrity

**Shared checks:** chunk count and size distribution · metadata completeness · semantic tag coverage · glossary normalization · terminology lock alignment · claims registry alignment · voice constraints present · marketing safety (draft seeds flagged, Do-Not-Claim list present) · design metadata and figure registry alignment · authority hierarchy · version metadata · no chunk sourced from a stale derived artifact without its `stale` tag.

**Per enabled track:**
- model and dimensions match `RAG_Config.json`
- chapter vector count equals the chunks sent to that track (Track C: `current.json` points at a file whose `chunkSetHash` matches the current `RAG/Chunks/` file)
- **retrieval smoke test:** the same 5 questions from the AudienceMap search questions (queries use the query prefix `search_query: ` on Track L). Each must retrieve, in the top 5, a chunk from the mapped manuscript section.
- **multilingual smoke test (Track C):** 2 of those questions, translated into each language in `cloud.multilingualSmokeTest`, must also retrieve a chunk from the mapped section in the top 5.

**Parity (when both tracks are enabled):**
- every cloud chunk ID exists in the local collection with the same `version`
- the local-only chunk IDs are exactly the `cloudEligible: false` set
- informational: top-3 overlap per smoke-test question across the two tracks (low overlap is worth a look, not a failure)

**Extended retrieval check (when the PHASE 0.9 evaluation set exists):** run the chapter's `answerable` items from `_BookGovernance/Audit/EvalSet/<EDITION>/<ChapterName>_EvalSet.jsonl` against each enabled track and report the share whose `expected_anchor` section appears in the top 5. This is informational: the pass thresholds belong to the product that consumes the store, and the `not_in_book` and `personal_advice` items test that product's answer behavior, not retrieval.

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
- Gateway mode: `cloud.gateway.baseUrl` reachable, `cloud.gateway.embedFlow` present, gateway credential variables set. Direct mode: Azure OpenAI endpoint reachable and the `text-embedding-3-large` deployment present. Either way, a chat path if PHASE 6 cloud workflows will use one
- Storage account reachable; container `<RAG_BLOB_CONTAINER>` present and private; PHASE 5 identity has Storage Blob Data Contributor, cloud consumers have Storage Blob Data Reader
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

Default: n8n/Ollama drafting profiles use `local`; web, CMS, Azure-hosted assistant, and non-English reader profiles use `cloud`. A cloud profile may answer in the reader's language, but quotations and cited wording come from the English chunk text, and any translation is a draft.

# 8. Produce PHASE 5 checklist and triggers

Save `<CH_ROOT>/<ChapterName>_PHASE5_RAGChecklist.md`:

- Canonical ingestion files created; chunk count; cloud-eligible count
- All metadata validated; semantic tags, governance, marketing, and design fields applied
- **Track L:** model/dimensions, ChromaDB before/after counts, smoke test, `gateStatus: PASS | FAIL`
- **Track C:** enabled/disabled; model/dimensions, Blob `current.json` before/after counts and `chunkSetHash`, smoke test (including multilingual), `gateStatus: PASS | FAIL | DISABLED`
- Parity result (if both enabled)
- LLM environment state recorded (local and cloud)
- Query profiles created
- Any missing elements
- Recommendations for PHASE 6 (automation activation)
- Overall `gateStatus: PASS | FAIL`: PASS when Track L passes **and** Track C is PASS or DISABLED

Triggers (rename any older one to `*_superseded_<timestamp>.md`):
- `RAG/Trigger/RAG_LOCAL_READY.md` when Track L passes: collection, model, dims, counts, timestamp.
- `RAG/Trigger/RAG_CLOUD_READY.md` when Track C passes: container, `current.json` path, model, dims, counts, timestamp.
- `RAG/Trigger/RAG_READY.md` when the overall gate passes: paths of the deliverables, each track's status, timestamp.
- Otherwise `RAG/Trigger/RAG_INCOMPLETE.md` listing the blockers per track.

Re-run rule: when PHASE 4 Part 0 re-syncs the manuscript (eBook re-export), PHASE 5 re-runs for that chapter, and **both** enabled tracks are rebuilt from the new chunk set. An index built from an older chunk set is stale. PHASE 6 §3G runs this re-run nightly for any chapter whose inputs changed, then notifies `cloud.consumers`.

## PHASE 5 exit gate

PHASE 6 may start when `RAG_READY.md` exists. Local-only workflows need `RAG_LOCAL_READY.md`; cloud-grounded workflows also need `RAG_CLOUD_READY.md`.
