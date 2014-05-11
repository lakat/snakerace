import unittest
import textwrap

from snakerace import linespec

class TestParseLineSpec(unittest.TestCase):
    def test_parsing(self):
        result = linespec.parse("something/kkk.py:3")

        self.assertEquals(
            linespec.LineSpec('something/kkk.py', 3),
            result)

    def test_parsing_ignores_things_after_space(self):
        result = linespec.parse("something/kkk.py:3 Some code")

        self.assertEquals(
            linespec.LineSpec('something/kkk.py', 3),
            result)


def make_linespecs(long_string):
    return linespec.parse_lines(textwrap.dedent(long_string).strip().split())


class TestSorting(unittest.TestCase):
    def test_sorting(self):
        linespecs = make_linespecs("""
        file1.py:2
        file1.py:3
        file2.py:4
        file1.py:2
        """)

        result = linespec.group(linespecs)

        self.assertEquals(
            [
                make_linespecs("""
                file1.py:2
                file1.py:3
                """),
                make_linespecs("""
                file2.py:4
                """),
                make_linespecs("""
                file1.py:2
                """),
            ],
            result
        )

    def test_restarted_sequence(self):
        linespecs = make_linespecs("""
        file1.py:2
        file1.py:1
        """)

        result = linespec.group(linespecs)

        self.assertEquals(
            [
                make_linespecs("""
                file1.py:2
                """),
                make_linespecs("""
                file1.py:1
                """),
            ],
            result
        )
