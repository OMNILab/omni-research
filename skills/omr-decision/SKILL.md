---
name: omr-decision
description: Create architectural decisions with alternatives, rationale, and evidence references. Documents at least 3 alternatives, selects best option based on evidence and judgment, identifies risks, and ensures traceability. Enforces Gate B review before implementation - checks alternatives documented, risks stated, and evidence refs valid. Use when user wants to "make a decision", "choose architecture", or "select approach" after planning is complete. REQUIRES omr-core skill and workspace with research plan.
version: 1.0.0
author: OmniResearch Team
license: MIT
metadata:
  requires_skills: [omr-core]
  requires_workspace: true
  category: architecture-decisions
  phase: 2.4
---

# omr-decision: Make Architecture Decision

## Purpose

Make an architectural decision with explicit alternatives, rationale, and evidence traceability. This skill formalizes the decision-making process by requiring at least 3 alternatives, clear selection rationale, risk documentation, and links back to evidence sources.

## Trigger

```
/omr-decision
```

**No arguments required** — operates on evidence-map and optionally judgment-summary

**Prerequisites:**
- `docs/plans/evidence-{id}.md` must exist (required)
- `docs/plans/judgment-{id}.md` may exist (optional, improves decision quality)

## What This Skill Does

### 1. Read Evidence and Judgment

**Required:**
- Evidence map: `docs/plans/evidence-{id}.md`

**Optional:**
- Judgment summary: `docs/plans/judgment-{id}.md`
- Research plan: `docs/plans/plan-{id}.md`

**If evidence map missing:**
- Error: "Missing evidence. Run `/omr-evidence` first."
- Do not proceed

**Load data:**
- Primary evidence list with findings
- Supporting evidence list
- Open gaps
- Judgment conclusion (if available)
- Research priorities (if plan available)

### 2. Generate Alternatives

**Alternative generation process:**

1. **Analyze evidence-supported approaches:**
   - What approaches are validated in primary evidence?
   - What approaches are suggested in supporting evidence?
   - What novel approaches address identified gaps?

2. **Generate at least 3 alternatives:**
   - Alternative A: Baseline (existing validated approach)
   - Alternative B: Evidence-suggested (improvement from supporting evidence)
   - Alternative C: Novel (addresses gap, extends evidence)
   - Alternative D: Hybrid (combines multiple approaches)

3. **For each alternative:**
   - Description: Clear technical specification
   - Evidence basis: Links to supporting papers/blogs
   - Pros: Advantages from evidence
   - Cons: Limitations from evidence
   - Risks: Uncertainties and challenges

**Alternative structure:**
```yaml
alternatives:
  - id: A
    description: "Vector-only memory architecture"
    evidence_basis:
      - P-001: "Validated as baseline approach"
      - B-001: "Production implementations use vector-only"
    pros:
      - "Simpler implementation"
      - "Lower latency"
      - "Well-tested in production"
    cons:
      - "Limited long-term retention (P-001 shows 72% vs. 84%)"
      - "No lifecycle management"
    risks:
      - "May not meet 7-day retention target"
    selected: false
    reason: "Baseline for comparison, but insufficient for lifecycle needs"

  - id: B
    description: "Graph-only memory with relational indexing"
    evidence_basis:
      - P-002: "Suggests graph structure for relationships"
      - B-002: "Blog proposes graph for evolution"
    pros:
      - "Explicit relationships"
      - "Better evolution tracking"
    cons:
      - "Retrieval latency higher (no benchmarks yet)"
      - "Less validated than vector"
    risks:
      - "Performance unknown (no empirical evidence)"
      - "Implementation complexity"
    selected: false
    reason: "Addresses evolution gap, but lacks validation"

  - id: C
    description: "Hybrid vector-graph fusion with lifecycle stages"
    evidence_basis:
      - P-001: "Proven improvement for retrieval"
      - P-003: "Formation threshold formalized"
      - P-002: "Lifecycle framework proposed"
    pros:
      - "Best retrieval accuracy (P-001: +16.7%)"
      - "Lifecycle mechanisms integrated"
      - "Formation + evolution support"
    cons:
      - "Higher complexity"
      - "No direct precedent for full lifecycle"
    risks:
      - "Novel combination (unvalidated)"
      - "May require custom evaluation"
    selected: true
    reason: "Addresses primary gap (lifecycle) while leveraging proven retrieval improvement"

  - id: D
    description: "Hybrid with adaptive mode-switching"
    evidence_basis:
      - P-001: "Hybrid proven"
      - B-003: "Blog proposes adaptive switching"
    pros:
      - "Flexibility for different tasks"
    cons:
      - "Complex mode logic"
      - "No evidence for switching criteria"
    risks:
      - "Highly speculative (blog-only)"
      - "Implementation overhead"
    selected: false
    reason: "Speculative, insufficient evidence support"
```

