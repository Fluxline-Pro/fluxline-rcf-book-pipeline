import contextlib
import io
import os
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import check_summary_format as c  # noqa: E402


def doc(*bullets, h="##"):
    return [f"{h} Chapter 9 Summary", "", "**Label**", ""] + [f"-   {b}" for b in bullets] + ["", f"{h} Workbook Exercise 9.1", "-   ignored; bullet; with; semicolons; here."]


def run_main(lines=None, argv_extra=()):
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "m.md")
        if lines is not None:
            with open(p, "w", encoding="utf-8") as fh:
                fh.write("\n".join(lines))
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = c.main([*argv_extra, p])
        return code, out.getvalue(), err.getvalue()


class SummaryFormat(unittest.TestCase):
    def test_short_one_sentence_passes(self):
        self.assertEqual(c.check(doc("Values show what we stand for and why.")), [])

    def test_semicolon_counts_as_a_break_but_two_sentences_pass(self):
        self.assertEqual(c.sentence_count("Values show what we stand for; virtues show how."), 2)
        self.assertEqual(c.check(doc("Values show what we stand for; virtues show how.")), [])

    def test_three_sentences_fail(self):
        self.assertEqual(len(c.check(doc("One. Two. Three."))), 1)
        self.assertEqual(len(c.check(doc("One; two; three."))), 1)

    def test_word_limit_boundary(self):
        self.assertEqual(c.check(doc(" ".join(["word"] * 25) + ".")), [])
        self.assertEqual(len(c.check(doc(" ".join(["word"] * 26) + "."))), 1)

    def test_dashes_arrows_equals_are_not_words(self):
        self.assertEqual(c.word_count("Pathos --- resonance — felt → Value = Virtue"), 5)

    def test_eg_is_not_a_sentence_break(self):
        self.assertEqual(c.sentence_count("Pair them (e.g., Value: Integrity) with a virtue."), 1)

    def test_italic_markers_are_not_words(self):
        self.assertEqual(c.word_count("*Ask* **now** please"), 3)

    def test_section_ends_at_the_next_heading_of_same_or_higher_level(self):
        self.assertEqual(len(list(c.summary_bullets(doc("Fine.")))), 1)
        h3 = ["### Chapter 9 Summary", "- one.", "### Next", "- a; b; c; d."]
        self.assertEqual([t for _, t in c.summary_bullets(h3)], ["one."])
        sub = ["## Chapter 9 Summary", "### Sub", "- inside.", "## Next", "- outside."]
        self.assertEqual([t for _, t in c.summary_bullets(sub)], ["inside."])

    def test_heading_with_extra_words_is_not_the_summary(self):
        self.assertEqual(list(c.summary_bullets(["## Chapter 6 Summary Exercises", "- x."])), [])

    def test_closing_frame_noted_from_chapter_7_not_failed(self):
        d = [x.replace("Chapter 9", "Chapter 7") for x in doc("Fine.")]
        d.insert(4, "**Closing Frame: Values**")
        self.assertEqual(list(c.closing_frames(d)), [5])
        code, out, _ = run_main(d)
        self.assertEqual(code, 0)
        self.assertIn("Closing Frame", out)
        self.assertEqual(list(c.closing_frames(doc("Fine."))), [])

    def test_closing_frame_heading_form_and_section_boundary(self):
        d = ["## Chapter 8 Summary", "### Closing Frame: X", "- ok.", "## Workbook Exercise 8.1", "**Closing Frame: Y**"]
        self.assertEqual(list(c.closing_frames(d)), [2])

    def test_closing_frame_allowed_before_chapter_7(self):
        d = [x.replace("Chapter 9", "Chapter 6") for x in doc("Fine.")]
        d.insert(4, "**Closing Frame: Values**")
        self.assertEqual(list(c.closing_frames(d)), [])

    def test_main_exit_codes(self):
        self.assertEqual(run_main(doc("Fine."))[0], 0)
        self.assertEqual(run_main(doc("One. Two. Three."))[0], 1)
        code, _, err = run_main(["# Title", "- no summary section"])
        self.assertEqual(code, 2)
        self.assertIn("no 'Chapter N Summary'", err)
        self.assertEqual(run_main(None)[0], 2)  # file missing
        self.assertEqual(run_main(doc(" ".join(["w"] * 30) + "."), ["--max-words", "40"])[0], 0)


if __name__ == "__main__":
    unittest.main()
