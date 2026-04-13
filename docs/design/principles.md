# Design Principles

## Core Design Decisions

| Dimension | Decision | Rationale |
|-----------|----------|-----------|
| Skill model | 12 composable skills | Right granularity — not too coarse, not too fine |
| Progress model | Skill tree (game-inspired) | Visible progress, unlock-based, motivating |
| Planning model | Reverse skill tree | Goal-driven, shortest path, deadline-friendly |
| Patterns | Emerged from practice, saved | Flexible rigor, not rigid pipelines |
| Gates | Skill-level (A, B, C, D) | Quality checkpoints, configurable enforcement |
| Agency | Configurable per pattern | Novice guidance + expert speed + agent automation |
| Archive | Auto + manual trigger | Safety (auto) + control (manual) |
| Synthesis | Configurable output modes | Context-aware (survey/report/manuscript/brief) |
| State | Artifact-bound | All state in files, no hidden state, inspectable |
| Composability | Synchronous skill calls | Simple, deterministic, no async complexity |

## What Makes omr Different

| Other Tools | omr |
|-------------|-----|
| Fixed pipeline | Flexible patterns (5 patterns, custom patterns) |
| No visibility into progress | Skill tree shows exact state |
| Manual iteration | Automatic reconciliation with blast radius |
| One output type | Configurable synthesis (survey/report/manuscript/brief) |
| No quality gates | 4 gates enforce rigor |
| Artifacts scattered | Everything in structured folders with metadata |
| No version control | Semantic versioning + history tracking |
| No traceability | Full artifact ID system + cross-refs |
| One research style | Multiple entry points (evidence/idea/decision/experiment) |

## Simplest Mental Model

**omr = Skills + Tree + Gates + Patterns + Reconciliation**

1. **Skills** = tools (do one thing well)
2. **Tree** = progress visualization (what's unlocked)
3. **Gates** = quality checks (don't publish garbage)
4. **Patterns** = recipes (save working sequences)
5. **Reconciliation** = iteration support (research changes)

## Evidence-Bound Research Philosophy

**Core stance: `research ≠ information-gathering`**

True deep research requires a complete lifecycle:

```
Collection → Definition → Evidence → Judgment → Decision → Validation → Writeback
```

**Three principles:**
- **Traceable**: Every claim links to source, decision, or experiment
- **Evidence-bound**: Clear boundaries between "proven", "suggested", "inferred"
- **Reproducible**: Artifacts versioned alongside conclusions

## Pattern-Based Composition Philosophy

**Skills are NOT pipeline stages** — they are **composable ingredients**.

- Patterns are saved sequences, not forced workflows
- Skills can be invoked freely in any order
- Pattern selection happens after first action (guidance without commitment)
- Multiple patterns can run concurrently (parallel research threads)

## Skill-Level Gates Philosophy

**Gates are skill contracts, not pattern-level rules.**

- Each skill declares its quality requirements
- Patterns can override gate enforcement (Experiment-First, Rapid-Prototype)
- Gates check artifacts, not user intent
- Semi-automated vs fully-automated configurable

## Artifact-Bound State Philosophy

**All state lives in artifacts, not in memory.**

- No hidden state — everything inspectable via files
- Metadata in YAML frontmatter
- Versioning in artifact filenames + history JSON
- Dependency tracking in metadata
- Machine-readable indexes for tooling

## Reconciliation as First-Class Concept

**Iteration is NOT an exception** — it's a core capability.

- New evidence triggers automatic reconciliation
- Blast radius analysis shows full impact
- Archive old versions automatically
- Maintain traceability through updates
- Rollback support via archived versions

## Configurable Output Philosophy

**Synthesis is NOT one-size-fits-all** — output type depends on context.

- Survey for academic research
- Report for industry deliverables
- Manuscript for publication
- Brief for quick findings
- Mode determined by pattern or user override
