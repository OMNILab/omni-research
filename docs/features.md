# Features Design of Omni-Research Skills

## Overall Rules

- Follow agent skill spec strictly
- Leverage `skill-creator` skill primarily to manage skills
- Follow Claude skill marketplace patterns
- **Evidence-bound research**: All claims traceable to sources with explicit boundaries
- **Gate-driven quality**: Stages separated by review gates; no skipping ahead
- **Pattern-based composition**: Skills are composable ingredients; patterns are templates

## Overview

Omni-Research is a skill set for general-purpose deep research, adapted from Prof. Jin's `agent-memory-survey` architecture. It transforms rigorous research methodology into reusable agent skills applicable to any topic.

### Core Capabilities

- **Broad input acceptance**: Web links, text snippets, GitHub projects, papers, videos, and more — all classified as raw materials
- **Full research lifecycle**: Not just information gathering — explore, develop, validate, and writeback
- **Dual output model**: Static documents (authoritative, evidence-bound) + living wiki (continuously updated)
- **Pattern flexibility**: Multiple research patterns (Evidence-First, Idea-First, Decision-First, Experiment-First, Rapid-Prototype)
- **Configurable synthesis**: Survey, report, manuscript, or brief — output type defined by pattern

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
│   ├── omr-methodology/   # Adapted from agent-memory-survey/docs/method
│   └── patterns/          # Saved research patterns
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
│   ├── report/               # Structured findings (industry)
│   ├── manuscript/           # Publication-ready (academic)
│   ├── brief/                # Executive summaries (quick)
│   ├── plans/                # Formal, traceable artifacts
│   │   ├── research-brief.md
│   │   ├── evidence-map.md
│   │   ├── judgment-summary.md
│   │   ├── research-plan.md
│   │   ├── architecture-decision.md
│   │   ├── experiment-spec.md
│   │   └── evaluation-report.md
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

| Skill | Purpose | Stage |
|-------|---------|-------|
| `omr-bootstrap` | Initialize new research project | Init |
| `omr-collection` | Collect and classify raw materials | Collection |
| `omr-evidence` | Map materials to evidence matrix | Definition + Evidence |
| `omr-research-plan` | Judge evidence and plan research | Judgment + Planning |
| `omr-decision` | Create architecture-decision | Decision |
| `omr-evaluation` | Run evaluation, produce report | Validation |
| `omr-synthesis` | Write up findings (configurable output) | Writeback |
| `omr-wiki` | Generate living knowledge base | Writeback |
| `omr-reconcile` | Reconcile state when evidence changes | Iteration |
| `omr-idea-note` | Capture speculative thoughts | Any |
| `omr-research-archive` | Snapshot current progress | Lifecycle |

**Total: 12 skills** (11 core + configurable synthesis)

### omr-synthesis: Configurable Output Modes

| Mode | Output | Best For |
|------|--------|----------|
| `survey` | `docs/survey/` (chapters) | Academic research, literature reviews |
| `report` | `docs/report/` (structured findings) | Industry research, stakeholder deliverables |
| `manuscript` | `docs/manuscript/` (publication-ready) | Academic papers, conference submissions |
| `brief` | `docs/brief/` (executive summary) | Quick findings, time-boxed research |

Mode determined by pattern config (default) or user override (`--mode` flag).

### Skill Contracts

Each skill has an explicit contract:

```yaml
skill: omr-decision
requires:
  - artifact: evidence-map.md
    optional: false
  - artifact: judgment-summary.md
    optional: true
produces:
  - artifact: architecture-decision.md
gates:
  - id: gate_b
    checks:
      - "Alternatives documented"
      - "Risks stated"
      - "Evidence refs valid"
    enforcement: "user-confirm"  # or "auto-pass" for agents
```

### Detailed Skill Capabilities

---

#### omr-bootstrap

**Purpose:** Initialize a new research project workspace.

**Trigger:** `/omr-bootstrap "<topic>"`

**Inputs:**
- `<topic>` (required): Research topic string

**Outputs:**
- Workspace structure: `raw/`, `docs/`, `src/`, `wiki/`
- `CLAUDE.md` with project context
- `docs/index/.gitkeep` (empty index placeholders)

**Metadata:**
```yaml
---
id: PROJ-001
type: project
topic: "agent memory mechanisms"
created_at: 2026-04-11T10:30:00Z
pattern_detected: null
workspace: ./agent-memory-mechanisms/
---
```

**Behavior:**
1. Create workspace directory structure
2. Generate `CLAUDE.md` with topic context
3. Initialize empty index files
4. Display skill tree (all skills locked except collection, idea-note)
5. Prompt: "What's your first action?"

**Gates:** None

**Can call:** None

**Pattern detection:** None (pattern emerges from subsequent actions)

**Example:**
```
User: /omr-bootstrap "agent memory mechanisms"
System: ✓ Workspace created at ./agent-memory-mechanisms/
        What's your first action?
        [1] I have papers to collect
        [2] I have an idea to explore
        ...
```

---

#### omr-collection

**Purpose:** Download, classify, and index raw materials.

**Trigger:** `/omr-collection <materials>` or automatic after material ingest

**Inputs:**
- Materials (required): URLs, file paths, or direct content
- `CLAUDE.md` (implicit): Project context

**Outputs:**
- Classified materials in `raw/paper/`, `raw/web/`, `raw/github/`, `raw/models/`, `raw/datasets/`, `raw/deep-research/`
- `docs/index/papers-index.json` + `.md`
- `docs/index/blogs-index.json` + `.md`
- `docs/index/github-index.json` + `.md`

