---
name: omr-evaluation
description: Design and run evaluation experiments to validate architecture decisions. Creates experiment specification with hypothesis, metrics, and ground truth strategy. Implements prototype code and evaluation tests. Runs experiments and produces evaluation report with results mapped to hypothesis. Enforces Gate C review - checks metrics answer research question, failure conditions explicit, and reproducible design. Use when user wants to "test", "validate", "evaluate decision", or "run experiments".
---

# omr-evaluation: Validate Decision Through Experiments

## Purpose

Design and execute evaluation experiments to validate architecture decisions. This skill transforms decisions into testable hypotheses, implements prototypes, runs evaluations, and produces evidence-bound results that either support or refute the decision.

## Trigger

```
/omr-evaluation
```

**No arguments required** — operates on architecture-decision and research plan

**Prerequisites:**
- `docs/plans/decision-{id}.md` must exist (required, unless Experiment-First pattern)
- Research plan context (implicit, improves hypothesis formulation)

**Pattern override:**
- Experiment-First pattern: allows `omr-evaluation` without prior `decision-{id}.md`

## What This Skill Does

### 1. Read Architecture Decision

**Required:**
- Architecture decision: `docs/plans/decision-{id}.md`

**Optional:**
- Research plan: `docs/plans/plan-{id}.md`
- Evidence map: `docs/plans/evidence-{id}.md`

**If decision missing (unless Experiment-First):**
- Error: "Missing decision. Run `/omr-decision` first."
- Do not proceed

**Load data:**
- Selected alternative description
- Evidence references
- Risks documented
- Research priorities (if plan available)

### 2. Formulate Hypothesis

**Hypothesis derivation:**

From decision selected alternative:
- Extract key claim: "Hybrid fusion improves long-term retention"
- Identify mechanism: "Vector-graph fusion + lifecycle stages"
- Define improvement: "Retention at 7-day interval"
- Set target: "10% improvement over baseline"

**Hypothesis structure:**
```yaml
hypothesis: "Hybrid vector-graph fusion with lifecycle stages improves long-term memory retention compared to vector-only baseline"
target_improvement: "10% retention increase at 7-day interval"
mechanism: "Formation threshold + evolution management"
```

**Hypothesis validation:**
- Ask user: "Hypothesis: '{hypothesis}'. Accept? [Y/n/edit]"
- If edit: Allow user to refine hypothesis

### 3. Define Metrics

**Metrics aligned to research question:**

**Required metrics:**
- Primary metric: Directly answers research question
- Baseline metric: Comparison point from existing evidence

**Optional metrics:**
- Secondary metrics: Additional performance indicators
- Cost metrics: Latency, complexity, resource usage

**Metric structure:**
```yaml
metrics:
  - name: retention_7day
    type: accuracy
    description: "Memory retention rate at 7-day interval"
    baseline: 0.72  # from P-001 evidence
    target: 0.80    # +10% improvement target
    unit: "fraction (0-1)"

  - name: latency_avg
    type: milliseconds
    description: "Average retrieval latency"
    baseline: 50    # from P-001 evidence
    target: 100     # acceptable threshold
    unit: "ms"

  - name: memory_size
    type: count
    description: "Memory entries after 7 days"
    baseline: 1000  # from B-001 production data
    target: 1500    # evolution should grow memory
    unit: "entries"
```

**Metric selection criteria:**
- Must answer research question (Gate C check)
- Must have baseline for comparison
- Must have clear target/success threshold
- Must be measurable/reproducible

### 4. Define Ground Truth Strategy

**Ground truth strategies:**

| Strategy | Description | Use Case |
|----------|-------------|----------|
| **rule-derived** (preferred) | Deterministic rules, no human annotation | Algorithmic validation, clear criteria |
| **benchmark-derived** | Use existing benchmark datasets | Standard evaluation, comparison possible |
| **simulation-derived** | Generate synthetic scenarios | Novel mechanisms, no existing benchmarks |

