# PHASE 4: Kindle DOCX Chapter Compilation (Updated)

**Purpose:**  
Transform the fully governed, design‑validated, PHASE 1–3.5 chapter outputs into a **Kindle‑ready DOCX** for *that chapter only*, using the final folder structure as the authoritative source of truth.

**Source Location:**

Code

```
/Books/RCF_FIRST_EDITION_FINAL/Chapters/<ChapterName>/Final/
```

**Output Location:**

Code

```
/Books/RCF_FIRST_EDITION_FINAL/Chapters/<ChapterName>/Final/Kindle/<ChapterName>_Kindle.docx
```

## **Pull from the** `eBook` **Folder (HTML Blocks + EPUB‑Ready Content)**

In addition to the Final Manuscript and DesignPacket assets, PHASE 4 must also ingest the chapter’s **eBook** folder:

**Source:**

Code

```
/Documents/Books/RCF_FIRST_EDITION/RCF/Chapters/<ChapterName>/Final/eBook/
```

**Purpose:**  
The `eBook` folder contains **clean HTML blocks**, **EPUB‑friendly formatting**, and **chapter‑level metadata** generated during PHASE 3. These files serve as the structural backbone for Kindle conversion and must be incorporated into the DOCX.

**Include the following from the eBook folder:**

1. **HTML Content Blocks**
    - Section‑by‑section HTML
    - Clean semantic tags
    - Kindle‑safe inline formatting
    - Paragraph and heading hierarchy
    - Embedded callout structures
    - Figure anchors and captions
2. **EPUB‑Friendly Formatting**
    - `<h1>`, `<h2>`, `<h3>` mapped to DOCX Heading styles
    - `<p>` mapped to DOCX Body style
    - `<blockquote>` mapped to DOCX Quote style
    - `<figure>` placeholders mapped to DOCX Caption style
    - `<aside>` mapped to DOCX Sidebar or Callout style
3. **Metadata Blocks**
    - TOC entries
    - Section anchors
    - Chapter metadata
    - Figure metadata
    - Accessibility tags (alt text, ARIA roles)
4. **Design‑Aligned HTML Components**
    - DSM‑derived components (callouts, tips, summaries)
    - Visual placeholders
    - Structured layout notes

**Integration Instructions:**

- Convert each HTML block into DOCX content using the global style map.
- Preserve semantic hierarchy (H1 → Chapter Title, H2 → Major Sections, H3 → Subsections).
- Insert figure placeholders where `<figure>` tags appear.
- Maintain EPUB‑safe spacing, indentation, and callout formatting.
- Ensure all HTML components are transformed into Kindle‑friendly DOCX equivalents.

**Result:**  
The final DOCX will contain:

- Manuscript text
- Design‑validated structure
- Figure placeholders
- Reference guides
- Workbook practice section
- Marketing exploration section
- **AND the fully structured HTML backbone from the eBook folder**

This ensures the DOCX is **100% Kindle‑ready**, **EPUB‑safe**, and consistent with your DSM + DesignPacket.

## **1. Gather all final chapter assets (PHASE 1–3.5)**

Pull ONLY from the `Final/` folder:

- Manuscript (clean text blocks)
- ReviewPacket (summary, definitions, glossary terms)
- ReferenceGuides (concept breakdowns)
- Workbook (exercise text only, no DOCX formatting)
- Training (instructor notes, objectives)
- Slides (semantic HTML outline, not images)
- Audiobook (narration script, segment markers)
- InDesign (pull quotes, section headers, sidebar summaries)
- DesignPacket (figure prompts, layout notes)
- Marketing (pull-lines, framework cards, newsletter excerpt)
- Governance (normalized glossary, metadata, figure registry)

These are the **final, locked** assets.

## **2. Normalize all text for DOCX ingestion**

Apply consistent formatting:

- Heading levels (H1 → Chapter Title, H2 → Major Sections, H3 → Subsections)
- Paragraph spacing
- Indentation
- Lists
- Quotes
- Callouts
- Figure references
- Section breaks

Ensure all text is **EPUB‑safe** and **Kindle‑friendly**.

## **3. Insert chapter front matter**

Include:

- Chapter title
- Chapter number
- Part / Lesson / Core Value
- Short chapter summary (from ReviewPacket)
- Optional: 1–2 pull‑quotes (from InDesign Packet)

## **4. Insert main manuscript body**

Use the **Manuscript** folder as the authoritative source.

- Preserve section hierarchy
- Preserve semantic breaks
- Preserve inline emphasis
- Insert figure placeholders where referenced
- Insert captions from DesignPacket or Governance FigureRegistry

## **5. Insert supporting materials**

### **5A. Reference Guides**

Add as end‑of‑chapter “Concept Cards.”

### **5B. Workbook Exercise**

Add as “Practice Section” at the end of the chapter.

### **5C. Training Notes**

Add as “Instructor Notes” appendix (optional).

### **5D. Marketing Seeds (optional)**

Add a “Further Exploration” section containing:

- 1–2 pull‑lines
- 1 framework card
- Newsletter excerpt (shortened)

This is optional but helpful for Kindle readers.

## **6. Insert figures and images**

From:

- DesignPacket (figure prompts → convert into captions)
- InDesign Packet (figure suggestions)
- Governance FigureRegistry (titles, descriptions)

If actual images exist, insert them.
If not, insert **image placeholders** with captions.

## **7. Apply global DOCX styles**

Use consistent styles:

- Title
- Heading 1
- Heading 2
- Heading 3
- Body
- Quote
- Caption
- Callout
- Sidebar

Ensure styles are Kindle‑friendly.

## **8. Generate Kindle‑friendly structure**

Produce:

- Clean HTML blocks (embedded in DOCX)
- EPUB‑safe formatting
- TOC entries
- Chapter metadata
- Section anchors
- Figure anchors

This ensures the DOCX can be converted to EPUB/AZW3 later.

## **9. Save final DOCX**

Save as:

Code

```
<ChapterName>_Kindle.docx
```

To:

Code

```
/Documents/Books/RCF_FIRST_EDITION/RCF/Chapters/<ChapterName>/Final/Kindle/
```

## **10. Produce PHASE 4 Checklist**

Save as:

Code

```
<ChapterName>_PHASE4_KindleChecklist.md
```

Checklist includes:

- All assets gathered
- All sections included
- Figures inserted or placeholders added
- Styles applied
- TOC generated
- Metadata added
- DOCX saved
- Any missing elements
- Recommendations for PHASE 5 (RAG rebuild)