# PHASE 2.5: Manuscript Lock Audit (v1.1)

> **Pipeline position:** per chapter, between PHASE 2 (Governance) and PHASE 3 (Design + Production) · **Upstream gate:** `Governance/Trigger/GOVERNANCE_READY.md` (§1 below) · **Downstream:** PHASE 3, 3.5, 3.5A, 3.5B, 3W, and 4, which all require `Manuscript/Trigger/MANUSCRIPT_LOCKED.md`
> **Canonical paths, status ladder, triggers, and deliverables:** see `MASTER_PIPELINE_OVERVIEW.md`. If this file and the Overview disagree, the Overview wins and the discrepancy is logged.

**New in release v1.2.5 (2026-10-24).** Until now, the full content audit of a chapter (PHASE 0.9 Mode D) ran at PHASE 4 Part B, step B0. By then the design packet, the eBook, the print IDMLs, and sometimes the audiobook recording already existed. Its findings forced manuscript edits that had to flow back through every format, and one chapter's audio had already been recorded. PHASE 2.5 moves that audit to the one point where a fix is still cheap: after governance, before anything is designed, laid out, or recorded.

**New in release v1.3.0 (2026-10-31): independent research verification.** After Pass 4 (Claude), the chapter's externally verifiable claims and citations get a second, independent check in **Microsoft Copilot Researcher**, run by <AUTHOR> as a human-in-the-loop handoff (`COPILOT_HANDOFFS/COPILOT_PHASE2_5_RESEARCH_REVIEW.md`). Claude reconciles the two reviews (`RESEARCH_RECONCILIATION.md`), <AUTHOR> decides, and `RESEARCH_CLEAR.md` is written just before the lock, bound to the same hashes. See §3.2b and §5. The gate lives here, not in PHASE 2, because this phase edits the DOCX and records the lock hashes: a clearance issued earlier would be invalidated by the fixes applied here. PHASE 3 needs no new gate; it already requires the lock.

**What it does, in one line:** it reads the chapter in full for content problems, <AUTHOR> decides every finding, the approved fixes go into the DOCX (then the MD), and the chapter's manuscript is **locked** with its hashes recorded.

**The order (<AUTHOR>, 2026-10-24):**
1. **Before PHASE 1:** the DOCX is semi-locked (PASS 7 and the polish window), as before.
2. **PHASE 1 and PHASE 2:** as before.
3. **PHASE 2.5:** the lock audit. Output: a decisions log and `MANUSCRIPT_LOCKED.md`.
4. **PHASE 3, 3.5, 3.5A, 3.5B, 3W, and 4:** each requires `MANUSCRIPT_LOCKED.md`.
5. **PHASE 4 Part B, B0:** a cross-chapter consistency check and a check of what changed since each chapter's lock. It is no longer a full content audit.
6. **PHASE 4 Part C:** the audiobook is recorded only after the lock, so a re-recording should never be needed.

---

**Purpose:**
Find everything in the chapter that a reader, a layout, a narrator, or a question-answering system would get wrong or contradictory, and settle it **before** design. This is the last point where a wording fix is one edit in one file. After the lock, the same fix touches the eBook, the print IDMLs, the workbook, Kindle, the audiobook, and both vector stores.

PHASE 2.5 is **report-first**: it never changes the manuscript on its own. It changes the DOCX only to apply decisions <AUTHOR> has written down, with a backup and a change log.

## What it is, and what it isn't

| PHASE 2.5 is | PHASE 2.5 is not |
|---|---|
| A full read-through of one chapter for content: definitions, cross-references, terms, list counts, glossary, acronyms, headings, figures | A voice, style, or line edit. <AUTHOR>'s voice is settled in PASS 7 |
| PHASE 0.9's Pass 1 and Pass 2, run on the governed chapter against the book ledger (Mode P, extended to the full category set) | A re-run of PHASE 2. Governance checks the derived artifacts against the manuscript; this checks the manuscript against itself and the rest of the book |
| The author's decision loop, then a DOCX-first apply | An auto-fixer. Nothing is applied without a written decision |
| The lock: the DOCX and MD hashes, recorded once | A lock on the derived artifacts. Those stay governed by PHASE 2 |

---

## 1. Entry gate

All of these must hold. If any fails, write `Manuscript/Trigger/MANUSCRIPT_LOCK_INCOMPLETE.md` naming the failure, and tell <AUTHOR>.

