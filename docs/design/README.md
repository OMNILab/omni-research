# Omni-Research Design Documents

This folder contains detailed design specifications for the omni-research skill system.

## Design Documents

| Document | Purpose |
|----------|---------|
| [overview.md](overview.md) | Research philosophy, core capabilities, evidence hierarchy |
| [architecture.md](architecture.md) | Repository structure, generated workspace structure |
| [skills.md](skills.md) | Core skills list, contracts, detailed capabilities per skill |
| [patterns.md](patterns.md) | Research patterns library, pattern emergence workflow |
| [gates.md](gates.md) | Quality gates system (A, B, C, D), enforcement modes |
| [progress.md](progress.md) | Skill tree model, progress visualization, dual view mode |
| [iteration.md](iteration.md) | Reconciliation system, archiving behavior, blast radius analysis |
| [metadata.md](metadata.md) | Artifact metadata system, versioning, naming conventions, status workflow |
| [outputs.md](outputs.md) | Dual output model, synthesis modes, wiki generation |
| [workflows.md](workflows.md) | End-to-end workflow examples for each pattern |
| [principles.md](principles.md) | Design principles, core decisions, what makes omr different |

## Quick Reference

**12 Core Skills:**
1. `omr-bootstrap` — Initialize workspace
2. `omr-collection` — Collect materials
3. `omr-evidence` — Map evidence
4. `omr-research-plan` — Judge + plan
5. `omr-decision` — Architectural decision
6. `omr-evaluation` — Run experiments
7. `omr-synthesis` — Write findings (survey/report/manuscript/brief)
8. `omr-wiki` — Generate wiki
9. `omr-reconcile` — Update state on evidence change
10. `omr-idea-note` — Capture insights
11. `omr-research-archive` — Snapshot progress

**4 Gates:**
- Gate A: Before planning
- Gate B: Before decision
- Gate C: Before evaluation
- Gate D: Before synthesis

**5 Patterns:**
- Evidence-First
- Idea-First
- Decision-First
- Experiment-First
- Rapid-Prototype

**Mental Model:**
```
omr = Skills + Tree + Gates + Patterns + Reconciliation
```