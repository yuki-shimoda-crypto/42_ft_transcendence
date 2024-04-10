# docker

.PHONY: up
up:
	docker compose up --build

.PHONY: up-d
up-d:
	docker compose up -d --build

.PHONY: down
down:
	docker compose down

.PHONY: down-v
down-v:
	docker compose down -v

.PHONY: exec-db
exec-db:
	docker compose exec -it db bash

.PHONY: exec-web_dev
exec-web_dev:
	docker compose exec -it web_dev zsh

.PHONY: exec-web_prod
exec-web_prod:
	docker compose exec -it web_prod bash

.PHONY: logs
logs:
	docker compose logs

.PHONY: logs-f
logs-f:
	docker compose logs -f

.PHONY: logs-F
logs-F:
	docker compose logs -f --tail 0

.PHONY: ps
ps:
	docker compose ps

.PHONY: ps-a
ps-a:
	docker compose ps -a

# format
.PHONY: format
format: format-CSS format-HTML format-JavaScript format-MD format-Python

.PHONY: format-CSS
format-CSS:
	-npx prettier "**/*.css" --write
	-npx stylelint "**/*.{css,html,js}" --fix

.PHONY: format-HTML
format-HTML:
	-npx prettier "**/*.html" --write
	-npx stylelint "**/*.html" --fix

.PHONY: format-JavaScript
format-JavaScript:
	-npx prettier "**/*.js" --write
	-npx stylelint "**/*.js" --fix

.PHONY: format-MD
format-MD:
	-npx prettier "**/*.md" --write

.PHONY: format-Python
format-Python:
	-black .
	-isort .

# lint
.PHONY: lint
lint: lint-CSS lint-HTML lint-Dockerfile lint-JavaScript lint-MD lint-Python lint-YAML

.PHONY: lint-CSS
lint-CSS:
	npx prettier "**/*.css" --check
	npx stylelint "**/*.{css,html,js}"

.PHONY: lint-HTML
lint-HTML:
	npx htmlhint "**/*.html"
	npx stylelint "**/*.html"

.PHONY: lint-Dockerfile
lint-Dockerfile:
	hadolint Dockerfile Dockerfile.dev

.PHONY: lint-JavaScript
lint-JavaScript:
	npx eslint .
	npx prettier "**/*.js" --check
	npx stylelint "**/*.js"

.PHONY: lint-MD
lint-MD:
	npx prettier "**/*.md" --check

.PHONY: lint-Python
lint-Python:
	black --check .
	flake8 .
	isort --check-only .
	mypy .

.PHONY: lint-YAML
lint-YAML:
	yamllint .

# test
.PHONY: test
test:
	pytest