**Metadata:**
```yaml
---
id: COL-001
type: collection
sources_count: 15
papers: 10
blogs: 3
github: 2
classification_timestamp: 2026-04-11T11:00:00Z
---
```

**Behavior:**
1. Accept materials (URLs, paths, content)
2. Classify by tier (paper/blog/github/model/dataset/deep-research)
3. Download papers (arXiv, OpenReview)
4. Clone GitHub repos
5. Extract metadata (title, authors, date, abstract)
6. Generate indexes (JSON + markdown)
7. Update skill tree: unlock `omr-evidence`
8. Trigger pattern detection after 3+ sources

**Gates:** None

**Can call:** `omr-reconcile` (if new material contradicts existing evidence)

**Edge cases:**
- URL inaccessible: Warn user, skip, continue
- Classification ambiguous: Ask user: "Is this a paper or blog?"
- Duplicate material: Skip, warn user

**Example:**
```
User: /omr-collection https://arxiv.org/abs/2401.12345
System: ✓ Downloaded: arxiv-2401.12345.pdf → raw/paper/
        ✓ Indexed: docs/index/papers-index.json
        Papers indexed: 5

        Pattern emerging: Evidence-First (detected)
        Save pattern? [y/N]
```

---

#### omr-evidence

**Purpose:** Define research question and map evidence landscape.

**Trigger:** `/omr-evidence`

**Inputs:**
- Materials in `raw/` (required)
- `docs/index/*` (implicit): Material indexes

**Outputs:**
- `docs/plans/brief-{id}.md` — Research brief
- `docs/plans/evidence-{id}.md` — Evidence map

**Metadata (research-brief):**
```yaml
---
id: Q-001
type: research-brief
version: 1.0.0
question: "How do AI agents maintain long-term memory?"
scope: "Lifecycle mechanisms for agent memory"
non_goals: ["Retrieval optimization only"]
success_criteria: ["Identify formation patterns", "Map evolution strategies"]
created_at: 2026-04-11T11:30:00Z
status: draft
dependencies: [COL-001]
---
```

**Metadata (evidence-map):**
```yaml
---
id: Q-001
type: evidence-map
version: 1.0.0
primary_evidence: [P-001, P-002, P-003]
supporting_evidence: [B-001, B-002]
open_gaps: ["No longitudinal studies", "Evaluation methodology unclear"]
papers_analyzed: 10
blogs_analyzed: 3
created_at: 2026-04-11T11:30:00Z
status: draft
dependencies: [COL-001]
---
```

**Behavior:**
1. Scan `raw/paper/` for PDFs
2. Scan `raw/web/` for blogs
3. Extract key findings per material
4. Generate research brief: question, scope, non-goals, success criteria
5. Generate evidence map: primary evidence, supporting evidence, gaps
6. Update skill tree: unlock `omr-research-plan`

**Gates:** None (Gate A is on `omr-research-plan`)

**Can call:** None

**Prerequisite check:**
- If `raw/` empty: "No materials found. Run `/omr-collection` first."

**Example:**
```
User: /omr-evidence
System: ✓ Analyzing 10 papers, 3 blogs...

        Research Question: "How do AI agents maintain long-term memory?"
        Scope: Lifecycle mechanisms (formation, evolution, retrieval)

        Primary Evidence:
        - P-001: Vector + graph fusion improves retrieval
        - P-002: Memory lifecycle underexplored

        Open Gaps:
        - No longitudinal studies on memory evolution

        ✓ Generated: brief-Q-001.md, evidence-Q-001.md
        📊 Skill tree: omr-research-plan [READY]
```

---

#### omr-research-plan

**Purpose:** Synthesize judgment from evidence and plan research execution.

**Trigger:** `/omr-research-plan`

**Inputs:**
- `evidence-{id}.md` (required)
- `brief-{id}.md` (implicit): Research context

**Outputs:**
- `docs/plans/judgment-{id}.md` — Judgment summary
- `docs/plans/plan-{id}.md` — Research plan

**Metadata (judgment-summary):**
```yaml
---
id: J-001
type: judgment-summary
version: 1.0.0
question_id: Q-001
main_conclusion: "Current research focuses on retrieval, neglects lifecycle"
confidence: medium
contradictions: []
evidence_weight: strong
created_at: 2026-04-11T12:00:00Z
status: draft
dependencies: [Q-001]
gate_a_passed: null
---
```

**Metadata (research-plan):**
```yaml
---
id: Q-001
type: research-plan
version: 1.0.0
priorities:
  - 1: "Design memory lifecycle model"
  - 2: "Implement formation + evolution"
  - 3: "Evaluate against benchmarks"
timeline_estimated: "3-5 days"
resource_allocation: "2 parallel tracks"
created_at: 2026-04-11T12:00:00Z
status: draft
dependencies: [J-001]
gate_a_passed: null
---
```

**Behavior:**
1. Read evidence-map
2. Synthesize judgment: main conclusion, confidence, contradictions
3. Generate plan: priorities, timeline, resource allocation
4. Present Gate A review
5. If gate passed: update skill tree, unlock `omr-decision`

**Gates:** Gate A (Evidence sufficient for planning?)

**Gate A checks:**
- [ ] Evidence coverage adequate
- [ ] Research question clear
- [ ] Scope defined
- [ ] Judgment confidence reasonable

**Can call:** None

**Gate failure handling:**
- If Gate A fails: "Evidence insufficient. Add more materials via `/omr-collection` or revise scope."

