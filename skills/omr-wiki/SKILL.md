---
name: omr-wiki
description: Generate living knowledge base from synthesis findings. Extracts key concepts from survey/report/manuscript/brief and creates interlinked wiki pages for quick reference. Auto-generates wiki index with navigation. Links back to source documents for deep dives. Continuously updated as new findings emerge. Use when user wants to "create wiki", "generate concept pages", or after synthesis completion.
---

# omr-wiki: Generate Living Knowledge Base

## Purpose

Generate a living, interlinked knowledge base from synthesis findings. This skill transforms static synthesis documents into dynamic wiki pages that provide quick reference while maintaining deep links back to authoritative source documents.

## Trigger

```
/omr-wiki
```

**No arguments required** — operates on synthesis chapters or judgment summary

**Prerequisites:**
- Synthesis chapters OR judgment summary (required)
- If neither: Error "Run `/omr-synthesis` first."

**Automatic trigger:**
- After `omr-synthesis` Gate D passed, user may accept auto-trigger

## What This Skill Does

### 1. Read Synthesis Documents

**Required:**
- Synthesis chapters: `docs/survey/*.md`, `docs/report/*.md`, `docs/manuscript/*.md`, `docs/brief/*.md`
- OR Judgment summary: `docs/plans/judgment-{id}.md`

**If synthesis exists:**
- Read all chapter files
- Extract key concepts from each chapter
- Note interlinks between concepts

**If judgment only (no synthesis):**
- Read judgment summary
- Extract key concepts from main conclusion
- Note evidence references

**If neither:**
- Error: "No synthesis or judgment found. Run `/omr-synthesis` first."
- Do not proceed

### 2. Extract Key Concepts

**Concept extraction process:**

1. **Scan chapter titles:**
   - Chapter 2: "Formation" → Concept: Memory Formation
   - Chapter 3: "Evolution" → Concept: Memory Evolution
   - Chapter 4: "Retrieval" → Concept: Memory Retrieval

2. **Scan key findings sections:**
   - "Importance threshold" → Concept: Importance Threshold
   - "Hybrid fusion" → Concept: Vector-Graph Fusion
   - "Lifecycle stages" → Concept: Memory Lifecycle

3. **Identify concept hierarchy:**
   - Parent: Memory Lifecycle
   - Children: Memory Formation, Memory Evolution, Memory Retrieval

4. **Identify concept relationships:**
   - Formation → links to Threshold (mechanism)
   - Evolution → links to Lifecycle (stage)
   - Retrieval → links to Fusion (approach)

**Concept list example:**
```yaml
concepts:
  - name: "Memory Lifecycle"
    hierarchy: root
    children: ["Memory Formation", "Memory Evolution", "Memory Retrieval"]
    source: "survey/03-evolution.md"

  - name: "Memory Formation"
    hierarchy: child
    parent: "Memory Lifecycle"
    mechanism: "Importance Threshold"
    source: "survey/02-formation.md"

  - name: "Importance Threshold"
    hierarchy: mechanism
    parent: "Memory Formation"
    evidence: "P-003 (proven)"
    source: "survey/02-formation.md#2.2"

  - name: "Vector-Graph Fusion"
    hierarchy: approach
    parent: "Memory Retrieval"
    evidence: "P-001 (suggests)"
    source: "survey/04-retrieval.md#4.3"
```

### 3. Generate Wiki Pages

**Wiki page structure:**

```
wiki/
├── README.md               # Auto-generated index
├── Memory-Lifecycle.md     # Root concept
├── Memory-Formation.md     # Child concept
├── Memory-Evolution.md     # Child concept
├── Memory-Retrieval.md     # Child concept
├── Importance-Threshold.md # Mechanism
├── Vector-Graph-Fusion.md  # Approach
└── Memory-Evaluation.md    # Evaluation methodology
```

**Wiki page template:**