**Alternative naming:**
- Use clear, descriptive names
- IDs: A, B, C, D (or descriptive slugs: baseline, graph-only, hybrid-fusion)
- Avoid vague names: "Approach 1", "Option A"

### 3. Select Best Alternative

**Selection criteria:**

1. **Evidence support:**
   - Weight: How many primary evidence support it?
   - Strength: proven vs. suggests vs. inferred

2. **Gap addressing:**
   - Does it address identified open gaps?
   - Does it extend validated mechanisms?

3. **Risk assessment:**
   - Are risks manageable?
   - Can risks be mitigated with evaluation?

4. **Feasibility:**
   - Implementation complexity reasonable?
   - Timeline aligned with research plan?

**Selection process:**
- Score each alternative on criteria
- Discuss trade-offs
- Select alternative with best overall fit
- Document rationale

**Selection rationale:**
```markdown
Selected: Alternative C (Hybrid fusion with lifecycle)

**Rationale:**
1. Evidence support: Strong (P-001 proven, P-002 suggests framework)
2. Gap addressing: Yes (addresses lifecycle gap identified in judgment)
3. Risks: Manageable (novel but testable)
4. Feasibility: Moderate complexity, aligned with timeline

**Trade-off accepted:**
Higher complexity vs. comprehensive lifecycle support

**Alternative A rejected:** Baseline insufficient for lifecycle needs
**Alternative B rejected:** Unvalidated performance
**Alternative D rejected:** Speculative, insufficient evidence
```

### 4. Document Risks

**Risk categories:**

1. **Technical risks:**
   - Implementation complexity
   - Performance unknown
   - Integration challenges

2. **Evidence risks:**
   - Novel combination (unvalidated)
   - Missing precedents
   - Speculative components

3. **Evaluation risks:**
   - Custom evaluation needed
   - Benchmark not standardized
   - Ground truth unclear

4. **Timeline risks:**
   - May exceed estimate
   - Unexpected blockers
   - Resource constraints

**Risk structure:**
```yaml
risks:
  - category: technical
    description: "Higher complexity than baseline vector-only"
    severity: moderate
    mitigation: "Phase implementation, start with retrieval then add evolution"

  - category: evidence
    description: "No direct precedent for full lifecycle model"
    severity: moderate
    mitigation: "Validate incrementally, publish findings"

  - category: evaluation
    description: "May require custom evaluation methodology"
    severity: moderate
    mitigation: "Use rule-derived ground truth, borrow from P-001 benchmarks"

  - category: timeline
    description: "Novel approach may exceed 3-5 day estimate"
    severity: low
    mitigation: "Accept extended timeline if needed"
```

### 5. Link Evidence References

**Evidence traceability:**

For every claim in decision:
- Link to specific evidence source
- Use IDs: P-001, B-002, J-001
- Reference type: proven, suggests, inferred

**Example traceability:**
```markdown
## Decision Rationale

**Why hybrid fusion selected:**
- Retrieval improvement proven: [P-001](../index/papers-index.md#p-001)
- Lifecycle framework proposed: [P-002](../index/papers-index.md#p-002)
- Formation threshold formalized: [P-003](../index/papers-index.md#p-003)
- Judgment conclusion: [J-001](judgment-J-001.md#main-conclusion)

**Why baseline rejected:**
- Insufficient retention: [P-001](../index/papers-index.md#p-001) shows 72% vs. target 80%
- Lifecycle unsupported: No evidence in [evidence-Q-001.md](evidence-Q-001.md#open-gaps)

**Why graph-only rejected:**
- Unvalidated performance: [P-002](../index/papers-index.md#p-002) suggests but doesn't prove
```

