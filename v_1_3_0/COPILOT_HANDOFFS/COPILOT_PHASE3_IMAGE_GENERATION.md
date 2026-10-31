# COPILOT_PHASE3_IMAGE_GENERATION (prompt v1.0)

**Step:** PHASE 3, A0 (figures) · **Copilot mode:** Create (image generation) · **Output:** image files + `<FigureID>_AltText_Rationale.md` · **Consumed by:** the figure registry (PHASE 3 A0) and PHASE 3.5 design QA

Follows `COPILOT_HANDOFF_STANDARD.md`. This is an **additional generator** next to Gemini and Firefly. It does not replace the Visual DSM, Claude Design, Photoshop/Illustrator/InDesign, or <AUTHOR>'s judgment. No generated image becomes canonical until PHASE 3.5 and <AUTHOR> approve it.

## When to run it

PHASE 3 A0 writes `Figures/<ChapterName>_FigurePrompts.md` (the Gemini prompt, the no-text fallback, the manuscript check, and save-as names for each figure). For each figure that you choose to make with Copilot, Claude also writes `Figures/Copilot/<FigureID>_CopilotHandoff.md` from the template below, with the blanks filled from the registry and the manuscript. You paste one handoff per figure.

## Files and facts to supply (manifest)

| # | Item | Required | Why |
|---|---|---|---|
| 1 | The manuscript passage the figure illustrates (paste the text, or upload the section as DOCX/PDF) | **Yes** | The meaning to preserve |
| 2 | Condensed Visual DSM for the book (palette hex values, line weight, style, do/don't). Use the condensed card `DesignPacket/_ds/DSM_CopilotCard.md` (written by PHASE 3), not the full system | **Yes** | The look |
| 3 | The figure's registry row (ID, number, title, caption, spec, accents) | **Yes** | What it must be |
| 4 | Terminology lock: terms that may appear, if the image has any text | Yes | No invented terms |
| 5 | One or two approved images from earlier chapters (PNG/JPEG) | Optional | Visual consistency |
| 6 | Placement, orientation and target size (print 7×10 in; eBook), accessibility intent | **Yes** | Composition |

Upload at most five images. Do not upload DSM design files that contain licensed fonts or brand assets you do not have the right to share.

## Prompt template (fill the blanks, then paste into Copilot Create)

```
ROLE
You are generating one conceptual illustration for a published non-fiction book. Follow the supplied style rules exactly.

AUTHORITY
You may generate images from the description below. You may propose alt text and a short visual rationale, separately from the image.

PROHIBITIONS
- Do not invent new concepts, models, terms, labels, numbers, acronyms or explanatory text. Preserve the meaning of the passage; do not add to it.
- No text in the image at all, unless this brief says "infographic: text allowed" and lists the exact words.
- Do not use the prohibited imagery or symbolism listed below.
- Do not describe the image instead of making it. Generate it.
- Do not claim the image is print-ready.

FILES
The material in this conversation: the passage, the condensed style rules, the figure row, and any approved reference images.

SOURCE-OF-TRUTH ORDER
1. The manuscript passage below. 2. The style rules below. 3. Any approved reference images. Your own taste last.

THE PASSAGE (meaning to preserve)
<PASTE THE SECTION TEXT>

WHAT THE FIGURE IS
- Figure ID: <FigureID>  ·  Figure <number>: <title>
- Caption (for context only; do not render): <caption>
- The one idea it must carry: <one sentence from the registry spec>

STYLE (Visual DSM, condensed)
- Palette: <hex values and roles>
- Style: <flat/line/gradient; line weight; level of detail>
- Mood: <e.g. calm, steady, grounded>
- Background: <plain / transparent-look / white>
- Consistency: match the uploaded reference images in palette, line quality and level of abstraction.

COMPOSITION
- Orientation and size: <portrait 1024x1536 | wide 1536x1024 | square 1024x1024>; intended placement: <full page / half page / inline / chapter opener>
- Keep the main subject away from the edges (a safe margin of about 8%); leave quiet space where the page will place the caption.
- Make it simple enough to be refined later in Illustrator or InDesign (clear shapes, no fine texture that cannot be redrawn).
- Print and eBook: it will appear in both.

PROHIBITED IMAGERY / SYMBOLISM
<e.g. no clinical or medical imagery; no religious symbols; no faces of real people; no brand logos; no hands-in-prayer; ...>

ACCESSIBILITY INTENT
The image must carry its meaning through shape and arrangement, not colour alone, and must read in greyscale.

TASK
1. Generate <N> distinct options for this one figure (not variations of one drawing: different compositions of the same idea).
2. After the images, in text, give for the option I choose (ask me which): (a) alt text of 125 characters or fewer; (b) a long description of 2 to 4 sentences; (c) a visual rationale of 2 to 3 sentences saying which part of the passage each element shows. Keep these separate from the image.
3. Say plainly which parts of the passage the image does not show.

OUTPUT
Images, then the text items (a) to (c). No extra commentary.

GATE EFFECT
The images are drafts for the author's selection. They are not canonical until the author approves them and they pass design QA.

LIMITATIONS
The image is AI-generated and is a concept at the generator's native resolution, not a print-ready file. The author finishes or redraws it for print.

PRIVACY
Use only the material in this conversation.

HUMAN APPROVAL
The author chooses, edits or rejects every image.
```

## After Copilot answers

1. Save every image you might use to `<CH_ROOT>/Figures/Drafts/` as `<FigureID>_copilot_<YYYYMMDD>_<n>.png`, even the ones you reject (the revision history).
2. Save the text answers to `<CH_ROOT>/Figures/Copilot/<FigureID>_AltText_Rationale.md`, with the standard front matter.
3. Choose one. Finish it in Photoshop or Illustrator to the print and eBook specs; save the finals as the PHASE 3 A0 save-as names (`Figures/RGB`, `Figures/CMYK`).
4. Update the figure registry row (below). Claude does this in PHASE 3 A0 when you say which option you picked; or do it by hand.

## Figure registry columns added in v1.3.0

PHASE 3 A0 already writes number, caption, spec, accents, status, paths, tool used and alt text. v1.3.0 adds (to `Governance/<ChapterName>_FigureRegistry.json` and its table):

| Field | Meaning |
|---|---|
| `sourceSection` | Manuscript section the figure illustrates |
| `generator` | `Copilot Create` · `Gemini` · `Firefly` · `Illustrator` · `Photoshop` · `hand-drawn` ... |
| `promptVersion` | e.g. `COPILOT_PHASE3_IMAGE_GENERATION v1.0` |
| `dsmVersion` | Visual DSM version used |
| `generatedOn` | Date |
| `aiGenerated` | `true` when any AI tool produced the base image. Required for the production record |
| `approval` | `pending` · `approved <initials> <date>` · `rejected` |
| `filename` | Final file name(s) |
| `placement` | Chapter opener, inline, full page ... |
| `dimensions` | Pixel size as generated, and the print and eBook target |
| `colorMode` | `RGB concept` · `RGB final` · `CMYK final` |
| `resolutionStatus` | `native <w>x<h>` · `upscaled/redrawn to <ppi> ppi` · `needs rework` |
| `altText`, `longDescription`, `rationale` | From Copilot's text, edited by <AUTHOR> |
| `rights` | Provenance and rights note, for example "AI-generated (Microsoft Copilot), finished by <AUTHOR>; no third-party material supplied" |
| `revisionHistory` | Dated list: option chosen, edits, re-generations |

A figure whose `aiGenerated` is true feeds the AI-use disclosure check in PHASE 7.

## Gate effect

A Copilot image enters PHASE 3.5 (design QA) like any other figure. It is `pending` until PHASE 3.5 has checked it against the DSM and the accessibility rules, and <AUTHOR> has written `approved`. PHASE 3.5 will not certify a chapter Production Ready while a figure is `pending` or its resolution status is `RGB concept` with no finished version.

## Limitations

Copilot may ignore palette instructions, add text, or produce slightly different results on every run. It cannot guarantee the style matches the DSM or earlier chapters. Colour accuracy, CMYK conversion, resolution, and print suitability need Photoshop/Illustrator and a proof. The three fixed sizes mean pixel dimensions are small for print.
