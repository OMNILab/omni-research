---
name: omr-reconcile
description: Update research state when new evidence contradicts existing artifacts. Analyzes impact blast radius across dependent artifacts, proposes reconciliation options, archives old versions, and updates affected downstream artifacts. Maintains traceability through reconciliation history. Can trigger automatically after new material collection. Use when user wants to "update research", "reconcile contradictions", or when new evidence arrives.
---

# omr-reconcile: Reconcile Research State on Evidence Changes

## Purpose

Update research state when new evidence contradicts existing artifacts. This skill analyzes the impact blast radius, proposes reconciliation options, archives superseded versions, and updates all affected downstream artifacts while maintaining complete traceability.

## Trigger

```
/omr-reconcile
```

**No arguments required** — triggered by contradiction detection

**Automatic triggers:**
- New material collected via `omr-collection` contradicts existing evidence
- Gate failure during `omr-research-plan` or `omr-decision`
- User manual request

**Trigger detection:**
- If new paper abstract contradicts decision selected alternative
- If new blog claims contradict primary evidence
- If Gate A/B failure indicates insufficient evidence

## What This Skill Does

### 1. Detect Trigger Event

**Trigger types:**

| Type | Source | Detection |
|------|--------|-----------|
| `new_evidence` | `omr-collection` | New paper abstract contradicts existing artifact |
| `gate_failure` | Gate A/B/C/D | Evidence insufficient, decision flawed |
| `manual_request` | User command | `/omr-reconcile` explicit invocation |

**Contradiction detection:**

For each new material collected:
1. Extract abstract/summary
2. Compare with existing decisions (selected alternative)
3. Compare with existing evidence (primary evidence claims)
4. Check for contradictions:
   - New paper claims X, decision assumes ¬X
   - New paper refutes existing paper's claims

**Contradiction example:**
```
Existing decision DEC-001:
  Selected: "Hybrid fusion improves retention"
  Evidence: P-001 demonstrates hybrid > vector-only

New paper P-005:
  Abstract: "Graph-only memory outperforms hybrid fusion"
  Claim: Graph-only > hybrid

Contradiction: P-005 refutes DEC-001 assumption
```

### 2. Analyze Blast Radius

**Blast radius analysis:**

1. Identify affected artifact (trigger artifact)
2. Trace dependency chain (artifacts depending on trigger)
3. Mark affected artifacts:
   - ⚠️ Contradicted (needs update)
   - ⚠️ Needs re-run (depends on contradicted artifact)
   - ✓ Unaffected (independent)

**Blast radius visualization:**
```
New paper P-005 contradicts DEC-001
    ↓
Affected: DEC-001 (contradicted)
    ↓
Dependent: EXP-001 (depends on DEC-001)
    ↓
EXP-001 needs re-run (tests hybrid, may be suboptimal)
    ↓
SYN-001 (depends on EXP-001) → needs update

Blast radius:
- DEC-001: ⚠️ Contradicted (needs revision)
- EXP-001: ⚠️ Needs re-run
- SYN-001: ⚠️ Needs update (not published yet)
```

**Dependency tracking:**

Read artifact metadata:
```yaml
# decision-DEC-001.md
dependencies: [Q-001, J-001]
dependents: [EXP-001]  # Artifacts that depend on this
```

Trace chain:
```
DEC-001 → dependents: [EXP-001]
EXP-001 → dependents: [SYN-001]
SYN-001 → dependents: []
```

### 3. Propose Reconciliation Options

**Reconciliation options:**

| Option | Action | Use Case |
|--------|--------|----------|
| **Re-evaluate** | Update evidence → update judgment → re-decide → re-run experiment | Major contradiction, evidence weight changed |
| **Accept contradiction** | Document as "debated approach", proceed with decision | Minor contradiction, both approaches valid |
| **Fork parallel thread** | Create parallel research thread for alternative | Both approaches worth investigating |

**Option presentation:**

```
⚠️  New evidence contradicts Decision DEC-001

Impact analysis:
- DEC-001: ⚠️ Contradicted (P-005 claims graph-only > hybrid)
- EXP-001: ⚠️ Tests hybrid (may be suboptimal)
- SYN-001: Not published (safe)

Reconciliation options:

[1] Re-evaluate → Update decision → Re-run experiment
    - Add P-005 to evidence
    - Update judgment (contradiction present)
    - Re-decide with graph-only as alternative
    - Re-run experiment comparing hybrid vs. graph-only
    - Update synthesis

[2] Accept contradiction → Document as "debated approach"
    - Keep DEC-001 (hybrid selected)
    - Add note: "P-005 contradicts, debated approach"
    - Document both in synthesis
    - Proceed with current state

[3] Fork parallel thread → Investigate graph-only separately
    - Create new research thread: "graph-only approach"
    - Run parallel experiment
    - Compare both findings
    - Synthesis includes both

Choose [1-3]:
```

