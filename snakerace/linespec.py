import collections


LineSpecDataObject = collections.namedtuple('LineSpec', ['fname', 'lineno'])


class LineSpec(LineSpecDataObject):
    def as_line(self):
        return "{fname}:{lineno}\n".format(
            fname=self.fname, lineno=self.lineno)


def parse(line):
    linespec = line.split(' ')[0]
    fname, lineno_string = linespec.split(':')
    return LineSpec(fname, int(lineno_string))
