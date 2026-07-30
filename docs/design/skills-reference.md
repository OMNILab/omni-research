# Skills Reference (Quick)

See individual `skills/omr-*/SKILL.md` files for detailed capabilities per skill.

## Core Skills List

| Skill | Purpose | Stage | Gates |
|-------|---------|-------|-------|
| `omr-core` | Infrastructure | Core | None |
| `omr-bootstrap` | Initialize workspace | Init | None |
| `omr-collection` | Collect materials | Collection | None |
| `omr-analyze` | Scan + brief + evidence-map + judgment + plan | Definition + Judgment + Planning | Gate A (internal) |
| `omr-decision` | Architecture decision | Decision | Gate B |
| `omr-evaluation` | Run experiments | Validation | Gate C |
| `omr-synthesis` | Write findings (+ wiki internal, `--no-wiki` to skip) | Writeback | Gate D |
| `omr-reconcile` | Update on evidence change + archive (`--archive` / `--rollback` / `--list` / `--review`) | Iteration | None |
| `omr-idea-note` | Capture insights | Any | None |

**Total: 9 skills** (8 core + `omr-core` infrastructure)

## Deprecated / Merged Skills

Merged in v2.0.0 as part of skill consolidation (12 → 9). Keep references for backward compatibility.

| Skill | Status | Merged Into |
|-------|--------|-------------|
| `omr-evidence` | Deprecated (v2.0.0, phase 2.2) | `omr-analyze` — brief + evidence-map |
| `omr-research-plan` | Deprecated (v2.0.0, phase 2.2) | `omr-analyze` — judgment + plan (Gate A now internal) |
| `omr-wiki` | Deprecated (v2.0.0, phase 3.1) | `omr-synthesis` — wiki is an internal post-Gate-D step |
| `omr-research-archive` | Deprecated (v2.0.0, phase 3.4) | `omr-reconcile` — archive via `--archive` / `--rollback` / `--list` / `--review` |

## Skill Contracts (Template)

```yaml
skill: omr-{name}
requires:
  - artifact: {artifact-id}.md
    optional: false
produces:
  - artifact: {output-id}.md
gates:
  - id: gate_{x}
    checks: [list]
    enforcement: user-confirm | auto-pass
```

## Synthesis Modes

| Mode | Output | Best For |
|------|--------|----------|
| `survey` | Chapters (01-07) | Academic research |
| `report` | Structured findings | Industry deliverables |
| `manuscript` | Publication-ready | Papers, conferences |
| `brief` | Executive summary | Quick findings |
