# Quality Gates

## Gate System Overview

| Gate | Position | Purpose | Required Artifacts |
|------|----------|---------|-------------------|
| **A** | Before `omr-research-plan` | Evidence sufficient for planning? | research-brief.md, evidence-map.md |
| **B** | Before `omr-decision` | Architecture decision sound? | research-brief.md, evidence-map.md, judgment-summary.md (optional) |
| **C** | Before `omr-evaluation` | Experiment design valid? | architecture-decision.md |
| **D** | Before `omr-synthesis` | Results traceable, no over-claiming? | evaluation-report.md OR judgment-summary.md |

## Gate A: Before Research Planning

**Review Criteria:**
- [ ] Evidence coverage adequate
- [ ] Research question clear
- [ ] Scope defined
- [ ] Judgment confidence reasonable

**Failure handling:** "Evidence insufficient. Add materials via `/omr-collection` or revise scope."

## Gate B: Before Architecture Decision

**Review Criteria:**
- [ ] Alternatives documented (≥3)
- [ ] Risks stated
- [ ] Evidence refs valid
- [ ] Selection rationale clear

**Failure handling:** "Decision incomplete. Document alternatives, risks, rationale."

## Gate C: Before Evaluation

**Review Criteria:**
- [ ] Metrics answer research question
- [ ] Failure conditions explicit
- [ ] Ground truth strategy defined
- [ ] Reproducible evaluation design

**Failure handling:** "Experiment design incomplete. Define metrics, ground truth, failure conditions."

## Gate D: Before Synthesis

**Review Criteria:**
- [ ] Results traceable to hypotheses
- [ ] Evidence boundaries stated
- [ ] No over-claiming ("proves" vs "suggests")
- [ ] Cross-references valid

**Failure handling:** "Synthesis incomplete. Fix over-claiming, add evidence boundaries, verify cross-refs."

## Gate Enforcement Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| **Semi-automated** (default) | User confirms at each gate | Interactive research |
| **Fully-automated** | Gates auto-pass | Agent-driven execution |
| **Configurable** | Set per pattern or project | Mixed environments |

## Gate Metadata Recording

```yaml
gates_passed:
  - gate: gate_b
    passed_at: 2026-04-11T15:00:00Z
    reviewer: user
    checks:
      - "Alternatives documented: ✓"
      - "Risks stated: ✓"
      - "Evidence refs valid: ✓"
```

## Contract Overrides for Gates

Patterns can override gate enforcement:
- Experiment-First: Gate C still applies, but `omr-evaluation` can run without prior decision
- Rapid-Prototype: All gates disabled

## Gate Failure → Reconciliation

When a gate fails, the system offers:
1. Fix the artifact to pass gate
2. Reconcile state (call `omr-reconcile`)
3. Switch to different pattern with different gate requirements
