---
stepsCompleted: [1, 2]
inputDocuments: []
session_topic: 'Polishing the design of omr skills — interactions, naming conventions, workflow integration'
session_goals: 'Clearer skill boundaries, better modularity, enhanced user workflow'
selected_approach: 'AI-Recommended Techniques'
techniques_used: ['Morphological Analysis', 'Assumption Reversal', 'SCAMPER Method']
ideas_generated: []
context_file: ''
---

# Brainstorming Session Results

**Facilitator:** Xiaming
**Date:** 2026-04-11

## Session Overview

**Topic:** Polishing the design of omr skills — interactions, naming conventions, workflow integration
**Goals:** Clearer skill boundaries, better modularity, enhanced user workflow

### Context Guidance

_Current omr skills (omr-init, omr-ingest, omr-evidence, omr-brief, omr-decision, omr-experiment, omr-evaluate, omr-writeback, omr-index) were adapted from agent-memory-survey methodology. The design needs refinement in how skills interact, how they're named, and how they integrate into a coherent user workflow._

### Session Setup

_Three focus areas identified: skill interactions (how skills compose and hand off), naming conventions (clarity and discoverability), and workflow integration (seamless user experience across the pipeline). Target outcomes: clearer boundaries between skills, better modularity for reuse, and an enhanced user workflow._

## Technique Selection

**Approach:** AI-Recommended Techniques
**Analysis Context:** Polishing omr skills design with focus on interactions, naming conventions, workflow integration

**Recommended Techniques:**

- **Morphological Analysis:** Systematically map design space across skill scope, triggers, outputs, dependencies, and naming patterns to identify gaps and opportunities
- **Assumption Reversal:** Challenge foundational assumptions about skill interactions, naming conventions, and workflow patterns to discover breakthrough insights
- **SCAMPER Method:** Apply systematic improvement framework (Substitute, Combine, Adapt, Modify, Put to other uses, Eliminate, Reverse) to generate actionable improvements

**AI Rationale:** This sequence moves from comprehensive mapping (Morphological Analysis) to paradigm challenge (Assumption Reversal) to systematic refinement (SCAMPER), perfectly suited for system design refinement with clear actionable outcomes.

## Technique 1: Morphological Analysis — Results

**Interactive Focus:** Mapped design space across 7 parameters, resolved 5, discovered critical gaps (iteration, ideas, plans, archive)

**Key Breakthroughs:**

### 1. Final Skill Set: 12 Skills

| Category | Skill | Stage | Output |
|----------|-------|-------|--------|
| Core Pipeline | `omr-bootstrap` | Init | Workspace |
| | `omr-collection` | Collection | raw/ + docs/index/ |
| | `omr-evidence` | Definition + Evidence | research-brief.md + evidence-map.md |
| | `omr-research-plan` | Judgment + Planning | judgment-summary.md + research-plan.md |
| | `omr-decision` | Decision | architecture-decision.md |
| | `omr-evaluation` | Validation | experiment-spec.md + evaluation-report.md |
| | `omr-synthesis` | Writeback | survey/report/manuscript/brief (configurable) |
| | `omr-wiki` | Writeback | wiki/ |
| Lifecycle | `omr-reconcile` | Any (iteration) | Reconciliation state |
| | `omr-idea-note` | Any (speculative) | docs/ideas/ |
| | `omr-research-archive` | Any (lifecycle) | docs/archive/ |

### Gate System (4 Gates)

| Gate | Position | Purpose |
|------|----------|---------|
| **Gate A** | Before `omr-research-plan` | Evidence sufficient for planning? |
| **Gate B** | Before `omr-decision` | Architecture decision sound? |
| **Gate C** | Before `omr-evaluation` | Experiment design valid? |
| **Gate D** | Before `omr-synthesis` | Results traceable, no over-claiming? |

### omr-synthesis: Configurable Output Modes

`omr-synthesis` is a meta-skill that produces different output types based on research context. Mode determined by pattern config (default) or user override (`--mode` flag).

| Mode | Output | Best For |
|------|--------|----------|
| `survey` | `docs/survey/` (chapters) | Academic research, literature reviews |
| `report` | `docs/report/` (structured findings) | Industry research, stakeholder deliverables |
| `manuscript` | `docs/manuscript/` (publication-ready) | Academic papers, conference submissions |
| `brief` | `docs/brief/` (executive summary) | Quick findings, time-boxed research |

**Pattern-driven (default):**
```yaml
# Evidence-First pattern config
synthesis_mode: survey
```

**User override:**
```
User: /omr-synthesis --report
System: ✓ Produces docs/report/ (overrides pattern default)
```

### 2. Resolved Design Parameters

