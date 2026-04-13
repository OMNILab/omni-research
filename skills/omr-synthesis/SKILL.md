---
name: omr-synthesis
description: Write authoritative research findings in configurable output formats (survey chapters, industry reports, academic manuscripts, or executive briefs). Ensures traceability by linking every claim to evidence, decisions, or experiments. Enforces strict evidence boundaries (proven, suggested, inferred). Enforces Gate D review - checks results traceable, evidence boundaries stated, and no over-claiming. Use when user wants to "write up findings", "document results", "create survey", or "publish research". REQUIRES omr-core skill and workspace with completed research.
version: 1.0.0
author: OmniResearch Team
license: MIT
metadata:
  requires_skills: [omr-core]
  requires_workspace: true
  category: findings-documentation
  phase: 3.1
---

# omr-synthesis: Document Research Findings

## Purpose

Write authoritative research findings with configurable output format. This skill transforms evaluation results, decisions, and evidence into structured documents with strict traceability and evidence boundaries, ensuring every claim is linked to sources and no over-claiming occurs.

## Trigger

```
/omr-synthesis [--mode <mode>]
```

**Optional argument:** `--mode <mode>` - Override default synthesis mode
- Modes: `survey`, `report`, `manuscript`, `brief`

**Default mode:** Determined by pattern config or user preference

**Prerequisites:**
- Evaluation report OR judgment summary (required)
- Architecture decision (implicit, for decision context)
- Evidence map (implicit, for evidence references)

## What This Skill Does

### 1. Determine Output Mode

**Mode selection:**

| Source | Priority |
|--------|----------|
| `--mode` flag | Highest (user override) |
| Pattern config | Medium (Evidence-First → survey, Decision-First → report) |
| Default | Lowest (survey) |

**Mode characteristics:**

| Mode | Structure | Depth | Evidence Boundaries | Output Dir |
|------|-----------|-------|---------------------|------------|
| `survey` | Chapters (01-07) | Comprehensive | Explicit per section | `docs/survey/` |
| `report` | Structured findings | Medium | Key findings only | `docs/report/` |
| `manuscript` | Paper format | Deep | Academic rigor | `docs/manuscript/` |
| `brief` | Executive summary | Minimal | Top-level only | `docs/brief/` |

**Mode selection logic:**
```
1. Check --mode flag
   If provided: use specified mode

2. Check pattern config
   If Evidence-First: survey (comprehensive)
   If Decision-First: report (structured)
   If Idea-First: brief (quick)
   If Experiment-First: brief (quick)

3. Default
   If no pattern: survey (most comprehensive)
```

### 2. Read Input Artifacts

**Required:**
- Evaluation report: `docs/plans/report-{id}.md` (if evaluation complete)
- OR Judgment summary: `docs/plans/judgment-{id}.md` (if evidence-only)

**If neither exists:**
- Error: "Missing results. Run `/omr-evaluation` or `/omr-evidence` first."
- Do not proceed

**Optional:**
- Architecture decision: `docs/plans/decision-{id}.md`
- Research plan: `docs/plans/plan-{id}.md`
- Evidence map: `docs/plans/evidence-{id}.md`

### 3. Generate Structure

**Survey structure (7 chapters):**

```
docs/survey/
├── 00-introduction.md       # Context, motivation, scope
├── 01-framework.md          # Conceptual framework
├── 02-formation.md          # Formation mechanisms
├── 03-evolution.md          # Evolution mechanisms
├── 04-retrieval.md          # Retrieval mechanisms
├── 05-evaluation.md         # Evaluation methodology
├── 06-implementation.md     # Implementation insights
└── 07-conclusion.md         # Summary, contributions, future work
```

**Report structure (structured findings):**

```
docs/report/
├── executive-summary.md     # Key findings overview
├── findings-01.md           # Finding 1 with evidence
├── findings-02.md           # Finding 2
├── findings-03.md           # Finding 3
├── methodology.md           # Approach, evaluation
├── recommendations.md       # Actionable recommendations
└── appendix.md              # Detailed data, references
```

**Manuscript structure (academic paper):**

```
docs/manuscript/
├── abstract.md              # Abstract (250 words)
├── introduction.md          # Introduction
├── related-work.md          # Literature review
├── methodology.md           # Methods
├── experiments.md           # Experiments, results
├── discussion.md            # Discussion, limitations
├── conclusion.md            # Conclusion
└── references.md            # Bibliography
```

**Brief structure (executive summary):**

```
docs/brief/
├── overview.md              # Research question, scope
├── key-findings.md          # Top 3 findings
├── results.md               # Evaluation results summary
├── implications.md          # Implications, recommendations
└── next-steps.md            # Future directions
```

### 4. Write Chapters/Sections

**Content generation principles:**

