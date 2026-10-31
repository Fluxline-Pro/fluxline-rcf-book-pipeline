# PHASE 3: CLAUDE DESIGN HAND-OFF (v3.2)

> **Pipeline position:** PHASE 3 of 7 (Design + Production) · **Upstream gate:** `Governance/Trigger/GOVERNANCE_READY.md` exists **and** `Manuscript/Trigger/MANUSCRIPT_LOCKED.md` is current (PHASE 2.5, v1.2.5) · **Downstream:** PHASE 3.5 Design QA
> **Canonical paths, status ladder, triggers, and deliverables:** see `MASTER_PIPELINE_OVERVIEW.md`.

**Release v1.2.5 (2026-10-24): PHASE 3 starts from the manuscript lock.** The chapter's content audit now runs before design, in PHASE 2.5. PHASE 3 needs a **current** `Manuscript/Trigger/MANUSCRIPT_LOCKED.md`: it exists, the DOCX and MD hashes it records match the files, and no `MANUSCRIPT_REVISED.md` section is newer. If the lock is missing or stale, stop, write nothing, and tell <AUTHOR> to finish PHASE 2.5 (or its delta audit). A0 now starts when the lock is written, not when `GOVERNANCE_READY.md` is.

**Release v1.2.1 (2026-10-22): PHASE 3 starts automatically when PHASE 2 passes.** When `Governance/Trigger/GOVERNANCE_READY.md` is issued, the automation:
1. writes the chapter's **figure prompts and figure checklist** (A0);
2. builds the **design packet** as Claude artifacts from the packet DSM (A2b).

<AUTHOR> makes the figures (AI tool, then Photoshop for the RGB and CMYK files) and approves the packet.

**Design packet as Claude artifacts (2026-10-22).** The design packet no longer needs a separate Claude Design project. Claude builds each A2 output as an individual artifact from a design packet DSM (`<PACKET_DSM_ROOT>`) made once from a finished chapter's DesignPacket. See **A2b**. The Part B prompt remains the design brief.

**Release v1.2 (2026-10-22): eBook first, then print IDML.** The chapter's eBook page is built first. PHASE 3.5B then generates the print IDMLs (chapter and workbook exercise) that replicate it, and <AUTHOR> finishes them in InDesign. See `PHASE 3.5B- eBook-First Print Build (IDML).md`.

**Release v1.1.3 (2026-10-21): print build.** The print layout track (A3) now starts from a generated, styled import: PHASE 3.5A writes `InDesign/<ChapterName>_Import.txt` from the manuscript DOCX and the print template, and <AUTHOR> finishes the layout by hand. `Ch<N>_Print7x10.dc.html` is still the design reference.

**v3.2 changes (2026-09-30 workbook track):** the workbook is tracked in `PHASE 3W- Workbook Track (eBook + Print).md`.
- Claude Design still builds the workbook, now from the workbook manuscript, and only once `Workbook/Trigger/WORKBOOK_MANUSCRIPT_READY.md` exists.
- <AUTHOR> produces the eBook (8.5×11 in) and full-color print (7×10 in) PDFs in InDesign from it, and uploads them to `Workbook/`.
- The HTML-built workbook eBook (`Workbook_Master.html` → PDF/EPUB) is gone.

**v3.1 changes (2026-09-27 audiobook timing):** the audiobook and the `<BOOK>_AUDIOBOOK` set moved to **PHASE 4 Part C / Part B**. <AUTHOR> can still change wording in the eBook and print InDesign books, and the audiobook is recorded from the Kindle output built after that. XTTS makes a draft there, and <AUTHOR> records the final narration in Adobe Audition. PHASE 3 keeps the narration script and pronunciation guide from PHASE 1 as they are.

**v3 changes (2026-09-22 pipeline alignment):**
- Adds the operator section (inputs, outputs, folders, production tracks, book assembly, exit gate). The Claude Design System Prompt below is unchanged except for one clarification that PDF/PPTX/EPUB are exported *from* the HTML.
- **Kindle decision (2026-09-22):** PHASE 3 no longer produces a Kindle edition. PHASE 3 finishes the DesignPacket, the figures, and the manual print and eBook layouts; **all Kindle work happens in PHASE 4**, chapter by chapter, from those finished assets. PHASE 3 therefore has one new required output: exported figure image assets, which PHASE 4 needs.
- Names the DSM location and the `/DesignPacket/` layout already in use for Chapters 1–3.
- Defines where the six book-level deliverables are produced and stored.

