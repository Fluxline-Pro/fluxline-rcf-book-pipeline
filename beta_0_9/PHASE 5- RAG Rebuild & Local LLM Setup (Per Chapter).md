# PHASE 5: RAG Rebuild & Local LLM Setup (Per Chapter)

**Purpose:**  
Rebuild the chapter’s RAG ingestion surface using the *final, locked* PHASE 1–4 outputs, then configure your local LLM environment (Ollama / LM Studio) to use the updated RAG for grounded generation, marketing automation, and future n8n workflows.

This phase is run **per chapter**, after PHASE 4 is complete.

# **1. Gather All Final, Locked Chapter Outputs**

Pull ONLY from:

Code

```
/Documents/Books/RCF_FIRST_EDITION/RCF/Chapters/<ChapterName>/Final/
```

Include:

- Manuscript
- ReviewPacket
- Workbook
- Training
- ReferenceGuides
- Slides
- Audiobook
- Kindle (PHASE 4 DOCX + HTML blocks)
- InDesign
- DesignPacket
- Marketing (Intake + Seeds)
- Governance (GlossaryNormalized, Metadata, FigureRegistry)
- RAG (previous metadata, if any — for comparison only)

These are the authoritative, governed, design‑validated assets.

# **2. Build the Chapter’s RAG Ingestion Schema**

Generate a complete ingestion JSON for this chapter using the unified schema:

### Must include:

- chunk definitions
- semantic tags
- metadata
- glossary terms
- framework terms
- claims registry
- voice constraints
- terminology lock
- marketing intake fields
- marketing seed fields
- design metadata
- governance flags
- authority hierarchy
- version metadata
- artifact manifest

Save to:

Code

```
/Final/RAG/<ChapterName>_RAG_Ingestion.json
```

# **3. Chunk the Chapter for RAG Ingestion**

Chunk the manuscript + supporting materials using:

- **550–1000 word chunks**
- **80–120 word overlap**
- **semantic boundaries preserved**
- **section names included as metadata**
- **no concept split mid‑explanation**

Output to:

Code

```
/Final/RAG/Chunks/
```

# **4. Rebuild the ChromaDB Collection (Per Chapter or Global)**

### If rebuilding per chapter:

Create or update collection:

Code

```
collection_name = "rcf_book"
```

### Steps:

1. Delete old vectors for this chapter (if present).
2. Ingest new chunks.
3. Ingest new metadata.
4. Ingest new semantic tags.
5. Ingest new authority hierarchy.
6. Ingest new marketing fields.
7. Ingest new design fields.
8. Ingest new governance flags.

This ensures the RAG reflects the *final, locked* chapter.

# **5. Validate RAG Integrity**

Run a validation pass:

### Check:

- chunk count
- metadata completeness
- semantic tag coverage
- glossary normalization
- terminology lock alignment
- claims registry alignment
- voice constraints
- marketing safety
- design metadata
- figure registry alignment
- HTML readiness
- authority hierarchy
- version metadata

### Output:

Code

```
/Final/RAG/<ChapterName>_RAG_ValidationReport.md
```

# **6. Configure Local LLM Environment**

### Ollama:

- Ensure drafting model is installed (e.g., Qwen2.5 14B Instruct).
- Ensure embedding model is installed (e.g., nomic-embed-text).
- Confirm local server is running.

### LM Studio (optional):

- Load same model.
- Start local server for n8n access.

### Update system prompts:

- VoiceKit
- TerminologyLock
- Claims discipline
- Marketing rules
- Design rules
- Governance rules
- RAG query rules

Save to:

Code

```
/Final/RAG/<ChapterName>_LLM_SystemPrompt.md
```

# **7. Create Chapter-Level RAG Query Profiles**

Generate reusable query templates:

- “Explain this concept”
- “Generate social posts”
- “Generate Reddit drafts”
- “Generate newsletter excerpts”
- “Generate podcast kits”
- “Generate scripts”
- “Generate design prompts”
- “Generate HTML blocks”
- “Generate SEO articles”

Save to:

Code

```
/Final/RAG/<ChapterName>_RAG_QueryProfiles.md
```

# **8. Produce PHASE 5 Checklist**

Save as:

Code

```
/Final/<ChapterName>_PHASE5_RAGChecklist.md
```

Checklist includes:

- All ingestion files created
- All chunks generated
- All metadata validated
- All semantic tags applied
- All governance flags applied
- All marketing fields applied
- All design fields applied
- ChromaDB updated
- Local LLM configured
- Query profiles created
- Any missing elements
- Recommendations for PHASE 6 (automation activation)