| Parameter | Decision |
|-----------|----------|
| State Management | Artifact-bound (all state in files) |
| Composability | Synchronous skill-to-skill calls |
| User Agency | Configurable: semi-automated (default) / fully-automated |
| Workflow Topology | Cyclic (omr-reconcile for feedback loops) |
| Naming Scheme | Output-First (Scheme B): skill name = what it produces |
| Iteration | First-class via omr-reconcile with configurable triggers |

### 3. Skill Interaction Map

| Skill | Can Call | Reason |
|-------|----------|--------|
| `omr-collection` | `omr-reconcile` | New material may need reconciliation |
| `omr-reconcile` | `omr-evidence`, `omr-research-plan` | Re-evaluate affected artifacts |
| `omr-evaluation` | `omr-survey`, `omr-wiki` | Auto-trigger writeback on success |
| `omr-research-plan` | — | Judgment + plan produced together |
| `omr-survey` | `omr-wiki` | Survey update may trigger wiki sync |

**User Creative Strengths:** Strong instinct for gaps (identified missing iteration/loops), naming precision (omr-reconcile, omr-bootstrap), commitment to simplicity (rejected async events)

**Energy Level:** High engagement, decisive decision-making

## Technique 2: Assumption Reversal — Results

**Interactive Focus:** Challenged "skills are pipeline stages" assumption

**Key Breakthrough:**

### Pattern-Based Research Composition (Major Design Shift)

**Insight:** Skills are NOT pipeline stages — they are **composable ingredients**. Research patterns are selected at bootstrap time. Each pattern defines: which skills to invoke, in what order, with what gates. The same skills compose differently for different research approaches.

**Before vs. After:**

| Dimension | Before | After |
|-----------|--------|-------|
| Skills | Pipeline stages | Composable capabilities |
| Pipeline | One fixed flow | Multiple patterns |
| Bootstrap | Creates workspace | Asks "Which pattern?" + creates workspace |
| Gates | Hardcoded per skill | Defined by pattern |
| Entry points | Start at bootstrap | Start anywhere pattern allows |

**Example Patterns:**

| Pattern | Flow | Gates | Best For |
|---------|------|-------|----------|
| Evidence-First | collection → evidence → judgment → decision → validation → survey → wiki | A, B, C | Academic research, literature surveys |
| Idea-First | idea-note → decision → validation → evidence → survey → wiki | C only | Exploratory research, speculative work |
| Decision-First | decision → evidence → judgment → validation → survey → wiki | B, C | Engineering research, prototype-driven |
| Rapid-Prototype | validation → evidence → decision → survey | None | Quick validation, proof-of-concept |

**Implications:**

1. Each skill needs clear **inputs/outputs/prerequisites** (not implicit stage knowledge)
2. Patterns are **templates** stored in `skills/patterns/`
3. `omr-bootstrap` becomes **pattern selector + workspace creator**
4. `omr-reconcile` follows **pattern logic** for iteration
5. Users can **define custom patterns** for their research style

**User Creative Strengths:** Identified the core tension (pipeline rigidity vs. research flexibility), proposed compositional solution that preserves rigor while enabling freedom

## Technique 3: SCAMPER Method — Results

**Interactive Focus:** Systematic improvement across 7 lenses, deep dive into skill tree adaptation

### S — Substitute

- "Pattern" → "Recipe" metaphor (more intuitive)
- Implicit prerequisites → Explicit contracts (`requires:` / `produces:`)
- Fixed skills → Minimal core + optional extensions

### C — Combine

- `omr-survey` + `omr-wiki` → Single skill with modes (keep separate for clarity)
- Pattern definition = Project config (no separate config file)

### A — Adapt: Game Skill Trees (Major Feature)

**Mapping:**

| Game Concept | omr Equivalent |
|--------------|----------------|
| Core skills | Always unlocked: bootstrap, collection, reconcile |
| Skill branches | Research patterns |
| Prerequisites | Artifact requirements for skill invocation |
| Unlock conditions | Producing artifact unlocks downstream |
| Visible progress | Skill tree visualization |
| Respec | `omr-reconcile` = branch switch |

**Benefits:**
- Clear progress visualization
- Prerequisite enforcement
- Pattern = branch choice
- Motivation through unlocking
- Onboarding via visible map

### M — Modify

- Skill granularity → Sub-skills with nested tree nodes
- Gate positions → Checkpoints between skill branches
- Naming → Output-first names + visual labels (e.g., "📝 Evidence Map")

### P — Put to Other Uses: Research Audit

Skill tree state = research provenance. Complete trail of which skills were invoked, in what order, producing which artifacts. Enables "show me how you reached this conclusion."

### E — Eliminate

