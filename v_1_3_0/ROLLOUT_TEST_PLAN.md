# Rollout test plan: one sacrificial chapter (v1.3.0)

**Why:** v1.3.0 is released as ALPHA/BETA. The next bugs are state-transition bugs, and they only show when the machine moves. Do not call v1.3.0 live, and do not enable batch behavior, until one chapter has gone through everything below **without anyone rescuing the architecture by hand**. That pass is what earns the `RC` tag.

**Where:** a **sandbox copy** of a book root (as in the runner's dry-run notes), never live Ch6 or a real chapter. Give it a short test chapter with a few real, checkable claims, one deliberately overstated claim, one deliberately bad citation, one figure, and a workbook exercise. Keep a copy of the runner's logs and the `_Pipeline/STATUS.md` history.

**Before you start:** the sandbox runs from the `v_1_3_0` phase files, with the runner pointed at them (back up the instructions folder first). `copilotRequired: yes` for the test chapter.

## The walk-through

Tick each line. A line is a pass only if it happened with no hand-edited trigger file or manual fix.

### A. Governance and lock (PHASE 1, 2, 2.5)

- [ ] Drop the manuscript: PHASE 1 starts by itself; its outputs land where the folder map says. Create `_Pipeline/APPROVE_EDITORIAL.md`: PHASE 2 starts.
- [ ] PHASE 2 passes and writes `GOVERNANCE_READY.md`; PHASE 2.5 starts by itself.
- [ ] **Deliberately cause a HOLD:** leave the 2.5 decisions blank and re-run (`RERUN_P2.5.md`). Expected: `MANUSCRIPT_LOCK_INCOMPLETE.md`, an email that names the open decisions, and **no retry loop**.
- [ ] **Two-stage Researcher (or Copilot Chat) handoff:** run `COPILOT_PHASE2_5_RESEARCH_REVIEW.md` in Copilot. Check: Copilot stops after Stage 1; Stage 2 files are only added after you write `STAGE 2 FILES ATTACHED`; the report carries `stage1Completed: yes`, rules on every Stage 1 claim ID (`COVERAGE: n of n`), and quotes sentences instead of line numbers. If Researcher fails, the same steps work in a regular Copilot Chat (first live run, Ch6, 2026-10-31: Stage 2 ran in a new chat without the Stage 1 list and skipped 50 of 121 claims, which is why these checks exist).
- [ ] Before the report is saved, `RERUN_P2.5.md` gives `RESEARCH_INCOMPLETE.md` ("Waiting: Copilot research report"), applies no fix, and the email says what to do.
- [ ] The report is validated (hash = `reviewedSha256`); the deliberately bad citation is caught; `RESEARCH_RECONCILIATION.md` lists the disagreements; new research rows appear in the decisions log.
- [ ] Decide everything; `RERUN_P2.5.md`; fixes applied DOCX first, MD from it; `RESEARCH_CLEAR.md` is written **before** `MANUSCRIPT_LOCKED.md`, with equal hashes. **Inspect the hashes by hand once** (`Get-FileHash`).
- [ ] Try writing the lock without `RESEARCH_CLEAR.md` (waive nothing): it must refuse.
- [ ] Waiver path: repeat the stage with a `research` waiver and a Claude backup run; `RESEARCH_CLEAR.md` records the waiver and the backup, not a Copilot review.
- [ ] **`MANUSCRIPT_REVISED` loop:** change one sentence (a claim-strengthening one) with an approval line. Expected, with each step started by its file (`RERUN_P1.md`, then `RERUN_P2.md`, then `RERUN_P2.5.md`, in that order, since saving the REVISED file wakes nothing): PHASE 1 for the changed section, PHASE 2, a delta audit, a Copilot re-run for that section (`Copilot_Research_Handoff_<n>.md`), a new lock with new hashes, the old lock renamed `_superseded_`. Then change one spelling: no Copilot re-run.
- [ ] Reference fix after the lock goes through `MANUSCRIPT_REVISED`, not InDesign.
- [ ] **The Ch1 to Ch5 path:** a second sandbox chapter marked protected; PHASE 2.5 run with Claude in chat produces a first lock with `copilotRequired: no` (audit, decisions, references finished, DOCX = MD; no `RESEARCH_CLEAR.md`); then a "Copilot research retrofit" `MANUSCRIPT_REVISED` section runs the two-stage research and writes a new lock.

### B. Figures, eBook, print (PHASE 3, 3.5, 3W)

- [ ] PHASE 3 starts only after the lock (try it before: it must be blocked).
- [ ] Figure prompts and the design packet (including training materials) are written. **One figure handoff:** generate Option 1 in Copilot Create; save `…_opt1.png`, its text file and a `revisionHistory` entry; ask for Option 2 separately; both are recorded.
- [ ] eBook pass (`RERUN_P3.5B.md`, `ebook`), your notes, one wording note through REVISED, then the print IDML (`idml`) for the chapter **and** the workbook exercise.
- [ ] You review, edit and pass off the print book in InDesign; export all PDFs.
- [ ] PHASE 3.5 and PHASE 3W QA pass; `DESIGN_READY.md`, `WORKBOOK_READY.md`.

### C. Final wording and the formats (PHASE 4)

- [ ] Upload the final eBook PDF: Step 0F pauses with `MANUSCRIPT_SYNC_INCOMPLETE.md` ("Waiting: Copilot final eBook review"). Give the PDF to Copilot for `COPILOT_PHASE4_FINAL_EBOOK_REVIEW.md`; save the report; `RERUN_P4.md`; Part 0 continues. **Deliberately** leave a wording difference in the PDF: Part 0 asks for your decision.
- [ ] Re-export the eBook PDF after a fix: Step 0F re-opens for the changed pages.
- [ ] 0P closes. Create `LAYOUT_VERIFIED.md` and `RERUN_P4.md`. Test the negative cases: an older `LAYOUT_VERIFIED.md` than the PDF is stale; a superseded `WORKBOOK_READY.md` blocks; the email names each.
- [ ] Congruency pass 1 passes; Kindle builds only after that. Optional Copilot print and Kindle reviews are run once each.
- [ ] Narration script is rebuilt from the Kindle output; congruency pass 2 passes after the recording (a stand-in recording is fine for the test). **The audiobook is the last step** before PHASE 5.

### D. Knowledge, automation, release (PHASE 5 to 7)

- [ ] PHASE 5 starts only after all the files above are finished; the RAG chunks match the final wording (no earlier version).
- [ ] PHASE 6 produces drafts only; nothing touches the manuscript or the finished files.
- [ ] PHASE 6.5: deterministic checks, Claude's QA, then the Copilot cross-format review; the Copilot `PASS` alone does not produce Publishing Ready.
- [ ] PHASE 7: the release check pre-fills; you sign; the chapter is Published.

## Record the result

For every line that did not pass, write the file, the state, what you expected, and what happened (and the runner log lines). Fix those first; re-run only the affected state. When the whole walk-through passes once:
1. update the CHANGELOG (replace "to be confirmed by the rollout test" with the result);
2. tag `v1_3_0.RC`;
3. only then deploy `v_1_3_0` to the live `instructions/` folder, with a backup and the reconciled `BOOK_VALUES.md`.

## Things to watch in every state

- Every file you must create by hand also needs a `RERUN_P<n>.md` (see "What wakes the runner" in `HOW_TO_RUN_THE_PIPELINE.md`).
- No state loops: a waiting state sends one email and stops.
- Every email names the one action you need to take.
- Hashes in `RESEARCH_CLEAR.md`, `MANUSCRIPT_LOCKED.md` and `MANUSCRIPT_SYNCED.md` agree with the files (the hash-of-record rule in PHASE 2.5 §0).
