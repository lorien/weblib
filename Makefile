.PHONY: build venv deps clean release check test docs

build: venv deps

venv:
	virtualenv -p python3 .env

deps:
	.env/bin/pip install -r requirements_dev.txt
	.env/bin/pip install -e .[full]

clean:
	find -name '*.pyc' -delete
	find -name '*.swp' -delete
	find -name __pycache__ -delete

release:
	git push; git push --tags; rm dist/*; python3 setup.py clean sdist; twine upload dist/*

check:
	python setup.py check -s \
		&& pyroma --min 10 . \
		&& pylint setup.py weblib tests \
		&& flake8 setup.py weblib tests \
		&& pytype setup.py weblib tests \
		&& mypy setup.py weblib tests

test:
	coverage run -m pytest \
		&& coverage report -m

docs:
	if [ -e docs/_build ]; then rm -r docs/_build; fi
	sphinx-build -b html docs docs/_build
