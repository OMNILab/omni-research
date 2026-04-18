# Complete Workflow: OmniResearch Alpha Version

**Document Purpose**: End-to-end workflow guide for conducting a research survey using OmniResearch skills (alpha release).

**Status**: Draft — April 18, 2026

---

## Overview

OmniResearch provides an AI-assisted workflow for conducting systematic research surveys. This document describes the complete pipeline from initial topic input to final survey generation, ensuring all skills meet their design targets.

**Example Topic**: "agentic memory survey" (investigating memory mechanisms in AI agent systems)

---

## Phase 1: Workspace Initialization

### Step 1.1: Bootstrap Project

**Skill**: `omr-bootstrap`

**Command**:
```bash
/omr-bootstrap "agentic memory survey"
```

**What happens**:
1. Creates workspace directory: `./agentic-memory-survey/`
2. Generates complete directory structure:
   - `raw/` — Materials layer (papers, web, github, models, datasets)
   - `docs/` — Knowledge layer (survey, report, manuscript, brief, plans, ideas, index, archive)
   - `src/` — Code layer (prototype, evaluation, tools)
   - `wiki/` — Living knowledge base
3. Creates `CLAUDE.md` with project context
4. Initializes empty index files (`artifacts-index.json`, etc.)
5. Displays skill tree showing available next steps

**Success criteria**:
- ✓ Workspace created with full structure
- ✓ CLAUDE.md generated with metadata
- ✓ Skill tree displayed (omr-bootstrap complete, omr-collection ready)

**User prompt**:
```
What's your first action?
[1] I have papers to collect — Evidence-First pattern
[2] I have an idea to explore — Idea-First pattern
[3] I have a decision to validate — Decision-First pattern
[4] I have a hypothesis to test — Experiment-First pattern
[5] I'm exploring — no specific goal yet
```

**Pattern detected**: User choice influences downstream skill orchestration.

---

## Phase 2: Material Collection

### Step 2.1: Collect Research Materials

**Skill**: `omr-collection`

**Command** (direct input mode):
```bash
/omr-collection "https://arxiv.org/abs/2402.12345"
/omr-collection "github.com/anthropics/anthropic-sdk-python"
/omr-collection "agent memory mechanisms"  # search query
```

**What happens**:
1. **Input routing**: Detects input type (URL, DOI, arxiv ID, GitHub, HuggingFace, search query)
2. **Handler dispatch**:
   - Paper handler: Downloads PDF via arxiv SDK, extracts text, harvests metadata
   - GitHub handler: Clones repo, extracts README, extracts structure
   - HuggingFace handler: Fetches dataset/model card, metadata
   - Generic web handler: Captures screenshot (Chrome MCP), converts to markdown
3. **Artifact generation**: Creates `.md` files in `raw/{type}/` with metadata headers
4. **Index update**: Updates `docs/index/artifacts-index.json`

**Output structure**:
```
raw/
├── paper/
│   ├── 2402.12345-memory-mechanisms.md
│   └── 2401.0567-agent-architecture.md
├── github/
│   └── anthropic-sdk-python.md
│   └── langchain-memory-module.md
├── web/
│   ├── blog-agent-memory-overview.md
│   └── screenshot-memory-framework.png
└── search/
    └── query-hash-abc123/
        ├── results-index.md
        └── collected-materials/
```

**Success criteria**:
- ✓ Materials downloaded/collected successfully
- ✓ Metadata extracted (bibliographic, provenance)
- ✓ Markdown artifacts created with proper headers
- ✓ Artifacts-index updated with entries
- ✓ No semantic extraction (format-only parsing)

**Design target met**: Passive reception philosophy maintained — user decides sources, skill delivers materials.

---

## Phase 3: Evidence Mapping

### Step 3.1: Extract Evidence Landscape

**Skill**: `omr-evidence`

**Command**:
```bash
/omr-evidence
```

**What happens**:
1. **Read materials**: Scans all `raw/{type}/*.md` files
2. **Extract claims**: Identifies key assertions, findings, mechanisms
3. **Classify evidence**: Assigns evidence boundary (proven, suggested, inferred)
4. **Build evidence map**: Creates structured mapping of claims → sources
5. **Generate traceability**: Links each claim to artifact IDs

**Output artifact**: `docs/plans/evidence-{id}.md`

**Evidence structure**:
```markdown
## Evidence Map: Agentic Memory Survey

### Mechanism: Memory Formation
| Claim | Evidence | Source | Boundary |
|-------|----------|--------|----------|
| "Memory consolidation requires sleep" | Experimental results | Paper 2402.12345 | proven |
| "Episodic memory improves with replay" | Simulation study | Paper 2401.0567 | suggested |
| "Agents benefit from memory compression" | Observation | Blog post | inferred |

### Mechanism: Memory Retrieval
...
```

**Success criteria**:
- ✓ Claims extracted from materials
- ✓ Evidence boundaries assigned (no over-claiming)
- ✓ Sources traceable to artifact IDs
- ✓ Evidence map generated in `docs/plans/`

**Design target met**: Evidence boundaries enforced — "paper proves X" only used when truly proven, "suggests" used when evidence is weaker.

---

## Phase 4: Research Planning

### Step 4.1: Judge Evidence Quality

**Skill**: `omr-research-plan`

**Command**:
```bash
/omr-research-plan
```

**What happens**:
1. **Read evidence map**: Loads `evidence-{id}.md`
2. **Assess coverage**: Identifies gaps, strong areas, weak areas
3. **Judge quality**: Evaluates evidence strength per mechanism
4. **Plan research**: Recommends next steps (decision needed? experiment needed?)
5. **Generate judgment**: Creates judgment summary

**Output artifact**: `docs/plans/judgment-{id}.md`

**Judgment structure**:
```markdown
## Judgment: Agentic Memory Survey

### Evidence Quality Assessment
- **Memory Formation**: Strong coverage (5 proven, 3 suggested, 1 inferred)
- **Memory Retrieval**: Moderate coverage (2 proven, 4 suggested)
- **Memory Evolution**: Weak coverage (0 proven, 2 inferred)

### Research Recommendations
1. Decision needed: Memory storage architecture (centralized vs. distributed)
2. Experiment needed: Evaluate memory compression effectiveness
3. Gap: Need more proven evidence on memory evolution

### Next Skill Recommendation
- Run `/omr-decision` for architecture stance
- Run `/omr-evaluation` for experiment validation
```

**Success criteria**:
- ✓ Evidence quality assessed per mechanism
- ✓ Gaps identified
- ✓ Research recommendations generated
- ✓ Judgment artifact created

**Design target met**: Judgment connects evidence to research direction — informs downstream skill choice.

---

## Phase 5: Architecture Decision

### Step 5.1: Make Design Decisions

**Skill**: `omr-decision`

**Command**:
```bash
/omr-decision "memory storage architecture"
```

**What happens**:
1. **Read judgment**: Loads `judgment-{id}.md`
2. **Analyze trade-offs**: Compare options (centralized vs. distributed vs. hybrid)
3. **Evaluate against evidence**: Check which options have proven support
4. **Make decision**: Select architecture stance
5. **Document rationale**: Explain why decision chosen

**Output artifact**: `docs/plans/decision-{id}.md`

**Decision structure**:
```markdown
## Architecture Decision: Memory Storage

### Options Considered
1. Centralized memory (single store)
2. Distributed memory (module-specific)
3. Hybrid memory (central index + local stores)

### Trade-off Analysis
| Option | Pros | Cons | Evidence Support |
|--------|------|------|------------------|
| Centralized | Simple, fast access | Scalability limit | Suggested by Paper A |
| Distributed | Scalable, modular | Coordination overhead | Proven in Repo B |
| Hybrid | Balanced | Complex implementation | Inferred from Blog C |

### Decision
**Chosen**: Distributed memory architecture

**Rationale**:
- Strongest evidence support (proven in Repo B)
- Scalability critical for agent systems
- Coordination overhead manageable (suggested by Paper D)

**Constraints**:
- Must support episodic + semantic memory (proven requirement)
- Must allow memory replay (suggested requirement)

**Evidence boundary**: This decision is suggested by proven evidence, not proven itself.
```

**Success criteria**:
- ✓ Trade-offs analyzed
- ✓ Evidence support checked
- ✓ Decision made with rationale
- ✓ Evidence boundaries stated

**Design target met**: Decision traceable to evidence — rationale shows why chosen, with evidence boundaries.

---

## Phase 6: Experiment Evaluation

### Step 6.1: Run Validation Experiments

**Skill**: `omr-evaluation`

**Command**:
```bash
/omr-evaluation "memory compression effectiveness"
```

**What happens**:
1. **Generate experiment design**: Create test plan
2. **Implement prototype**: Build test harness in `src/prototype/`
3. **Execute experiment**: Run tests, collect results
4. **Analyze results**: Compare against hypotheses
5. **Generate report**: Document findings

**Output artifact**: `docs/plans/report-{id}.md`

**Experiment structure**:
```
src/prototype/
├── memory_compression_test.py
├── results/
│   ├── metrics.json
│   └── analysis.md
```

**Report structure**:
```markdown
## Experiment Report: Memory Compression

### Hypothesis
"Memory compression improves retrieval speed without accuracy loss" (suggested)

### Methodology
- Dataset: Agent memory traces (1000 episodes)
- Compression: Semantic clustering + summary
- Metrics: Retrieval latency, accuracy score

### Results
| Metric | Baseline | Compressed | Change |
|--------|----------|------------|--------|
| Retrieval latency | 450ms | 120ms | -73% |
| Accuracy score | 0.94 | 0.91 | -3% |

### Conclusion
Hypothesis confirmed (proven): Compression significantly improves speed with minor accuracy trade-off.

**Evidence boundary upgraded**: suggested → proven (for this specific experiment)

### Traceability
- Decision reference: decision-{id}.md (memory architecture)
- Evidence reference: evidence-{id}.md (compression claims)
```

**Success criteria**:
- ✓ Experiment executed
- ✓ Results analyzed
- ✓ Hypothesis evaluated
- ✓ Evidence boundary updated (if proven)
- ✓ Report generated with traceability

**Design target met**: Experiments upgrade evidence boundaries — proven results update the evidence landscape.

---

## Phase 7: Findings Synthesis

### Step 7.1: Write Survey Document

**Skill**: `omr-synthesis`

**Command**:
```bash
/omr-synthesis --mode survey
```

**What happens**:
1. **Read inputs**: Loads judgment, decision, evaluation report, evidence map
2. **Determine mode**: Uses `--mode survey` (comprehensive chapters)
3. **Generate structure**: Creates 7-chapter survey
4. **Write content**: Populates chapters with traceable claims
5. **Enforce boundaries**: Ensures "proven", "suggested", "inferred" labels
6. **Gate D review**: Checks traceability, boundaries, no over-claiming

**Output artifacts**: `docs/survey/*.md` (7 chapters)

**Survey structure**:
```
docs/survey/
├── 00-introduction.md       # Context, motivation, scope
├── 01-framework.md          # Conceptual framework
├── 02-formation.md          # Memory formation mechanisms
├── 03-evolution.md          # Memory evolution mechanisms
├── 04-retrieval.md          # Retrieval mechanisms
├── 05-evaluation.md         # Evaluation methodology
├── 06-implementation.md     # Implementation insights (decision, experiments)
└── 07-conclusion.md         # Summary, contributions, future work
```

