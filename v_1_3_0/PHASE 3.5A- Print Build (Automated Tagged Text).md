# PHASE 3.5A: Print Build (Automated Tagged Text) (v1.0)

> **Pipeline position:** a print side step that can run any time after PHASE 1 has copied the chapter DOCX into `Manuscript/`, usually alongside PHASE 3 · **Upstream gate:** §1 below (`DESIGN_READY.md` is **not** required) · **Downstream:** <AUTHOR>'s manual print layout in InDesign → the print PDF → PHASE 4 Part 0P print QA
> **Canonical paths, status ladder, triggers, and deliverables:** see `MASTER_PIPELINE_OVERVIEW.md`. If this file and the Overview disagree, the Overview wins and the discrepancy is logged.

**New in release v1.1.3 (2026-10-21).** Until now, print layout started from an empty InDesign document: <AUTHOR> placed the manuscript and applied every paragraph and character style by hand. PHASE 3.5A generates an **InDesign tagged-text file** from the chapter DOCX, with every paragraph and character style already set to the print template's styles. <AUTHOR> places it into a copy of the template, and the layout work starts from styled text.

**Release v1.2:** PHASE 3.5B (`PHASE 3.5B- eBook-First Print Build (IDML).md`) is now the default print build: it generates the print IDML itself, replicating the finished eBook. 3.5A stays available for a chapter whose eBook isn't built yet, or for a plain styled import.

**Role (v1.3.0).** 3.5A is the fallback print route (3.5B is the default). Neither is the final print authority: <AUTHOR> in InDesign is.

**What it is not.** It doesn't lay out pages, place images, or export a PDF. It never opens InDesign, never edits the manuscript, and never changes the template. Layout stays <AUTHOR>'s manual work (§6). Generating an IDML document directly is deferred to a later release; tagged text is the only output.

**Reference implementation:** `idml_build.py` in `<LOCAL_TOOLS_ROOT>` (deterministic; no LLM; `python-docx` plus the Python standard library), with unit tests in `<LOCAL_TOOLS_ROOT>/tests/test_idml_build.py`.

---

## 1. Entry gate

All five must hold. If any fails, write nothing and tell <AUTHOR> which one.

1. **The DOCX exists** at `<CH_ROOT>/Manuscript/<ChapterName>_Manuscript.docx` (`<CH_ROOT>` = `Chapters/<ChapterName>/Final/`).
2. **It is newer than `_BookGovernance/Audit/Trigger/AUDIT_CLEAR.md`.** A DOCX older than the book audit hasn't been through PASS 7 and the polish window (PHASE 1, "Polish window").
3. **The figures are finished.** Every figure in the FigureRegistry is final and saved in the chapter's `Figures/` folder **before** the eBook and print builds: the RGB master in `Figures/RGB/` (PNG for illustrations, JPG for photos) and the CMYK print TIFF in `Figures/CMYK/`. A missing print TIFF doesn't stop the build, but it fails the figure check.
4. **The print template exists:** `<PRINT_TEMPLATE_BOOK>` in `<PRINT_DSM_ROOT>`. The IDML in that folder is always taken as current: there is no version to choose and nothing to back up.
5. **The manuscript is locked (release v1.2.5).** `<CH_ROOT>/Manuscript/Trigger/MANUSCRIPT_LOCKED.md` exists (PHASE 2.5), its DOCX hash matches the DOCX, and no `MANUSCRIPT_REVISED.md` section is newer than it.

`DESIGN_READY.md` is **not** required. The print build reads the manuscript, not the Claude Design packet, so it can start as soon as the DOCX is final.

**Runs:** on request, by hand or with `<CH_ROOT>/_Pipeline/RERUN_P3.5A.md`. Re-run it whenever the DOCX, `style_map.json`, or the template changes: the manifest's hashes show which input moved. After `Manuscript/Trigger/MANUSCRIPT_REVISED.md`, or a PHASE 4 Part 0 sync that changes the DOCX, re-run it if print layout hasn't started yet. If it has, carry the change into the InDesign document by hand; PHASE 4 Part 0P catches anything missed.

## 2. Inputs

