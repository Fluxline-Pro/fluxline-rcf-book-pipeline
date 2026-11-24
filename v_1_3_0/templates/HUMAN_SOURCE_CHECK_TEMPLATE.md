# Ch<N> "<Chapter title>": human source check

<!-- Template: v_1_3_0/templates/HUMAN_SOURCE_CHECK_TEMPLATE.md (PHASE 2.5 §3.7, #62). Claude fills it in confirm mode,
     after every decision is applied and DOCX = MD. Save as <CH_ROOT>/DeepResearch/<ChapterName>_HumanSourceCheck.md.
     Rules for Claude:
     - Quote each sentence exactly as it reads now, with its ^n^ markers.
     - Copy DOIs and URLs from the reference list, never from memory.
     - Label every AI ruling a hint.
     - Write a fact as verified only if you read the source on the page in this run, and say where (site, page).
       Mark anything recalled "usually summarised as".
     - Invent no page, DOI or quotation. Never pad: list only what a human has to check.
     - Leave Opened:, Notes:, AI notes: and Initials/date: blank. Only the author fills them. -->

builtFrom: docxSha256 <hash> · mdSha256 <hash>
Prepared by Claude, <YYYY-MM-DD>, for author verification (PHASE 2.5 §3.7). Checked by: <AUTHOR> (<initials>).
<!-- builtFrom is rewritten on every rebuild; a rebuilt item's boxes, Opened and Initials/date are cleared (its Notes and AI notes stay), unchanged items keep their marks. -->

**What this is.** The AI checks are done: Pass 4, the Copilot research review, and your decisions. This sheet is the part only you can do: **open each source and confirm it says what the sentence says.** Copilot's and Claude's rulings are hints only. Treat them as leads, not verdicts.

**How to mark each item.**
- `[x] Says it` means the source states it (or clearly supports it at this strength).
- `[x] Says less` means the source supports a weaker or narrower version. Note what it actually says.
- `[x] Doesn't say it` means you couldn't find support. Note where you looked.
- `[x] Source too weak` means it's true, but the source isn't good enough for this book.

On each item's **Opened:** line, name what you read yourself: the source and page (or section), for example `Opened: van der Kolk 2014, ch. 6` or `Opened: DOI page, abstract only`. If you used an AI tool (Perplexity, Copilot, ChatGPT) to research an item, paste what it said under **AI notes:**, not Notes, so the sheet shows what you checked and what the AI told you. Only your Notes become fixes; AI notes are a record. If there was nothing to open (you reworded an uncited number, dropped a source, or searched and found nothing), write `Opened: none — <why>`, for example `Opened: none — dropped, refs 4 and 5 cover it`. Add a page number or quote in **Notes** when you can. Put your initials and the date (`<initials> <YYYY-MM-DD>`) on each item's `Initials/date:` line when you finish it. Write any fix you want in Notes: the next `RERUN_P2.5.md` turns your notes into tracked changes for you to accept in Word. A correction you make with the source open needs no new Copilot review. Only a newly added source does.

**<Pick one>**
- **Before the lock:** your signature below is the author verification for the lock, and the last step before PHASE 3.
- **After the lock** (chapters locked before #62): a finding is a revision through PHASE 2.5 §7 (`MANUSCRIPT_REVISED.md` with an `Approved:` line and a `human-verified:` line). After a freeze chapter's final lock, it is errata (§9) only if it's a major error; otherwise a next-edition log row. *(For a chapter already exported: a fix also means a re-export.)*

**Time.** Tier 1 is <n> items, probably <estimate>. Tier 2 is a skim of about <n> minutes. Tier 3 needs nothing.

**Access.** Journal articles: the DOI links (note which are open access); your university library covers the rest. Books: your copy, a library, or a Google Books preview (<list the books>).

---

## Tier 1: open the source

### A. Quotes and named works

**1. Epigraph.** "<quotation>" — <attribution>
- **Check:** the exact wording in the named work (page). Is it the author's own line, or are they quoting someone? Is the epigraph's book in the References? By house rule it is reference 1, with no marker on the attribution line.
- **Hint:** <Copilot / Pass 4 ruling, short>
- [ ] Says it  [ ] Says less  [ ] Doesn't say it  [ ] Source too weak
- Opened:
- Notes:
- AI notes:
- Initials/date:

### B. Numbers

**<n>. <short label> (ref <n>).** "<sentence, exactly, with ^n^>"
- **Check:** <the figure, its unit, its scope (who, when), and whether the source states it or it was derived>.
- **Link:** <DOI or URL from the reference list>
- **Hint:** <ruling>
- [ ] Says it  [ ] Says less  [ ] Doesn't say it  [ ] Source too weak
- Opened:
- Notes:
- AI notes:
- Initials/date:

*(An uncited number:)* `- [ ] Source found  [ ] Reword  [ ] Label as illustration`

### C. Named research (what X found)

**<n>. <Author year> (ref <n>).** "<sentence>"
- **Check:** <is it a study (data) or a review/theory paper; what the paper actually reports; sample and design limits; whether the sentence is stronger than the paper>.
- The same lines as above: **Link**, **Hint**, the boxes, **Opened**, **Notes**, **AI notes**, **Initials/date**.

### D. Mechanisms (brain, body), cited or not

**<n>. <label>.** "<sentence>"
- **Check:** <whether the cited source covers the mechanism; the textbook wording; any simplification that crosses into being wrong>.
- The same lines as above: **Link**, **Hint**, the boxes, **Opened**, **Notes**, **AI notes**, **Initials/date**.

### E. Source quality (box set: Keep / Replace with a stronger source / Drop)

**<n>. Refs <n>.** <why the source may be weak or off-topic for its claim>
- [ ] Keep  [ ] Replace with a stronger source  [ ] Drop (other refs cover it)
- Opened:
- Notes:
- AI notes:
- Initials/date:

---

## Tier 2: skim (consensus statements; spot-check)

- [ ] <statement> (<why it's Tier 2>)
- [ ] **Safety lines are present:** <list them>

## Tier 3: no check needed

<Stories, RCF framework constructs, exercises, encouragement: a one-line list.>

---

## When you're done

Sign the last line, then tell Claude or create `_Pipeline/RERUN_P2.5.md`. Claude turns your Notes (not the AI notes) into tracked changes in your voice, in a review copy, for you to accept in Word. Accepting one records your decision (`Edited by author`); if the source supports a claim after all, write `Keep — <reason>` instead. After they're accepted and synced, the sheet is rebuilt for the changed items only: re-mark those (and fill `Opened:` on any item that lacks it), sign again, and create `RERUN_P2.5.md` once more. Then the lock can be written.

<!-- Sign once every Tier 1 item is marked: "Signed: <initials> <YYYY-MM-DD>" (e.g. Signed: TW 2026-11-22). A rebuild clears this line. -->
Signed:
