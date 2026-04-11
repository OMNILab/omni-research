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
| | `omr-judgment` | Judgment | judgment-summary.md |
| | `omr-decision` | Decision | architecture-decision.md |
| | `omr-validation` | Validation | experiment-spec.md + evaluation-report.md |
| | `omr-survey` | Writeback | docs/survey/ |
| | `omr-wiki` | Writeback | wiki/ |
| Lifecycle | `omr-reconcile` | Any (iteration) | Reconciliation state |
| | `omr-research-plan` | After judgment | research-plan.md |
| | `omr-idea-note` | Any (speculative) | docs/ideas/ |
| | `omr-research-archive` | Any (lifecycle) | docs/archive/ |

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
| `omr-reconcile` | `omr-evidence`, `omr-judgment` | Re-evaluate affected artifacts |
| `omr-validation` | `omr-survey`, `omr-wiki` | Auto-trigger writeback on success |
| `omr-judgment` | `omr-research-plan` | Judgment feeds plan |
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
