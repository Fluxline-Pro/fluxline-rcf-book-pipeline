# PHASE 1: Claude Markdown Script for each PASS 7-finished Chapter

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
    
11. Review all content in the Chapter for accuracy
		- Make suggested wording edits in the chapter
		- Spelling, grammar, punctuation per sentence ONLY without removing voice
		- Updates to references and footnotes as appropriate
		- Wording changes based on technicalities in describing referenced topics
		
12. Organize all outputs into the following folder structure:
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

13. Ensure all files follow naming format:
    <ChapterName>_<ArtifactType>.<ext>

14. Produce a final “Chapter Production Checklist” summarizing:
    - All artifacts created
    - All folders populated
    - Any missing elements
    - Suggested glossary terms marked with Chapter number (References: Ch 1)
    - Any recommended follow-up steps
    - All in a Markdown file