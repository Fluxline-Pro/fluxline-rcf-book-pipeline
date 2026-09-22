# PHASE 1: Claude Markdown Script for each PASS 7-finished Chapter (v2)

**v2 changes:**
- NEW Step 11: "Marketing & Local LLM Intake Packet" (grounding files + seed drafts for the local LLM / n8n marketing workflow), saved in its own `/Marketing/` build folder.
- Folder structure, naming, and Production Checklist updated to include `/Marketing/`.
- NEW Run Mode: Retrofit mode, for chapters already built (Chapters 1–5), so nothing existing is regenerated or overwritten.
- Original Steps 1–10 are unchanged. Former Steps 11–14 are now Steps 12–15.

---

# RUN MODE (declare before starting)

**MODE A: New Chapter.** Run Steps 1–15 in full.

**MODE B: Retrofit (chapter already has Phase 1 outputs).** For Chapters 1–5:
- Do NOT regenerate, rewrite, or overwrite any existing artifact.
- Skip Steps 1–10 and Step 12.
- Run Step 11 (Marketing & Local LLM Intake Packet) in full.
- Run Step 13 (folder verification only: create the missing `/Marketing/` folders, touch nothing else).
- Run Step 15 as an **append**: add a "Marketing Addendum" section to the existing Chapter Production Checklist. Do not replace the file.

If the run mode is not stated, ask which one applies before doing anything.

---

# INPUT

You will receive a finalized PASS 7 manuscript for a single chapter of my book.
This manuscript is fully locked and ready for production. Using this chapter,
perform the following tasks and save all outputs into my Personal OneDrive
inside the folder: /Documents/Books/RCF_FIRST_EDITION/RCF/Chapters/<ChapterName>/.

Input chapters are located in:
   /Documents/Books/RCF_FIRST_EDITION/PASS7

1. Create a “Chapter Review Packet” containing:
   - A 1-page chapter summary
   - Key insights and takeaways
   - Glossary terms introduced or used
   - Important definitions
   - Frameworks or models referenced
   - Structured metadata JSON for CMS and RAG ingestion

2. Create a “Workbook Exercise Packet” containing:
   - The chapter’s main workbook exercise
   - Additional Practical Application exercises derived from the chapter
   - Reflection prompts
   - Application questions
   - A DOCX file formatted for workbook inclusion based on the complementary workbook exercise given as part of this prompt

3. Create “Training Materials” including:
   - Instructor notes
   - Teaching objectives
   - Discussion questions
   - Facilitation guide
   - Workshop or class training outline

4. Create multiple “One-Page Reference Guides”:
   - One guide per major topic in the chapter
   - Each guide includes:
       * Core concept breakdown
       * Key terms and definitions for the glossary
       * Visual or structured explanation
       * Practical application checklist

5. Create "Slide Deck” outlines containing:
   - Title slide
   - 8–20 slides summarizing the chapter
   - Visual breakdowns of major concepts
   - Key quotes or insights
   - Reflection questions
   - Headings, subheadings, body text, suggested images and/or infographics 
   - These will be given to Claude Design later to create as HTML, exported as PPTX and PDF

6. Create an “XLSX Equation Sheet” ONLY IF the chapter contains:
   - Scoring systems
   - Equations
   - Models requiring calculation
   - Include example calculations and editable cells

7. Create “Kindle/eBook Prep Files” including:
   - Clean HTML blocks for the chapter
   - EPUB-friendly formatting
   - Chapter metadata
   - TOC entries

8. Create “InDesign Prep Files” including:
   - Clean text blocks for layout
   - Pull quotes
   - Section headers
   - Sidebar summaries
   - Layout notes
   - 2-3 suggested Figures for infographic designs to include in the chapter
   - Suggested chapter design layout spreads based on InDesign Templates for the chapter flow
   - These will be given to Claude Design to review and create mockups

9. Create “Audiobook/XTTS Prep Files” including:
   - Narration script
   - Pronunciation guide
   - Segment markers
   - Pacing notes
   - Full transcript of the chapter in MD format

10. Create “RAG/ChromaDB Ingestion Packet” including:
    - Chunked text blocks
    - Embeddings-ready text
    - Metadata JSON
    - Semantic tags
    - Summary blocks for retrieval

---

## 11. Create the “Marketing & Local LLM Intake Packet” (NEW)

