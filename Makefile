.PHONY: init test clean build docs

init:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	python -m pytest tests/ --cov=kkexpr --cov-report=term-missing

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

build:
	python setup.py build
	python setup.py sdist bdist_wheel

docs:
	cd docs && make html

lint:
	flake8 kkexpr tests
	mypy kkexpr

format:
	black kkexpr tests 