**Example:**
```
User: /omr-research-plan
System: ✓ Judgment: "Current research neglects lifecycle" (medium confidence)
        ✓ Plan: Design lifecycle model (Priority 1), 3-5 days

        ⚠️  GATE A: Before Planning
        Review criteria:
        [✓] Evidence coverage adequate
        [✓] Research question clear
        [✓] Scope defined

        Proceed with plan? [Y/n]

User: Y
System: ✓ Gate A passed
        📊 Skill tree: omr-decision [READY]
```

---

#### omr-decision

**Purpose:** Make an architectural decision with alternatives and rationale.

**Trigger:** `/omr-decision`

**Inputs:**
- `evidence-{id}.md` (required)
- `judgment-{id}.md` (optional)
- `plan-{id}.md` (implicit): Research context

**Outputs:**
- `docs/plans/decision-{id}.md` — Architecture decision

**Metadata:**
```yaml
---
id: DEC-001
type: architecture-decision
version: 1.0.0
question_id: Q-001
alternatives:
  - id: A
    description: "Vector-only memory"
    selected: false
    reason: "Baseline, validated in P-001"
  - id: C
    description: "Hybrid fusion with lifecycle stages"
    selected: true
    reason: "Addresses gap identified in J-001"
risks:
  - "Higher complexity than baseline"
  - "No direct precedent for lifecycle model"
  - "May require custom evaluation"
evidence_refs: [P-001, P-002, J-001]
created_at: 2026-04-11T14:00:00Z
status: draft
dependencies: [Q-001, J-001]
gate_b_passed: null
---
```

**Behavior:**
1. Read evidence-map + judgment-summary (if available)
2. Propose alternatives (at least 3)
3. Select best alternative based on evidence + judgment
4. Document risks and rationale
5. Link evidence references (traceability)
6. Present Gate B review
7. If gate passed: update skill tree, unlock `omr-evaluation`

**Gates:** Gate B (Architecture decision sound?)

**Gate B checks:**
- [ ] Alternatives documented (≥3)
- [ ] Risks stated
- [ ] Evidence refs valid
- [ ] Selection rationale clear

**Can call:** None

**Prerequisite check:**
- If `evidence-map.md` missing: "Missing evidence. Run `/omr-evidence` first."

**Example:**
```
User: /omr-decision
System: ✓ Alternatives:
        A. Vector-only (baseline)
        B. Graph-only (P-002 suggests)
        C. Hybrid fusion with lifecycle (novel)

        Selected: C (addresses gap)

        Risks: Higher complexity, no precedent

        ⚠️  GATE B: Before Implementation
        Review criteria:
        [✓] Alternatives documented: 3
        [✓] Risks stated
        [✓] Evidence refs valid

        Proceed with decision? [Y/n/modify]
```

---

#### omr-evaluation

**Purpose:** Design and run evaluation to validate decision.

**Trigger:** `/omr-evaluation`

**Inputs:**
- `decision-{id}.md` (required)
- `plan-{id}.md` (implicit): Research context

**Outputs:**
- `docs/plans/spec-{id}.md` — Experiment specification
- `docs/plans/report-{id}.md` — Evaluation report
- `src/prototype/` — Prototype code
- `src/evaluation/` — Test code

**Metadata (experiment-spec):**
```yaml
---
id: EXP-001
type: experiment-spec
version: 1.0.0
decision_id: DEC-001
hypothesis: "Hybrid fusion improves long-term retention"
metrics:
  - name: retention_7day
    type: accuracy
    baseline: 0.72
    target: 0.80
  - name: latency_avg
    type: milliseconds
    baseline: 50
    target: 100
ground_truth_strategy: rule-derived
failure_conditions:
  - "Retention < baseline at any interval"
  - "Latency > 2x baseline"
created_at: 2026-04-11T15:00:00Z
status: draft
dependencies: [DEC-001]
gate_c_passed: null
---
```

**Metadata (evaluation-report):**
```yaml
---
id: EXP-001
type: evaluation-report
version: 1.0.0
decision_id: DEC-001
hypothesis_supported: true
metrics_results:
  - name: retention_7day
    baseline: 0.72
    result: 0.84
    improvement: "+16.7%"
    target_met: true
  - name: latency_avg
    baseline: 50
    result: 55
    improvement: "+10%"
    target_met: true
ground_truth: rule-derived
confidence: high
recommendations: ["Proceed to synthesis"]
created_at: 2026-04-11T16:00:00Z
status: draft
dependencies: [EXP-001-spec]
gate_c_passed: null
---
```

**Behavior:**
1. Read architecture-decision
2. Generate experiment spec: hypothesis, metrics, ground truth, failure conditions
3. Present Gate C review for spec
4. If gate passed: implement prototype in `src/prototype/`
5. Write tests in `src/evaluation/`
6. Run tests, collect metrics
7. Generate evaluation report with results
8. Map results to hypothesis
9. Update skill tree: unlock `omr-synthesis`

**Gates:** Gate C (Experiment design valid?)

**Gate C checks:**
- [ ] Metrics answer research question
- [ ] Failure conditions explicit
- [ ] Ground truth strategy defined
- [ ] Reproducible evaluation design

**Can call:** `omr-synthesis`, `omr-wiki` (auto-trigger on success)

**Contract overrides:**
- Experiment-First pattern: allows `omr-evaluation` without prior `decision-{id}.md`

**Ground truth strategies:**
- **rule-derived** (preferred): No human annotation, deterministic rules
- **benchmark-derived**: Use existing benchmark datasets
- **simulation-derived**: Generate synthetic scenarios

