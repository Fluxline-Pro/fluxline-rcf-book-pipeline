# PHASE 5 — Claude Design Publication Pipeline  
### EPUB • Kindle • HTML Master • Workbook eBook • RAG

## PURPOSE
Transform the fully completed PASS 7 manuscript and workbook into publication‑ready digital formats using Claude Design (HTML generation) and Claude Python (EPUB/Kindle packaging).

PHASE 5 produces:
- Reflowable EPUB manuscript  
- Kindle AZW3/MOBI manuscript  
- Reflowable EPUB workbook  
- Kindle AZW3/MOBI workbook  
- DSM‑compliant HTML masters  
- RAG‑optimized HTML versions  
- Metadata + TOC + packaging reports  

---

# INPUTS
- PASS 7 manuscript  
- PASS 7 workbook content  
- DSM (Design System Manual)  
- Figure Registry  
- PHASE 3 HTML component library  
- InDesign print layout (reference only)

---

# OUTPUTS
- `RCF_Manuscript.epub`  
- `RCF_Manuscript.azw3`  
- `RCF_Workbook.epub`  
- `RCF_Workbook.azw3`  
- `Manuscript_Master.html`  
- `Workbook_Master.html`  
- `RAG_Manuscript.html`  
- `RAG_Workbook.html`  
- Metadata + TOC + validation reports  

---

# PHASE 5 WORKFLOW

## 1. Gather Final Manuscript + Workbook Content
Source:
/Documents/Books/RCF_FIRST_EDITION/PASS7/

Claude Design receives:
- Final chapter text
- Final workbook exercises
- Final figure references
- Final headings + callouts + tables

---

## 2. Normalize Content for HTML Conversion
Claude Design performs:
- Heading hierarchy normalization
- Paragraph spacing normalization
- List + bullet normalization
- Quote + callout normalization
- Figure reference normalization
- Semantic HTML structuring

---

## 3. Generate DSM‑Compliant HTML Manuscript
Claude Design outputs:
- One HTML file per chapter
- DSM typography tokens
- DSM spacing tokens
- DSM callout + table components
- Semantic + accessible markup

All HTML begins with:

<!DOCTYPE html><html lang="en">

And ends with:

</html>


---

## 4. Generate DSM‑Compliant HTML Workbook
Claude Design outputs:
- Exercises
- Reflection prompts
- Knowledge checks
- Activity cards
- Tables + callouts

All DSM rules apply.

---

## 5. Merge HTML Files into Publication Masters
Claude Design merges into:

### Manuscript:
Manuscript_Master.html

### Workbook:
Workbook_Master.html


Includes:
- Front matter
- Back matter
- TOC anchors
- Metadata blocks
- Figure registry references

---

## 6. Convert HTML → EPUB (Claude Python)
Claude Python packages:
- `content.xhtml`
- `toc.xhtml`
- `toc.ncx`
- `content.opf`
- DSM‑derived CSS
- Images + figures
- Metadata

Outputs:
RCF_Manuscript.epub
RCF_Workbook.epub


Validation:
- EPUBCheck
- Navigation integrity
- Structural integrity

---

## 7. Convert EPUB → Kindle
Claude Python converts EPUB to:
- `.azw3` (modern Kindle)
- `.mobi` (legacy)
- `.kf8` (optional fixed layout)

Outputs:
RCF_Manuscript.azw3
RCF_Workbook.azw3


---

## 8. Generate RAG‑Optimized HTML
Claude Design produces:
- Chunk‑friendly HTML
- Semantic headings
- Retrieval‑optimized structure
- Metadata blocks
- Figure anchors

Outputs:
RAG_Manuscript.html
RAG_Workbook.html


---

## 9. Final Packaging + Delivery
Claude Python:
- Organizes final outputs
- Generates publication checklist
- Generates validation report
- Saves all files to:
/Documents/Books/RCF_FIRST_EDITION/RCF/Final/


---

# PHASE 5 DELIVERABLES
### Manuscript
- DSM HTML master
- EPUB
- Kindle AZW3
- Kindle MOBI
- RAG HTML

### Workbook
- DSM HTML master
- EPUB
- Kindle AZW3
- Kindle MOBI
- RAG HTML

### Metadata
- OPF
- NCX
- TOC
- Manifest

### Validation
- EPUBCheck report
- Kindle conversion report
- RAG readiness report

---

# FINAL CHECKLIST
Claude Design + Claude Python must confirm:
- DSM compliance
- Semantic HTML
- Accessibility
- EPUB validity
- Kindle validity
- TOC correctness
- Metadata completeness
- Figure registry alignment
- RAG readiness
- File organization

---

# FINAL OUTPUT RULE
All outputs must:
- Follow DSM
- Be fully accessible
- Be responsive
- Be Kindle‑safe
- Be EPUB‑safe
- Be semantically correct
- Be publication‑ready
- Be consistent with print + workbook + training materials

---

# STATUS
**PHASE 5 updated and ready for execution.**