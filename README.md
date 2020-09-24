# Complete Web Development Bootcamp 🔥

![complete-web-development-bootcamp](./cwdb.svg)

## Prerequisite

- [Python 3.6+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Pyenv](https://github.com/pyenv/pyenv)

## Initialize Project

Run this command everytime `before` start to develop this repo

```sh
make setup
```

## Run App

```sh
make docker-start
```


## Seed data to database

```sh
make mockdata
```

## Stop app and database

```sh
make docker-stop
```

## Manual

Run `make help` to list available commands:

```sh
λ  make help
Choose a command run in complete-web-development-bootcamp:

setup          Initialize project
init           install the package to the active Python is site-packages
start          Start app
docker-start   Start docker-compose
docker-stop    Stop docker-compose
mockdata       mock data
clean-pyc      remove Python file artifacts
lint           check style with flake8
```

## Code Style Guide

> Use the [autopep8](https://pypi.org/project/autopep8) auto-formatter to avoid arguing over formatting.
