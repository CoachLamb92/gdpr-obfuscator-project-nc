PROJECT_NAME = obfuscator-project
PYTHON_INTERPRETER = python
WD=$(shell pwd)
PYTHONPATH=${WD}
SHELL := /bin/bash
PROFILE = default
PIP:=pip

create-environment:
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> check python3 version"
	( \
		$(PYTHON_INTERPRETER) --version; \
	)
	@echo ">>> Setting up VirtualEnv."
	( \
	    $(PIP) install -q virtualenv virtualenvwrapper; \
	    virtualenv venv --python=$(PYTHON_INTERPRETER); \
	)

# Define utility variable to help calling Python from the virtual environment
ACTIVATE_ENV := source venv/bin/activate

# Execute python related functionalities from within the project's environment
define execute_in_env
	$(ACTIVATE_ENV) && $1
endef


requirements: create-environment
	$(call execute_in_env, $(PIP) install -r ./requirements.txt)

################################################################################################################
# Set Up
## Install Flake8
flake8:
	$(call execute_in_env, $(PIP) install flake8)

## Install pytest coverage
pytest-cov:
	$(call execute_in_env, $(PIP) install pytest-cov)

## Install bandit
bandit:
	$(call execute_in_env, $(PIP) install bandit)

## Set up dev requirements
dev-setup: pytest-cov flake8 bandit


# Build / Run
## Run the PEP8 checks (flake8)
flake8-src:
	$(call execute_in_env, flake8 src/)
flake8-tests:
	$(call execute_in_env, flake8 tests/)

## Run the security test (bandit)
security-test:
	$(call execute_in_env, bandit -lll */*.py)

## Run the unit tests
unit-test:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest tests/ -v)

## Run the coverage check
check-coverage:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest --cov=src/ tests/ --cov-fail-under=90)

## Run all checks
run-checks: security-test flake8-src flake8-tests unit-test check-coverage

## Run the showcase file
showcase:
	$(call execute_in_env, python showcase_project.py)

########################################################################
