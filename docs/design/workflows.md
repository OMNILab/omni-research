# Workflow Examples

## Evidence-First Pattern

```bash
# 1. Initialize project
/omr-bootstrap "agent memory mechanisms"

# 2. First action (pattern emerges)
/omr-collection https://arxiv.org/abs/2401.xxxxx
# System: "Pattern emerging: Evidence-First. Save? [y/N]"
# User: y

# 3. Analyze (brief + evidence-map + judgment + plan, Gate A internal)
/omr-analyze  # → research-brief.md + evidence-map.md + judgment-summary.md + research-plan.md
# Gate A review (internal checkpoint, after judgment before plan)

# 4. Make decision (Gate B)
/omr-decision  # → decision-DEC-001.md
# Gate B review

# 5. Evaluate (Gate C)
/omr-evaluation  # → spec-EXP-001.md + report-EXP-001.md + src/prototype/
# Gate C review

# 6. Synthesize (Gate D, wiki auto-generated)
/omr-synthesis  # → docs/survey/ (mode: survey from pattern) + wiki/*.md
# Gate D review

# Skill tree: Complete ✓
```

## Idea-First Pattern

```bash
# 1. Initialize + capture idea
/omr-bootstrap "speculative topic"
/omr-idea-note "What if memory works like quantum superposition?"

# 2. Make decision (no gates until D)
/omr-decision  # → decision-DEC-001.md (no evidence yet)

# 3. Build and test
/omr-evaluation  # → src/prototype/ + report-EXP-001.md

# 4. Analyze (backfill brief + evidence-map + judgment + plan)
/omr-analyze  # → research-brief.md + evidence-map.md + judgment-summary.md + research-plan.md (validate/refute decision)

# 5. Synthesize (Gate D, wiki auto-generated)
/omr-synthesis --brief  # → docs/brief/ + wiki/*.md
# Gate D review
```

## Decision-First Pattern

```bash
# 1. Initialize
/omr-bootstrap "engineering hypothesis"

# 2. Make decision first
/omr-decision  # → decision-DEC-001.md (hypothesis-driven)

# 3. Analyze (brief + evidence-map + judgment + plan, Gate A internal)
/omr-analyze  # → research-brief.md + evidence-map.md + judgment-summary.md + research-plan.md
# Gate A review (internal checkpoint, after judgment before plan)

# 4. Evaluate (Gate C)
/omr-evaluation  # → spec + report + prototype
# Gate C review

# 5. Synthesize (Gate D, wiki auto-generated)
/omr-synthesis  # → docs/report/ (mode: report from pattern) + wiki/*.md
# Gate D review
```

## Experiment-First Pattern

```bash
# 1. Initialize
/omr-bootstrap "quick validation"

# 2. Start by building
/omr-evaluation  # → spec + prototype + report (no prior decision needed)

# 3. Analyze (brief + evidence-map + judgment + plan, Gate A internal)
/omr-analyze  # → research-brief.md + evidence-map.md + judgment-summary.md + research-plan.md

# 4. Make decision based on results
/omr-decision  # → decision (informed by experiment)

# 5. Synthesize (Gate D, wiki auto-generated)
/omr-synthesis --brief  # → docs/brief/ + wiki/*.md
# Gate D review
```

## Reconciliation Scenario

```bash
# Mid-research, new paper arrives
/omr-collection https://arxiv.org/abs/2402.99999
# System: "New evidence contradicts Decision DEC-001. Reconcile? [Y/n]"

# User approves reconciliation
/omr-reconcile
# System:
#   ✓ Re-evaluating evidence + updating judgment (calling omr-analyze)...
#   ⚠️  Gate B: Decision needs revision
#   ✓ Archived: decision-DEC-001-v1.0.0.md
#   ✓ Updated: decision-DEC-001-v2.0.0.md

# Continue with new state
/omr-evaluation  # Re-run experiment with updated decision
```

## Manual Archive Scenario

```bash
# Before risky pivot
/omr-reconcile --archive
# System:
#   ✓ Archiving current state...
#   ✓ Archived: docs/archive/20260411T163000/
#   Snapshot saved. You can rollback if needed.

# Try risky approach
/omr-decision  # New decision
/omr-evaluation  # Test

# If fails, rollback
/omr-reconcile --rollback DEC-001-v1.0.0
# System:
#   ✓ Restored: decision-DEC-001 from v1.0.0
#   ✓ New current version: decision-DEC-001-v3.0.0
```
