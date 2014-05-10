import unittest

from snakerace import scripts


class TestParseGetLinesArgs(unittest.TestCase):
    def test_empty_call_results_system_exit(self):
        with self.assertRaises(SystemExit) as ctx:
            scripts.parse_getlines_params([])

    def test_source_alone_raises_system_exit(self):
        with self.assertRaises(SystemExit) as ctx:
            scripts.parse_getlines_params(['--sources', 'sourcefile.py'])

    def test_source_parsed(self):
        result = scripts.parse_getlines_params(
            ['--sources', 'sourcefile.py', '--args', 'prog'])

        self.assertEquals(['sourcefile.py'], result.sources)

    def test_cmdline_parsed(self):
        result = scripts.parse_getlines_params(
            ['--sources', 'sourcefile.py', '--args', 'prog', 'a', 'b'])

        self.assertEquals(
            ['prog', 'a', 'b'], result.args)
