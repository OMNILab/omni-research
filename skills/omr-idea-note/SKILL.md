---
name: omr-idea-note
description: Capture speculative thoughts and creative insights outside formal research pipeline. Creates timestamped idea notes that can be linked to decisions and experiments later. Available anytime during research process. Supports Idea-First research pattern where creative thinking precedes evidence collection. Use when user wants to "capture idea", "record insight", "note hypothesis", or "save thought".
---

# omr-idea-note: Capture Creative Insights

## Purpose

Capture speculative thoughts and creative insights outside the formal research pipeline. This skill provides a lightweight mechanism for documenting ideas that may later inspire decisions, hypotheses, or research directions, supporting both Idea-First and exploratory research patterns.

## Trigger

```
/omr-idea-note "<insight>"
```

**Required argument:** `<insight>` - Text content or structured insight

**Examples:**
- `/omr-idea-note "What if memory behaves like quantum superposition?"`
- `/omr-idea-note "Hypothesis: Threshold dynamic based on context"`
- `/omr-idea-note --structured '{"title": "...", "insight": "..."}'`

## What This Skill Does

### 1. Accept Insight Content

**Insight formats:**

**Freeform text:**
```
/omr-idea-note "What if agent memory behaves like quantum superposition — holding multiple states simultaneously?"
```

**Structured JSON:**
```
/omr-idea-note --structured '{"title": "Quantum Memory Superposition", "insight": "Memory could hold multiple states like quantum superposition", "tags": ["speculative", "physics-inspired"], "linked_to": []}'
```

**Markdown file:**
```
/omr-idea-note --file ./my-idea.md
```

**Direct input:**
```
/omr-idea-note
System: Enter your insight (multi-line supported):
User: What if memory works like quantum superposition?
      Memory could exist in multiple states simultaneously
      This would allow flexible context switching
      <end>
```

### 2. Generate Idea Metadata

**Idea metadata:**
```yaml
---
id: IDEA-001
type: idea-note
timestamp: 20260411T103000
slug: quantum-memory-superposition
title: "Quantum Memory Superposition"
insight: "What if agent memory behaves like quantum superposition — holding multiple states simultaneously?"
tags:
  - speculative
  - physics-inspired
  - novel-mechanism
linked_decisions: []
linked_experiments: []
linked_artifacts: []
created_at: 2026-04-11T10:30:00Z
updated_at: 2026-04-11T10:30:00Z
status: draft
dependencies: []  # Standalone, no dependencies
---
```

**Metadata generation:**

1. **ID generation:**
   - Format: `IDEA-{sequence}`
   - Sequence: Incremental (IDEA-001, IDEA-002, ...)

2. **Timestamp:**
   - Format: `YYYYMMDDTHHMMSS`
   - Example: `20260411T103000`

3. **Slug generation:**
   - Extract keywords from insight
   - Lowercase, hyphenated
   - Example: "Quantum memory superposition" → `quantum-memory-superposition`

4. **Tags:**
   - Auto-detect: speculative, hypothesis, novel-mechanism
   - User-provided: if structured input
   - Default: [speculative]

### 3. Create Idea Document

**Idea document structure:**
```markdown
---
id: IDEA-001
type: idea-note
timestamp: 20260411T103000
slug: quantum-memory-superposition
tags: [speculative, physics-inspired]
---

# Quantum Memory Superposition

**Captured:** 2026-04-11T10:30:00Z

## Insight

What if agent memory behaves like quantum superposition — holding multiple states simultaneously?

## Context

This idea emerged from thinking about how agents handle multiple contexts. Quantum superposition allows particles to exist in multiple states until observed/measured.

## Potential Applications

- Multi-context agents (different contexts simultaneously)
- Flexible task switching (no single dominant memory state)
- Probabilistic retrieval (multiple relevant memories)

## Speculative Hypothesis

If memory exists in superposition:
- Retrieval would select based on observation (task context)
- Multiple relevant memories could coexist
- State collapse occurs upon explicit selection

## Novelty

No evidence for quantum-inspired memory in current research (see [evidence-Q-001.md](../plans/evidence-Q-001.md)).

This is purely speculative, inspired by physics analogy.

## Next Steps

- [ ] Link to decision if inspiring architecture choice
- [ ] Link to experiment if testing hypothesis
- [ ] Evaluate feasibility (is quantum analogy useful?)

## Tags

- speculative (unvalidated)
- physics-inspired (analogy)
- novel-mechanism (no precedent)

## Links

**Linked to:** None yet

**Can link later:**
- If inspires decision: Link to DEC-XXX
- If tested in experiment: Link to EXP-XXX
- If explored in research: Link to Q-XXX

## Status

Draft (speculative, not yet linked to research artifacts)

## Version History

- v1.0.0: Initial capture (2026-04-11T10:30:00Z)
```

### 4. Store Idea Note

**Storage location:**

```
docs/ideas/
├── idea-20260411T103000-quantum-memory-superposition.md
├── idea-20260411T110000-contextual-thresholds.md
├── idea-20260411T120000-evolution-feedback-loop.md
└── ideas-index.json
```

**Ideas index:**
```json
{
  "ideas": [
    {
      "id": "IDEA-001",
      "timestamp": "20260411T103000",
      "slug": "quantum-memory-superposition",
      "title": "Quantum Memory Superposition",
      "tags": ["speculative", "physics-inspired"],
      "created_at": "2026-04-11T10:30:00Z",
      "file": "docs/ideas/idea-20260411T103000-quantum-memory-superposition.md",
      "linked_to": []
    }
  ],
  "last_updated": "2026-04-11T10:30:00Z"
}
```

### 5. Offer Next Actions

**Prompt user for next steps:**

```
✓ Idea captured: IDEA-001
✓ Saved: docs/ideas/idea-20260411T103000-quantum-memory-superposition.md

Tags: speculative, physics-inspired

What's next?

[1] Keep as idea (no further action)
[2] Link to existing decision (if inspiring architecture)
[3] Create decision from idea (Idea-First pattern)
[4] Create hypothesis for experiment (Experiment-First pattern)
[5] Just save (return to research)

Choose [1-5] or describe intent:
```

**If user chooses:**

**Option 1: Keep as idea**
```
System: ✓ Idea saved for future reference
        No further action needed

        Idea will remain in docs/ideas/ for future linking

        ✓ Complete
```

**Option 2: Link to existing decision**
```
System: ✓ Linking to existing decision...

        Available decisions:
        - DEC-001: Hybrid fusion with lifecycle

        Select decision to link:

User: DEC-001

System: ✓ Linked: IDEA-001 → DEC-001
        ✓ Updated: decision-DEC-001.md (idea_refs: [IDEA-001])
        ✓ Idea note updated (linked_decisions: [DEC-001])

        Idea now linked to decision
```

**Option 3: Create decision from idea (Idea-First)**
```
System: ✓ Creating decision from idea...

        Idea: Quantum memory superposition

        This is speculative (no evidence support).
        Proceed with Idea-First pattern? [Y/n]

User: Y

System: ✓ Auto-triggering `/omr-decision` (Idea-First basis)

        Note: Decision will be speculative (no evidence backfill yet)
        Recommend: Run `/omr-evidence` after decision to backfill
```

**Option 4: Create hypothesis for experiment**
```
System: ✓ Creating hypothesis from idea...

        Hypothesis: "Quantum-inspired memory superposition improves context switching"

        Auto-triggering `/omr-evaluation` (Experiment-First basis)

        Note: Hypothesis speculative, needs validation
```

**Option 5: Just save**
```
System: ✓ Saved
        Return to research whenever ready
```

### 6. Link to Future Artifacts

**Linking mechanism:**

When future decision/experiment created:
- Check ideas index for related tags
- Prompt: "This decision relates to IDEA-001. Link? [y/N]"
- If yes: Add `idea_refs: [IDEA-001]` to decision metadata

**Automatic linking suggestions:**

During `/omr-decision`:
```
System: ✓ Generating alternatives...

        ⚠️  Idea detected: IDEA-001 "Quantum memory superposition"
        This idea may inspire Alternative D.

        Include as alternative? [y/N]

User: y

System: ✓ Added: Alternative D (quantum-inspired superposition)
        ✓ Linked: DEC-001 → IDEA-001
```

### 7. Update Skill Tree

**Skill tree state:**

- `omr-idea-note` available anytime (can run anytime)
- No prerequisites required
- Does not unlock/lock other skills
- Standalone skill

**Skill tree example:**
```
omr-bootstrap ✓
    │
    ├── omr-collection ● (locked)
    │       │
    │       ├── omr-evidence ●
    │       │
    │       └── omr-idea-note ✓ (can run anytime) ← Available
    │
    └── omr-reconcile ✓ (can run anytime)
```

## Gates

None (idea capture is lightweight, no gates)

## Can Call

None (standalone skill)

## Can Be Called By

- Any skill (available anytime)
- `omr-bootstrap`: Suggests Idea-First pattern via idea note
- `omr-decision`: May link to idea for inspiration
- `omr-evaluation`: May link to idea for hypothesis

## Prerequisites

None (can run anytime, even before `omr-bootstrap`)

**Note:** If workspace not initialized:
- Create `docs/ideas/` directory first
- Proceed with idea capture

## Examples

### Example 1: Basic idea capture
```
User: /omr-idea-note "What if memory behaves like quantum superposition?"

System: ✓ Generating idea metadata...
        ✓ ID: IDEA-001
        ✓ Slug: quantum-memory-superposition

        ✓ Saved: docs/ideas/idea-20260411T103000-quantum-memory-superposition.md

        Tags: speculative, physics-inspired

        What next?
        [1] Keep as idea
        [2] Link to decision
        [3] Create decision
        [5] Just save

User: 5

System: ✓ Saved for future reference
```

### Example 2: Structured input
```
User: /omr-idea-note --structured '{"title": "Contextual Thresholds", "insight": "Threshold should adapt based on task context", "tags": ["hypothesis", "adaptive"]}'

System: ✓ Parsing structured input...

        Title: Contextual Thresholds
        Insight: Threshold should adapt based on task context
        Tags: hypothesis, adaptive

        ✓ ID: IDEA-002
        ✓ Saved: docs/ideas/idea-20260411T110000-contextual-thresholds.md

        What next?
```

### Example 3: Multi-line input
```
User: /omr-idea-note

System: Enter your insight (multi-line, type <end> to finish):

User: Evolution could use feedback loop
      Memory state changes based on retrieval success
      Failed retrieval → prune
      Successful retrieval → reinforce
      <end>

System: ✓ Multi-line insight captured...

        Title: Evolution Feedback Loop
        Insight: Evolution could use feedback loop based on retrieval success...

        ✓ ID: IDEA-003
        ✓ Saved

        What next?
```

### Example 4: Link to decision
```
User: /omr-idea-note "Threshold should be context-adaptive"

System: ✓ Saved: IDEA-002

        What next?

User: 2 (link to decision)

System: Available decisions:
        - DEC-001: Hybrid fusion with lifecycle

        Link to DEC-001? [Y/n]

User: Y

System: ✓ Linked: IDEA-002 → DEC-001
        ✓ Decision updated (idea_refs: [IDEA-002])
        ✓ Idea updated (linked_decisions: [DEC-001])

        Idea now influences decision
```

### Example 5: Create decision (Idea-First)
```
User: /omr-idea-note "Quantum memory superposition"

System: ✓ Saved: IDEA-001

        What next?

User: 3 (create decision)

System: ✓ Creating decision from idea (Idea-First pattern)

        Idea: Quantum memory superposition
        Evidence: None (speculative)

        Proceed without evidence? [Y/n]

User: Y

System: ✓ Auto-triggering `/omr-decision`

        Note: Decision will be speculative basis
        Recommend: Backfill evidence later with `/omr-evidence`

        Starting `/omr-decision`...
```

### Example 6: Pre-bootstrap idea
```
User: /omr-idea-note "I have an idea about memory systems"

System: ⚠️  Workspace not initialized

        Creating docs/ideas/ directory...

        ✓ Saved: docs/ideas/idea-XXX.md

        Note: Run `/omr-bootstrap` to initialize workspace

        Idea saved anyway (available for linking later)
```