**Rule-derived example:**
```yaml
ground_truth_strategy: rule-derived
rules:
  - name: retention_valid
    criteria: "Memory entry retained if accessed ≥3 times in 7-day period"
    implementation: "Count access frequency, check threshold"
  - name: relevance_score
    criteria: "Importance threshold > 0.7 for retention"
    implementation: "Calculate importance, filter by threshold"
```

**Benchmark-derived example:**
```yaml
ground_truth_strategy: benchmark-derived
benchmark:
  name: "Memory Retention Benchmark (MRB)"
  source: "P-001 evaluation dataset"
  file: "raw/datasets/mrb-test-set.json"
  size: 1000 scenarios
```

**Simulation-derived example:**
```yaml
ground_truth_strategy: simulation-derived
simulation:
  scenarios: 15
  duration: 7 days each
  operations_per_day: 100
  profile: "diverse agent tasks"
```

**Strategy selection:**
- Prefer rule-derived (no annotation cost)
- Use benchmark-derived if available in evidence
- Use simulation-derived for novel mechanisms

### 5. Define Failure Conditions

**Failure conditions:**

```yaml
failure_conditions:
  - "Retention < baseline at any interval"
  - "Latency > 2x baseline"
  - "Memory size uncontrolled growth (> 5x baseline)"
  - "Hypothesis not supported by majority of scenarios"
```

**Failure condition criteria:**
- Must be explicit and measurable (Gate C check)
- Must prevent false positives
- Must define what constitutes "failure"

### 6. Create Experiment Specification

**Metadata:**
```yaml
---
id: EXP-001
type: experiment-spec
version: 1.0.0
decision_id: DEC-001
plan_id: PLAN-001
hypothesis: "Hybrid fusion improves long-term retention by 10%"
target_improvement: "+10% retention at 7-day"
metrics:
  - name: retention_7day
    baseline: 0.72
    target: 0.80
  - name: latency_avg
    baseline: 50
    target: 100
ground_truth_strategy: rule-derived
failure_conditions:
  - "Retention < baseline"
  - "Latency > 2x baseline"
scenario_count: 15
estimated_duration: "2 days"
created_at: 2026-04-11T15:00:00Z
updated_at: 2026-04-11T15:00:00Z
status: draft
dependencies: [DEC-001]
gate_c_passed: null
---
```

**Content structure:**
```markdown
# Experiment Specification: {hypothesis}

## Hypothesis

**Claim:** Hybrid vector-graph fusion with lifecycle stages improves long-term memory retention

**Target:** 10% improvement over baseline (72% → 80% at 7-day interval)

**Mechanism tested:** Formation threshold + evolution management

## Metrics

### Primary: retention_7day
- **Baseline:** 0.72 (from [P-001](../index/papers-index.md#p-001))
- **Target:** 0.80 (+10% improvement)
- **Unit:** fraction (0-1)
- **Critical:** Yes (directly answers research question)

### Secondary: latency_avg
- **Baseline:** 50ms (from [P-001](../index/papers-index.md#p-001))
- **Target:** ≤100ms
- **Unit:** milliseconds
- **Critical:** No (performance indicator)

### Secondary: memory_size
- **Baseline:** 1000 entries (from [B-001](../index/blogs-index.md#b-001))
- **Target:** ≤1500 entries (controlled growth)
- **Unit:** count
- **Critical:** No (resource indicator)

## Ground Truth

**Strategy:** rule-derived (no human annotation)

**Rules:**
1. **Retention valid:** Memory entry retained if accessed ≥3 times in 7-day period
2. **Importance threshold:** Importance score > 0.7 for retention

## Failure Conditions

Experiment fails if:
- Retention < baseline (72%) at any interval
- Latency > 2x baseline (100ms)
- Memory size uncontrolled (> 5x baseline)
- Hypothesis unsupported by majority scenarios

## Experimental Design

**Scenarios:** 15 diverse agent tasks

**Duration:** 7 days per scenario (simulated)

**Operations:** 100 operations per day (memory read/write)

**Profile:** Mix of retrieval-heavy, formation-heavy, evolution-heavy tasks

## Implementation Plan

1. Implement hybrid prototype in `src/prototype/`
2. Write evaluation tests in `src/evaluation/`
3. Run 15 scenarios
4. Collect metrics
5. Map results to hypothesis

## Reproducibility

- Prototype code version-controlled
- Evaluation tests automated
- Metrics collected automatically
- Ground truth rules documented

## Next Steps

Proceed to Gate C review before implementation.
```