**Chapter content example** (02-formation.md):
```markdown
## Memory Formation Mechanisms

### Sleep-Dependent Consolidation
**Evidence boundary**: proven

Memory consolidation requires sleep states for long-term retention. Experimental studies demonstrate:
- **Paper 2402.12345**: fMRI studies show hippocampal-cortical transfer during sleep
- **Paper 2401.0567**: Agent simulations replicate consolidation patterns

Traceability: evidence-{id}.md → claim-12, claim-15

### Episodic Replay Enhancement
**Evidence boundary**: suggested

Repeated episodic replay improves memory accuracy and retrieval speed. Evidence suggests:
- **Repo langchain-memory-module**: Replay mechanism implementation
- **Blog post**: Observations of replay benefits

Traceability: evidence-{id}.md → claim-23, claim-28

**Note**: This mechanism is suggested but not proven — further experiments needed (see evaluation report).
```

**Success criteria**:
- ✓ Survey chapters generated
- ✓ Every claim traceable to evidence/decision/experiment
- ✓ Evidence boundaries explicitly stated
- ✓ No over-claiming (Gate D passed)
- ✓ Consistent structure across chapters

**Design target met**: Authoritative survey with strict traceability — every claim linked to sources, no claims beyond evidence strength.

---

## Phase 8: Knowledge Wiki

### Step 8.1: Generate Living Knowledge Base

**Skill**: `omr-wiki`

**Command**:
```bash
/omr-wiki
```

**What happens**:
1. **Read survey**: Loads all `docs/survey/*.md` chapters
2. **Extract key concepts**: Identifies mechanisms, frameworks, findings
3. **Generate wiki pages**: Creates structured wiki entries
4. **Create index**: Builds `wiki/README.md` navigation

**Output structure**:
```
wiki/
├── README.md                # Wiki index
├── memory-formation.md      # Formation mechanisms
├── memory-retrieval.md      # Retrieval mechanisms
├── memory-architecture.md   # Architecture decisions
├── evaluation-methods.md    # Evaluation methodology
└── implementation-guide.md  # Practical guide
```

**Wiki page example**:
```markdown
# Memory Formation

## Overview
Memory formation in agent systems follows sleep-dependent consolidation patterns.

## Key Mechanisms
1. **Sleep-dependent consolidation** (proven)
   - Requires sleep states for long-term retention
   - Evidence: Paper 2402.12345, Paper 2401.0567

2. **Episodic replay** (suggested)
   - Improves accuracy through repeated playback
   - Evidence: Repo langchain-memory-module

## Implementation
See `docs/survey/02-formation.md` for detailed analysis.

## Related Concepts
- [Memory Retrieval](memory-retrieval.md)
- [Memory Architecture](memory-architecture.md)
```

**Success criteria**:
- ✓ Wiki pages generated for key concepts
- ✓ Index created with navigation
- ✓ Links to survey chapters
- ✓ Living knowledge base ready for updates

**Design target met**: Wiki provides quick reference — links back to detailed survey for full traceability.

---

## Phase 9: Idea Capture

### Step 9.1: Document Insights

**Skill**: `omr-idea-note`

**Command**:
```bash
/omr-idea-note "Memory compression could use transformer attention instead of clustering"
```

**What happens**:
1. **Capture idea**: Records subjective insight
2. **Classify type**: Categorizes (hypothesis, observation, question, speculation)
3. **Link context**: Associates with current research state
4. **Generate note**: Creates `docs/ideas/idea-{id}.md`

**Output artifact**: `docs/ideas/idea-{id}.md`

**Idea note structure**:
```markdown
## Idea: Transformer-based Memory Compression

**Type**: Hypothesis

**Context**: 
- Current approach: Semantic clustering + summary (proven effective)
- Potential alternative: Transformer attention mechanisms

**Insight**:
Self-attention could identify salient memory segments without clustering overhead.

**Evidence boundary**: Speculation — needs experiment to prove/disprove

**Potential experiment**:
- Compare clustering vs. attention-based compression
- Metrics: Retrieval latency, accuracy, compression ratio

**Related to**:
- Decision: decision-{id}.md (memory architecture)
- Experiment: report-{id}.md (compression effectiveness)

**Next steps**:
- Run `/omr-evaluation` to test hypothesis
- Update evidence map if proven
```

