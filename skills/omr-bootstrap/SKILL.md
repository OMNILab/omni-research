---
name: omr-bootstrap
description: Initialize a new omni-research project workspace. Creates complete directory structure (raw/, docs/, src/, wiki/), generates CLAUDE.md with research context, and displays skill tree showing available next actions. Use whenever starting a new research project, even if user doesn't explicitly say "bootstrap" or mentions "new project", "start research", "initialize workspace", or provides a research topic they want to investigate.
license: MIT
metadata:
  version: "1.0.0"
  author: OmniResearch Team
  requires_skills: omr-core
  requires_workspace: false
  category: project-setup
  phase: 1.0
---

# omr-bootstrap: Initialize Research Workspace

## Purpose

Initialize a complete omni-research project workspace with proper structure, metadata, and AI agent context. This is the entry point for all omni-research projects.

## Invocation

```
/omr-bootstrap "<topic>"
```

**Required argument:** `<topic>` - Research topic string (e.g., "agent memory mechanisms", "quantum computing error correction")

## What This Skill Does

### 1. Create Workspace Directory Structure

Generate the full omni-research workspace hierarchy:

```
<workspace>/<project-id>/
├── raw/                      # Raw material layer
│   ├── paper/                # Downloaded papers (PDF)
│   ├── web/                  # Blogs, URLs, screenshots
│   ├── github/               # Cloned repos
│   ├── models/               # AI model checkpoints, configs
│   ├── datasets/             # Benchmarks, data
│   └── deep-research/        # AI-generated research reports
│
├── docs/                     # Distilled knowledge layer
│   ├── survey/               # Broad survey chapters
│   ├── report/               # Structured findings (industry)
│   ├── manuscript/           # Publication-ready (academic)
│   ├── brief/                # Executive summaries (quick)
│   ├── plans/                # Formal, traceable artifacts
│   ├── ideas/                # Subjective thinking, insights
│   ├── index/                # Machine-readable indexes
│   │   ├── artifacts-index.json
│   │   ├── papers-index.json
│   │   ├── papers-index.md
│   │   ├── versions/
│   │   └── traceability-matrix.md
│   ├── archive/              # Archived materials
│   └── schemas/              # JSON schemas for validation
│
├── src/                      # Generated code projects
│   ├── prototype/            # Reference implementations
│   ├── evaluation/           # Validation experiments
│   └── tools/                # Project-specific utilities
│
├── wiki/                     # Living knowledge base
│   └── README.md             # Auto-generated index
│
└── CLAUDE.md                 # Project context for AI agents
```

**Directory naming:** Use the topic as the project-id, converting to lowercase and replacing spaces with hyphens. Example: "agent memory mechanisms" → `agent-memory-mechanisms/`.

**Working directory:** Create the workspace in the current directory or ask user for preferred location if unclear.

### 2. Generate CLAUDE.md

Create `CLAUDE.md` with:

**Header:** Project metadata and context
```yaml
---
id: PROJ-{timestamp}
type: project
topic: "{topic}"
created_at: {ISO-8601-timestamp}
pattern_detected: null
workspace: ./{project-id}/
status: initialized
---
```

**Content sections:**
```markdown
# {topic} Research Project

## Project Overview
This workspace is initialized for researching {topic}.

## Omni-Research Integration
This project uses omni-research skills for evidence-bound, traceable research.

### Available Skills
- omr-collection: Collect and classify materials
- omr-evidence: Map evidence landscape
- omr-research-plan: Judge evidence and plan research
- omr-decision: Make architectural decisions
- omr-evaluation: Run experiments
- omr-synthesis: Write findings (survey/report/manuscript/brief)
- omr-wiki: Generate wiki
- omr-reconcile: Update state on evidence changes
- omr-idea-note: Capture insights
- omr-research-archive: Snapshot progress

### Evidence Philosophy
- All claims must be traceable to sources
- Evidence boundaries: "proven", "suggested", "inferred"
- Never claim "paper proves X" when it only suggests

## Workspace Structure
See docs/design/architecture.md for detailed structure explanation.

## Next Steps
Choose your research pattern:
- Evidence-First: Start with literature collection
- Idea-First: Start with creative insight
- Decision-First: Start with architectural stance
- Experiment-First: Start by building/testing

Run `/omr-collection` to begin material collection.
```

### 3. Initialize Empty Index Files

