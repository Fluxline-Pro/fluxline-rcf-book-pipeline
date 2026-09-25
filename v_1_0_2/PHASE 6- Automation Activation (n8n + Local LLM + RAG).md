# PHASE 6: Automation Activation (n8n + Local LLM + Cloud LLM + RAG + OpenClaw) (v4)

> **Pipeline position:** PHASE 6 of 7 (Automation) · **Upstream gate:** `RAG/Trigger/RAG_READY.md` exists · **Downstream:** PHASE 6.5 Publication QA
> **Canonical paths, status ladder, triggers, and deliverables:** see `MASTER_PIPELINE_OVERVIEW.md`.

**v4 changes (2026-09-24 dual-RAG):**
- PHASE 5 now builds two indexes: **Local** (ChromaDB + ONNX/TEI embeddings) and **Cloud** (Azure AI Search + Azure OpenAI embeddings). Every workflow declares which index it is grounded on, and it embeds its queries with **that index's** model.
- The AutomationIndex entry records both tracks and their triggers. `RAG_LOCAL_READY.md` enables local workflows; `RAG_CLOUD_READY.md` enables cloud-grounded workflows.
- New §4B (connect the cloud LLM) and new Test 6 (index parity and routing). Tests 1 and 3 run once per enabled track.
- Azure keys live only in the n8n credential store or environment variables, never in exported workflow JSON.

**v3 changes (2026-09-22 pipeline alignment):** AutomationIndex at `<BOOK_ROOT>/_BookAutomation/`; fixed homes for n8n exports and OpenClaw pipelines; every trigger created by an earlier phase; human approval gate.

---

**Purpose:**
Activate the automation ecosystem for the chapter using the rebuilt RAG indexes (PHASE 5), the locked PHASE 1–4 outputs, and the LLM environments. This phase enables:

- automated marketing drafts
- automated design drafts (inputs to Claude Design, never replacements for DSM output)
- automated governance checks (report-only)
- automated metadata consistency checks
- content calendar drafts (scheduling needs approval)
- chapter-level and multi-chapter batch workflows
- cloud-grounded consumers (Azure-hosted assistants, web/CMS search), when the cloud track is enabled

Run **per chapter**, or in batch mode once multiple chapters have `RAG_READY.md`.

## Deliverables (PHASE 6)

| Deliverable | Path |
|---|---|
| N8N_AUTOMATIONS | `/_BookAutomation/n8n/<BOOK>_<WorkflowName>.json` (exported, chapter-parameterized workflows, credentials stripped) |
| OpenClaw pipelines | `/_BookAutomation/OpenClaw/<BOOK>_<PipelineName>.yaml` (or `.json` — pick one format and use it for every pipeline) |
| AutomationIndex.json | `/_BookAutomation/AutomationIndex.json` |
| ActivationReport | `<CH_ROOT>/<ChapterName>_PHASE6_ActivationReport.md` |
| Checklist | `<CH_ROOT>/<ChapterName>_PHASE6_AutomationChecklist.md` |
| Automation drafts (outputs) | `<CH_ROOT>/Marketing/Generated/<YYYYMMDD>/` (all `status: draft`) |

`/_BookAutomation/` = `<BOOK_ROOT>/_BookAutomation/`

## Approval rule (applies to every workflow, local or cloud)

- Generated content is written with `status: draft`, `voiceCheck: pending`, and `groundedOn: local | cloud`.
- Only <AUTHOR> moves an item to `approved`. Only approved items may be scheduled or published.
- Automations never edit the manuscript and never overwrite files in `Final/` outside `Marketing/Generated/`. Governance automations report; they do not fix.
- Automations never write to either vector index. Only PHASE 5 rebuilds them.

# 1. Register the chapter in the Automation Index

Add or update the chapter's entry in `/_BookAutomation/AutomationIndex.json`:

```json
{
  "chapterName": "",
  "chapterNumber": "",
  "folderPath": "<CH_ROOT>",
  "certificationLevel": "",
  "triggers": {
    "marketingReady": "<CH_ROOT>/Marketing/Trigger/MARKETING_READY.md",
    "governanceReady": "<CH_ROOT>/Governance/Trigger/GOVERNANCE_READY.md",
    "designReady": "<CH_ROOT>/DesignPacket/Trigger/DESIGN_READY.md",
    "ragLocalReady": "<CH_ROOT>/RAG/Trigger/RAG_LOCAL_READY.md",
    "ragCloudReady": "<CH_ROOT>/RAG/Trigger/RAG_CLOUD_READY.md",
    "ragReady": "<CH_ROOT>/RAG/Trigger/RAG_READY.md"
  },
  "rag": {
    "local": { "enabled": true, "collection": "<RAG_COLLECTION>", "embeddingModel": "", "indexManifest": "<CH_ROOT>/RAG/Index/<ChapterName>_RAG_Index_Local.json" },
    "cloud": { "enabled": false, "index": "<RAG_INDEX_CLOUD>", "embeddingModel": "", "indexManifest": "<CH_ROOT>/RAG/Index/<ChapterName>_RAG_Index_Cloud.json" }
  },
  "ragIngestionPath": "<CH_ROOT>/RAG/<ChapterName>_RAG_Ingestion.json",
  "llmSystemPromptPath": "<CH_ROOT>/RAG/<ChapterName>_LLM_SystemPrompt.md",
  "queryProfilesPath": "<CH_ROOT>/RAG/<ChapterName>_RAG_QueryProfiles.md",
  "n8nWorkflows": [],
  "openClawPipelines": [],
  "automationStatus": "inactive",
  "lastActivationTest": ""
}
```

Status values: `inactive` → `active` → `batch-ready`. New entries start `inactive`. The `rag.*.enabled` flags and models are copied from `_BookAutomation/RAG/RAG_Config.json` and the chapter's index manifests; they are not decided here.

# 2. Load the chapter's RAG profile into n8n

Import:

- `<ChapterName>_RAG_Ingestion.json`
- `<ChapterName>_RAG_QueryProfiles.md` (each profile names its track)
- `<ChapterName>_LLM_SystemPrompt.md`
- the chapter's index manifests (collection/index name, model, dimensions)

These are the grounding layer for every automation. A workflow retrieves only from the track its query profile names.

# 3. Activate n8n chapter workflows

Each workflow is tagged **local** (Ollama + ChromaDB) or **cloud** (Azure OpenAI + Azure AI Search). Default routing: 3A–3E run **local**. A workflow runs **cloud** only when it serves an Azure-hosted consumer or <AUTHOR> chooses cloud for it.

### 3A. Marketing automation (drafts)
Social posts · Reddit drafts · Newsletter excerpts · Podcast kits · Short scripts · Audiobook teasers · Image prompts · SEO articles · Content calendar

### 3B. Design automation (drafts only)
HTML slide deck drafts · HTML training drafts · HTML one-pager drafts · Infographic prompts · Layout suggestions
→ Outputs are input material for Claude Design. Anything that would enter `DesignPacket/` goes through PHASE 3 and 3.5.