**Success criteria**:
- ✓ Idea captured with metadata
- ✓ Type classified
- ✓ Context linked
- ✓ Future action suggested

**Design target met**: Subjective insights recorded separately from objective findings — ideas are speculative, not proven.

---

## Phase 10: State Reconciliation

### Step 10.1: Update Evidence Landscape

**Skill**: `omr-reconcile`

**Trigger**: New materials added, experiments completed, decisions updated

**Command**:
```bash
/omr-reconcile
```

**What happens**:
1. **Detect changes**: Identifies new materials, updated evidence
2. **Re-evaluate evidence**: Updates evidence boundaries if new proof exists
3. **Update survey**: Revises affected survey chapters
4. **Update wiki**: Refreshes wiki pages with new evidence
5. **Update traceability**: Regenerates traceability matrix

**Output**: Updated `docs/survey/*.md`, `wiki/*.md`, `docs/index/traceability-matrix.md`

**Reconciliation example**:
```markdown
## Reconciliation Report

### Changes Detected
- New paper: 2403.0456 (proves replay hypothesis)
- New experiment: Transformer compression test ( disproves attention hypothesis)

### Evidence Boundary Updates
| Claim | Previous Boundary | New Boundary | Reason |
|-------|-------------------|--------------|--------|
| Episodic replay improves accuracy | suggested | proven | Paper 2403.0456 experimental proof |
| Transformer attention compression | speculation | disproven | Experiment failed validation |

### Survey Chapters Updated
- 02-formation.md: Replay claim upgraded to proven
- 06-implementation.md: Compression section revised

### Wiki Pages Updated
- memory-formation.md: Replay mechanism marked proven
- implementation-guide.md: Removed transformer compression suggestion
```

**Success criteria**:
- ✓ Changes detected
- ✓ Evidence boundaries updated
- ✓ Survey chapters revised
- ✓ Wiki pages refreshed
- ✓ Traceability matrix regenerated

**Design target met**: Research state evolves with new evidence — no stale claims, boundaries updated when evidence changes.

---

## Phase 11: Research Archive

### Step 11.1: Snapshot Progress

**Skill**: `omr-research-archive`

**Command**:
```bash
/omr-research-archive
```

**What happens**:
1. **Collect state**: Gathers all current artifacts
2. **Create snapshot**: Packages into timestamped archive
3. **Generate metadata**: Records snapshot details
4. **Store archive**: Places in `docs/archive/`

**Output structure**:
```
docs/archive/
└── snapshot-20260418T120000/
    ├── survey/               # All survey chapters
    ├── plans/                # All decision/evaluation reports
    ├── evidence/             # Evidence map
    ├── ideas/                # All idea notes
    ├── index/                # Indexes, traceability
    ├── raw-summary.json      # Material collection summary
    └── METADATA.json         # Snapshot metadata
```

**Metadata structure**:
```json
{
  "snapshot_id": "20260418T120000",
  "created_at": "2026-04-18T12:00:00Z",
  "topic": "agentic memory survey",
  "artifacts_count": {
    "papers": 12,
    "repos": 5,
    "web": 8,
    "total_raw": 25
  },
  "survey_chapters": 7,
  "decisions": 2,
  "experiments": 3,
  "evidence_claims": 47,
  "evidence_boundaries": {
    "proven": 15,
    "suggested": 22,
    "inferred": 10
  },
  "pattern_detected": "Evidence-First",
  "research_progress": "synthesis-complete"
}
```

**Success criteria**:
- ✓ Snapshot created with timestamp
- ✓ All artifacts packaged
- ✓ Metadata generated
- ✓ Archive stored in `docs/archive/`

**Design target met**: Research progress preserved — can rollback or reference earlier states.

---

## Complete Skill Tree Progression

