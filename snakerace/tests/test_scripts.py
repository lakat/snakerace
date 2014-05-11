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


class TestTournamentGetLinesArgs(unittest.TestCase):
    def test_empty_call_results_system_exit(self):
        with self.assertRaises(SystemExit) as ctx:
            scripts.parse_tournament_params([])

    def generate_params(self, race='race:main', fname=None):
        if fname is None:
            return [race]
        return [race, '--linespec-file={fname}'.format(fname=fname)]

    def test_pbd_args_parsed(self):
        result = scripts.parse_tournament_params(
            self.generate_params(race='therace:somethin'))

        self.assertEquals('therace:somethin', result.race)

    def test_filename_default(self):
        result = scripts.parse_tournament_params(
            self.generate_params())

        self.assertEquals('-', result.linespec_file)

    def test_filename_specified(self):
        result = scripts.parse_tournament_params(
            self.generate_params(fname='aaa'))

        self.assertEquals('aaa', result.linespec_file)


def example_fun():
    pass


class TestImport(unittest.TestCase):
    def test_importing(self):
        fun_name = __name__ + ":example_fun"

        result = scripts.get_race(fun_name)

        self.assertEquals(example_fun, result)
