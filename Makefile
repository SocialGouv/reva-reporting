SHELL := /bin/bash
.SHELLFLAGS = -ec
.ONESHELL:
.SILENT:

.EXPORT_ALL_VARIABLES:
REPO_DIRECTORY:=$(shell pwd)
PYTHONPATH:=${PYTHONPATH}:${REPO_DIRECTORY}

.PHONY: help
help:
	echo "❓ Use \`make <target>'"
	grep -E '^\.PHONY: [a-zA-Z0-9_-]+ .*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = "(: |##)"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$3}'


.PHONY: lint  ## 🐍 Lint Python files to conform to the PEP 8 style guide
lint:
	flake8

.PHONY: conda_env  ## 🐍 Create a Python conda environment
conda_env:
	conda create --name reva-reporting python=3.9 -y
	conda activate reva-reporting

.PHONY: dependencies  ## ⏬ Install development dependencies
dependencies:
	pip install -e .[dev]

.PHONY: unit_tests  ## ✅ Launch the unit tests
unit_tests:
	pytest tests

.PHONY: local_postgres  ## 📥 Create a local Postgres
local_postgres:
	docker rm reva-datawarehouse-postgres
	docker run --name reva-datawarehouse-postgres -p 5433:5432 -e POSTGRES_DB=reva-datawarehouse -e POSTGRES_PASSWORD=password -d postgres:9.6
