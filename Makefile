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

.PHONY: exec-web-dev
exec-web-dev:
	docker compose exec -it web-dev zsh

.PHONY: exec-web-prod
exec-web-prod:
	docker compose exec -it web-prod bash

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

# django
.PHONY: django-runserver
django-runserver:
	python3 PongChat/manage.py runserver 0.0.0.0:8000

.PHONY: django-migrate
django-migrate:
	python3 PongChat/manage.py migrate

.PHONY: django-createsuperuser
django-createsuperuser:
	python3 PongChat/manage.py createsuperuser

.PHONY: django-shell
django-shell:
	python3 PongChat/manage.py shell

# Django management commands inside Docker container
.PHONY: django-web-dev-runserver
django-web-dev-runserver:
	docker compose exec -it web-dev python3 PongChat/manage.py runserver 0.0.0.0:8000

.PHONY: django-web-dev-migrate
django-web-dev-migrate:
	docker compose exec -it web-dev python3 PongChat/manage.py migrate

.PHONY: django-web-dev-createsuperuser
django-web-dev-createsuperuser:
	docker compose exec -it web-dev python3 PongChat/manage.py createsuperuser

.PHONY: django-web-dev-shell
django-web-dev-shell:
	docker compose exec -it web-dev python3 PongChat/manage.py shell

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

# Format commands inside Docker container
.PHONY: format-web-dev
format-web-dev: format-web-dev-CSS format-web-dev-HTML format-web-dev-JavaScript format-web-dev-MD format-web-dev-Python

.PHONY: format-web-dev-CSS
format-web-dev-CSS:
	docker compose exec -it web-dev npx prettier "**/*.css" --write
	docker compose exec -it web-dev npx stylelint "**/*.{css,html,js}" --fix

.PHONY: format-web-dev-HTML
format-web-dev-HTML:
	docker compose exec -it web-dev npx prettier "**/*.html" --write
	docker compose exec -it web-dev npx stylelint "**/*.html" --fix

.PHONY: format-web-dev-JavaScript
format-web-dev-JavaScript:
	docker compose exec -it web-dev npx prettier "**/*.js" --write
	docker compose exec -it web-dev npx stylelint "**/*.js" --fix

.PHONY: format-web-dev-MD
format-web-dev-MD:
	docker compose exec -it web-dev npx prettier "**/*.md" --write

.PHONY: format-web-dev-Python
format-web-dev-Python:
	docker compose exec -it web-dev black .
	docker compose exec -it web-dev isort .

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

# Lint commands inside Docker container
.PHONY: lint-web-dev
lint-web-dev: lint-web-dev-CSS lint-web-dev-HTML lint-web-dev-Dockerfile lint-web-dev-JavaScript lint-web-dev-MD lint-web-dev-Python lint-web-dev-YAML

.PHONY: lint-web-dev-CSS
lint-web-dev-CSS:
	docker compose exec -it web-dev npx prettier "**/*.css" --check
	docker compose exec -it web-dev npx stylelint "**/*.{css,html,js}"

.PHONY: lint-web-dev-HTML
lint-web-dev-HTML:
	docker compose exec -it web-dev npx htmlhint "**/*.html"
	docker compose exec -it web-dev npx stylelint "**/*.html"

.PHONY: lint-web-dev-Dockerfile
lint-web-dev-Dockerfile:
	docker compose exec -it web-dev hadolint Dockerfile Dockerfile.dev

.PHONY: lint-web-dev-JavaScript
lint-web-dev-JavaScript:
	docker compose exec -it web-dev npx eslint .
	docker compose exec -it web-dev npx prettier "**/*.js" --check
	docker compose exec -it web-dev npx stylelint "**/*.js"

.PHONY: lint-web-dev-MD
lint-web-dev-MD:
	docker compose exec -it web-dev npx prettier "**/*.md" --check

.PHONY: lint-web-dev-Python
lint-web-dev-Python:
	docker compose exec -it web-dev black --check .
	docker compose exec -it web-dev flake8 .
	docker compose exec -it web-dev isort --check-only .
	docker compose exec -it web-dev mypy .

.PHONY: lint-web-dev-YAML
lint-web-dev-YAML:
	docker compose exec -it web-dev yamllint .

# test
.PHONY: test
test:
	PYTHONPATH=$(shell pwd)/PongChat pytest --cache-clear

.PHONY: test-cov
test-cov:
	pytest --cov

.PHONY: test-html
test-html:
	pytest --cov=. --cov-report=html
