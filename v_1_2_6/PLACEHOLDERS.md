# Placeholders

Every phase file in `v_1_2_5/` is written against placeholder tokens instead of one author's folders. Replace them once, and the whole pipeline points at your book.

Tokens look like `<THIS>`. A few also appear inside example file names (`<BOOK>_Kindle.docx`), so a plain find-and-replace across the folder is enough.

---

## The tokens

| Token | What it is | Example |
|---|---|---|
| `<BOOK_ROOT>` | Absolute path to your book's root folder. Every other path is relative to it. | `D:\Books\MYBOOK_FIRST_EDITION` |
| `<BOOK_SLUG>` | Folder-safe name for the book, used in the root folder name | `MYBOOK_FIRST_EDITION` |
| `<BOOK>` | Short prefix for book-level deliverable folders and files | `MYBOOK` → `MYBOOK_Kindle.docx`, `MYBOOK_KINDLE_EBOOK/` |
| `<BOOK_TITLE>` | Full title, as it appears on the cover | `The Quiet Engine` |
| `<EDITION>` | Edition label | `First Edition` |
| `<AUTHOR>` | Author's name. Appears in the PHASE 7 sign-off and wherever a phase needs a human decision. | `A. Writer` |
| `<ChapterName>` | Per-chapter folder and file prefix. The phases assume `Ch<N>_<PascalCaseTitle>` and governance flags anything that drifts from it. | `Ch1_YourChapterTitle` |
| `<PASS7_SOURCE>` | Folder holding your locked final-draft manuscripts (see "PASS 7" below) | `<BOOK_ROOT>/_PASS7/` |
| `<DRAFT_SOURCE>` | Folder holding the current full-book draft that PHASE 0.9 audits before PASS 7 (one file per chapter) | `<BOOK_ROOT>/_PASS6/` |
| `<DSM_NAME>` | Name of your Design System Manual — the token, typography, and component spec the design phase must obey | `Quiet Engine DSM` |
| `<dsm-slug>` | Folder name of that DSM inside `DesignPacket/_ds/` | `quiet-engine-dsm` |
| `<RAG_COLLECTION>` | Local vector store (ChromaDB) collection name for the whole book | `quiet_engine_book` |
| `<RAG_BLOB_CONTAINER>` | Azure Blob Storage container holding the book's cloud vector files. Container names are 3–63 characters: lowercase letters, digits, and single hyphens | `quiet-engine-book-rag` |
| `<GATEWAY_URL>` | Base URL of the governance gateway that Track C and cloud workflows call instead of a model endpoint (only with `cloud.embeddingProvider: "governance-gateway"`) | `https://governance.example.com` |
| `<CLOUD_EMBED_FLOW>` | Name of the gateway flow that embeds book text for Track C | `book-embed` |
| `<RAG_REFRESH_TIME>` | Local time the PHASE 6 §3G nightly RAG refresh runs | `22:00` |
| `<WORKBOOK_INDESIGN_ROOT>` | Folder outside `<BOOK_ROOT>` where the workbook InDesign documents, book file (INDB), links, and fonts live. No phase reads it; it's named so the phases can say where the source is | `C:\Users\a.writer\OneDrive\InDesign\MYBOOK_Workbook` |
| `<WORKBOOK_BOOK_ROOT>` | (v1.1, optional) The assembled-workbook folder that receives each chapter's final workbook PDF (`<NN>_Ex_<L>_<N>_Chapter<C>.pdf`), if you don't upload to each chapter's `Workbook/` folder. Print workbook PDFs go in its `InDesign/` subfolder (v1.1.2). See PHASE 3W W2 / W2b | `D:\Books\MYBOOK_WORKBOOK_FIRST_EDITION` |
| `<LOCAL_TOOLS_ROOT>` | (v1.1) Folder with the local automation scripts the phases name as reference implementations: `references_check.py`, `glossary_rollup.py`, `release_check.py`, `print_check.py` (v1.1.2), `congruency_check.py` (v1.2.6, PHASE 4 Step 0C), `idml_build.py` (v1.1.3, PHASE 3.5A print build), `ebook_paginate.py`, `ebook_print.py`, `idml_chapter_build.py`, `idml_workbook_build.py` (v1.2, PHASE 3.5B), `dsm_css.py` (v1.2.2, design system alignment), `docx_md_sync.py` (v1.2.5, brings the MD replica in line with the canonical DOCX: PHASE 2.5 and every DOCX-first edit) | `D:\Automation\LocalAI` |
| `<PRINT_DSM_ROOT>` | (v1.1.3) The print design system folder: the print templates (IDML), the print DSM, and `style_map.json` (DOCX style → InDesign style). Also holds <AUTHOR>'s finished chapter IDMLs, which PHASE 3.5B builds on. Read only by PHASE 3.5A and 3.5B, and never written to by any phase. The IDML files in it are always taken as current | `<BOOK_ROOT>/_PrintDSM` |
| `<EBOOK_DSM_ROOT>` | (v1.2) The eBook design system folder (Claude Design): the DSM, fonts, figures, and the chapters' `Chapter<N>_eBook.dc.html` page files. PHASE 3.5B writes the eBook page files here; on the print side it is read for content only | `<BOOK_ROOT>/_eBookDSM` |
| `<PACKET_DSM_ROOT>` | (2026-10-22) The design packet DSM: tokens, components, and content patterns extracted once from a finished chapter's DesignPacket. PHASE 3 builds every chapter's packet as Claude artifacts from it (A2b). Read-only after <AUTHOR> approves it (`DSM_APPROVED.md` in it lets the automation build packets) | `<BOOK_ROOT>/_PacketDSM` |
| `<EBOOK_DESIGN_SYSTEM>` | (v1.2.2) The book eBook's Design System artifact (link). Every book eBook page takes its tokens and components from it (PHASE 3.5B §3a) | `https://claude.ai/artifact/…` |
| `<WORKBOOK_EBOOK_DESIGN_SYSTEM>` | (v1.2.2) The workbook eBook's Design System artifact (link), for every exercise page | `https://claude.ai/artifact/…` |
| `<PACKET_DESIGN_SYSTEM>` | (v1.2.2) The design packet's Design System artifact (link); `<PACKET_DSM_ROOT>` is its local mirror | `https://claude.ai/artifact/…` |
| `<PRINT_TEMPLATE_BOOK>` | (v1.1.3) The book's print template (IDML) in `<PRINT_DSM_ROOT>`, used by PHASE 3.5A | `<PRINT_DSM_ROOT>/Book_Templates_v4.idml` |
| `<PRINT_TEMPLATE_WORKBOOK>` | (v1.1.3, optional) The workbook's print template (IDML), used by the PHASE 3W workbook print build (off by default). Usually in the workbook's own `_PrintDSM/` | `D:\Books\MYBOOK_WORKBOOK_FIRST_EDITION\_PrintDSM\Workbook_Templates_v4.idml` |
| `<CH_ROOT>` | Derived, not set by you: `<BOOK_ROOT>/Chapters/<ChapterName>/Final/` | — |

