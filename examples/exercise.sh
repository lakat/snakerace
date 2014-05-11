set -eux

tmpdir=$(mktemp -d)

sr-getlines --sources racey_module.py --args racer.py $tmpdir |
    PYTHONPATH=./ sr-break-run-continue example_race:SampleTournament