- `omr-research-archive` → Automatic by default (when reconcile supersedes artifacts), manual trigger available for user-initiated snapshots
- Explicit gates → Implicit in skill tree progression (optional visualization)

### R — Reverse: Output-First Skill Tree (Major Feature)

**Backward Planning:** Start from desired artifact, trace prerequisite chain backward to current state.

**User Experience:**
```
> What's your research goal?
  [1] Produce a survey
  [2] Validate a decision
  ...

> Goal [1]: Produce a survey
> To produce a survey, you need to unlock:
  1. omr-collection ✓
  2. omr-evidence ○
  3. omr-judgment ●
  4. omr-decision ●
  5. omr-validation ●
  6. omr-survey ●

> Recommended pattern: Evidence-First
> Begin? [Y/n]
```

**Benefits:**
- Goal-oriented research
- Effort estimation (X skills between you and goal)
- Gap visualization
- Pattern recommendation based on goal
- Clear finish line

**Dual View Mode:**
- Forward view: Explore what's possible (no specific goal)
- Reverse view: Plan shortest path to goal
- Toggle between perspectives anytime

### Final Design Synthesis

| Component | Decision |
|-----------|----------|
| Skill model | 12 composable skills |
| Progress model | Skill tree (game-inspired) |
| Planning model | Reverse skill tree (goal-first) |
| Patterns | Templates stored in `skills/patterns/` |
| Prerequisites | Explicit contracts per skill |
| Gates | Checkpoints in skill tree progression |
| Agency | Configurable per pattern |
| Visualization | Forward/reverse toggle |
| Archive | Auto + manual trigger |
| Use cases | Research + teaching + audit |

**User Creative Strengths:** Strong preference for goal-oriented design (reverse tree), clear decisions on simplification (archive), valued audit trail for provenance

## Advanced Elicitation: Pattern System Deep Dive

**Method Applied:** First Principles Analysis
**Focus:** Strip away assumptions about patterns, rebuild from fundamental truths

### Fundamental Truths

1. Research is NOT always sequential — iterative, multiple entry points
2. Artifacts have dependencies — can't produce decision without evidence
3. Skills are deterministic — same inputs → same outputs
4. Different research goals need different rigor levels
5. Users are diverse — novices need guidance, experts want speed
6. Complexity is costly — every pattern/gate/skill adds overhead
7. Reuse is valuable — working patterns should be shareable

### Assumptions Challenged

| Assumption | Challenge | Result |
|------------|-----------|--------|
| Patterns are pre-defined templates | What if patterns EMERGE from practice? | **Adopted:** Patterns recorded from skill sequences |
| Patterns selected at bootstrap | What if selection happens AFTER first action? | **Adopted:** Defer pattern detection until user acts |
| Patterns define gate enforcement | What if gates are SKILL-LEVEL? | **Adopted:** Each skill declares its own gates |
| Patterns are monolithic | What if patterns are MODULAR components? | **Adopted:** Patterns = entry + core + branches + termination |
| One pattern per project | What if MULTIPLE concurrent patterns? | **Adopted:** Parallel research threads supported |

### Rebuilt Model: Core Concepts

| Concept | Definition |
|---------|------------|
| **Skill** | Atomic capability with explicit inputs/outputs. Deterministic. Reusable. |
| **Artifact** | File(s) produced by skill. Has dependencies. Immutable once produced. |
| **Pattern** | Named sequence of skill invocations. EMERGES from practice, saved as template. |
| **Dependency Graph** | Actual map of artifact dependencies. Enforced by skill contracts, not patterns. |
| **Gate** | Skill-level quality check. Declared in skill contract. Not pattern-imposed. |
| **Pattern Instance** | Specific execution with concrete artifacts. What actually happened. |

### Pattern Structure (First-Principles)

```yaml
PATTERN = {
  name: "Evidence-First",
  description: "Rigorous research starting from literature",

  # Not rigid sequence — dependency-resolved graph
  graph: {
    entry_points: ["omr-collection"],
    nodes: ["omr-evidence", "omr-judgment", "omr-decision", ...],
    edges: ["omr-collection → omr-evidence", ...]
  },

  # Skill-level gates, not pattern-level
  skill_gates: {
    "omr-decision": "gate_a",
    "omr-validation": "gate_b",
    "omr-survey": "gate_c"
  },

  # Recommendations, not enforcement
  recommendations: {
    agency: "semi-automated",
    estimated_time: "3-5 days"
  }
}
```

### Skill Contract Structure

```yaml
skill: omr-decision
requires:
  - artifact: evidence-map.md
    optional: false
  - artifact: judgment-summary.md
    optional: true
produces:
  - artifact: architecture-decision.md
    schema: "docs/schemas/architecture-decision.schema.json"
gates:
  - id: gate_a
    checks:
      - "Alternatives documented"
      - "Risks stated"
      - "Evidence refs valid"
    enforcement: "user-confirm"  # or "auto-pass" for agents
```

