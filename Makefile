.PHONY: lint format run dev

lint:
	pipenv run ./scripts/run_lint_python.sh

format:
	pipenv run isort .
	pipenv run black .

run:
	pipenv run python ./main.py

dev:
	ln -fs .development.env .env
	pipenv run python ./main.py