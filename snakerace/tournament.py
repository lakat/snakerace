import textwrap
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


def run_tournament(linespecs, tournament):
    race_conditions = []

    debug_cmd, subproc_args = tournament.setup()
    subproc_cmd = ' '.join(subproc_args)

    controlled_racer = freezer.Debugger(debug_cmd)

    for source, line in linespecs:
        tournament.cleanup()
        controlled_racer.add_temporary_breakpoint(source, line)
        controlled_racer.cont()
        subprocess.call(subproc_args)
        result = controlled_racer.cont()
        if failed(result):
            error_prolog = textwrap.dedent("""
            {debug_cmd} runs until {source} line {line}
            {subproc_cmd} executed completely
            {debug_cmd} continues, and raises:

            """).format(
                debug_cmd=debug_cmd,
                subproc_cmd=subproc_cmd,
                source=source,
                line=line)
            race_conditions.append(error_prolog + extract_trace(result))
            # restart the program
            controlled_racer.cont()

    tournament.teardown()
    return race_conditions
