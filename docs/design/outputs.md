# Dual Output Model

## Documents (Distilled Knowledge)

**Synthesis modes** (configurable output types):

| Mode | Output | Structure | Depth | Evidence Boundaries |
|------|--------|-----------|-------|---------------------|
| `survey` | `docs/survey/*.md` | Chapters (01-07) | Comprehensive | Explicit per section |
| `report` | `docs/report/*.md` | Structured findings | Medium | Key findings only |
| `manuscript` | `docs/manuscript/*.md` | Paper format | Deep | Academic rigor |
| `brief` | `docs/brief/*.md` | Executive summary | Minimal | Top-level only |

**Plans:** Formal artifacts (brief, evidence-map, decisions, specs)
**Archive:** Historical versions, deprecated materials

## Wiki (Living Knowledge Base)

- **Concept pages**: Interlinked, continuously updated
- **Auto-sync**: Reflects latest survey + evaluation findings
- **Quick reference**: Condensed for rapid lookup

**Wiki structure:**
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

**Wiki pages link back to source documents.**

## Synthesis Skill Details

**Purpose:** Write authoritative findings in configurable output format.

**Trigger:** `/omr-synthesis [--mode <mode>]`

**Inputs:**
- `report-{id}.md` OR `judgment-{id}.md` (required)
- Pattern config (implicit): Default synthesis mode

**Behavior:**
1. Read evaluation-report + architecture-decision + evidence-map
2. Determine mode (pattern config or `--mode` flag)
3. Generate chapters/sections based on mode
4. Ensure traceability: link every claim
5. Apply evidence boundaries
6. Present Gate D review
7. If gate passed: unlock `omr-wiki`

**Gate D checks:**
- [ ] Results traceable to hypotheses
- [ ] Evidence boundaries stated
- [ ] No over-claiming
- [ ] Cross-references valid

## Wiki Skill Details

**Purpose:** Generate living knowledge base from synthesis findings.

**Trigger:** `/omr-wiki`

**Inputs:**
- Synthesis chapters OR judgment-summary (required)

**Behavior:**
1. Read synthesis chapters
2. Extract key concepts
3. Generate wiki pages per concept
4. Create interlinks
5. Link back to source documents
6. Generate `wiki/README.md` index

**No gates.**

## Cross-Reference Format

```markdown
This approach was validated in [EXP-001](../plans/experiment-spec.md#exp-001),
supporting Decision [DEC-005](../plans/architecture-decision.md#dec-005).

Evidence: [Paper X](../index/papers-index.md#paper-x) suggests... (not proves)
```

## Traceability Matrix

Auto-generated at `docs/index/traceability-matrix.md`:

| Question | Evidence | Decision | Experiment | Survey Section |
|----------|----------|----------|-------------|----------------|
| Q-001 | Paper A, B | DEC-003 | EXP-002 | §2.3 Formation |