**Example:**
```
User: /omr-evaluation
System: ✓ Spec: Test hybrid fusion vs. vector-only
        Hypothesis: Improves 7-day retention by 10%
        Metrics: retention_7day, latency_avg
        Ground truth: rule-derived

        ⚠️  GATE C: Before Experiment
        Review criteria:
        [✓] Metrics answer question
        [✓] Failure conditions explicit
        [✓] Reproducible

        Proceed with implementation? [Y/n]

User: Y
System: ✓ Implementing prototype in src/prototype/
        ✓ Writing tests in src/evaluation/
        ✓ Running 15 scenarios...

        Results:
        - Retention: 84% (baseline 72%, +16.7%)
        - Latency: 55ms (baseline 50ms, +10%)

        Hypothesis: Supported ✓

        ✓ Generated: spec-EXP-001.md, report-EXP-001.md
        📊 Skill tree: omr-synthesis [READY]
```

---

#### omr-synthesis

**Purpose:** Write authoritative findings in configurable output format.

**Trigger:** `/omr-synthesis [--mode <mode>]`

**Inputs:**
- `report-{id}.md` OR `judgment-{id}.md` (required)
- `decision-{id}.md` (implicit): Decision context
- Pattern config (implicit): Default synthesis mode

**Outputs:**
- Mode-dependent:
  - `survey`: `docs/survey/*.md` (chapters)
  - `report`: `docs/report/*.md` (structured findings)
  - `manuscript`: `docs/manuscript/*.md` (publication-ready)
  - `brief`: `docs/brief/*.md` (executive summary)

**Metadata:**
```yaml
---
id: SYN-001
type: synthesis
version: 1.0.0
mode: survey                      # survey | report | manuscript | brief
question_id: Q-001
decision_ids: [DEC-001]
experiment_ids: [EXP-001]
chapters:
  - title: "Framework"
    file: "01-framework.md"
  - title: "Formation"
    file: "02-formation.md"
  - title: "Evolution"
    file: "03-evolution.md"
created_at: 2026-04-11T17:00:00Z
status: draft
dependencies: [EXP-001, DEC-001]
gate_d_passed: null
---
```

**Behavior:**
1. Read evaluation-report + architecture-decision + evidence-map
2. Determine mode (pattern config or `--mode` flag)
3. Generate chapters/sections based on mode
4. Ensure traceability: link every claim to evidence/decision/experiment
5. Apply evidence boundaries: distinguish "proven", "suggested", "inferred"
6. Present Gate D review
7. If gate passed: update skill tree, unlock `omr-wiki`

**Gates:** Gate D (Results traceable, no over-claiming?)

**Gate D checks:**
- [ ] Results traceable to hypotheses
- [ ] Evidence boundaries stated
- [ ] No over-claiming ("paper proves" vs "suggests")
- [ ] Cross-references valid

**Can call:** `omr-wiki` (auto-trigger after gate passed)

**Mode differences:**

| Mode | Structure | Depth | Evidence Boundaries |
|------|-----------|-------|---------------------|
| `survey` | Chapters (01-07) | Comprehensive | Explicit per section |
| `report` | Structured findings | Medium | Key findings only |
| `manuscript` | Paper format | Deep | Academic rigor |
| `brief` | Executive summary | Minimal | Top-level only |

**Example:**
```
User: /omr-synthesis
System: ✓ Mode: survey (pattern default: Evidence-First)
        ✓ Generating chapters: Framework, Formation, Evolution, Retrieval

        Chapter 2.3: "Memory Formation"
        Evidence: P-001 validates importance threshold
        Decision: DEC-001 selects hybrid fusion
        Experiment: EXP-001 shows +16.7% retention

        ⚠️  GATE D: Before Publish
        Review criteria:
        [✓] Results traceable
        [✓] Evidence boundaries stated
        [✓] No over-claiming

        Publish synthesis? [Y/n]

User: Y
System: ✓ Gate D passed
        ✓ Generated: docs/survey/01-framework.md, ...
        📊 Skill tree: omr-wiki [READY]
```

---

#### omr-wiki

**Purpose:** Generate living knowledge base from synthesis findings.

**Trigger:** `/omr-wiki`

**Inputs:**
- Synthesis chapters OR judgment-summary (required)

**Outputs:**
- `wiki/*.md` — Concept pages with interlinks
- `wiki/README.md` — Auto-generated index

**Metadata (per wiki page):**
```yaml
---
id: WIKI-001
type: wiki-page
concept: "Memory Lifecycle"
source_chapters:
  - survey/02-formation.md
  - survey/03-evolution.md
source_decisions: [DEC-001]
last_synced: 2026-04-11T18:00:00Z
status: published
---
```

**Behavior:**
1. Read synthesis chapters
2. Extract key concepts
3. Generate wiki pages per concept
4. Create interlinks between concepts
5. Link back to source documents
6. Generate `wiki/README.md` index

**Gates:** None

**Can call:** None

**Wiki page structure:**
```markdown
# Memory Lifecycle

> Detailed in [Survey §2.3](../docs/survey/02-formation.md#§2.3)

## Definition
...

## Key Mechanisms
- Formation: [see Memory Formation](./memory-formation.md)
- Evolution: [see Memory Evolution](./memory-evolution.md)

## Evidence
- Supported by [EXP-001](../docs/plans/report-EXP-001.md)
```

**Example:**
```
User: /omr-wiki
System: ✓ Extracting concepts: Memory Lifecycle, Vector-Graph Fusion, ...
        ✓ Generating wiki pages with interlinks

        Wiki pages:
        - Memory-Lifecycle.md (links to Formation, Evolution)
        - Vector-Graph-Fusion.md (links to Retrieval)
        - Memory-Evaluation.md (links to Benchmarks)

        ✓ Generated: wiki/*.md
        📊 Skill tree: Complete ✓
```