### 7. Present Gate C Review

**Gate C: Before Experiment Execution**

**Position:** Before implementation and testing
**Purpose:** Ensure experiment design valid

**Gate C checks:**
- [ ] Metrics answer research question
- [ ] Failure conditions explicit
- [ ] Ground truth strategy defined
- [ ] Reproducible evaluation design

**Gate C review process:**

1. Display experiment spec
2. Show gate criteria checklist
3. Ask user confirmation:
   ```
   ⚠️  GATE C: Before Experiment

   Review criteria:
   [✓] Metrics answer research question (retention_7day critical)
   [✓] Failure conditions explicit (3 conditions defined)
   [✓] Ground truth strategy: rule-derived
   [✓] Reproducible design (automated tests)

   Hypothesis: Hybrid fusion improves retention by 10%

   Proceed with implementation? [Y/n/modify]
   ```

4. If user approves:
   - Mark `gate_c_passed: true` in spec metadata
   - Proceed to implementation

5. If user rejects:
   - Ask: "What needs modification?"
   - Offer: [Edit hypothesis] [Add metrics] [Revise ground truth]
   - Loop until approved or user cancels

### 8. Implement Prototype

**Prototype structure:**

```
src/prototype/
├── main.py              # Core implementation
├── memory/
│   ├── formation.py     # Formation mechanism
│   ├── evolution.py     # Evolution mechanism
│   └── retrieval.py     # Retrieval mechanism
├── config.yaml          # Configuration
└── README.md            # Usage documentation
```

**Implementation process:**
1. Implement selected alternative from decision
2. Follow architecture from decision document
3. Use evidence-backed mechanisms (from evidence refs)
4. Ensure testability (metrics must be measurable)

**Prototype code example:**
```python
# src/prototype/memory/formation.py

class FormationMechanism:
    """Formation with importance threshold (from P-003)"""

    def __init__(self, threshold=0.7):
        self.threshold = threshold  # P-003: importance threshold formalized

    def should_form(self, memory_candidate):
        """Determine if memory should be formed"""
        importance = self.calculate_importance(memory_candidate)
        return importance > self.threshold

    def calculate_importance(self, item):
        """Importance calculation (rule-derived ground truth)"""
        # Access frequency, recency, relevance
        return item.access_count / max(item.age_days, 1)
```

### 9. Write Evaluation Tests

**Evaluation structure:**

```
src/evaluation/
├── test_retention.py    # Retention metric test
├── test_latency.py      # Latency metric test
├── test_memory_size.py  # Size metric test
├── scenarios/
│   ├── scenario_01.json
│   ├── scenario_02.json
│   └── ...
├── run_evaluation.py    # Test runner
└── results/
    └── results.json     # Collected metrics
```

**Test code example:**
```python
# src/evaluation/test_retention.py

import pytest
from prototype.memory import HybridMemory

def test_retention_7day():
    """Test 7-day retention against baseline 72%"""

    # Setup
    memory = HybridMemory(config="prototype/config.yaml")
    scenario = load_scenario("scenarios/scenario_01.json")

    # Run 7-day simulation
    for day in range(7):
        run_operations(memory, scenario.operations_per_day)

    # Measure retention
    retained = memory.get_retained_entries()
    total = memory.get_total_entries()
    retention_rate = len(retained) / len(total)

    # Check against baseline
    baseline = 0.72
    assert retention_rate >= baseline, f"Retention {retention_rate} < baseline {baseline}"

    return retention_rate
```