```markdown
---
id: WIKI-001
type: wiki-page
concept: "Memory Lifecycle"
hierarchy: root
children: ["Memory Formation", "Memory Evolution", "Memory Retrieval"]
source_chapters:
  - survey/03-evolution.md
  - survey/02-formation.md
  - survey/04-retrieval.md
source_decisions: [DEC-001]
source_experiments: [EXP-001]
last_synced: 2026-04-11T18:00:00Z
status: published
---

# Memory Lifecycle

> Detailed in [Survey §3](../docs/survey/03-evolution.md)

## Definition

Memory lifecycle is the complete process of memory management from formation through evolution to retrieval. It comprises three stages: formation (encoding), evolution (maintenance), and retrieval (access).

## Key Mechanisms

### Formation
[Memory Formation](./Memory-Formation.md) - Encoding information into long-term storage

Mechanism: [Importance Threshold](./Importance-Threshold.md) - Determines persistence

### Evolution
[Memory Evolution](./Memory-Evolution.md) - Managing memory changes over time

Mechanism: Adaptive pruning + consolidation

### Retrieval
[Memory Retrieval](./Memory-Retrieval.md) - Accessing stored information

Approach: [Vector-Graph Fusion](./Vector-Graph-Fusion.md) - Hybrid retrieval

## Evidence

**Supported by:**
- [P-002](../docs/index/papers-index.md#p-002) suggests lifecycle framework (evidence: suggests)
- [EXP-001](../docs/plans/report-EXP-001.md) validates lifecycle mechanisms (confidence: high)

**Evidence boundary:** Lifecycle framework suggested by P-002, validated experimentally in EXP-001.

## Implementation

Our implementation: Hybrid fusion with lifecycle stages

See: [DEC-001](../docs/plans/decision-DEC-001.md#alternative-c)

## Evaluation Results

Retention: 84% (baseline 72%, +16.7%)

See: [EXP-001](../docs/plans/report-EXP-001.md#results)

## Related Concepts

- [Memory Formation](./Memory-Formation.md)
- [Memory Evolution](./Memory-Evolution.md)
- [Memory Retrieval](./Memory-Retrieval.md)

## Deep Dive

For comprehensive coverage, see [Survey §3: Evolution](../docs/survey/03-evolution.md)
```

**Wiki page generation principles:**

1. **Quick reference:** Condensed version for rapid lookup
2. **Deep links:** Link back to source documents for details
3. **Interlinks:** Link to related wiki concepts
4. **Evidence summary:** Top-level evidence, link to full details
5. **Living update:** Timestamped, can be updated

### 4. Create Interlinks

**Interlink strategy:**

Parent-child links:
```markdown
## Key Mechanisms

### Formation
[Memory Formation](./Memory-Formation.md) - Child concept
```

Child-parent links:
```markdown
## Context

Part of: [Memory Lifecycle](./Memory-Lifecycle.md)

Mechanism: [Importance Threshold](./Importance-Threshold.md)
```

Sibling links:
```markdown
## Related Stages

- [Memory Formation](./Memory-Formation.md) - Encoding stage
- [Memory Evolution](./Memory-Evolution.md) - Maintenance stage
- [Memory Retrieval](./Memory-Retrieval.md) - Access stage
```

Cross-concept links:
```markdown
**Mechanism:** [Importance Threshold](./Importance-Threshold.md)

**Approach:** [Vector-Graph Fusion](./Vector-Graph-Fusion.md)
```

### 5. Generate Wiki Index

**Wiki index (README.md):**

```markdown
# Wiki: Agent Memory Research

> Living knowledge base for quick reference

## Overview

This wiki provides condensed summaries of key concepts from our research on agent memory mechanisms.

For comprehensive details, see [Survey](../docs/survey/00-introduction.md).

## Concept Hierarchy

```
Memory Lifecycle (root)
    ├── Memory Formation (stage)
    │       └── Importance Threshold (mechanism)
    ├── Memory Evolution (stage)
    │       └── Adaptive Pruning (mechanism)
    └── Memory Retrieval (stage)
            └── Vector-Graph Fusion (approach)
