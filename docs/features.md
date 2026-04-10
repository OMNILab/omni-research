# Features Design of Omni-Research Skills

## Overall Rules

- Follow agent skill spec strictly
- Leverage `skill-creator` skill primarily to manage skills
- Follow Claude skill marketplace patterns
- **Evidence-bound research**: All claims traceable to sources with explicit boundaries
- **Gate-driven quality**: Stages separated by review gates; no skipping ahead

## Overview

Omni-Research is a skill set for general-purpose deep research, adapted from Prof. Jin's `agent-memory-survey` architecture. It transforms rigorous research methodology into reusable agent skills applicable to any topic.

### Core Capabilities

- **Broad input acceptance**: Web links, text snippets, GitHub projects, papers, videos, and more — all classified as raw materials
- **Full research lifecycle**: Not just information gathering — explore, develop, validate, and writeback
- **Dual output model**: Static documents (authoritative, evidence-bound) + living wiki (continuously updated)

## Research Philosophy

### Core Stance: `research ≠ information-gathering`

True deep research requires a complete lifecycle:

```
Collection → Definition → Evidence → Judgment → Decision → Validation → Writeback
```

Research outputs must be:

- **Traceable**: Every claim links to source, decision, or experiment
- **Evidence-bound**: Clear boundaries between "proven", "suggested", "inferred"
- **Reproducible**: Artifacts (code, data, configs) versioned alongside conclusions

### Evidence Hierarchy

Materials are classified by evidence strength:

| Tier | Type | Role | Storage |
|------|------|------|---------|
| 1 | Peer-reviewed papers | Primary research evidence | `raw/paper/` |
| 2 | Technical blogs | Engineering supplement | `raw/web/` |
| 3 | Deep-research reports | Leads only, not anchor evidence | `raw/deep-research/` |
| 4 | GitHub/projects | Implementation reference | `raw/github/` |
| 5 | AI models | Implementation reference | `raw/models/` |
| 6 | Benchmarks/datasets | Evaluation reference | `raw/datasets/` |

**Non-negotiable**: Never claim "paper proves X" when it only suggests.

## Repository Structure

```
omni-research/
├── docs/                  # Project documentation (this skill set only)
├── skills/                # Agentic skills source
│   ├── omr-*.md           # All skills prefixed with omr-
│   └── omr-methodology/   # Adapted from agent-memory-survey/docs/method
└── thirdparty/            # External references (not part of this project)
```

## Generated Workspace Structure

Each research project creates an isolated workspace:

```
<workspace>/<project-id>/
├── raw/                      # Raw material layer
│   ├── paper/                # Downloaded papers (PDF)
│   ├── web/                  # Blogs, URLs, screenshots
│   ├── github/               # Cloned repos
│   ├── models/               # AI model checkpoints, configs
│   ├── datasets/             # Benchmarks, data
│   └── deep-research/        # AI-generated research reports
│
├── docs/                     # Distilled knowledge layer
│   ├── survey/               # Broad survey chapters
│   ├── plans/                # Formal, traceable artifacts
│   │   ├── research-brief.md
│   │   ├── evidence-map.md
│   │   ├── architecture-decision.md
│   │   └── experiment-spec.md
│   ├── ideas/                # Subjective thinking, insights
│   ├── index/                # Machine-readable indexes
│   │   ├── papers-index.json
│   │   ├── papers-index.md
│   │   └── traceability-matrix.md
│   ├── archive/              # Archived materials
│   └── <topic-specific>/     # E.g., memory-eval, architecture
│
├── src/                      # Generated code projects
│   ├── prototype/            # Reference implementations
│   ├── evaluation/           # Validation experiments
│   └── tools/                # Project-specific utilities
│
├── wiki/                     # Living knowledge base
│   ├── README.md             # Auto-generated index
│   └── <concept>.md          # Interlinked concept pages
│
└── CLAUDE.md                 # Project context for AI agents
```

## Skill Set Design

### Core Skills (omr-*)

| Skill | Purpose | Trigger |
|-------|---------|---------|
| `omr-init` | Initialize new research project | `/omr-init <topic>` |
| `omr-ingest` | Classify and route raw materials | New material arrives |
| `omr-evidence` | Map paper to evidence matrix | Paper evaluation needed |
| `omr-brief` | Generate research-brief artifact | Start research stage |
| `omr-decision` | Create architecture-decision | Design choices needed |
| `omr-experiment` | Generate experiment-spec | Validation needed |
| `omr-evaluate` | Run evaluation, produce report | `make eval` |
| `omr-writeback` | Update survey/wiki from findings | Gate C passed |
| `omr-index` | Rebuild reference indexes | `make refs` |

### Methodology Skill

`omr-methodology` — Adapted from `agent-memory-survey/docs/method`:

| File | Purpose |
|------|---------|
| `workflow.md` | Pipeline definition |
| `gates.md` | Quality gate criteria (A, B, C) |
| `roles.md` | Research role definitions |
| `artifacts.md` | Standard artifact specifications |
| `traceability.md` | Cross-document tracking rules |
| `templates/` | Artifact templates |

## Research Pipeline

### Stage 1: Material Collection

- **Input**: Raw materials (paper, web, GitHub, models, datasets)
- **Output**: Classified materials in `raw/`, initial indexes in `docs/index/`
- **Skill**: `omr-ingest`