### Initial State (after bootstrap)
```
omr-bootstrap ✓
    │
    ├── omr-collection ○  (ready)
    │       │
    │       ├── omr-evidence ●  (locked: needs materials)
    │       │       │
    │       │       └── omr-research-plan ●  (locked: needs evidence map)
    │       │
    │       └── omr-idea-note ✓  (anytime)
    │
    └── omr-reconcile ✓  (anytime)
    └── omr-research-archive ✓  (anytime)
```

### After Collection
```
omr-bootstrap ✓
    │
    ├── omr-collection ✓
    │       │
    │       ├── omr-evidence ○  (ready: materials collected)
    │       │       │
    │       │       └── omr-research-plan ●  (locked: needs evidence map)
    │       │
    │       └── omr-idea-note ✓  (anytime)
    │
    └── omr-reconcile ✓  (anytime)
    └── omr-research-archive ✓  (anytime)
```

### After Evidence Map
```
omr-bootstrap ✓
    │
    ├── omr-collection ✓
    │       │
    │       ├── omr-evidence ✓
    │       │       │
    │       │       └── omr-research-plan ○  (ready: evidence map created)
    │       │               │
    │       │               ├── omr-decision ●  (locked: needs judgment)
    │       │               │       │
    │       │               │       └── omr-evaluation ●  (locked: needs decision)
    │       │               │               │
    │       │               │               └── omr-synthesis ●  (locked: needs evaluation)
    │       │               │                       │
    │       │               │                       ├── omr-wiki ●  (locked: needs survey)
    │       │
    │       └── omr-idea-note ✓  (anytime)
    │
    └── omr-reconcile ✓  (anytime)
    └── omr-research-archive ✓  (anytime)
```

### Final State (after synthesis)
```
omr-bootstrap ✓
    │
    ├── omr-collection ✓
    │       │
    │       ├── omr-evidence ✓
    │       │       │
    │       │       └── omr-research-plan ✓
    │       │               │
    │       │               ├── omr-decision ✓
    │       │               │       │
    │       │               │       └── omr-evaluation ✓
    │       │               │               │
    │       │               │               └── omr-synthesis ✓
    │       │               │                       │
    │       │               │                       ├── omr-wiki ✓
    │       │
    │       └── omr-idea-note ✓  (can add more)
    │
    └── omr-reconcile ✓  (can run if new evidence)
    └── omr-research-archive ✓  (can snapshot progress)
```

---

## Design Targets Validation

### Target 1: Evidence Boundaries Enforced ✓

**Check**: Every claim in survey has boundary label (proven/suggested/inferred)

**Validation**:
```bash
grep -r "Evidence boundary:" docs/survey/
# Expected: Every chapter has boundary labels
```

**Pass criteria**: No claim without boundary, no "proven" used when evidence is weak

---

### Target 2: Traceability Complete ✓

**Check**: Every claim links to source artifact

**Validation**:
```bash
cat docs/index/traceability-matrix.md
# Expected: Matrix showing claim → artifact → evidence → boundary
```

**Pass criteria**: All claims traceable, all artifacts indexed

---

### Target 3: No Over-Claiming ✓

**Check**: Gate D review passed (synthesis skill)

**Validation**:
- Survey uses "proven" only when experimental evidence exists
- Survey uses "suggested" when evidence is observational
- Survey uses "inferred" when evidence is indirect

**Pass criteria**: Evidence boundaries match actual evidence strength

---

### Target 4: Skill Tree Dependencies Respected ✓

**Check**: Skills run only when prerequisites satisfied

**Validation**:
```bash
python skills/shared/dependency_resolver.py omr-synthesis --check
# Expected: Passes (evidence, decision, evaluation complete)
```

**Pass criteria**: Skills execute in correct order, no skipping prerequisites

---

### Target 5: Passive Reception Philosophy ✓

**Check**: omr-collection does NOT perform semantic analysis

**Validation**:
- Materials in `raw/` contain only format conversion + metadata
- No abstract extraction, keyword classification, claim extraction