---

#### omr-reconcile

**Purpose:** Update research state when new evidence contradicts existing artifacts.

**Trigger:** `/omr-reconcile` OR automatic after new material collection

**Inputs:**
- At least one existing artifact (required)
- New evidence or gate failure (triggering event)

**Outputs:**
- Updated artifacts (affected downstream)
- `docs/archive/*-v{old-version}.md` — Archived superseded versions
- `docs/index/versions/{id}-history.json` — Version history update

**Metadata (reconciliation state):**
```yaml
---
id: REC-001
type: reconciliation
trigger: new_evidence
trigger_artifact: P-005
affected_artifacts:
  - DEC-001 (contradicted)
  - EXP-001 (needs re-run)
reconciliation_actions:
  - re_evaluate_evidence
  - update_judgment
  - re_decide
completed_at: 2026-04-11T16:45:00Z
archived_versions:
  - decision-DEC-001-v1.0.0.md
---
```

**Behavior:**
1. Detect trigger (new evidence, gate failure, manual)
2. Analyze impact: which artifacts affected
3. Show blast radius: dependency chain
4. Propose reconciliation options:
   - [1] Re-evaluate → update affected artifacts
   - [2] Accept contradiction → document in survey
   - [3] Fork parallel research thread
5. If user approves:
   - Call affected skills in order
   - Archive old versions
   - Update version history
6. Maintain traceability through reconciliation

**Gates:** None

**Can call:** `omr-evidence`, `omr-research-plan`, `omr-decision`, `omr-evaluation` (as needed)

**Blast radius analysis:**
```
New paper P-005 contradicts DEC-001
    ↓
Affected: DEC-001 → EXP-001 → SYN-001
    ↓
DEC-001 needs Gate B re-review
EXP-001 needs re-run
SYN-001 needs update
```

**Example:**
```
User: /omr-collection https://arxiv.org/abs/2402.99999
System: ✓ New paper P-005: Graph-only outperforms fusion
        ⚠️  Contradicts Decision DEC-001

        Impact analysis:
        - DEC-001: ⚠️ Contradicted
        - EXP-001: ⚠️ Tests hybrid (may be suboptimal)
        - SYN-001: Not yet published (safe)

        Reconciliation options:
        [1] Re-evaluate → Update decision → Re-run experiment
        [2] Accept contradiction → Document as "debated approach"
        [3] Fork parallel thread (Idea-First for graph-only)

User: [1]
System: ✓ Re-evaluating evidence (calling omr-evidence)...
        ✓ Updating judgment...
        ⚠️  Gate B: Decision needs revision

        DEC-001 (v2.0.0):
        - Alternatives: Add graph-only as co-equal
        - Risks: Add "comparative study needed"

        Approve? [Y/n]

User: Y
System: ✓ Archived: decision-DEC-001-v1.0.0.md
        ✓ Updated: decision-DEC-001-v2.0.0.md
        ✓ Version history: docs/index/versions/DEC-001-history.json
        📊 Skill tree: omr-evaluation [READY: re-run]
```

---

#### omr-idea-note

**Purpose:** Capture speculative thoughts and creative insights.

**Trigger:** `/omr-idea-note "<insight>"`

**Inputs:**
- `<insight>` (required): Text content or structured insight

**Outputs:**
- `docs/ideas/idea-{timestamp}-{slug}.md` — Idea note

**Metadata:**
```yaml
---
id: IDEA-001
type: idea-note
timestamp: 20260411T103000
slug: quantum-memory-superposition
insight: "What if agent memory behaves like quantum superposition?"
tags: [speculative, physics-inspired]
linked_decisions: []
linked_experiments: []
created_at: 2026-04-11T10:30:00Z
status: draft
---
```

**Behavior:**
1. Accept insight text
2. Generate slug from content
3. Store timestamped note
4. No dependency tracking (standalone)
5. Can be linked to decisions/experiments later

**Gates:** None

**Can call:** None (standalone skill)

**Can be called by:** Any skill (anytime)

**Use cases:**
- Capture speculative thoughts outside formal pipeline
- Note hypotheses before decision
- Record insights during evaluation

**Example:**
```
User: /omr-idea-note "What if memory works like quantum superposition — holding multiple states simultaneously?"

System: ✓ Generated: docs/ideas/idea-20260411T103000-quantum-memory-superposition.md

        Idea captured. Use `/omr-decision` to formalize.
```

---

#### omr-research-archive

**Purpose:** Snapshot current research state for preservation or rollback.

**Trigger:** `/omr-research-archive` OR automatic during reconciliation

**Inputs:**
- At least one existing artifact (required)
- Archive reason (optional)

**Outputs:**
- `docs/archive/{timestamp}/` — Archived snapshot
- `docs/archive/index.json` — Archive index

**Metadata (archive snapshot):**
```yaml
---
id: ARCH-001
type: archive
snapshot_timestamp: 2026-04-11T16:30:00Z
reason: "User-initiated before risky pivot"
artifacts_archived:
  - brief-Q-001.md
  - evidence-Q-001.md
  - decision-DEC-001.md
  - report-EXP-001.md
archive_path: docs/archive/20260411T163000/
---
```

**Behavior:**
1. Collect current artifacts
2. Copy to timestamped archive folder
3. Generate archive index
4. Preserve version metadata
5. Mark artifacts as archived in main index

**Gates:** None

**Can call:** None

**Automatic triggers:**
- When `omr-reconcile` supersedes artifacts
- Before Gate D (optional safety snapshot)
- User manual request

