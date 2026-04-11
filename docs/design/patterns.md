# Research Patterns

## What Are Patterns?

A **pattern** is a named sequence of skill invocations that satisfies a research goal. Patterns emerge from practice and are saved as reusable templates.

**Patterns are NOT rigid pipelines** — they're recipes. Skills can be invoked freely; patterns record successful paths.

## Pattern Library

### Evidence-First
Rigorous research starting from literature collection.
```
omr-collection → omr-evidence → omr-research-plan → omr-decision → omr-evaluation → omr-synthesis → omr-wiki
```
- Gates: A, B, C, D
- Synthesis mode: survey
- Best for: Academic research, literature surveys

### Idea-First
Speculative research starting from creative insight.
```
omr-idea-note → omr-decision → omr-evaluation → omr-evidence → omr-synthesis → omr-wiki
```
- Gates: D only
- Synthesis mode: brief
- Best for: Exploratory research, speculative work
- Note: `judgment-summary.md` (optional) not produced before decision

### Decision-First
Hypothesis-driven research starting from architectural stance.
```
omr-decision → omr-evidence → omr-research-plan → omr-evaluation → omr-synthesis → omr-wiki
```
- Gates: C, D
- Synthesis mode: report
- Best for: Engineering research, prototype-driven

### Experiment-First
Empirical research starting from building and testing.
```
omr-evaluation → omr-evidence → omr-decision → omr-synthesis → omr-wiki
```
- Gates: D only
- Synthesis mode: brief
- Best for: Quick validation, proof-of-concept
- Contract override: `omr-evaluation` can run without prior decision

### Rapid-Prototype
Fastest path to working output.
```
omr-evaluation → omr-evidence → omr-decision → omr-synthesis
```
- Gates: none
- Synthesis mode: brief
- Best for: Hackathons, time-boxed exploration

## Pattern Emergence

1. Bootstrap → Workspace created, no pattern forced
2. First action → User selects first skill
3. Pattern detection → After 3+ invocations, system proposes pattern name
4. Pattern save → User accepts/rejects saving as template
5. Template library → Saved patterns stored in `skills/patterns/`

## Pattern Selection Timing

Patterns are detected **after first action**, not forced at bootstrap. Provides guidance without forced commitment.

## Pattern Config Format

```yaml
name: Evidence-First
description: Rigorous research starting from literature
synthesis_mode: survey
graph:
  entry_points: [omr-collection]
  nodes: [omr-evidence, omr-research-plan, omr-decision, ...]
  edges: [omr-collection → omr-evidence, ...]
skill_gates:
  omr-research-plan: gate_a
  omr-decision: gate_b
  omr-evaluation: gate_c
  omr-synthesis: gate_d
contract_overrides: {}  # Experiment-First would override omr-evaluation requirements
agency: semi-automated
estimated_time: 3-5 days
```

## Pattern Validation Rule

A pattern is valid if every skill's **MANDATORY** requirements are satisfied by upstream skill outputs. Optional requirements may be unsatisfied.

## Multiple Concurrent Patterns

Projects can have multiple parallel patterns:
- Evidence-First for literature survey
- Idea-First for speculative branch
- Patterns share isolated artifacts or fork workspace