### Pattern Emergence Workflow

1. **Bootstrap** → Workspace created, no pattern forced
2. **First action** → User selects first skill (collection, idea, decision, etc.)
3. **Pattern detection** → After 3+ invocations, system proposes pattern name
4. **Pattern save** → User accepts/rejects saving as reusable template
5. **Template library** → Saved patterns stored in `skills/patterns/`

### Dependency Resolution (Automatic)

```
User: /omr-decision
System: ❌ Cannot invoke — missing required artifacts:
  - evidence-map.md (produce via: omr-evidence)

User: /omr-evidence
System: ✓ Produces evidence-map.md
        → Unlocks: omr-judgment, omr-decision
```

### Key Design Shifts

| Dimension | Before | After |
|-----------|--------|-------|
| Pattern creation | Pre-selected at bootstrap | Emerged from practice, saved |
| Gate ownership | Pattern-level | Skill-level contracts |
| Pattern timing | Forced at init | Detected after actions |
| Concurrency | One pattern per project | Multiple parallel patterns |
| Sequence model | Rigid linear | Dependency-resolved graph |
| Flexibility | Pattern constrains skills | Skills invoked freely, pattern records path |

**User Creative Strengths:** Recognized value of emergent patterns over rigid templates, appreciated skill-level gate ownership for modularity

### Tree of Thoughts: Pattern Composition Model

**Three paths explored:**
1. Strict Dependency Graph — one global graph, patterns = views (too rigid)
2. Pattern-Local Graphs — each pattern owns its graph (flexible but divergent)
3. Contract-Based Composition — no graphs, runtime resolution (too dynamic)

**Selected: Path 2+ (Pattern-Local Graphs + Shared Contracts)**

- Skill contracts are SHARED — single source of truth for requires/produces
- Pattern graphs are LOCAL — each pattern defines its own flow
- Optional requirements handle context — mandatory reqs must be satisfied, optional may be skipped
- Pattern validation — system validates no impossible paths against contracts

**Validation rule:** A pattern is valid if every skill's MANDATORY requirements are satisfied by an upstream skill's outputs. Optional requirements may be unsatisfied.

**Renamed:** `omr-validation` → `omr-evaluation`

**Added pattern:** Experiment-First

### Complete Pattern Library

#### Evidence-First
Rigorous research starting from literature collection.
```
omr-collection → omr-evidence → omr-research-plan → omr-decision → omr-evaluation → omr-synthesis → omr-wiki
```
Gates: A (before planning), B (before decision implementation), C (before experiment), D (before publish)
Agency: semi-automated
Synthesis mode: survey
Best for: Academic research, literature surveys, systematic reviews

#### Idea-First
Speculative research starting from creative insight.
```
omr-idea-note → omr-decision → omr-evaluation → omr-evidence → omr-synthesis → omr-wiki
```
Gates: D only (before publish)
Agency: semi-automated
Synthesis mode: brief
Best for: Exploratory research, speculative work, early-stage ideation
Note: `judgment-summary.md` (optional for `omr-decision`) is not produced before decision — satisfies validation rule

#### Decision-First
Hypothesis-driven research starting from an architectural stance.
```
omr-decision → omr-evidence → omr-research-plan → omr-evaluation → omr-synthesis → omr-wiki
```
Gates: C (before experiment), D (before publish)
Agency: semi-automated
Synthesis mode: report
Best for: Engineering research, prototype-driven investigation

#### Experiment-First
Empirical research starting from building and testing.
```
omr-evaluation → omr-evidence → omr-decision → omr-synthesis → omr-wiki
```
Gates: D only (before publish)
Agency: semi-automated or fully-automated
Synthesis mode: brief
Best for: Quick validation, proof-of-concept, empirical testing, rapid prototyping
Note: Minimal ceremony — start by building/testing, then backfill evidence and decisions

#### Rapid-Prototype
Fastest path to a working output.
```
omr-evaluation → omr-evidence → omr-decision → omr-synthesis
```
Gates: none
Agency: fully-automated
Synthesis mode: brief
Best for: Hackathons, proof-of-concept, time-boxed exploration

### Skill Contract Definitions (Shared)

