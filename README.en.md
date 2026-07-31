# OmniResearch

[中文](README.md) | **English**

Reusable AI agent skills for serious research: collect materials, bound evidence, decide, evaluate, and write findings back to files with clear provenance.

Repository: [OMNILab/omni-research](https://github.com/OMNILab/omni-research)

---

## Vision

**Research ≠ information gathering.** OmniResearch (OMR) turns deep research into a composable skill lifecycle:

```text
Collect → Analyze (define · evidence · judge · plan) → Decide → Validate → Write back
```

The goal is not “dump a pile of links,” but to move an investigation forward under explicit evidence boundaries, leaving inspectable, reproducible, and revisable artifacts.

---

## When to use it

| Scenario | How you use OMR |
|----------|-----------------|
| **Literature survey** | Collect papers & repos → map evidence → synthesize a survey |
| **Idea-led exploration** | Capture a hypothesis → decide / experiment → backfill evidence |
| **Architecture choice** | Document alternatives first → constrain with evidence & eval |
| **Fast hypothesis check** | Prototype and evaluate early → then analyze & synthesize |
| **Ongoing research** | Reconcile when new evidence arrives; keep versions & blast radius |
| **Multi-agent / handoff** | All state lives in files (`.omr/`, `docs/`, `materials/`) |

After install, invoke skills via slash commands in Cursor, Claude Code, Codex, and other Agent Skills–compatible environments.

---

## Design philosophy

One line: **Skills + Tree + Gates + Patterns + Reconciliation**.

| Principle | Meaning |
|-----------|---------|
| **Evidence boundaries** | Label claims `proven` / `suggested` / `inferred` — no over-claiming |
| **Composable skills** | Skills are ingredients, not a fixed pipeline; patterns are saved recipes |
| **Artifact-bound state** | Progress and conclusions live in files — no hidden memory state |
| **Quality gates** | Gates A–D govern advancement; Gate L chooses “go deeper vs move on” |
| **Traceable writeback** | Full reports on disk; chat returns only a short summary + paths |
| **Iteration is normal** | New evidence triggers reconcile instead of starting from scratch |

Unlike one-shot “summarize this page” tools, OMR emphasizes **boundaries, gates, patterns, and reproducible artifacts** for work that must stand up to scrutiny.

More: [Overview](docs/design/overview.md) · [Principles](docs/design/principles.md)

---

## Install skills

**Install all 9 skills in one batch** so the full lifecycle works — collection through synthesis, plus idea notes and reconciliation. Partial installs leave later stages unavailable.

Full guide (three methods, per-agent paths, troubleshooting): **[Skill installation](docs/INSTALL.md)**

### Method 1 — `npx skills add` (recommended)

One command across Cursor / Claude Code / Codex and other agents:

```bash
npx skills add OMNILab/omni-research --skill '*' -g -y
```

### Method 2 — Claude Code marketplace

```text
/plugin marketplace add OMNILab/omni-research
```

Install the full set of `omr-*` skills from the **omniresearch** marketplace in the plugin UI.

### Method 3 — Download and extract

```bash
git clone https://github.com/OMNILab/omni-research.git
cp -R omni-research/skills/omr-* ~/.cursor/skills/   # Cursor example
# or ~/.claude/skills/, ~/.agents/skills/, etc. — see install guide
```

You can also package `.skill` archives and unzip them into the agent skills directory (see install guide).

---

## Quick start

### 1. Bootstrap a research workspace

```text
/omr-bootstrap "your research topic"
```

This creates only:

- `AGENTS.md` — project instructions for the agent
- `.omr/tree-state.json` — skill progress state

Content folders such as `materials/`, `docs/`, `wiki/`, and `src/` are created **on demand** when a skill first writes into them.

### 2. Run a research loop

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

Static skill specs stay in the installed skills directory (for example `~/.cursor/skills/`, `~/.claude/skills/`, or `~/.agents/skills/`). Research projects keep only mutable state in `.omr/`.

Architecture notes: [Workspace architecture](docs/design/architecture.md) · [Outputs model](docs/design/outputs.md)

---

## Documentation

| Audience | Links |
|----------|-------|
| Install & setup | [Skill installation](docs/INSTALL.md) |
| Design overview | [Design docs index](docs/design/README.md) · [Overview](docs/design/overview.md) · [Principles](docs/design/principles.md) |
| Skills & contracts | [Skills reference](docs/design/skills-reference.md) · [Agent skill spec](docs/agent-skill-spec.md) |
| Day-to-day workflow | [Workflows](docs/design/workflows.md) · [Patterns](docs/design/patterns.md) · [Gates](docs/design/gates.md) |
| Visual map | [Skills flowchart](docs/omr-skills-flowchart.md) |

---

## For contributors

Developer-oriented layout and packaging live under [`skills/`](skills/) and [`scripts/`](scripts/). Prefer the [install guide](docs/INSTALL.md) and design docs above for day-to-day research; end users should not need packaging details for normal work.