## Replace them

PowerShell, from the repo root:

```powershell
# [ordered] matters: <BOOK_ROOT> and <BOOK_SLUG> must be replaced before <BOOK>,
# or '<BOOK>_ROOT>' is what you get. A plain @{} hashtable has no guaranteed order.
$map = [ordered]@{
  '<BOOK_ROOT>'      = 'D:\Books\MYBOOK_FIRST_EDITION'
  '<BOOK_SLUG>'      = 'MYBOOK_FIRST_EDITION'
  '<BOOK_TITLE>'     = 'The Quiet Engine'
  '<BOOK>'           = 'MYBOOK'
  '<EDITION>'        = 'First Edition'
  '<AUTHOR>'         = 'A. Writer'
  '<PASS7_SOURCE>'   = 'D:\Books\MYBOOK_FIRST_EDITION\_PASS7'
  '<DRAFT_SOURCE>'   = 'D:\Books\MYBOOK_FIRST_EDITION\_PASS6'
  '<DSM_NAME>'       = 'Quiet Engine DSM'
  '<dsm-slug>'       = 'quiet-engine-dsm'
  '<RAG_COLLECTION>' = 'quiet_engine_book'
  '<RAG_BLOB_CONTAINER>' = 'quiet-engine-book-rag'
  '<GATEWAY_URL>'    = 'https://governance.example.com'
  '<CLOUD_EMBED_FLOW>' = 'book-embed'
  '<RAG_REFRESH_TIME>' = '22:00'
  '<WORKBOOK_INDESIGN_ROOT>' = 'C:\Users\a.writer\OneDrive\InDesign\MYBOOK_Workbook'
  '<WORKBOOK_BOOK_ROOT>' = 'D:\Books\MYBOOK_WORKBOOK_FIRST_EDITION'
  '<LOCAL_TOOLS_ROOT>' = 'D:\Automation\LocalAI'
  # <PRINT_DSM_ROOT> before <PRINT_TEMPLATE_*>, which may contain it
  '<PRINT_DSM_ROOT>' = 'D:\Books\MYBOOK_FIRST_EDITION\_PrintDSM'
  '<EBOOK_DSM_ROOT>' = 'D:\Books\MYBOOK_FIRST_EDITION\_eBookDSM'
  '<PACKET_DSM_ROOT>' = 'D:\Books\MYBOOK_FIRST_EDITION\_PacketDSM'
  '<EBOOK_DESIGN_SYSTEM>' = 'https://claude.ai/artifact/your-book-ebook-system'
  '<WORKBOOK_EBOOK_DESIGN_SYSTEM>' = 'https://claude.ai/artifact/your-workbook-ebook-system'
  '<PACKET_DESIGN_SYSTEM>' = 'https://claude.ai/artifact/your-packet-system'
  '<PRINT_TEMPLATE_BOOK>' = 'D:\Books\MYBOOK_FIRST_EDITION\_PrintDSM\Book_Templates_v4.idml'
  '<PRINT_TEMPLATE_WORKBOOK>' = 'D:\Books\MYBOOK_WORKBOOK_FIRST_EDITION\_PrintDSM\Workbook_Templates_v4.idml'
}
# UTF-8 without BOM, LF endings, trailing newline preserved — the files contain
# em dashes and arrows, and Set-Content would rewrite the encoding.
$utf8 = New-Object System.Text.UTF8Encoding $false
Get-ChildItem v_1_2_5\*.md | ForEach-Object {
  $t = [System.IO.File]::ReadAllText($_.FullName, $utf8)
  foreach ($k in $map.Keys) { $t = $t.Replace($k, $map[$k]) }
  [System.IO.File]::WriteAllText($_.FullName, $t, $utf8)
}
```

