# Iteration and Reconciliation

## When Reconciliation Triggers

| Trigger | Source | Action |
|---------|--------|--------|
| New paper arrives | `omr-collection` | Auto-flag: "Reconcile?" |
| Evidence map updated | `omr-evidence` | Check affected decisions |
| Gate failure | Gate A/B/C/D | Prompt: "Reconcile state?" |
| Manual request | User command | `/omr-reconcile` |

## Reconciliation Workflow

```
New evidence detected
    ↓
omr-reconcile analyzes impact
    ↓
Flags affected artifacts (blast radius)
    ↓
Offers: "Re-evaluate? (will update decision, re-test experiment)"
    ↓
User approves
    ↓
Call affected skills in order
    ↓
Archive old versions
    ↓
Update version history
```

## Blast Radius Analysis

Example:
```
New paper P-005 contradicts DEC-001
    ↓
Affected chain:
  DEC-001 → EXP-001 → SYN-001
    ↓
DEC-001 needs Gate B re-review
EXP-001 needs re-run
SYN-001 needs update (if published)
```

System shows full dependency chain, not just immediate artifact.

## Reconciliation Options

| Option | Behavior | Use Case |
|--------|----------|----------|
| [1] Re-evaluate → Update → Re-run | Full update chain | Strong contradiction |
| [2] Accept contradiction → Document | Add as debated approach | Weak contradiction |
| [3] Fork parallel thread | Spawn new pattern | Alternative hypothesis |

## Skill Calling Order

Reconciliation calls skills in dependency order:
```
omr-reconcile → 
  omr-evidence (re-evaluate) →
  omr-research-plan (update judgment) →
  omr-decision (re-decide, Gate B) →
  omr-evaluation (re-run, Gate C)
```

## Archiving Behavior

### Automatic Archiving
- Triggered when `omr-reconcile` supersedes artifacts
- Old version moved to `docs/archive/{id}-v{old-version}.md`
- Version history updated in `docs/index/versions/{id}-history.json`

### Manual Archiving
- User triggers `/omr-research-archive`
- Timestamped snapshot of all current artifacts
- Snapshot stored in `docs/archive/{timestamp}/`
- Use case: Preserve state before risky pivot

### Archive Structure

```
docs/archive/
├── 20260411T163000/
│   ├── brief-Q-001.md
│   ├── decision-DEC-001.md
│   └── report-EXP-001.md
├── decision-DEC-001-v1.0.0.md
├── decision-DEC-001-v2.0.0.md (current)
└── index.json
```

## Version History Tracking

```json
{
  "id": "DEC-001",
  "history": [
    {
      "version": "1.0.0",
      "created_at": "2026-04-11T14:20:00Z",
      "status": "archived",
      "reason": "Superseded by v2.0.0 due to new contradicting evidence",
      "file": "docs/archive/decision-DEC-001-v1.0.0.md"
    },
    {
      "version": "2.0.0",
      "created_at": "2026-04-11T16:45:00Z",
      "status": "published",
      "reason": "Updated to include graph-only as alternative",
      "file": "docs/plans/decision-DEC-001.md"
    }
  ]
}
```

## Reconciliation Metadata

```yaml
---
id: REC-001
type: reconciliation
trigger: new_evidence
trigger_artifact: P-005
affected_artifacts:
  - DEC-001 (contradicted)
  - EXP-001 (needs re-run)
reconciliation_actions:
  - re_evaluate_evidence
  - update_judgment
  - re_decide
completed_at: 2026-04-11T16:45:00Z
archived_versions:
  - decision-DEC-001-v1.0.0.md
---
```

## Rollback Support

Archived versions can be restored:
- View archived version: `/omr-archive --view DEC-001-v1.0.0`
- Restore archived version: `/omr-reconcile --restore DEC-001-v1.0.0`
- Creates new current version from archived state
