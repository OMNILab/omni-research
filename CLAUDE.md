# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**OmniSkills** — A suite of AI agent capabilities designed to accelerate scientific innovation. The repo is organized as a monorepo with independent research projects under `thirdparty/` and shared skills under `skills/`.

## Repository Structure

- `docs/` — Top-level documentation
- `skills/` — Shared AI agent skills (OmniSkills)
- `thirdparty/` — Independent research subprojects, each with their own CLAUDE.md, build system, and conventions
  - `agent-memory-survey/` — Agent Memory research (survey, prototypes, reference indexing)

## Working with Subprojects

Each subproject in `thirdparty/` is self-contained with its own `CLAUDE.md`, `AGENTS.md`, build tools, and test suite. **Always consult the subproject's own `CLAUDE.md` first** when working within it.

### agent-memory-survey

Key commands (must run from within `thirdparty/agent-memory-survey/`):

```bash
uv venv "$HOME/.venvs/agentresearch"
source "$HOME/.venvs/agentresearch/bin/activate"
uv sync --active --extra dev

make test        # run all tests
make lint        # ruff check
make refs        # rebuild reference indexes
make eval        # memory lifecycle evaluation
make docs        # check doc links
```

Single test: `uv run --active --extra dev pytest tests/test_memory.py -q`

- Python 3.10+, managed with `uv`
- Tech stack: chromadb, networkx, sentence-transformers, pandas
- Linting: ruff (E, F, I, B rules), line-length 88