### 10. Run Evaluation

**Evaluation execution:**

1. Run all 15 scenarios
2. Collect metrics per scenario
3. Aggregate results
4. Calculate improvement vs. baseline
5. Map to hypothesis

**Results collection:**
```json
{
  "experiment_id": "EXP-001",
  "scenarios_run": 15,
  "metrics_results": [
    {
      "scenario": 1,
      "retention_7day": 0.85,
      "latency_avg": 52,
      "memory_size": 1200
    },
    {
      "scenario": 2,
      "retention_7day": 0.83,
      "latency_avg": 55,
      "memory_size": 1100
    },
    ...
  ],
  "aggregate": {
    "retention_7day_mean": 0.84,
    "retention_7day_std": 0.02,
    "latency_avg_mean": 55,
    "memory_size_mean": 1250
  }
}
```

### 11. Generate Evaluation Report

**Metadata:**
```yaml
---
id: EXP-001
type: evaluation-report
version: 1.0.0
decision_id: DEC-001
spec_id: EXP-001
hypothesis: "Hybrid fusion improves retention by 10%"
hypothesis_supported: true
metrics_results:
  - name: retention_7day
    baseline: 0.72
    result: 0.84
    improvement: "+16.7%"
    target_met: true
    critical: true
  - name: latency_avg
    baseline: 50
    result: 55
    improvement: "+10%"
    target_met: true
    critical: false
ground_truth: rule-derived
confidence: high
recommendations:
  - "Proceed to synthesis"
  - "Document novel lifecycle mechanism"
created_at: 2026-04-11T16:00:00Z
updated_at: 2026-04-11T16:00:00Z
status: draft
dependencies: [EXP-001-spec]
gate_c_passed: true
---
```

**Content structure:**
```markdown
# Evaluation Report: {hypothesis}

## Hypothesis

**Claim:** Hybrid fusion improves long-term retention by 10%

**Result:** Supported ✓

## Metrics Results

### Primary: retention_7day
- **Baseline:** 0.72 (72%)
- **Result:** 0.84 (84%)
- **Improvement:** +16.7%
- **Target:** 0.80 (target met ✓)

**Conclusion:** Retention significantly improved, exceeds target

### Secondary: latency_avg
- **Baseline:** 50ms
- **Result:** 55ms
- **Improvement:** +10%
- **Target:** ≤100ms (target met ✓)

**Conclusion:** Latency acceptable, within threshold

### Secondary: memory_size
- **Baseline:** 1000 entries
- **Result:** 1250 entries
- **Improvement:** +25%
- **Target:** ≤1500 (target met ✓)

**Conclusion:** Controlled growth, evolution working

## Hypothesis Assessment

**Hypothesis supported:** Yes

**Evidence:**
- Primary metric (retention) met target: 84% vs. 80% target
- All critical metrics passed
- No failure conditions triggered

## Confidence Assessment

**Confidence:** High

**Rationale:**
- Large improvement (+16.7% vs. target +10%)
- Consistent across 15 scenarios (std dev 0.02)
- Ground truth rule-derived (deterministic)

## Ground Truth Validation

**Strategy:** rule-derived

**Rules applied:**
- Retention threshold: ≥3 accesses → retained
- Importance threshold: >0.7 → retained

**Validation:** Rules correctly implemented, deterministic results

## Limitations

- Simulation-based (no real-world agent tasks)
- 7-day interval only (longer intervals untested)
- Ground truth rule-derived (may not match real importance)

## Recommendations

1. Proceed to `/omr-synthesis` to document findings
2. Document novel lifecycle mechanism as contribution
3. Consider longer interval evaluation (14-day, 30-day)

## Traceability

| Metric | Evidence Source | Decision Ref |
|--------|------------------|--------------|
| retention_7day baseline | [P-001](../index/papers-index.md#p-001) | [DEC-001](decision-DEC-001.md) |
| latency baseline | [P-001](../index/papers-index.md#p-001) | [DEC-001](decision-DEC-001.md) |
| Hypothesis | [DEC-001](decision-DEC-001.md#selected-alternative) | Decision C |

## Next Steps

Proceed to `/omr-synthesis` for writeup.
```

