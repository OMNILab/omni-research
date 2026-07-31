# OmniResearch

[中文](README.md) | **English**

A suite of AI agent skills for evidence-bound scientific research — collect materials, analyze evidence, make decisions, evaluate ideas, and write findings with clear provenance.

Repository: [OMNILab/omni-research](https://github.com/OMNILab/omni-research)

---

## What you get

OmniResearch turns an AI coding agent into a research co-pilot with a structured workflow:

1. **Start a project** — create a minimal workspace and project context
2. **Collect materials** — papers, repos, web pages, datasets
3. **Analyze evidence** — map claims with strict evidence boundaries (`proven` / `suggested` / `inferred`)
4. **Decide & evaluate** — document architecture choices and validate them
5. **Write up** — save reports to files and get a short summary in chat

You do not need to understand the internal skill packaging model to use it. Install the skills, bootstrap a workspace, then invoke skills as you research.

---

## Quick start

### 1. Install skills

Install foundation first, then the skills you need. See the full guide:

- [Marketplace installation guide](docs/MARKETPLACE-INSTALL.md)

Typical order:

```text
/find-skills omr-core
/find-skills omr-bootstrap
/find-skills omr-collection
/find-skills omr-analyze
/find-skills omr-decision
/find-skills omr-evaluation
/find-skills omr-synthesis
/find-skills omr-idea-note
/find-skills omr-reconcile
```

### 2. Bootstrap a research workspace

```text
/omr-bootstrap "your research topic"
```

This creates only:

- `AGENTS.md` — project instructions for the agent
- `.omr/tree-state.json` — skill progress state

Content folders such as `materials/`, `docs/`, `wiki/`, and `src/` are created **on demand** when a skill first writes into them.

### 3. Run a research loop

| Goal | Invoke |
|------|--------|
| Collect papers / repos / pages | `/omr-collection` |
| Capture a speculative idea | `/omr-idea-note` |
| Map evidence and plan next steps | `/omr-analyze` |
| Record an architecture decision | `/omr-decision` |
| Design and run an evaluation | `/omr-evaluation` |
| Write findings to files + summary | `/omr-synthesis` |
| Update when new evidence arrives | `/omr-reconcile` |

**Example — Evidence-First path**

```text
/omr-bootstrap "agent memory mechanisms"
/omr-collection "https://arxiv.org/abs/2402.12345"
/omr-analyze
/omr-decision
/omr-evaluation
/omr-synthesis --mode survey
```

Synthesis always writes the full report under `docs/<mode>/` and replies with a short summary only (paths, key findings, gate status).

---

## Skills

| Skill | What it does for you | Spec |
|-------|----------------------|------|
| **omr-core** | Shared infrastructure (contracts, patterns, skill tree) | [SKILL.md](skills/omr-core/SKILL.md) |
| **omr-bootstrap** | Start a research workspace | [SKILL.md](skills/omr-bootstrap/SKILL.md) |
| **omr-collection** | Collect papers, repos, web pages, datasets | [SKILL.md](skills/omr-collection/SKILL.md) |
| **omr-analyze** | Evidence map, judgment, research plan | [SKILL.md](skills/omr-analyze/SKILL.md) |
| **omr-decision** | Architecture decision with alternatives | [SKILL.md](skills/omr-decision/SKILL.md) |
| **omr-evaluation** | Experiment design and validation | [SKILL.md](skills/omr-evaluation/SKILL.md) |
| **omr-synthesis** | File-based report + chat summary (+ wiki) | [SKILL.md](skills/omr-synthesis/SKILL.md) |
| **omr-idea-note** | Capture speculative ideas anytime | [SKILL.md](skills/omr-idea-note/SKILL.md) |
| **omr-reconcile** | Update research when evidence changes | [SKILL.md](skills/omr-reconcile/SKILL.md) |

Flow overview: [OMR skills flowchart](docs/omr-skills-flowchart.md)

---

## Research patterns

Start wherever your work already is — you do not have to begin with literature review.

| Pattern | Start with | Best when |
|---------|------------|-----------|
| Evidence-First | `/omr-collection` | Systematic survey from papers |
| Idea-First | `/omr-idea-note` | You have a hypothesis to explore |
| Decision-First | `/omr-decision` | Architecture choice comes first |
| Experiment-First | `/omr-evaluation` | You want to prototype/test early |
| Rapid-Prototype | collect → synthesize | Fast draft from available material |
| Loop | `/omr-idea-note` or `/omr-collection` | Deepen ideas or evidence via Gate L cycles |

Details: [Research patterns](docs/design/patterns.md) · [Workflow examples](docs/design/workflows.md)

---

## Quality gates

Gates keep claims honest and decisions reviewable:

| Gate | When | Ensures |
|------|------|---------|
| **A** | Inside `omr-analyze` | Evidence boundaries and confidence before planning |
| **B** | Before committing a decision | Alternatives and risks are documented |
| **C** | Before trusting evaluation | Metrics and reproducibility are explicit |
| **D** | Before publishing synthesis | Traceability and no over-claiming |
| **L** | Loop pattern (analyze / idea-note) | Iterate deeper or advance to the next stage |

Details: [Quality gates](docs/design/gates.md)

---

## Workspace layout (created as needed)

```text
my-project/
├── AGENTS.md              # created by bootstrap
├── .omr/
│   ├── tree-state.json    # created by bootstrap
│   └── loop-state.json    # when Loop pattern / Gate L is active
├── materials/             # on demand — collected materials
├── docs/                  # on demand — plans, reports, indexes
├── wiki/                  # on demand — living concept pages
└── src/                   # on demand — prototypes / experiments
```

Static skill specs stay in the installed skills (for example under `~/.agents/skills/` or `~/.claude/skills/`). Research projects keep only mutable state in `.omr/`.

Architecture notes: [Workspace architecture](docs/design/architecture.md) · [Outputs model](docs/design/outputs.md)

---

## Documentation

| Audience | Links |
|----------|-------|
| Install & setup | [Marketplace install](docs/MARKETPLACE-INSTALL.md) |
| Design overview | [Design docs index](docs/design/README.md) · [Overview](docs/design/overview.md) · [Principles](docs/design/principles.md) |
| Skills & contracts | [Skills reference](docs/design/skills-reference.md) · [Agent skill spec](docs/agent-skill-spec.md) |
| Day-to-day workflow | [Workflows](docs/design/workflows.md) · [Patterns](docs/design/patterns.md) · [Gates](docs/design/gates.md) |
| Visual map | [Skills flowchart](docs/omr-skills-flowchart.md) |

---

## For contributors

Developer-oriented layout and packaging live under [`skills/`](skills/) and [`scripts/`](scripts/). Prefer the design docs above for system internals; end users should not need them for normal research work.
