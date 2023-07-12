TOP := $(shell dirname "$(abspath $(lastword $(MAKEFILE_LIST)))")
PYTHON ?= python
PIP ?= pip
COVERAGE ?= coverage
PYLINT ?= pylint
PYLINT_RCFILE ?= .pylintrc

.PHONY: help
help:
	@echo
	@echo "▐ Help"
	@echo "▝▀▀▀▀▀▀"
	@echo
	@echo "Available targets:"
	@echo
	@echo  "    help:               this help"
	@echo  "    develop:            run setup.py develop -O1 --install-dir ."
	@echo  "    test:               run all tests"
	@echo  "    clean:              clean the build tree"
	@echo  "    build:              build the wheel and source distribution gzip files"
	@echo
	@echo  "    test_install:       install locally (user level) from https://test.pypi.org/"
	@echo  "    install:            install from https://pypi.org/"
	@echo  "    uninstall:          uninstall with pip"
	@echo
	@echo  "    rpm:                build an RPM package"
	@echo
	@echo  "    test_upload:        use twine to upload to the test pypi repo"
	@echo  "    upload:             use twine to upload to the pypi repo"
	@echo


.PHONY: develop
develop:
	PYTHONPATH=. $(PYTHON) setup.py develop -O1 --install-dir .


.PHONY: test
test:
	$(COVERAGE) erase
	PYTHONPATH=src $(COVERAGE) run -m unittest discover --verbose -s test
	$(COVERAGE) report -m # --skip-empty
	$(PYLINT) --rcfile $(PYLINT_RCFILE) *.py */*.py


.PHONY: clean
clean:
	$(COVERAGE) erase
	rm -rf ./.tox ./.coverage* ./coverage.json ./coverage.xml ./htmlcov/ ./build/ ./dist/
	rm -rf ./easy-install* ./easy_install* ./setuptools.pth ./*.egg-link termcolor_dg_demo termcolor_dg_demo_log
	find . -depth -name '__pycache__' -exec rm -rf \{\} \;
	find . -depth \( -name '*.pyc' -o -name '*.pyo' -o -name '*.egg-info' -o -name '*.py,cover'  \) -exec rm -rf \{\} \;


.PHONY: build
build: clean
	# https://stackoverflow.com/a/46875147 - Fix the image locations, version/tag detection would be nice.
	# Remove URLs
	sed -i 's#https://raw.githubusercontent.com/gunchev/termcolor_dg/.*/##g' README.md
	# Redirect to github
	sed -i 's#](\([a-zA-Z0-9/:_%]*\.png\)#](https://raw.githubusercontent.com/gunchev/termcolor_dg/master/\1#g' README.md
	$(PYTHON) -m build
	# With "$(PYTHON) setup.py sdist" we can get more source formats, but can't upload more than one anyways.
	# Remove URLs
	sed -i 's#https://raw.githubusercontent.com/gunchev/termcolor_dg/.*/##g' README.md


.PHONY: test_install
test_install:
	$(PIP) install --user -i https://test.pypi.org/simple/ termcolor_dg


.PHONY: install
install:
	$(PIP) install --user termcolor_dg


.PHONY: uninstall
uninstall:
	$(PIP) uninstall termcolor_dg


.PHONY: rpm
rpm:
	$(PYTHON) setup.py sdist
	rpmbuild -ba termcolor_dg.spec --define "_sourcedir $(TOP)/dist"


# https://packaging.python.org/en/latest/guides/using-testpypi/
# Upload to https://test.pypi.org/
.PHONY: test_upload
test_upload: build
	twine upload --repository testpypi dist/termcolor_dg-*.whl dist/termcolor_dg-*.tar.gz


# Upload to https://pypi.org/
.PHONY: upload
upload: build
	twine upload dist/termcolor_dg-*.whl dist/termcolor_dg-*.tar.gz