### 12. Update Skill Tree

**After evaluation complete:**
- Mark `omr-evaluation` as complete ✓
- Unlock `omr-synthesis` as ready ○

### 13. Prompt Next Action

```
✓ Spec: Hybrid fusion vs. vector-only
✓ Hypothesis: Improves 7-day retention by 10%
✓ Prototype implemented in src/prototype/
✓ Tests written in src/evaluation/
✓ Evaluation run (15 scenarios)

Results:
- Retention: 84% (baseline 72%, +16.7%)
- Latency: 55ms (baseline 50ms, +10%)
- Memory size: 1250 entries (controlled growth)

Hypothesis: Supported ✓
Confidence: High

✓ Report: report-EXP-001.md
📊 Skill tree: omr-synthesis [READY]

Next step: `/omr-synthesis` to document findings
```

## Gates

**Gate C: Experiment design valid?**

**Position:** Before implementation and execution
**Checks:**
1. Metrics answer research question (primary metric critical)
2. Failure conditions explicit (all failure modes defined)
3. Ground truth strategy defined (rule/benchmark/simulation)
4. Reproducible evaluation design (automated tests)

**Enforcement:**
- User confirmation required (default mode)
- Auto-pass if explicitly configured for agents

**Gate failure handling:**
- If Gate C fails: "Design incomplete. Options: [Add metrics] [Define failure conditions] [Specify ground truth]"
- Do not proceed to implementation until gate passed

## Can Call

- `omr-synthesis` (auto-trigger on evaluation success)
- `omr-wiki` (auto-trigger after synthesis)

## Prerequisites

- Architecture decision exists (required, unless Experiment-First)
- If decision missing (and not Experiment-First): Error "Run `/omr-decision` first."

**Pattern override:**
- Experiment-First: allows evaluation without decision
- Decision-First: Gate C required
- Evidence-First: Gate C required

## Examples

### Example 1: Gate C passed, hypothesis supported
```
User: /omr-evaluation

System: ✓ Reading decision...
        ✓ Formulating hypothesis...

        Hypothesis: "Hybrid fusion improves retention by 10%"

        Metrics:
        - retention_7day (primary): 72% → 80% target
        - latency_avg: 50ms → 100ms threshold
        - memory_size: 1000 → 1500 controlled

        Ground truth: rule-derived
        Failure conditions: 3 defined

        ⚠️  GATE C: Before Experiment
        [✓] Metrics answer question
        [✓] Failure conditions explicit
        [✓] Ground truth defined
        [✓] Reproducible

        Proceed? [Y/n]

User: Y

System: ✓ Gate C passed
        ✓ Implementing prototype...
        ✓ Writing tests...
        ✓ Running 15 scenarios...

        Results:
        - Retention: 84% (+16.7%, target met)
        - Latency: 55ms (+10%, acceptable)
        - Memory: 1250 entries (controlled)

        Hypothesis: Supported ✓
        Confidence: High

        ✓ Report: report-EXP-001.md
        📊 Skill tree: omr-synthesis [READY]
```

### Example 2: Gate C failed (missing failure conditions)
```
User: /omr-evaluation

System: ✓ Formulating spec...

        ⚠️  GATE C: Before Experiment
        [✓] Metrics answer question
        [✗] Failure conditions: undefined
        [✓] Ground truth defined
        [✓] Reproducible

        Gate C failed: Missing failure conditions

        Define failure conditions before proceeding.

        Options:
        [1] Auto-generate from metrics
        [2] Manual input
        [3] Cancel

User: 1

System: ✓ Generated failure conditions:
        - Retention < baseline
        - Latency > 2x baseline
        - Hypothesis unsupported

        Proceed? [Y/n]
```

