# Quality Gates

## Gate System Overview

| Gate | Position | Purpose | Required Artifacts |
|------|----------|---------|-------------------|
| **A** | Within `omr-analyze` (after judgment, before plan) | Evidence sufficient for planning? | research-brief.md, evidence-map.md, judgment-summary.md |
| **B** | Before `omr-decision` | Architecture decision sound? | research-brief.md, evidence-map.md, judgment-summary.md (optional) |
| **C** | Before `omr-evaluation` | Experiment design valid? | architecture-decision.md |
| **D** | Before `omr-synthesis` | Results traceable, no over-claiming? | evaluation-report.md OR judgment-summary.md |
| **L** | Within `omr-analyze` (after judgment, before Gate A) or `omr-idea-note` (after note write) | Iterate deeper or advance? | `.omr/loop-state.json` (Loop active) |

## Gate L: Iterate or Advance (Loop pattern)

Gate L is the **Loop control surface**. It is presented only when the Loop pattern is active **or** `.omr/loop-state.json` has `active: true`. Other patterns skip Gate L.

**Position:**
- `omr-analyze`: `after_judgment_before_gate_a` — deepen evidence before planning
- `omr-idea-note`: `after_note_write` — refine ideas before decision/collection

**Review Criteria:**
- [ ] Focus question still productive
- [ ] New material / tighter question available for next cycle
- [ ] Confidence / coverage improved since last iteration
- [ ] Ready to exit loop into the next stage

**Outcomes:**
- **Iterate** — stay in cycle (collection / re-analyze / another idea note); update loop-state
- **Advance** — deactivate loop; proceed to Gate A (analyze path) or decision/collection (idea-dev)
- **Stop / park** — save state, do not unlock next stage

**Helper:** `omr-core/scripts/loop_state.py`

**Relationship to Gate A:** Gate L asks “keep digging?”; Gate A asks “evidence good enough to plan?” Advancing from Gate L still requires Gate A on the deep-analyze path.

## Gate A: Within omr-analyze (Internal Checkpoint)

Gate A is now an **internal checkpoint** within `omr-analyze`, positioned after judgment synthesis and before plan generation (position: `after_judgment_before_plan`). It is no longer a standalone gate before `omr-research-plan`. When Gate A passes, `omr-analyze` unlocks `omr-decision`.

**Review Criteria:**
- [ ] Evidence coverage adequate
- [ ] Research question clear
- [ ] Scope defined
- [ ] Judgment confidence reasonable

**Failure handling:** "Evidence insufficient. Add materials via `/omr-collection` or revise scope." `omr-analyze` re-runs the evidence/judgment phases before producing `research-plan.md`.

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
- Loop: Gate L required on `omr-idea-note` / `omr-analyze`; Gate A still applies after Advance on deep-analyze path

## Gate Failure → Reconciliation

When a gate fails, the system offers:
1. Fix the artifact to pass gate
2. Reconcile state (call `omr-reconcile`)
3. Switch to different pattern with different gate requirements