1. **Governance passed.** `<CH_ROOT>/Governance/Trigger/GOVERNANCE_READY.md` exists and isn't superseded.
2. **Both manuscript files exist:** `<CH_ROOT>/Manuscript/<ChapterName>_Manuscript.docx` (canonical) and `_Manuscript.md` (replica).
3. **DOCX = MD.** `python <LOCAL_TOOLS_ROOT>/docx_md_sync.py <docx> <md>` (dry run) reports 0 blocks rewritten and 0 dropped. If it doesn't, the MD is out of date: run it with `--apply` (backup first) before the audit, and record that in the report. The MD is never hand-patched.
4. **No revision is pending.** If `Manuscript/Trigger/MANUSCRIPT_REVISED.md` has a section newer than `GOVERNANCE_READY.md`, PHASE 1 and PHASE 2 haven't caught up with it yet. Stop, and say so.
5. **The book-level audit inputs exist:**
   - `_BookGovernance/Audit/Audit_Config.json` and `Audit_CanonicalTerms.json` (PHASE 0.9 Mode F);
   - the latest book ledger: the `ledger.json` of the newest run folder in `_BookGovernance/Audit/` (Mode F, or an earlier lock audit);
   - the book glossary (`glossaryPath` in the config) and `_BookGovernance/Glossary/Glossary_Canonical.json`, if it exists.

