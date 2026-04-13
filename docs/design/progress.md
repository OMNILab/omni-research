# Skill Tree: Progress Visualization

## Game-Inspired Model

Skills unlock progressively based on artifact prerequisites, similar to game skill trees.

**Example state:**
```
omr-bootstrap ✓
    │
    ├── omr-collection ✓  (papers downloaded)
    │       │
    │       ├── omr-evidence ○  (ready to run)
    │       │       │
    │       │       └── omr-research-plan ●  (locked: needs evidence-map.md)
    │       │
    │       └── omr-idea-note ✓  (can run anytime)
    │
    └── omr-reconcile ✓  (can run anytime)
```

**Legend:**
- ✓ = complete (artifact produced)
- ○ = ready to run (prerequisites satisfied)
- ● = locked (missing prerequisites)

## Prerequisite System

Each skill has explicit prerequisites (from contracts):

| Skill | Prerequisites | Unlocks After Completion |
|-------|---------------|--------------------------|
| `omr-collection` | workspace | `omr-evidence` |
| `omr-evidence` | materials in raw/ | `omr-research-plan` |
| `omr-research-plan` | evidence-map.md | `omr-decision` |
| `omr-decision` | evidence-map.md (judgment optional) | `omr-evaluation` |
| `omr-evaluation` | architecture-decision.md | `omr-synthesis` |
| `omr-synthesis` | evaluation-report OR judgment | `omr-wiki` |

## Always-Unlocked Skills

- `omr-idea-note` — Standalone, anytime
- `omr-reconcile` — Iteration support, anytime
- `omr-research-archive` — Snapshot, anytime

## Dual View Mode

### Forward View: "What can I do next?"
- Explore possibilities
- See unlocked skills
- Good for open-ended research

**Display:**
```
Available skills:
[✓] omr-evidence (ready)
[●] omr-research-plan (locked: needs evidence-map.md)
[✓] omr-idea-note (anytime)
```

### Reverse View: "I want to produce X. What skills do I need?"
- Goal-driven planning
- Shortest path resolution
- Good for deadline research

**Example:**
```
Goal: Produce survey
Path: 
  1. omr-collection ✓
  2. omr-evidence ○
  3. omr-research-plan ●
  4. omr-decision ●
  5. omr-evaluation ●
  6. omr-synthesis ●

Estimated: 5 skills between you and goal
Missing: 4 artifacts
```

## Skill Tree Updates

Skill tree updates automatically after each skill completion:
1. Mark skill as ✓ complete
2. Check downstream skills for unlock
3. Update any unlocked skills to ○
4. Display updated tree to user

## Toggle Between Views

User can toggle anytime:
- `/omr-tree --forward` → Show forward view
- `/omr-tree --reverse --goal survey` → Show reverse view for goal

## Pattern Integration

Patterns define skill tree paths:
- Evidence-First → Predefined unlock sequence
- Experiment-First → Different starting point, different unlock order
