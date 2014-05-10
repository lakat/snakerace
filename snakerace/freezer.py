import subprocess
import fcntl
import pexpect


class Debugger(object):
    def __init__(self, script):
        self.script = script
        self.subproc = None
        self.poll_interval = 0.1

    def communicate(self, command):
        if self.subproc is None:
            self.subproc = pexpect.spawn(' '.join(['pdb', self.script]))
            self.read_response()

        self.subproc.sendline(command)
        return self.read_response()

    def read_response(self):
        self.subproc.expect("(Pdb)")
        return self.subproc.before

    def add_temporary_breakpoint(self, source, line):
        command = 'tbreak {source}:{line}'.format(source=source, line=line)
        self.communicate(command)

    def cont(self):
        return self.communicate('continue')

    def exit(self):
        self.subproc.sendline('exit')


def main():
    debugger = Debugger('sample.py')
    debugger.add_temporary_breakpoint('some_module.py', 3)
    debugger.cont()
    debugger.cont()
    debugger.exit()


if __name__ == "__main__":
    main()
