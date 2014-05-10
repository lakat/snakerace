import textwrap
import tempfile
import shutil
import os
import subprocess
import sys

import getlines
import freezer


def failed(result):
    return 'Traceback' in result


def extract_trace(result):
    start = result.find('Traceback')
    end = result.find('Uncaught exception. Entering post mortem debugging')
    assert start > 0
    assert end > 0
    return result[start:end]


def main():
    temp_dir = tempfile.mkdtemp()
    lockdir = os.path.join(temp_dir, 'lockdir')

    program_a = 'racer.py {lockdir}'.format(
        lockdir=lockdir)

    program_b = 'python ' + program_a
    module = 'racey_module.py'

    getlines.run_with_coverage(program_a.split(), [module])
    lines = getlines.getlines(module)

    dbg = freezer.Debugger(program_a)
    dbg.cont()

    race_conditions = []

    for line in lines:
        dbg.add_temporary_breakpoint(module, line)
        dbg.cont()
        subprocess.call(program_b.split())
        result = dbg.cont()
        if failed(result):
            error_prolog = textwrap.dedent("""
            {program_a} runs until {module} line {line}
            {program_b} executed completely
            {program_a} continues, and raises:

            """).format(
                program_a=program_a,
                program_b=program_b,
                module=module,
                line=line)
            race_conditions.append(error_prolog + extract_trace(result))
            # restart the program
            dbg.cont()

    shutil.rmtree(temp_dir)

    if race_conditions:
        for race_condition in race_conditions:
            sys.stderr.write(race_condition)
            sys.stderr.write('\n')

        sys.stderr.write("\nFAILED: %s race conditions\n\n" % len(
            race_conditions))
        sys.exit(1)
    else:
        sys.stdout.write('no race conditions found\n')


if __name__ == "__main__":
    main()
