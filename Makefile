#!make
	
define USAGE
Commands:
    check-format                Check code formats
    install                     Install requirements.txt dependencies
    lint                        Run linter (flake8)
    test                        Run tests and validate project
endef

export USAGE

help:
	@echo "$$USAGE"

lint:
	@flake8 --ignore E501,W503,E203

install:
	@pip3 install -r requirements.txt

check-format:
	@black --check .

build:
	@python3 -m build