**Use cases:**
- Preserve state before risky pivot
- Create rollback point
- Historical record for audit

**Example:**
```
User: /omr-research-archive
System: ✓ Archiving current state...

        Archived:
        - brief-Q-001.md → docs/archive/20260411T163000/brief-Q-001.md
        - decision-DEC-001.md → docs/archive/20260411T163000/decision-DEC-001.md
        - report-EXP-001.md → docs/archive/20260411T163000/report-EXP-001.md

        Archive index: docs/archive/index.json
        Snapshot saved. You can rollback if needed.
```

### Methodology Skill

`omr-methodology` — Adapted from `agent-memory-survey/docs/method`:

| File | Purpose |
|------|---------|
| `workflow.md` | Pipeline definition |
| `gates.md` | Quality gate criteria (A, B, C, D) |
| `roles.md` | Research role definitions |
| `artifacts.md` | Standard artifact specifications |
| `traceability.md` | Cross-document tracking rules |
| `templates/` | Artifact templates |

## Research Patterns

### What Are Patterns?

A **pattern** is a named sequence of skill invocations that satisfies a research goal. Patterns emerge from practice and are saved as reusable templates.

**Patterns are NOT rigid pipelines** — they're recipes. Skills can be invoked freely; patterns record successful paths.

### Pattern Library

#### Evidence-First
Rigorous research starting from literature collection.
```
omr-collection → omr-evidence → omr-research-plan → omr-decision → omr-evaluation → omr-synthesis → omr-wiki
```
Gates: A, B, C, D
Synthesis mode: survey
Best for: Academic research, literature surveys

#### Idea-First
Speculative research starting from creative insight.
```
omr-idea-note → omr-decision → omr-evaluation → omr-evidence → omr-synthesis → omr-wiki
```
Gates: D only
Synthesis mode: brief
Best for: Exploratory research, speculative work

#### Decision-First
Hypothesis-driven research starting from an architectural stance.
```
omr-decision → omr-evidence → omr-research-plan → omr-evaluation → omr-synthesis → omr-wiki
```
Gates: C, D
Synthesis mode: report
Best for: Engineering research, prototype-driven investigation

#### Experiment-First
Empirical research starting from building and testing.
```
omr-evaluation → omr-evidence → omr-decision → omr-synthesis → omr-wiki
```
Gates: D only
Synthesis mode: brief
Best for: Quick validation, proof-of-concept, empirical testing

#### Rapid-Prototype
Fastest path to a working output.
```
omr-evaluation → omr-evidence → omr-decision → omr-synthesis
```
Gates: none
Synthesis mode: brief
Best for: Hackathons, proof-of-concept, time-boxed exploration

### Pattern Emergence

1. **Bootstrap** → Workspace created, no pattern forced
2. **First action** → User selects first skill
3. **Pattern detection** → After 3+ invocations, system proposes pattern name
4. **Pattern save** → User accepts/rejects saving as reusable template
5. **Template library** → Saved patterns stored in `skills/patterns/`

### Pattern Selection Timing

Patterns are detected **after first action**, not forced at bootstrap. This provides guidance without forced commitment.

## Quality Gates

### Gate A: Before Research Planning

**Position**: Before `omr-research-plan`
**Purpose**: Evidence sufficient for planning?

**Required Artifacts**:
- `research-brief.md` — Clear question, scope
- `evidence-map.md` — Evidence landscape mapped

**Review Criteria**:
- [ ] Evidence coverage adequate
- [ ] Research question clear
- [ ] Scope defined

### Gate B: Before Architecture Decision

**Position**: Before `omr-decision`
**Purpose**: Architecture decision sound?

**Required Artifacts**:
- `research-brief.md`
- `evidence-map.md`
- `judgment-summary.md` (optional)

**Review Criteria**:
- [ ] Alternatives documented
- [ ] Risks stated
- [ ] Evidence refs valid

### Gate C: Before Evaluation

**Position**: Before `omr-evaluation`
**Purpose**: Experiment design valid?

**Required Artifacts**:
- `architecture-decision.md`

**Review Criteria**:
- [ ] Metrics answer research question
- [ ] Failure conditions explicit
- [ ] Reproducible evaluation design

### Gate D: Before Synthesis

**Position**: Before `omr-synthesis`
**Purpose**: Results traceable, no over-claiming?

**Required Artifacts**:
- `evaluation-report.md` OR `judgment-summary.md`

**Review Criteria**:
- [ ] Results traceable to hypotheses
- [ ] Evidence boundaries stated
- [ ] No over-claiming

### Gate Enforcement

- **Semi-automated mode** (default): User confirms at each gate
- **Fully-automated mode** (agents): Gates auto-pass
- **Configurable**: Set per pattern or project

## Skill Tree: Progress Visualization

### Game-Inspired Progress Model

```
omr-bootstrap ✓
    │
    ├── omr-collection ✓  (papers downloaded)
    │       │
    │       ├── omr-evidence ○  (ready to run)
    │       │       │
    │       │       └── omr-research-plan ●  (locked: needs evidence-map.md)
    │       │
    │       └── omr-idea-note ✓  (can run anytime)
    │
    └── omr-reconcile ✓  (can run anytime)
```

**Legend:**
- ✓ = complete
- ○ = ready to run
- ● = locked (needs prerequisites)

### Dual View Mode

**Forward view**: "What can I do next?" — Explore possibilities
**Reverse view**: "I want to produce X. What skills do I need?" — Goal-driven planning

Toggle between perspectives anytime.

## Reconciliation: Research Iteration

### When Reconciliation Triggers

