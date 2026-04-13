---
created_from: 
  - brainstorming-session-2026-04-11-001.md
  - brainstorming-session-2026-04-12-1124.md
date: 2026-04-12
status: draft
---

# Implementation Plan: omr Skills System

## Executive Summary

**Goal**: Implement a composable research skill system with 11 skills, skill tree visualization, pattern emergence, gate enforcement, and reconciliation support.

**Design Philosophy**: Skills are NOT pipeline stages — they are composable ingredients. Patterns emerge from practice, gates are skill-level, dependencies are artifact-bound.

**Total Skills**: 11 core skills
**Gates**: 4 gates (A, B, C, D) at skill-level
**Patterns**: 5 predefined + user-defined patterns
**Timeline**: 8-12 weeks (phased approach)

---

## Phase 1: Foundation (Weeks 1-3)

### 1.1 Skill Contract System

**Objective**: Define artifact-bound dependencies with explicit contracts

**Implementation**:

1. **Contract Schema** (`skills/schemas/contract.schema.json`)
   ```json
   {
     "skill": "skill-name",
     "requires": [{"artifact": "filename.md", "optional": false}],
     "produces": [{"artifact": "output.md", "schema": "path/to/schema.json"}],
     "gates": [{"id": "gate_id", "checks": [], "enforcement": "user-confirm"}]
   }
   ```

2. **Contract Registry** (`skills/contracts/`)
   - Create contract file for each of 11 skills
   - Validate contracts against schema
   - Test dependency resolution logic

3. **Dependency Resolver** (Python script)
   - Input: requested skill + current workspace state
   - Output: can invoke? (check requires satisfied) + unlock downstream skills
   - Pattern override support (Experiment-First allows omr-evaluation without prior decision)

**Deliverables**:
- ✓ 11 contract files validated
- ✓ Dependency resolver working
- ✓ Test: invoke skill with missing prerequisite → blocked
- ✓ Test: produce artifact → unlock downstream skills

**Dependencies**: None (first component)

---

### 1.2 Workspace Structure

**Objective**: Define standard workspace layout + CLAUDE.md generation

**Implementation**:

1. **Directory Structure** (`omr-bootstrap` creates):
   ```
   project-name/
   ├── CLAUDE.md              # Project instructions
   ├── raw/                   # Materials
   │   ├── paper/
   │   ├── web/
   │   ├── github/
   │   ├── dataset/
   │   ├── search/
   │   └── failed/
   ├── docs/
   │   ├── index/             # Metadata indexes
   │   ├── ideas/             # Idea notes
   │   ├── archive/           # Archived artifacts
   │   ├── survey/            # Synthesis output
   │   ├── report/
   │   ├── manuscript/
   │   └── brief/
   ├── wiki/                  # Wiki output
   ├── src/                   # Code prototypes
   └── skills/                # Pattern definitions
       ├── patterns/
       └── contracts/
   ```

2. **CLAUDE.md Template** (auto-generated)
   - Project name + research question (if provided)
   - Active pattern (detected after first action)
   - Skill tree state (which skills unlocked)
   - Last updated timestamp

3. **Bootstrap Script** (`omr-bootstrap`)
   - Create directory structure
   - Generate CLAUDE.md from template
   - Initialize empty indexes
   - NO pattern selection yet (deferred)

**Deliverables**:
- ✓ Workspace structure created
- ✓ CLAUDE.md generated
- ✓ Bootstrap skill working
- ✓ Test: create new project → structure exists

**Dependencies**: None (parallel with 1.1)

---

### 1.3 Skill Tree Visualization

**Objective**: Visual progress tracking showing unlocked skills

**Implementation**:

1. **Skill Tree State** (`skills/tree-state.json`)
   ```json
   {
     "unlocked": ["omr-bootstrap", "omr-collection"],
     "ready": ["omr-evidence"],
     "locked": ["omr-research-plan", "omr-decision", ...],
     "completed": ["omr-bootstrap"]
   }
   ```