### Example 7: File input
```
User: /omr-idea-note --file ./my-idea.md

System: ✓ Reading file ./my-idea.md...

        Content:
        Title: Evolution Feedback Loop
        Insight: Evolution uses retrieval success as feedback...

        ✓ ID: IDEA-003
        ✓ Saved: docs/ideas/idea-XXX.md

        What next?
```

## What NOT to Do

- Do NOT require evidence for ideas (ideas are speculative)
- Do NOT force linking to decisions (ideas can stay standalone)
- Do NOT auto-trigger decision creation without user approval
- Do NOT validate ideas (no gates, no validation)
- Do NOT require workspace initialization (can run pre-bootstrap)
- Do NOT claim ideas as findings (ideas ≠ validated results)

## Success Criteria

- [ ] Insight content captured
- [ ] Idea metadata generated (ID, timestamp, slug)
- [ ] Idea document created in `docs/ideas/`
- [ ] Ideas index updated
- [ ] User prompted for next actions
- [ ] Optional: Linked to decision/experiment (if user requests)

## Edge Cases

### Empty insight

If user provides empty insight:
- Prompt: "Insight content required. Enter your idea:"
- If still empty: Error "Cannot capture empty idea."

### Duplicate slug

If idea slug already exists:
- Append timestamp: `quantum-memory-superposition-20260411T103000`
- Proceed with unique slug

### Pre-bootstrap idea

If workspace not initialized:
- Create `docs/ideas/` directory
- Proceed with idea capture
- Note: "Run `/omr-bootstrap` to initialize workspace"

### Very long insight

If insight > 1000 characters:
- Prompt: "Insight very long. Summarize or keep full? [summarize/full]"
- If summarize: Extract key sentences
- If full: Keep entire content

### Multiple ideas at once

If user provides multiple ideas:
- Prompt: "Multiple ideas detected. Capture separately? [Y/n]"
- If yes: Create multiple idea notes sequentially
- If no: Combine into single idea note

### Non-text insight

If user provides image/code/non-text:
- Prompt: "Non-text insight. Describe or attach file? [describe/file]"
- If describe: Convert to text description
- If file: Link to file path

## Integration with Other Skills

**Available anytime:**
- Can run before `omr-bootstrap`
- Can run during any research stage
- Can run after synthesis complete

**Can be called by:**
- `omr-bootstrap`: "Start with idea" option → calls `/omr-idea-note`
- `omr-decision`: May suggest linking to existing ideas
- `omr-evaluation`: May link idea as hypothesis source

**Links to future artifacts:**
- Ideas can link to decisions (if inspiring architecture)
- Ideas can link to experiments (if tested as hypothesis)
- Ideas can link to research questions (if explored)

**Idea-First pattern:**
```
omr-idea-note → omr-decision → omr-evaluation → omr-evidence → omr-synthesis → omr-wiki
```

Idea captured first, then decision created (speculative basis), then evaluation tests hypothesis, then evidence backfills support, then synthesis documents findings.

**Standalone mode:**
Ideas can remain standalone (never linked to formal artifacts), serving as creative inspiration bank.

## Use Cases

### Idea-First research

User has creative insight before evidence collection:
1. Capture idea: `/omr-idea-note`
2. Create decision from idea (Idea-First)
3. Test hypothesis: `/omr-evaluation`
4. Backfill evidence: `/omr-evidence`
5. Synthesize findings

### Exploratory thinking

User exploring without specific goal:
- Capture multiple ideas as they emerge
- Review ideas later for research directions
- Select promising idea to formalize

### Creative breaks

User during formal research:
- Capture speculative thoughts outside pipeline
- Ideas don't block formal progress
- Link later if relevant

### Hypothesis generation

User needs hypothesis for experiment:
- Capture idea as hypothesis source
- Link to experiment spec
- Test idea via evaluation

### Innovation tracking

User tracking novel mechanisms:
- Capture all novel ideas
- Review for innovation potential
- Select for investigation