### Example 3: Hypothesis not supported
```
User: /omr-evaluation

System: ✓ Running evaluation...

        Results:
        - Retention: 70% (baseline 72%, -2.8%)
        - Latency: 55ms (+10%, acceptable)

        ⚠️  Hypothesis NOT supported
        - Retention decreased vs. baseline
        - Failure condition triggered

        Confidence: Low (hypothesis refuted)

        Recommendations:
        [1] Revisit decision (alternative may be flawed)
        [2] Debug prototype (implementation issue?)
        [3] Run `/omr-reconcile` to update decision

        Report: report-EXP-001.md (hypothesis refuted)
```

### Example 4: Experiment-First pattern (no prior decision)
```
User: /omr-evaluation

System: ⚠️  No decision found.
        Pattern detected: Experiment-First

        Proceed without decision? [Y/n]

User: Y

System: ✓ Creating speculative hypothesis...

        Hypothesis: "Novel mechanism improves performance"

        Metrics: Define based on goal

        What's your goal?

User: Test memory retention improvement

System: ✓ Metrics:
        - retention_7day (primary)
        - latency_avg (secondary)

        Ground truth: rule-derived

        Proceed? [Y/n]
```

### Example 5: Missing prerequisites
```
User: /omr-evaluation

System: ⚠️  Missing prerequisites:
        - decision-{id}.md not found
        - Not Experiment-First pattern

        Cannot proceed without decision.

        Run `/omr-decision` first.

        Aborting...
```

## What NOT to Do

- Do NOT proceed without decision (unless Experiment-First confirmed)
- Do NOT skip Gate C review (user must confirm)
- Do NOT proceed without metrics answering research question
- Do NOT proceed without failure conditions defined
- Do NOT claim hypothesis supported if metrics failed
- Do NOT claim high confidence if results inconsistent
- Do NOT use human annotation ground truth (prefer rule-derived)
- Do NOT proceed if failure conditions triggered

## Success Criteria

- [ ] Experiment spec created with hypothesis + metrics
- [ ] Ground truth strategy defined
- [ ] Failure conditions explicit
- [ ] Gate C passed
- [ ] Prototype implemented in `src/prototype/`
- [ ] Tests written in `src/evaluation/`
- [ ] Evaluation run (all scenarios)
- [ ] Results collected and analyzed
- [ ] Hypothesis mapped to results (supported or refuted)
- [ ] Evaluation report generated
- [ ] Skill tree updated (unlock `omr-synthesis`)

## Edge Cases

### Hypothesis partially supported

If some metrics pass, others fail:
- Report: "Hypothesis partially supported"
- Confidence: Medium
- Recommendations: "Partial success — investigate failed metrics"
- Do not claim full support

### Ground truth ambiguous

If rule-derived ground truth unclear:
- Refine rules with user input
- Add more deterministic criteria
- Ensure reproducibility

### Prototype implementation issues

If prototype fails to implement decision:
- Debug and fix
- If unfixable: Report implementation failure
- Recommend: "Revisit decision for feasibility"

### Evaluation timeout

If evaluation runs too long:
- Reduce scenario count
- Simplify operations
- Optimize prototype

### Results inconsistent

If results vary widely across scenarios:
- Analyze variance
- Identify scenario-specific factors
- Report: "Results inconsistent, confidence reduced"

## Integration with Other Skills

**After evaluation:**
- Unlock `omr-synthesis` for writeup
- May auto-trigger `omr-synthesis` if hypothesis supported

**Before evaluation:**
- Requires `omr-decision` for decision (unless Experiment-First)
- May use `omr-research-plan` for plan context

**Reconciliation:**
- If new evidence contradicts evaluation, `omr-reconcile` may call this skill to re-run

**Pattern flexibility:**
- Evidence-First: Gate C required, decision required
- Idea-First: Gate C required, decision may be speculative
- Decision-First: Gate C required, decision required
- Experiment-First: Gate C may be relaxed, decision optional