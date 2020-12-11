.PHONY: build run lint test

lint:
	pipenv run ./scripts/run_lint_python.sh


format:
	pipenv run black .
