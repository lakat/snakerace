import unittest

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