bash / macOS / Linux:

```bash
cd v_1_2_5
# Same rule: longer tokens first, so <BOOK> does not eat <BOOK_ROOT>.
sed -i 's|<BOOK_ROOT>|/Books/MYBOOK_FIRST_EDITION|g; s|<BOOK_SLUG>|MYBOOK_FIRST_EDITION|g; s|<BOOK_TITLE>|The Quiet Engine|g; s|<PASS7_SOURCE>|/Books/MYBOOK_FIRST_EDITION/_PASS7|g; s|<DRAFT_SOURCE>|/Books/MYBOOK_FIRST_EDITION/_PASS6|g; s|<WORKBOOK_INDESIGN_ROOT>|/Users/a.writer/OneDrive/InDesign/MYBOOK_Workbook|g; s|<WORKBOOK_BOOK_ROOT>|/Books/MYBOOK_WORKBOOK_FIRST_EDITION|g; s|<LOCAL_TOOLS_ROOT>|/Automation/LocalAI|g; s|<PRINT_DSM_ROOT>|/Books/MYBOOK_FIRST_EDITION/_PrintDSM|g; s|<EBOOK_DSM_ROOT>|/Books/MYBOOK_FIRST_EDITION/_eBookDSM|g; s|<PACKET_DSM_ROOT>|/Books/MYBOOK_FIRST_EDITION/_PacketDSM|g; s|<EBOOK_DESIGN_SYSTEM>|https://claude.ai/artifact/your-book-ebook-system|g; s|<WORKBOOK_EBOOK_DESIGN_SYSTEM>|https://claude.ai/artifact/your-workbook-ebook-system|g; s|<PACKET_DESIGN_SYSTEM>|https://claude.ai/artifact/your-packet-system|g; s|<PRINT_TEMPLATE_BOOK>|/Books/MYBOOK_FIRST_EDITION/_PrintDSM/Book_Templates_v4.idml|g; s|<PRINT_TEMPLATE_WORKBOOK>|/Books/MYBOOK_WORKBOOK_FIRST_EDITION/_PrintDSM/Workbook_Templates_v4.idml|g; s|<BOOK>|MYBOOK|g; s|<EDITION>|First Edition|g; s|<AUTHOR>|A. Writer|g; s|<DSM_NAME>|Quiet Engine DSM|g; s|<dsm-slug>|quiet-engine-dsm|g; s|<RAG_COLLECTION>|quiet_engine_book|g; s|<RAG_BLOB_CONTAINER>|quiet-engine-book-rag|g; s|<GATEWAY_URL>|https://governance.example.com|g; s|<CLOUD_EMBED_FLOW>|book-embed|g; s|<RAG_REFRESH_TIME>|22:00|g' *.md
```