```yaml
omr-bootstrap:
  requires: []
  produces: [workspace structure, CLAUDE.md]
  gates: []

omr-collection:
  requires: [workspace]
  produces: [raw/*, docs/index/*]
  gates: []

omr-evidence:
  requires: [materials in raw/]
  produces: [research-brief.md, evidence-map.md]
  gates: []

omr-research-plan:
  requires: [evidence-map.md]
  produces: [judgment-summary.md, research-plan.md]
  gates: [gate_a]  # Evidence sufficient for planning?

omr-decision:
  requires: [evidence-map.md]
  optional_requires: [judgment-summary.md]
  produces: [architecture-decision.md]
  gates: [gate_b]  # Architecture decision sound?

omr-evaluation:
  requires: [architecture-decision.md]
  optional_requires: [experiment-spec.md]
  produces: [experiment-spec.md, evaluation-report.md]
  gates: [gate_c]  # Experiment design valid?

omr-synthesis:
  requires: [evaluation-report.md OR judgment-summary.md]
  produces: [docs/survey/* OR docs/report/* OR docs/manuscript/* OR docs/brief/*]
  gates: [gate_d]  # Results traceable, no over-claiming?
  modes: [survey, report, manuscript, brief]
  default_mode: defined by pattern

omr-wiki:
  requires: [any synthesis chapter OR any judgment]
  produces: [wiki/*]
  gates: []

omr-idea-note:
  requires: []
  produces: [docs/ideas/*]
  gates: []

omr-reconcile:
  requires: [at least one existing artifact]
  produces: [reconciliation state, archived artifacts]
  gates: []
```

### Pattern Validation Examples

**Evidence-First** ✓
- omr-research-plan gets evidence-map.md (mandatory ✓) → produces judgment-summary.md + research-plan.md
- omr-decision gets evidence-map.md (mandatory ✓) + judgment-summary.md (optional ✓ from research-plan)
- omr-evaluation gets architecture-decision.md (mandatory ✓)
- omr-survey gets evaluation-report.md (mandatory ✓)

**Idea-First** ✓
- omr-decision gets evidence-map.md (mandatory ✓), judgment-summary.md not produced (optional, OK ✓)
- omr-evaluation gets architecture-decision.md (mandatory ✓)
- omr-survey gets evaluation-report.md (mandatory ✓)

**Experiment-First** ✓
- omr-evaluation: requires architecture-decision.md — but none exists yet!
  → Pattern declares: omr-evaluation produces experiment-spec.md first (exploratory mode)
  → Modified contract: omr-evaluation can run WITHOUT architecture-decision.md in experiment-first mode
  → architecture-decision.md is produced retroactively via omr-decision after evidence
- Validated: mandatory requirements satisfied per pattern-specific overrides

**Key insight:** Some patterns need CONTRACT OVERRIDES — Experiment-First allows `omr-evaluation` without prior `architecture-decision.md`. Pattern definitions must declare these overrides explicitly.

```yaml
# Pattern-specific override example
Experiment-First:
  contract_overrides:
    omr-evaluation:
      requires: []  # Allow evaluation without prior decision
```

### Skill Merge: omr-judgment → omr-research-plan

**Rationale:** Judgment and planning are naturally coupled — you judge evidence IN ORDER TO plan research. Two separate skills for what's really one cognitive act.

**Before:** 12 skills
```
omr-evidence → omr-judgment → omr-research-plan → omr-decision
                   ↓                  ↓
           judgment-summary.md   research-plan.md
```

**After:** 11 skills
```
omr-evidence → omr-research-plan → omr-decision
                      ↓
            judgment-summary.md + research-plan.md
```