| Input | Path | Role |
|---|---|---|
| **Manuscript DOCX** (canonical) | `<CH_ROOT>/Manuscript/<ChapterName>_Manuscript.docx` | The only text source. Its paragraph and character styles drive the mapping |
| Manuscript MD (replica) | `<CH_ROOT>/Manuscript/<ChapterName>_Manuscript.md` | Consistency guard only. The MD is regenerated from the DOCX, **never the reverse**. If the MD is newer than the DOCX, stop: the edit belongs in the DOCX |
| FigureRegistry | `<CH_ROOT>/Governance/<ChapterName>_FigureRegistry.json` | Figure numbers, alt text, and image paths relative to `<CH_ROOT>`: `imagePath` (the RGB master) and, optionally, `printImagePath` (the CMYK TIFF) |
| Print figures | `<CH_ROOT>/Figures/CMYK/Ch<N>_Fig<#>_<Name>.tif` | CMYK TIFF, 300 ppi at placed size. The RGB PNG/JPG in `Figures/RGB/` is the eBook and Kindle master and never stands in for print |
| Style map | `<PRINT_DSM_ROOT>/style_map.json` | DOCX style → InDesign style (start from `templates/style_map.example.json` in this release) |
| Print template | `<PRINT_TEMPLATE_BOOK>` (IDML) | The style names that exist (`Resources/Styles.xml`) and the template hash |

**Style names use the colon form** the IDML stores: the group, a colon, then the style (`Body Styles:Body Text Heading 1`); ungrouped styles have no prefix (`Normal Paragraph Style`). The style map, the checks, the manifest, and the report all use this form. Only the tagged-text file escapes the colon (`<ParaStyle:Body Styles\:Body Text Heading 1>`), because tagged text requires it.

**The style map** (`style_map.json`):
- `paragraph`: DOCX paragraph style → InDesign paragraph style.
- `character`: DOCX character style → InDesign character style, plus the direct-formatting keys `direct:italic`, `direct:bold`, `direct:bold+italic`, `direct:superscript`, `direct:subscript` for runs that have no character style.
- `figures`: `path_pattern` (a glob; `{chapter}` = `<ChapterName>`, `{short}` = `Ch<N>`, `{n}` = the figure number, e.g. `{short}_Fig{n}_*.tif`), `tif_dir` (relative to `<CH_ROOT>`, e.g. `Figures/CMYK`), and `placeholder_style` (the paragraph style for the figure placeholder line).
- A value that starts with `CONFIRM` or `TODO` is treated as **unmapped**. <AUTHOR> confirms each entry against the print DSM and the template, then removes the prefix.

## 3. Steps

1. **Gate** (§1). Confirm the MD isn't newer than the DOCX.
2. **Read the template** as a zip and parse `Resources/Styles.xml`. Collect every paragraph and character style name in colon form, walking the style groups.
3. **Read the style map** and list any entry still marked `CONFIRM` / `TODO`.
4. **Map the DOCX**, paragraph by paragraph:
   - Empty paragraphs are skipped; spacing comes from the template's styles.
   - Each paragraph takes the style its DOCX style maps to. **An unmapped paragraph keeps its text with no style (`<ParaStyle:>`) and is listed in the report. It is never guessed**, not even from a similar name.
   - Each run takes its character style, or its direct-formatting key; plain runs carry no character style. An unmapped run keeps its text unstyled and is listed.
   - Tabs and forced line breaks are kept. `<`, `>` and `\` in the text are escaped.
5. **Figures.** Each caption paragraph ("Figure N …") gets a placeholder line before it, in `figures.placeholder_style`: `[[FIGURE N | <file> | alt: <alt text>]]`. The image resolves in this order:
   1. a TIFF in `tif_dir` that matches `path_pattern`;
   2. the FigureRegistry `printImagePath`, then `imagePath`, if it points to a TIFF.

   Print figures must be CMYK TIFFs. A figure found only as an RGB PNG or JPG is reported as "RGB only; CMYK TIFF missing". A figure with no file is written as `UNRESOLVED`. Either one fails the check.
6. **Running heads.** Chapter number from `<ChapterName>` (`Ch<N>_…`) and chapter title from the DOCX's title property (or given explicitly). Both are recorded in the manifest so <AUTHOR> can set the running-head text variables.
7. **Write the outputs** (§4), and exit with **0** (all checks pass), **1** (a check failed; see the report), or **2** (bad input: a missing or unreadable file, a non-IDML template, or the MD newer than the DOCX).

```
python <LOCAL_TOOLS_ROOT>/idml_build.py ^
  --docx "<CH_ROOT>/Manuscript/<ChapterName>_Manuscript.docx" ^
  --md "<CH_ROOT>/Manuscript/<ChapterName>_Manuscript.md" ^
  --style-map "<PRINT_DSM_ROOT>/style_map.json" ^
  --template "<PRINT_TEMPLATE_BOOK>" ^
  --figure-registry "<CH_ROOT>/Governance/<ChapterName>_FigureRegistry.json" ^
  --out-dir "<CH_ROOT>/InDesign" --chapter-name <ChapterName>