### 4. Execute Reconciliation

**Option 1: Re-evaluate (full update)**

**Reconciliation workflow:**

1. **Add new evidence:**
   - Update `docs/index/papers-index.json` (add P-005)
   - Update `docs/plans/evidence-{id}.md` (add P-005 to primary evidence)

2. **Update judgment:**
   - Call `omr-evidence` (re-map evidence landscape)
   - New judgment: "Hybrid vs. graph-only debated"
   - Confidence: medium (contradictions present)

3. **Re-decide:**
   - Call `omr-decision` (revise decision with new alternatives)
   - Add graph-only as co-equal alternative
   - Risks: Add "Comparative study needed"

4. **Re-run experiment:**
   - Call `omr-evaluation` (re-run with updated decision)
   - Compare hybrid vs. graph-only
   - New results may favor graph-only

5. **Update synthesis:**
   - Call `omr-synthesis` (update with new findings)
   - Document both approaches
   - Note contradiction resolution

6. **Archive old versions:**
   - Archive: `decision-DEC-001-v1.0.0.md`
   - Create: `decision-DEC-001-v2.0.0.md`

**Reconciliation execution example:**

```
User: 1

System: ✓ Re-evaluating evidence (calling omr-evidence)...

        Evidence updated: P-005 added (graph-only claims)

        New judgment:
        - Hybrid vs. graph-only debated (contradiction present)
        - Confidence: medium

        ✓ Updating judgment...

        ⚠️  Gate B: Decision needs revision

        DEC-001 (v2.0.0):
        - Alternatives: Add graph-only as co-equal (Alternative B)
        - Risks: Add "Comparative study needed"
        - Selection: C (hybrid) provisional, pending comparison

        Approve? [Y/n]

User: Y

System: ✓ Archived: decision-DEC-001-v1.0.0.md → docs/archive/
        ✓ Updated: decision-DEC-001-v2.0.0.md
        ✓ Version history: docs/index/versions/DEC-001-history.json

        ✓ Re-running experiment (calling omr-evaluation)...

        EXP-002: Compare hybrid vs. graph-only
        - Hypothesis: "Graph-only may outperform hybrid"
        - Metrics: retention, latency

        Running evaluation...

        Results:
        - Hybrid: 84% retention
        - Graph-only: 82% retention
        - Graph-only latency: 40ms (vs. hybrid 55ms)

        Conclusion: Hybrid better retention, graph-only faster

        ✓ New evaluation: report-EXP-002.md
        ✓ Updated synthesis: docs/survey/03-evolution.md

        Reconciliation complete!

        📊 Skill tree: omr-decision [v2], omr-evaluation [EXP-002], omr-synthesis [updated]
```

**Option 2: Accept contradiction (document only)**

**Workflow:**

1. Add note to decision: "P-005 contradicts, debated approach"
2. Update synthesis: Document both approaches
3. No re-evaluation or re-run
4. Proceed with current state

**Execution:**
```
User: 2

System: ✓ Accepting contradiction...

        ✓ Note added to DEC-001:
        "⚠️ P-005 contradicts hybrid superiority. Debated approach."

        ✓ Synthesis updated: docs/survey/03-evolution.md
        "Hybrid vs. graph-only debated (P-001 vs. P-005)."

        ✓ Decision unchanged, contradiction documented

        Proceeding with current state...

        Note: Future evaluation may resolve debate
```

**Option 3: Fork parallel thread**

**Workflow:**

1. Create new research thread: "graph-only approach"
2. New decision: graph-only selected
3. New experiment: evaluate graph-only separately
4. Parallel synthesis: "graph-only findings"
5. Compare both threads later

**Execution:**
```
User: 3

System: ✓ Forking parallel thread...

        New thread: "graph-only approach"

        ✓ New decision: decision-DEC-002.md
        - Selected: graph-only (Alternative B)
        - Evidence: P-005 suggests

        ✓ New experiment: spec-EXP-002.md
        - Test graph-only separately

        ✓ Parallel synthesis: docs/report/graph-only-findings.md

        ✓ Two threads now:
        1. Hybrid approach (DEC-001, EXP-001)
        2. Graph-only approach (DEC-002, EXP-002)

        Future: Comparative synthesis to resolve
```

### 5. Archive Old Versions

**Archiving process:**

1. Collect superseded artifacts
2. Copy to `docs/archive/` with version suffix
3. Update version history
4. Mark as archived in metadata

**Archive structure:**
```
docs/archive/
├── 20260411T163000/               # Timestamped snapshot
│   ├── decision-DEC-001-v1.0.0.md # Archived version
│   ├── report-EXP-001-v1.0.0.md   # Archived version
│   └── brief-Q-001-v1.0.0.md      # Archived version
└── index.json                     # Archive index
```

