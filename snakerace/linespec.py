import collections
import itertools


LineSpecDataObject = collections.namedtuple('LineSpec', ['fname', 'lineno'])


class LineSpec(LineSpecDataObject):
    def as_line(self):
        return "{fname}:{lineno}\n".format(
            fname=self.fname, lineno=self.lineno)


def parse(line):
    fname, lineno_string = line.split(':')
    if ' ' in lineno_string:
        lineno_string = lineno_string.split(' ')[0]

    return LineSpec(fname, int(lineno_string))


def parse_lines(lines):
    return [parse(line) for line in lines]


def group(linespecs):
    groups = []
    for _key, group in itertools.groupby(linespecs, key=lambda x: x.fname):
        last_number = 0
        actual_group = []
        for linespec in group:
            if linespec.lineno > last_number:
                last_number = linespec.lineno
                actual_group.append(linespec)
            else:
                groups.append(actual_group)
                actual_group = [linespec]

        if actual_group:
            groups.append(actual_group)

    return groups
