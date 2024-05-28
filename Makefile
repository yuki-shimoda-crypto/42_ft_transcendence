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
.PHONY: django-web_dev-runserver
django-web_dev-runserver:
	docker compose exec -it web_dev python3 PongChat/manage.py runserver 0.0.0.0:8000

.PHONY: django-web_dev-migrate
django-web_dev-migrate:
	docker compose exec -it web_dev python3 PongChat/manage.py migrate

.PHONY: django-web_dev-createsuperuser
django-web_dev-createsuperuser:
	docker compose exec -it web_dev python3 PongChat/manage.py createsuperuser

.PHONY: django-web_dev-shell
django-web_dev-shell:
	docker compose exec -it web_dev python3 PongChat/manage.py shell

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
.PHONY: format-web_dev
format-web_dev: format-web_dev-CSS format-web_dev-HTML format-web_dev-JavaScript format-web_dev-MD format-web_dev-Python

.PHONY: format-web_dev-CSS
format-web_dev-CSS:
	docker compose exec -it web_dev npx prettier "**/*.css" --write
	docker compose exec -it web_dev npx stylelint "**/*.{css,html,js}" --fix

.PHONY: format-web_dev-HTML
format-web_dev-HTML:
	docker compose exec -it web_dev npx prettier "**/*.html" --write
	docker compose exec -it web_dev npx stylelint "**/*.html" --fix

.PHONY: format-web_dev-JavaScript
format-web_dev-JavaScript:
	docker compose exec -it web_dev npx prettier "**/*.js" --write
	docker compose exec -it web_dev npx stylelint "**/*.js" --fix

.PHONY: format-web_dev-MD
format-web_dev-MD:
	docker compose exec -it web_dev npx prettier "**/*.md" --write

.PHONY: format-web_dev-Python
format-web_dev-Python:
	docker compose exec -it web_dev black .
	docker compose exec -it web_dev isort .

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
.PHONY: lint-web_dev
lint-web_dev: lint-web_dev-CSS lint-web_dev-HTML lint-web_dev-Dockerfile lint-web_dev-JavaScript lint-web_dev-MD lint-web_dev-Python lint-web_dev-YAML

.PHONY: lint-web_dev-CSS
lint-web_dev-CSS:
	docker compose exec -it web_dev npx prettier "**/*.css" --check
	docker compose exec -it web_dev npx stylelint "**/*.{css,html,js}"

.PHONY: lint-web_dev-HTML
lint-web_dev-HTML:
	docker compose exec -it web_dev npx htmlhint "**/*.html"
	docker compose exec -it web_dev npx stylelint "**/*.html"

.PHONY: lint-web_dev-Dockerfile
lint-web_dev-Dockerfile:
	docker compose exec -it web_dev hadolint Dockerfile Dockerfile.dev

.PHONY: lint-web_dev-JavaScript
lint-web_dev-JavaScript:
	docker compose exec -it web_dev npx eslint .
	docker compose exec -it web_dev npx prettier "**/*.js" --check
	docker compose exec -it web_dev npx stylelint "**/*.js"

.PHONY: lint-web_dev-MD
lint-web_dev-MD:
	docker compose exec -it web_dev npx prettier "**/*.md" --check

.PHONY: lint-web_dev-Python
lint-web_dev-Python:
	docker compose exec -it web_dev black --check .
	docker compose exec -it web_dev flake8 .
	docker compose exec -it web_dev isort --check-only .
	docker compose exec -it web_dev mypy .

.PHONY: lint-web_dev-YAML
lint-web_dev-YAML:
	docker compose exec -it web_dev yamllint .

# test
.PHONY: test
test:
	pytest
