# PHASE 6.9: Audiobook — Narration Script, Recording, Audiobook QA (v1.0)

> **Pipeline position:** PHASE 6.9 of 7 (the audiobook, the last step before release) · **Upstream gate:** the chapter's latest PHASE 6.5 PublicationQA report certifies **Publishing Ready**, congruency pass 2 is PASS, and the manuscript still matches its lock or `MANUSCRIPT_SYNCED.md` · **Downstream:** PHASE 7 Final Checklist & Sign-off
> **Canonical paths, status ladder, triggers, and deliverables:** see `MASTER_PIPELINE_OVERVIEW.md`.

**New (2026-11-16, <AUTHOR>'s decision; unreleased).** The audiobook used to be PHASE 4 Part C, recorded from the Kindle output before PHASE 5. The PHASE 6 and 6.5 work could still change the manuscript after that, so recordings needed pickups, and about 150 edits across Ch1 to Ch5 left the audio choppy and unlike <AUTHOR>'s voice in the edited places. All of Part C now runs here, once the chapter's own checks are done:
- the narration script, the XTTS draft, <AUTHOR>'s recording and the audiobook QA;
- each chapter is **recorded in full** at this phase. There are no pickup re-records after it;
- the book-level `<BOOK>_AUDIOBOOK` set (formerly PHASE 4 Part B, B4b) is assembled here in book mode, after every chapter's 6.9.

No earlier phase waits on audio any more. Congruency pass 2 (PHASE 4) no longer includes the narration script or the audio, and PHASE 6.5 no longer certifies the audiobook.

**It runs per chapter (<AUTHOR>'s decision, 2026-11-16, #43).** A chapter's 6.9 starts once its own checks pass: its PHASE 6.5 report says Publishing Ready, `MANUSCRIPT_SYNCED.md` exists, and congruency pass 2 is PASS. It does not wait for other chapters or for the book-wide final audit (B0). If a later approved revision, for example a B0 cross-chapter fix, changes a recorded chapter, its `AUDIOBOOK_READY.md` goes stale (the PHASE 7 release check compares the recorded hashes), and the chapter is recorded again in full.

**Recording in batches (<AUTHOR>, 2026-11-16).** The pipeline still readies each chapter on its own, but <AUTHOR> records in batches of about seven chapters (roughly 1.5 hours of narration per chapter), once a batch's chapters are all ready. Waiting for a batch lowers the chance that a later cross-chapter fix forces a re-record. A chapter whose script is ready simply waits (`AUDIOBOOK_INCOMPLETE.md`, "Waiting: recording") until its batch is recorded.

---

# RUN MODES

- **Chapter mode:** one chapter (or a narrated front matter, Part opener or back matter section) under `<CH_ROOT>` = `<BOOK_ROOT>/Chapters/<ChapterName>/Final/`.
- **Book mode:** the `<BOOK>_AUDIOBOOK` set in `<BOOK_ROOT>/_BookPublication/`. Run once every narrated section has passed chapter mode.

**Protected chapters (Ch1 to Ch5)** follow the same steps with Claude in chat, because the runner never processes them. They are locked like every other chapter, so every gate check applies to them. Their full re-recording here replaces the pickups made so far.

**Trigger.** When PHASE 6.5 certifies the chapter Publishing Ready, PHASE 6.9 is queued. Once congruency pass 2 is PASS, steps 1 and 2 build the script and tell <AUTHOR> it is ready to record. A new MP3 in `Audiobook/` starts the audiobook QA on its own (the local watcher), but it doesn't wake the runner: once the QA email arrives, <AUTHOR> creates `_Pipeline/RERUN_P6.9.md`, and the phase runs again from the entry check. Step 1 leaves the script alone on that run (see step 1), so steps 5 and 6 can pass.

---

# INPUTS (chapter mode)

| Input | Path |
|---|---|
| Latest Publication QA report, certifying Publishing Ready | `<CH_ROOT>/Governance/<ChapterName>_PublicationQA_*.md`; for front matter, Part openers and back matter, which PHASE 6.5 checks in book mode: `<BOOK_ROOT>/_BookGovernance/<BOOK>_PublicationQA_*.md` |
| Manuscript (MD and DOCX) and its lock or sync trigger | `<CH_ROOT>/Manuscript/`, `Manuscript/Trigger/MANUSCRIPT_LOCKED.md`, `Manuscript/Trigger/MANUSCRIPT_SYNCED.md` |
| Kindle DOCX: the reading order and the text the script is built from | `<CH_ROOT>/Kindle/<ChapterName>_Kindle.docx` (PHASE 4 Part A) |
| Narration prep: pronunciation guide, segment markers, pacing notes | `<CH_ROOT>/Audiobook/<ChapterName>_NarrationScript.md` (first made in PHASE 1 Step 9) |
| Congruency report, pass 2 (PASS) | `<BOOK_ROOT>/_BookGovernance/CongruencyQA/<ChapterName>_Congruency_Pass2.md` + `.json` |

**The chapter's own checks are done here.** The script is built from the Kindle DOCX, which PHASE 4 Part A builds from the synced manuscript. If PHASE 6.5's fixes changed the manuscript (through `MANUSCRIPT_REVISED.md`, a new lock and a Part 0 re-sync), Part A rebuilt the Kindle DOCX, so it carries those fixes. A later approved revision makes `AUDIOBOOK_READY.md` stale (section 6).

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
- This chapter's `MANUSCRIPT_SYNCED.md` exists. (The book-wide final audit is not part of this check, #43.)
- The congruency pass 2 report is PASS and newer than every one of its inputs.

---

# 1. Build the narration script from the Kindle output

Update `Audiobook/<ChapterName>_NarrationScript.md` from `Kindle/<ChapterName>_Kindle.docx`: same reading order, headings, and text as the Kindle build.

**The 6.9 script.** A script built here carries the line `<!-- phase69Build: <YYYY-MM-DD HH:MM> · kindleDocxSha256: <hash> -->` (local time; an HTML comment, so it is never read as narration). The build time is the moment its narrated text was last set.
- **No such line** (the script predates 6.9, for example from PHASE 4 Part C): rebuild it and always write the line with the current time, even if the text comes out the same.
- **The line is there**, and the Kindle DOCX hash differs from the one it records (or <AUTHOR> asks): rebuild. If the narrated text changed, write the current time; if it didn't, keep the old build time and only update the hash.
- Edits that leave the narration alone (the pronunciation guide, pacing notes, segment markers) never change the build time.
- A recording counts in this phase only if it was written after the build time. An older recording does not count, even one newer than an older script.
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

- It is <AUTHOR>'s recording (not a file from `Drafts/`), and every final MP3 was written after the 6.9 script's build time (step 1).
- **Coverage:** every narration segment is present and in order. The transcript is diffed against the script to list skipped or changed lines, retake leftovers, and framework terms heard differently. List them; never judge delivery or voice.
- **Technical spec** from the distributor. ACX, for example, asks for RMS between −23 and −18 dB, peaks no higher than −3 dB, a noise floor below −60 dB, 44.1 kHz constant-bit-rate MP3 at 192 kbps or higher, and room tone at the head and tail. Check the distributor's current requirements, and record the measured values.
- Framework terms are pronounced as the pronunciation guide says (<AUTHOR> confirms).
- `audiobookStatus: RECORDED | DRAFT_ONLY | PENDING | N/A`

A line the QA flags is fixed in the Audition session and the chapter master is exported again, or <AUTHOR> accepts it in the checklist.

# 5. Congruency check, PHASE 6.9 pass

After the QA, run the congruency check's PHASE 6.9 pass: `congruency_check.py <ChapterName> --pass 3`. The local watcher also runs it by itself once every MP3 was written after the 6.9 build time and has a newer audiobook QA report. It repeats pass 2 and adds the two checks that left pass 2:
- the manuscript against the narration script (differences with the segment id; narration-only descriptions are accepted once);
- the audiobook QA result (text match, the lines the transcript flagged, ACX failures, an MP3 recorded before the 6.9 build time, the phase69Build line).

Report: `_BookGovernance/CongruencyQA/<ChapterName>_Congruency_Pass3.md` + `.json`, with a PASS or HOLD verdict. <AUTHOR> decides a HOLD as in PHASE 4 Step 0C.

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

Write `Audiobook/Trigger/AUDIOBOOK_READY.md` (renaming any older one, and any `AUDIOBOOK_INCOMPLETE.md`, to `*_superseded_<timestamp>.md`) when `gateStatus` is PASS: `audiobookStatus: RECORDED` (or `N/A` for a section that isn't narrated), the QA has no open item, and the congruency verdict is PASS. Otherwise write `AUDIOBOOK_INCOMPLETE.md` listing what is open. The format (the PHASE 7 release check reads the hash lines):

```
# AUDIOBOOK_READY — <ChapterName>
writtenOn: <date>
manuscriptDocxSha256: <hash>
manuscriptMdSha256: <hash>
narrationScriptSha256: <hash>
mp3: Audiobook/<NN>_<ChapterName>.mp3 | sha256: <hash>
audiobookQA: <report file>
congruencyPass3: _BookGovernance/CongruencyQA/<ChapterName>_Congruency_Pass3.md
```

Write one `mp3:` line per final MP3, with nothing else on the hash lines.

**Stale rule (no pickups).** `AUDIOBOOK_READY.md` is stale when a hash it records no longer matches. Re-run this phase (`_Pipeline/RERUN_P6.9.md`): if the narrated text is unchanged, the script stays as it is (step 1), the recording still counts, and a new `AUDIOBOOK_READY.md` is written. If narrated text changed (only through an approved `MANUSCRIPT_REVISED.md` revision), the chapter goes through its usual re-run (new lock, PHASE 4 Part 0 and Part A, PHASE 5, 6, 6.5) and is then recorded again **in full** here. Fixes made inside this phase, before `AUDIOBOOK_READY.md` is written, are fine.

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
