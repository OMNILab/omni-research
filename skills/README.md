# Skills Directory

**OmniResearch** — A suite of 9 AI agent skills for accelerating scientific innovation. Each skill is self-contained with its own assets, scripts, and SKILL.md specification. Shared infrastructure lives in `skills/shared/`.

---

## Skill Overview

| Skill | Version | Category | Phase | Description |
|-------|---------|----------|-------|-------------|
| omr-core | 1.0.0 | infrastructure | 1.0 | Foundation: contracts, dependency resolver, skill tree, patterns |
| omr-bootstrap | 1.0.0 | project-setup | 1.0 | Workspace creation + AGENTS.md generation |
| omr-collection | 1.1.0 | research-logistics | 2.1 | Material collection (papers, repos, web pages) |
| omr-analyze | 2.0.0 | evidence-analysis | 2.2–2.3 | Evidence extraction, judgment, research planning |
| omr-decision | 1.0.0 | architecture-decisions | 2.4 | Architecture decisions with alternatives & rationale |
| omr-evaluation | 1.0.0 | experiment-execution | 2.5 | Experiment design & prototype validation |
| omr-synthesis | 2.0.0 | findings-documentation | 3.1 | Findings writeback + living wiki generation |
| omr-idea-note | 1.0.0 | idea-capture | 3.3 | Speculative idea capture (Idea-First pattern) |
| omr-reconcile | 2.0.0 | state-management | 3.4 | Contradiction handling + state archiving |

**Merged skills (v2.0.0):** omr-evidence + omr-research-plan → **omr-analyze**; omr-synthesis + omr-wiki → **omr-synthesis**; omr-reconcile + omr-research-archive → **omr-reconcile**.

---

## Directory Layout

```
skills/
├── shared/                     # Shared infrastructure (used by all skills)
│   ├── contracts/              # 8 skill contract definitions (JSON)
│   ├── schemas/                # Contract schema validation
│   │   └── contract.schema.json
│   ├── tree/                   # Skill tree state tracking
│   ├── dependency_resolver.py  # Prerequisite checking
│   ├── detect_pattern.py       # Research pattern detection
│   ├── runtime_utils.py        # Shared runtime utilities
│   ├── skill_tree.py           # Tree visualization
│   ├── validate_contract.py    # Contract validation
│   └── test_e2e.py             # End-to-end tests
│
├── omr-core/                   # Foundation infrastructure (Phase 1.0)
│   ├── SKILL.md
│   ├── contracts/              # Canonical contract copies (8 JSON)
│   ├── patterns/               # 5 research pattern definitions
│   ├── schemas/                # Contract schema
│   ├── scripts/                # Infrastructure scripts
│   └── tree/                   # Skill tree state
│
├── omr-bootstrap/              # Workspace creation (Phase 1.0)
│   ├── SKILL.md
│   ├── assets/
│   │   └── AGENTS.md.template  # Project instructions template
│   └── scripts/
│       └── bootstrap_workspace.py
│
├── omr-collection/             # Material collection (Phase 2.1)
│   ├── SKILL.md
│   ├── handlers/               # 4 content handlers
│   ├── scripts/                # CLI, router, orchestrator, search
│   ├── utils/                  # Runtime utilities
│   └── tests/
│
├── omr-analyze/                 # Evidence + planning (Phase 2.2–2.3)
│   └── SKILL.md
│
├── omr-decision/               # Architecture decisions (Phase 2.4)
│   ├── SKILL.md
│   └── scripts/
│       └── make_decision.py
│
├── omr-evaluation/             # Experiment execution (Phase 2.5)
│   ├── SKILL.md
│   └── scripts/
│       └── run_evaluation.py
│
├── omr-synthesis/              # Findings + wiki (Phase 3.1)
│   ├── SKILL.md
│   └── scripts/
│       └── synthesize_findings.py
│
├── omr-idea-note/              # Idea capture (Phase 3.3)
│   ├── SKILL.md
│   └── scripts/
│       └── capture_idea.py
│
├── omr-reconcile/              # Reconciliation + archive (Phase 3.4)
│   ├── SKILL.md
│   └── scripts/
│       └── reconcile_evidence.py
│
├── patterns/                   # Symlink to omr-core/patterns
├── scripts/                    # Packaging & testing utilities
│   ├── package_all_skills.py
│   ├── simple_package_skill.py
│   └── test_marketplace_install.py
└── tree-state.json             # Symlink to omr-core/tree/tree-state.json
```

---

## Design Philosophy

### Modular Skill Structure

Each skill directory contains:
- **SKILL.md**: Skill specification, usage, and examples
- **scripts/**: Implementation scripts (CLI entry points, handlers, utilities)
- **assets/**: Templates and static resources (if applicable)
- **handlers/**: Skill-specific content handlers (if applicable)

**Benefits**:
- Skills are self-contained and independently packageable
- Easy to test individually
- Clear separation of concerns

### Shared Infrastructure

`skills/shared/` contains infrastructure used across all skills:
- **Contract definitions**: Artifact-bound dependencies for 8 skills
- **Contract schema**: JSON schema for validating contracts
- **Contract validation**: Script to validate all contracts
- **Dependency resolver**: Prerequisite checking before skill invocation
- **Skill tree state**: Tracks unlocked/ready/locked/completed skills
- **Pattern detection**: Identifies research pattern from collected materials
- **Runtime utilities**: Shared helper functions (canonical copy in `omr-core/scripts/`)

---

## Quality Gates

The research pipeline is governed by 4 quality gates:

| Gate | Location | Checks |
|------|----------|--------|
| **A** | omr-analyze (internal, after judgment before plan) | Evidence boundaries, judgment confidence |
| **B** | omr-decision (before evaluation) | Alternatives documented, risks identified |
| **C** | omr-evaluation (before synthesis) | Metrics defined, reproducibility ensured |
| **D** | omr-synthesis (before wiki generation) | Traceability complete, evidence boundaries enforced |

---

## Research Patterns

Five patterns define flexible entry points into the research pipeline:

| Pattern | Entry Point | Description |
|---------|-------------|-------------|
| Evidence-First | omr-collection | Collect materials, then analyze |
| Idea-First | omr-idea-note | Capture hypothesis, then validate |
| Decision-First | omr-decision | Start from architecture decision |
| Experiment-First | omr-evaluation | Begin with prototype experiment |
| Rapid-Prototype | omr-collection + omr-synthesis | Fast collect → synthesize loop |

Pattern definitions live in `skills/omr-core/patterns/` and `skills/patterns/`.

---

## Usage

### Contract Validation

```bash
python skills/shared/validate_contract.py
```

### Dependency Resolution

```bash
python skills/shared/dependency_resolver.py omr-analyze --check --workspace /path/to/project
```

### Skill Tree Visualization

```bash
python skills/shared/skill_tree.py            # Forward view
python skills/shared/skill_tree.py --reverse  # Reverse view
```

### Workspace Bootstrap

```bash
python skills/omr-bootstrap/scripts/bootstrap_workspace.py my-project "Research question?"
```

### Material Collection

```bash
python skills/omr-collection/scripts/cli.py "https://arxiv.org/abs/2402.12345" "agent memory"
python skills/omr-collection/handlers/paper_handler.py /path/to/project 2402.12345
python skills/omr-collection/handlers/github_handler.py /path/to/project anthropics/anthropic-sdk-python
```

### Marketplace Install Test

```bash
python skills/scripts/test_marketplace_install.py
```