---

# PART A — OPERATOR INSTRUCTIONS (for <AUTHOR> / Claude Cowork)

## A0. Automatic start: figure prompts, then the design packet (release v1.2.1)

**Trigger:** `Manuscript/Trigger/MANUSCRIPT_LOCKED.md` is issued (PHASE 2.5 passed, Locked; v1.2.5), with `Governance/Trigger/GOVERNANCE_READY.md` in place. Before v1.2.5 the trigger was `GOVERNANCE_READY.md` alone. The runner starts PHASE 3 for the chapter. A protected chapter runs these steps with Claude in chat instead.

**Condensed DSM cards (v1.3.0).** Whenever it builds or refreshes the design packet, Claude also writes one-page cards for the Copilot handoffs: `DesignPacket/_ds/DSM_CopilotCard.md` (eBook: palette hex values and roles, type scale, spacing, callouts, pull quotes, figure and caption rules, do/don't) and `DesignPacket/_ds/PRINT_DSM_CopilotCard.md` (print equivalents, copied from `<PRINT_DSM_ROOT>`; nothing is written into the print DSM folder). They are copied from the DSM, never invented, and carry the DSM version. The Copilot handoffs upload these cards, not the full design system.

**Step 1: figure prompts and checklist (automatic).**
- Write `<CH_ROOT>/Figures/<ChapterName>_FigurePrompts.md` and create `Figures/RGB/`, `Figures/CMYK/`, and `Figures/Drafts/` if missing. An existing prompts file is backed up and updated, never overwritten blindly: keep <AUTHOR>'s notes and any revised prompts.
- **Sources:** the FigureRegistry (number, title, caption, spec, accents), the manuscript (exact labels, line numbers), and the book's figure house style (taken from the last finished chapter's prompts file).
- **Per figure, the file carries:**
  - the manuscript lines and the exact caption;
  - a **prompt for Google Gemini** (also usable in Firefly);
  - **optionally, a Microsoft Copilot image handoff** (v1.3.0): if <AUTHOR> wants to make the figure with Copilot Create, write `Figures/Copilot/<FigureID>_CopilotHandoff.md` from `COPILOT_HANDOFFS/COPILOT_PHASE3_IMAGE_GENERATION.md`, filled with the passage, the condensed Visual DSM, the registry row, the terminology lock, placement and size, and the prohibited imagery. <AUTHOR> carries it to Copilot; nothing here invokes Copilot. Copilot's three fixed sizes (up to 1536 px) are below the 2400 px rule below: its images are **RGB concepts** to refine or redraw, never final files;
  - a **no-text fallback** (labels set afterwards in Express or InDesign);
  - a **check against the manuscript**: what must be true of the image;
  - the **save-as names** for both files.
- **Rules for every prompt:**
  - every label is the manuscript's exact wording;
  - the house style is followed;
  - output is at least 2400 px wide (6.5 in at 300 ppi or more);
  - the title is never in the image, because the caption is set in the layout;
  - no faces, clip art, or stock-photo look.
- **Figure suggestions.** List, separately, figures the chapter does *not* have but would benefit from. Each suggestion gives its manuscript location and a one-line reason, and is marked **Suggested, not in the registry**. A suggestion becomes a figure only when <AUTHOR> approves it; then it goes through the registry, PHASE 2, and the manuscript (a caption and a reference). Never add one on your own.
- **Figure checklist** at the top of the file: what <AUTHOR> must create in Photoshop, one row per figure, both formats:

  | Figure | RGB master (eBook, Kindle) | CMYK print file | Status |
  |---|---|---|---|
  | Fig N: Title | `Figures/RGB/Ch<N>_Fig<#>_<Name>.png` (PNG for illustrations, JPG for photos), sRGB, ≥ 2400 px wide | `Figures/CMYK/Ch<N>_Fig<#>_<Name>.tif`, CMYK, 300 ppi at the placed width (6.5 in ≥ 1950 px), LZW, flattened | to make / draft / final |

