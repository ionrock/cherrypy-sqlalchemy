.PHONY: clean-pyc clean-build docs clean
VENV=venv
CHEESE=https://pypi.python.org/pypi
BUMPTYPE=patch

help:
	@echo "bootstrap - create a virtualenv and install the necessary packages for development."
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release."
	@echo '          use `-e CHEESE=http://localpypi` to release somewhere else.'
	@echo "dist - package"
	@echo "bump - bump the version number via bumpversion."
	@echo '       use `-e BUMPTYPE=minor` to specify `major` or `minor` (default is `patch`).'

bootstrap:
	virtualenv $(VENV)
	$(VENV)/bin/pip install -r dev_requirements.txt

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint:
	flake8 cp_sqlalchemy tests

test:
	$(VENV)/bin/py.test

test-all:
	tox

coverage:
	coverage run --source cp_sqlalchemy setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	rm -f docs/cp_sqlalchemy.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ cp_sqlalchemy
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

release: clean
	python setup.py sdist register -r $(CHEESE) upload -r $(CHEESE)

dist: clean
	python setup.py sdist
	ls -l dist

bump:
	$(VENV)/bin/bumpversion $(BUMPTYPE)

run:
	$(VENV)/bin/honcho start -f Procfile.dev