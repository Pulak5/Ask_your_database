.PHONY: env up down test lint eval train serve deploy-aws destroy-aws clean

ENV ?= .venv
PY := $(ENV)/bin/python
PIP := $(ENV)/bin/pip

env:
	@echo "Creating local conda env at $(ENV)"
	conda create --prefix $(ENV) python=3.11 -y

install:
	$(PIP) install -e .

up:
	docker compose up -d --build

down:
	docker compose down -v

test:
	$(PY) -m pytest tests -q

lint:
	$(PY) -m ruff check src tests

eval:
	$(PY) -m src.eval.run_eval --help

train:
	$(PY) -m src.training.train_lora --help

serve:
	bash src/serving/serve_vllm.sh

deploy-aws:
	cd infra/terraform && terraform apply -auto-approve

destroy-aws:
	cd infra/terraform && terraform destroy -auto-approve

clean:
	rm -rf results outputs build *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true