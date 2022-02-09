.PHONY: all
all: develop


.PHONY: develop
develop:
	PYTHONPATH=. python setup.py develop -O1 --install-dir .


.PHONY: test
test:
	coverage erase
	PYTHONPATH=src coverage run -m unittest discover --verbose -s test
	# coverage combine  # Will fail if only one run...
	coverage report -m --skip-empty
	pylint2 $(shell git ls-files '*.py')
	pylint $(shell git ls-files '*.py')


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


# https://packaging.python.org/en/latest/guides/using-testpypi/
# Upload to https://test.pypi.org/
.PHONY: test_upload
test_upload: build
	twine upload --repository testpypi dist/termcolor_dg-*.whl dist/termcolor_dg-*.tar.gz


.PHONY: test_install
test_install:
	pip install --user -i https://test.pypi.org/simple/ termcolor_dg


.PHONY: test_uninstall
test_uninstall:
	pip uninstall termcolor_dg


.PHONY: upload
upload: build
	twine upload dist/termcolor_dg-*.whl dist/termcolor_dg-*.tar.gz
