# Get the covered lines of examples/some_module.py
sr-getlines --sources examples/some_module.py --args examples/sample.py

cd examples
echo "racey_module:8" | sr-tournament snakerace.tests.example_race:SampleTournament