**Purpose:** Produce verified, grounded source material that my local LLM (Ollama / LM Studio, orchestrated through n8n) uses to generate marketing content for the RCF book, the Resonant Identity Podcast, the audiobook, and Resonance. This packet is *intake and seed material*. It does not publish anything. The local model writes final copy from it, and I approve every piece before it goes out.

**Source rule:** Use ONLY the PASS 7 manuscript and the artifacts already generated in Steps 1–10. Do not add outside facts, statistics, research, credentials, testimonials, reviews, or endorsements.

Save everything in:
`/Documents/Books/RCF_FIRST_EDITION/RCF/Chapters/<ChapterName>/Marketing/`
with three subfolders: `/Intake/`, `/Seeds/`, `/Trigger/`.

### 11A. Intake files (grounding layer) → `/Marketing/Intake/`

1. **`<ChapterName>_MKT_ChapterContext.md`**
   - Compressed chapter context, **maximum 2,000 words** (it must fit a local 8k-token window alongside a voice kit and a task prompt).
   - Includes: chapter thesis, major concepts with one-sentence definitions in my wording, framework structure, key examples or stories, and where the chapter sits in the book (Part / Lesson / Core Value).
   - Tag each block with its manuscript section name.

2. **`<ChapterName>_MKT_ClaimsRegistry.md`**
   - Table: Claim ID | Claim (in my terms) | Manuscript section | Verbatim support (under 25 words) | Use level (`Safe to state` / `Attribute to the book`).
   - A **"Do Not Claim" list** for this chapter: guaranteed outcomes, clinical, therapeutic, or medical claims, statistics not in the manuscript, fabricated testimonials, credentials not in the manuscript, and any claim that stretches the chapter's actual scope.
   - Purpose: stop the local model from drifting or inventing.

3. **`<ChapterName>_MKT_VoiceNotes.md`**
   - Chapter-specific voice guidance: cadence, recurring metaphors (architectural and mythic-human where used), and terms that must remain exact.
   - Phrases to avoid: corporate softening, over-explanation, generic self-help clichés, filler.
   - **3 short verbatim sample passages** (each under 120 words) chosen as few-shot examples of my voice.

4. **`<ChapterName>_MKT_TerminologyLock.json`**
   - Every framework term used in the chapter, with exact casing as it appears in the manuscript, approved aliases, and forbidden substitutes.
   - Framework terms (RCF, Behavioral Gravity, Identity Coherence, Window of Choice, DRIVEs, Distortion, Truth, and any chapter-specific terms) must be taken from the manuscript, not assumed.
   - Never restate scoring rubrics, equations, or numeric scales unless copied verbatim from the manuscript.

5. **`<ChapterName>_MKT_AudienceMap.md`**
   - Which audiences this chapter serves (self-development readers, coaches and somatic practitioners, leaders and L&D professionals, systems thinkers, podcast hosts).
   - For each: the question or pain the chapter answers.
   - **3 pitch angles** for podcast guesting, each 2–3 sentences.
   - **10–15 real search-style questions** people would ask that this chapter answers, each mapped to a manuscript section (for SEO and transcript pages).

6. **`<ChapterName>_MKT_Metadata.json`**
   - chapterNumber, chapterTitle, part, lesson, coreValue, topics, glossaryTerms, audiences, channelFit, estimatedContextWords, assetList, and status.

### 11B. Seed files (starter drafts) → `/Marketing/Seeds/`

All seeds are `status: draft`. The local LLM refines them; I approve them.

1. **`<ChapterName>_MKT_PullLines.md`**: 12–15 pull-lines, **verbatim** from the manuscript, each under 40 words. For each: manuscript section, word count, standalone-clarity rating (High / Medium), and best-use tags (quote card, newsletter, podcast, audiobook teaser).
2. **`<ChapterName>_MKT_FrameworkCards.md`**: one card per major concept: name, one-sentence definition, 3 key points, "when it applies," chapter reference, suggested visual.
3. **`<ChapterName>_MKT_NewsletterExcerpt.md`**: a 350–500 word excerpt-style piece in my voice, 3 subject-line options, and a `[CTA: set at launch]` placeholder.
4. **`<ChapterName>_MKT_PodcastEpisodeKit.md`**: episode hook (2–3 sentences), 6–8 talking points, 8-question guest/host bank, show-notes draft, segment outline (no timestamps), and an SEO article outline with H2s written as questions.
5. **`<ChapterName>_MKT_ShortScripts.md`**: 3 scripts of about 60 seconds each (hook → concept → one practice → soft close), suitable for audio or video.
6. **`<ChapterName>_MKT_PitchKit.md`**: 3 podcast-guest pitch paragraphs, 1 practitioner outreach hook, 1 ARC reader blurb (60 words maximum), and target-fit tags. No invented credentials, quotes, or social proof.
7. **`<ChapterName>_MKT_AudiobookTeasers.md`**: 2 candidate 60–90 second excerpts, referencing the segment markers and pacing notes from Step 9 so they can be rendered with XTTS without rework.
8. **`<ChapterName>_MKT_LeadMagnetCandidate.md`**: only if a fitting one-page tool exists. Reference the existing Workbook or Reference Guide file rather than creating new content. If none fits, write a one-line note saying so.

