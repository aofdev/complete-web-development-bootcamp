.PHONY: clean-pyc help lint init setup docker-start docker-stop
.DEFAULT_GOAL := help
ENV_DIR := ~/.pyenv/versions/complete-web-development-bootcamp
PROJECTNAME := $(shell basename "$(PWD)")

## setup: Initialize project
setup: init docker-start

## init: install the package to the active Python's site-packages
init:
ifeq ($(wildcard $(ENV_DIR)),)
	@echo "Initialize pyenv virtual environment"
	pyenv activate 3.8.5 complete-web-development-bootcamp || pyenv install 3.8.5 && pyenv virtualenv 3.8.5 complete-web-development-bootcamp
endif
	@echo "Install python requirements"
	$(ENV_DIR)/bin/pip install -r app/requirements.txt

	@echo "Cleaning cache python file artifacts"
	@make clean-pyc

	@echo "\nActivate the env"
	source $(ENV_DIR)/bin/activate && (exec zsh || exec bash)

## start: Start app
start:
	@ echo "> Start app"
	@ uvicorn main:app --reload --app-dir app

## docker-start: Start docker-compose
docker-start:
	@ echo "> Start development environment"
	@ docker-compose up -d --build

## docker-stop: Stop docker-compose
docker-stop:
	@ echo "> Stop development environment"
	@ docker-compose down

## mockdata: mock data
mockdata:
	@ echo "> Start mock data"
	@ echo "> Import development database"
	@ ./seed/import.sh

## clean-pyc: remove Python file artifacts
clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

## lint: check style with flake8
lint:
	@ flake8 app

help: Makefile
	@echo
	@echo " Choose a command run in "$(PROJECTNAME)":"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'
	@echo