2. **Tree Renderer** (ASCII art or HTML)
   - Forward view: explore what's possible
   - Reverse view: plan shortest path to goal
   - Toggle switch in UI

3. **Update Mechanism**
   - On artifact produced → update tree state
   - On skill invoked → mark completed
   - On dependency satisfied → unlock downstream

**Deliverables**:
- ✓ Tree state tracked
- ✓ ASCII visualization working
- ✓ Test: produce artifact → tree updates

**Dependencies**: 1.1 (need dependency resolver)

---

## Phase 2: Core Skills Implementation (Weeks 4-6)

### 2.1 omr-collection (Detailed from Session 2)

**Objective**: Material collection with search support + minimal parsing

**Architecture** (from brainstorming-session-2026-04-12-1124.md):

**Components**:
1. **Input Router** (detect URL vs search query)
   - Pattern matching: URLs, DOIs, Arxiv IDs
   - Search detection: quoted string OR no URL pattern
   - Fallback: treat as search query

2. **4 Handlers**:
   - Generic Web: Chrome MCP → snapshot + markdown
   - Paper: PDF download → marker/pdfplumber → markdown
   - GitHub: README + release info (GitHub API)
   - HuggingFace: README + card (browser + HF API)

3. **Search Integration** (hybrid confirmation):
   - Search APIs: arxiv API, GitHub search, HF search
   - Present results: top-10 per source (sensible defaults)
   - User confirmation: accept default OR override
   - Output: `raw/search/query-hash/`

4. **Configurable Depth**:
   - Default: README + metadata (researcher-appropriate)
   - Override flags: `--download-dataset`, `--full-repo`, `--with-supplementary`

5. **Error Handling**:
   - Retry: 2x with 2s delay
   - Fallback: Generic Web snapshot
   - Error artifacts: `raw/failed/url-hash-error.md`

**Deliverables**:
- ✓ 4 handlers working
- ✓ Search with hybrid confirmation
- ✓ Configurable depth flags
- ✓ Error handling (retry + fallback)
- ✓ Test: collect paper → DOI naming
- ✓ Test: search query → user confirmation
- ✓ Test: failed URL → error artifact

**Dependencies**: 1.1 (contract), 1.2 (workspace)

**Implementation Priorities** (from session 2):
- **Phase 2.1a**: Core handlers (Generic Web, Paper, GitHub, HuggingFace)
- **Phase 2.1b**: Search integration (APIs + confirmation UI)
- **Phase 2.1c**: Reliability (retry + fallback + error artifacts)
- **Phase 2.1d**: Pattern compatibility flags

---

### 2.2 omr-evidence

**Objective**: Extract evidence from materials + create brief + evidence map

**Implementation**:

1. **Input**: Materials in `raw/` (papers, web, github, datasets)
2. **Processing**:
   - Read markdown artifacts
   - Extract: research questions, claims, evidence, gaps
   - NO semantic metadata (minimal parsing from session 2)

3. **Output**:
   - `research-brief.md` (question_id, scope, context)
   - `evidence-map.md` (primary evidence, gaps, confidence)

4. **Contract**:
   ```yaml
   requires: [materials in raw/]
   produces: [research-brief.md, evidence-map.md]
   gates: []
   ```

**Deliverables**:
- ✓ Evidence extraction working
- ✓ Brief + evidence map generated
- ✓ Test: read papers → produce brief + map

**Dependencies**: 2.1 (need collected materials)

---

### 2.3 omr-research-plan (Merged Skill)

**Objective**: Judge evidence + plan research approach (merged from session 1)

**Implementation**:

1. **Input**: `evidence-map.md` (mandatory)
2. **Processing**:
   - Synthesize judgment from evidence
   - Plan research approach (priorities, timeline)
   - Gate A: Evidence sufficient for planning?

3. **Output**:
   - `judgment-summary.md` (main conclusion, confidence)
   - `research-plan.md` (priorities, timeline)

4. **Gate A**:
   ```yaml
   checks:
     - Evidence coverage adequate
     - Research question clear
     - Scope defined
   enforcement: user-confirm
   ```

