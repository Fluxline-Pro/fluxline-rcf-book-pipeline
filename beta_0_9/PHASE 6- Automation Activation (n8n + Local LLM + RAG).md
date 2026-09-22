# PHASE 6: Automation Activation (n8n + Local LLM + RAG + OpenClaw)

**Purpose:**  
Activate the full automation ecosystem for the chapter using the rebuilt RAG (PHASE 5), the locked PHASE 1–4 outputs, and your local LLM environment. This phase enables:

- automated marketing generation
- automated design generation
- automated governance checks
- automated metadata updates
- automated content scheduling
- automated chapter‑level workflows
- automated multi‑chapter batch workflows

PHASE 6 is run **per chapter**, but can also be run in batch mode once multiple chapters are locked.

# **1. Register the Chapter in the Automation Index**

Add the chapter to your global automation index:

Code

```
/RCF_KnowledgeBase/Automation/AutomationIndex.json
```

Include:

- chapterName
- chapterNumber
- folderPath
- RAG ingestion path
- LLM system prompt path
- n8n workflow paths
- automation status (“inactive”, “active”, “batch-ready”)

This allows n8n and OpenClaw to discover the chapter automatically.

# **2. Load the Chapter’s RAG Profile into n8n**

Import:

- `<ChapterName>_RAG_Ingestion.json`
- `<ChapterName>_RAG_QueryProfiles.md`
- `<ChapterName>_LLM_SystemPrompt.md`

These become the grounding layer for all automations.

# **3. Activate n8n Chapter Workflows**

Enable the following workflows:

### **3A. Marketing Automation**

- Social post generator
- Reddit draft generator
- Newsletter excerpt generator
- Podcast kit generator
- Short script generator
- Audiobook teaser generator
- Image prompt generator
- SEO article generator
- Content calendar generator

### **3B. Design Automation**

- HTML slide deck generator
- HTML training material generator
- HTML one‑pager generator
- Infographic prompt generator
- Layout suggestion generator

### **3C. Governance Automation**

- claims validation
- terminology validation
- metadata consistency checks
- voice consistency checks
- marketing safety checks
- figure registry alignment
- glossary normalization checks

### **3D. Publishing Automation**

- Kindle DOCX validation
- EPUB readiness checks
- InDesign asset checks
- PDF export checks

### **3E. Knowledge System Automation**

- RAG query testing
- RAG semantic map updates
- CMS ingestion
- LMS ingestion

Enable triggers:

- `MARKETING_READY.md`
- `DESIGN_READY.md`
- `GOVERNANCE_READY.md`
- daily cron
- weekly cron
- manual run

# **4. Connect Local LLM to n8n**

Configure:

### **Ollama**

- drafting model endpoint
- embedding model endpoint
- system prompt injection
- RAG query injection
- marketing rules
- design rules
- governance rules

### **LM Studio (optional)**

- OpenAI‑compatible endpoint
- multi‑step reasoning
- long‑form generation
- design packet integration

This ensures n8n can call your local LLM for grounded generation.

# **5. Activate OpenClaw Pipelines (Optional but Recommended)**

Enable multi‑step pipelines:

### **5A. Multi‑Asset Marketing Pipeline**

- pull-lines → social → newsletter → SEO → scripts → podcast kit

### **5B. Multi‑Asset Design Pipeline**

- design packet → HTML → figure prompts → layout notes

### **5C. Multi‑Asset Governance Pipeline**

- metadata → glossary → claims → terminology → voice → RAG

### **5D. Multi‑Asset Publishing Pipeline**

- Kindle → EPUB → PDF → InDesign → LMS → CMS

OpenClaw handles multi‑step reasoning and multi‑agent workflows.

# **6. Run Chapter Activation Test**

Perform a full test run:

### **Test 1 — RAG Query**

Ask:

- “Explain the chapter’s thesis.”
- “Generate 3 social posts.”
- “Generate 1 Reddit draft.”
- “Generate 1 design prompt.”

### **Test 2 — n8n Workflow**

Trigger:

- Social workflow
- Newsletter workflow
- Design workflow
- Governance workflow

### **Test 3 — LLM Grounding**

Verify:

- no hallucinations
- no claim drift
- no terminology drift
- voice consistency
- design consistency

### **Test 4 — Publishing**

Verify:

- Kindle DOCX integrity
- HTML readiness
- EPUB safety

Save results to:

Code

```
/Final/<ChapterName>_PHASE6_ActivationReport.md
```

# **7. Mark Chapter as “Automation Active”**

Update:

Code

```
AutomationIndex.json
```

Set:

Code

```
"automationStatus": "active"
```

This signals that the chapter is now fully integrated into your automation ecosystem.

# **8. Produce PHASE 6 Checklist**

Save as:

Code

```
/Final/<ChapterName>_PHASE6_AutomationChecklist.md
```

Checklist includes:

- RAG loaded
- LLM configured
- n8n workflows activated
- OpenClaw pipelines activated
- automation index updated
- activation tests passed
- any missing elements
- recommendations for batch mode