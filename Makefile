# OmniResearch — developer tasks
.PHONY: help format lint check

PYTHON_PATHS := skills scripts

help:
	@echo "Targets:"
	@echo "  format  Format all Python scripts (ruff format + import sort)"
	@echo "  lint    Lint all Python scripts (ruff check)"
	@echo "  check   Verify format + lint without writing (CI)"

format:
	ruff format $(PYTHON_PATHS)
	ruff check --select I --fix $(PYTHON_PATHS)

lint:
	ruff check $(PYTHON_PATHS)

check:
	ruff format --check $(PYTHON_PATHS)
	ruff check $(PYTHON_PATHS)
