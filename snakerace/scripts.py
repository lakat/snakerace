import sys
import argparse

from snakerace import getlines


def parse_getlines_params(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--sources', help='filename to be watched for executed lines',
        required=True, nargs='+')

    parser.add_argument(
        '--args', help='program to be executed', nargs='+', required=True)

    return parser.parse_args(args)


def run_tournament():
    pass


def run_getlines():
    params = parse_getlines_params(sys.argv[1:])
    getlines.run_with_coverage(params.args, params.sources)
    for source in params.sources:
        print source
        print getlines.getlines(source)
