.PHONY: test help
.DEFAULT_GOAL := help

SHELL := /bin/bash

export ROOTDIR:=$(shell pwd)
export CURRENT_VERSION:=$(shell python3.6 -c "import os; about={}; exec(open(os.path.join('meme_generator', '_meta.py')).read(), about); print(about['__version__'])")
export CURRENT_USER:=$(shell id -u ${USER}):$(shell id -g ${USER})
define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"


help:
	@python3.6 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


# Development

env-create: ## (re)create a development environment using tox
	tox -e meme_generator --recreate
	@echo -e "\r\nYou can activate the environment with:\r\n\r\n$$ source ./.tox/meme_generator/bin/activate\r\n"

env-compile: ## compile requirements.txt / requirements-dev.txt using pip-tools
	pip-compile --no-header --no-emit-trusted-host --output-file requirements.txt requirements.in
	pip-compile --no-header --no-emit-trusted-host --output-file requirements-dev.txt requirements-dev.in

env-sync: ## synchornize requirements.txt /requirements-dev.txt with tox virtualenv using pip tools
	pip-sync requirements.txt requirements-dev.txt

env-add-package: ## add new dependency to requirements.in
	@[ "${PACKAGE}" ] || ( echo "PACKAGE is not set"; exit 1 )
	@grep -qxF '${PACKAGE}' requirements.in || echo -e "\n${PACKAGE}" >> requirements.in
	$(MAKE) env-compile
	$(MAKE) env-create
	@echo "Added $(PACKAGE) to requirements.in"

env-add-dev-package: ## add new development dependency to requirements-dev.in
	@[ "${PACKAGE}" ] || ( echo "PACKAGE is not set"; exit 1 )
	@grep -qxF '${PACKAGE}' requirements-dev.in || echo -e "\n${PACKAGE}" >> requirements-dev.in
	$(MAKE) env-compile
	$(MAKE) env-create
	@echo "Added $(PACKAGE) to requirements-dev.in"

env-upgrade-package: ## upgrade the package specified on PACKAGE
	@[ "${PACKAGE}" ] || ( echo "PACKAGE is not set"; exit 1 )
	pip-compile --upgrade-package ${PACKAGE} --no-index --no-header --no-emit-trusted-host --output-file requirements.txt requirements.in

env-upgrade-dev-package: ## upgrade the development package specified on PACKAGE
	@[ "${PACKAGE}" ] || ( echo "PACKAGE is not set"; exit 1 )
	pip-compile --upgrade-package ${PACKAGE} --no-index --no-header --no-emit-trusted-host --output-file requirements-dev.txt requirements-dev.in

env-upgrade-all: ## upgrade all dependencies
	pip-compile --upgrade --no-index --no-header --no-emit-trusted-host --output-file requirements.txt requirements.in
	pip-compile --upgrade --no-index --no-header --no-emit-trusted-host --output-file requirements-dev.txt requirements-dev.in

### QUALITY

test: ## run tests with pytest
	PYTHONPATH=$$(pwd)/meme_generator py.test

check-type-annotations-pep484:
	mypy .

check-docstrings-pep257:
	pydocstyle .

check-code-style-pep8:
	pycodestyle .

# Package & Publish

version: ## shows the current package version
	@echo $(CURRENT_VERSION)

# Calculates target version for a tag
ifneq ($(PART),)
TARGET_VERSION := $(shell bump2version --dry-run --allow-dirty --current-version $(CURRENT_VERSION) $(PART) --list | grep new_version= | sed -r s,"^.*=",,)
endif

version-next: ## shows the next version to bump
	@[ "${PART}" ] || ( echo "You must provide which PART of semantic version you want to bump: major.minor.patch"; exit 1 )
	@echo $(TARGET_VERSION)

tag-bump: ## bumps version and creates and commits tag
	@[ "${PART}" ] || ( echo "You must provide which PART of semantic version you want to bump: major.minor.patch"; exit 1 )
	@if [ $(shell if grep -Fq '## $(TARGET_VERSION) ' CHANGELOG.md; then echo "yes"; else echo "no"; fi) = "yes" ];                 \
	then							                                           \
		echo Going to commit tag v$(TARGET_VERSION);                           \
		bump2version  --commit --tag --current-version $(CURRENT_VERSION) $(PART); \
		echo "Please push tag to GitLab with:  ";                                          \
		echo "make tag-push";                                          \
	else		                                                               \
		echo "Tag for v$(TARGET_VERSION) aborted. Please update CHANGELOG.md with the description of changes";   \
	fi

tag-push: ## Pushes tag for current version
	git push origin v$(CURRENT_VERSION)
	git push

tag-delete: ## deletes tag
	git tag -d $(TAG)
	git push --delete origin $(TAG)

dist: clean-build clean-pyc ## build wheel package (compiled)
	python setup.py bdist_wheel --cythonize

dist-dev: clean-build clean-pyc ## build wheel package (source code)
	python setup.py bdist_wheel

sdist: clean-build clean-pyc ## build a source distribution (sdist)
	python setup.py sdist

# Cleanup

clean-all: clean clean-env clean-docker ## remove everything (artifacts, environments, etc.)

clean: clean-build clean-dist clean-pyc clean-test ## remove all build, test, coverage and Python artifacts


clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr .eggs/
	find . ! -path './.tox/*' -name '*.egg-info' -exec rm -fr {} +
	find . ! -path './.tox/*' -name '*.egg' -exec rm -f {} +
	find meme_generator -name '*.c' -exec rm -f {} +

clean-dist: ## remove dist packages
	rm -fr dist/

clean-pyc: ## remove Python file artifacts
	find . ! -path './.tox/*' -name '*.pyc' -exec rm -f {} +
	find . ! -path './.tox/*' -name '*.pyo' -exec rm -f {} +
	find . ! -path './.tox/*' -name '*~' -exec rm -f {} +
	find . ! -path './.tox/*' -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -rf .pytest_cache
	rm -f .coverage

clean-env: ## remove virtual environments (created by tox)
	rm -fr .tox/

clean-docker: ## remove Docker images, containers, etc.
	docker-compose -f docker/dev/docker-compose.yml down --rmi local --volumes --remove-orphans

enable-sudo:
	@sudo echo "sudo enabled"