**Impact:** Evidence-First and Decision-First patterns simplified (one fewer step). Idea-First, Experiment-First, Rapid-Prototype unchanged (don't use judgment/plan).

### Comparative Analysis Matrix: Design Validation

**Five key decisions evaluated against weighted criteria:**

#### Matrix 1: Skill Composition Models

| Criterion | Weight | Path 1: Strict Graph | Path 2+: Local Graphs + Shared Contracts | Path 3: Contract-Based |
|-----------|--------|---------------------|------------------------------------------|----------------------|
| Simplicity | 20% | 5 | 4 | 2 |
| Flexibility | 25% | 2 | 4 | 5 |
| Predictability | 15% | 5 | 4 | 2 |
| Pattern emergence | 15% | 2 | 4 | 5 |
| Visualization | 10% | 5 | 4 | 2 |
| Debuggability | 10% | 5 | 4 | 2 |
| Maintainability | 5% | 4 | 3 | 3 |
| **Weighted Score** | **100%** | **3.75** | **3.90** ✓ | **3.15** |

**Verdict:** Path 2+ confirmed — flexibility + predictability balance.

#### Matrix 2: Pattern Selection Timing

| Criterion | Weight | At Bootstrap | After First Action | Never (Pure Emergence) |
|-----------|--------|-------------|-------------------|----------------------|
| User guidance | 30% | 5 | 4 | 1 |
| Flexibility | 25% | 2 | 4 | 5 |
| Cognitive load | 20% | 2 | 4 | 5 |
| Predictability | 15% | 5 | 4 | 2 |
| Onboarding | 10% | 5 | 4 | 1 |
| **Weighted Score** | **100%** | **3.45** | **4.00** ✓ | **2.80** |

**Verdict:** After First Action wins — guidance without forced commitment.

#### Matrix 3: Gate Enforcement Strategy

| Criterion | Weight | Pattern-Level | Skill-Level (current) | Hybrid (skill default + pattern override) |
|-----------|--------|-------------|---------------------|------------------------------------------|
| Modularity | 25% | 2 | 5 | 4 |
| Flexibility | 25% | 2 | 3 | 5 |
| Consistency | 20% | 5 | 4 | 3 |
| Simplicity | 15% | 4 | 4 | 2 |
| Audit trail | 15% | 3 | 4 | 5 |
| **Weighted Score** | **100%** | **2.95** | **4.10** ✓ | **3.85** |

**Verdict:** Skill-level gates confirmed. Key insight: Contract overrides already implement hybrid model (Experiment-First pattern overrides `omr-evaluation` requirements).

#### Matrix 4: Research Archive Strategy

| Criterion | Weight | Explicit Skill Only | Auto-Only | Auto + Manual Trigger (current) |
|-----------|--------|-------------------|-----------|-------------------------------|
| Safety | 25% | 5 | 2 | 4 |
| Simplicity | 25% | 3 | 5 | 3 |
| User control | 25% | 5 | 1 | 5 |
| Data integrity | 15% | 3 | 5 | 5 |
| Discoverability | 10% | 2 | 4 | 4 |
| **Weighted Score** | **100%** | **3.85** | **2.90** | **4.20** ✓ |

**Verdict:** Auto + Manual Trigger confirmed — safety + user control balance.

#### Matrix 5: Skill Granularity

| Criterion | Weight | 9 Skills (merged) | 11 Skills (current) | 14+ Skills (split) |
|-----------|--------|-------------------|---------------------|---------------------|
| Cognitive load | 25% | 5 | 4 | 2 |
| Modularity | 25% | 2 | 4 | 5 |
| Composability | 20% | 2 | 4 | 5 |
| Naming clarity | 15% | 3 | 4 | 3 |
| Maintenance | 15% | 4 | 4 | 2 |
| **Weighted Score** | **100%** | **3.15** | **4.00** ✓ | **3.40** |

**Verdict:** 11 skills confirmed — right granularity.

### Validation Summary

| Decision | Winner | Confidence |
|----------|--------|-----------|
| Composition model | Path 2+ (Local Graphs + Shared Contracts) | High |
| Pattern selection timing | After First Action | High |
| Gate enforcement | Skill-level (with pattern overrides) | High |
| Archive strategy | Auto + Manual Trigger | High |
| Skill granularity | 11 skills | High |

**Result:** All design decisions validated. No weaknesses surfaced requiring redesign. Model is consistent across evaluation criteria.

### End-to-End Walkthrough: Complete Research Session

**Scenario:** Researcher investigating "Agent Memory Mechanisms"

#### Step 1: Bootstrap
```
User: /omr-bootstrap "agent memory mechanisms"

System: ✓ Workspace created at ./agent-memory-mechanisms/
        ✓ Generated: CLAUDE.md, workspace structure
        ✓ Skills available: 11 core skills

        What's your first action?
        [1] I have papers to collect — start with materials
        [2] I have an idea to explore — start with insight
        [3] I have a decision to validate — start with architecture
        [4] I have a hypothesis to test — start with evaluation
        [5] I'm exploring — no specific goal yet
```
**Design check:** ✓ Pattern selection deferred until first action

#### Step 2: Collection — Pattern Emergence
```
User: [1] I have papers to collect

System: ✓ Downloaded 3 materials
        ✓ Classified: 2 papers → raw/paper/, 1 blog → raw/web/
        ✓ Indexed: docs/index/papers-index.json, blogs-index.json

        📊 Skill Tree Updated:
        [✓] omr-collection ──► 2 papers, 1 blog indexed
             │
             ├──[○] omr-evidence ──► [READY]
             │      │
             │      └──[●] omr-research-plan ──► [LOCKED: needs evidence-map.md]
             │
             └──[✓] omr-idea-note ──► Available anytime

        Pattern emerging: Evidence-First (detected)
        Save this pattern as default for similar projects? [y/N]
```
**Design check:** ✓ Pattern emerged from first action, ✓ Skill tree shows progress

#### Step 3: Evidence Mapping
```
User: /omr-evidence

System: ✓ Generated: research-brief.md (question_id: Q-001, scope defined)
        ✓ Generated: evidence-map.md (primary evidence identified, gaps noted)

        📊 Skill Tree Updated:
        [✓] omr-evidence ──► research-brief.md + evidence-map.md
             │
             └──[○] omr-research-plan ──► [READY] (Gate A)
```
**Design check:** ✓ Dependency satisfied, ✓ Downstream skills unlocked

#### Step 4: Judgment + Planning (Gate A)
```
User: /omr-research-plan

System: ✓ Requires: evidence-map.md (satisfied ✓)

        Synthesizing judgment and planning research approach...

        ✓ Generated: judgment-summary.md
          - Main conclusion: "Current research focuses on retrieval, neglects lifecycle"
          - Confidence: Medium

        ✓ Generated: research-plan.md
          - Priority 1: Design memory lifecycle model
          - Timeline: 3-5 days estimated

        ⚠️  GATE A: Before Planning
        Evidence sufficient for research planning?

        Review criteria:
        [✓] Evidence coverage adequate
        [✓] Research question clear
        [✓] Scope defined

        Proceed with this plan? [Y/n]
```
```
User: Y

System: ✓ Gate A passed

        📊 Skill Tree Updated:
        [✓] omr-research-plan ──► judgment-summary.md + research-plan.md
             │
             └──[○] omr-decision ──► [READY] (Gate B)
```
**Design check:** ✓ Gate A enforced before planning, ✓ Merged skill produces both outputs

#### Step 5: Architecture Decision (Gate B)
```
User: /omr-decision

System: ✓ Generated: architecture-decision.md (DEC-001)
          - Alternatives: A (vector-only), B (graph-only), C (hybrid fusion)
          - Selected: Alternative C
          - Evidence refs: [Paper 1, Paper 2]
          - Risks documented

        ⚠️  GATE B: Before Implementation
        Architecture decision sound?

        Review criteria:
        [✓] Alternatives documented
        [✓] Risks stated
        [✓] Evidence refs valid

        Proceed with this decision? [Y/n]

        📊 Skill Tree Updated:
        [✓] omr-decision ──► architecture-decision.md
             │
             └──[○] omr-evaluation ──► [READY] (Gate C)
```
**Design check:** ✓ Gate B enforced, ✓ Traceability (decision_id, evidence_refs)

#### Step 6: Evaluation (Gate C)
```
User: /omr-evaluation

System: ✓ Generated: experiment-spec.md (EXP-001)
          - Hypothesis defined
          - Metrics specified
          - Ground truth: rule-derived

        Running evaluation...
        ✓ Prototype implemented in src/prototype/
        ✓ Tests executed: 15 scenarios

        ✓ Generated: evaluation-report.md
          - Hypothesis: Supported
          - Decision DEC-001: Validated
          - Traceability: EXP-001 → DEC-001 → Q-001

        ⚠️  GATE C: Before Survey Writeback
        Experiment design valid?

        Review criteria:
        [✓] Metrics answer research question
        [✓] Failure conditions explicit
        [✓] Reproducible evaluation

        Proceed to writeback? [Y/n]

        📊 Skill Tree Updated:
        [✓] omr-evaluation ──► experiment-spec.md + evaluation-report.md
             │
             ├──[○] omr-survey ──► [READY] (Gate D)
             └──[○] omr-wiki ──► [READY]
```
**Design check:** ✓ Gate C enforced, ✓ Traceability maintained

#### Step 7: Reconciliation (Testing Iteration)
```
User: /omr-ingest https://arxiv.org/abs/2402.99999

System: ✓ Downloaded new paper → raw/paper/
        ⚠️  New evidence detected — reconciliation needed

        New paper contradicts Decision DEC-001:
        - Claims graph-only memory outperforms fusion

        Impact analysis:
        - Decision DEC-001: ⚠️ Contradicted
        - Experiment EXP-001: ⚠️ May test suboptimal approach

        Call omr-reconcile? [Y/n]

User: Y

System: ✓ Re-evaluating evidence...
        ✓ Updated: evidence-map.md, judgment-summary.md
        ⚠️  Gate B: Decision needs revision

        Decision DEC-001 (updated):
        - Alternatives: Add graph-only as co-equal option
        - Risks: Add "comparative study needed"

        Approve updated decision? [Y/n]

User: Y

System: ✓ Decision updated
        ✓ Previous artifacts archived: docs/archive/decision-dec-001-v1/

        📊 Skill Tree Updated:
        [✓] omr-reconcile ──► State reconciled
             │
             └──[○] omr-evaluation ──► [READY: re-run with updated decision]
```
**Design check:** ✓ Reconciliation triggered by new evidence, ✓ Skills called in order, ✓ Archives preserved

#### Step 8: Synthesis Writeback (Gate D)
```
User: /omr-synthesis

System: ✓ Mode: survey (pattern default for Evidence-First)
        ✓ Generated: docs/survey/*.md

        ⚠️  GATE D: Before Publish
        Synthesis ready for publication.

        Review criteria:
        [✓] Results traceable to hypotheses
        [✓] Evidence boundaries stated
        [✓] No over-claiming

        Publish synthesis? [Y/n]

        📊 Skill Tree Updated:
        [✓] omr-synthesis ──► docs/survey/
             │
             └──[○] omr-wiki ──► [READY]
```
**Design check:** ✓ Gate D enforced, ✓ Synthesis mode from pattern config, ✓ Traceability complete

#### Step 9: Wiki Sync
```
User: /omr-wiki

System: ✓ Generated: wiki/*.md with cross-references to survey

        📊 Skill Tree Complete:
        [✓] omr-wiki ──► wiki/
```

### End-to-End Verification Summary

| Feature | Tested | Status |
|---------|--------|--------|
| Pattern emergence | ✓ | Works — pattern saved after collection |
| Skill dependencies | ✓ | Works — skills unlock progressively |
| Skill tree visualization | ✓ | Works — shows progress at each step |
| Gate enforcement (A/B/C/D) | ✓ | Works — gates check criteria before each skill |
| Traceability (Q → DEC → EXP → Survey) | ✓ | Works — IDs maintained throughout |
| Reconciliation | ✓ | Works — new evidence triggers re-evaluation |
| Archiving | ✓ | Works — v1 artifacts preserved |
| Merged skill (judgment+plan) | ✓ | Works — produces both outputs efficiently |

**Result:** Design works end-to-end. All pieces fit together coherently.

### Feynman Technique: Simple Explanation + Gap Analysis

**Method Applied:** Explain the pattern system simply as if teaching a newcomer

**Complete Simple Explanation:**

#### The Core Idea: Research is NOT Linear

Real research is messy. Sometimes you start with a hunch (decision-first), start by building something (experiment-first), start with a creative insight (idea-first), or start by reading everything (evidence-first). omr doesn't force you into one path. It gives you skills that work together and lets you pick your starting point.

#### 12 Skills Explained Simply

| Skill | What It Does | Output |
|-------|--------------|--------|
| `omr-bootstrap` | Set up a new research project | A folder with structure |
| `omr-collection` | Download and organize materials | PDFs, blogs, code in `raw/` |
| `omr-evidence` | Read materials and extract what matters | Brief + evidence map |
| `omr-research-plan` | Judge evidence and plan your attack | Judgment + plan |
| `omr-decision` | Make an architectural choice | Decision with alternatives |
| `omr-evaluation` | Build and test your idea | Code + evaluation report |
| `omr-synthesis` | Write up what you found | Survey/report/manuscript/brief |
| `omr-wiki` | Turn findings into a wiki | Living knowledge base |
| `omr-idea-note` | Capture a speculative thought | Note in `docs/ideas/` |
| `omr-reconcile` | Fix things when new evidence arrives | Updated artifacts + archives |
| `omr-research-archive` | Snapshot your progress | Archive of current state |

#### The Simplest Mental Model

**omr = Skills + Tree + Gates + Patterns + Reconciliation**

1. **Skills** = tools (do one thing well)
2. **Tree** = progress visualization (what's unlocked)
3. **Gates** = quality checks (don't publish garbage)
4. **Patterns** = recipes (save working sequences)
5. **Reconciliation** = iteration support (research changes)

#### What Makes This Different

| Other Tools | omr |
|-------------|-----|
| Fixed pipeline | Flexible patterns |
| No visibility into progress | Skill tree shows exact state |
| Manual iteration | Automatic reconciliation |
| One output type | Configurable synthesis (survey/report/manuscript/brief) |
| No quality gates | 4 gates enforce rigor |
| Artifacts scattered | Everything in structured folders |

#### Gaps Identified

1. **Onboarding example missing** — The explanation assumes someone already knows what they want to research. Should show a "blank slate" example for first-time users.

2. **Multi-pattern concurrency underspecified** — Said "multiple patterns can run in parallel" but didn't explain HOW the user would do that. Need: how to spawn a parallel pattern, how artifacts are shared/isolated, how conflicts are handled.

3. **Pattern sharing not explained** — Said patterns are saved, but not where or how they're shared across projects. Need: pattern storage format, import/export mechanism, pattern library location.

4. **Failure scenarios glossed over** — What happens if a gate fails? Can you skip it? (Answer: yes, if you switch to fully-automated mode, but not clearly stated.) Need: explicit gate failure handling workflow.