Create placeholder files:

- `docs/index/.gitkeep` (empty file, ensures directory exists)
- `docs/index/artifacts-index.json` (empty JSON array: `{"artifacts": []}`)
- `docs/index/versions/.gitkeep` (empty directory)

**Why empty indexes:** These will be populated as artifacts are created by subsequent skills.

### 4. Display Skill Tree

Show the current skill tree state:

```
omr-bootstrap ✓
    │
    ├── omr-collection ●  (locked: ready after workspace created)
    │       │
    │       ├── omr-evidence ●  (locked: needs materials in raw/)
    │       │       │
    │       │       └── omr-research-plan ●  (locked: needs evidence-map.md)
    │       │
    │       └── omr-idea-note ✓  (can run anytime)
    │
    └── omr-reconcile ✓  (can run anytime)
    └── omr-research-archive ✓  (can run anytime)

Legend:
✓ = available (can run now)
● = locked (missing prerequisites)
○ = ready (prerequisites satisfied, but not run yet)

Next recommended: omr-collection
```

**Update after this skill:** Mark `omr-bootstrap` as ✓ complete, unlock `omr-collection` to ○ ready.

### 5. Prompt for First Action

After workspace creation, present interactive menu:

```
✓ Workspace created at ./{project-id}/
✓ CLAUDE.md generated with project context
✓ Directory structure initialized

What's your first action?

[1] I have papers to collect — start with materials (Evidence-First pattern)
[2] I have an idea to explore — start with insight (Idea-First pattern)
[3] I have a decision to validate — start with architecture (Decision-First pattern)
[4] I have a hypothesis to test — start with building (Experiment-First pattern)
[5] I'm exploring — no specific goal yet

Choose [1-5] or describe your intent:
```

**Pattern detection:** Note the user's choice — this will influence pattern emergence later (after 3+ skill invocations).

## Implementation Notes

**Topic handling:**
- Preserve original topic capitalization in `CLAUDE.md` header
- Use lowercase-hyphenated form for directory name
- Extract keywords from topic for metadata

**Timestamp generation:**
- Use current system time in ISO-8601 format
- Generate project-id with timestamp suffix if duplicate exists: `agent-memory-20260411T103000/`

**Schema directory:**
- Copy standard schemas from omni-research source: `docs/schemas/*.schema.json`
- These define validation rules for all artifact types

**Error handling:**
- If directory already exists: Ask user "Workspace exists. Overwrite, merge, or cancel?"
- If insufficient permissions: Error message with suggested alternative location
- If topic invalid (empty string): "Please provide a research topic."

## Examples

### Example 1: Basic initialization
```
User: /omr-bootstrap "agent memory mechanisms"

System: ✓ Creating workspace for "agent memory mechanisms"...

        ✓ Workspace created at ./agent-memory-mechanisms/
        ✓ CLAUDE.md generated
        ✓ Directory structure initialized
        ✓ Index placeholders created

        📊 Skill tree:
        omr-bootstrap ✓
        omr-collection ○ (ready)
        omr-idea-note ✓ (anytime)

        What's your first action?
        [1] I have papers to collect
        [2] I have an idea to explore
        ...
```

### Example 2: Duplicate workspace
```
User: /omr-bootstrap "agent memory"

System: ⚠️  Workspace "agent-memory" already exists.
        Options:
        [1] Overwrite (delete existing, create new)
        [2] Merge (keep existing files, add missing)
        [3] Cancel (abort initialization)

        Choose [1-3]:
```

### Example 3: Alternative location
```
User: /omr-bootstrap "quantum computing"

System: ✓ Creating workspace...
        Current directory: /Users/xiamingchen/projects/
        Workspace created at: /Users/xiamingchen/projects/quantum-computing/

        What's your first action?
        ...
```

## What NOT to Do

- Do NOT prompt for pattern selection at bootstrap (patterns emerge later)
- Do NOT create any artifacts beyond structure and CLAUDE.md
- Do NOT invoke other skills automatically (wait for user choice)
- Do NOT generate research questions or decisions (those are later skills)

## Success Criteria

- [ ] Workspace directory created with full structure
- [ ] CLAUDE.md generated with correct metadata
- [ ] Skill tree displayed showing available next steps
- [ ] User prompted for first action choice
- [ ] No errors in directory creation
- [ ] Project-id follows naming convention (lowercase-hyphenated)