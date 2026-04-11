# Workflow Examples

## Evidence-First Pattern

```bash
# 1. Initialize project
/omr-bootstrap "agent memory mechanisms"

# 2. First action (pattern emerges)
/omr-collection https://arxiv.org/abs/2401.xxxxx
# System: "Pattern emerging: Evidence-First. Save? [y/N]"
# User: y

# 3. Map evidence
/omr-evidence  # → brief-Q-001.md + evidence-Q-001.md

# 4. Plan research (Gate A)
/omr-research-plan  # → judgment-Q-001.md + plan-Q-001.md
# Gate A review

# 5. Make decision (Gate B)
/omr-decision  # → decision-DEC-001.md
# Gate B review

# 6. Evaluate (Gate C)
/omr-evaluation  # → spec-EXP-001.md + report-EXP-001.md + src/prototype/
# Gate C review

# 7. Synthesize (Gate D)
/omr-synthesis  # → docs/survey/ (mode: survey from pattern)
# Gate D review

# 8. Generate wiki
/omr-wiki  # → wiki/*.md

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

# 4. Backfill evidence
/omr-evidence  # → brief-Q-001.md + evidence-Q-001.md (validate/refute decision)

# 5. Synthesize (Gate D)
/omr-synthesis --brief  # → docs/brief/
# Gate D review

# 6. Generate wiki
/omr-wiki  # → wiki/*.md
```

## Decision-First Pattern

```bash
# 1. Initialize
/omr-bootstrap "engineering hypothesis"

# 2. Make decision first
/omr-decision  # → decision-DEC-001.md (hypothesis-driven)

# 3. Gather evidence to validate
/omr-evidence  # → brief-Q-001.md + evidence-Q-001.md

# 4. Plan research (Gate A)
/omr-research-plan  # → judgment + plan
# Gate A review

# 5. Evaluate (Gate C)
/omr-evaluation  # → spec + report + prototype
# Gate C review

# 6. Synthesize (Gate D)
/omr-synthesis  # → docs/report/ (mode: report from pattern)
# Gate D review
```

## Experiment-First Pattern

```bash
# 1. Initialize
/omr-bootstrap "quick validation"

# 2. Start by building
/omr-evaluation  # → spec + prototype + report (no prior decision needed)

# 3. Gather evidence post-build
/omr-evidence  # → brief + evidence-map

# 4. Make decision based on results
/omr-decision  # → decision (informed by experiment)

# 5. Synthesize (Gate D)
/omr-synthesis --brief  # → docs/brief/
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
#   ✓ Re-evaluating evidence (calling omr-evidence)...
#   ✓ Updating judgment (calling omr-research-plan)...
#   ⚠️  Gate B: Decision needs revision
#   ✓ Archived: decision-DEC-001-v1.0.0.md
#   ✓ Updated: decision-DEC-001-v2.0.0.md

# Continue with new state
/omr-evaluation  # Re-run experiment with updated decision
```

## Manual Archive Scenario

```bash
# Before risky pivot
/omr-research-archive
# System:
#   ✓ Archiving current state...
#   ✓ Archived: docs/archive/20260411T163000/
#   Snapshot saved. You can rollback if needed.

# Try risky approach
/omr-decision  # New decision
/omr-evaluation  # Test

# If fails, rollback
/omr-reconcile --restore DEC-001-v1.0.0
# System:
#   ✓ Restored: decision-DEC-001 from v1.0.0
#   ✓ New current version: decision-DEC-001-v3.0.0
```
