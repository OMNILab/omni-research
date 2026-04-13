---
name: omr-evidence
description: Define research questions and map the evidence landscape by analyzing collected materials. Creates research brief with clear scope and success criteria, and evidence map showing primary evidence, supporting materials, and open gaps. Uses strict evidence boundaries (proven, suggested, inferred). Triggers automatically when materials are ready for analysis. Use when user asks to "analyze papers", "map evidence", "define research scope", or says "now what" after collecting materials. REQUIRES omr-core skill and workspace with collected materials.
version: 1.0.0
author: OmniResearch Team
license: MIT
metadata:
  requires_skills: [omr-core]
  requires_workspace: true
  category: evidence-analysis
  phase: 2.2
---

# omr-evidence: Map Evidence Landscape

## Purpose

Define research questions and map the evidence landscape from collected materials. This skill transforms raw materials into a structured research brief and evidence map with clear boundaries between proven, suggested, and inferred findings.

## Trigger

```
/omr-evidence
```

**No arguments required** — operates on materials in `raw/` directory

**Automatic trigger conditions:**
- After `omr-collection` completes with ≥1 paper
- User explicitly requests evidence analysis
- User asks "now what" or "analyze these papers"

## What This Skill Does

### 1. Scan Raw Materials

**Required prerequisite:**
- At least 1 material in `raw/` directory
- `docs/index/papers-index.json` must exist

**Scan process:**
1. Read `docs/index/papers-index.json` for paper list
2. Read `docs/index/blogs-index.json` for blog list
3. Read `docs/index/github-index.json` for GitHub repos
4. Count materials per tier

**If no materials found:**
- Error: "No materials in `raw/`. Run `/omr-collection` first."
- Do not proceed

### 2. Extract Key Findings

For each paper in `raw/paper/`:
1. Read abstract (from index metadata)
2. If abstract missing, attempt to extract from PDF (using text parsing)
3. Identify key contributions stated by authors
4. Note methodology (theoretical, empirical, survey)
5. Extract limitations acknowledged by authors
6. Map to evidence strength:
   - "We prove X" → `proven`
   - "We demonstrate X" → `suggests`
   - "We hypothesize X" → `inferred`
   - "X may be" → `speculative` (exclude from evidence)

**Evidence strength classification:**

| Author Statement | Evidence Boundary | Usage in Research |
|------------------|-------------------|-------------------|
| "We prove X" | proven | Can anchor claims |
| "We demonstrate/show X" | suggests | Supporting evidence |
| "We hypothesize/propose X" | inferred | Lead for further investigation |
| "X may be/could be" | speculative | Exclude from evidence map |

**Non-negotiable rule:**
Never claim "paper proves X" when authors only "suggest" or "demonstrate".

### 3. Generate Research Brief

Create `docs/plans/brief-{id}.md`:

**Metadata:**
```yaml
---
id: Q-001
type: research-brief
version: 1.0.0
question: "How do AI agents maintain long-term memory?"
scope: "Lifecycle mechanisms for agent memory"
non_goals: ["Retrieval optimization only", "Short-term memory (< 1 day)"]
success_criteria:
  - "Identify formation patterns"
  - "Map evolution strategies"
  - "Compare retrieval mechanisms"
created_at: 2026-04-11T11:30:00Z
updated_at: 2026-04-11T11:30:00Z
status: draft
dependencies: [COL-001]
---
```

**Content structure:**
```markdown
# Research Brief: {question}

## Research Question

{Primary question derived from material themes}

## Scope

**Included:**
- {Scope definition}

**Excluded (Non-goals):**
- {Non-goals to prevent scope creep}

## Success Criteria

- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

## Material Coverage

- Papers analyzed: {N}
- Blogs analyzed: {M}
- GitHub repos: {K}

## Evidence Sources

Primary evidence: {N papers}
Supporting evidence: {M blogs}
Implementation references: {K repos}

## Next Steps

Proceed to `/omr-research-plan` to synthesize judgment from evidence.
```

**Question derivation:**
- Extract common themes from paper titles/abstracts
- If multiple themes, generate primary + secondary questions
- Ask user to confirm: "Detected question: '{question}'. Accept? [Y/n/edit]"

### 4. Generate Evidence Map

Create `docs/plans/evidence-{id}.md`:

**Metadata:**
```yaml
---
id: Q-001
type: evidence-map
version: 1.0.0
question_id: Q-001
primary_evidence: [P-001, P-002, P-003]
supporting_evidence: [B-001, B-002]
open_gaps:
  - "No longitudinal studies on memory evolution"
  - "Evaluation methodology lacks standardization"
  - "Formation mechanisms underexplored"
papers_analyzed: 10
blogs_analyzed: 3
github_analyzed: 2
created_at: 2026-04-11T11:30:00Z
updated_at: 2026-04-11T11:30:00Z
status: draft
dependencies: [COL-001]
---
```

**Content structure:**
```markdown
# Evidence Map: {question}

## Primary Evidence (Tier 1)

### P-001: Memory Systems for AI Agents
- **Finding:** Hybrid vector-graph memory improves retrieval accuracy
- **Evidence:** proven (validated with benchmarks)
- **Limitations:** Evaluated on short-term tasks only (max 7 days)
- **Relevance:** Directly addresses formation mechanisms

### P-002: Long-term Memory in Agents
- **Finding:** Memory lifecycle comprises formation, evolution, retrieval
- **Evidence:** suggests (empirical demonstration on simulated tasks)
- **Limitations:** No real-world validation
- **Relevance:** Defines lifecycle framework

### P-003: Memory Formation Patterns
- **Finding:** Importance threshold determines memory persistence
- **Evidence:** proven (mathematical derivation)
- **Relevance:** Formalizes formation criteria

## Supporting Evidence (Tier 2)

### B-001: Production Memory Systems
- **Finding:** Engineering implementations use vector databases
- **Evidence:** suggests (case studies from industry)
- **Relevance:** Practical validation of hybrid approaches

### B-002: Memory Evolution in Practice
- **Finding:** Manual pruning required to prevent memory bloat
- **Evidence:** inferred (blog proposes, no validation)
- **Relevance:** Highlights evolution challenges

## Implementation References (Tier 4)

### GH-001: Agent Memory Framework
- **Type:** Reference implementation
- **Approach:** Vector-only memory
- **Relevance:** Baseline for comparison

## Open Gaps

1. **No longitudinal studies:** Memory evolution over weeks/months unexplored
2. **Evaluation methodology unclear:** No standardized benchmarks for lifecycle
3. **Formation mechanisms underexplored:** Theory exists, practical implementation lacking

## Evidence Boundaries

**Proven:**
- Hybrid memory improves retrieval (P-001)
- Importance threshold determines persistence (P-003)

**Suggested:**
- Lifecycle comprises formation, evolution, retrieval (P-002)
- Vector databases used in production (B-001)

**Inferred:**
- Manual pruning needed (B-002, blog proposes)

**Not Evidence:**
- Speculative claims excluded from map

## Coverage Analysis

- Papers: 10 analyzed, 3 primary evidence
- Blogs: 3 analyzed, 2 supporting
- GitHub: 2 reference implementations

**Coverage assessment:** Moderate — key mechanisms identified, but gaps in longitudinal validation and evaluation methodology.
```

### 5. Update Skill Tree

After evidence map created:
- Unlock `omr-research-plan` (mark as ready ○)
- Keep `omr-evidence` marked as complete ✓

### 6. Display Summary

Show evidence landscape to user:
```
Research Question: "How do AI agents maintain long-term memory?"
Scope: Lifecycle mechanisms (formation, evolution, retrieval)

Primary Evidence:
- P-001: Vector + graph fusion improves retrieval [proven]
- P-002: Memory lifecycle framework defined [suggests]
- P-003: Importance threshold formalized [proven]

Open Gaps:
- No longitudinal studies on memory evolution
- Evaluation methodology lacks standardization

✓ Generated: brief-Q-001.md, evidence-Q-001.md
📊 Skill tree: omr-research-plan [READY]
```

## Metadata

**Evidence state:**
```yaml
---
id: Q-001
type: evidence-map
version: 1.0.0
primary_evidence_count: 3
supporting_evidence_count: 2
open_gaps_count: 2
coverage_assessment: moderate
created_at: 2026-04-11T11:30:00Z
status: draft
dependencies: [COL-001]
---
```

## Implementation Details

### Question Derivation Algorithm

```
1. Collect all paper titles
2. Extract keywords from abstracts
3. Identify common themes:
   - Count keyword frequency
   - Group related concepts
   - Select top 3 themes

4. Formulate question:
   - If single dominant theme: "How does {theme} work?"
   - If multiple themes: "What are the {theme1}, {theme2}, and {theme3} mechanisms?"

5. Ask user confirmation:
   - Display detected question
   - Options: [Accept] [Edit] [Reject and provide own]
```

### Scope Definition

**Included scope:**
- Derived from primary evidence focus
- Align with success criteria
- Broad enough to cover evidence, narrow enough to be tractable

**Excluded scope (non-goals):**
- Common scope creep areas:
  - Related but distinct topics (e.g., retrieval-only optimization)
  - Out-of-domain applications
  - Implementation details not in evidence

### Evidence Boundary Detection

**Language cues for boundary classification:**

| Phrase | Boundary | Example |
|--------|----------|---------|
| "we prove", "proof of", "theorem" | proven | "We prove that X reduces latency by 15%" |
| "we demonstrate", "we show", "results indicate" | suggests | "We demonstrate improved accuracy" |
| "we propose", "we hypothesize", "we conjecture" | inferred | "We propose a new mechanism" |
| "may", "could", "might", "possibly" | speculative | "This could improve performance" |
| "should", "would likely" | speculative | "This should reduce cost" |

**Boundary enforcement:**
- If paper claims "prove", classify as `proven`
- If paper claims "show/demonstrate", classify as `suggests`
- If paper claims "propose/hypothesize", classify as `inferred`
- If paper uses speculative language, **exclude from evidence map**

**Critical rule:**
Never upgrade evidence strength. If paper "suggests" X, never write "proven" in evidence map.

### Gap Detection

**Gap categories:**

1. **Methodological gaps:**
   - No longitudinal studies
   - Missing benchmarks
   - Evaluation unclear

2. **Evidence gaps:**
   - Key mechanism unvalidated
   - Contradictory findings
   - Missing real-world validation

3. **Implementation gaps:**
   - Theory exists, practice missing
   - Engineering challenges unaddressed
   - Tooling insufficient

**Gap identification process:**
1. Read limitations sections of papers
2. Check for "future work" mentions
3. Compare claims vs. validation
4. Note contradictions between papers

### Evidence Linking

**Cross-reference format:**
```markdown
### P-001: Memory Systems
- **Finding:** Hybrid memory improves retrieval
- **Evidence:** proven (benchmarks validated)
- **Links to:** P-002 (lifecycle framework), B-001 (production validation)
```

**Dependency tracking:**
- Note which papers cite each other
- Identify supporting papers (cite primary paper)
- Map evidence clusters (papers supporting same claim)

## Gates

None (Gate A is on `omr-research-plan`)

## Can Call

None

## Prerequisites

- Materials in `raw/` directory (required)
- If empty: Error "Run `/omr-collection` first."

## Examples

### Example 1: Basic evidence mapping
```
User: /omr-evidence

System: ✓ Scanning materials...
        Papers: 10, Blogs: 3, GitHub: 2

        ✓ Extracting key findings...

        Detected research question:
        "How do AI agents maintain long-term memory?"

        Accept? [Y/n/edit]

User: Y

System: ✓ Research brief generated: brief-Q-001.md
        ✓ Evidence map generated: evidence-Q-001.md

        Primary Evidence (proven):
        - P-001: Hybrid memory improves retrieval
        - P-003: Importance threshold formalized

        Supporting Evidence (suggests):
        - P-002: Lifecycle framework defined
        - B-001: Production validation

        Open Gaps:
        - No longitudinal studies
        - Evaluation methodology unclear

        📊 Skill tree: omr-research-plan [READY]
```

### Example 2: Question editing
```
User: /omr-evidence

System: Detected research question:
        "How do AI agents maintain long-term memory?"

        Accept? [Y/n/edit]

User: edit

System: Enter your question:

User: What mechanisms enable long-term memory persistence in AI agents?

System: ✓ Question updated
        ✓ Research brief generated with custom question
        ✓ Evidence map generated
```

### Example 3: Insufficient evidence
```
User: /omr-evidence

System: ⚠️  No materials found in `raw/`
        Cannot proceed without evidence sources.

        Run `/omr-collection` first to add papers, blogs, or other materials.

        Aborting...
```

### Example 4: Evidence boundary warning
```
User: /omr-evidence

System: ✓ Extracting findings from P-005...

        ⚠️  Evidence boundary violation detected:
        Paper P-005 claims "We show that X improves performance"
        Cannot be classified as "proven" — classified as "suggests"

        Never claim "paper proves X" when it only "shows" X.

        Evidence map updated with correct boundary: suggests
```

### Example 5: Gap-heavy evidence landscape
```
User: /omr-evidence

System: ✓ Evidence map generated

        ⚠️  Coverage assessment: Weak
        Open gaps: 5 critical, 3 moderate

        Critical gaps:
        - No empirical validation of core mechanism
        - Contradictory findings between P-001 and P-002
        - Missing standard evaluation methodology

        Recommendation: Add more materials via `/omr-collection` before proceeding to planning.

        Proceed anyway? [Y/n]
```

## What NOT to Do

- Do NOT claim papers "prove" findings when they only "suggest"
- Do NOT include speculative findings in evidence map
- Do NOT proceed without materials in `raw/`
- Do NOT auto-generate research question without user confirmation
- Do NOT skip gap detection (always analyze limitations)
- Do NOT claim complete coverage when gaps exist
- Do NOT use deep-research reports as primary evidence (Tier 3 only)

## Success Criteria

- [ ] Research brief created with clear question, scope, non-goals
- [ ] Evidence map created with primary + supporting evidence
- [ ] Evidence boundaries correctly assigned (proven/suggests/inferred)
- [ ] Open gaps identified and documented
- [ ] Cross-references between papers noted
- [ ] Skill tree updated (unlock `omr-research-plan`)
- [ ] User confirmed research question
- [ ] Coverage assessment provided

## Edge Cases

### Single paper

If only 1 paper:
- Generate brief with narrow scope
- Evidence map: 1 primary evidence
- Note: "Coverage limited — add more materials recommended"
- Still proceed (Gate A will catch insufficient evidence)

### Contradictory evidence

If papers contradict:
- Note in evidence map: "Contradiction detected"
- Evidence: P-001 claims X, P-002 claims ¬X
- Gap: "Resolution needed — comparative study required"
- Do not resolve contradiction (that's `omr-research-plan`'s job)

### Missing abstracts

If paper lacks abstract:
- Attempt PDF text extraction
- If fails: Use title as placeholder
- Note in evidence map: "Abstract missing — manual review needed"
- Ask user: "Paper {ID} lacks abstract. Provide summary? [y/N]"

### Deep-research reports

If deep-research reports present (Tier 3):
- Include in evidence map with clear label: "lead-only"
- Note: "Not anchor evidence — use as exploration leads only"
- Do not classify as primary or supporting evidence

### Non-English papers

If papers not in English:
- Note in evidence map: "Non-English content"
- Use abstract if provided in English
- Otherwise: "Requires translation — manual review needed"

## Integration with Other Skills

**After evidence:**
- Unlock `omr-research-plan` for judgment synthesis
- Prepare for Gate A review

**Before evidence:**
- Requires `omr-collection` for materials

**Reconciliation:**
- If new materials added later, `omr-reconcile` may call this skill to update evidence map