```

## Core Concepts

### Root Concepts

- **[Memory Lifecycle](./Memory-Lifecycle.md)** - Complete memory management process
  - Evidence: P-002 suggests, EXP-001 validates
  - Implementation: DEC-001

### Stage Concepts

- **[Memory Formation](./Memory-Formation.md)** - Encoding information
  - Mechanism: Importance Threshold
  - Evidence: P-003 proven

- **[Memory Evolution](./Memory-Evolution.md)** - Maintaining memory over time
  - Mechanism: Adaptive pruning
  - Evidence: P-002 suggests

- **[Memory Retrieval](./Memory-Retrieval.md)** - Accessing stored information
  - Approach: Vector-Graph Fusion
  - Evidence: P-001 suggests

### Mechanism Concepts

- **[Importance Threshold](./Importance-Threshold.md)** - Persistence criterion
  - Evidence: P-003 proven
  - Validation: EXP-001 confirms

- **[Vector-Graph Fusion](./Vector-Graph-Fusion.md)** - Hybrid retrieval approach
  - Evidence: P-001 suggests
  - Validation: EXP-001 shows +16.7%

### Methodology Concepts

- **[Memory Evaluation](./Memory-Evaluation.md)** - Benchmark methodology
  - Approach: Rule-derived ground truth
  - Results: 84% retention

## Quick Reference

| Concept | Evidence | Implementation | Validation |
|---------|----------|----------------|------------|
| Lifecycle | P-002 suggests | DEC-001 | EXP-001 ✓ |
| Formation | P-003 proven | Threshold 0.7 | EXP-001 ✓ |
| Retrieval | P-001 suggests | Hybrid fusion | EXP-001 +16.7% |

## Navigation

- **By hierarchy:** See tree above
- **By evidence:** See [Traceability Matrix](../docs/index/traceability-matrix.md)
- **By chapter:** See [Survey](../docs/survey/00-introduction.md)

## Source Documents

- [Survey](../docs/survey/) - Comprehensive chapters
- [Decision](../docs/plans/decision-DEC-001.md) - Architecture choice
- [Evaluation](../docs/plans/report-EXP-001.md) - Validation results

## Updates

This wiki is continuously updated as new findings emerge.

Last synced: 2026-04-11T18:00:00Z

To update, run `/omr-wiki` after new synthesis.
```

### 6. Update Metadata

**Wiki metadata:**
```yaml
---
id: WIKI-001
type: wiki-page
concept: "Memory Lifecycle"
hierarchy: root
children_count: 3
links_to:
  - Memory-Formation.md
  - Memory-Evolution.md
  - Memory-Retrieval.md
  - Importance-Threshold.md
source_chapters:
  - docs/survey/03-evolution.md
source_decisions: [DEC-001]
source_experiments: [EXP-001]
last_synced: 2026-04-11T18:00:00Z
update_frequency: "after synthesis"
status: published
---
```

### 7. Display Summary

```
✓ Extracting concepts: Memory Lifecycle, Formation, Evolution, Retrieval, Threshold, Fusion
✓ Generating 7 wiki pages with interlinks

Wiki pages:
- Memory-Lifecycle.md (links to Formation, Evolution, Retrieval)
- Memory-Formation.md (links to Threshold, Lifecycle)
- Memory-Evolution.md (links to Lifecycle)
- Memory-Retrieval.md (links to Fusion, Lifecycle)
- Importance-Threshold.md (links to Formation)
- Vector-Graph-Fusion.md (links to Retrieval)
- Memory-Evaluation.md (links to Evaluation)

✓ Generated: wiki/*.md
✓ Wiki index: wiki/README.md

📊 Skill tree: Complete ✓

Research complete! All artifacts published.
```

## Gates

None (wiki generation is final stage, no gates)

## Can Call

None

## Prerequisites

- Synthesis chapters OR judgment summary (required)
- If neither: Error "Run `/omr-synthesis` first."

## Examples

### Example 1: Wiki from survey
```
User: /omr-wiki

System: ✓ Reading survey chapters (8 chapters)...
        ✓ Extracting concepts...

        Concepts found:
        - Memory Lifecycle (root)
        - Memory Formation (child)
        - Memory Evolution (child)
        - Memory Retrieval (child)
        - Importance Threshold (mechanism)
        - Vector-Graph Fusion (approach)
        - Memory Evaluation (methodology)

        ✓ Generating 7 wiki pages...

        ✓ Interlinks created:
        Lifecycle → Formation, Evolution, Retrieval
        Formation → Threshold, Lifecycle
        Retrieval → Fusion, Lifecycle

        ✓ Wiki index generated

        Wiki ready at wiki/*.md
        📊 Skill tree: Complete ✓
```

