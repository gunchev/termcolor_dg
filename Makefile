TOP := $(shell dirname "$(abspath $(lastword $(MAKEFILE_LIST)))")


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
	PYTHONPATH=. python setup.py develop -O1 --install-dir .


.PHONY: test
test:
	coverage erase
	PYTHONPATH=src coverage run -m unittest discover --verbose -s test
	# coverage combine  # Will fail if only one run...
	coverage report -m --skip-empty
	# pylint2 $(shell git ls-files '*.py')
	# pylint $(shell git ls-files '*.py')
	pylint *.py */*.py


.PHONY: clean
clean:
	coverage erase
	rm -rf ./.tox ./.coverage* ./coverage.json ./coverage.xml ./htmlcov/ ./build/ ./dist/
	rm -rf ./easy-install* ./easy_install* ./setuptools.pth ./*.egg-link termcolor_dg_demo termcolor_dg_demo_log
	find . -depth -name '__pycache__' -exec rm -rf \{\} \;
	find . -depth \( -name '*.pyc' -o -name '*.pyo' -o -name '*.egg-info' -o -name '*.py,cover'  \) -exec rm -rf \{\} \;


.PHONY: build
build: clean
	# fix the image locations, version/tag detection would be nice
	# Remove URLs
	sed -i 's#https://gitlab.com/dngunchev/termcolor_dg/.*/##g' README.md
	sed -i 's#](\([a-zA-Z0-9/:_%]*\.png\)#](https://gitlab.com/dngunchev/termcolor_dg/-/raw/master/\1#g' README.md
	python -m build
	sed -i 's#https://gitlab.com/dngunchev/termcolor_dg/.*/##g' README.md
	# python setup.py sdist  # gives more source formats, but can't upload more than one anyways


.PHONY: test_install
test_install:
	pip install --user -i https://test.pypi.org/simple/ termcolor_dg


.PHONY: install
install:
	pip install --user termcolor_dg


.PHONY: uninstall
uninstall:
	pip uninstall termcolor_dg


.PHONY: rpm
rpm: build
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