### 6. Create Architecture Decision Document

**Metadata:**
```yaml
---
id: DEC-001
type: architecture-decision
version: 1.0.0
question_id: Q-001
judgment_id: J-001
plan_id: PLAN-001
alternatives_count: 4
selected_alternative: C
alternatives:
  - id: A
    description: "Vector-only memory"
    selected: false
    reason: "Baseline, validated in P-001"
  - id: C
    description: "Hybrid fusion with lifecycle stages"
    selected: true
    reason: "Addresses gap identified in J-001"
risks:
  - "Higher complexity than baseline"
  - "No direct precedent for lifecycle model"
  - "May require custom evaluation"
evidence_refs: [P-001, P-002, P-003, B-001, J-001]
created_at: 2026-04-11T14:00:00Z
updated_at: 2026-04-11T14:00:00Z
status: draft
dependencies: [Q-001, J-001]
gate_b_passed: null
---
```

**Content structure:**
```markdown
# Architecture Decision: {topic}

## Decision

**Selected approach:** Hybrid vector-graph fusion with lifecycle stages

**Question:** [Q-001](brief-Q-001.md#question)
**Judgment:** [J-001](judgment-J-001.md#main-conclusion)

## Alternatives

### Alternative A: Vector-only memory
**Description:** Traditional vector database approach
**Evidence:** [P-001](../index/papers-index.md#p-001) validates as baseline
**Pros:** Simpler, lower latency, production-tested
**Cons:** Limited retention (72% vs. 84%), no lifecycle
**Selected:** No — insufficient for lifecycle needs

### Alternative C: Hybrid fusion with lifecycle (SELECTED)
**Description:** Vector-graph hybrid with formation, evolution, retrieval stages
**Evidence:** [P-001](../index/papers-index.md#p-001) proven, [P-002](../index/papers-index.md#p-002) suggests framework
**Pros:** Best retrieval, lifecycle support, addresses gap
**Cons:** Higher complexity, novel combination
**Selected:** Yes — addresses primary gap

### Alternative D: Hybrid with adaptive mode-switching
**Description:** Dynamic switching between vector-only and hybrid modes
**Evidence:** [B-003](../index/blogs-index.md#b-003) blog proposes (speculative)
**Pros:** Flexibility
**Cons:** Speculative, complex logic
**Selected:** No — insufficient evidence

## Selection Rationale

**Why Alternative C selected:**
1. **Evidence support:** Strong (P-001 proven retrieval improvement)
2. **Gap addressing:** Addresses lifecycle gap (J-001 conclusion)
3. **Feasibility:** Moderate complexity, aligned with timeline

**Trade-offs accepted:**
- Higher complexity ↔ Comprehensive lifecycle support
- Novel combination ↔ Extends proven mechanisms

## Risks

### Technical: Higher complexity
- **Mitigation:** Phase implementation (retrieval → evolution)

### Evidence: No direct precedent
- **Mitigation:** Validate incrementally, publish findings

### Evaluation: Custom methodology needed
- **Mitigation:** Rule-derived ground truth, adapt P-001 benchmarks

## Evidence Traceability

| Claim | Evidence | Type |
|-------|----------|------|
| Hybrid improves retrieval | [P-001](../index/papers-index.md#p-001) | proven |
| Lifecycle framework | [P-002](../index/papers-index.md#p-002) | suggests |
| Formation threshold | [P-003](../index/papers-index.md#p-003) | proven |
| Lifecycle neglected | [J-001](judgment-J-001.md) | judgment |

## Implementation Plan

1. **Phase 1:** Implement retrieval (vector-graph fusion)
2. **Phase 2:** Add formation mechanism (importance threshold)
3. **Phase 3:** Add evolution mechanism (lifecycle management)

## Next Steps

Proceed to Gate B review before implementation.
```

### 7. Present Gate B Review

**Gate B: Before Architecture Implementation**

**Position:** Before proceeding to evaluation
**Purpose:** Ensure architecture decision sound

**Gate B checks:**
- [ ] Alternatives documented (≥3)
- [ ] Risks stated
- [ ] Evidence refs valid
- [ ] Selection rationale clear

**Gate B review process:**