A protected chapter (see the runner's `protectedChapterFolders`) is never audited by the automation. <AUTHOR> runs PHASE 2.5 for it with Claude in chat, if at all.

---

## 2. Inputs

| Input | Location | Used for |
|---|---|---|
| Manuscript DOCX (canonical) and MD (replica) | `<CH_ROOT>/Manuscript/` | The text audited. Read the MD for the passes; quote locations by heading, so they hold in both |
| Book ledger | `_BookGovernance/Audit/<latest RUN_ID>/ledger.json` | What the other chapters say: terms, equations, thresholds, lists, figures, cross-references |
| Canonical terms and config | `_BookGovernance/Audit/Audit_CanonicalTerms.json`, `Audit_Config.json` | Canonical forms, definitions, known corrections, the voice note |
| Glossary | `glossaryPath`; `_BookGovernance/Glossary/Glossary_Canonical.json` (defining-chapter rules) | Glossary gaps and conflicts; which chapter defines a term |
| The chapter's governed records | `Governance/<ChapterName>_GlossaryNormalized.json`, `_FigureRegistry.json`, `_CrossReferenceReport.md` (PHASE 2) | Figure numbers and captions, terms this chapter defines, governance's cross-reference results |
| The other chapters' locked manuscripts | `Chapters/<Other>/Final/Manuscript/` where `MANUSCRIPT_LOCKED.md` exists (read-only) | Confirming a cross-reference ("see Chapter 7") or a conflict the ledger points to |
| Exercise registry | `_BookGovernance/Workbook/Workbook_ExerciseRegistry.json` | Exercise IDs the manuscript names |

---

## 3. Steps

### 3.1 Read-through (PHASE 0.9 Pass 1 → Pass 2)

1. **Pass 1, extract,** on the chapter's MD, exactly as in PHASE 0.9: headings, terms, acronyms, equations, thresholds, lists, figures, cross-references. Save `pass1/<ChapterName>_Pass1.json` in the run folder (§5).
2. **Merge** this chapter's entries into a copy of the latest ledger, replacing the chapter's older entries. Keep every location.
3. **Pass 2, detect,** against that ledger, the glossary, and `Audit_CanonicalTerms.json`, with the full category list in §4. Use PHASE 0.9's shared system prompt and Pass 2 prompt unchanged; add the lock-audit categories from §4 to the category list. Save `pass2/<ChapterName>_Pass2.json`.
4. **Confirm before reporting.** For every cross-chapter finding, open the other chapter's manuscript and check the excerpt is real. A ledger entry for a chapter that isn't locked yet is evidence, not proof: mark the finding `needs_author_review` and name that chapter.
5. **Pass 3** (evaluation questions), if `pass3.enabled`. The chapter's headings are now about to be fixed, so this is the right time to write its evaluation set. Save `pass3/<ChapterName>_EvalSet.jsonl`; it goes to `EvalSet/<EDITION>/` once the chapter is locked.
6. **Pass 4, science and source verification** (v1.3.0, always on). Run PHASE 0.9's *Pass 4* on the chapter: extract the science-type claims, rate their risk, confirm every cited source exists and says what the sentence says, and save `_BookGovernance/References/ScienceClaims/<ChapterName>_ScienceClaims.md`. Its Medium and High claims join Pass 2's findings in the category **SCIENCE** (§4), so they land in the decisions log with everything else. On a revision, run it on the changed sections only. Local models never rate a claim.

7. **Copilot research handoff (v1.3.0).** Write `<CH_ROOT>/Governance/Research/Copilot_Research_Handoff.md`: the upload manifest from `COPILOT_HANDOFFS/COPILOT_PHASE2_5_RESEARCH_REVIEW.md` with the real paths and the DOCX SHA-256 as `reviewedSha256`, so <AUTHOR> can run it and fill the same hash into the report. Do not paste Pass 4's conclusions into the prompt (they would anchor the second reviewer); the `ScienceClaims` file is an optional upload after Copilot has made its own claim list. Skip this step when `<CH_ROOT>/Governance/Copilot/Copilot_Waivers.md` has a `research: waived — <reason> (<initials> <date>)` line (the waiver table is in `COPILOT_HANDOFFS/COPILOT_HANDOFF_STANDARD.md`). A chapter locked before v1.3.0 needs no research handoff unless it opts in (§7).

If a chapter is too long for the model's context, split it at H2 headings and carry the ledger between parts, as PHASE 0.9 does.

### 3.2 Findings report and decisions log

Write two files:

- **The findings report:** `<CH_ROOT>/Governance/<ChapterName>_LockAudit_<YYYYMMDD_HHMM>.md` (+ `.json` with the raw findings). Sections: Summary (counts by category and severity), Blocking, Major, Minor (table), Cross-chapter findings, Glossary delta, and Not checked (anything the run couldn't confirm, and why).
- **The decisions log:** `<CH_ROOT>/Manuscript/<ChapterName>_LockDecisions.md`. One row per finding, every severity:

| # | Category | Severity | Location (heading › paragraph) | Manuscript text (≤ 25 words) | Conflicts with | Issue | Suggestion | **Decision** | Applied |
|---|---|---|---|---|---|---|---|---|---|

Leave **Decision** and **Applied** blank. Then stop with the lock pending (§3.3). Don't apply anything in the same run as the audit.

### 3.2b Copilot research verification and reconciliation (v1.3.0)

The pipeline never invokes Copilot. The steps are:

1. 🤖 The audit run (§3.1 step 7) writes the handoff list. The email says "PHASE 2.5: <n> findings to decide; research review to run in Copilot".
2. 🧑 <AUTHOR> runs the Researcher review in Microsoft Copilot (any time while filling in the decisions log) and saves `Governance/Research/COPILOT_RESEARCH_REPORT.md`, with the front-matter block filled in.
3. 🤖 On the next run (`_Pipeline/RERUN_P2.5.md`), **before** reading the decisions (§3.3), Claude:
   - **Validates the report:** the front matter lists the manifest files; `manuscriptSha256` equals the DOCX hash recorded as `reviewedSha256` in `Governance/Research/Copilot_Research_Handoff.md` (the text Copilot was given; the DOCX will differ from it after fixes are applied, which is expected). A report with a different hash, or no front matter, is rejected. Whether the report is still good for the text now being locked is decided by what changed since: list the decisions log's applied rows and apply the invalidation rules in §7 step 4a (softening-only changes keep it valid; added or strengthened claims, numbers, causal or absolute statements, and new or changed citations need a Copilot re-run on those sections).
   - **Verifies Copilot's claims itself.** For every claim Copilot rated `UNSUPPORTED`, `OVERSTATED`, `NEEDS CITATION`, or contradicted, and every reference it says does not exist or is wrong: open the source Copilot names (it must have a URL or DOI that resolves) and check the finding. A source that does not resolve is itself a finding against the report (`unverifiable Copilot source`), not evidence. Copilot's `VERIFIED` is evidence, not a verdict. Never copy Copilot text into the manuscript or records without checking it.
   - **Writes `Governance/Research/RESEARCH_RECONCILIATION.md`.** One row for each claim where the two reviews differ, or where either rates it Medium/High or flags a reference:

| Claim ID | Manuscript claim (≤ 25 words) | Pass 4 (Claude) conclusion | Copilot conclusion | Source disagreement | Claude's check | Recommended resolution (smallest defensible wording, a citation, or keep) | Blocking? | **Author decision** |
|---|---|---|---|---|---|---|---|---|

   Claims both reviews rate Low and agree on are counted, not listed. Claims Copilot found that Pass 4 missed are added as new SCIENCE findings.
   - **Adds a row to the decisions log** for each reconciliation row that needs a decision (category **SCIENCE**, Suggestion = the smallest correction), with **Decision** blank. If any new blank row was added, stop with the lock pending (§3.3). <AUTHOR> decides, and re-runs.
4. **No report, no fixes.** When the research review is required (not waived, not a pre-v1.3.0 chapter) and no valid report exists, the apply run does not edit the DOCX. It stops with `RESEARCH_INCOMPLETE.md` ("Waiting: Copilot research report") so the report always describes the text that is about to be changed.
5. Copilot never edits the manuscript, and a Copilot suggestion is never applied without a written Decision. Personal narrative, metaphor, framework definitions and exercises are not research findings, whatever Copilot says about them.

**Blocking vs non-blocking research findings:**

| Blocking (closed before `RESEARCH_CLEAR.md`) | Non-blocking (listed, never a reason to wait) |
|---|---|
| A High-risk claim rated unsupported, overstated or contradicted, or a safety-relevant statement not supported | Medium-risk wording suggestions |
| A citation that doesn't exist, is misattributed, or doesn't support its sentence | `NEEDS CITATION` on a Low-risk, well-established statement |
| A fabricated or unverifiable reference | Style observations; minor APA details (the references check owns these) |
| Pass 4 and Copilot contradict each other on a High claim and <AUTHOR> hasn't decided | `CANNOT VERIFY` on a Low-risk claim <AUTHOR> accepts |
| An `AUTHOR DECISION REQUIRED` item that changes production text | |
| Changes made since the report that add or strengthen a claim or change a citation and have not been re-reviewed by Copilot (or waived) | |

"Closed" means: softened, cited, removed, kept by <AUTHOR> with initials and a reason, or with an outside reviewer. It is never closed on an AI verdict alone (Claude's or Copilot's).

### 3.3 The author-decision loop

<AUTHOR> fills in the **Decision** column. Each row takes one of:

| Decision | Meaning | What happens |
|---|---|---|
| `Fix` | Apply the suggestion as written | Applied in §3.4 |
| `Fix: <wording>` | Apply <AUTHOR>'s own wording instead | Applied in §3.4, verbatim |
| `Keep — <reason>` | The text is right as it is (an intentional choice, a voice decision, a false positive) | Nothing changes. The reason is recorded, and the same finding isn't raised again for this chapter |
| `Canonical: <form or definition>` | The finding is a book-wide decision (which definition, which spelling, which list) | Added to `Audit_CanonicalTerms.json` (and `Audit_Config.json` → `canonicalTerms` / `knownCorrections`), then applied here. Other chapters that are already locked are listed for <AUTHOR> as cross-chapter follow-ups; they are not edited by this run |
| `Defer — <chapter>` | Only for a cross-chapter finding whose other side is in a chapter that isn't locked yet | Carried to that chapter's lock audit. It doesn't block this lock |
| `Cite: <source>` | SCIENCE findings: replace or add the source the sentence relies on (author's choice, verified before it is applied) | Applied in §3.4 after the source is opened and checked |
| `Reviewer — <who>` | SCIENCE findings: send the claim to an outside reviewer (neuroscientist, clinical psychologist, physiologist) | The claim goes in `ScienceClaims_ReviewerPacket_<scope>.md`. It doesn't pass until the reviewer answers or <AUTHOR> decides `Fix`, `Keep — <reason>` with initials. A `blocking` SCIENCE finding can't be left at `Reviewer` when the lock is written |

To save time, <AUTHOR> may decide a whole group in one row at the end of the table: for example `All minor: Fix` or `All minor TERM_DRIFT: Fix`. Individual rows override a group row.

When <AUTHOR> isn't present (always, in automated runs), the log is the only channel. <AUTHOR> fills it in, then creates `<CH_ROOT>/_Pipeline/RERUN_P2.5.md` (any notes inside go to Claude). On that run:

1. Read the decisions log first.
2. A row whose manuscript text no longer matches (the DOCX changed since the audit) is re-evaluated, not applied.
3. Blank rows block the lock. A **blocking** finding can be closed only by `Fix`, `Fix: …`, `Canonical: …`, or `Keep — <reason>` with <AUTHOR>'s initials.

### 3.4 Apply: DOCX first, then the MD

1. **Back up** both files to `<CH_ROOT>/Governance/_Backups/<YYYYMMDD_HHMM>_lockaudit/Manuscript/`.
2. **DOCX (canonical):** edit each decided row in place. Change only the runs that differ, and keep the paragraph and character styles, comments, and section breaks. Never regenerate the DOCX from the Markdown.
3. **MD (replica):** bring it in line with the DOCX with `docx_md_sync.py`:
   ```
   python <LOCAL_TOOLS_ROOT>/docx_md_sync.py <CH_ROOT>/Manuscript/<ChapterName>_Manuscript.docx <CH_ROOT>/Manuscript/<ChapterName>_Manuscript.md
   ```
   Read the dry-run list: every rewritten block must be one of the decided rows, and nothing may be dropped. Then run it again with `--apply`. A third dry run must report 0 rewritten and 0 dropped.
4. **Fill the Applied column** with the before → after text (≤ 25 words each side) and the date.
5. **Version:** increment `chapterVersion` in `Governance/<ChapterName>_VersionMetadata.json` (patch level), set `revisionDate`, and add a `majorChanges` entry: `"Lock audit (PHASE 2.5): <n> fixes applied"`. If nothing was applied, leave the version alone.
6. **Figures and glossary records:** a decided caption change is also written to `Governance/<ChapterName>_FigureRegistry.json`; a decided definition is written to `_GlossaryNormalized.json`. Both are backed up first.

### 3.5 Delta re-check and downstream impact

1. **Re-run Pass 1 → Pass 2 on the changed sections only.** A fix must not introduce a new conflict. A new finding goes back into the decisions log (§3.3), and the lock waits for it.
2. **Downstream impact list.** Search the chapter's derived artifacts for the old wording of every applied fix: ReviewPacket, ReferenceGuides, Workbook (the exercise DOCX and every exercise ID the fix touches, against the registry), Training, Slides, InDesign prep (pull quotes, callout recommendations), the Audiobook narration script, eBook HTML blocks, Marketing Intake (claims registry, terminology lock, voice samples), the PHASE 1 RAG packet, and the DesignPacket staging in `DesignPacket/uploads/`.
   - **A verbatim quotation of the old wording** (a pull quote, a claim, a voice sample, a staged design file) is updated to the new wording, with a backup and a log line. This is the same Tier A rule PHASE 2 uses.
   - **Anything else** (a paraphrase, a slide that teaches the old definition, a workbook prompt) is listed as needing PHASE 2. The lock waits: <AUTHOR> creates `_Pipeline/RERUN_P2.md`, PHASE 2 re-validates and re-issues `GOVERNANCE_READY.md`, and PHASE 2.5 then runs again in confirm mode (§3.6).
   - The workbook manuscript is governed by PHASE 3W: a hit there is fixed in the workbook DOCX, its MD is regenerated, and the W0 gate (`WORKBOOK_MANUSCRIPT_READY.md`) is re-run.

### 3.6 Confirm mode (a re-run after the decisions are applied)

When PHASE 2.5 runs again and the decisions log is fully decided and applied, it doesn't re-audit the whole chapter. It checks:
- DOCX = MD (`docx_md_sync.py` dry run: 0 rewritten, 0 dropped);
- every row is decided, and every `Fix` row is applied;
- the delta re-check (§3.5.1) is clean;
- the downstream impact list is closed;
- `GOVERNANCE_READY.md` is newer than the last applied fix, if PHASE 2 had to re-validate.

Then it writes the lock (§5).

---

## 4. Finding categories

PHASE 0.9's Pass 2 categories, all of them, with the eight lock-audit categories first. Severity follows PHASE 0.9 (`blocking`, `major`, `minor`).

| Category | What it catches | Example |
|---|---|---|
| **DEFINITION_CONFLICT** | A term defined differently here than in another chapter, the glossary, or `Audit_CanonicalTerms.json` | A framework term defined as a "practice" here and a "state" in its defining chapter |
| **CROSS_REF** | A "see Chapter / Section / Figure / Exercise" that points to something missing, renumbered, or not saying what is claimed | "As we saw in Chapter 4" for an idea Chapter 4 never introduces |
| **TERM_DRIFT** | A framework term spelled, capitalized, or worded differently from canonical | "the decision index" for "The Decision Integrity Index" |
| **LIST_COUNT** | A stated count that doesn't match its items, or a named list whose items differ from another chapter | "three steps" followed by four |
| **GLOSSARY_GAP** | A term this chapter defines that the glossary lacks, a glossary term never used, or a definition the glossary words differently. Follows the defining-chapter rule in `Glossary_Canonical.json` | A new term defined in the chapter and missing from the glossary |
| **ACRONYM** | Used before it's expanded, expanded two ways, or never expanded | An abbreviation in the opening section, expanded only at the end |
| **HEADING_ANCHOR** | Duplicate headings, skipped levels, or headings too vague to serve as a citation anchor in RAG and the eBook navigation | "Overview" under three different H2s |
| **FIGURE** | A figure referenced but missing, present but never referenced, numbered out of order, or a caption that contradicts the text or the FigureRegistry | "(see Figure 3)" in a chapter with two figures |
| EQUATION | The same formula written differently, renamed variables, an undefined variable | |
| THRESHOLD | Score bands or cut-offs that disagree across chapters | |
| KNOWN_CORRECTION | An instance of a term on the known-corrections list | |
| **SCIENCE** (v1.3.0) | A scientific, neurobiological, physiological or psychological claim, or a cited source, that Pass 4 rated Medium or High: an absolute or overstated causal claim, a specific number or mechanism, a source that doesn't say what the sentence says, a citation that doesn't resolve, a safety-relevant claim. Severity: a contradicted or safety-relevant High is `blocking`, other High is `major`, Medium is `minor` | "Negative thoughts all start in the body" (no source; absolute) |

**Not findings:** voice, style, metaphor, sentence rhythm, and capitalized framework terms that match canonical. The shared system prompt's voice note applies. When unsure, mark `confidence: low` and `needs_author_review: true` rather than guessing.

---

## 5. Outputs and trigger

| Output | Path |
|---|---|
| Run folder (Pass 1, Pass 2, Pass 3 files; the updated ledger) | `<BOOK_ROOT>/_BookGovernance/Audit/<YYYYMMDD>_L_<ChapterName>/` → `pass1/`, `pass2/`, `pass3/`, `ledger.json` |
| Findings report | `<CH_ROOT>/Governance/<ChapterName>_LockAudit_<YYYYMMDD_HHMM>.md` + `.json` |
| **Decisions log** | `<CH_ROOT>/Manuscript/<ChapterName>_LockDecisions.md` |
| Locked snapshot (for the B0 delta check) | `<CH_ROOT>/Manuscript/_Locked/<ChapterName>_Manuscript_v<chapterVersion>.docx` + `.md` |
| Copilot research report (saved by <AUTHOR>) | `<CH_ROOT>/Governance/Research/COPILOT_RESEARCH_REPORT.md` (+ `_part2.md` …) |
| Research reconciliation (Claude) | `<CH_ROOT>/Governance/Research/RESEARCH_RECONCILIATION.md` |
| **Research gate** | `<CH_ROOT>/Governance/Research/RESEARCH_CLEAR.md`, or `RESEARCH_INCOMPLETE.md` |
| **Lock trigger** | `<CH_ROOT>/Manuscript/Trigger/MANUSCRIPT_LOCKED.md`, or `MANUSCRIPT_LOCK_INCOMPLETE.md` |

The run folder's `ledger.json` becomes the latest book ledger. The next chapter's lock audit, and B0, start from it.

**`RESEARCH_CLEAR.md`** is written just before the lock, after every fix is applied and DOCX = MD, so its hashes are the locked hashes. Rename any existing one to `RESEARCH_CLEAR_superseded_<YYYYMMDD_HHMM>.md` first. It is written only when:
- Pass 4 ran and (unless waived) a current Copilot report was reconciled;
- no **blocking** research finding is open (§3.2b);
- the reference list matches the approved citations (every marker resolves to one reference; `references_check.py` shows no unresolved item);
- terminology is consistent with the terminology lock (no SCIENCE fix introduced a new term);
- every accepted wording correction was applied through the decisions log (Applied column filled), none silently;
- <AUTHOR>'s decisions are recorded with initials.

```
# RESEARCH_CLEAR — <ChapterName>
clearedAt: <ISO date-time>
docxSha256: <hash>      # equals MANUSCRIPT_LOCKED.md docxSha256
mdSha256: <hash>
passFour: <ScienceClaims file>  (High <n> · Medium <n> · sourcesChecked <n of n>)
copilotReport: <file name>   |   waived — <reason> (<initials> <date>)
copilotReportSha256: <the reviewed DOCX hash, = reviewedSha256 in Copilot_Research_Handoff.md>
reconciliation: Governance/Research/RESEARCH_RECONCILIATION.md  (rows <n> · decided <n> · blocking open 0)
changesAfterReport: none | softened-only (<n> rows, listed) | rerun sections: <list>
referenceList: matches approved citations (<n> references)
authorApproval: <initials> <date>
```

If the text changed after the Copilot report in a way that adds or strengthens an empirical claim, a number, a causal or absolute statement, or changes a citation, the report is stale for those sections: re-run the Copilot review on them first (§7). Softening-only fixes keep it valid. Otherwise write `RESEARCH_INCOMPLETE.md` naming what is open.

**`MANUSCRIPT_LOCKED.md`** is written only when every item of the exit gate (§6) holds, which now includes `RESEARCH_CLEAR.md`. Before writing it, rename any existing one to `MANUSCRIPT_LOCKED_superseded_<YYYYMMDD_HHMM>.md`. It records:

```
# MANUSCRIPT_LOCKED — <ChapterName>
lockedAt: <ISO date-time>
chapterVersion: <version>
runId: <YYYYMMDD>_L_<ChapterName>
docx: <CH_ROOT>/Manuscript/<ChapterName>_Manuscript.docx
docxSha256: <hash>
md: <CH_ROOT>/Manuscript/<ChapterName>_Manuscript.md
mdSha256: <hash>
docxEqualsMd: yes (docx_md_sync.py dry run: 0 rewritten, 0 dropped)
findings: blocking <n> · major <n> · minor <n>
decisions: fix <n> · keep <n> · canonical <n> · deferred <n> (to: <chapters>)
scienceClaims: High <n> (softened/cited <n> · kept by author <n> · with outside reviewer <n>) · Medium <n> · sourcesChecked: <n of n resolve> · file: _BookGovernance/References/ScienceClaims/<ChapterName>_ScienceClaims.md
researchClear: Governance/Research/RESEARCH_CLEAR.md (clearedAt <date>; hashes equal this lock)  |  not applicable (locked before v1.3.0)
decisionsLog: Manuscript/<ChapterName>_LockDecisions.md
snapshot: Manuscript/_Locked/<ChapterName>_Manuscript_v<version>.docx / .md
governanceReady: <date of the GOVERNANCE_READY.md this lock follows>
```

Otherwise write `MANUSCRIPT_LOCK_INCOMPLETE.md` listing what is open: blank decisions, unapplied fixes, a new delta finding, an open impact item, or a failed DOCX = MD check.

**A stale lock is never left in place.** The lock is stale when either hash no longer matches the files, or when `MANUSCRIPT_REVISED.md` has a section newer than the lock. Every downstream gate checks both.

---

## 6. PHASE 2.5 exit gate

`MANUSCRIPT_LOCKED.md` is written when:
- [ ] the chapter has Pass 1 and Pass 2 files (and Pass 3, if enabled) in the run folder;
- [ ] every finding in the decisions log has a Decision, and no **blocking** finding is open;
- [ ] every `Fix`, `Fix: …`, and `Canonical: …` row is applied, DOCX first, with the Applied column filled;
- [ ] every `Canonical: …` decision is in `Audit_CanonicalTerms.json`;
- [ ] Pass 4 ran: the chapter has a `ScienceClaims` file, every cited source resolves, and every **High** science claim is softened, cited, removed, kept by <AUTHOR> with initials and a reason, or sitting with an outside reviewer (never on an AI verdict alone). A `blocking` SCIENCE finding is closed, not deferred;
- [ ] `RESEARCH_CLEAR.md` is written and its hashes equal the files being locked (v1.3.0; a chapter locked before v1.3.0 needs it only when it opts in, §7);
- [ ] DOCX = MD (`docx_md_sync.py`: 0 rewritten, 0 dropped);
- [ ] the delta re-check is clean and the downstream impact list is closed;
- [ ] the locked snapshot is saved, and the hashes are recorded.

PHASE 3 (A0 included), 3.5, 3.5A, 3.5B, 3W, and 4 do not start for the chapter without a current `MANUSCRIPT_LOCKED.md`.

---

## 7. After the lock: changing the manuscript

After the lock, any change to the manuscript needs `Manuscript/Trigger/MANUSCRIPT_REVISED.md` **and <AUTHOR>'s approval**:

1. <AUTHOR> edits the DOCX, then brings the MD in line with `docx_md_sync.py`, and bumps the version.
2. <AUTHOR> adds a dated section to `MANUSCRIPT_REVISED.md`: the changed sections, the reason, and an **Approved: <initials> <date>** line. A section without the approval line is not acted on.
3. PHASE 1 re-runs for the changed sections, and PHASE 2 re-validates (PHASE 1, "Revision trigger").
4. PHASE 2.5 runs a **delta audit** of the changed sections only (§3.1 on those sections, then §3.2–§3.6) and writes a new `MANUSCRIPT_LOCKED.md` with the new hashes. The old lock is superseded.
4a. **Research gate (v1.3.0).** The delta audit decides whether the change touches research:
   - **Re-run Pass 4 and the Copilot Researcher review on the changed sections** when the revision adds, removes or strengthens an empirical claim, a number, a causal or absolute statement, or removes a hedge; adds, replaces or renumbers a citation; or touches any sentence listed in the chapter's `ScienceClaims` file. The old `RESEARCH_CLEAR.md` is superseded and a new one is written for the new hashes.
   - **No Copilot re-run** when the revision only softens a claim, or changes spelling, punctuation, formatting, narrative, metaphor or framework wording. Pass 4 still re-checks the changed sentences, and the new `RESEARCH_CLEAR.md` records `changesAfterReport`.
   - The same rule applies to PHASE 4 Part 0 wording changes taken from the eBook PDF.
   - **Opting a pre-v1.3.0 chapter in:** a `MANUSCRIPT_REVISED.md` section titled "Copilot research retrofit" (approved as above) runs §3.2b for the whole chapter, applies any decided fixes, and writes `RESEARCH_CLEAR.md` with the new lock.
5. Anything already built from the old text (the eBook, the print IDMLs, the workbook) carries the change by hand, as before. PHASE 4 Part 0 stops if the revision is newer than the eBook PDF.

The one other sanctioned path is PHASE 4 Part 0: a difference between the final eBook PDF and the locked manuscript is a post-lock change too, so it is applied only with <AUTHOR>'s decision in `_Pipeline/P4_DECISIONS.md` (PHASE 4, 0.3).

---

## 8. Rules

- **The DOCX is canonical.** Fixes go into the DOCX first; the MD follows through `docx_md_sync.py`, never by hand.
- **No decision, no edit.** Nothing is applied without a written Decision in the log. The audit run and the apply run are separate.
- **Flag; never rewrite.** Suggestions are one line. Voice and style are not findings.
- **One chapter at a time.** The run may read every other chapter, but it edits only this chapter's manuscript and records, plus `Audit_CanonicalTerms.json` / `Audit_Config.json` for `Canonical:` decisions and its own run folder in `_BookGovernance/Audit/`.
- **A locked chapter isn't reopened by another chapter's audit.** A conflict with an already-locked chapter is listed for <AUTHOR> as a cross-chapter follow-up; if <AUTHOR> wants that chapter changed, it goes through its own `MANUSCRIPT_REVISED.md`.
- **Science is verified, not assumed (v1.3.0).** AI output, the Deep Researcher workflow's included, is evidence and never a verdict. Every returned source is opened and existence-checked. Ollama and phi4 may retrieve or format; they never rate a claim or a source. Suggested wording for a SCIENCE finding is one line and softer, not stronger; <AUTHOR> decides the wording.
- **Copilot is a second opinion, never a source of truth (v1.3.0).** Its report is evidence. Claude verifies each source it names, and neither Claude's nor Copilot's verdict closes a High claim. Copilot never edits the manuscript, and nothing in this pipeline invokes it.
- **Protected chapters** are never processed by the automation.
- **Back up before every edit** (`Governance/_Backups/<YYYYMMDD_HHMM>_lockaudit/`); never delete.
- **Never leave a stale trigger.** Rename older READY and LOCKED files to `*_superseded_<timestamp>.md`.

---

# How to run

**Automatic (default).** When PHASE 2 passes and writes `GOVERNANCE_READY.md`, the runner starts PHASE 2.5 for the chapter.

1. 🤖 **Audit run:** §1 gate → §3.1 read-through → §3.2 report and decisions log. 📧 Email: "PHASE 2.5: <n> findings to decide", with the decisions log path.
2. 🧑 **<AUTHOR>:** open `Manuscript/<ChapterName>_LockDecisions.md`, fill in every **Decision**, then create `_Pipeline/RERUN_P2.5.md`.
3. 🧑 **<AUTHOR>, in parallel:** run `COPILOT_HANDOFFS/COPILOT_PHASE2_5_RESEARCH_REVIEW.md` in Microsoft Copilot (Researcher) and save `Governance/Research/COPILOT_RESEARCH_REPORT.md`.
3a. 🤖 **Reconcile run:** §3.2b validates the report and writes `RESEARCH_RECONCILIATION.md`; new research rows go into the decisions log. If any are blank: 📧 "N research items to decide", a second 🧑 decision round, and `RERUN_P2.5.md` again.
3b. 🤖 **Apply run:** §3.3 read decisions → §3.4 apply (DOCX, then `docx_md_sync.py`) → §3.5 delta re-check and impact → §3.6 confirm → §5 lock. 📧 Email: "manuscript locked; PHASE 3 starts", or "needs you" with what is open.
4. ✅ `Governance/Research/RESEARCH_CLEAR.md`, then `Manuscript/Trigger/MANUSCRIPT_LOCKED.md`. PHASE 3 A0 (figure prompts and the design packet) starts from it.

If the audit finds nothing, the first run writes the decisions log with no rows, and the lock, in one go.

**By hand (Claude chat, or a protected chapter).** Paste this file with the chapter's MD, the latest `ledger.json`, `Audit_Config.json`, `Audit_CanonicalTerms.json`, and the glossary, and ask for §3.1–§3.2. Decide the rows in chat, then ask for §3.4–§5. Run `docx_md_sync.py` yourself if the assistant can't run local tools.

**Without AI.** Use §4 as a checklist and read the chapter once per category. Record each finding and your decision in the decisions log, make the fixes in the DOCX, regenerate the MD with `docx_md_sync.py`, and write `MANUSCRIPT_LOCKED.md` with the two hashes (`Get-FileHash -Algorithm SHA256` in PowerShell, `sha256sum` in bash).