### Example 2: Wiki from judgment (no synthesis)
```
User: /omr-wiki

System: ⚠️  No synthesis found.
        Using judgment summary for wiki...

        Concepts from judgment:
        - Memory Lifecycle (main conclusion)
        - Retrieval Mechanisms (evidence-backed)

        ✓ Generating 2 wiki pages...

        Note: Limited wiki (judgment-only basis)

        Recommend: Run `/omr-synthesis` for comprehensive wiki
```

### Example 3: Auto-trigger after synthesis
```
System: ✓ Synthesis published: docs/survey/

        Generate wiki? [Y/n]

User: Y

System: ✓ Auto-triggering `/omr-wiki`
        ✓ Generating wiki from survey...

        Wiki complete!
```

### Example 4: Missing prerequisites
```
User: /omr-wiki

System: ⚠️  Missing prerequisites:
        - No synthesis found
        - No judgment found

        Cannot generate wiki without source.

        Run `/omr-synthesis` first.

        Aborting...
```

### Example 5: Concept hierarchy visualization
```
User: /omr-wiki

System: ✓ Concepts extracted: 7

        Hierarchy:
        Memory Lifecycle (root)
            ├── Memory Formation
            │       └── Importance Threshold
            ├── Memory Evolution
            └── Memory Retrieval
                    └── Vector-Graph Fusion

        ✓ Pages generated with hierarchy links

        Wiki index shows tree visualization
```

## What NOT to Do

- Do NOT proceed without synthesis or judgment (minimum required)
- Do NOT copy entire synthesis content (wiki is condensed)
- Do NOT omit interlinks (wiki must be interconnected)
- Do NOT omit deep links (must link back to sources)
- Do NOT generate wiki pages without source references
- Do NOT claim wiki is authoritative (synthesis is authoritative, wiki is quick reference)

## Success Criteria

- [ ] Key concepts extracted from synthesis/judgment
- [ ] Concept hierarchy identified
- [ ] Wiki pages generated (one per concept)
- [ ] Interlinks created between concepts
- [ ] Deep links to source documents included
- [ ] Wiki index generated (README.md)
- [ ] Metadata per wiki page recorded
- [ ] Wiki status: published
- [ ] Skill tree: Complete ✓

## Edge Cases

### Single concept

If synthesis yields only one concept:
- Generate single wiki page
- No interlinks (single page)
- Note: "Single concept wiki"

### Flat concept structure

If concepts have no hierarchy:
- Generate flat wiki pages
- No parent-child links
- Use "Related concepts" for sibling links

### Judgment-only wiki

If using judgment only:
- Limited concepts (main conclusion only)
- Wiki pages: 2-3 max
- Note: "Judgment-based wiki, recommend synthesis for comprehensive version"

### Deep synthesis (many chapters)

If synthesis has >10 chapters:
- Extract key concepts (not all chapters)
- Focus on root + top-level concepts
- Link to chapters in wiki pages

### No implementation

If no evaluation/decision:
- Wiki: Evidence-only (no implementation section)
- Note: "No implementation documented"

## Integration with Other Skills

**After wiki:**
- Research complete (all artifacts published)
- Skill tree: Complete ✓

**Before wiki:**
- Requires synthesis or judgment (minimum)
- Synthesis should be Gate D passed (authoritative)

**Living update:**
- If new synthesis generated later, `/omr-wiki` can update wiki
- Wiki pages timestamped with `last_synced`
- Continuous update supported

**Reconciliation:**
- If new evidence changes synthesis, wiki can be regenerated
- Old wiki pages archived or updated

## Dual Output Model

**Documents (authoritative):**
- Survey/report/manuscript/brief in `docs/`
- Complete, evidence-bound, static
- Gate-reviewed, publication-quality

**Wiki (living):**
- Concept pages in `wiki/`
- Quick reference, interlinked, dynamic
- Links back to documents for deep dives
- Continuously updated as findings evolve

**Relationship:**
- Documents = authoritative source
- Wiki = quick reference derived from documents
- Wiki always links back to documents
- Wiki is NOT authoritative (documents are)