**Deliverables**:
- ✓ Judgment + plan produced together
- ✓ Gate A enforced
- ✓ Test: evidence map → judgment + plan
- ✓ Test: gate fail → blocked

**Dependencies**: 2.2 (need evidence-map.md)

---

### 2.4 omr-decision

**Objective**: Architecture decision with alternatives + evidence refs

**Implementation**:

1. **Input**:
   - `evidence-map.md` (mandatory)
   - `judgment-summary.md` (optional)

2. **Processing**:
   - Define alternatives
   - Select best option
   - Link to evidence refs
   - Document risks

3. **Output**:
   - `architecture-decision.md` (decision_id, alternatives, selected, evidence_refs, risks)

4. **Gate B**:
   ```yaml
   checks:
     - Alternatives documented
     - Risks stated
     - Evidence refs valid
   enforcement: user-confirm
   ```

**Deliverables**:
- ✓ Decision produced
- ✓ Gate B enforced
- ✓ Test: evidence → decision with alternatives

**Dependencies**: 2.2 (evidence-map.md), optionally 2.3 (judgment-summary.md)

---

### 2.5 omr-evaluation

**Objective**: Experiment execution + evaluation report

**Implementation**:

1. **Input**:
   - `architecture-decision.md` (mandatory, except Experiment-First override)
   - `experiment-spec.md` (optional, generated if missing)

2. **Processing**:
   - Generate experiment spec (hypothesis, metrics, ground truth)
   - Build prototype in `src/`
   - Run evaluation
   - Produce report

3. **Output**:
   - `experiment-spec.md` (if not exists)
   - `evaluation-report.md` (hypothesis support, decision validation, traceability)

4. **Gate C**:
   ```yaml
   checks:
     - Metrics answer research question
     - Failure conditions explicit
     - Reproducible evaluation
   enforcement: user-confirm
   ```

5. **Pattern Override** (Experiment-First):
   ```yaml
   Experiment-First:
     contract_overrides:
       omr-evaluation:
         requires: []  # Allow without prior decision
   ```

**Deliverables**:
- ✓ Evaluation working
- ✓ Gate C enforced
- ✓ Pattern override supported
- ✓ Test: decision → evaluation
- ✓ Test: Experiment-First → evaluation without decision

**Dependencies**: 2.4 (decision), or pattern override

---

## Phase 3: Synthesis & Lifecycle (Weeks 7-8)

### 3.1 omr-synthesis (Configurable Output)

**Objective**: Configurable synthesis (survey/report/manuscript/brief)

**Implementation**:

1. **Input**:
   - `evaluation-report.md` OR `judgment-summary.md`
   - Mode: from pattern config OR user override (`--mode` flag)

2. **Modes**:
   - `survey`: `docs/survey/` (chapters)
   - `report`: `docs/report/` (structured findings)
   - `manuscript`: `docs/manuscript/` (publication-ready)
   - `brief`: `docs/brief/` (executive summary)

3. **Output**: Mode-specific directory with chapters/findings

4. **Gate D**:
   ```yaml
   checks:
     - Results traceable to hypotheses
     - Evidence boundaries stated
     - No over-claiming
   enforcement: user-confirm
   ```

**Deliverables**:
- ✓ 4 modes working
- ✓ Gate D enforced
- ✓ Test: evaluation → survey (Evidence-First default)
- ✓ Test: override → report

**Dependencies**: 2.5 (evaluation-report.md) or 2.3 (judgment-summary.md)

---

### 3.2 omr-wiki

**Objective**: Wiki generation from synthesis

**Implementation**:

1. **Input**: Any synthesis chapter OR judgment
2. **Processing**: Convert to wiki format with cross-refs
3. **Output**: `wiki/*.md`

**Deliverables**:
- ✓ Wiki generation
- ✓ Test: survey → wiki

**Dependencies**: 3.1 (synthesis) or 2.3 (judgment)

---

### 3.3 omr-idea-note

**Objective**: Capture speculative ideas

**Implementation**:

1. **Input**: None (available anytime)
2. **Output**: `docs/ideas/*.md` (idea note)

**Deliverables**:
- ✓ Idea note creation
- ✓ Test: idea → docs/ideas/

**Dependencies**: None (standalone)

---

### 3.4 omr-reconcile

**Objective**: Iteration support when new evidence arrives

**Implementation**:

1. **Trigger**: New material collected OR user-initiated
2. **Processing**:
   - Re-evaluate affected artifacts
   - Update downstream skills
   - Archive previous versions

3. **Output**:
   - Updated artifacts
   - `docs/archive/artifact-v1/` (previous versions)

4. **Skill Calls**:
   - Call `omr-evidence` (re-evaluate)
   - Call `omr-research-plan` (re-judge)
   - Call `omr-decision` (re-decide)

**Deliverables**:
- ✓ Reconciliation working
- ✓ Archiving preserved
- ✓ Test: new evidence → reconcile → update decision

**Dependencies**: All core skills (2.1-2.5)

---

## Phase 4: Pattern System (Weeks 9-10)

### 4.1 Pattern Definitions

**Objective**: Define 5 predefined patterns

**Implementation**:

1. **Pattern Schema** (`skills/schemas/pattern.schema.json`)
   ```json
   {
     "name": "pattern-name",
     "description": "...",
     "graph": {
       "entry_points": [],
       "nodes": [],
       "edges": []
     },
     "skill_gates": {},
     "contract_overrides": {},
     "recommendations": {
       "agency": "semi-automated",
       "estimated_time": "3-5 days",
       "synthesis_mode": "survey"
     }
   }
   ```

2. **5 Patterns**:
   - Evidence-First (rigorous, survey)
   - Idea-First (speculative, brief)
   - Decision-First (engineering, report)
   - Experiment-First (empirical, brief + override)
   - Rapid-Prototype (fastest, brief, no gates)

3. **Pattern Library** (`skills/patterns/`)
   - Store pattern definitions
   - User can save custom patterns

**Deliverables**:
- ✓ 5 patterns defined
- ✓ Pattern schema validated
- ✓ Test: select pattern → workflow follows graph

**Dependencies**: Phase 2 (need all core skills)

---

### 4.2 Pattern Emergence

**Objective**: Detect pattern from user actions + save as template

**Implementation**:

1. **Detection** (after 3+ skill invocations):
   - Track skill sequence
   - Match against existing patterns
   - Propose pattern name

2. **Save** (user confirms):
   - Save skill sequence as pattern
   - Store in `skills/patterns/user-defined/`

3. **Bootstrap Integration**:
   - NO pattern selection at bootstrap
   - Pattern detected after first action

**Deliverables**:
- ✓ Pattern detection working
- ✓ User-defined patterns saved
- ✓ Test: invoke skills → pattern detected → save

**Dependencies**: 4.1 (pattern definitions)

---

### 4.3 Reverse Skill Tree (Goal-First)

**Objective**: Plan shortest path to desired artifact

**Implementation**:

1. **Goal Input**: "Produce a survey"
2. **Backward Planning**:
   - Trace prerequisite chain from goal
   - Show: X skills between you and goal
   - Recommend: pattern based on goal

3. **UI**:
   ```
   > Goal: Produce a survey
   > Need to unlock:
     1. omr-collection ✓
     2. omr-evidence ○
     3. omr-research-plan ●
     ...
   
   > Recommended pattern: Evidence-First
   ```

**Deliverables**:
- ✓ Reverse tree working
- ✓ Goal-oriented planning
- ✓ Test: goal → shortest path

**Dependencies**: 1.3 (skill tree)

---

## Phase 5: Polish & Testing (Weeks 11-12)

### 5.1 End-to-End Testing

**Objective**: Test complete workflows for all 5 patterns

**Test Scenarios**:

1. **Evidence-First** (complete session from session 1):
   - Bootstrap → collection → evidence → research-plan → decision → evaluation → synthesis → wiki
   - All gates (A, B, C, D) enforced
   - Traceability: Q → DEC → EXP → Survey

