# COPILOT_PHASE2_5_RESEARCH_REVIEW (prompt v1.1)

**Step:** PHASE 2.5, Research verification · **Copilot mode:** Researcher · **Output:** `COPILOT_RESEARCH_REPORT.md` · **Consumed by:** PHASE 2.5 §3.2b (Claude's reconciliation) · **Gate:** `RESEARCH_CLEAR.md`

Follows the standard in `COPILOT_HANDOFF_STANDARD.md`. Where this file is silent, the standard applies.

## When to run it

After PHASE 2.5's first (audit) run has written the findings report and the chapter's `ScienceClaims` file (PHASE 0.9 Pass 4). You can fill in the decisions log meanwhile, but PHASE 2.5 applies no fix until this report is saved (or the step is waived). Run it once per chapter, on the chapter text as it stands before any fixes. Pass 4 is Claude's own claim extraction, with the local Deep Researcher workflow as evidence gathering. This step is the second, independent model: it is meant to catch what the first reviewer shared a blind spot on, so do not paste Claude's conclusions into the prompt as facts.

**Deep Researcher and this step.** The local Deep Researcher workflow (search, junk triage, citation verification, quote-accuracy QA) plus the author's claim-by-claim review of its results is the **evidence and review record for Pass 4**. It does not replace this step: this is the second, independent model. For a retrofit of a chapter whose wording was already revised after that review, the full chapter is still reviewed; Copilot should say whether the new wording itself overstates anything.

Not required for chapters with `copilotRequired: no`. They can opt in through `MANUSCRIPT_REVISED.md` (see HOW_TO_RUN).

## Two stages, one conversation

This review is deliberately **two-stage**, so Claude's findings and the Deep Researcher evidence cannot anchor Copilot's own reading:

```
STAGE 1  Copilot builds its OWN claim inventory from the chapter alone
   |
   v     STOP: Copilot returns the inventory and waits
   |
STAGE 2  you upload Claude's ScienceClaims + Deep Researcher evidence (+ audit report, claims registry if any);
         Copilot verifies, searches sources, compares, and writes the report
   |
   v
Claude reconciles --> you decide
```

Keep both stages in **one conversation** (Researcher mode). Do not upload any Stage 2 file before Copilot has returned its Stage 1 inventory and said it is waiting. If you do by mistake, tell Copilot to disregard them and start the conversation again.

## STAGE 1 UPLOADS (independent review)

| # | File | Required | Why |
|---|---|---|---|
| 1 | `<CH_ROOT>/Manuscript/<ChapterName>_Manuscript.docx` (or the PDF of it) | **Yes** | The text under review. DOCX is canonical |
| 2 | The chapter's reference list (the References section of the DOCX; if you keep a separate list, upload that too) | **Yes** | Citations to check |
| 3 | `<BOOK_ROOT>/_BookGovernance/Glossary/Glossary_Canonical.json` (or the normalized glossary / terminology lock) | **Yes** | Framework terms are not empirical claims |

Plus the handoff metadata: the `reviewedSha256` and the handoff file name come from the handoff file (`Copilot_Research_Handoff.md`); the prepared Ch1 to Ch6 packets pre-fill them in the prompt, otherwise you fill them into the report afterwards (see After Copilot answers). Nothing else is uploaded.

## STAGE 2 UPLOADS (comparison and verification; only after Stage 1 is returned)

| # | File | Required | Why |
|---|---|---|---|
| 4 | `<BOOK_ROOT>/_BookGovernance/References/ScienceClaims/<ChapterName>_ScienceClaims.md` | Yes, if it exists | Claude's claim inventory (Pass 4) |
| 5 | Deep Researcher evidence: the reports (`.../ScienceClaims/Results/<ClaimID>_Report.md`) or the chapter's evidence bundle | Yes, if it exists | Evidence already gathered; evidence, not a verdict |
| 6 | `<CH_ROOT>/Governance/<ChapterName>_LockAudit_<ts>.md` (the audit run's findings report) | Optional | What is already flagged |
| 7 | `<CH_ROOT>/Marketing/Intake/<ChapterName>_MKT_ClaimsRegistry.md`, if the chapter has one | Optional | Marketing-facing claims |

Do not upload: the design packet, images, the audiobook, drafts older than the DOCX, anything with credentials. Keep each stage's upload, and the whole conversation, under 20 files.

## Prompt (paste everything below this line into Copilot, with Researcher selected)

```
ROLE
BOOK CONTEXT (author: edit or delete this line): <BOOK_CONTEXT, e.g. "This book is the consumer form of a doctoral dissertation, so sources should meet academic standards.">
You are an independent research verifier for a non-fiction book chapter. You are not the author and not the editor. Your job is to check the chapter's externally verifiable claims and citations against authoritative sources, and report what you find. You are a second opinion; another reviewer has already looked at this chapter.

AUTHORITY
You may read the uploaded files, search for authoritative and peer-reviewed sources, and recommend the smallest defensible wording correction for a claim. You may not edit the manuscript.

PROHIBITIONS
- Do not rewrite, "improve", or restyle the manuscript. Recommend a correction only for a claim the evidence does not support, and make it the smallest change that would be defensible (usually hedging: "tends to", "often", "research suggests", or removing an absolute).
- Do not invent sources, authors, years, page numbers, DOIs, URLs or quotations. Every source you give must be one you actually found; give its URL or DOI. If you cannot find a source, say CANNOT VERIFY.
- Do not mark anything VERIFIED from memory. VERIFIED means you found a source and the source says what the sentence says.
- Do not treat personal stories, lived experience, metaphors, the author's framework definitions, the author's interpretations, or practical exercises as claims needing citations. Classify them and move on.
- Do not certify the chapter as scientifically correct, expert-reviewed, or safe.

SOURCE-OF-TRUTH ORDER
The uploaded DOCX is the text. The glossary defines the author's framework terms. The reference list is the author's own citations. Your own knowledge is last.

FILES
Stage 1: the chapter DOCX, its reference list and the glossary. List every uploaded file by name. If you cannot see a required file, say so and stop. Stage 2 files (the ScienceClaims inventory, Deep Researcher reports or evidence bundle, a lock-audit report, a claims registry) come later. If any of them is already in this conversation, say so, do NOT open or use it, and ask me to remove it and restart.

WORKFLOW (two stages, one conversation)

STAGE 1: INDEPENDENT REVIEW. Do only this, then stop.
1. List the files you can see.
2. Read the chapter DOCX in full.
3. Build your own list of externally verifiable claims: empirical, historical, medical, psychological, neurobiological, physiological, technical, legal, quantitative or academic statements. Give each an ID (C-01, C-02, ...) in manuscript order, with the section heading, a short verbatim excerpt of 25 words or fewer, a category, whether it needs a citation, the citation the author gives (if any), and your initial wording-risk estimate (Low, Medium, High). Do not search for sources yet.
4. Classify every passage you skip as NARRATIVE, FRAMEWORK, METAPHOR, INTERPRETATION or EXERCISE (a one-line count is enough; list the ones that sit close to a claim).
5. Return the Stage 1 inventory (the claim table plus the non-claim counts), then write exactly: "STAGE 1 COMPLETE. Waiting for the Stage 2 files."
STOP AFTER STAGE 1. Do not evaluate any other claim inventory, Deep Researcher report or prior research finding yet, and do not search for sources yet. Wait for me to write "STAGE 2 FILES ATTACHED".

STAGE 2: COMPARISON AND VERIFICATION. Begin only after I write "STAGE 2 FILES ATTACHED". Do not change your Stage 1 inventory; if you find a further claim, add it with an "S2-" ID and say so.
6. For each claim, decide whether it needs a citation and compare it with the citation the author gives.
7. Search for authoritative or peer-reviewed support, and for evidence that contradicts or qualifies the claim. Prefer systematic reviews, meta-analyses, major textbooks, professional-body guidance, and primary studies.
8. Judge the wording, not just the topic: flag unsupported certainty ("always", "never", "all", "only", "proves"), causality stated where the evidence is correlational, universality stated where findings are about averages or specific populations, specific numbers or mechanisms, and outcome promises. Flag clinical or safety-relevant statements (breathwork, trauma, medication, mental-health advice).
9. For each citation in the reference list: does it exist, are the authors/year/title/venue right, and does it support the sentence it is attached to?
10. Compare your inventory with the uploaded ScienceClaims inventory and treat the Deep Researcher material as evidence to check, not as a verdict. Add the section "Differences from the uploaded claims list": claims you found that it lacks, claims it has that you rated differently, and why. Do not change your own ratings to match it.
11. For every claim, give the smallest proposed correction, or "none needed".
12. Give complete source details for every source you relied on: authors, year, title, journal or publisher, volume/issue/pages, DOI or URL, and the exact passage or finding that supports (or contradicts) the claim. This will be used for later APA verification, so do not abbreviate.
13. State plainly what you could not verify and why.

OUTPUT SCHEMA
At the end of Stage 2 (not before), return one Markdown document titled COPILOT_RESEARCH_REPORT, with these parts in this order. Its claim table starts from your unchanged Stage 1 inventory:

Front matter (as a code block):
 handoff: COPILOT_PHASE2_5_RESEARCH_REVIEW v1.1
 handoffFile: <leave as: ASK-AUTHOR-TO-FILL>
 chapter: <chapter name>
 manuscriptSha256: <leave as: ASK-AUTHOR-TO-FILL>
 reviewDate: <today>
 copilotMode: Researcher
 filesUploaded: <Stage 1 files; Stage 2 files>
 stage1Completed: <yes | no. Write yes only if you returned the Stage 1 inventory before any Stage 2 file was supplied>
 deviations: <none or what differed>

1. Summary: counts by verification result; counts blocking / non-blocking; the three most important findings.
2. Claim table with these columns exactly:
 Claim ID | Section | Excerpt (<=25 words) | Category | Citation needed (yes/no) | Existing source | Verification result | Evidence summary | Source details | Wording risk (Low/Medium/High) | Smallest proposed correction | Confidence and limitations | Author decision required (yes/no)
 - Category: EMPIRICAL, HISTORICAL, MEDICAL, PSYCHOLOGICAL, NEUROBIOLOGICAL, PHYSIOLOGICAL, TECHNICAL, LEGAL, QUANTITATIVE, ACADEMIC.
 - Verification result: exactly one of VERIFIED, PARTIALLY SUPPORTED, UNSUPPORTED, OVERSTATED, NEEDS CITATION, CANNOT VERIFY, AUTHOR DECISION REQUIRED.
3. Citation check table: Ref # | As cited by the author | Found? | Corrected details (if different) | Supports the sentence? (yes / partly / no / cannot tell).
4. Possible fabricated or unverifiable references (list; empty if none).
5. Passages classified as non-claims (counts, plus any close to a claim).
6. Differences from the uploaded claims list.
7. Safety-relevant statements.
8. What I could not verify, and why.
9. Limitations of this review (state that this is an AI review, not expert review).

GATE EFFECT (for your information)
Claude will compare your report with its own findings and write a reconciliation. The author will then decide each item. Your report changes nothing by itself.

LIMITATIONS
You cannot confirm that a cited source's full text says what the sentence says if you can read only an abstract or a summary; say which you read. This review is not peer review or expert review.

RETURN
Output the report as plain Markdown that can be saved as COPILOT_RESEARCH_REPORT.md.

PRIVACY
Use only the uploaded files and public sources. Do not ask for or use any other personal or business data.

HUMAN APPROVAL
Nothing you recommend is applied without the author's written decision.
```

## After Copilot answers

1. **After Stage 1:** read the inventory. Only then upload the Stage 2 files and write: `STAGE 2 FILES ATTACHED`.
2. **After Stage 2:** read the report. Replace `ASK-AUTHOR-TO-FILL` in the front matter if any remain: `manuscriptSha256` is the `reviewedSha256` written in the handoff file you were given (`Governance/Research/Copilot_Research_Handoff.md`, or `Copilot_Research_Handoff_<n>.md` for a re-run; check with `Get-FileHash <docx>` if you changed the file), `handoffFile` is that file's name, and `filesUploaded` lists the files you really uploaded at each stage.
3. Save it as `<CH_ROOT>/Governance/Research/COPILOT_RESEARCH_REPORT.md` (create the folder). If the conversation was split, name the parts `COPILOT_RESEARCH_REPORT_part2.md` and so on. You may also save the Stage 1 inventory as `COPILOT_RESEARCH_STAGE1.md`: Claude uses it to confirm the inventory was made independently.
4. Re-run PHASE 2.5 (`_Pipeline/RERUN_P2.5.md`) when you have finished the decisions already in the log. PHASE 2.5 §3.2b reconciles the report.

## Gate effect, blocking and non-blocking

`RESEARCH_CLEAR.md` is written by PHASE 2.5 (§5) only when no **blocking** research finding is open. Non-blocking findings do not stop the lock.

**Blocking** (must be closed: fixed, cited, removed, or kept by `<AUTHOR>` with initials and a reason):
- A High-risk empirical claim rated `UNSUPPORTED`, `OVERSTATED`, or contradicted, or a safety-relevant statement not supported.
- A citation that does not exist, is attributed to the wrong authors/year, or does not support its sentence (`major` if it is only misattributed, `blocking` if the claim rests on it alone).
- A fabricated or unverifiable reference.
- Claude and Copilot reach contradictory conclusions on a High claim, and `<AUTHOR>` has not decided.
- Any `AUTHOR DECISION REQUIRED` item that changes production text.
- Changes made since the report that add or strengthen a claim or change a citation, not yet re-reviewed by Copilot (a hash that differs after your own fixes is expected, and does not by itself invalidate the report).

**Non-blocking** (listed, not required to close): Medium-risk wording suggestions; `NEEDS CITATION` on a Low-risk, widely established statement; stylistic observations; minor APA details (the references check covers those); `CANNOT VERIFY` on a Low-risk claim that `<AUTHOR>` accepts.

Copilot's rating is never the deciding vote. Where it disagrees with Pass 4, the item goes to `<AUTHOR>` as a contradiction (see `RESEARCH_RECONCILIATION.md`, PHASE 2.5 §3.2b).

## What invalidates the result

The Copilot report and `RESEARCH_CLEAR.md` apply to one text. They are invalid, and the affected sections need a new Copilot run, when:
- the DOCX hash differs from the one in the report's front matter **and** the change adds, removes, or makes stronger an empirical claim, a number, a causal or absolute statement, or a citation;
- a citation is added, replaced, or renumbered;
- a SCIENCE sentence is touched by any later `MANUSCRIPT_REVISED.md` section.

They stay valid when a later change only softens a claim, fixes spelling, punctuation or formatting, or changes the wording of narrative, metaphor or framework text. Softening still goes through the decisions log. When in doubt, re-run the changed sections only.