**Version history:**
```json
// docs/index/versions/DEC-001-history.json
{
  "id": "DEC-001",
  "history": [
    {
      "version": "1.0.0",
      "created_at": "2026-04-11T14:20:00Z",
      "status": "archived",
      "reason": "Superseded by v2.0.0 due to new contradicting evidence (P-005)",
      "file": "docs/archive/20260411T163000/decision-DEC-001-v1.0.0.md"
    },
    {
      "version": "2.0.0",
      "created_at": "2026-04-11T16:45:00Z",
      "status": "published",
      "reason": "Updated to include graph-only as alternative after P-005 contradiction",
      "file": "docs/plans/decision-DEC-001.md"
    }
  ]
}
```

### 6. Update Main Index

**Artifacts index update:**

```json
// docs/index/artifacts-index.json
{
  "artifacts": [
    {
      "id": "DEC-001",
      "type": "architecture-decision",
      "version": "2.0.0",
      "status": "published",
      "file": "docs/plans/decision-DEC-001.md",
      "reconciled": true,
      "reconciliation_history": "docs/index/versions/DEC-001-history.json"
    }
  ]
}
```

### 7. Generate Reconciliation Report

**Reconciliation metadata:**
```yaml
---
id: REC-001
type: reconciliation
trigger: new_evidence
trigger_artifact: P-005
trigger_type: paper
trigger_claim: "Graph-only outperforms hybrid fusion"
affected_artifacts:
  - id: DEC-001
    type: architecture-decision
    impact: contradicted
    action: revised
    old_version: 1.0.0
    new_version: 2.0.0
  - id: EXP-001
    type: evaluation-report
    impact: needs_re-run
    action: re-evaluated
    new_id: EXP-002
  - id: SYN-001
    type: synthesis
    impact: needs_update
    action: updated
reconciliation_action: re_evaluate
reconciliation_options:
  - re_evaluate
  - accept_contradiction
  - fork_thread
selected_option: re_evaluate
completed_at: 2026-04-11T16:45:00Z
archived_versions:
  - decision-DEC-001-v1.0.0.md
  - report-EXP-001-v1.0.0.md
status: complete
---
```

### 8. Maintain Traceability

**Traceability through reconciliation:**

Every artifact maintains:
```yaml
dependencies: [Q-001, J-001]
reconciled_from: DEC-001-v1.0.0  # If reconciled
reconciliation_reason: "New evidence P-005 contradicted"
```

Cross-reference in new artifacts:
```markdown
**Previous version:** [DEC-001 v1.0.0](../archive/decision-DEC-001-v1.0.0.md)

**Reconciliation:** P-005 contradicted hybrid superiority

**Update:** Added graph-only as co-equal alternative
```

## Gates

None (reconciliation is iterative process, no gates)

## Can Call

- `omr-evidence` (re-map evidence)
- `omr-research-plan` (re-plan judgment)
- `omr-decision` (re-decide architecture)
- `omr-evaluation` (re-run experiment)
- `omr-synthesis` (update synthesis)
- `omr-research-archive` (archive superseded versions)

## Prerequisites

- At least one existing artifact (required)
- Trigger event (new evidence or gate failure)

**If no artifacts:**
- Error: "No artifacts to reconcile. This is a new workspace."
- Do not proceed

## Examples

### Example 1: New evidence contradiction
```
User: /omr-collection https://arxiv.org/abs/2402.99999

System: ✓ New paper P-005: Graph-only outperforms fusion
        ⚠️  Contradicts Decision DEC-001

        Impact analysis:
        - DEC-001: ⚠️ Contradicted
        - EXP-001: ⚠️ Tests hybrid (may be suboptimal)
        - SYN-001: Not yet published (safe)

        Reconciliation options:
        [1] Re-evaluate → Update decision → Re-run experiment
        [2] Accept contradiction → Document as "debated approach"
        [3] Fork parallel thread

User: 1

System: ✓ Re-evaluating evidence...
        ✓ Updating judgment...
        ⚠️  Gate B: Decision needs revision

        DEC-001 (v2.0.0):
        - Alternatives: Add graph-only as co-equal
        - Risks: Add "Comparative study needed"

        Approve? [Y/n]

User: Y

System: ✓ Archived: decision-DEC-001-v1.0.0.md
        ✓ Updated: decision-DEC-001-v2.0.0.md
        ✓ Version history: docs/index/versions/DEC-001-history.json
        📊 Skill tree: omr-evaluation [READY: re-run]
```

### Example 2: Gate failure reconciliation
```
System: ⚠️  GATE A failed: Evidence insufficient

        Evidence coverage: weak (2 primary evidence)
        Required: ≥3 primary evidence

        Reconciliation options:
        [1] Add more materials (call omr-collection)
        [2] Reduce scope to match evidence
        [3] Proceed anyway (low confidence accepted)

User: 1

System: ✓ Triggering reconciliation...
        Add materials before proceeding.

        Call `/omr-collection` to add papers.

        After collection, re-run `/omr-evidence` to update evidence map.
```

