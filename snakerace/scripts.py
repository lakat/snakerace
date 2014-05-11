import sys
import argparse
import importlib
import subprocess

from snakerace.proto import getlines
from snakerace.proto import tournament
from snakerace import linespec


def parse_getlines_params(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--sources', help='filename to be watched for executed lines',
        required=True, nargs='+')

    parser.add_argument(
        '--args', help='program to be executed', nargs='+', required=True)

    return parser.parse_args(args)


def parse_tournament_params(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'race', help='race callable')
    parser.add_argument(
        '--linespec-file', help='File containing line specifications',
        default='-')

    return parser.parse_args(args)


def parse_cat_params(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', nargs='*', help='Filenames to cat', default=['-'])

    return parser.parse_args(args)


def open_file_or_stdin(fname):
    if fname == '-':
        return sys.stdin
    else:
        return open(fname, 'rb')


def break_run_continue():
    params = parse_tournament_params(sys.argv[1:])
    race_class = get_race(params.race)

    linespec_source = open_file_or_stdin(params.linespec_file)

    linespecs = linespec.parse_lines(
        linespec_source.readlines()
    )

    result = tournament.run_tournament(
        linespecs, race_class(), sys.stdout)

    race_conditions = result.race_conditions

    if race_conditions:
        for race_condition in race_conditions:
            sys.stderr.write(race_condition)
            sys.stderr.write('\n')

        sys.stderr.write(
            "\nFAILED: {failues} out of {race_count} runs\n\n".format(
                failues=len(race_conditions), race_count=result.race_counter))
        sys.exit(1)
    else:
        sys.stdout.write('no race conditions found\n')


def run_getlines():
    params = parse_getlines_params(sys.argv[1:])
    getlines.run_with_coverage(params.args, params.sources)
    for source in params.sources:
        for linespec_ in getlines.getlines(source):
            sys.stdout.write(linespec_.as_line())


def get_race(path_to_callable):
    module_name, function_name = path_to_callable.split(':')
    module = importlib.import_module(module_name)
    return getattr(module, function_name)


def cat_main():
    import termcolor
    params = parse_cat_params(sys.argv[1:])

    linespecs = []
    for fname in params.filenames:
        fhandle = open_file_or_stdin(fname)
        linespecs = linespec.parse_lines(fhandle.readlines())
        fhandle.close()

    for linespecs_for_file in linespec.group(linespecs):
        highlighted_lines = [ls.lineno for ls in linespecs_for_file]
        fname = linespecs_for_file[0].fname

        with open(fname, 'rb') as fhandle:
            lines = fhandle.read().split('\n')

        for idx, line in enumerate(lines):
            formatted_line = termcolor.colored(
                line,
                'yellow' if idx + 1 in highlighted_lines else 'white'
                ) + termcolor.colored('\n', 'white')

            sys.stdout.write(formatted_line)

