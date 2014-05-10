import subprocess
from coverage import coverage


def run_with_coverage(args, sources):
    proc = subprocess.Popen(
        ['coverage', 'run', '--source=' + ','.join(sources)] + args)
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
    return result.covered_lines


def main():
    run_with_coverage(['sample.py'], ['some_module.py'])
    print (
        "The following lines has been covered in some_module.py:"
        + ','.join(str(num) for num in getlines('some_module.py')))


if __name__ == "__main__":
    main()
