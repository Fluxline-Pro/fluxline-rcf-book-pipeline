# Placeholders

Every phase file in `v_1_0_2/` is written against placeholder tokens instead of one author's folders. Replace them once, and the whole pipeline points at your book.

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
| `<DSM_NAME>` | Name of your Design System Manual — the token, typography, and component spec the design phase must obey | `Quiet Engine DSM` |
| `<dsm-slug>` | Folder name of that DSM inside `DesignPacket/_ds/` | `quiet-engine-dsm` |
| `<RAG_COLLECTION>` | Local vector store (ChromaDB) collection name for the whole book | `quiet_engine_book` |
| `<RAG_INDEX_CLOUD>` | Cloud vector index (Azure AI Search) name for the whole book. Azure index names allow lowercase letters, digits, and dashes only | `quiet-engine-book` |
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
  '<DSM_NAME>'       = 'Quiet Engine DSM'
  '<dsm-slug>'       = 'quiet-engine-dsm'
  '<RAG_COLLECTION>' = 'quiet_engine_book'
  '<RAG_INDEX_CLOUD>' = 'quiet-engine-book'
}
# UTF-8 without BOM, LF endings, trailing newline preserved — the files contain
# em dashes and arrows, and Set-Content would rewrite the encoding.
$utf8 = New-Object System.Text.UTF8Encoding $false
Get-ChildItem v_1_0_2\*.md | ForEach-Object {
  $t = [System.IO.File]::ReadAllText($_.FullName, $utf8)
  foreach ($k in $map.Keys) { $t = $t.Replace($k, $map[$k]) }
  [System.IO.File]::WriteAllText($_.FullName, $t, $utf8)
}
```

bash / macOS / Linux:

```bash
cd v_1_0_2
# Same rule: longer tokens first, so <BOOK> does not eat <BOOK_ROOT>.
sed -i 's|<BOOK_ROOT>|/Books/MYBOOK_FIRST_EDITION|g; s|<BOOK_SLUG>|MYBOOK_FIRST_EDITION|g; s|<BOOK_TITLE>|The Quiet Engine|g; s|<BOOK>|MYBOOK|g; s|<EDITION>|First Edition|g; s|<AUTHOR>|A. Writer|g; s|<DSM_NAME>|Quiet Engine DSM|g; s|<dsm-slug>|quiet-engine-dsm|g; s|<RAG_COLLECTION>|quiet_engine_book|g; s|<RAG_INDEX_CLOUD>|quiet-engine-book|g' *.md
```

On macOS use `sed -i ''` instead of `sed -i`.

Leave `<ChapterName>` and `<CH_ROOT>` alone — the phases resolve those per chapter as they run.

---

## Not placeholders, but worth changing

These are concrete because a working example teaches faster than a blank. Change them to suit your book; nothing depends on the specific values.

| Thing | Appears as | Note |
|---|---|---|
| **"PASS 7"** | The final-draft stage a manuscript must reach before PHASE 1 | It means the seventh editing pass in the pipeline this came from. Substitute your own name for "the draft is locked and I will not rewrite it now". The lock matters; the number does not. |
| **Print trim size** | `7×10`, `Ch<N>_Print7x10.dc.html` | Set to your trim. |
| **Local models** | `Qwen2.5 14B Instruct` (drafting, Ollama), `nomic-ai/nomic-embed-text-v1.5` (embedding, ONNX/TEI container, 768 dims) | Defaults, not requirements. Pick an embedder whose context window holds a whole chunk (1000 words ≈ 1,350 tokens); `all-MiniLM-L6-v2`, for example, silently truncates at 256 tokens. Keep one embedding model per track for the whole book — changing it means re-embedding every chapter for that track. |
| **Cloud models** | Azure OpenAI `text-embedding-3-small` (1536 dims) into Azure AI Search; optional Azure OpenAI chat deployment | Optional track (`cloud.enabled` in `RAG_Config.json`). Any cloud embedder + vector store works if PHASE 5 §4B's schema rules are kept. |
| **Toolchain** | Claude and Claude Design (generation), InDesign (print), XTTS (narration), Ollama + ONNX/TEI + ChromaDB (local RAG), Azure OpenAI + Azure AI Search (cloud RAG, optional), n8n + OpenClaw (orchestration) | Swap freely. The gates, deliverables, and source-of-truth rules are the pipeline; the tools are an implementation. |
| **Framework terms** | The terminology lock and voice kit in PHASE 1 | Fill with the vocabulary your book defines — the terms that must never drift across formats. |
| **Book-level folders** | `_BookMarketing/`, `_BookGovernance/`, `_BookPublication/`, `_BookAutomation/`, `_FinalizedReleases/`, `_Archive/` | Rename if you like; update `MASTER_PIPELINE_OVERVIEW.md` §4 to match, since that file is the tie-breaker. |
| **Optional artifact types** | Workbook, training materials, equations, audiobook | Drop what your book does not have. Record the omission in the checklist rather than leaving items silently blank — an unexplained gap and a deliberate one look identical six chapters later. |

---

## Two conventions worth keeping

**Chapter naming.** `Ch<N>_<PascalCaseTitle>` is what lets governance catch drift automatically. Any stable convention works, but pick one before chapter one — renaming mid-book means touching every manifest, trigger, and vector.

**`Final/` as the chapter root.** Phases 4 onward read only from `Chapters/<ChapterName>/Final/`. That one rule is what keeps a half-finished draft from reaching a published file.
