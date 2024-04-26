#!/usr/bin/env make

# Change this to be your variant of the python command
# Set the env variable PYTHON to another value if needed
# PYTHON=python3 make version
PYTHON ?= python # python3 py

# Print out colored action message
MESSAGE = printf "\033[32;01m---> $(1)\033[0m\n"

all:


# ---------------------------------------------------------
# Check the current python executable.
#
version:
	@printf "Currently using executable: $(PYTHON)\n"
	which $(PYTHON)
	$(PYTHON) --version


# ---------------------------------------------------------
# Setup a venv and install packages.
#
venv:
	[ -d .venv ] || $(PYTHON) -m venv .venv
	@printf "Now activate the Python virtual environment.\n"
	@printf "On Unix and Mac, do:\n"
	@printf ". .venv/bin/activate\n"
	@printf "On Windows (bash terminal), do:\n"
	@printf ". .venv/Scripts/activate\n"
	@printf "Type 'deactivate' to deactivate.\n"

install:
	$(PYTHON) -m pip install -r requirements.txt
	pre-commit install

installed:
	$(PYTHON) -m pip list


# ---------------------------------------------------------
# Pre-commit.
#
pre-commit:
	pre-commit run

pre-commit-all:
	pre-commit run --all-files


# ---------------------------------------------------------
# Cleanup generated and installed files.
#
clean:
	@$(call MESSAGE,$@)
	rm -f .coverage *.pyc
	rm -rf __pycache__
	rm -rf htmlcov

clean-doc: clean
	@$(call MESSAGE,$@)
	rm -rf doc

clean-all: clean clean-doc
	@$(call MESSAGE,$@)
	rm -rf .venv


# ---------------------------------------------------------
# Work with unit test and code coverage.
#
unittest:
	@$(call MESSAGE,$@)
	 $(PYTHON) -m unittest discover

coverage:
	@$(call MESSAGE,$@)
	coverage run -m unittest discover
	coverage html
	coverage report -m

coverage-xml:
	@$(call MESSAGE,$@)
	coverage run -m unittest discover
	coverage xml

test: unittest coverage


# ---------------------------------------------------------
# Generate documentation.
#
pdoc:
	@$(call MESSAGE,$@)
	pdoc --force --html --output-dir doc/pdoc/account account/*.py
	pdoc --force --html --output-dir doc/pdoc/database database/*.py
	pdoc --force --html --output-dir doc/pdoc/schedule schedule/*.py