On macOS use `sed -i ''` instead of `sed -i`.

Leave `<ChapterName>` and `<CH_ROOT>` alone — the phases resolve those per chapter as they run.

---

## Not placeholders, but worth changing

These are concrete because a working example teaches faster than a blank. Change them to suit your book; nothing depends on the specific values.

| Thing | Appears as | Note |
|---|---|---|
| **"PASS 7"** | The final-draft stage a manuscript must reach before PHASE 1 | It means the seventh editing pass in the pipeline this came from. Substitute your own name for "the draft is locked and I will not rewrite it now". The lock matters; the number does not. |
| **Print trim size** | `7×10`, `Ch<N>_Print7x10.dc.html`, and the uploaded print PDF `<ChapterName>_Print7x10.pdf` (v1.1.2; the book and the print workbook) | Set to your trim, and keep the file suffix in step with it. `print_check.py` checks a 7×10 in TrimBox, so change it there too. |
| **Workbook eBook page size** | `8.5×11 in` (US Letter) | A page size readers can print at home if they choose. Use A4 for a non-US audience. |
| **Local models** | `Qwen2.5 14B Instruct` (drafting, Ollama), `nomic-ai/nomic-embed-text-v1.5` (embedding, ONNX/TEI container, 768 dims) | Defaults, not requirements. Pick an embedder whose context window holds a whole chunk (1000 words ≈ 1,350 tokens); `all-MiniLM-L6-v2`, for example, silently truncates at 256 tokens. Keep one embedding model per track for the whole book — changing it means re-embedding every chapter for that track. |
| **Cloud models** | Azure OpenAI `text-embedding-3-large` (1024 dims by default, multilingual), vectors stored in Azure Blob Storage, reached through a governance gateway when you have one; optional chat deployment | Optional track (`cloud.enabled` in `RAG_Config.json`). `dimensions` can be raised to 3072. Without a gateway, set `cloud.embeddingProvider` to `azure-openai`. Any cloud embedder and store works if PHASE 5 §4B's layout and pointer rules are kept. |
| **Toolchain** | Claude and Claude Design (generation), InDesign (print, and the workbook's eBook and print), XTTS (draft narration), Adobe Audition (final narration, manual), Ollama + ONNX/TEI + ChromaDB (local RAG), Azure OpenAI + Azure Blob Storage (cloud RAG, optional), n8n + OpenClaw (orchestration) | Swap freely. The gates, deliverables, and source-of-truth rules are the pipeline; the tools are an implementation. |
| **Framework terms** | The terminology lock and voice kit in PHASE 1 | Fill with the vocabulary your book defines — the terms that must never drift across formats. |
| **Book-level folders** | `_BookMarketing/`, `_BookGovernance/`, `_BookPublication/`, `_BookAutomation/`, `_FinalizedReleases/`, `_Archive/` | Rename if you like; update `MASTER_PIPELINE_OVERVIEW.md` §4 to match, since that file is the tie-breaker. |
| **Optional artifact types** | Workbook, training materials, equations, audiobook | Drop what your book does not have. Record the omission in the checklist rather than leaving items silently blank — an unexplained gap and a deliberate one look identical six chapters later. |

---

## Two conventions worth keeping

**Chapter naming.** `Ch<N>_<PascalCaseTitle>` is what lets governance catch drift automatically. Any stable convention works, but pick one before chapter one — renaming mid-book means touching every manifest, trigger, and vector.

**`Final/` as the chapter root.** Phases 4 onward read only from `Chapters/<ChapterName>/Final/`. That one rule is what keeps a half-finished draft from reaching a published file.