### 3C. Governance automation (report-only)
Claims validation · Terminology validation · Metadata consistency · Voice consistency · Marketing safety · Figure registry alignment · Glossary normalization checks · **Index drift check** (each index manifest's chunk-set hash still matches the current `RAG/Chunks/` file; both tracks at the same chapter version)

### 3D. Publishing automation (checks)
Kindle DOCX validation · EPUB readiness · InDesign asset presence · PDF export checks

### 3E. Knowledge system automation
RAG query testing (per track) · RAG semantic map updates · CMS ingestion (drafts; cloud-grounded) · LMS ingestion (drafts)

### Triggers

| Trigger | Created by | Starts |
|---|---|---|
| `MARKETING_READY.md` | PHASE 1 / PHASE 2 | 3A |
| `GOVERNANCE_READY.md` | PHASE 2 | 3C |
| `DESIGN_READY.md` | PHASE 3.5 | 3B, 3D |
| `RAG_LOCAL_READY.md` | PHASE 5 (Track L) | local 3E; enables every **local** workflow |
| `RAG_CLOUD_READY.md` | PHASE 5 (Track C) | cloud 3E; enables every **cloud** workflow |
| `RAG_READY.md` | PHASE 5 (all enabled tracks) | enables the chapter for batch mode |
| daily cron / weekly cron / manual | n8n | per workflow |

A trigger only fires workflows for chapters whose `automationStatus` is `active` or `batch-ready`, and a workflow only runs if its track's trigger exists and its track is enabled in the AutomationIndex.

Export every activated workflow to `/_BookAutomation/n8n/` (credentials stripped) and list it in the chapter's `n8nWorkflows` with its track.

# 4. Connect the LLMs to n8n

### 4A. Local (required)
**Ollama:** drafting model endpoint · system prompt injection · RAG query injection · marketing, design, and governance rules
**Local retrieval:** query embeddings from the **same ONNX/TEI embedder and model as PHASE 5 Track L** (with the query prefix, e.g. `search_query: ` for nomic), then retrieval from ChromaDB `<RAG_COLLECTION>` (directly or through the orchestrator's `/v1/rag`)
**LM Studio (optional):** OpenAI-compatible endpoint · multi-step reasoning · long-form generation · design packet integration

### 4B. Cloud (only if the cloud track is enabled)
**Azure OpenAI:** chat deployment for cloud-grounded drafting · embedding deployment **identical to PHASE 5 Track C** for query vectors
**Azure AI Search:** vector (or hybrid vector + keyword) query against `<RAG_INDEX_CLOUD>`, filtered by `chapterName`
**Credentials:** n8n credential store (or environment variables) only. Never pasted into Code nodes, workflow JSON, reports, or logs.
**Rule:** never query one index with the other track's embeddings. The dimensions differ, and even equal-sized vectors from different models are meaningless to each other.

# 5. Activate OpenClaw pipelines

Define each pipeline in `/_BookAutomation/OpenClaw/` and list it in the chapter's `openClawPipelines`. Each pipeline step declares its track (local/cloud):

- **5A. Multi-asset marketing:** pull-lines → social → newsletter → SEO → scripts → podcast kit
- **5B. Multi-asset design:** design packet → HTML drafts → figure prompts → layout notes
- **5C. Multi-asset governance:** metadata → glossary → claims → terminology → voice → RAG (both indexes' drift checks)
- **5D. Multi-asset publishing checks:** Kindle → EPUB → PDF → InDesign → LMS → CMS

OpenClaw handles multi-step reasoning and multi-agent workflows; the approval rule above applies to every step.

# 6. Run the chapter activation test

Run Tests 1 and 3 once **per enabled track**. Label every sample output with its track.

**Test 1 — RAG query (per track):** "Explain the chapter's thesis." · "Generate 3 social posts." · "Generate 1 Reddit draft." · "Generate 1 design prompt." Every answer cites chunk IDs from the index it queried.

**Test 2 — n8n workflow:** trigger the Social, Newsletter, Design, and Governance workflows (plus one cloud workflow, if the cloud track is enabled).

**Test 3 — LLM grounding (per track):** no hallucinations · no claim drift (every claim traces to the ClaimsRegistry) · no terminology drift · voice consistency · design consistency

**Test 4 — Publishing:** Kindle DOCX integrity · HTML readiness · EPUB safety

**Test 5 — Approval rule:** confirm every output landed as `status: draft` (with `groundedOn`) in `Marketing/Generated/`, that nothing was published or scheduled, and that no workflow wrote to either index.

**Test 6 — Index routing and parity (if both tracks are enabled):** each workflow queried only its declared track; the query embedding model matched that index's manifest; the two index manifests share the same chunk-set hash and chapter version; no Azure secret appears in any exported workflow or report.

Save results (pass/fail per test and per track, sample outputs, issues) to `<CH_ROOT>/<ChapterName>_PHASE6_ActivationReport.md`.

# 7. Mark the chapter "Automation Active"

Only if Tests 1–6 pass (Test 6 counts as passed when the cloud track is disabled), set `"automationStatus": "active"` and `lastActivationTest` in `AutomationIndex.json`.

# 8. Produce PHASE 6 checklist

Save `<CH_ROOT>/<ChapterName>_PHASE6_AutomationChecklist.md`:

- RAG loaded (per track: collection/index, model, trigger present)
- LLMs connected (local; cloud if enabled)
- n8n workflows activated and exported (with track, credentials stripped)
- OpenClaw pipelines defined and activated
- Automation index updated
- Activation tests passed (per track)
- Any missing elements
- Recommendations for batch mode
- `gateStatus: PASS | FAIL`

## PHASE 6 exit gate

PHASE 6.5 may start when the checklist shows `gateStatus: PASS` and `automationStatus` is `active`.