| Trigger | Source | Action |
|---------|--------|--------|
| New paper arrives | `omr-collection` | Auto-flag: "Reconcile?" |
| Evidence map updated | `omr-evidence` | Check affected decisions |
| Gate failure | Gate A/B/C/D | Prompt: "Reconcile state?" |
| Manual request | User command | `/omr-reconcile` |

### How Reconciliation Works

```
New evidence detected
    ↓
omr-reconcile analyzes impact
    ↓
Flags affected artifacts
    ↓
Offers: "Re-evaluate? (will update decision, re-test experiment)"
    ↓
User approves
    ↓
System updates all dependent artifacts
    ↓
Old versions archived automatically
```

### Archiving Behavior

- **Automatic**: When `omr-reconcile` supersedes artifacts
- **Manual**: User triggers `/omr-research-archive` for snapshot
- **Location**: `docs/archive/` with timestamp

## Traceability System

### Artifact IDs

All artifacts carry unique IDs:

- `question_id` — Research question identifier (e.g., Q-001)
- `decision_id` — Architecture decision identifier (e.g., DEC-001)
- `experiment_id` — Evaluation experiment identifier (e.g., EXP-001)

### Artifact Metadata System

Every artifact includes standardized YAML frontmatter for consistency, version control, and traceability.

#### Standard Metadata Header

```yaml
---
# Identity
id: Q-001                          # Unique artifact ID
type: research-brief               # Artifact type
version: 1.0.0                     # Semantic versioning

# Provenance
created_at: 2026-04-11T10:30:00Z
updated_at: 2026-04-11T10:30:00Z
created_by: user                   # user | agent-name
status: draft                      # draft | reviewed | published | archived

# Lineage
pattern: evidence-first            # Pattern name (if any)
stage: definition                  # Research stage
dependencies: []                   # IDs of artifacts this depends on
dependents: []                     # IDs of artifacts that depend on this

# Quality
gates_passed: []                   # List of gates passed
review_notes: []                   # Review comments

# Traceability
traceability_refs: []              # Cross-references to other artifacts
---
```

#### File Naming Convention

**Pattern:** `{type}-{id}-v{major}.{minor}.{patch}.md`

| Artifact Type | Filename Pattern | Example |
|---------------|------------------|---------|
| research-brief | `brief-{id}-v{version}.md` | `brief-Q-001-v1.0.0.md` |
| evidence-map | `evidence-{id}-v{version}.md` | `evidence-Q-001-v1.0.0.md` |
| judgment-summary | `judgment-{id}-v{version}.md` | `judgment-Q-001-v1.0.0.md` |
| research-plan | `plan-{id}-v{version}.md` | `plan-Q-001-v1.0.0.md` |
| architecture-decision | `decision-{id}-v{version}.md` | `decision-DEC-001-v1.0.0.md` |
| experiment-spec | `spec-{id}-v{version}.md` | `spec-EXP-001-v1.0.0.md` |
| evaluation-report | `report-{id}-v{version}.md` | `report-EXP-001-v1.0.0.md` |
| synthesis | `synthesis-{id}-v{version}.md` | `synthesis-Q-001-v1.0.0.md` |
| idea-note | `idea-{timestamp}-{slug}.md` | `idea-20260411T103000-quantum-memory.md` |

**Version suffix optional for current version:**
- `decision-DEC-001.md` = current version (symlink or copy)
- `decision-DEC-001-v1.0.0.md` = specific version (archived)

#### Versioning Rules

**Semantic Versioning (MAJOR.MINOR.PATCH):**

| Change Type | Version Increment | Example |
|-------------|-------------------|---------|
| Breaking change (invalidates downstream) | MAJOR | 1.0.0 → 2.0.0 |
| Additive change (new fields, compatible) | MINOR | 1.0.0 → 1.1.0 |
| Bug fix, typo, formatting | PATCH | 1.0.0 → 1.0.1 |

**Version lifecycle:**

```
draft (v0.1.0) 
    → reviewed (v1.0.0)
    → published (v1.0.0)
    → superseded (v1.0.0 archived, v2.0.0 created)
```

#### Status Workflow

```
draft → reviewed → published → archived
  ↓        ↓          ↓
  └────────┴──────────┴→ superseded
```

| Status | Meaning | Can Edit? |
|--------|---------|-----------|
| `draft` | Work in progress | Yes |
| `reviewed` | Passed gate review | No (fork to edit) |
| `published` | Final, traceable | No (only supersede) |
| `archived` | Historical record | No (read-only) |
| `superseded` | Replaced by newer version | No (pointer to current) |

#### Artifact-Specific Metadata

**architecture-decision example:**

```yaml
---
id: DEC-001
type: architecture-decision
question_id: Q-001
alternatives:
  - id: A
    description: "Vector-only memory"
    selected: false
    reason: "Baseline approach"
  - id: C
    description: "Hybrid fusion with lifecycle"
    selected: true
    reason: "Addresses gap"
risks: ["Higher complexity", "No direct precedent"]
evidence_refs: [P-001, P-002]
gate_b_passed: true
---
```

**evaluation-report example:**

```yaml
---
id: EXP-001
type: evaluation-report
decision_id: DEC-001
hypothesis: "Hybrid fusion improves long-term retention"
metrics:
  - name: retention_7day
    baseline: 0.72
    result: 0.84
    improvement: "+16.7%"
ground_truth: rule-derived
result: supported
confidence: high
gate_c_passed: true
---
```

#### Dependency Tracking

**Automatic dependency recording:**

