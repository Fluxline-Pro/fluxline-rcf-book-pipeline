# PHASE 6: Automation Activation (n8n + Local LLM + RAG + OpenClaw) (v3)

> **Pipeline position:** PHASE 6 of 7 (Automation) · **Upstream gate:** `RAG/Trigger/RAG_READY.md` exists · **Downstream:** PHASE 6.5 Publication QA
> **Canonical paths, status ladder, triggers, and deliverables:** see `MASTER_PIPELINE_OVERVIEW.md`.

**v3 changes (2026-09-22 pipeline alignment):**
- AutomationIndex moved from `/KnowledgeBase/Automation/` to the book root: `<BOOK_ROOT>/_BookAutomation/AutomationIndex.json`.
- n8n workflow exports and OpenClaw pipeline definitions now have fixed homes, since both are required deliverables.
- OpenClaw pipelines are now **required** (previously "optional"), matching the deliverable map.
- Every trigger this phase listens for is now created by an earlier phase (`MARKETING_READY` → PHASE 1/2, `GOVERNANCE_READY` → PHASE 2, `DESIGN_READY` → PHASE 3.5, `RAG_READY` → PHASE 5).
- Adds the human approval gate: automations generate drafts. Nothing publishes, schedules live posts, or overwrites `Final/` files without <AUTHOR>'s approval.

---

**Purpose:**
Activate the automation ecosystem for the chapter using the rebuilt RAG (PHASE 5), the locked PHASE 1–4 outputs, and the local LLM environment. This phase enables:

- automated marketing drafts
- automated design drafts (inputs to Claude Design, never replacements for DSM output)
- automated governance checks (report-only)
- automated metadata consistency checks
- content calendar drafts (scheduling needs approval)
- chapter-level and multi-chapter batch workflows

Run **per chapter**, or in batch mode once multiple chapters have `RAG_READY.md`.

## Deliverables (PHASE 6)

| Deliverable | Path |
|---|---|
| N8N_AUTOMATIONS | `/_BookAutomation/n8n/<BOOK>_<WorkflowName>.json` (exported, chapter-parameterized workflows) |
| OpenClaw pipelines | `/_BookAutomation/OpenClaw/<BOOK>_<PipelineName>.yaml` (or `.json` — pick one format and use it for every pipeline) |
| AutomationIndex.json | `/_BookAutomation/AutomationIndex.json` |
| ActivationReport | `<CH_ROOT>/<ChapterName>_PHASE6_ActivationReport.md` |
| Checklist | `<CH_ROOT>/<ChapterName>_PHASE6_AutomationChecklist.md` |
| Automation drafts (outputs) | `<CH_ROOT>/Marketing/Generated/<YYYYMMDD>/` (all `status: draft`) |

`/_BookAutomation/` = `<BOOK_ROOT>/_BookAutomation/`

## Approval rule (applies to every workflow)

- Generated content is written with `status: draft`, `voiceCheck: pending`.
- Only <AUTHOR> moves an item to `approved`. Only approved items may be scheduled or published.
- Automations never edit the manuscript and never overwrite files in `Final/` outside `Marketing/Generated/`. Governance automations report; they do not fix.

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
    "ragReady": "<CH_ROOT>/RAG/Trigger/RAG_READY.md"
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

Status values: `inactive` → `active` → `batch-ready`. New entries start `inactive`.

# 2. Load the chapter's RAG profile into n8n

Import:

- `<ChapterName>_RAG_Ingestion.json`
- `<ChapterName>_RAG_QueryProfiles.md`
- `<ChapterName>_LLM_SystemPrompt.md`

These are the grounding layer for every automation.

# 3. Activate n8n chapter workflows

### 3A. Marketing automation (drafts)
Social posts · Reddit drafts · Newsletter excerpts · Podcast kits · Short scripts · Audiobook teasers · Image prompts · SEO articles · Content calendar

