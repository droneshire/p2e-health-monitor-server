PYTHON ?= python
DIR := ${CURDIR}
PY_PATH=$(DIR)
export PYTHONPATH=$(PY_PATH)
RUN_PY = $(PYTHON) -m
BLACK_CMD = $(RUN_PY) black --line-length 100 .
# NOTE: exclude any virtual environment subdirectories here
PY_FIND_COMMAND = find -name '*.py' ! -path './venv/*'
MYPY_CONFIG=$(PY_PATH)/mypy_config.ini

install:
	pip3 install -r requirements.txt

run_isort:
	isort $(shell $(PY_FIND_COMMAND))

run_black:
	$(BLACK_CMD)

format: run_isort run_black
	echo "Formatting..."

check_format:
	$(BLACK_CMD) --check --diff

run_mypy:
	$(RUN_PY) mypy $(shell $(PY_FIND_COMMAND)) --config-file $(MYPY_CONFIG) --no-namespace-packages

run_pylint:
	$(RUN_PY) pylint $(shell $(PY_FIND_COMMAND))

autopep8:
	autopep8 --in-place --aggressive --aggressive $(shell $(PY_FIND_COMMAND))

lint: check_format run_mypy run_pylint
	echo "Linting..."

test:
	$(RUN_PY) unittest discover -s test/ -p *_test.py -v

server:
	$(RUN_PY) app --port 8080 --host localhost --webhook TEST

.PHONY: install run_black run_isort format check_format run_mypy run_pylint lint test server