### Stage 2: Problem Definition

- **Input**: User intent + initial materials
- **Output**: `research-brief.md`
- **Required Fields**: `question_id`, `scope`, `non_goals`, `success_criteria`
- **Skill**: `omr-brief`

### Stage 3: Evidence Indexing

- **Input**: `research-brief` + materials
- **Output**: `evidence-map.md`, updated indexes
- **Process**: Papers → `omr-evidence` skill; Non-papers → calibration template
- **Skills**: `omr-evidence`, `omr-index`

### Stage 4: Research Judgment

- **Input**: `evidence-map`
- **Output**: Survey chapter drafts, judgment summaries
- **Process**: Distinguish paper evidence vs. engineering judgment vs. synthetic inference

### Stage 5: Architecture Decision

- **Input**: `research-brief` + `evidence-map` + judgments
- **Output**: `architecture-decision.md`
- **Gate**: Must pass **Gate A** before proceeding
- **Required Fields**: `decision_id`, `alternatives`, `risks`, `evidence_refs`

### Stage 6: Experiment Specification

- **Input**: `architecture-decision`
- **Output**: `experiment-spec.md`
- **Gate**: Must pass **Gate B** before implementation
- **Required Fields**: `experiment_id`, `hypothesis`, `metrics`, `ground_truth_strategy`

### Stage 7: Implementation & Evaluation

- **Input**: `experiment-spec`
- **Output**: Code in `src/`, `evaluation-report.md`, artifacts
- **Process**: Run evaluation, map results to hypotheses
- **Skill**: `omr-evaluate`

### Stage 8: Survey Writeback

- **Input**: `evaluation-report`
- **Output**: Updated `docs/survey/`, `wiki/`, `survey-update-note.md`
- **Gate**: Must pass **Gate C** before publishing
- **Skill**: `omr-writeback`

## Quality Gates

### Gate A: Before Implementation

**Required Artifacts**:
- `research-brief.md` — Clear question, scope, success criteria
- `evidence-map.md` — Primary/supporting evidence identified
- `architecture-decision.md` — Alternatives documented, risks stated

**Review Criteria**:
- [ ] Evidence supports decision direction
- [ ] Alternatives fairly considered
- [ ] Traceability IDs valid

### Gate B: Before Experiment

**Required Artifacts**:
- `experiment-spec.md` — Linked to `decision_id`
- Ground truth strategy defined (rule-derived preferred over human annotation / LLM-judge)

**Review Criteria**:
- [ ] Metrics answer research question
- [ ] Failure conditions explicit
- [ ] Reproducible evaluation design

### Gate C: Before Survey Update

**Required Artifacts**:
- `evaluation-report.md` — Results with traceability
- `survey-update-note.md` — Proposed changes with evidence refs

**Review Criteria**:
- [ ] Results traceable to hypotheses
- [ ] Evidence boundaries stated
- [ ] No over-claiming

## Traceability System

### Artifact IDs

All artifacts carry unique IDs:

- `question_id` — Research question identifier
- `decision_id` — Architecture decision identifier
- `experiment_id` — Evaluation experiment identifier

### Cross-Reference Format

```markdown
<!-- In survey chapter -->
This approach was validated in [EXP-001](../plans/experiment-spec.md#exp-001),
supporting Decision [DEC-005](../plans/architecture-decision.md#dec-005).

Evidence: [Paper X](../index/papers-index.md#paper-x) suggests... (not proves)
```

### Traceability Matrix

Auto-generated at `docs/index/traceability-matrix.md`:

| Question | Evidence | Decision | Experiment | Survey Section |
|----------|----------|----------|-------------|----------------|
| Q-001 | Paper A, B | DEC-003 | EXP-002 | §2.3 Formation |

## Dual Output Model

### Documents (Distilled Knowledge)

- **Survey**: Authoritative, evidence-bound chapters
- **Plans**: Formal artifacts (brief, evidence-map, decisions, specs)
- **Archive**: Historical versions, deprecated materials

### Wiki (Living Knowledge Base)

- **Concept pages**: Interlinked, continuously updated
- **Auto-sync**: Reflects latest survey + evaluation findings
- **Quick reference**: Condensed for rapid lookup

Wiki pages link back to source documents:

```markdown
> This concept is detailed in [Survey §3.2](../docs/survey/03-evolution.md#§3.2)
```

## Workflow Example

```bash
# 1. Initialize project
/omr-init "agent memory mechanisms"

# 2. Ingest materials
/omr-ingest https://arxiv.org/abs/2401.xxxxx  # → raw/paper/
/omr-ingest https://blog.example.com/post     # → raw/web/

# 3. Define research question
/omr-brief  # → docs/plans/research-brief.md

# 4. Index and map evidence
make refs                                  # → docs/index/papers-index.md
/omr-evidence raw/paper/xxx.pdf            # → evidence-map update

# 5. Make architecture decisions
/omr-decision                              # → docs/plans/architecture-decision.md
# Gate A review

# 6. Specify and run experiments
/omr-experiment                            # → docs/plans/experiment-spec.md
# Gate B review
make eval                                  # → src/evaluation/, docs/evaluation-report.md

# 7. Update knowledge base
/omr-writeback                             # → docs/survey/, wiki/
# Gate C review
```