2. **Idea-First**:
   - Idea-note → decision → evaluation → evidence → synthesis
   - Gate D only

3. **Decision-First**:
   - Decision → evidence → research-plan → evaluation → synthesis
   - Gates C, D

4. **Experiment-First**:
   - Evaluation (override: no decision) → evidence → decision → synthesis
   - Gate D only
   - Pattern override works

5. **Rapid-Prototype**:
   - Evaluation → evidence → decision → synthesis
   - No gates

6. **Reconciliation**:
   - New evidence → reconcile → update decision → archive v1

**Deliverables**:
- ✓ All patterns tested end-to-end
- ✓ Reconciliation tested
- ✓ No bugs found

**Dependencies**: All phases (complete system)

---

### 5.2 Documentation

**Objective**: User-facing documentation

**Implementation**:

1. **Getting Started**:
   - Onboarding example for first-time users
   - Goal-oriented tutorial (reverse tree)

2. **Skill Reference**:
   - 11 skills explained simply (Feynman technique from session 1)
   - Contract details + prerequisites

3. **Pattern Guide**:
   - 5 patterns explained
   - When to use each
   - How to define custom patterns

4. **Architecture Docs**:
   - Skill tree visualization
   - Gate system
   - Pattern emergence
   - Reconciliation workflow

5. **API Docs** (if skills expose CLI):
   - Command reference
   - Flag options

**Deliverables**:
- ✓ Getting started guide
- ✓ Skill reference
- ✓ Pattern guide
- ✓ Architecture docs

**Dependencies**: Phase 5.1 (need working system)

---

### 5.3 Gap Resolution

**Objective**: Address gaps identified in Feynman analysis (session 1)

**Gaps to Resolve**:

1. **Onboarding example**: Add "blank slate" example for first-time users (addressed in documentation)

2. **Multi-pattern concurrency**: 
   - Implement: parallel pattern support
   - Artifact isolation: pattern-specific subdirectories OR shared with conflict resolution
   - UI: spawn parallel pattern, track multiple trees

3. **Pattern sharing**:
   - Storage: `skills/patterns/user-defined/`
   - Import/export: `pattern-export.json`
   - Library: central pattern repository (future)

4. **Gate failure handling**:
   - Explicit workflow: gate fails → options (revise artifact, override with fully-automated mode, abort)
   - User choice preserved

**Deliverables**:
- ✓ Onboarding example complete
- ✓ Multi-pattern concurrency working (if prioritized)
- ✓ Pattern import/export (if prioritized)
- ✓ Gate failure workflow documented

**Dependencies**: 5.2 (documentation)

---

## Implementation Roadmap Summary

| Phase | Weeks | Key Deliverables | Dependencies |
|-------|-------|------------------|--------------|
| **1. Foundation** | 1-3 | Contract system, Workspace, Skill tree | None |
| **2. Core Skills** | 4-6 | 5 core skills (collection, evidence, research-plan, decision, evaluation) + gates | Phase 1 |
| **3. Synthesis & Lifecycle** | 7-8 | Synthesis (4 modes), Wiki, Idea-note, Reconcile | Phase 2 |
| **4. Pattern System** | 9-10 | 5 patterns, Pattern emergence, Reverse tree | Phase 2 |
| **5. Polish & Testing** | 11-12 | End-to-end testing, Documentation, Gap resolution | All phases |

**Total**: 8-12 weeks (phased, parallel where possible)

---

## Critical Design Decisions (From Brainstorming Sessions)

### Session 1 Decisions (Polishing Design)

1. **Skill Composition**: Local graphs + shared contracts (not strict global graph)
2. **Pattern Selection**: After first action (not at bootstrap)
3. **Gate Enforcement**: Skill-level (not pattern-level)
4. **Archive Strategy**: Auto + manual trigger
5. **Skill Granularity**: 11 skills (merged judgment+plan)
6. **Pattern Emergence**: Save from practice, not pre-selected
7. **Reverse Tree**: Goal-first planning

### Session 2 Decisions (omr-collection Architecture)