### 11C. Frontmatter (every file in `/Marketing/`)

```yaml
---
chapter: <ChapterName>
chapterNumber: <N>
artifactType: <MKT_...>
status: draft
sourceSections: [<section names>]
voiceCheck: pending
generated: <YYYY-MM-DD>
---
```

### 11D. Book-level voice kit (create only if missing)

- Check for `/Documents/Books/RCF_FIRST_EDITION/RCF/_BookMarketing/VoiceKit.md`.
- If it does not exist, create it from this chapter's VoiceNotes and TerminologyLock.
- If it exists, **do not overwrite it.** Write proposed additions to `<ChapterName>_MKT_VoiceKitProposals.md` in `/Marketing/Intake/` for my review.

### 11E. Trigger file (created LAST)

- Only after every file above exists and passes the rules below, create `/Marketing/Trigger/MARKETING_READY.md` listing all files, the chapter number, and a timestamp. My n8n workflow watches for this file.
- If anything required is missing or fails a rule, create `MARKETING_INCOMPLETE.md` listing exactly what is missing, and do NOT create `MARKETING_READY.md`.

### 11F. Rules for the Marketing packet

- Verbatim quotes must match the manuscript exactly, including punctuation.
- No outcome promises, no medical, therapeutic, or diagnostic claims, and no fabricated statistics, testimonials, reviews, or endorsements.
- Terminology must match the TerminologyLock exactly.
- Voice: precision-first, architectural metaphor where the manuscript uses it, no corporate softening, no filler.
- Pull-lines stay under 40 words each. Do not reproduce large passages of the chapter in any marketing asset.
- The whole Intake set should stay within roughly 6,000 words, and each file must be usable on its own within an 8k context window.
- Every claim in a seed file must trace to the ClaimsRegistry or to a verbatim manuscript line.

---

## 12. Review all content in the Chapter for accuracy
		- Make suggested wording edits in the chapter
		- Spelling, grammar, punctuation per sentence ONLY without removing voice
		- Updates to references and footnotes as appropriate
		- Wording changes based on technicalities in describing referenced topics

*(Formerly Step 11. In Mode B, skip this step.)*

## 13. Organize all outputs into the following folder structure:
    /Documents/Books/RCF_FIRST_EDITION/RCF/Chapters/<ChapterName>/
        /Manuscript/
        /ReviewPacket/
        /Workbook/
        /Training/
        /ReferenceGuides/
        /Slides/
        /Equations/
        /Kindle/
        /InDesign/
        /Audiobook/
        /RAG/
        /Marketing/
            /Intake/
            /Seeds/
            /Trigger/

## 14. Ensure all files follow naming format:
    <ChapterName>_<ArtifactType>.<ext>

(Marketing files use the `<ChapterName>_MKT_<Type>.<ext>` form, which satisfies this format.)

## 15. Produce a final “Chapter Production Checklist” summarizing:
    - All artifacts created
    - All folders populated
    - Any missing elements
    - Suggested glossary terms marked with Chapter number (References: Ch 1)
    - Any recommended follow-up steps
    - All in a Markdown file

**Marketing additions to the checklist (both modes):**
- Every Marketing file listed with its status
- Count of claims in the ClaimsRegistry and count of pull-lines
- Confirmation that every pull-line was verified verbatim against the manuscript
- Estimated word count of `ChapterContext.md` (must be 2,000 or fewer)
- Trigger status: `MARKETING_READY` or `MARKETING_INCOMPLETE`
- Any VoiceKit proposals awaiting my review

In Mode B, append this as a "Marketing Addendum" section to the existing checklist file rather than creating a new one.