1. Display decision document
2. Show gate criteria checklist
3. Ask user confirmation:
   ```
   ⚠️  GATE B: Before Implementation

   Review criteria:
   [✓] Alternatives documented: 4 alternatives (A, B, C, D)
   [✓] Risks stated: 3 risks documented
   [✓] Evidence refs valid: P-001, P-002, P-003, J-001
   [✓] Selection rationale clear

   Decision: Hybrid fusion with lifecycle (Alternative C)

   Proceed with decision? [Y/n/modify]
   ```

4. If user approves:
   - Mark `gate_b_passed: true` in decision metadata
   - Record timestamp and reviewer
   - Proceed to next step

5. If user rejects:
   - Ask: "What needs modification?"
   - Offer options: [Add alternative] [Revise risks] [Change selection]
   - Loop until approved or user cancels

### 8. Update Skill Tree

**After Gate B passed:**
- Mark `omr-decision` as complete ✓
- Unlock `omr-evaluation` as ready ○

### 9. Prompt Next Action

```
✓ Alternatives: A (vector-only), B (graph-only), C (hybrid fusion), D (adaptive)
✓ Selected: C (hybrid fusion with lifecycle)
✓ Risks: Higher complexity, no precedent, custom evaluation needed

⚠️  GATE B: Before Implementation
Criteria:
[✓] Alternatives documented
[✓] Risks stated
[✓] Evidence refs valid

Proceed? [Y/n]

User: Y

System: ✓ Gate B passed
        ✓ Decision: decision-DEC-001.md
        📊 Skill tree: omr-evaluation [READY]

        Next step: `/omr-evaluation` to validate decision
```

## Gates

**Gate B: Architecture decision sound?**

**Position:** Before proceeding to evaluation
**Checks:**
1. Alternatives documented (≥3 alternatives required)
2. Risks stated (all risks identified and documented)
3. Evidence refs valid (all claims link to evidence)
4. Selection rationale clear (reason for selection explained)

**Enforcement:**
- User confirmation required (default mode)
- Auto-pass if explicitly configured for agents

**Gate failure handling:**
- If Gate B fails: "Decision incomplete. Options: [Add alternatives] [Document risks] [Link evidence]"
- Do not unlock `omr-evaluation` until gate passed

## Can Call

None

## Prerequisites

- Evidence map exists (required)
- Judgment summary may exist (optional, improves decision quality)
- If evidence map missing: Error "Run `/omr-evidence` first."

## Examples

### Example 1: Gate B passed
```
User: /omr-decision

System: ✓ Reading evidence...
        ✓ Generating alternatives...

        Alternatives:
        A. Vector-only (baseline, P-001 validated)
        B. Graph-only (P-002 suggests)
        C. Hybrid fusion (P-001 + P-002, addresses gap)
        D. Adaptive hybrid (B-003 proposes, speculative)

        Selected: C (addresses lifecycle gap from J-001)

        Risks: Higher complexity, no precedent

        ⚠️  GATE B: Before Implementation
        [✓] Alternatives: 4
        [✓] Risks: 3 documented
        [✓] Evidence refs: valid
        [✓] Rationale: clear

        Proceed? [Y/n]

User: Y

System: ✓ Gate B passed
        ✓ Decision: decision-DEC-001.md
        📊 Skill tree: omr-evaluation [READY]
```

### Example 2: Gate B failed (insufficient alternatives)
```
User: /omr-decision

System: ✓ Generating alternatives...

        Alternatives generated: 2
        A. Vector-only
        B. Hybrid fusion

        ⚠️  GATE B: Before Implementation
        [✗] Alternatives: 2 (< 3 required)
        [✓] Risks: documented
        [✓] Evidence refs: valid

        Gate B failed: Insufficient alternatives

        Options:
        [1] Generate more alternatives
        [2] Accept 2 alternatives (proceed anyway)
        [3] Manual alternative input

User: 1

System: Generating additional alternatives...
        Added: C. Graph-only, D. Adaptive hybrid

        Alternatives: 4
        Proceed? [Y/n]
```