### 3B. Design automation (drafts only)
HTML slide deck drafts · HTML training drafts · HTML one-pager drafts · Infographic prompts · Layout suggestions
→ Outputs are input material for Claude Design. Anything that would enter `DesignPacket/` goes through PHASE 3 and 3.5.

### 3C. Governance automation (report-only)
Claims validation · Terminology validation · Metadata consistency · Voice consistency · Marketing safety · Figure registry alignment · Glossary normalization checks

### 3D. Publishing automation (checks)
Kindle DOCX validation · EPUB readiness · InDesign asset presence · PDF export checks

### 3E. Knowledge system automation
RAG query testing · RAG semantic map updates · CMS ingestion (drafts) · LMS ingestion (drafts)

### Triggers

| Trigger | Created by | Starts |
|---|---|---|
| `MARKETING_READY.md` | PHASE 1 / PHASE 2 | 3A |
| `GOVERNANCE_READY.md` | PHASE 2 | 3C |
| `DESIGN_READY.md` | PHASE 3.5 | 3B, 3D |
| `RAG_READY.md` | PHASE 5 | 3E, and enables all others |
| daily cron / weekly cron / manual | n8n | per workflow |

A trigger only fires workflows for chapters whose `automationStatus` is `active` or `batch-ready`.

Export every activated workflow to `/_BookAutomation/n8n/` and list it in the chapter's `n8nWorkflows`.

# 4. Connect the local LLM to n8n

**Ollama:** drafting model endpoint · embedding model endpoint (same model as PHASE 5) · system prompt injection · RAG query injection · marketing, design, and governance rules

**LM Studio (optional):** OpenAI-compatible endpoint · multi-step reasoning · long-form generation · design packet integration

# 5. Activate OpenClaw pipelines

Define each pipeline in `/_BookAutomation/OpenClaw/` and list it in the chapter's `openClawPipelines`:

- **5A. Multi-asset marketing:** pull-lines → social → newsletter → SEO → scripts → podcast kit
- **5B. Multi-asset design:** design packet → HTML drafts → figure prompts → layout notes
- **5C. Multi-asset governance:** metadata → glossary → claims → terminology → voice → RAG
- **5D. Multi-asset publishing checks:** Kindle → EPUB → PDF → InDesign → LMS → CMS

OpenClaw handles multi-step reasoning and multi-agent workflows; the approval rule above applies to every step.

# 6. Run the chapter activation test

**Test 1 — RAG query:** "Explain the chapter's thesis." · "Generate 3 social posts." · "Generate 1 Reddit draft." · "Generate 1 design prompt."

**Test 2 — n8n workflow:** trigger the Social, Newsletter, Design, and Governance workflows.

**Test 3 — LLM grounding:** no hallucinations · no claim drift (every claim traces to the ClaimsRegistry) · no terminology drift · voice consistency · design consistency

**Test 4 — Publishing:** Kindle DOCX integrity · HTML readiness · EPUB safety

**Test 5 — Approval rule:** confirm every output landed as `status: draft` in `Marketing/Generated/` and nothing was published or scheduled.

Save results (pass/fail per test, sample outputs, issues) to `<CH_ROOT>/<ChapterName>_PHASE6_ActivationReport.md`.

# 7. Mark the chapter "Automation Active"

Only if Tests 1–5 pass, set `"automationStatus": "active"` and `lastActivationTest` in `AutomationIndex.json`.

# 8. Produce PHASE 6 checklist

Save `<CH_ROOT>/<ChapterName>_PHASE6_AutomationChecklist.md`:

- RAG loaded
- LLM connected
- n8n workflows activated and exported
- OpenClaw pipelines defined and activated
- Automation index updated
- Activation tests passed
- Any missing elements
- Recommendations for batch mode
- `gateStatus: PASS | FAIL`

## PHASE 6 exit gate

PHASE 6.5 may start when the checklist shows `gateStatus: PASS` and `automationStatus` is `active`.
