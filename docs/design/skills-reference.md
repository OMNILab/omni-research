# Skills Reference (Quick)

See [skills.md](skills.md) for detailed capabilities per skill.

## Core Skills List

| Skill | Purpose | Stage | Gates |
|-------|---------|-------|-------|
| `omr-bootstrap` | Initialize workspace | Init | None |
| `omr-collection` | Collect materials | Collection | None |
| `omr-evidence` | Map evidence | Definition + Evidence | None |
| `omr-research-plan` | Judge + plan | Judgment + Planning | Gate A |
| `omr-decision` | Architecture decision | Decision | Gate B |
| `omr-evaluation` | Run experiments | Validation | Gate C |
| `omr-synthesis` | Write findings | Writeback | Gate D |
| `omr-wiki` | Generate wiki | Writeback | None |
| `omr-reconcile` | Update on evidence change | Iteration | None |
| `omr-idea-note` | Capture insights | Any | None |
| `omr-research-archive` | Snapshot progress | Lifecycle | None |

**Total: 12 skills** (11 core + configurable synthesis)

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