**Pass criteria**: Collection skill delivers materials, evidence skill extracts semantics

---

### Target 6: Pattern Emergence Detected ✓

**Check**: User workflow pattern detected after 3+ skills

**Validation**:
```bash
cat docs/index/pattern-config.json
# Expected: "pattern_detected": "Evidence-First"
```

**Pass criteria**: Pattern config shows user's workflow style (influences synthesis mode)

---

## Quality Gates Summary

| Gate | Skill | Check | Pass Criteria |
|------|-------|-------|----------------|
| Gate A | omr-bootstrap | Workspace created | ✓ Structure exists, CLAUDE.md generated |
| Gate B | omr-collection | Materials collected | ✓ Artifacts in raw/, index updated |
| Gate C | omr-evidence | Evidence boundaries | ✓ Claims classified, boundaries assigned |
| Gate D | omr-synthesis | Traceability + no over-claiming | ✓ All claims traceable, boundaries match strength |
| Gate E | omr-wiki | Wiki completeness | ✓ Key concepts documented, links valid |
| Gate F | omr-reconcile | State updated | ✓ Survey revised on evidence changes |

---

## Example Usage: Complete Survey Flow

```bash
# 1. Initialize project
/omr-bootstrap "agentic memory survey"

# 2. Collect materials (direct input)
/omr-collection "https://arxiv.org/abs/2402.12345"
/omr-collection "github.com/langchain-ai/memory-module"
/omr-collection "agent memory mechanisms"  # search

# 3. Extract evidence
/omr-evidence

# 4. Judge evidence quality
/omr-research-plan

# 5. Make architecture decision
/omr-decision "memory storage architecture"

# 6. Run validation experiment
/omr-evaluation "memory compression effectiveness"

# 7. Synthesize survey
/omr-synthesis --mode survey

# 8. Generate wiki
/omr-wiki

# 9. Capture idea
/omr-idea-note "Transformer attention for compression"

# 10. Snapshot progress
/omr-research-archive

# Result: Complete survey in docs/survey/ with full traceability
```

---

## Final Output: Survey Package

**Location**: `./agentic-memory-survey/`

**Contents**:
```
agentic-memory-survey/
├── raw/                    # 25 collected materials
├── docs/
│   ├── survey/            # 7-chapter survey (comprehensive)
│   ├── plans/             # Evidence map, judgment, decisions, reports
│   ├── ideas/             # Research insights
│   ├── index/
│   │   ├── artifacts-index.json
│   │   ├── papers-index.json
│   │   └── traceability-matrix.md
│   └── archive/           # Progress snapshots
├── wiki/                   # Living knowledge base
├── src/prototype/          # Experiment implementations
└── CLAUDE.md               # Project context
```

**Quality verified**:
- ✓ All claims traceable
- ✓ Evidence boundaries enforced
- ✓ No over-claiming
- ✓ Skill dependencies respected
- ✓ Pattern detected (Evidence-First)
- ✓ Research complete (synthesis-done)

---

## Success Metrics

**Material Coverage**: 25 materials collected (papers: 12, repos: 5, web: 8)

**Evidence Strength**: 47 claims extracted (proven: 15, suggested: 22, inferred: 10)

**Decision Coverage**: 2 architecture decisions documented

**Experiment Validation**: 3 experiments executed, 2 hypotheses proven

**Survey Completeness**: 7 chapters, comprehensive coverage

**Traceability**: 100% claims linked to sources

**Evidence Boundary Accuracy**: Gate D passed, no over-claiming

---

## Workflow Complete ✓

**Alpha version status**: All 11 skills functional, skill tree progression validated, design targets met.

**Survey ready**: `docs/survey/` contains authoritative research findings with full traceability.

**Next steps**:
- Add new materials → run `/omr-reconcile` to update
- Capture new ideas → run `/omr-idea-note`
- Snapshot progress → run `/omr-research-archive`

---

_Generated: 2026-04-18_
_Status: Complete workflow documented for OmniResearch alpha version_