- **Photoshop steps** in the file, once: open the final RGB master, then Edit → Convert to Profile → the print profile used for the earlier chapters' TIFFs; check that the image is ≥ 300 ppi at its placed size; flatten; save as TIFF (LZW, no layers).
- **After <AUTHOR> makes them:** check each against the manuscript, then update the FigureRegistry: status, final file paths (`imagePath` RGB, `printImagePath` CMYK), the **tool used** (AI disclosure rule), and alt text. For a figure made with Copilot (or any generator), also fill the provenance fields (`generator`, `promptVersion`, `dsmVersion`, `generatedOn`, `aiGenerated: true`, `approval: pending`, `colorMode`, `resolutionStatus`, `rights`, `revisionHistory`), keep every draft in `Figures/Drafts/`, and put Copilot's alt-text, long description and rationale drafts in the registry for <AUTHOR> to edit. A generated image is never canonical and never `approved` here: it goes through PHASE 3.5 and <AUTHOR>'s approval. Never add a label, term or number to a figure that the manuscript does not contain. Figures must be final before the eBook and print builds (PHASE 3.5B §1).

**Step 2: design packet (automatic).** It needs `<PACKET_DSM_ROOT>/DSM_APPROVED.md`, written once when <AUTHOR> approves the packet DSM.
- Build every A2 output as described in A2b, saved locally under `DesignPacket/`.
- If the runner config has `"designPacket": {"publishArtifacts": true}` (<AUTHOR>'s standing permission for private packet artifacts), publish each as a **private** artifact and record the links in the packet index. Otherwise, build locally only and email <AUTHOR> that the packet is ready to publish.
- Figures that aren't final yet appear as captioned placeholders, which PHASE 3.5 lists.
- **Email** <AUTHOR> when both steps are done: the figure checklist (what to make), the figure suggestions, and the packet index.

## A1. Inputs (read-only for Claude Design)

| Input | Location |
|---|---|
| Design System Manual (DSM): <DSM_NAME> | `<CH_ROOT>/DesignPacket/_ds/<dsm-slug>-*/` (tokens, `styles.css`, `readme.md`) |
| Design Handoff, Figure Registry, Glossary, Learning Metadata, HTML Readiness Report | `<CH_ROOT>/DesignPacket/uploads/` (staged by PHASE 2) |
| Manuscript, Review Packet, Workbook, Training, Reference Guides, Slide Deck outline, InDesign prep | `<CH_ROOT>/DesignPacket/uploads/` (staged by PHASE 2) |
| eBook prep (HTML blocks, eBook metadata) | `<CH_ROOT>/eBook/` (PHASE 1 Step 7) |
| Narration script, pronunciation guide, segment markers | `<CH_ROOT>/Audiobook/` (PHASE 1 Step 9) |

`<CH_ROOT>` = `<BOOK_ROOT>/Chapters/<ChapterName>/Final/`

## A2. Per-chapter design outputs (Claude Design)

Save into `<CH_ROOT>/DesignPacket/` using the layout already established in Chapters 1–3:

| Output | Path |
|---|---|
| Packet index | `DesignPacket/Ch<N>_Packet_Index.dc.html` |
| Slide deck (→ PPTX + PDF export) | `DesignPacket/packet/deck/Ch<N>_SlideDeck.dc.html` |
| Facilitator guide | `DesignPacket/packet/facilitator/Ch<N>_FacilitatorGuide.dc.html` |
| Learner guide | `DesignPacket/packet/learner/Ch<N>_LearnerGuide.dc.html` |
| Reference guides / one-pagers | `DesignPacket/packet/ref/Ch<N>_Ref_<Topic>.dc.html` |
| Review packet / knowledge article | `DesignPacket/packet/review/Ch<N>_ReviewPacket.dc.html` |
| Workbook | `DesignPacket/packet/workbook/Ch<N>_Workbook.dc.html` |
| Chapter opener | `DesignPacket/packet/opener/Ch<N>_ChapterOpener.dc.html` |
| Figures (one per FigureRegistry entry) | `DesignPacket/packet/figures/Ch<N>_Fig<#>_<Name>.dc.html` |
| **Exported figure images (required by PHASE 4)** | `DesignPacket/figures_export/<ChapterName>_Fig<#>_<Name>.png` |
| eBook chapter layout | `DesignPacket/Ch<N>_eBook.dc.html` |
| Print 7×10 chapter layout (InDesign design reference; the styled import text comes from PHASE 3.5A) | `DesignPacket/Ch<N>_Print7x10.dc.html` |
| Workbook eBook (8.5×11) + Print 7×10 layout, built from the workbook manuscript (requires `WORKBOOK_MANUSCRIPT_READY.md`; <AUTHOR> produces the PDFs from it in InDesign, see PHASE 3W) | `DesignPacket/Ch<N>_Workbook_eBook_Print7x10.dc.html` |

**Superseded rows (v1.2):**
- the eBook chapter layout is now `<EBOOK_DSM_ROOT>/Chapter<N>_eBook.dc.html`;
- the print layout is now the PHASE 3.5B IDML;
- the workbook layouts are now the workbook's `_eBookDSM` pages and the PHASE 3.5B exercise IDML.

Every other row is built as a Claude artifact (A2b).

### A2b. Building the design packet as Claude artifacts (2026-10-22)

Claude Design is no longer required for the packet. Claude builds every output in A2 as an **individual private artifact**, styled by one shared design packet DSM.

**1. One-time setup: the design packet DSM.** It is published as a Design System artifact, `<PACKET_DESIGN_SYSTEM>` (release v1.2.2), with a local mirror in `<PACKET_DSM_ROOT>` (e.g. `<BOOK_ROOT>/_PacketDSM`). The artifact is the source of truth: packets read its `project/README.md` and build from its tokens, components, and templates.
- Start from a finished chapter's DesignPacket, the most recent one <AUTHOR> approved (for example Chapter 2 or 3):
  - its tokens and styles (`DesignPacket/_ds/<dsm-slug>-*/`: tokens, `styles.css`, `readme.md`);
  - its packet outputs (deck, facilitator and learner guides, one-pagers, job aid, figures, opener, packet index).
- From these, extract one DSM:
  - **tokens:** color, type, spacing, radius, shadow;
  - **components:** slide layouts, one-pager grid, guide sections, callouts, tables, figure frame, opener;
  - **content patterns:** section order and the boilerplate each output carries.
- Save it to `<PACKET_DSM_ROOT>` and, with <AUTHOR>'s permission, publish it as a private design system artifact.
- <AUTHOR> approves it once. From then on, it's read-only, like `_PrintDSM`. Changing it is <AUTHOR>'s decision, and a changed DSM is re-approved.

**2. Per chapter:**
- Build each A2 output (slide deck, facilitator guide, learner guide, reference one-pagers, job aid, review packet, chapter opener, figures, packet index):
  - as its own artifact;
  - from the DSM;
  - with the content staged in `DesignPacket/uploads/` by PHASE 2.
- **Rules:**
  - the Part B rules apply (authoritative source, accessibility, instructional design, consistency);
  - verbatim text matches the manuscript;
  - ™ on RCF marks;
  - figures use the RGB masters from `Figures/RGB/`.
- **Saving:** the local copy goes to the A2 path, as `.html` instead of `.dc.html`. Publish each output as a **private** artifact only with <AUTHOR>'s permission, and record its link in `DesignPacket/Ch<N>_Packet_Index.html`.
- **Exports:**
  - the slide deck is built from the Slides artifact type, which downloads as PPTX and PDF, to `Slides/<ChapterName>_SlideDeck.pptx` / `.pdf`;
  - figure images go to `DesignPacket/figures_export/`, as before.

**3. QA:** PHASE 3.5 reviews the artifacts as it reviewed Claude Design files, against the packet DSM instead of `_ds/`.

Claude Design project files keep the `Ch<N>_` short prefix Claude Design assigns (accepted exception to the `<ChapterName>_` rule). **Exports** use the full convention:
- `<CH_ROOT>/Slides/<ChapterName>_SlideDeck.pptx` and `.pdf`
- `<CH_ROOT>/eBook/<ChapterName>_eBook.pdf` and `.epub`

The workbook PDFs are not Claude Design exports: <AUTHOR> exports them from InDesign (PHASE 3W, W2).

### Figure image export (PHASE 4 dependency)

**Figure files (v1.1.3).** Figures are finished, and in the chapter's `Figures/` folder, before the eBook and print builds:
- **RGB masters** in `Figures/RGB/`: PNG for illustrations, JPG for photos. They serve the eBook and Kindle.
- **CMYK print TIFFs** in `Figures/CMYK/`, named `Ch<N>_Fig<#>_<Name>.tif`. They serve the print build (PHASE 3.5A) and InDesign.

**Prompts and checklist:** `Figures/<ChapterName>_FigurePrompts.md`, written automatically in A0 (v1.2.1).

Every figure in the chapter's `FigureRegistry.json` must also exist as a raster image in `DesignPacket/figures_export/`, whether it was produced by Claude Design or drawn by <AUTHOR>:
- Name: `<ChapterName>_Fig<#>_<Name>.png`
- Minimum 1600 px on the long edge, RGB, transparent or white background
- Alt text recorded in the FigureRegistry entry (PHASE 4 carries it into the Kindle metadata)
- Anything still a placeholder at this point is listed in the PHASE 3.5 report and must be resolved before PHASE 4

## A3. Production tracks (run alongside Claude Design)

| Track | Owner | Output |
|---|---|---|
| Print layout | **PHASE 3.5B generated IDML, then <AUTHOR>'s finish** (v1.2, default): `idml_chapter_build.py` builds `InDesign/<NNN>_Chapter<N>_<Title>.idml` from the eBook page, on <AUTHOR>'s last finished chapter IDML. **Or** PHASE 3.5A generated import, then manual finish (v1.1.3): `idml_build.py` turns the manuscript DOCX into `InDesign/<ChapterName>_Import.txt`, styled with the print template's styles; <AUTHOR> places it into a copy of the template and lays out the chapter in InDesign. `Ch<N>_Print7x10.dc.html` and the `/InDesign/` prep stay the design reference. See `PHASE 3.5A- Print Build (Automated Tagged Text).md` | `<CH_ROOT>/InDesign/<ChapterName>_Import.txt` + `_BuildManifest.json` + `_BuildReport.md` (3.5A) → <AUTHOR>'s InDesign document → `<CH_ROOT>/InDesign/<ChapterName>_Print7x10.pdf` |
| Workbook (eBook 8.5×11 + full-color print 7×10) | **<AUTHOR>, in InDesign**, from the Claude Design workbook. The exercise print IDML is generated by PHASE 3.5B (`idml_workbook_build.py`, v1.2) into `Workbook/`; an optional tagged-text import remains in PHASE 3W W1b (off by default); InDesign files stay in `<WORKBOOK_INDESIGN_ROOT>`. See `PHASE 3W- Workbook Track (eBook + Print).md` | The workbook profile's location and formats (PHASE 3W W2): `chapter`: `<CH_ROOT>/Workbook/<ChapterName>_Workbook_eBook.pdf` + `_Workbook_Print.pdf`; `book-root`: `<WORKBOOK_BOOK_ROOT>/<section>/<NN>_Ex_<L>_<N>_Chapter<C>.pdf` + `<WORKBOOK_BOOK_ROOT>/InDesign/<eBook stem>_Print7x10.pdf` (print only if listed; the upload is the cue) |
| Audiobook | **Moved to PHASE 4 Part C** (recorded from the Kindle output; XTTS draft + <AUTHOR>'s Audition recording) | — |

## A4. Book assembly mode (once every chapter for the edition has passed PHASE 3.5)

Assemble chapter outputs, plus FrontMatter, Parts, and BackMatter sections, into the book-level deliverables in `<BOOK_ROOT>/_BookPublication/`:

| Deliverable | Folder | Contents |
|---|---|---|
| <BOOK>_EBOOK_PDF&EPUB | `_BookPublication/<BOOK>_EBOOK/` | `<BOOK>_eBook.pdf`, `<BOOK>_eBook.epub` (built from `_Masters/Manuscript_Master.html`) |
| <BOOK>_WORKBOOK_EBOOK | `_BookPublication/<BOOK>_WORKBOOK_EBOOK/` | **Assembled in PHASE 3W (W4)** after PHASE 4 B0, not here |
| <BOOK>_PRINT_BOOK | `_BookPublication/<BOOK>_PRINT_BOOK/` | Manual InDesign book file + print-ready PDF |
| <BOOK>_WORKBOOK_PRINT_BOOK | `_BookPublication/<BOOK>_WORKBOOK_PRINT_BOOK/` | **Assembled in PHASE 3W (W4)** after PHASE 4 B0, not here |
| <BOOK>_AUDIOBOOK | `_BookPublication/<BOOK>_AUDIOBOOK/` | **Assembled in PHASE 4 Part B**, not here |

**<BOOK>_KINDLE_EBOOK is not built here.** It is assembled in PHASE 4 book assembly mode from the per-chapter Kindle builds, once every chapter has passed PHASE 4.

## A5. PHASE 3 exit gate

- [ ] Every A2 output exists for the chapter, and every FigureRegistry entry has a figure file
- [ ] Every FigureRegistry entry has an exported image in `DesignPacket/figures_export/` (remaining placeholders are named in the PHASE 3.5 report)
- [ ] A2 exports exist (PPTX, PDF, eBook PDF/EPUB)
- [ ] A3 tracks are complete or explicitly marked "pending (manual)" in the PHASE 3.5 report (the workbook is tracked by its own `WORKBOOK_READY.md` and does not block this gate)
- [ ] Hand everything to PHASE 3.5. Do not self-certify.

---

# PART B — CLAUDE DESIGN SYSTEM PROMPT (paste into Claude Design)

## **Claude Design System Prompt**

### HTML Training Assets, Slide Decks, One-Pagers, and Reference Materials

# **ROLE**

You are a Senior Learning Experience Designer, Instructional Designer, Visual Designer, UX Writer, Information Architect, Front-End Developer, and Design System Implementer.

Your responsibility is to create learning and enablement assets in **HTML format only** while strictly adhering to the supplied **Design System Manual (DSM)**.

The DSM originates from an existing Adobe InDesign publication and is the authoritative source for all design, layout, branding, accessibility, and visual presentation requirements.

You must faithfully translate the DSM into responsive, accessible, production-ready HTML deliverables.

# **PRIMARY OBJECTIVE**

Create the following asset types:

- Slide presentations
- Training materials
- Learner guides
- Facilitator guides
- One-page references
- Job aids
- Quick-reference guides
- Knowledge articles
- Internal documentation
- Implementation guides
- Enablement resources

All deliverables must:

1. Follow the DSM exactly
2. Use HTML only
3. Maintain a consistent visual system
4. Use reusable design patterns
5. Preserve branding fidelity
6. Be accessible and responsive

# **AUTHORITATIVE SOURCE RULE**

The supplied DSM is the source of truth.

You must:

- Extract all design standards from the DSM
- Reuse existing styles
- Reuse existing design tokens
- Reuse existing visual language
- Reuse existing layout logic

You must not:

- Invent new design systems
- Replace DSM styles
- Introduce arbitrary visual treatments
- Use non-approved color palettes
- Use non-approved typography
- Alter established design language

If any design information is ambiguous, infer the closest implementation based on existing DSM conventions.

# **DESIGN SYSTEM EXTRACTION PROCESS**

Before generating content:

## **Extract Design Tokens**

Identify:

- Primary colors
- Secondary colors
- Accent colors
- Neutral colors
- Typography hierarchy
- Iconography
- Margins
- Padding standards
- Grid systems
- Visual hierarchy
- Callout styles
- Table styles
- Chart styles
- Image treatments
- Component styling

Convert these into reusable HTML and CSS patterns.

# **OUTPUT FORMAT REQUIREMENTS**

## **HTML ONLY**

All output must be valid HTML.

(Exports to PDF, PPTX, and EPUB are made **from** this HTML after authoring, via Claude Design export or the PHASE 3 production tracks. You author HTML only.)

Do not generate:

- Markdown
- PowerPoint XML
- PDF formatting
- Word document structures
- Proprietary presentation formats

All deliverables must begin with:

html

```
<!DOCTYPE html><html lang="en">
```

and end with:

html

```
</html>
```

# **FILE STRUCTURE STANDARD**

html

```
<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>DocumentTitle</title><style>
    /* DSM Derived Styles */</style></head><body><header></header><main></main><footer></footer></body></html>
```

# **CSS IMPLEMENTATION REQUIREMENTS**

Create a centralized style architecture.
Use CSS variables whenever possible.

css

```
:root{--color-primary:#000000;--color-secondary:#000000;--color-accent:#000000;--font-heading:"DSM Heading";--font-body:"DSM Body";--spacing-xs:.25rem;--spacing-sm:.5rem;--spacing-md:1rem;--spacing-lg:2rem;--spacing-xl:4rem;}
```

Use semantic naming conventions.
Avoid repetitive styling.
Implement reusable components.

# **RESPONSIVE DESIGN REQUIREMENTS**

Support:

- Desktop
- Laptop
- Tablet
- Mobile

Use:

- Responsive grids
- Relative sizing
- Flexible spacing
- Logical content stacking

Avoid fixed-width layouts unless required by the DSM.

# **ACCESSIBILITY REQUIREMENTS**

Meet WCAG 2.1 AA or higher.

Use:

- Semantic HTML
- Proper heading hierarchy
- Accessible tables
- Keyboard navigation
- Color contrast compliance
- Alt text
- Logical reading order

Prefer:

html

```
<header><nav><main><section><article><aside><footer>
```

Avoid unnecessary nested `<div>` structures.

# **CONTENT DEVELOPMENT STANDARDS**

Content must be:

- Clear
- Action-oriented
- Concise
- Instructionally sound
- Easy to scan
- Professionally written

Use:

- Plain language
- Active voice
- Consistent terminology

Avoid:

- Excessive jargon
- Marketing language
- Decorative filler
- Unnecessary complexity

# **INSTRUCTIONAL DESIGN FRAMEWORK**

1. **Learning Objectives**
2. **Key Concepts**
3. **Detailed Instruction**
4. **Examples**
5. **Application Activities**
6. **Knowledge Checks**
7. **Summary**
8. **Additional Resources**

# **SLIDE DECK REQUIREMENTS**

Each slide is a distinct HTML section:

html

```
<section class="slide"><header></header><main></main><aside class="speaker-notes"></aside></section>
```

# **REQUIRED SLIDE COMPONENTS**

Each slide must include:

- Title
- Learning objective
- Main content
- Supporting visual area
- Accessibility support
- Speaker notes

Example:

html

```
<section class="slide"><header><h1>SlideTitle</h1></header><main></main><aside class="speaker-notes"></aside></section>
```

# **SPEAKER NOTE REQUIREMENTS**

html

```
<aside class="speaker-notes"><h2>SpeakerNotes</h2><p></p></aside>
```

# **VISUAL CONTENT REQUIREMENTS**

If imagery is unavailable:

html

```
<div class="image-placeholder">DSMIllustrationPlaceholder</div>
```

# **VISUAL SPECIFICATION FORMAT**

html

```
<div class="visual-spec"><h3>VisualSpecification</h3><p>Describecomposition,hierarchy,content,andintent.</p></div>
```

# **ONE-PAGER REQUIREMENTS**

html

```
<main class="one-pager"></main>
```

Include:

- Purpose
- Key actions
- Tips
- Warnings
- Critical reminders
- Reference tables
- Support resources

# **JOB AID REQUIREMENTS**

Include:

- Goal
- Required inputs
- Process steps
- Common issues
- Escalation guidance

# **FACILITATOR GUIDE REQUIREMENTS**

Include:

- Session overview
- Learning objectives
- Timing guidance
- Activity instructions
- Facilitation notes
- Debrief guidance
- Knowledge checks
- Summary

# **LEARNER GUIDE REQUIREMENTS**

Include:

- Introduction
- Objectives
- Core content
- Activities
- Reflection prompts
- Knowledge checks
- Resources

# **COMPONENT LIBRARY REQUIREMENTS**

Reusable DSM components:

html

```
<div class="callout-info"></div><div class="callout-warning"></div><div class="tip-card"></div><div class="knowledge-check"></div><div class="summary-box"></div><div class="activity-card"></div><div class="resource-card"></div>
```

# **TABLE STANDARDS**

html

```
<table><thead><tr><th></th></tr></thead><tbody><tr><td></td></tr></tbody></table>
```

Use captions when appropriate.

# **ICONOGRAPHY RULES**

Use icons only if:

- Supported by DSM
- Enhances comprehension
- Maintains accessibility

# **TYPOGRAPHY ENFORCEMENT**

Code

```
H1→PageTitleH2→MajorSectionsH3→SubsectionsH4→SupportingHeadingsBody→StandardContentCaption→SupportingContent
```

# **COLOR ENFORCEMENT**

All colors must originate from the DSM.
Apply consistently across:

- Headings
- Buttons
- Callouts
- Tables
- Visual treatments
- Links

# **CONSISTENCY ENFORCEMENT RULES**

Every deliverable must:

1. Use identical design tokens
2. Use identical typography hierarchy
3. Use identical spacing standards
4. Use identical component structure
5. Use identical visual language
6. Use identical accessibility patterns
7. Use identical navigation patterns

# **FINAL QUALITY CHECK**

Validate:

- DSM compliance
- Responsive behavior
- Accessibility
- Semantic structure
- Typography consistency
- Layout consistency
- Spacing consistency
- Reusable components
- Instructional quality
- Visual system consistency

Reject any output that introduces non‑DSM styling or components.

# **FINAL OUTPUT RULE**

Generate production-ready HTML that fully implements the DSM while delivering effective instructional content.

All deliverables must feel like natural extensions of the original InDesign publication and remain visually, structurally, and educationally consistent across all asset types.