### Example 3: Manual reconciliation request
```
User: /omr-reconcile

System: ✓ Scanning for contradictions...

        No active contradictions detected.

        Current state:
        - DEC-001: published
        - EXP-001: published
        - SYN-001: published

        All artifacts consistent.

        Reconcile anyway? [y/N]

User: N

System: No reconciliation needed. State stable.
```

### Example 4: Accept contradiction option
```
User: 2 (accept contradiction)

System: ✓ Accepting contradiction without re-evaluation

        ✓ Note added to DEC-001:
        "⚠️ P-005 contradicts hybrid superiority. Debated approach."

        ✓ Synthesis updated:
        "Hybrid vs. graph-only debated (P-001 vs. P-005)."

        ✓ Decision unchanged (proceeding with hybrid)

        Note: Future evaluation recommended to resolve debate

        Reconciliation complete (documented).
```

### Example 5: Fork parallel thread
```
User: 3 (fork thread)

System: ✓ Forking parallel research thread...

        New thread: "graph-only approach"
        Thread ID: THREAD-002

        ✓ Creating new decision: DEC-002
        - Selected: graph-only (P-005 suggests)

        ✓ Creating new experiment: EXP-002
        - Test graph-only separately

        ✓ Two parallel threads:
        THREAD-001: Hybrid approach (DEC-001, EXP-001)
        THREAD-002: Graph-only approach (DEC-002, EXP-002)

        Future: Comparative synthesis to merge findings
```

### Example 6: Missing prerequisites
```
User: /omr-reconcile

System: ⚠️  No artifacts found.
        This appears to be a new workspace.

        Reconciliation requires at least one existing artifact.

        Run `/omr-bootstrap` first if workspace not initialized.

        Aborting...
```

## What NOT to Do

- Do NOT proceed without existing artifacts (new workspace has nothing to reconcile)
- Do NOT auto-reconcile without user approval (must present options)
- Do NOT delete old versions (always archive)
- Do NOT skip blast radius analysis (must show affected artifacts)
- Do NOT claim reconciliation complete if downstream not updated
- Do NOT hide contradictions (must document clearly)

## Success Criteria

- [ ] Trigger event detected
- [ ] Blast radius analyzed (all affected artifacts identified)
- [ ] Reconciliation options presented to user
- [ ] User selected option
- [ ] Affected artifacts updated (depending on option)
- [ ] Old versions archived
- [ ] Version history updated
- [ ] Main index updated
- [ ] Traceability maintained (reconciliation history recorded)
- [ ] Reconciliation report generated

## Edge Cases

### No active contradiction

If scan finds no contradictions:
- Report: "No active contradictions detected"
- Ask: "Reconcile anyway? [y/N]"
- If no: Abort (state stable)

### Minor contradiction

If contradiction is minor (不影响 core decision):
- Option: Accept contradiction (document only)
- Recommendation: "Minor contradiction, document and proceed"

### Major contradiction

If contradiction invalidates decision:
- Option: Re-evaluate (full update)
- Recommendation: "Major contradiction, full reconciliation needed"

### Synthesis already published

If synthesis published before contradiction:
- Cannot update published synthesis
- Option: Create v2 synthesis or archive + republish
- Recommendation: "Archive published synthesis, create v2"

### Unpublished synthesis

If synthesis not published:
- Safe to update (no archival needed)
- Update synthesis directly
- Recommendation: "Synthesis draft, safe to update"

### Circular dependencies

If artifacts have circular dependencies (rare):
- Break cycle by updating one artifact
- Re-run dependent artifacts
- Recommendation: "Circular dependency detected, manual resolution needed"

## Integration with Other Skills

**Can call:**
- `omr-evidence`: Re-map evidence landscape
- `omr-research-plan`: Re-plan with updated judgment
- `omr-decision`: Re-decide with new alternatives
- `omr-evaluation`: Re-run experiments
- `omr-synthesis`: Update synthesis with new findings
- `omr-research-archive`: Archive superseded versions

**Called by:**
- `omr-collection`: Auto-trigger if new material contradicts
- Gate failures: Auto-trigger if evidence insufficient

**Reconciliation loop:**
```
New evidence → omr-reconcile →
  calls omr-evidence →
  calls omr-research-plan →
  calls omr-decision →
  calls omr-evaluation →
  calls omr-synthesis →
  calls omr-research-archive →
Reconciliation complete
```

**Traceability preservation:**
Every reconciliation maintains complete history:
- Old versions archived
- Version history recorded
- Cross-references preserved
- Reason documented