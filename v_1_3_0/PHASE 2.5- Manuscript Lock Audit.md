# PHASE 2.5: Manuscript Lock Audit (v1.1)

> **Pipeline position:** per chapter, between PHASE 2 (Governance) and PHASE 3 (Design + Production) · **Upstream gate:** `Governance/Trigger/GOVERNANCE_READY.md` (§1 below) · **Downstream:** PHASE 3, 3.5, 3.5A, 3.5B, 3W, and 4, which all require `Manuscript/Trigger/MANUSCRIPT_LOCKED.md`
> **Canonical paths, status ladder, triggers, and deliverables:** see `MASTER_PIPELINE_OVERVIEW.md`. If this file and the Overview disagree, the Overview wins and the discrepancy is logged.

**New in release v1.2.5 (2026-10-24).** Until now, the full content audit of a chapter (PHASE 0.9 Mode D) ran at PHASE 4 Part B, step B0. By then the design packet, the eBook, the print IDMLs, and sometimes the audiobook recording already existed. Its findings forced manuscript edits that had to flow back through every format, and one chapter's audio had already been recorded. PHASE 2.5 moves that audit to the one point where a fix is still cheap: after governance, before anything is designed, laid out, or recorded.

**New in release v1.3.0 (2026-10-31): independent research verification.** After Pass 4 (Claude), the chapter's externally verifiable claims and citations get a second, independent check in **Microsoft Copilot Researcher** (or a regular Copilot Chat if Researcher fails), run by <AUTHOR> as a human-in-the-loop handoff (`COPILOT_HANDOFFS/COPILOT_PHASE2_5_RESEARCH_REVIEW.md`). Claude reconciles the two reviews (`RESEARCH_RECONCILIATION.md`), <AUTHOR> decides, and `RESEARCH_CLEAR.md` is written just before the lock, bound to the same hashes. See §3.2b and §5. The gate lives here, not in PHASE 2, because this phase edits the DOCX and records the lock hashes: a clearance issued earlier would be invalidated by the fixes applied here. PHASE 3 needs no new gate; it already requires the lock.

