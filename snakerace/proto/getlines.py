import subprocess
from coverage import coverage

from snakerace import linespec


def run_with_coverage(args, sources):
    proc = subprocess.Popen(
        ['coverage', 'run', '--source=' + ','.join(sources)] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    proc.communicate()


class CoverageResult(object):
    def __init__(self, raw_result):
        (
            self.filename,
            self.executable_lines,
            self.excluded_lines,
            self.missing_lines,
            _ignored
        ) = raw_result

    @property
    def covered_lines(self):
        return sorted(
            list(set(self.executable_lines) - set(self.missing_lines)))


def getlines(source):
    cov = coverage()
    cov.load()
    result = CoverageResult(cov.analysis2(source))
    return [linespec.LineSpec(source, line) for line in result.covered_lines]