### Example 3: Alternative modification
```
User: /omr-decision

System: Alternatives:
        A. Vector-only
        B. Graph-only
        C. Hybrid fusion

        Selected: C

        Proceed? [Y/n/modify]

User: modify

System: What to modify?
        [1] Alternatives
        [2] Risks
        [3] Selection

User: 1

System: Current alternatives:
        A. Vector-only
        B. Graph-only
        C. Hybrid fusion

        Add alternative? [y/N]

User: y

System: Enter alternative description:

User: Vector-graph hybrid with separate evolution module

System: ✓ Added: D. Vector-graph hybrid with separate evolution module

        Updated alternatives: 4
        Proceed? [Y/n/modify]
```

### Example 4: Missing prerequisites
```
User: /omr-decision

System: ⚠️  Missing prerequisites:
        - evidence-map.md not found

        Cannot proceed without evidence.

        Run `/omr-evidence` first.

        Aborting...
```

### Example 5: Idea-First pattern (no prior evidence)
```
User: /omr-decision

System: ⚠️  No evidence map found.
        Pattern detected: Idea-First

        Proceed without evidence? [Y/n]

User: Y

System: ✓ Generating alternatives (speculative basis)...

        Alternatives:
        A. Baseline approach (industry standard)
        B. Novel approach from idea
        C. Hybrid of baseline + novel

        ⚠️  Note: No evidence support — decision speculative

        Risks: Unvalidated, requires evidence backfill later

        Proceed? [Y/n]

User: Y

System: ✓ Decision created (speculative basis)
        ✓ Note: Run `/omr-evidence` to backfill evidence
        📊 Skill tree: omr-evaluation [READY]
```

## What NOT to Do

- Do NOT proceed without evidence map (unless Idea-First pattern confirmed)
- Do NOT skip Gate B review (user must confirm)
- Do NOT unlock `omr-evaluation` if Gate B failed
- Do NOT generate < 3 alternatives (Gate B requires ≥3)
- Do NOT select alternative without rationale
- Do NOT make claims without evidence references
- Do NOT use deep-research reports as primary evidence (Tier 3 only)
- Do NOT claim "proven" for speculative alternatives

## Success Criteria

- [ ] Decision document created
- [ ] ≥3 alternatives documented
- [ ] Selected alternative clearly identified
- [ ] Rationale documented for selection
- [ ] Risks stated
- [ ] Evidence references valid and linked
- [ ] Gate B review presented
- [ ] Gate B passed (user approved)
- [ ] `gate_b_passed: true` recorded in metadata
- [ ] Skill tree updated (unlock `omr-evaluation`)

## Edge Cases

### Idea-First pattern

If evidence map missing but Idea-First pattern active:
- Allow proceeding without evidence
- Generate alternatives on speculative basis
- Note: "Decision speculative — requires evidence backfill"
- Gate B: Relax evidence ref requirement
- Still require alternatives + risks

### Decision-First pattern

If Decision-First pattern active:
- Skip Gate A (not required)
- Proceed directly to decision
- Allow decision without judgment summary
- Gate B still required (alternatives + risks)

### Contradictory evidence

If evidence contradicts alternatives:
- Note in decision: "Evidence contradiction detected"
- Alternative A supported by P-001
- Alternative B supported by P-005 (contradicts P-001)
- Selection: Document trade-off between contradictory evidence
- Risk: "Resolution needed — comparative study required"

### Single obvious alternative

If only one alternative is clearly superior:
- Still generate ≥3 alternatives (Gate B requirement)
- Document rejected alternatives with rationale
- Gate B: Pass if ≥3 alternatives documented

### Speculative novel approach

If selected alternative is novel (no direct evidence):
- Document as "Novel, extends evidence"
- Link to evidence: "Combines P-001 (retrieval) + P-002 (framework)"
- Risk: "Novel combination, unvalidated"
- Gate B: Pass if risks documented

## Integration with Other Skills

**After decision:**
- Unlock `omr-evaluation` for validation
- Prepare for Gate C review

**Before decision:**
- Requires `omr-evidence` for evidence map (unless Idea-First)
- May use `omr-research-plan` judgment (improves decision quality)

**Reconciliation:**
- If new evidence contradicts decision, `omr-reconcile` may call this skill to re-decide

**Pattern flexibility:**
- Evidence-First: Gate B required, evidence refs required
- Idea-First: Gate B required, evidence refs relaxed
- Decision-First: Gate B required, may proceed without judgment
- Experiment-First: Gate B may be relaxed