**Unreleased (2026-11-16, <AUTHOR>'s decision, #42): every content check runs here, and the manuscript freezes after PHASE 4 Part 0.** For a **freeze chapter** (its lock carries a `freezePilot:` line, §5), this phase is the one place the chapter's text is checked for content: research, hedges, citations and footnote form, glossary casing, house form, callouts and the house rules in force (§3.1b). After the lock, <AUTHOR>'s small edits in the eBook and print layouts are the only routine changes; PHASE 4 Part 0 syncs them back once, and that sync is the **final lock**. After it the manuscript is read-only: a content finding goes to the next-edition log, and only a major error reopens it, through the errata step (§9). <AUTHOR> makes the edits in Word; Claude prompts each item, gives a highlighted review copy, syncs the MD and keeps one short decisions log. The pilot is the first chapter locked with the line; earlier chapters keep the process below without it.

**Unreleased (2026-11-22, <AUTHOR>'s decision, #62): the author's HumanSourceCheck before the lock.** The AI checks (Pass 4, the Copilot research review, the reconciliation) are reliable on hedging and wording. They are not proof that a source says what a sentence says: a Ch10 epigraph passed both reviews and was not in the book it was attributed to. So the lock now also needs <AUTHOR>'s own check. Once the decisions are applied, Claude builds `<CH_ROOT>/DeepResearch/<ChapterName>_HumanSourceCheck.md`, a checklist of only the claims a human must confirm, one item at a time. <AUTHOR> opens each source, marks the item, notes any fix, and signs the sheet. That signature is the author verification for the lock, and so the last step before PHASE 3 (§3.7). It applies to chapters whose first lock is written on or after 2026-11-22 (`humanSourceCheckRequired: yes`); Ch1 to Ch9 keep their locks and are checked after them.

**What it does, in one line:** it reads the chapter in full for content problems, <AUTHOR> decides every finding, the approved fixes go into the DOCX (then the MD), and the chapter's manuscript is **locked** with its hashes recorded.

**The order (<AUTHOR>, 2026-10-24):**
1. **Before PHASE 1:** the DOCX is semi-locked, i.e. editorially complete (PASS 7 and the polish window), as before.
2. **PHASE 1 and PHASE 2:** as before.
3. **PHASE 2.5:** the lock audit. Output: a decisions log and `MANUSCRIPT_LOCKED.md`.
   It ends with <AUTHOR>'s **HumanSourceCheck** (§3.7, #62): the sourced claims are checked against their sources before the lock, so before PHASE 3.
4. **PHASE 3, 3.5, 3.5A, 3.5B, 3W, 4, and 6.9 (2026-11-16):** each requires `MANUSCRIPT_LOCKED.md`.
5. **PHASE 4 Part B, B0:** a cross-chapter consistency check and a check of what changed since each chapter's lock. It is no longer a full content audit.
6. **The audiobook** is recorded only after the lock. (2026-11-16: it moved from PHASE 4 Part C to PHASE 6.9, after PHASE 6.5, because later checks still changed the text and the recordings needed pickups. Each chapter is recorded in full there.)
7. **Freeze chapters (2026-11-16, #42):** every content check is done here, before the lock (§3.1b); PHASE 4 Part 0 is the final lock; after it the manuscript is read-only, except for errata (§9).

---

**Purpose:**
Find everything in the chapter that a reader, a layout, a narrator, or a question-answering system would get wrong or contradictory, and settle it **before** design. This is the last point where a wording fix is one edit in one file. After the lock, the same fix touches the eBook, the print IDMLs, the workbook, Kindle, the audiobook, and both vector stores.

PHASE 2.5 is **report-first**: it never changes the manuscript on its own. It changes the DOCX only to apply decisions <AUTHOR> has written down, with a backup and a change log.

## What it is, and what it isn't

| PHASE 2.5 is | PHASE 2.5 is not |
|---|---|
| A full read-through of one chapter for content: definitions, cross-references, terms, list counts, glossary, acronyms, headings, figures, Chapter Summary bullet length | A voice, style, or line edit. <AUTHOR>'s voice is settled in PASS 7 |
| PHASE 0.9's Pass 1 and Pass 2, run on the governed chapter against the book ledger (Mode P, extended to the full category set) | A re-run of PHASE 2. Governance checks the derived artifacts against the manuscript; this checks the manuscript against itself and the rest of the book |
| The author's decision loop, then a DOCX-first apply | An auto-fixer. Nothing is applied without a written decision |
| The lock: the DOCX and MD hashes, recorded once | A lock on the derived artifacts. Those stay governed by PHASE 2 |

---

## 0. The lock state machine (v1.3.0)

This is the one place that says what "locked" means, who moves a chapter between states, and what sends it back. Every other file points here.

**One vocabulary for the manuscript's lifecycle:**

| Stage | Called | Set by | Evidence |
|---|---|---|---|
| After PASS 7 and the polish window | **Semi-locked** (editorially complete) | <AUTHOR> | The DOCX is settled; wording changes only through PHASE 1 Editorial Suggestions or this phase (after the lock: `MANUSCRIPT_REVISED.md`) |
| After PHASE 1 and PHASE 2 | **Governed** | PHASE 2 | `GOVERNANCE_READY.md` (Design Ready) |
| After this phase | **Research-cleared and locked** | PHASE 2.5 | `RESEARCH_CLEAR.md` (when `copilotRequired: yes`) and `MANUSCRIPT_LOCKED.md`, with the DOCX and MD hashes |
| PHASE 3 onward | **Production source** | (nothing new) | Every build reads the locked text; references are final |
| After PHASE 4 Part 0 | **Final-wording synced** | PHASE 4 | `MANUSCRIPT_SYNCED.md` |
| Freeze chapters (#42): after the first Part 0 sync | **Final lock**, then **read-only** | PHASE 4 | `MANUSCRIPT_SYNCED.md` with a `finalLock: yes` line; later content findings in the next-edition log (§9) |

The final eBook PDF does **not** create the lock. It starts the PHASE 4 final-wording verification chain.

**States inside this phase:**

| # | State | Gate file or sign | Hash of record | Moved by | What wakes the runner | Goes back to |
|---|---|---|---|---|---|---|
| S0 | Governed, ready to audit | `GOVERNANCE_READY.md` | none | PHASE 2 | automatic | none |
| S1 | Audit run done; decisions blank | `LockDecisions.md` with blank rows; `Copilot_Research_Handoff.md` | `reviewedSha256` (the DOCX before any fix) | PHASE 2.5 audit run | none | none (next: <AUTHOR> fills decisions and runs Copilot) |
| S2 | Waiting for the Copilot research report | `RESEARCH_INCOMPLETE.md` ("Waiting: Copilot research report") | `reviewedSha256` | <AUTHOR> (two-stage run in Researcher or Copilot Chat, saves the report) | **create `_Pipeline/RERUN_P2.5.md`** | stays in S2 until the report is valid and every Stage 1 claim ID is ruled by Copilot, ruled by a Claude backup, or waived by a `research-ids:` line |
| S3 | Reconciled; new research rows to decide | `RESEARCH_RECONCILIATION.md`; new blank rows in the decisions log | `reviewedSha256` | Claude (reconcile run), then <AUTHOR> decides | **`RERUN_P2.5.md`** | S3 while any blocking row is open |
| S4 | All decided; applying | Applied column filled, DOCX first, MD by `docx_md_sync.py`, delta re-check | new DOCX and MD hashes | Claude (apply run) | `RERUN_P2.5.md` | decisions pending again if the delta re-check finds a new finding (S3 for research rows); `RERUN_P2.md` first if the downstream impact list needs PHASE 2 |
| S4h | Waiting for the HumanSourceCheck (#62; `humanSourceCheckRequired: yes`) | `<ChapterName>_HumanSourceCheck.md` not signed, or rebuilt after fixes; `MANUSCRIPT_LOCK_INCOMPLETE.md` ("Waiting: HumanSourceCheck …") | the hashes on its `builtFrom:` line | <AUTHOR> (marks, notes, signs) | **`RERUN_P2.5.md`** | S3/S4 if a marked item needs a fix (§3.7 step 4), then S4h again for the re-sign |
| S5 | Research-cleared | `RESEARCH_CLEAR.md` (always written for `copilotRequired: yes`; it records any waiver) | equals the lock | Claude | automatic, in the same run | S3 if a blocking research finding or a stale report remains |
| S6 | **Locked** | `MANUSCRIPT_LOCKED.md` + `_Locked/` snapshot | `docxSha256` / `mdSha256` | Claude | PHASE 3 starts automatically | S7 |
| S7 | Revised after the lock | `MANUSCRIPT_REVISED.md` section with `Approved: <initials> <date>` | the lock's hashes until re-locked | <AUTHOR> | create `RERUN_P1.md` for the changed sections, then `RERUN_P2.md`, then `RERUN_P2.5.md` (delta audit); saving the REVISED file wakes nothing | S6 with new hashes |
| S8 | **Final-locked** (freeze chapters, #42) | `MANUSCRIPT_SYNCED.md` with `finalLock: yes` | that file's hashes | PHASE 4 Part 0 | nothing; the chapter moves on to Part A | S7 only through an `Errata` section (§9), then S6, Part 0 and S8 again |

**Paths through the states:** with `copilotRequired: yes`, S1 → S2 → S3 → S4 → S5 → S6. With `copilotRequired: no` (Ch1 to Ch5's first lock), S1 → S4 → S6. A chapter with `humanSourceCheckRequired: yes` (#62) passes through S4h after S4 on either path (S4 → S4h → S5 → S6, or S4 → S4h → S6). With `copilotRequired: no`: no research report, no `RESEARCH_CLEAR.md`, but references finished and every other exit item still apply. A downstream impact that needs PHASE 2 sends S4 through `RERUN_P2.md` (PHASE 2 re-issues `GOVERNANCE_READY.md`) and back to confirm mode.

**The sanctioned edit paths. There are no others:**

1. **This phase's decisions** (before the lock): a written Decision, DOCX first, MD from the DOCX.
2. **A `MANUSCRIPT_REVISED.md` section with <AUTHOR>'s approval line** (after the lock): wording from your eBook-pass notes, reference fixes, a research retrofit, or an author exception. Always: DOCX first, MD by `docx_md_sync.py`, a delta audit of the changed sections (including the §7 step 4a research rule), then a **new lock with new hashes**. An exception such as the 2026-10-30 Ch1 to Ch6 science-wording edits is still recorded as a REVISED section, never made out of band.
3. **PHASE 4 Part 0's accept path** (after the lock): a safety net for wording the final eBook PDF carries that the manuscript lacks. It never applies wording that adds or strengthens an empirical claim, a number, or a causal or absolute statement, or that changes a citation: those go through path 2.
4. **Errata** (freeze chapters, after the final lock; #42): a `MANUSCRIPT_REVISED.md` section titled `Errata — <criterion>: NE-<nnn>` with <AUTHOR>'s approval line, for a major error only, then path 2's chain and a new final lock (§9).

**For a freeze chapter (#42)** the paths are used in order. Path 1 is where every content check happens (§3.1b). Between the lock and Part 0, path 3 is the routine route: <AUTHOR>'s small edits in the eBook and print layouts, synced back once. Path 2 stays for a change Part 0 may not apply (a claim, a number, a citation) or one too big for a layout edit (confirmed by <AUTHOR>, 2026-11-17). After the final lock, path 4 is the only one; any other content finding goes to the next-edition log.

**The hash of record** is the DOCX and MD hash in `MANUSCRIPT_SYNCED.md` when Part 0 changed the manuscript after the lock with <AUTHOR>'s decision and the manuscript still matches those hashes (#48: hashes, not file dates; an identical-content restore is not an edit); otherwise it is the hash in `MANUSCRIPT_LOCKED.md`. Every gate that compares a hash uses this rule. After a final lock (#42) it is the final-lock file's hash, which equals the lock's when Part 0 found no differences. For a freeze chapter's workbook manuscript (#42): The workbook's hash of record is the synced DOCX and MD hash in the standing `WORKBOOK_READY.md`, or, before W3 has run, the lock's `workbook:` hash; Step 0V and PHASE 7 check it alongside the PDF hashes. The workbook hashes never make the chapter lock stale.

**Verifying sources, in one chain** (each step produces evidence; none is a verdict):

```text
Claude Pass 4 (claims, risk, source exists?) ──▶ local Deep Researcher (evidence) ──▶ your claim-by-claim review
   ──▶ Copilot Researcher, two-stage and independent ──▶ Claude reconciliation (every named source opened)
   ──▶ your decisions ──▶ your HumanSourceCheck (#62) ──▶ RESEARCH_CLEAR.md ──▶ MANUSCRIPT_LOCKED.md
```

A High claim never closes on an AI verdict alone. A source problem found **after** the lock is a path 2 revision, never an edit in InDesign.

**Ch1 to Ch5 (protected chapters).** They are locked now, like every other chapter. The runner ignores their files, so <AUTHOR> ran their first lock, and runs any re-lock, with Claude in chat: the same audit on the text at the time (Pass 1, 2 and 4, the decisions log, DOCX = MD, references finished, section 6), recording `copilotRequired: no` (author decision 2026-10-31); the research retrofit runs as a REVISED section (path 2). Their earlier `MANUSCRIPT_SYNCED.md` history carries forward. Ch1 to Ch6 stay on the pre-#42 process: no `freezePilot:` line and no final lock, unless <AUTHOR> names one.

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

A protected chapter (see the runner's `protectedChapterFolders`) is never audited by the automation. <AUTHOR> runs PHASE 2.5 for it with Claude in chat.

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

7. **Copilot research handoff (v1.3.0): build `<CH_ROOT>/DeepResearch/`.** This folder is **reference only** and the one home for the research chain. Build it with: `START_HERE.md` (the steps, in plain words); `PROMPT_PasteIntoCopilot.md` (the prompt and, after it, the "Resume at Stage 2" block, both from `COPILOT_HANDOFFS/COPILOT_PHASE2_5_RESEARCH_REVIEW.md`, filled in with the chapter name, the DOCX hash and the handoff file name); `Copilot_Research_Handoff.md` (the manifest: hashes, where each snapshot came from, `reviewedSha256`); `1_Upload_First/` (snapshots of the chapter DOCX and the glossary); and `2_Upload_Second/` (snapshots of the `ScienceClaims` file, the Deep Researcher evidence bundle, and the claims registry). Snapshots are copies, never edited. If the manuscript changes, or the prompt file's version changes (an existing folder built from the v1.1 prompt gets the current `PROMPT_PasteIntoCopilot.md` and `START_HERE.md` this way), a rebuild redoes only `START_HERE.md`, `PROMPT_PasteIntoCopilot.md`, `1_Upload_First/` and `2_Upload_Second/` for the re-run, and writes `Copilot_Research_Handoff_<n>.md` beside the earlier manifests. A rebuild never deletes or overwrites the results (`COPILOT_RESEARCH_REPORT*.md`, `RESEARCH_RECONCILIATION.md`, any superseded `RESEARCH_CLEAR`) or the earlier manifests. <AUTHOR> drags `1_Upload_First` into Copilot, then `2_Upload_Second` after Copilot's own claim list, and saves the results in this same folder. **Every Copilot re-run** (a delta audit after a revision, or a re-review of sections changed since the report, §7 step 4a) gets its own handoff file, `Copilot_Research_Handoff_<n>.md`, with its own `reviewedSha256`, the list of sections to review, and the files to upload; a re-run report is checked against that file, and the earlier report keeps its own handoff. The handoff is **two-stage** (Stage 1 uploads: the DOCX, whose References section is the reference list, and the glossary; Stage 2 uploads: the `ScienceClaims` inventory, the Deep Researcher evidence and the claims registry, and optionally the audit run's findings report, which is not snapshotted), so Pass 4's conclusions and the Deep Researcher evidence never reach Copilot until it has returned its own independent claim inventory and stopped. Skip this step when `<CH_ROOT>/Governance/Copilot/Copilot_Waivers.md` has a `research: waived — <reason> (<initials> <date>)` line (the waiver table is in `COPILOT_HANDOFFS/COPILOT_HANDOFF_STANDARD.md`). a chapter with `copilotRequired: no` needs no research handoff unless it opts in (§7).

If a chapter is too long for the model's context, split it at H2 headings and carry the ledger between parts, as PHASE 0.9 does.

### 3.1b Content checks before the lock (freeze chapters, 2026-11-16, #42)

For a freeze chapter, every content check runs here, once, before the lock. These checks used to run later: in PHASE 6.5 and in the close-out audits run in chat on finished chapters. They are **moved, not copied**: after the final lock, no phase checks a freeze chapter's text for content (§9). Each finding becomes a row in the decisions log (§3.2).

| Check | What it covers | How |
|---|---|---|
| Research | Pass 4 and the Copilot review applied, every High claim closed, `RESEARCH_CLEAR.md` (§3.1 steps 6 and 7, §3.2b) | as now |
| Hedges | Outcome promises and absolutes in empirical claims ("always", "never", "literally", "ensures", "proves") are softened ("can", "may", "helps", "is designed to"); framework definitions keep their claim and are not hedged twice | read-through; the suggestion is one softer line |
| Citations and footnote form | Every marker resolves to one reference; numbered footnotes, never in-text "(Author, year)"; the marker sits after the punctuation; lettered pointers keep their form ("(see Footnote A)") | `references_check.py`, then a read-through |
| Glossary casing and term forms | Framework terms match the terminology lock and `Glossary_Canonical.json`: capitals, a leading "The", slash forms, plural forms; plus TERM_DRIFT and GLOSSARY_GAP (§4) | Pass 2, then a read-through |
| House form | Heading punctuation, exercise titles, curly quotes and apostrophes, em dashes for emphasis only, the Chapter Summary rule (SUMMARY_FORMAT, §4) | `check_summary_format.py`, then a read-through |
| Callouts and pull quotes | The callout rules in force; each recommended callout's source sentence still exists; none sits right before the sentence it echoes | PHASE 1 callout recommendations against the text |
| Epigraph (2026-11-16/17, #47) | The chapter opens with an attributed epigraph, right after the Lesson and Core Value labels; the quotation and its attribution are verified as a source line (Pass 4 and the Copilot review, like any cited claim, then <AUTHOR>'s HumanSourceCheck, §3.7, for chapters under #62). The epigraph's book is reference 1, with no marker on the attribution line (MASTER §10, 2026-11-21). From the chapters locked on or after that date; Ch1, Ch4 and Ch6 are not retrofitted unless <AUTHOR> names them | read-through, then the research checks |
| Figures | Every figure referenced in the text and captioned (FIGURE, §4) | read-through |
| Workbook exercise | The same checks on the chapter's workbook DOCX; the workbook freezes with the chapter (§9), so its wording is settled here too | read-through |
| Typos and grammar | Spelling, agreement, doubled words, dangling clauses | read-through |
| House rules | The rules in force on the lock date (`MASTER_PIPELINE_OVERVIEW.md` section 10). A rule adopted later doesn't apply to this chapter (forward only) | the dated list |

**How it runs (simplified, #42).** <AUTHOR> makes the manuscript edits, in Word:
1. Claude writes each item in the decisions log: the heading, the exact current sentence, the suggested wording with a one-line reason, and the type, `mechanical` or `voice`.
2. Claude makes a **review copy**, `Manuscript/<ChapterName>_Manuscript_REVIEW_<YYYYMMDD>.docx` (and one for the workbook DOCX), with each spot highlighted and a comment giving the item number and the suggestion. It is never a gate input. An older review copy moves to the chapter's archive (`Chapters/<ChapterName>/ARCHIVE/<YYYYMMDD>/`, logged in `ARCHIVE_MANIFEST.md`; MASTER section 10) when a new one is made.
3. Claude puts the items to <AUTHOR> one at a time (in chat; in an automated run the log is the channel): the heading, the sentence and the suggestion. A mechanical item (marker position, pointer form, casing) can be answered `Apply for me`, and Claude applies it in the DOCX (§3.4). A voice item is <AUTHOR>'s to word in the DOCX.
4. After <AUTHOR> saves, Claude brings the MD in line with `docx_md_sync.py`, verifies it (0 dropped, and every rewritten block either a decided item or a listed known exception), re-checks the changed paragraphs (§3.5), and records each decision in its row.
5. **An author rewrite** that goes beyond the listed items gets these checks again on the rewritten paragraphs, with a new review copy, before the lock. For research, only the rewritten sentences that state or attribute a source, a claim or a number go to a **scoped Copilot re-review**: its own prompt and `Copilot_Research_Handoff_<n>.md` (§3.2b), covering just those sentences. The rest of the clearance carries forward, and `RESEARCH_CLEAR.md` records the basis, the scoped report and `changesAfterReport`.

Worked example: the pilot chapter (2026-11-16, CHANGELOG #42). The pre-build check put about 60 manuscript items, the figure items and 10 workbook items to <AUTHOR>. <AUTHOR>'s Word pass then rewrote far more than the listed items, so the new text got a second review copy (typos, house form, wording questions, claims that had got stronger). The 11 restated source sentences went to a scoped Copilot re-review (8 verified, 3 partially supported and narrowed along its suggestions), and the chapter was locked with `freezePilot:`.

### 3.2 Findings report and decisions log

Write two files:

- **The findings report:** `<CH_ROOT>/Governance/<ChapterName>_LockAudit_<YYYYMMDD_HHMM>.md` (+ `.json` with the raw findings). Sections: Summary (counts by category and severity), Blocking, Major, Minor (table), Cross-chapter findings, Glossary delta, and Not checked (anything the run couldn't confirm, and why).
- **The decisions log:** `<CH_ROOT>/Manuscript/<ChapterName>_LockDecisions.md`. One row per finding, every severity:

| # | Category | Severity | Location (heading › paragraph) | Manuscript text (≤ 25 words) | Conflicts with | Issue | Suggestion | **Decision** | Applied |
|---|---|---|---|---|---|---|---|---|---|

Leave **Decision** and **Applied** blank. Then stop with the lock pending (§3.3). Don't apply anything in the same run as the audit.

**Freeze chapters (#42): one short log.** The decisions log is the chapter's one record of its checks, §3.1b included. Its columns may be the short form `# | Category | Severity | Location (heading › paragraph) [DOCX ¶] | Current | Suggested (why) | Type (mechanical / voice) | Decision | Applied` (Category, Severity and Applied stay, because the exit gate reads them), and the findings report may be just a summary block at the top of the log (counts by category and severity, and what wasn't checked), with the raw `.json` kept. Write no other audit report.

### 3.2b Copilot research verification and reconciliation (v1.3.0)

The pipeline never invokes Copilot. The steps are:

1. 🤖 The audit run (§3.1 step 7) writes the handoff list. The email says "PHASE 2.5: <n> findings to decide; research review to run in Copilot".
2. 🧑 <AUTHOR> runs the Researcher review in Microsoft Copilot, or in a regular Copilot Chat if Researcher fails (any time while filling in the decisions log) and saves `DeepResearch/COPILOT_RESEARCH_REPORT.md`, with the front-matter block filled in, and the Stage 1 answer as `DeepResearch/COPILOT_RESEARCH_STAGE1.md`.
3. 🤖 On the next run (`_Pipeline/RERUN_P2.5.md`), **before** reading the decisions (§3.3), Claude:
   - **Validates the report:** the front matter lists the manifest files (plus the saved `COPILOT_RESEARCH_STAGE1.md` when `stage1Source` is `uploaded file`) and says `stage1Completed: yes` (the inventory was returned before any Stage 2 file was supplied; the saved `COPILOT_RESEARCH_STAGE1.md` is required and is used to confirm it (with `stage1Source: uploaded file`, Copilot writes `stage1Completed: see Stage 1 file` and the saved file alone proves independence; a report with no saved Stage 1 file is `not independent` and cannot pass the coverage check; the chapter then stays in S2 with `RESEARCH_INCOMPLETE.md` "Missing: COPILOT_RESEARCH_STAGE1.md; re-run Stage 1 or waive"), and a report that says otherwise, or that shows Stage 2 content in its Stage 1 inventory, is marked `not independent` and its claim inventory is not used as an independent check); **checks coverage:** the report's claim table must carry a row for every claim ID in the Stage 1 inventory (the saved `COPILOT_RESEARCH_STAGE1`), `rowsRuled` must equal `stage1Claims`, and Claude counts the IDs itself instead of trusting the `COVERAGE` line; any ID with no row makes the report `INCOMPLETE`: Claude writes `RESEARCH_INCOMPLETE.md` ("Missing Copilot rulings: <IDs>"), the chapter stays in S2, the reconciliation may still be written for the rows that were ruled, and no fix is applied to the DOCX (rule 4 below). No `RESEARCH_CLEAR.md` is written until Copilot rules on the missing IDs, Claude rules on them as a backup, or <AUTHOR> waives just those IDs with a `research-ids:` line in `Copilot_Waivers.md` (initials and a reason; it does not waive the research step). `RESEARCH_CLEAR.md` records the split in its `coverage:` line, and a Claude backup ruling is recorded as a backup, never as a Copilot review. A report made with the v1.1 prompt has no `stage1Claims` or `rowsRuled`: Claude counts the IDs from the saved Stage 1 file and does not reject the report for the missing fields; `manuscriptSha256` equals the `reviewedSha256` of the handoff file the report names in its `handoffFile:` line (`DeepResearch/Copilot_Research_Handoff.md`, or `Copilot_Research_Handoff_<n>.md` for a re-run), i.e. the text Copilot was given; the DOCX will differ from it after fixes are applied, which is expected. A report with a different hash, or no front matter, is rejected. Whether the report is still good for the text now being locked is decided by what changed since: list the decisions log's applied rows and apply the invalidation rules in §7 step 4a (softening-only changes and human-verified corrections, §3.7 step 5, keep it valid; added or strengthened claims, numbers, causal or absolute statements, and new or changed citations otherwise need a Copilot re-run on those sections).
   - **Verifies Copilot's claims itself.** For every claim Copilot rated `UNSUPPORTED`, `OVERSTATED`, `NEEDS CITATION`, or contradicted, and every reference it says does not exist or is wrong: open the source Copilot names (it must have a URL or DOI that resolves) and check the finding. A source that does not resolve is itself a finding against the report (`unverifiable Copilot source`), not evidence. Copilot's `VERIFIED` is evidence, not a verdict. Never copy Copilot text into the manuscript or records without checking it.
   - **Writes `DeepResearch/RESEARCH_RECONCILIATION.md`.** One row for each claim where the two reviews differ, or where either rates it Medium/High or flags a reference:

| Claim ID | Manuscript claim (≤ 25 words) | Pass 4 (Claude) conclusion | Copilot conclusion | Source disagreement | Claude's check | Recommended resolution (smallest defensible wording, a citation, or keep) | Blocking? | **Author decision** |
|---|---|---|---|---|---|---|---|---|

   Claims both reviews rate Low and agree on are counted, not listed. Claims Copilot found that Pass 4 missed are added as new SCIENCE findings.
   - **Adds a row to the decisions log** for each reconciliation row that needs a decision (category **SCIENCE**, Suggestion = the smallest correction), with **Decision** blank. If any new blank row was added, stop with the lock pending (§3.3). <AUTHOR> decides, and re-runs.
4. **No report, no fixes.** When the research review is required (not waived, not a `copilotRequired: no` chapter) and no valid, complete report exists (a report is complete when every Stage 1 claim ID is ruled by Copilot, ruled by a Claude backup, or waived by a `research-ids:` line), the apply run does not edit the DOCX. It stops with `RESEARCH_INCOMPLETE.md` ("Waiting: Copilot research report", "Missing Copilot rulings: <IDs>", or "Missing: COPILOT_RESEARCH_STAGE1.md") so the report always describes the text that is about to be changed.
5. Copilot never edits the manuscript, and a Copilot suggestion is never applied without a written Decision. Personal narrative, metaphor, framework definitions and exercises are not research findings, whatever Copilot says about them.

**Blocking vs non-blocking research findings:**

| Blocking (closed before `RESEARCH_CLEAR.md`) | Non-blocking (listed, never a reason to wait) |
|---|---|
| A High-risk claim rated unsupported, overstated or contradicted, or a safety-relevant statement not supported | Medium-risk wording suggestions |
| A citation that doesn't exist, is misattributed, or doesn't support its sentence | `NEEDS CITATION` on a Low-risk, well-established statement |
| A fabricated or unverifiable reference | Style observations; minor APA details (the references check owns these) |
| Pass 4 and Copilot contradict each other on a High claim and <AUTHOR> hasn't decided | `CANNOT VERIFY` on a Low-risk claim <AUTHOR> accepts |
| An `AUTHOR DECISION REQUIRED` item that changes production text | |
| Changes made since the report that add or strengthen a claim or change a citation and have not been re-reviewed by Copilot (or waived), unless they are human-verified corrections (§3.7 step 5) | |

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

**Freeze chapters (#42), two more values:**

| Decision | Meaning | What happens |
|---|---|---|
| `Apply for me` | A mechanical item: apply the suggestion as written | The same as `Fix`: Claude applies it in §3.4 |
| `Edited by author` | <AUTHOR> changed the passage in Word (a voice item, or <AUTHOR>'s own wording for any item) | Nothing to apply. Once the MD sync is verified, Applied records the before → after text and the row is closed. It closes a blocking finding only if the re-check (§3.5) of the new text is clean |

To save time, <AUTHOR> may decide a whole group in one row at the end of the table: for example `All minor: Fix` or `All minor TERM_DRIFT: Fix`. Individual rows override a group row.

When <AUTHOR> isn't present (always, in automated runs), the log is the only channel. <AUTHOR> fills it in, then creates `<CH_ROOT>/_Pipeline/RERUN_P2.5.md` (any notes inside go to Claude). On that run:

1. Read the decisions log first.
2. A row whose manuscript text no longer matches (the DOCX changed since the audit) is re-evaluated, not applied. A freeze chapter's `Edited by author` row is expected to differ: it is checked through §3.5, not re-evaluated as a new finding.
3. Blank rows block the lock. A **blocking** finding can be closed only by `Fix`, `Fix: …`, `Canonical: …`, or `Keep — <reason>` with <AUTHOR>'s initials; for a freeze chapter (#42) also by `Apply for me` (once applied) or `Edited by author` (once the §3.5 re-check of the new text is clean and Applied is filled). On any chapter, a row tagged `human-verified: HumanSourceCheck item <n>` (§3.7) may also be closed by `Edited by author`, on the same conditions.

### 3.4 Apply: DOCX first, then the MD

**Freeze chapters (#42):** Claude applies only the rows <AUTHOR> answered `Apply for me` (mechanical items) and `Fix` rows <AUTHOR> asked Claude to apply. <AUTHOR> edits the voice rows in Word. Step 3 (the MD) then follows for both.

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
- `GOVERNANCE_READY.md` is newer than the last applied fix, if PHASE 2 had to re-validate;
- for a chapter with `humanSourceCheckRequired: yes`, the HumanSourceCheck (§3.7) is signed and current, or waived.

Then it writes the lock (§5). Otherwise it stops with `MANUSCRIPT_LOCK_INCOMPLETE.md` and one of these lines:
- "Waiting: HumanSourceCheck": no sheet yet. It builds the sheet first.
- "Waiting: HumanSourceCheck, unsigned (items <n>)": items unmarked, missing `Opened:` or `Initials/date:` (or a bare `Opened: none` with no reason), or no valid `Signed:` line.
- "Waiting: HumanSourceCheck decisions (items <n>)": items marked for a fix, with rows not yet decided or applied. It drafts the fixes first (§3.7, step 4).
- "Waiting: HumanSourceCheck re-sign (items <n>)": the sheet was rebuilt after fixes (§3.7, step 6).

### 3.7 The author's HumanSourceCheck (#62, 2026-11-22)

**Why.** Claude's Pass 4 and Copilot's review check whether a claim is worded at the right strength. Only a person with the source open can confirm that the source says it. <AUTHOR> works best one task at a time, so the check is a checklist, not a search.

**Which chapters (forward only, like `copilotRequired`).** A chapter's **first lock written on or after 2026-11-22** records `humanSourceCheckRequired: yes`, and every later re-lock carries the value forward. A lock written earlier has no such field and counts as `no`; this covers Ch1 to Ch9. Their locks stand, and the gate never applies to their re-locks. Their sheets are worked through after the lock (step 7).

1. **When it's built.** In confirm mode (§3.6), after every decision is applied and DOCX = MD, so it quotes the text being locked. Write it to `<CH_ROOT>/DeepResearch/<ChapterName>_HumanSourceCheck.md` from `templates/HUMAN_SOURCE_CHECK_TEMPLATE.md`. Its `builtFrom:` line records the DOCX and MD sha256 it was built from.
2. **What goes in it.** Only what a human has to check, in three tiers:
   - **Tier 1, open the source.** Every epigraph and quotation with its attribution (the exact wording in the named work, and whether the epigraph's book is reference 1, MASTER §10); every number or statistic; every sentence saying what a named researcher, study or thinker found; brain and body mechanism claims, cited or not; safety-relevant lines; weak or off-topic sources (consumer sites, a page about something else).
   - **Tier 2, skim:** consensus statements, cross-chapter consistency, whether the safety lines are present.
   - **Tier 3:** no check (stories, framework constructs, exercises, encouragement); a one-line list only.

   A **Tier 1 item** is each `**<n>.` entry under the `## Tier 1` heading. Each one gives the sentence exactly as it reads (with its `^n^` markers), the reference and its DOI or URL copied from the reference list (none for a quotation from a book without one), a concrete **Check:** line, the Copilot and Pass 4 ruling labelled a **hint**, one line of boxes, an `Opened:` line (the source and page <AUTHOR> read himself, #67), a `Notes:` line, an optional `AI notes:` line (research from an AI tool that he pasted in, kept apart from his own notes), and its own `Initials/date:` line (`<initials> <YYYY-MM-DD>`). When there was nothing to open (an uncited number reworded or labelled, a source dropped, a search that found nothing), the one allowed form is `Opened: none — <why>`, for example `Opened: none — dropped, refs 4 and 5 cover it`. **Claude leaves `Opened:`, `Notes:`, `AI notes:` and `Initials/date:` blank; only <AUTHOR> fills them.** There are three box sets:
   - `Says it / Says less / Doesn't say it / Source too weak` (the default);
   - `Source found / Reword / Label as illustration` (an uncited number);
   - `Keep / Replace with a stronger source / Drop` (source quality).

   Claude writes a fact as verified only if it read the source on the page in this run, and says where (for example "read on the page in the Google Books preview, p. xvii"). Anything recalled is labelled "usually summarised as". No page, DOI or quotation is invented.
3. **Signed.** After HTML comments are stripped, the sheet is signed when:
   - every Tier 1 item has exactly one box ticked (`[x]`), an `Opened:` value (#67; a value that starts with `none` must match `^none — .+`, so a bare `none` fails) and an `Initials/date:` value;
   - the last non-blank line, trimmed, matches `^Signed: [A-Z]{2,3} \d{4}-\d{2}-\d{2}$`;
   - its `builtFrom:` DOCX hash equals the DOCX being locked;
   - every item not marked *Says it*, *Source found* or *Keep* (that is: *Says less*, *Doesn't say it*, *Source too weak*, *Reword*, *Label as illustration*, *Replace* or *Drop*) is **closed in the decisions log** (step 4).

   **Waiver.** Instead of a signature, <AUTHOR> may waive the check for the chapter with the line `human-source-check: waived — <reason> (<initials> <date>)` in `<CH_ROOT>/Governance/Copilot/Copilot_Waivers.md` (step key in `COPILOT_HANDOFFS/COPILOT_HANDOFF_STANDARD.md`).
4. **Marks and notes become decisions.** Each item not marked *Says it*, *Source found* or *Keep* becomes a SCIENCE row in the decisions log, with the tag `human-verified: HumanSourceCheck item <n>` in its Location. Claude puts <AUTHOR>'s note and a draft fix in his voice (only `Notes:` drives a draft fix, and only a note not prefixed `(earlier check, …)`; `AI notes:` is a record of what an AI tool said, never a fix on its own) in the Suggestion column ("Suggested" in the freeze short log). **The Decision is <AUTHOR>'s, never pre-filled.** Two ways it gets recorded:
   - Claude puts the draft as a tracked change into a review copy of the DOCX (`Manuscript/<ChapterName>_Manuscript_REVIEW_<date>.docx`; the freeze process's review copy, so §8's "no decision, no edit" holds). <AUTHOR> accepts or edits it in Word and saves it as the manuscript, and the row is recorded as `Edited by author`.
   - <AUTHOR> writes `Keep — <reason> (<initials>)`, for example "the source supports it at this strength after all".

   `docx_md_sync.py` runs only after the tracked changes are accepted. Then §3.4 to §3.6 run as usual.
5. **No Copilot re-run for a human-verified correction.** A correction <AUTHOR> made with the source open is `human-verified` and needs no Copilot re-run (§3.2b, §5, §7 4a). That covers:
   - a softened claim;
   - a fixed number;
   - a corrected attribution;
   - a citation renumbered, completed, or replaced **with a source already in the reviewed reference list** (the References section of the DOCX snapshot in the latest research handoff's `1_Upload_First/`).

   `RESEARCH_CLEAR.md` lists these under `changesAfterReport: human-verified (<n> rows)`. A **newly added source**, meaning one that isn't in the reference list Copilot reviewed (a replacement Copilot never saw included), goes to a scoped Copilot re-review for the sentence it supports.
   **Sheets built before #67.** On every confirm-mode run, not only a rebuild, Claude adds empty `- Opened:` and `- AI notes:` lines to any Tier 1 item that lacks them, without touching its boxes, Notes or `Initials/date:`. <AUTHOR> then fills `Opened:` on every Tier 1 item, marked or not, before signing.

6. **Rebuild and re-sign.** Applying the fixes changes the DOCX hash, so the sheet goes stale. The next run rebuilds it:
   - it writes the new hashes to `builtFrom:`;
   - for each item whose sentence changed, it updates the quoted sentence and clears that item's boxes, `Opened:` and `Initials/date:` (its `Notes:` and `AI notes:` stay as the record, each prefixed `(earlier check, <date>)`, and such notes never drive a new draft);
   - it adds a new Tier 1 item for each sourced claim, number or citation that the changed sections now contain and the sheet doesn't (numbered after the last item, so existing numbers stay stable for the decisions-log tags);
   - it marks an item whose sentence no longer exists (after a *Drop*) as `Retired: sentence removed (<date>)`, and leaves it in place with its number;
   - it keeps <AUTHOR>'s marks on unchanged items;
   - it clears the `Signed:` line.

   <AUTHOR> re-marks the rebuilt items (usually *Says it*, now that the fix is in), signs again, and creates `RERUN_P2.5.md`. The run stops with `MANUSCRIPT_LOCK_INCOMPLETE.md` ("Waiting: HumanSourceCheck re-sign (items <n>)") until then.
7. **Chapters locked before #62** (`humanSourceCheckRequired` absent or `no`). Their sheets are worked through after the lock, with the same marks. A finding is a revision through §7: a `MANUSCRIPT_REVISED.md` section with an `Approved:` line and a line `human-verified: HumanSourceCheck items <n>`, then `RERUN_P1/P2/P2.5`. After a freeze chapter's final lock, a finding goes through the errata step (§9) only if it meets one of §9's major-error criteria; otherwise it is a next-edition log row. The re-lock carries `humanSourceCheckRequired: no` forward, so it isn't gated.

---

## 4. Finding categories

PHASE 0.9's Pass 2 categories, all of them, with the lock-audit categories (the bold rows) first. Severity follows PHASE 0.9 (`blocking`, `major`, `minor`).

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
| **SUMMARY_FORMAT** (v1.3.0, minor) | A bullet in the chapter's "Chapter N Summary" that breaks the summary rule: more than two sentences (a semicolon counts as a break), or more than about 25 words; one sentence is preferred. From Chapter 7 on the summary also has no Closing Frame and no personal anecdotes (practical applications are fine); the script notes a Closing Frame, anecdotes are a read-through check. Run `python v_1_3_0/check_summary_format.py <manuscript.md>`; it lists the lines | A 39-word bullet, or three ideas joined by semicolons; a `**Closing Frame**` label in a Chapter 7+ summary |
| EQUATION | The same formula written differently, renamed variables, an undefined variable | |
| THRESHOLD | Score bands or cut-offs that disagree across chapters | |
| KNOWN_CORRECTION | An instance of a term on the known-corrections list | |
| **SCIENCE** (v1.3.0) | A scientific, neurobiological, physiological or psychological claim, or a cited source, that Pass 4 rated Medium or High: an absolute or overstated causal claim, a specific number or mechanism, a source that doesn't say what the sentence says, a citation that doesn't resolve, a safety-relevant claim. Severity: a contradicted or safety-relevant High is `blocking`, other High is `major`, Medium is `minor` | "Negative thoughts all start in the body" (no source; absolute) |

**Not findings:** voice, style, metaphor, sentence rhythm, and capitalized framework terms that match canonical. (SUMMARY_FORMAT is a structural length check on the Chapter Summary only, not a style judgment: the rule is one sentence per bullet, two at most, about 25 words at most, set by <AUTHOR> on 2026-11-10 with Chapter 5 as the model and applied from Chapter 6 on. Suggest the fix in one line; <AUTHOR> words it.) The shared system prompt's voice note applies. When unsure, mark `confidence: low` and `needs_author_review: true` rather than guessing.

---

## 5. Outputs and trigger

| Output | Path |
|---|---|
| Run folder (Pass 1, Pass 2, Pass 3 files; the updated ledger) | `<BOOK_ROOT>/_BookGovernance/Audit/<YYYYMMDD>_L_<ChapterName>/` → `pass1/`, `pass2/`, `pass3/`, `ledger.json` |
| Findings report | `<CH_ROOT>/Governance/<ChapterName>_LockAudit_<YYYYMMDD_HHMM>.md` + `.json` |
| **Decisions log** | `<CH_ROOT>/Manuscript/<ChapterName>_LockDecisions.md` |
| Locked snapshot (for the B0 delta check) | `<CH_ROOT>/Manuscript/_Locked/<ChapterName>_Manuscript_v<chapterVersion>.docx` + `.md` |
| Copilot research report (saved by <AUTHOR>) | `<CH_ROOT>/DeepResearch/COPILOT_RESEARCH_REPORT.md` (+ `_part2.md` …) |
| Research reconciliation (Claude) | `<CH_ROOT>/DeepResearch/RESEARCH_RECONCILIATION.md` |
| **Research gate** | `<CH_ROOT>/DeepResearch/RESEARCH_CLEAR.md`, or `RESEARCH_INCOMPLETE.md` |
| **HumanSourceCheck** (#62) | `<CH_ROOT>/DeepResearch/<ChapterName>_HumanSourceCheck.md` (signed by <AUTHOR>) |
| **Lock trigger** | `<CH_ROOT>/Manuscript/Trigger/MANUSCRIPT_LOCKED.md`, or `MANUSCRIPT_LOCK_INCOMPLETE.md` |

The run folder's `ledger.json` becomes the latest book ledger. The next chapter's lock audit, and B0, start from it.

**`RESEARCH_CLEAR.md`** is written just before the lock, after every fix is applied and DOCX = MD, so its hashes are the locked hashes. Rename any existing one to `RESEARCH_CLEAR_superseded_<YYYYMMDD_HHMM>.md` first. It is written only when:
- Pass 4 ran and (unless waived) a current Copilot report was reconciled;
- no **blocking** research finding is open (§3.2b);
- the reference list matches the approved citations (every marker resolves to one reference; `references_check.py` shows no unresolved item);
- terminology is consistent with the terminology lock (no SCIENCE fix introduced a new term);
- every accepted wording correction was applied through the decisions log (Applied column filled), none silently;
- <AUTHOR>'s decisions are recorded with initials;
- for a chapter with `humanSourceCheckRequired: yes`, the HumanSourceCheck (§3.7) is signed for these hashes, or waived (#62).

```
# RESEARCH_CLEAR — <ChapterName>
clearedAt: <ISO date-time>
docxSha256: <hash>      # equals MANUSCRIPT_LOCKED.md docxSha256
mdSha256: <hash>
passFour: <ScienceClaims file>  (High <n> · Medium <n> · sourcesChecked <n of n>)
copilotReport: <file name>   |   waived — <reason> (<initials> <date>) [backup: Claude run <file>, if one was made; recorded as a backup, never as a Copilot review]
copilotReportSha256: <one line per report: report file, its reviewedSha256 (from the handoff file it names), sections covered>
coverage: Copilot ruled <n> of <n> Stage 1 claims · Claude backup <IDs, file | none> · waived <IDs via research-ids | none>   |   n/a (research step waived in full)
reconciliation: DeepResearch/RESEARCH_RECONCILIATION.md  (rows <n> · decided <n> · blocking open 0)
changesAfterReport: none | softened-only (<n> rows, listed) | human-verified (<n> rows, from the HumanSourceCheck) | rerun sections: <list>
referenceList: matches approved citations (<n> references)
authorApproval: <initials> <date>
humanSourceCheck: DeepResearch/<ChapterName>_HumanSourceCheck.md (Signed: <initials> <date>; builtFrom equals docxSha256; Tier 1 <n> · says it <n> · fixed <n>)   |   waived — <reason> (<initials> <date>)   |   not required (`humanSourceCheckRequired: no`)
```

If the text changed after the Copilot report in a way that adds or strengthens an empirical claim, a number, a causal or absolute statement, or changes a citation, the report is stale for those sections: re-run the Copilot review on them first (§7). Softening-only fixes keep it valid, and so do the author's human-verified corrections from the HumanSourceCheck (§3.7, step 5). Only a source Copilot never reviewed needs a scoped re-run. Otherwise write `RESEARCH_INCOMPLETE.md` naming what is open.

**`MANUSCRIPT_LOCKED.md`** is written only when every item of the exit gate (§6) holds, which now includes `RESEARCH_CLEAR.md`. Before writing it, rename any existing one to `MANUSCRIPT_LOCKED_superseded_<YYYYMMDD_HHMM>.md`. It records:

```
# MANUSCRIPT_LOCKED — <ChapterName>
lockedAt: <ISO date-time>
pipelineRelease: v1.3.0      # the release of these phase files that wrote this lock
copilotRequired: yes|no     # see the rule below
freezePilot: <one line>     # #42: present on a freeze chapter's lock and carried forward; absent = the pre-#42 process
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
researchClear: DeepResearch/RESEARCH_CLEAR.md (clearedAt <date>; hashes equal this lock)  |  not applicable (`copilotRequired: no`)
humanSourceCheckRequired: yes|no   # #62: yes on a first lock written on or after 2026-11-22; re-locks carry it forward; absent = no
humanSourceCheck: DeepResearch/<ChapterName>_HumanSourceCheck.md (Signed: <initials> <date>)  |  waived — <reason> (<initials> <date>)  |  not required
decisionsLog: Manuscript/<ChapterName>_LockDecisions.md
snapshot: Manuscript/_Locked/<ChapterName>_Manuscript_v<version>.docx / .md
governanceReady: <date of the GOVERNANCE_READY.md this lock follows>
workbook:          # freeze chapters (#42): one indented line per exercise, file names only (in <CH_ROOT>/Workbook/):
  - <workbook DOCX name>: <sha256> · <workbook MD name>: <sha256>
```

Otherwise write `MANUSCRIPT_LOCK_INCOMPLETE.md` listing what is open: blank decisions, unapplied fixes, a new delta finding, an open impact item, a failed DOCX = MD check, or a HumanSourceCheck that is missing, unsigned, stale or waiting on fixes (§3.6 lists the lines).

**`copilotRequired`** decides whether the Copilot steps (research review here, the final eBook review in PHASE 4 Step 0F, the publication review in PHASE 6.5) are required for the chapter, so every gate reads this one field instead of guessing from dates:
- the **first** lock written by v1.3.0 files sets `yes`, except a protected chapter's first lock (Ch1 to Ch5), which records `no` (author decision 2026-10-31);
- a delta re-lock (§7) **carries the previous value forward**, so an ordinary revision of an older chapter does not make the steps mandatory;
- a "Copilot research retrofit" section in `MANUSCRIPT_REVISED.md` (§7) sets `yes` on the next lock;
- a lock written by earlier releases has no such field, and counts as `no`. An author may set `no` on a new chapter only by recording why in the decisions log.

**`freezePilot:`** (2026-11-16, #42) marks a freeze chapter: all checks before this lock, small edits only in PHASE 3 / 3.5, the final lock at PHASE 4 Part 0, read-only after it except errata. Every gate that treats a freeze chapter differently reads this one line. The pilot chapter's lock has it; Ch1 to Ch6 don't. A delta re-lock and an errata re-lock carry it forward. A freeze chapter's lock also records the workbook manuscript hashes (`workbook:`), because the workbook freezes with it (§9).

**When `freezePilot:` becomes the default (<AUTHOR>, 2026-11-17).** It stays opt-in until the pilot chapter has completed PHASE 4 (its Part 0 final lock and Part A). From then on, **every chapter's first lock** writes the line by default. A re-lock carries it forward only if the previous lock had it, so a re-lock of Ch1 to Ch6 never picks it up; they keep the old process unless <AUTHOR> names one.

**A stale lock is never left in place.** The lock is stale when either hash of record (section 0) no longer matches the files. Every downstream gate checks the hashes, not the file dates (#48, 2026-11-17): an identical-content restore is not a change, and a `MANUSCRIPT_REVISED.md` newer than the lock is informational on its own (a status-word tidy is not a text change). A revision that changes the text shows in the DOCX hash once the DOCX is edited (path 2); between the approval and that edit the lock still reads as current. After a freeze chapter's final lock only an approved `Errata` section still belongs in that file (§9). Before a lock exists there is no hash of record, so the PHASE 2.5 entry check (a section newer than `GOVERNANCE_READY.md`) still goes by the file's time.

---

## 6. PHASE 2.5 exit gate

**Invariant.** With `copilotRequired: yes`, `MANUSCRIPT_LOCKED.md` is not written until `RESEARCH_CLEAR.md` exists. `RESEARCH_CLEAR.md` is always written for such a chapter and records any waiver (`research: waived — …`); a waiver line alone never replaces it.

`MANUSCRIPT_LOCKED.md` is written when:
- [ ] the chapter has Pass 1 and Pass 2 files (and Pass 3, if enabled) in the run folder;
- [ ] every finding in the decisions log has a Decision, and no **blocking** finding is open;
- [ ] every `Fix`, `Fix: …`, and `Canonical: …` row is applied, DOCX first, with the Applied column filled (freeze chapters, #42: every `Apply for me` row too, and every `Edited by author` row has Applied filled after a clean §3.5 re-check; any chapter: the same for `Edited by author` rows tagged `human-verified`, #62);
- [ ] every `Canonical: …` decision is in `Audit_CanonicalTerms.json`;
- [ ] Pass 4 ran: the chapter has a `ScienceClaims` file, every cited source resolves, and every **High** science claim is softened, cited, removed, kept by <AUTHOR> with initials and a reason, or sitting with an outside reviewer (never on an AI verdict alone). A `blocking` SCIENCE finding is closed, not deferred;
- [ ] `RESEARCH_CLEAR.md` is written and its hashes equal the files being locked (v1.3.0; a chapter with `copilotRequired: no` needs it only when it opts in, §7);
- [ ] **the HumanSourceCheck is signed** (#62; chapters with `humanSourceCheckRequired: yes`, whether `copilotRequired` is yes or no): `<CH_ROOT>/DeepResearch/<ChapterName>_HumanSourceCheck.md` is signed as §3.7 step 3 defines it. Every item is marked, the `Signed:` line is valid, `builtFrom:` equals the DOCX being locked, and every item not marked *Says it* or *Source found* is closed in the decisions log. Or `<CH_ROOT>/Governance/Copilot/Copilot_Waivers.md` has a `human-source-check: waived — <reason> (<initials> <date>)` line;
- [ ] **references are finished** (every chapter): `references_check.py` on the final reference list shows no unresolved item, every marker resolves to one reference, every reference resolves and is complete in APA form, and the References section is final. After the lock, references change only through `MANUSCRIPT_REVISED.md`;
- [ ] DOCX = MD (`docx_md_sync.py`: 0 rewritten, 0 dropped);
- [ ] the delta re-check is clean and the downstream impact list is closed;
- [ ] the locked snapshot is saved, and the hashes are recorded;
- [ ] (freeze chapters, #42) every §3.1b check ran and every item is decided: nothing is left for a later phase to check.

PHASE 3 (A0 included), 3.5, 3.5A, 3.5B, 3W, and 4 do not start for the chapter without a current `MANUSCRIPT_LOCKED.md`.

---

## 7. After the lock: changing the manuscript

**Freeze chapters (#42).** This path is for the time between the lock and the final lock, and only for a change PHASE 4 Part 0 may not apply (a claim, a number, a citation) or one too big for a layout edit. <AUTHOR>'s small wording edits go into the eBook and print layouts instead, and Part 0 syncs them back. After the final lock, only an errata section is acted on (§9).

After the lock, any change to the manuscript needs `Manuscript/Trigger/MANUSCRIPT_REVISED.md` **and <AUTHOR>'s approval**:

1. <AUTHOR> edits the DOCX, then brings the MD in line with `docx_md_sync.py`, and bumps the version.
2. <AUTHOR> adds a dated section to `MANUSCRIPT_REVISED.md`: the changed sections, the reason, and an **Approved: <initials> <date>** line. A section without the approval line is not acted on.
3. PHASE 1 re-runs for the changed sections, and PHASE 2 re-validates (PHASE 1, "Revision trigger"). <AUTHOR> starts each by creating `RERUN_P1.md`, then `RERUN_P2.md`, then `RERUN_P2.5.md`; saving the REVISED file wakes nothing.
4. PHASE 2.5 runs a **delta audit** of the changed sections only (§3.1 on those sections, then §3.2–§3.6) and writes a new `MANUSCRIPT_LOCKED.md` with the new hashes. The old lock is superseded.
4a. **Research gate (v1.3.0).** The delta audit decides whether the change touches research:
   - **Re-run Pass 4 and the Copilot Researcher review on the changed sections** when the revision adds, removes or strengthens an empirical claim, a number, a causal or absolute statement, or removes a hedge; adds, replaces or renumbers a citation; or touches any sentence listed in the chapter's `ScienceClaims` file. A human-verified correction is the exception to the Copilot re-run only; Pass 4 still re-checks the changed sentences (next bullets). The old `RESEARCH_CLEAR.md` is superseded and a new one is written for the new hashes.
   - **No Copilot re-run** when the revision only softens a claim, or changes spelling, punctuation, formatting, narrative, metaphor or framework wording. Pass 4 still re-checks the changed sentences, and the new `RESEARCH_CLEAR.md` records `changesAfterReport`.
   - **No Copilot re-run for human-verified corrections** (#62, §3.7 step 5): a fix <AUTHOR> made from the HumanSourceCheck with the source open. The `MANUSCRIPT_REVISED.md` section carries a `human-verified: HumanSourceCheck items <n>` line, which marks those changes as the author's. The runner still compares the reference list with the **reviewed reference list**: the References section of the DOCX snapshot in the latest research handoff's `1_Upload_First/`. A citation renumbered, completed, or replaced with a source on that list needs no Copilot re-run. A source not on it goes to a scoped re-run. Pass 4 still re-checks the changed sentences. On a chapter with `humanSourceCheckRequired: yes`, the sheet is rebuilt for the changed sentences and signed again (§3.7 step 6).
   - PHASE 4 Part 0 never applies such wording; it goes through this path (section 0, path 2).
   - **Opting a `copilotRequired: no` chapter in:** a `MANUSCRIPT_REVISED.md` section titled "Copilot research retrofit" (approved as above) runs §3.2b for the whole chapter, applies any decided fixes, and writes `RESEARCH_CLEAR.md` with the new lock.
5. Anything already built from the old text (the eBook, the print IDMLs, the workbook) carries the change by hand, as before. PHASE 4 Part 0 stops if the revision is newer than the eBook PDF.

The one other sanctioned path is PHASE 4 Part 0: a difference between the final eBook PDF and the locked manuscript is a post-lock change too, so it is applied only with <AUTHOR>'s decision in `_Pipeline/P4_DECISIONS.md` (PHASE 4, 0.3).

---

## 8. Rules

- **The DOCX is canonical.** Fixes go into the DOCX first; the MD follows through `docx_md_sync.py`, never by hand.
- **No decision, no edit.** Nothing is applied without a written Decision in the log. The audit run and the apply run are separate. (Drafts for <AUTHOR> to accept go into a review copy, never the manuscript DOCX: the freeze process, §3.7 step 4.)
- **Flag; never rewrite.** Suggestions are one line. Voice and style are not findings.
- **One chapter at a time.** The run may read every other chapter, but it edits only this chapter's manuscript and records, plus `Audit_CanonicalTerms.json` / `Audit_Config.json` for `Canonical:` decisions and its own run folder in `_BookGovernance/Audit/`.
- **A locked chapter isn't reopened by another chapter's audit.** A conflict with an already-locked chapter is listed for <AUTHOR> as a cross-chapter follow-up; if <AUTHOR> wants that chapter changed, it goes through its own `MANUSCRIPT_REVISED.md`.
- **Science is verified, not assumed (v1.3.0).** AI output, the Deep Researcher workflow's included, is evidence and never a verdict. Every returned source is opened and existence-checked. Ollama and phi4 may retrieve or format; they never rate a claim or a source. Suggested wording for a SCIENCE finding is one line and softer, not stronger; <AUTHOR> decides the wording.
- **Copilot is a second opinion, never a source of truth (v1.3.0).** Its report is evidence. Claude verifies each source it names, and neither Claude's nor Copilot's verdict closes a High claim. Copilot never edits the manuscript, and nothing in this pipeline invokes it.
- **Protected chapters** are never processed by the automation.
- **Back up before every edit** (`Governance/_Backups/<YYYYMMDD_HHMM>_lockaudit/`); never delete.
- **Never leave a stale trigger.** Rename older READY and LOCKED files to `*_superseded_<timestamp>.md`.
- **House rules apply forward only (2026-11-16, #42).** A rule adopted on a date applies to the chapters not yet locked on that date. It is never retrofitted to a locked chapter unless <AUTHOR> names the chapter: before its final lock, through a REVISED section; after it, through the next-edition log. The dated list is in `MASTER_PIPELINE_OVERVIEW.md` section 10.
- **After the final lock, the manuscript is read-only (#42).** See §9.

---

## 9. After the final lock: read-only, the next-edition log, errata (freeze chapters, 2026-11-16, #42)

**The workbook freezes too (<AUTHOR>, 2026-11-17).** The chapter's workbook manuscript (DOCX and MD) follows the same rule: its wording checks run before this lock (§3.1b), which records its hashes; after the lock only small layout edits go into the workbook eBook and print; PHASE 3W W3 syncs them back once and writes `WORKBOOK_READY.md` with its own `finalLock: yes` line, before the chapter's Kindle build (PHASE 3W, W3); after that it is read-only except through errata. Below, "the manuscript" means both.

**Read-only.** From the final lock on (`MANUSCRIPT_SYNCED.md` with `finalLock: yes`; a re-export during PHASE 4 Step 0V, before Part A, is still part of Part 0, PHASE 4 0.8), no phase edits the manuscript DOCX or MD, proposes an edit to it, or asks <AUTHOR> to make one, except through the errata step below. This covers PHASE 4 (0R, 0G, Part A, Part B with B0), PHASE 0.9 Mode D, PHASE 5, 6, 6.5 (chapter and book mode), 6.9 and 7. Their checks compare the formats with the manuscript; when a format differs, the format is fixed.

**The next-edition log.** One file for the book, append-only: `<BOOK_ROOT>/_BookGovernance/NextEdition/NEXT_EDITION_LOG.md`. A phase that finds a content issue in a final-locked chapter adds a row and lists the row IDs in its own report. This is the one file such a phase may add to besides its own outputs; it never edits or deletes a row.

```
# NEXT_EDITION_LOG — <BOOK_TITLE>

| ID | Date | Chapter | Found by | Location (heading › paragraph) | Current text (≤ 25 words) | Issue | Suggestion | Major? | Status |
|---|---|---|---|---|---|---|---|---|---|
| NE-001 | <YYYY-MM-DD> | <ChapterName> | PHASE 6.5 (<report file>) | <heading › "first words…"> | <exact text> | <one line> | <one line> | no | open |
```

- **ID:** `NE-<nnn>`, numbered in order for the whole book.
- **Major?:** `no`, or `yes: <factual | safety | legal | claim/citation>` when the finder thinks the row meets the criteria below. A `yes` row is raised with <AUTHOR> at once (the phase's "needs you" email, or chat). <AUTHOR> confirms or changes it.
- **Status:** `open`, then `next edition` (kept for the next edition), `errata <YYYY-MM-DD>` (fixed through the errata step) or `closed — <reason> (<initials>)`.
- At the next edition, the chapter's PHASE 2.5 audit reads its `open` and `next edition` rows first.

**Major error: the only reasons to reopen a final-locked chapter.**
1. **Factual:** a statement of fact that is wrong (a date, a name, a number, a misattributed quotation).
2. **Safety:** wording that could lead a reader to harm, or a caution that is missing where one is needed.
3. **Legal:** defamation, a privacy problem, a copyright or trademark problem, a required notice missing.
4. **A broken claim or citation:** a citation that doesn't exist, doesn't resolve, or doesn't support its sentence, or a claim the research clearance would now rate unsupported or contradicted.

Not major errors: style, voice, casing, a hedge on a claim that is otherwise supported, a house rule adopted after the lock, and a cross-chapter wording difference that misleads no one. They go to the log.

**The errata step.**
1. The phase that finds it logs the row with `Major?: yes: <criterion>` and tells <AUTHOR>, with the evidence (the source opened, the fact checked).
2. **<AUTHOR> approves it:** a `MANUSCRIPT_REVISED.md` section titled `Errata — <criterion>: NE-<nnn>`, with the changed sections, the reason and `Approved: <initials> <date>`. After the final lock, add no other kind of section. Claude does not act on a section without that title or the approval line. Since #48 a newer REVISED file no longer stales the lock on its own (the gates compare hashes, §5), but such a section is still moved to the chapter's archive (`Chapters/<ChapterName>/ARCHIVE/<YYYYMMDD>/`, MASTER section 10) and its item logged for the next edition, so the file holds only approved errata.
3. <AUTHOR> edits the DOCX in Word (a review copy shows the spot; a mechanical fix can be `Apply for me`). Claude brings the MD in line with `docx_md_sync.py` and verifies it. An errata in the workbook edits the workbook DOCX the same way, and W3 then writes a new final-lock `WORKBOOK_READY.md` naming the errata ID. **A workbook-only errata** (the chapter text unchanged) needs only the PHASE 2.5 delta re-lock, the workbook layouts and W3, then the chapter's PHASE 6.5 and 7; Part 0, Part A, PHASE 5, 6 and 6.9 don't re-run, because nothing they read changed.
4. PHASE 1 for the changed sections and PHASE 2 re-validate (`RERUN_P1.md`, then `RERUN_P2.md`). Then a PHASE 2.5 delta audit of the changed sections, with the §7 step 4a research rule (`RERUN_P2.5.md`), writes a new `MANUSCRIPT_LOCKED.md`. `copilotRequired` and `freezePilot:` carry forward.
5. <AUTHOR> carries the fix into the eBook and print layouts (and the workbook, if it carries the text) and re-exports. PHASE 4 Part 0 compares the new PDF with the errata lock and expects `NO_DIFFERENCES` (the fix is already in the DOCX and MD), then writes a new final-lock `MANUSCRIPT_SYNCED.md` whose `finalLock:` line names the errata ID. Then 0P, 0V (a new `LAYOUT_VERIFIED.md`), 0C, Part A, and PHASE 5, 6 and 6.5 run again for the chapter.
6. **The audiobook:** the chapter's `AUDIOBOOK_READY.md` is now stale, because its manuscript hashes no longer match (the PHASE 7 release check compares them). Rename it `AUDIOBOOK_READY_superseded_<timestamp>.md`. PHASE 6.9 runs again; if narrated text changed, the chapter is recorded again in full (no pickups).
7. If B0 had already passed, it runs again for the changed chapter (since-lock delta).
8. The log row's status becomes `errata <YYYY-MM-DD>`, and the released chapter gets a new version through PHASE 7.

---

# How to run

**Automatic (default).** When PHASE 2 passes and writes `GOVERNANCE_READY.md`, the runner starts PHASE 2.5 for the chapter.

1. 🤖 **Audit run:** §1 gate → §3.1 read-through → §3.2 report and decisions log. 📧 Email: "PHASE 2.5: <n> findings to decide", with the decisions log path.
2. 🧑 **<AUTHOR>:** open `Manuscript/<ChapterName>_LockDecisions.md`, fill in every **Decision**, then create `_Pipeline/RERUN_P2.5.md`.
3. 🧑 **<AUTHOR>, in parallel:** run `COPILOT_HANDOFFS/COPILOT_PHASE2_5_RESEARCH_REVIEW.md` in Microsoft Copilot (Researcher) and save `DeepResearch/COPILOT_RESEARCH_REPORT.md`.
3a. 🤖 **Reconcile run:** §3.2b validates the report and writes `RESEARCH_RECONCILIATION.md`; new research rows go into the decisions log. If any are blank: 📧 "N research items to decide", a second 🧑 decision round, and `RERUN_P2.5.md` again.
3b. 🤖 **Apply run:** §3.3 read decisions → §3.4 apply (DOCX, then `docx_md_sync.py`) → §3.5 delta re-check and impact → §3.6 confirm → §5 lock. 📧 Email: "manuscript locked; PHASE 3 starts", or "needs you" with what is open.
4. ✅ `DeepResearch/RESEARCH_CLEAR.md`, then `Manuscript/Trigger/MANUSCRIPT_LOCKED.md`. PHASE 3 A0 (figure prompts and the design packet) starts from it.

If the audit finds nothing, the first run writes the decisions log with no rows, and the lock, in one go.

**By hand (Claude chat, or a protected chapter).** Paste this file with the chapter's MD, the latest `ledger.json`, `Audit_Config.json`, `Audit_CanonicalTerms.json`, and the glossary, and ask for §3.1–§3.2. Decide the rows in chat, then ask for §3.4–§5. Run `docx_md_sync.py` yourself if the assistant can't run local tools.

**Without AI.** Use §4 as a checklist and read the chapter once per category. Record each finding and your decision in the decisions log, make the fixes in the DOCX, regenerate the MD with `docx_md_sync.py`, and write `MANUSCRIPT_LOCKED.md` with the two hashes (`Get-FileHash -Algorithm SHA256` in PowerShell, `sha256sum` in bash).