```

## 4. Outputs

All in `<CH_ROOT>/InDesign/` (`Chapters/<ChapterName>/Final/InDesign/`):

| File | Contents |
|---|---|
| `<ChapterName>_Import.txt` | InDesign tagged text (`<UNICODE-WIN>`, UTF-16 with BOM): `<ParaStyle:…>` per paragraph, `<CharStyle:…>…<CharStyle:>` per styled run, figure placeholder lines |
| `<ChapterName>_BuildManifest.json` | SHA-256 of the template, the style map, the DOCX (and the MD and FigureRegistry, if given); the template's DOMVersion; the styles used, with counts; unmapped items; mapped styles missing from the template; each figure with its resolved path; running heads; the check results |
| `<ChapterName>_BuildReport.md` | The same, for <AUTHOR>: the check table, the unmapped items, figures, styles used, and the manual-finish steps |

Each run overwrites the three files; the manifest's hashes and timestamp identify the build.

## 5. Checks

| Check | Pass when |
|---|---|
| Styles exist | Every style the output uses exists in the template's `Styles.xml` (colon form) |
| Nothing unmapped | No DOCX paragraph, run, or figure placeholder is unmapped, and no map entry the chapter uses is still `CONFIRM` / `TODO` |
| Figures resolve | Every figure resolves to a CMYK TIFF: in `Figures/CMYK/` (the map's `tif_dir`), or at the FigureRegistry `printImagePath` / `imagePath` |
| Running heads set | Chapter number and title are both known |
| Template recorded | The template's SHA-256 is in the manifest |

**A failure blocks the closure of PHASE 3.5A only.** It doesn't block PHASE 3.5, `DESIGN_READY.md`, PHASE 4, or Kindle. PHASE 3.5 reads the build report (its "Print build (3.5A)" section).

## 6. Manual finish (<AUTHOR>, InDesign)

1. Open a **copy** of the print template (File → Save As into your print folder). Never edit or save over the template in `<PRINT_DSM_ROOT>`.
2. File → Place → `<ChapterName>_Import.txt`, with **Show Import Options** ticked. Choose **Use Tagged Text** with **Load Styles** (the template's style definitions win where they conflict). Check the import's list of missing styles: there should be none.
3. Replace each `[[FIGURE N | … ]]` placeholder with the placed image named on it.
4. Set the running heads, then lay out the chapter: openers, page breaks, widows and orphans.
5. **Add the callouts.** Callouts aren't part of the manuscript, so the import has none. Place the ones you approved from the PHASE 1 callout recommendations (`InDesign/` prep, validated in PHASE 2), using the template's Callouts styles.
6. Export the print PDF to `<CH_ROOT>/InDesign/<ChapterName>_Print7x10.pdf` (7×10 in, bleed on the top, bottom, and outside edge (0.125 in), no printer's marks). PHASE 4 Part 0P checks it against the final eBook PDF.

`DesignPacket/Ch<N>_Print7x10.dc.html` stays the design reference for the layout.

## 7. Rules

- **Never edit the DOCX or the MD.** The build only reads them. A wording problem goes to <AUTHOR>, who edits the DOCX and regenerates the MD (and files `MANUSCRIPT_REVISED.md` after PHASE 1).
- **Never write to `<PRINT_DSM_ROOT>`.** The templates, the print DSM, and `style_map.json` are <AUTHOR>'s. The tool refuses an output folder inside the template's or the style map's folder. A style-map change is a proposal in the report, made by <AUTHOR>.
- **Never call InDesign.** No scripting, no IDML writing, no automation of the layout.
- **Never guess an unmapped style.** Report it; the text stays unstyled until the map says otherwise.
- Workbook print build: see PHASE 3W **W1b** (off by default).
