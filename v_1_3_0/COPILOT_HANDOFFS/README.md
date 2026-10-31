# COPILOT_HANDOFFS (v1.3.0)

Microsoft 365 Copilot (the personal Premium account) is used in this pipeline as a **governed second opinion and artifact producer**: independent research verification, image generation, and independent review of finished artifacts. Claude builds, reconciles and maintains the gates; deterministic tools validate technical properties; <AUTHOR> approves.

**This is a human-in-the-loop handoff, not an integration.** Nothing here calls, drives or has access to your Copilot account. The pipeline names the files and the prompt; you carry them to Copilot and carry the result back.

```
Pipeline writes the handoff list ──▶ you open Microsoft Copilot ──▶ upload the named files
        ▲                                                              │ paste the prompt
        │                                                              ▼
Claude consumes the saved report ◀── you save it where it says ◀── Copilot answers
        │
        ▼ discrepancies reconciled ──▶ you decide ──▶ the gate advances
```

## Who does what

| | Does | Does not |
|---|---|---|
| **Claude** | Builds artifacts, prepares the handoff, reads Copilot's report, reconciles it with its own findings, applies decisions through the governed change process, keeps gates, hashes and audit trails | Open Copilot; accept a Copilot finding without your decision |
| **Microsoft Copilot** (Researcher / Chat / Create) | Independently verifies externally checkable claims and citations; reviews finished artifacts for visible differences; generates concept images from an approved brief | Edit the canonical manuscript; certify anything; publish; rewrite narrative, metaphor or framework text because it has no citation |
| **Deterministic tools** | Validate technical properties (hashes, DOCX = MD, congruency, references, preflight, EPUB validation, fonts, colour, bleed) | |
| **<AUTHOR>** | Initiates every Copilot step, approves every finding and image, signs every gate | |

## The handoffs

| File | Phase / step | Copilot mode | Output you save | Gate |
|---|---|---|---|---|
| `COPILOT_HANDOFF_STANDARD.md` | all | n/a | n/a | the shared contract, status labels, platform notes |
| `COPILOT_PHASE2_5_RESEARCH_REVIEW.md` | PHASE 2.5 | Researcher | `COPILOT_RESEARCH_REPORT.md` | `RESEARCH_CLEAR.md` before `MANUSCRIPT_LOCKED.md` |
| `COPILOT_PHASE3_IMAGE_GENERATION.md` | PHASE 3 A0 | Create | images + `<FigureID>_AltText_Rationale.md` | figure registry → PHASE 3.5 |
| `COPILOT_PHASE3_5_DESIGN_REVIEW.md` | PHASE 3.5 (optional) | Chat | `COPILOT_DESIGN_REVIEW.md` | folded into the DesignQA report |
| `COPILOT_PHASE4_FINAL_EBOOK_REVIEW.md` | PHASE 4 Step 0F | Chat | `COPILOT_FINAL_EBOOK_REVIEW.md` | the eBook PDF is not accepted as final wording source until resolved |
| `COPILOT_PRINT_PDF_REVIEW.md` | PHASE 4 0P (optional) | Chat | `COPILOT_PRINT_PDF_REVIEW.md` | print drift list, PHASE 6.5 |
| `COPILOT_KINDLE_REVIEW.md` | PHASE 4 Part B (optional) | Chat | `COPILOT_KINDLE_REVIEW.md` | Part B, PHASE 6.5 |
| `COPILOT_PHASE6_5_PUBLICATION_QA.md` | PHASE 6.5 | Chat | `COPILOT_PUBLICATION_QA.md` | one input to Publishing Ready, never the whole gate |

`COPILOT_AGENT_INSTRUCTIONS.md` is the standing role prompt for a dedicated Copilot agent (paste it into the agent's Instructions); `HOW_TO_USE_COPILOT.md` is the author's one-page guide to where Copilot is used, by PHASE.

`RESEARCH_RECONCILIATION.md` is **Claude's** output (PHASE 2.5 §3.2b), not a Copilot prompt: it compares the manuscript claim, Claude's Pass 4 conclusion, Copilot's conclusion, any source disagreement, the recommended resolution, and your decision.

## Where files go

| Kind | Location |
|---|---|
| Research report and reconciliation | `<CH_ROOT>/Governance/Research/` |
| Design, final eBook, print, Kindle, publication reviews | `<CH_ROOT>/Governance/Copilot/` (book level: `<BOOK_ROOT>/_BookGovernance/Copilot/`) |
| Copilot image handoffs, alt-text and rationale drafts | `<CH_ROOT>/Figures/Copilot/` |
| Generated image drafts | `<CH_ROOT>/Figures/Drafts/` |

## Rules that never change

1. Every Copilot step is started by <AUTHOR>.
2. Copilot's output is evidence or a draft. The source-of-truth order stays: canonical manuscript → glossary/terminology lock → approved metadata and registries → derived artifacts → publication builds.
3. A Copilot `PASS` is not a certification and cannot open a gate by itself.
4. Wording changes go through the decisions log (PHASE 2.5) or `MANUSCRIPT_REVISED.md`. Never straight from Copilot into a file.
5. Copilot never replaces a deterministic validator or a human check the workflow already has.
6. A report whose manuscript hash or file list does not match is stale and rejected.
7. Do not upload secrets or unrelated data (see the standard, part K).

## Optional or required?

| Step | Copilot-required chapters (`copilotRequired: yes`) | Chapter with `copilotRequired: no` |
|---|---|---|
| Research review (PHASE 2.5) | **Required**, or a `research` waiver | Opt-in, through `MANUSCRIPT_REVISED.md` and a re-lock |
| Image generation | Optional generator | Optional |
| Design review (3.5) | Optional | Optional |
| Final eBook review (4 / 0F) | **Required**, or a waiver | Optional |
| Print and Kindle reviews (Kindle is book level) | Optional | Optional |
| Publication QA (6.5) | **Required**, or a waiver | Optional |

A waiver is a line in `Governance/Copilot/Copilot_Waivers.md` (see the standard) with your initials, a date and a reason. It is recorded in the report; it is never silent.
