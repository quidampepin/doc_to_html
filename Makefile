.PHONY: default run install lint lint-ci bandit

default:

run:
	@python app.py

install:
	@pip install -r requirements.txt

install-dev:
	@pip install -r requirements-dev.txt

lint: 
	@flake8 .

fmt:
	@black .

fmt-ci:
	@black --check .

bandit:
	@bandit -r -ll *.py