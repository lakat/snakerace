import termcolor


class Progress(object):
    def __init__(self, stream):
        self.stream = stream

    def _write(self, msg, color):
        self.stream.write(termcolor.colored(msg, color))
        self.stream.write(termcolor.colored('\n', 'white'))

    def good(self, msg):
        self._write(msg, 'green')

    def bad(self, msg):
        self._write(msg, 'red')
