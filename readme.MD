## EV Stations Test Automation


### Technical stack:
- Python 3.11 based project
- Pytest as Test Runner
- Pytest-BDD as a helper for having a clean BDD suite
- Poetry as a dependency / configuration manager


### How to run the project:
- Make sure you have Python 3.11^ installed
- Make sure you have Poetry installed
```shell
python -m pip install poetry
python -m poetry shell
python -m poetry install
```


### Running the tests:
After Poetry takes care of all dependencies, tests should be easy to execute, as follows:

#### To execute the entire suite:
```shell
poetry run pytest -s
```

#### To execute by tag:
```shell
poetry run pytest -k <tag_name> -s
```
For example, you could have:
```shell
poetry run pytest -k all-commands -s
```

#### For parallel execution:
````shell
python -m poetry run pytest -n $number_of_threads
````