1. **Traceability:** Every claim links to evidence/decision/experiment
2. **Evidence boundaries:** Distinguish proven, suggested, inferred
3. **No over-claiming:** Never say "proves" when evidence only "suggests"

**Survey chapter example (02-formation.md):**

```markdown
# Chapter 2: Memory Formation

## 2.1 Overview

Memory formation is the process by which information is encoded into long-term memory storage. This chapter examines formation mechanisms identified in our research.

## 2.2 Importance Threshold Mechanism

**Key finding:** Importance threshold determines memory persistence

**Evidence:** proven
- [P-003](../index/papers-index.md#p-003) proves that importance threshold > 0.7 leads to retention
- Mathematical derivation validates threshold existence

**Evidence boundary:** This finding is **proven** by mathematical proof in P-003.

**Our validation:** We implemented this mechanism in our prototype (see [EXP-001](../plans/report-EXP-001.md#formation-implementation)).

**Results:** Our evaluation shows 84% retention (vs. baseline 72%), confirming importance threshold effectiveness.

**Traceability:** P-003 → Formation mechanism → EXP-001 validation → Retention improvement

## 2.3 Vector-Graph Fusion for Formation

**Key finding:** Hybrid fusion improves formation efficiency

**Evidence:** suggests
- [P-001](../index/papers-index.md#p-001) demonstrates 16.7% retention improvement
- Empirical validation shows improvement, but mechanism not proven

**Evidence boundary:** This finding is **suggested** by empirical demonstration in P-001. The exact mechanism is not proven.

**Our contribution:** We extended P-001's hybrid approach to include lifecycle stages (see [DEC-001](../plans/decision-DEC-001.md#alternative-c)).

**Novelty:** Hybrid + lifecycle combination is novel (no precedent in evidence).

**Risk:** Novel combination requires further validation (see [Limitations](#limitations)).

## 2.4 Formation in Practice

**Evidence:** inferred
- [B-001](../index/blogs-index.md#b-001) reports production systems using vector databases
- [B-002](../index/blogs-index.md#b-002) proposes formation heuristics

**Evidence boundary:** These are **inferred** from industry practice. No validation provided.

**Observation:** Industry uses simpler formation mechanisms than research proposes.

## 2.5 Limitations

- Formation mechanisms well-studied for retrieval, but evolution-underexplored (see [J-001](../plans/judgment-J-001.md#open-gaps))
- No longitudinal studies on formation persistence (see [Evidence Gaps](../plans/evidence-Q-001.md#open-gaps))
- Our evaluation limited to 7-day interval (see [EXP-001](../plans/report-EXP-001.md#limitations))

## 2.6 Summary

- Importance threshold: proven (P-003)
- Hybrid fusion: suggested (P-001)
- Production practices: inferred (B-001, B-002)
- Our contribution: Hybrid + lifecycle (validated in EXP-001)

**Confidence:** High for threshold, medium for fusion, low for practices
```

**Evidence boundary enforcement:**

| Evidence Type | Language | Example |
|---------------|----------|---------|
| proven | "proves", "validates", "establishes" | "P-003 proves threshold > 0.7" |
| suggests | "demonstrates", "shows", "indicates" | "P-001 demonstrates 16.7% improvement" |
| inferred | "proposes", "suggests", "observes" | "B-001 proposes production heuristics" |
| NOT ALLOWED | "proves" for "suggests" evidence | ❌ "P-001 proves fusion improves" |

**Non-negotiable rule:**
Never claim "paper proves X" when it only "suggests" or "demonstrates" X.

### 5. Link Traceability

**Cross-reference format:**

```markdown
**Evidence:** [P-001](../index/papers-index.md#p-001) demonstrates...
**Decision:** [DEC-001](../plans/decision-DEC-001.md#alternative-c) selected hybrid...
**Experiment:** [EXP-001](../plans/report-EXP-001.md#results) validates...
**Judgment:** [J-001](../plans/judgment-J-001.md#main-conclusion) concludes...
```

**Traceability chain:**

Every claim should show:
```
Evidence → Decision → Experiment → Synthesis
P-001 → DEC-001 → EXP-001 → Chapter 2.3
```

### 6. Generate Metadata

**Synthesis metadata:**
```yaml
---
id: SYN-001
type: synthesis
version: 1.0.0
mode: survey
question_id: Q-001
decision_ids: [DEC-001]
experiment_ids: [EXP-001]
judgment_ids: [J-001]
chapters:
  - title: "Introduction"
    file: "00-introduction.md"
  - title: "Framework"
    file: "01-framework.md"
  - title: "Formation"
    file: "02-formation.md"
  - title: "Evolution"
    file: "03-evolution.md"
  - title: "Retrieval"
    file: "04-retrieval.md"
  - title: "Evaluation"
    file: "05-evaluation.md"
  - title: "Implementation"
    file: "06-implementation.md"
  - title: "Conclusion"
    file: "07-conclusion.md"
chapters_count: 8
total_pages: ~50
created_at: 2026-04-11T17:00:00Z
updated_at: 2026-04-11T17:00:00Z
status: draft
dependencies: [EXP-001, DEC-001, Q-001]
gate_d_passed: null
---
```

### 7. Present Gate D Review

**Gate D: Before Publication**

**Position:** Before finalizing synthesis
**Purpose:** Ensure traceability and prevent over-claiming

**Gate D checks:**
- [ ] Results traceable to hypotheses
- [ ] Evidence boundaries stated
- [ ] No over-claiming ("proves" vs. "suggests")
- [ ] Cross-references valid

**Gate D review process:**

1. Display synthesis summary
2. Show gate criteria checklist
3. Ask user confirmation:
   ```
   ⚠️  GATE D: Before Publish

   Review criteria:
   [✓] Results traceable: All claims linked to evidence/decision/experiment
   [✓] Evidence boundaries: proven/suggests/inferred clearly stated
   [✓] No over-claiming: P-001 says "demonstrates", not "proves"
   [✓] Cross-references: All links valid

   Example check:
   - Chapter 2.3: P-001 "demonstrates" → correctly written as "suggests" ✓
   - Chapter 2.2: P-003 "proves" → correctly written as "proven" ✓

   Publish synthesis? [Y/n/modify]
   ```

4. If user approves:
   - Mark `gate_d_passed: true` in metadata
   - Update status: `published`
   - Proceed to wiki generation

5. If user rejects:
   - Ask: "What needs modification?"
   - Offer: [Fix traceability] [Correct boundaries] [Remove over-claiming]
   - Loop until approved or user cancels

### 8. Update Skill Tree

**After Gate D passed:**
- Mark `omr-synthesis` as complete ✓
- Unlock `omr-wiki` as ready ○

### 9. Auto-trigger Wiki Generation

**Automatic trigger:**
After synthesis complete, ask user:
```
✓ Synthesis published: docs/survey/ (8 chapters)

Would you like to generate wiki from synthesis? [Y/n]

User: Y

System: ✓ Auto-triggering `/omr-wiki`
```

If user declines, skip wiki generation.

## Gates

**Gate D: Results traceable, no over-claiming?**

**Position:** Before publishing synthesis
**Checks:**
1. Results traceable to hypotheses (all claims linked)
2. Evidence boundaries stated (proven/suggests/inferred explicit)
3. No over-claiming ("proves" vs. "suggests" enforced)
4. Cross-references valid (all links working)

**Enforcement:**
- User confirmation required (default mode)
- Auto-pass if explicitly configured for agents

**Gate failure handling:**
- If Gate D fails: "Traceability/boundary issue. Options: [Fix links] [Correct boundaries] [Remove over-claiming]"
- Do not mark as published until gate passed

## Can Call

- `omr-wiki` (auto-trigger after gate passed)

## Prerequisites

- Evaluation report OR judgment summary (required)
- If neither: Error "Run `/omr-evaluation` or `/omr-evidence` first."

## Examples

### Example 1: Survey mode (Evidence-First pattern)
```
User: /omr-synthesis

System: ✓ Mode: survey (Evidence-First pattern)
        ✓ Reading evaluation report...
        ✓ Reading decision...
        ✓ Reading evidence map...

        ✓ Generating 8 chapters...

        Chapter 2.3: "Memory Formation with Hybrid Fusion"
        - Evidence: P-001 demonstrates (suggests) ✓
        - Decision: DEC-001 selects hybrid ✓
        - Experiment: EXP-001 validates ✓

        ⚠️  GATE D: Before Publish
        [✓] Results traceable
        [✓] Evidence boundaries stated
        [✓] No over-claiming
        [✓] Cross-references valid

        Publish? [Y/n]

User: Y

System: ✓ Gate D passed
        ✓ Published: docs/survey/ (8 chapters)

        Generate wiki? [Y/n]
```

### Example 2: Brief mode (--mode override)
```
User: /omr-synthesis --mode brief

System: ✓ Mode: brief (user override)
        ✓ Generating executive summary...

        Key Findings:
        1. Importance threshold proven (P-003)
        2. Hybrid fusion suggested (P-001)
        3. Lifecycle mechanism novel (validated in EXP-001)

        ⚠️  GATE D: Before Publish
        [✓] Traceable
        [✓] Boundaries stated
        [✓] No over-claiming

        Publish? [Y/n]
```

### Example 3: Gate D failed (over-claiming)
```
User: /omr-synthesis

System: ⚠️  GATE D: Before Publish
        [✓] Traceable
        [✓] Boundaries stated
        [✗] Over-claiming detected

        Chapter 2.3 line 45:
        "P-001 proves hybrid fusion improves retention"

        ❌ Over-claiming: P-001 says "demonstrates", not "proves"

        Correct to: "P-001 demonstrates hybrid fusion improves retention"

        Fix automatically? [Y/n]

User: Y

System: ✓ Fixed over-claiming
        ✓ Corrected: "P-001 demonstrates"

        Re-checking...
        [✓] All checks passed

        Publish? [Y/n]
```

### Example 4: Missing traceability
```
User: /omr-synthesis

System: ⚠️  GATE D: Before Publish
        [✗] Traceability missing

        Chapter 3.2: "Evolution mechanism improves retention"

        ❌ No evidence link for this claim

        Add traceability:
        [1] Link to experiment: EXP-001 validates evolution
        [2] Link to decision: DEC-001 selects evolution
        [3] Mark as inferred (speculative)

User: 1

System: ✓ Added traceability: EXP-001
        ✓ Claim now traceable

        Re-checking...
        [✓] All checks passed
```

### Example 5: Manuscript mode (academic paper)
```
User: /omr-synthesis --mode manuscript

System: ✓ Mode: manuscript (academic format)
        ✓ Generating paper structure...

        Abstract: 250 words
        Introduction: Context, motivation
        Related Work: Literature review (P-001, P-002, P-003)
        Methodology: Hybrid + lifecycle approach (DEC-001)
        Experiments: Validation results (EXP-001)
        Discussion: Implications, limitations
        Conclusion: Contributions, future work

        ⚠️  GATE D: Academic rigor check
        [✓] Abstract complete
        [✓] References formatted
        [✓] Evidence boundaries academic-standard
        [✓] No over-claiming

        Publish? [Y/n]
```

### Example 6: Judgment-only synthesis (no evaluation)
```
User: /omr-synthesis

System: ⚠️  No evaluation report found.
        Using judgment summary for synthesis.

        Mode: brief (judgment-only synthesis)

        Key Judgment:
        - Retrieval well-studied, lifecycle neglected (J-001)
        - Evidence: moderate weight, manageable gaps

        Note: No experimental validation included.

        Proceed? [Y/n]

User: Y

System: ✓ Synthesis: docs/brief/ (judgment-based)
        ⚠️  No experimental results documented
```

## What NOT to Do

- Do NOT proceed without evaluation or judgment (minimum required)
- Do NOT skip Gate D review (user must confirm)
- Do NOT claim "proves" when evidence only "suggests"
- Do NOT write claims without traceability links
- Do NOT omit evidence boundaries (must state proven/suggests/inferred)
- Do NOT use deep-research reports as primary evidence (Tier 3 only)
- Do NOT generate all 4 modes (only one mode per invocation)

## Success Criteria

- [ ] Synthesis mode determined (from flag or pattern)
- [ ] Structure generated (chapters/sections per mode)
- [ ] Content written with traceability
- [ ] Evidence boundaries stated explicitly
- [ ] No over-claiming detected
- [ ] Cross-references valid
- [ ] Gate D passed
- [ ] Status updated to `published`
- [ ] Wiki generation triggered (if user approves)

## Edge Cases

### Judgment-only synthesis

If evaluation not complete:
- Use judgment summary as basis
- Mode: brief (less comprehensive)
- Note: "No experimental validation documented"
- Gate D: Relax experiment traceability requirement

### Partial evaluation

If evaluation partially complete:
- Document completed results
- Note incomplete sections
- Recommendation: "Complete evaluation for comprehensive synthesis"

### Mixed evidence boundaries

If claim has mixed evidence:
- Document: "Partially supported"
- Evidence: P-001 suggests, P-003 proves threshold
- Boundary: "Threshold proven, fusion suggested"

### No novel contribution

If decision is baseline (not novel):
- Document: "Validated existing approach"
- Contribution: "Reproduction and validation"
- Do not claim novelty

### Contradictory results

If results contradict hypothesis:
- Document honestly: "Hypothesis not supported"
- Evidence: EXP-001 shows retention decrease
- Recommendation: "Revisit decision"
- Do not hide contradiction

## Integration with Other Skills

**After synthesis:**
- Auto-trigger `omr-wiki` for living knowledge base
- Prepare for research completion

**Before synthesis:**
- Requires evaluation or judgment (minimum)
- Uses decision for decision context
- Uses evidence map for references

**Reconciliation:**
- If new evidence contradicts synthesis, `omr-reconcile` may call this skill to update

**Pattern flexibility:**
- Evidence-First: Survey mode, Gate D required
- Decision-First: Report mode, Gate D required
- Idea-First: Brief mode, Gate D required
- Experiment-First: Brief mode, Gate D may be relaxed

**Output reuse:**
- Survey chapters → Wiki concept pages
- Report findings → Wiki summaries
- Manuscript → Publication-ready
- Brief → Quick reference