#!/usr/bin/env python3
"""Check the bullets of a manuscript's "Chapter N Summary" against the summary rule.

Usage: python v_1_3_0/check_summary_format.py [--max-words N] <manuscript.md>

The rule (author, 2026-11-10; Chapter 5 is the model): every bullet is one sentence (two at most),
about 25 words at most, and a semicolon counts as a sentence break. Dashes, arrows and "=" are not words.
A bullet fails when it has more than two sentences or more than the word limit; a two-sentence bullet
passes but is counted, because one sentence is preferred. Exit codes: 0 pass, 1 bullets over the rule,
2 bad arguments, unreadable file, or no "Chapter N Summary" section found (a check that read nothing
must not pass). A "Closing Frame" in a Chapter 7+ summary prints a note but does not fail the check; Chapters 1-6 keep theirs
(from Chapter 7 on it is not allowed, nor are personal anecdotes, which a script cannot detect). A format check only: voice and wording stay the author's call (PHASE 2.5 SUMMARY_FORMAT).
"""
import argparse
import re
import sys

MAX_WORDS = 25
MAX_SENTENCES = 2
_HEADING = re.compile(r"^(#{1,6})\s+Chapter\s+\d+\s+Summary\b(?!\s+\w)", re.I)
_ANY_HEADING = re.compile(r"^(#{1,6})\s")
_BULLET = re.compile(r"^\s*[-*]\s+(.*\S)\s*$")


def summary_section(lines):
    """Yield (chapter_number, line_number, line) for each line inside the Chapter Summary section.

    The section ends at the next heading of the same or a higher level than its own heading."""
    level = chapter = None
    for n, line in enumerate(lines, 1):
        if level is None:
            if m := _HEADING.match(line):
                level, chapter = len(m.group(1)), int(re.search(r"\d+", line).group())
            continue
        if (m := _ANY_HEADING.match(line)) and len(m.group(1)) <= level:
            break
        yield chapter, n, line


def summary_bullets(lines):
    """Yield (line_number, text) for each bullet in the Chapter Summary section."""
    for _, n, line in summary_section(lines):
        if m := _BULLET.match(line):
            yield n, m.group(1)


_CLOSING = re.compile(r"^\s*(#{1,6}\s+|\*\*)\s*Closing Frame(?![A-Za-z])", re.I)
CLOSING_FRAME_FROM_CHAPTER = 7


def closing_frames(lines):
    """Yield line numbers of a "Closing Frame" label or heading in a Chapter 7+ summary (Chapters 1-6 keep theirs)."""
    for chapter, n, line in summary_section(lines):
        if chapter >= CLOSING_FRAME_FROM_CHAPTER and _CLOSING.match(line):
            yield n


def word_count(text):
    """Words, not counting emphasis markers, dashes, arrows or "=" (tokens with no letter or digit)."""
    return len([w for w in re.sub(r"\*+", "", text).split() if re.search(r"\w", w)])


def sentence_count(text):
    """Sentences, counting each semicolon as a break; an abbreviation like "e.g." is not a break."""
    text = re.sub(r"\b(e\.g|i\.e|vs|etc)\.", r"\1", text, flags=re.I)
    ends = re.findall(r"[.!?](?=[\"”)*]*\s+[A-Z“\"*(])", text)
    return 1 + len(ends) + text.count(";")


def check(lines, max_words=MAX_WORDS):
    """Return [(line, reason, text)] for each bullet over the rule."""
    problems = []
    for n, text in summary_bullets(lines):
        words, sents = word_count(text), sentence_count(text)
        why = []
        if sents > MAX_SENTENCES:
            why.append(f"{sents} sentences (max {MAX_SENTENCES}; a semicolon counts as a break)")
        if words > max_words:
            why.append(f"{words} words (max {max_words})")
        if why:
            problems.append((n, "; ".join(why), text))
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check a manuscript's Chapter Summary bullets.")
    ap.add_argument("manuscript")
    ap.add_argument("--max-words", type=int, default=MAX_WORDS)
    args = ap.parse_args(argv)
    try:
        with open(args.manuscript, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except OSError as e:
        print(f"cannot read {args.manuscript}: {e}", file=sys.stderr)
        return 2
    bullets = list(summary_bullets(lines))
    if not bullets:
        print("no 'Chapter N Summary' section with bullets found", file=sys.stderr)
        return 2
    problems = check(lines, args.max_words)
    for n, why, text in problems:
        print(f"line {n}: {why}\n    {text[:140]}")
    for n in closing_frames(lines):
        print(f"note line {n}: Closing Frame in the summary (not allowed from Chapter 7 on)")
    two = sum(1 for _, t in bullets if sentence_count(t) == 2)
    print(f"{len(bullets)} bullets checked, {len(problems)} over the rule, {two} with two sentences (one is preferred)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
