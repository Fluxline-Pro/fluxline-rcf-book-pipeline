# PHASE 6.9: Audiobook — Narration Script, Recording, Audiobook QA (v1.0)

> **Pipeline position:** PHASE 6.9 of 7 (the audiobook, the last step before release) · **Upstream gate:** the chapter's latest PHASE 6.5 PublicationQA report certifies **Publishing Ready**, and the manuscript still matches its lock or `MANUSCRIPT_SYNCED.md` · **Downstream:** PHASE 7 Final Checklist & Sign-off
> **Canonical paths, status ladder, triggers, and deliverables:** see `MASTER_PIPELINE_OVERVIEW.md`.

**New (2026-11-16, <AUTHOR>'s decision; unreleased).** The audiobook used to be PHASE 4 Part C, recorded from the Kindle output before PHASE 5. The PHASE 6 and 6.5 work could still change the manuscript after that, so recordings needed pickups, and about 150 edits across Ch1 to Ch5 left the audio choppy and unlike <AUTHOR>'s voice in the edited places. All of Part C now runs here, once the chapter's own checks are done:
- the narration script, the XTTS draft, <AUTHOR>'s recording and the audiobook QA;
- each chapter is **recorded in full** at this phase. There are no pickup re-records after it;
- the book-level `<BOOK>_AUDIOBOOK` set (formerly PHASE 4 Part B, B4b) is assembled here in book mode, after every chapter's 6.9.

No earlier phase waits on audio any more. Congruency pass 2 (PHASE 4) no longer includes the narration script or the audio, and PHASE 6.5 no longer certifies the audiobook.

**Until the tools change (see the CHANGELOG), this phase can't run for a chapter with a lock.** Today's `congruency_check.py` pass 2 still includes the narration script and the audio, so it can't PASS before a recording exists, and PHASE 5 and 6.5 wait for that PASS. Until then such a chapter waits at PHASE 5; what to do meanwhile is <AUTHOR>'s call. (Recording it early would not help: PHASE 7 needs `AUDIOBOOK_READY.md`, which only this phase writes.) Chapters without a lock (Ch1 to Ch5) are never held by the congruency check, so they can use this phase now, with Claude in chat.

---

# RUN MODES

- **Chapter mode:** one chapter (or a narrated front matter, Part opener or back matter section) under `<CH_ROOT>` = `<BOOK_ROOT>/Chapters/<ChapterName>/Final/`.
- **Book mode:** the `<BOOK>_AUDIOBOOK` set in `<BOOK_ROOT>/_BookPublication/`. Run once every narrated section has passed chapter mode.

**Chapters without a lock (the first book's Ch1 to Ch5)** follow the same steps with Claude in chat (the runner ignores protected chapters). Their full re-recording here replaces the pickups made so far. The gate checks that need a lock (hashes, congruency) are reported for them, never held.

**Trigger.** When PHASE 6.5 certifies the chapter Publishing Ready, PHASE 6.9 starts: steps 1 and 2 build the script and tell <AUTHOR> it is ready to record. A new MP3 in `Audiobook/` starts the audiobook QA on its own (the local watcher), but it doesn't wake the runner: once the QA email arrives, <AUTHOR> creates `_Pipeline/RERUN_P6.9.md`, and the phase runs again from the entry check. Step 1 leaves the script alone on that run (see step 1), so steps 5 and 6 can pass. Until the runner has a PHASE 6.9 job (see the CHANGELOG), ask Claude to run it.

---

# INPUTS (chapter mode)

| Input | Path |
|---|---|
| Latest Publication QA report, certifying Publishing Ready | `<CH_ROOT>/Governance/<ChapterName>_PublicationQA_*.md`; for front matter, Part openers and back matter, which PHASE 6.5 checks in book mode: `<BOOK_ROOT>/_BookGovernance/<BOOK>_PublicationQA_*.md` |
| Manuscript (MD and DOCX) and its lock or sync trigger | `<CH_ROOT>/Manuscript/`, `Manuscript/Trigger/MANUSCRIPT_LOCKED.md`, `Manuscript/Trigger/MANUSCRIPT_SYNCED.md` |
| Kindle DOCX: the reading order and the text the script is built from | `<CH_ROOT>/Kindle/<ChapterName>_Kindle.docx` (PHASE 4 Part A) |
| Narration prep: pronunciation guide, segment markers, pacing notes | `<CH_ROOT>/Audiobook/<ChapterName>_NarrationScript.md` (first made in PHASE 1 Step 9) |
| Congruency report, pass 2 (PASS) | `<BOOK_ROOT>/_BookGovernance/CongruencyQA/<ChapterName>_Congruency_Pass2.md` + `.json` |

**The chapter's own checks are done here.** The script is built from the Kindle DOCX, which PHASE 4 Part A builds from the synced manuscript. If PHASE 6.5's fixes changed the manuscript (through `MANUSCRIPT_REVISED.md`, a new lock and a Part 0 re-sync), Part A rebuilt the Kindle DOCX, so it carries those fixes. A later approved revision (for example a B0 cross-chapter fix) makes `AUDIOBOOK_READY.md` stale (section 6).

---

# DELIVERABLES (chapter mode)

| Deliverable | Path |
|---|---|
| Narration script built from the Kindle output | `<CH_ROOT>/Audiobook/<ChapterName>_NarrationScript.md` (pronunciation guide and segment markers kept) |
| XTTS draft (optional pacing guide; never published) | `<CH_ROOT>/Audiobook/Drafts/<NN>_<ChapterName>_XTTS_Draft.mp3` |
| **Final narration** (<AUTHOR>, Adobe Audition, manual) | `<CH_ROOT>/Audiobook/<NN>_<ChapterName>.mp3` (NN = book running order, matching FrontMatter numbering) |
| Audiobook QA report (automatic) | the audiobook QA folder, one report per MP3 |
| Congruency report, PHASE 6.9 pass | `<BOOK_ROOT>/_BookGovernance/CongruencyQA/<ChapterName>_Congruency_Pass3.md` + `.json` |
| PHASE 6.9 checklist | `<CH_ROOT>/<ChapterName>_PHASE6_9_AudiobookChecklist.md` |
| Gate trigger | `<CH_ROOT>/Audiobook/Trigger/AUDIOBOOK_READY.md` or `<CH_ROOT>/Audiobook/Trigger/AUDIOBOOK_INCOMPLETE.md` |

---

# 0. Entry check

Stop, write `Audiobook/Trigger/AUDIOBOOK_INCOMPLETE.md` naming what failed, and set `gateStatus: FAIL` in the checklist if any of these is not true:

- The latest `Governance/<ChapterName>_PublicationQA_*.md` (front matter, Part openers and back matter: the latest book-mode report) certifies **Publishing Ready** and is newer than `MANUSCRIPT_SYNCED.md` and the Kindle DOCX, so it certifies the current text.
- The manuscript DOCX and MD hashes match `MANUSCRIPT_LOCKED.md` or the newer `MANUSCRIPT_SYNCED.md`, and no `MANUSCRIPT_REVISED.md` section is newer than the lock.
- `Kindle/<ChapterName>_Kindle.docx` exists and is newer than the manuscript.
- The congruency pass 2 report is PASS and newer than every one of its inputs (chapters with a lock).

---

# 1. Build the narration script from the Kindle output

Update `Audiobook/<ChapterName>_NarrationScript.md` from `Kindle/<ChapterName>_Kindle.docx`: same reading order, headings, and text as the Kindle build.

**Leave the script alone** when a final MP3 newer than it exists: that recording was made from it, and rewriting the script would make the recording look stale. Rebuild it only when the Kindle DOCX is newer than the script, or when <AUTHOR> asks.
- Keep the pronunciation guide and segment markers, and move any marker whose text moved.
- Narration-only adaptations are marked notes, never silent text changes: figure and table references, URLs, and visual-only callouts get a spoken alternative or a skip note.
- This clears the "narration" items in the PHASE 4 Part 0 downstream impact list.

# 2. XTTS draft (optional)

Render the script with local XTTS to `Audiobook/Drafts/<NN>_<ChapterName>_XTTS_Draft.mp3` as a timing and pacing reference. Drafts are never published and never go into the book set.

Then tell <AUTHOR> the script is ready to record.

# 3. <AUTHOR> records the chapter in full

<AUTHOR> records the **whole chapter** in Adobe Audition from the narration script and exports the chapter master to `Audiobook/<NN>_<ChapterName>.mp3`. The Audition session may live outside `<BOOK_ROOT>`, like the print InDesign book. A recording made before this phase (for example a PHASE 4 Part C recording of Ch1 to Ch5) is replaced, not patched with pickups.

# 4. Audiobook QA

The local watcher runs the audiobook QA on the new MP3 by itself and emails the summary. It transcribes the MP3 with Whisper and compares it with the script. Record the result in the checklist:

- It is <AUTHOR>'s recording (not a file from `Drafts/`) and newer than the narration script.
- **Coverage:** every narration segment is present and in order. The transcript is diffed against the script to list skipped or changed lines, retake leftovers, and framework terms heard differently. List them; never judge delivery or voice.
- **Technical spec** from the distributor. ACX, for example, asks for RMS between −23 and −18 dB, peaks no higher than −3 dB, a noise floor below −60 dB, 44.1 kHz constant-bit-rate MP3 at 192 kbps or higher, and room tone at the head and tail. Check the distributor's current requirements, and record the measured values.
- Framework terms are pronounced as the pronunciation guide says (<AUTHOR> confirms).
- `audiobookStatus: RECORDED | DRAFT_ONLY | PENDING | N/A`

A line the QA flags is fixed in the Audition session and the chapter master is exported again, or <AUTHOR> accepts it in the checklist.

# 5. Congruency check, PHASE 6.9 pass

After the QA, run the congruency check's PHASE 6.9 pass. It repeats pass 2 and adds the two checks that left pass 2:
- the manuscript against the narration script (differences with the segment id; narration-only descriptions are accepted once);
- the audiobook QA result (text match, the lines the transcript flagged, ACX failures, an MP3 older than the script).

Report: `_BookGovernance/CongruencyQA/<ChapterName>_Congruency_Pass3.md` + `.json`, with a PASS or HOLD verdict. <AUTHOR> decides a HOLD as in PHASE 4 Step 0C.

**Pending tool change:** `congruency_check.py` accepts only `--pass 1|2`, and its pass 2 still includes these two checks. Until it has the PHASE 6.9 pass, a chapter that reaches this phase (today only Ch1 to Ch5, see the note at the top) runs `congruency_check.py <ChapterName> --pass 2` here, after the recording, and reads its script and audio rows as this check.

# 6. Checklist and gate

Save `<CH_ROOT>/<ChapterName>_PHASE6_9_AudiobookChecklist.md`:
- entry check result (section 0), with the Publication QA report used;
- narration script date and the Kindle DOCX it was built from;
- XTTS draft made (yes or no);
- final recording file and date;
- audiobook QA: report, coverage result, measured technical-spec values, flagged lines and how each was closed;
- pronunciation review by <AUTHOR>;
- congruency PHASE 6.9 pass verdict;
- `audiobookStatus`;
- `gateStatus: PASS | FAIL`.

Write `Audiobook/Trigger/AUDIOBOOK_READY.md` (renaming any older one to `*_superseded_<timestamp>.md`) when `gateStatus` is PASS: `audiobookStatus: RECORDED` (or `N/A` for a section that isn't narrated), the QA has no open item, and the congruency verdict is PASS. It records the manuscript DOCX and MD hashes, the narration script and MP3 SHA-256 hashes, the QA report, and the congruency report. Otherwise write `AUDIOBOOK_INCOMPLETE.md` listing what is open.

**Stale rule (no pickups).** `AUDIOBOOK_READY.md` is stale when a hash it records no longer matches. If narrated text changes after this phase (only through an approved `MANUSCRIPT_REVISED.md` revision), the chapter goes through its usual re-run (new lock, PHASE 4 Part 0 and Part A, PHASE 5, 6, 6.5) and is then recorded again **in full** here.

Front matter, Part openers, and back matter sections that are narrated follow the same steps in their `Audiobook/` folders.

## PHASE 6.9 chapter exit gate

PHASE 7 may start for the chapter when `Audiobook/Trigger/AUDIOBOOK_READY.md` is current, the PHASE 6.9 checklist shows `gateStatus: PASS`, and the PHASE 6.5 report still certifies Publishing Ready.

---

# BOOK MODE: <BOOK>_AUDIOBOOK

Run once, when every narrated section has a current `AUDIOBOOK_READY.md` and PHASE 4 Part B's B0 has written `_BookGovernance/Audit/Trigger/AUDIT_FINAL_CLEAR.md`.

Assemble `_BookPublication/<BOOK>_AUDIOBOOK/` from the **final recordings only** (never `Drafts/`):
- the ordered MP3 set: the running order matches the book TOC and the Kindle reading order, and the files are named `<NN>_<Section>.mp3`;
- `<BOOK>_Audiobook_TrackList.md`: track number, section, file, duration.

Then check the set (this moved here from PHASE 6.5): every section has <AUTHOR>'s final recording, no XTTS file from `Audiobook/Drafts/` is in the set, the running order and naming are right, the track list is present, and each section's checklist records its coverage and technical-spec results. Record the result in `_BookPublication/<BOOK>_AUDIOBOOK/<BOOK>_Audiobook_AssemblyReport.md`.

## PHASE 6.9 book exit gate

- [ ] `<BOOK>_AUDIOBOOK` set and track list exist, built only from <AUTHOR>'s final recordings
- [ ] Every narrated section's `AUDIOBOOK_READY.md` is current
- [ ] The assembly report lists no unresolved item

---

# FINAL RULE

This phase never edits the manuscript, the layouts or the Kindle files. The narration script is the only file it writes from the text; the recording is <AUTHOR>'s. PHASE 7 starts for a chapter only from a current `AUDIOBOOK_READY.md`.