1. **Passive Reception**: User decides sources (hybrid confirmation for search)
2. **Minimal Parsing**: Format extraction + metadata only (no semantic analysis)
3. **Handler Architecture**: 4 core handlers, no extensibility (Generic Web fallback)
4. **Artifact Structure**: AI-optimized (DOI/hash naming), not human-browseable
5. **Search Integration**: Special input (not separate skill), hybrid confirmation
6. **Configurable Depth**: Override flags for pattern compatibility (Experiment-First needs datasets)
7. **Error Handling**: Fail gracefully + retry + fallback + error artifacts

---

## Next Steps

### Immediate Actions (This Week)

1. **Create Contract Schema** (`skills/schemas/contract.schema.json`)
2. **Define Workspace Structure** (directory layout)
3. **Implement Bootstrap Skill** (minimal: create structure)
4. **Start Dependency Resolver** (Python script)
5. **Design Skill Tree State** (`skills/tree-state.json`)

### Week 2-3 Goals

1. **Complete Contract System** (11 contracts + resolver)
2. **Bootstrap Working** (create workspace + CLAUDE.md)
3. **Skill Tree Visualization** (ASCII renderer)
4. **Start omr-collection** (Phase 2.1a: core handlers)

### Week 4-6 Goals

1. **omr-collection Complete** (all 4 phases from session 2)
2. **omr-evidence Working**
3. **omr-research-plan Working** (merged skill + Gate A)
4. **omr-decision Working** (Gate B)
5. **omr-evaluation Working** (Gate C + pattern override)

### Week 7-12 Goals

Follow Phase 3-5 roadmap above.

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| **Complexity creep** | Stick to First Principles minimalism (session 2 philosophy) |
| **Pattern override bugs** | Validate pattern definitions against contracts before execution |
| **Search integration complexity** | Hybrid confirmation preserves passive reception (session 2 decision) |
| **Gate enforcement too rigid** | Configurable agency (semi-automated vs fully-automated) |
| **Skill tree visualization unclear** | Reverse view + forward view toggle (session 1 decision) |
| **Reconciliation cascade** | Limit to direct downstream skills, not full re-run |

---

## Success Criteria

1. ✓ All 11 skills working with contracts enforced
2. ✓ Skill tree visualization shows progress correctly
3. ✓ All 5 patterns tested end-to-end
4. ✓ Pattern emergence working (detect + save)
5. ✓ Reverse skill tree working (goal-first planning)
6. ✓ Reconciliation updates downstream correctly
7. ✓ Gates enforced at skill-level
8. ✓ omr-collection search integration working (hybrid confirmation)
9. ✓ Configurable synthesis modes (survey/report/manuscript/brief)
10. ✓ Documentation complete (getting started, skill reference, pattern guide)

---

## Metrics

| Metric | Target |
|--------|--------|
| Skills implemented | 11/11 |
| Patterns working | 5/5 |
| Gates enforced | 4/4 |
| End-to-end test pass rate | 100% |
| Pattern emergence accuracy | >80% match |
| Documentation coverage | All skills + patterns documented |
| User onboarding time | <30 minutes to first artifact |

---

## Open Questions (Deferred to Implementation)

1. **Concurrency**: Sequential vs parallel skill execution (Phase 5)
2. **Progress reporting**: Real-time status during long collections (Phase 5)
3. **Deduplication**: Duplicate URL/paper handling (Phase 5)
4. **Pattern library location**: Central repository vs project-local (Phase 5)
5. **Multi-pattern concurrency details**: Artifact isolation vs sharing (Phase 5.3)

---

## Conclusion

This plan synthesizes the comprehensive design decisions from both brainstorming sessions into a concrete, phased implementation roadmap. The core philosophy remains: skills are composable ingredients, patterns emerge from practice, dependencies are artifact-bound, and minimalism guides implementation.

**Key Innovation**: Pattern emergence + reverse skill tree + skill-level gates = flexible yet rigorous research system.

**Ready to Start**: Phase 1 (Foundation) can begin immediately.