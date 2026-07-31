---
name: omr-bootstrap
description: Initialize a new omni-research project workspace. Creates only AGENTS.md and .omr/tree-state.json; content directories are created on demand by later skills. Displays skill tree showing available next actions. Use whenever starting a new research project, even if user doesn't explicitly say "bootstrap" or mentions "new project", "start research", "initialize workspace", or provides a research topic they want to investigate.
license: MIT
metadata:
  version: "1.1.0"
  author: OmniResearch Team
  requires_skills: omr-core
  requires_workspace: false
  category: project-setup
  phase: 1.0
---

# omr-bootstrap: Initialize Research Workspace

## Purpose

Initialize a minimal omni-research project workspace with project context and skill-tree state. This is the entry point for all omni-research projects.

## Invocation

```
/omr-bootstrap "<topic>"
```

**Required argument:** `<topic>` - Research topic string (e.g., "agent memory mechanisms", "quantum computing error correction")

## What This Skill Does

### 1. Create Minimal Workspace Files

Create only the files required at init. Do **not** pre-create empty content folders.

```
<workspace>/<project-id>/
├── AGENTS.md                 # Project context for AI agents
└── .omr/
    └── tree-state.json       # Skill progression state
```

Content directories are created on demand by skills when they first write:

| Path | Created by |
|------|------------|
| `materials/papers\|web\|github\|datasets\|search\|failed/` | `omr-collection` |
| `docs/index/` | `omr-collection` / `omr-idea-note` |
| `docs/ideas/` | `omr-idea-note` |
| `docs/plans/` | `omr-analyze` / `omr-decision` / `omr-evaluation` |
| `docs/archive/` | `omr-reconcile` |
| `docs/survey\|report\|manuscript\|brief/` | `omr-synthesis` |
| `wiki/` | `omr-synthesis` |
| `src/` | `omr-evaluation` |

**Directory naming:** Use the topic as the project-id, converting to lowercase and replacing spaces with hyphens. Example: "agent memory mechanisms" → `agent-memory-mechanisms/`.

**Working directory:** Create the workspace in the current directory or ask user for preferred location if unclear.

### 2. Generate AGENTS.md

Create `AGENTS.md` with project metadata, skill tree state, and next-step guidance.

### 3. Display Skill Tree

Show the current skill tree state:

```
omr-bootstrap ✓
    │
    ├── omr-collection ○  (ready)
    │       │
    │       ├── omr-analyze ●  (locked: needs materials/)
    │       │
    │       └── omr-idea-note ✓  (can run anytime)
    │
    └── omr-reconcile ✓  (can run anytime)

Legend:
✓ = available (can run now)
● = locked (missing prerequisites)
○ = ready (prerequisites satisfied, but not run yet)

Next recommended: omr-collection
```

**Update after this skill:** Mark `omr-bootstrap` as ✓ complete, unlock `omr-collection` to ○ ready.

### 4. Prompt for First Action

After workspace creation, present interactive menu:

```
✓ Workspace created at ./{project-id}/
✓ AGENTS.md generated
✓ .omr/tree-state.json initialized
(materials/, docs/, wiki/, src/ will be created on demand)

What's your first action?

[1] I have papers to collect — start with materials (Evidence-First pattern)
[2] I have an idea to explore — start with insight (Idea-First pattern)
[3] I have a decision to validate — start with architecture (Decision-First pattern)
[4] I have a hypothesis to test — start with building (Experiment-First pattern)
[5] I need to deepen ideas/evidence — Loop pattern (Gate L cycles)
[6] I'm exploring — no specific goal yet

Choose [1-6] or describe your intent:
```

**Pattern detection:** Note the user's choice — this will influence pattern emergence later (after 3+ skill invocations).

**If user chooses [5] Loop:** Activate loop state after first skill:
- Idea deepening → `activate_loop(..., mode="idea-dev")` then suggest `/omr-idea-note`
- Materials deepening → `activate_loop(..., mode="deep-analyze")` then suggest `/omr-collection`

## Implementation Notes

**Topic handling:**
- Preserve original topic capitalization in `AGENTS.md` header
- Use lowercase-hyphenated form for directory name
- Extract keywords from topic for metadata

**Timestamp generation:**
- Use current system time in ISO-8601 format
- Generate project-id with timestamp suffix if duplicate exists: `agent-memory-20260411T103000/`

**State and specs:**
- Static contracts, schemas, and built-in patterns remain in installed `omr-core`
- Do not copy installed skills or static OMR specifications into the workspace
- Store mutable, self-contained OMR state under `.omr/`
- Do not pre-create empty content directories; create parents when writing files

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
        ✓ AGENTS.md generated
        ✓ .omr/tree-state.json initialized
        (materials/, docs/, wiki/, src/ will be created on demand)

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

## What NOT to Do

- Do NOT prompt for pattern selection at bootstrap (patterns emerge later)
- Do NOT pre-create empty content directories (`materials/`, `docs/survey/`, `wiki/`, `src/`, etc.)
- Do NOT create empty index placeholders; indexes are created when first written
- Do NOT create any artifacts beyond `AGENTS.md` and `.omr/tree-state.json`
- Do NOT invoke other skills automatically (wait for user choice)
- Do NOT generate research questions or decisions (those are later skills)
- Do NOT create a workspace `skills/` directory or copy installed skills into the project

## Success Criteria

- [ ] Workspace contains `AGENTS.md` and `.omr/tree-state.json` only (plus parents)
- [ ] No empty content directories created
- [ ] AGENTS.md generated with correct metadata
- [ ] Skill tree displayed
- [ ] User prompted for first action
- [ ] No other skills invoked
- [ ] Project-id follows naming convention (lowercase-hyphenated)