When `omr-decision` produces `decision-DEC-001.md`:
```yaml
dependencies:
  - id: Q-001
    type: research-brief
    file: docs/plans/brief-Q-001.md
  - id: Q-001
    type: evidence-map
    file: docs/plans/evidence-Q-001.md
```

**Reverse dependency (dependents) updated automatically:**

In `brief-Q-001.md`:
```yaml
dependents:
  - id: DEC-001
    type: architecture-decision
    file: docs/plans/decision-DEC-001.md
```

#### Index Files (Machine-Readable)

**Artifact Index:** `docs/index/artifacts-index.json`

```json
{
  "artifacts": [
    {
      "id": "Q-001",
      "type": "research-brief",
      "version": "1.0.0",
      "status": "published",
      "file": "docs/plans/brief-Q-001.md",
      "created_at": "2026-04-11T10:30:00Z",
      "dependencies": [],
      "dependents": ["DEC-001", "EVI-001"]
    }
  ]
}
```

**Version History:** `docs/index/versions/{id}-history.json`

```json
{
  "id": "DEC-001",
  "history": [
    {
      "version": "1.0.0",
      "created_at": "2026-04-11T14:20:00Z",
      "status": "archived",
      "reason": "Superseded by v2.0.0 due to new contradicting evidence",
      "file": "docs/archive/decision-DEC-001-v1.0.0.md"
    },
    {
      "version": "2.0.0",
      "created_at": "2026-04-11T16:45:00Z",
      "status": "published",
      "reason": "Updated to include graph-only as alternative",
      "file": "docs/plans/decision-DEC-001.md"
    }
  ]
}
```

#### Gate Metadata

When a gate is passed, record in artifact:

```yaml
gates_passed:
  - gate: gate_b
    passed_at: 2026-04-11T15:00:00Z
    reviewer: user
    checks:
      - "Alternatives documented: ✓"
      - "Risks stated: ✓"
      - "Evidence refs valid: ✓"
```

#### Schema Validation

**JSON Schema for each artifact type:** `docs/schemas/{type}.schema.json`

Skills validate output against schema before writing artifacts.

### Cross-Reference Format

```markdown
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

- **Survey/Report/Manuscript/Brief**: Authoritative, evidence-bound (output type configurable)
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

### Evidence-First Pattern

```bash
# 1. Initialize project
/omr-bootstrap "agent memory mechanisms"

# 2. First action (pattern emerges)
/omr-collection https://arxiv.org/abs/2401.xxxxx
# System: "Pattern emerging: Evidence-First. Save? [y/N]"
# User: y

# 3. Map evidence
/omr-evidence  # → research-brief.md + evidence-map.md

# 4. Plan research (Gate A)
/omr-research-plan  # → judgment-summary.md + research-plan.md
# Gate A review

# 5. Make decision (Gate B)
/omr-decision  # → architecture-decision.md
# Gate B review

# 6. Evaluate (Gate C)
/omr-evaluation  # → experiment-spec.md + evaluation-report.md
# Gate C review

# 7. Synthesize (Gate D)
/omr-synthesis  # → docs/survey/ (mode from pattern)
# Gate D review

# 8. Generate wiki
/omr-wiki  # → wiki/
```

### Idea-First Pattern

```bash
# 1. Initialize + capture idea
/omr-bootstrap "speculative topic"
/omr-idea-note "What if memory works like quantum superposition?"

# 2. Make decision (no gates until D)
/omr-decision  # → architecture-decision.md (no evidence yet)

# 3. Build and test
/omr-evaluation  # → prototype + results

# 4. Backfill evidence
/omr-evidence  # → validate or refute decision

# 5. Synthesize (Gate D)
/omr-synthesis --brief  # → docs/brief/
# Gate D review
```

### Reconciliation Scenario

```bash
# Mid-research, new paper arrives
/omr-collection https://arxiv.org/abs/2402.99999
# System: "New evidence contradicts Decision DEC-001. Reconcile? [Y/n]"

# User approves reconciliation
/omr-reconcile
# System:
#   ✓ Re-evaluating evidence...
#   ✓ Updating judgment...
#   ✓ Re-deciding (Gate B)...
#   ✓ Archived: docs/archive/decision-dec-001-v1/
#   ✓ Updated: architecture-decision.md

# Continue with new state
/omr-evaluation  # Re-run with updated decision
```

## Design Principles

### Core Decisions

| Dimension | Decision | Rationale |
|-----------|----------|-----------|
| Skill model | 12 composable skills | Right granularity |
| Progress model | Skill tree (game-inspired) | Visible progress |
| Planning model | Reverse skill tree | Goal-driven |
| Patterns | Emerged from practice, saved | Flexible rigor |
| Gates | Skill-level (A, B, C, D) | Quality checkpoints |
| Agency | Configurable per pattern | Novice + expert support |
| Archive | Auto + manual trigger | Safety + control |
| Synthesis | Configurable output modes | Context-aware |

### What Makes omr Different

| Other Tools | omr |
|-------------|-----|
| Fixed pipeline | Flexible patterns |
| No visibility into progress | Skill tree shows exact state |
| Manual iteration | Automatic reconciliation |
| One output type | Configurable synthesis (survey/report/manuscript/brief) |
| No quality gates | 4 gates enforce rigor |
| Artifacts scattered | Everything in structured folders |

## Simplest Mental Model

**omr = Skills + Tree + Gates + Patterns + Reconciliation**

1. **Skills** = tools (do one thing well)
2. **Tree** = progress visualization (what's unlocked)
3. **Gates** = quality checks (don't publish garbage)
4. **Patterns** = recipes (save working sequences)
5. **Reconciliation** = iteration support (research changes)
