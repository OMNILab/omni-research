---
name: omr-core
description: Foundation infrastructure for OmniResearch skills system. Provides contract system, dependency resolver, skill tree tracking, and pattern definitions. MUST install this before any other omr-* skills. Use when setting up OmniResearch environment or when skills report missing infrastructure dependencies. Automatically invoked by omr-bootstrap to initialize workspace infrastructure.
version: 1.0.0
author: OmniResearch Team
license: MIT
metadata:
  role: infrastructure-provider
  provides:
    - contracts (11 skill dependency definitions)
    - dependency_resolver (prerequisite checking)
    - skill_tree (progression tracking)
    - patterns (5 research workflow patterns)
  required_for:
    - omr-bootstrap
    - omr-collection
    - omr-evidence
    - omr-research-plan
    - omr-decision
    - omr-evaluation
    - omr-synthesis
    - omr-wiki
    - omr-idea-note
    - omr-reconcile
    - omr-research-archive
---

# omr-core: OmniResearch Infrastructure Foundation

## Purpose

Provides the foundational infrastructure for the OmniResearch skills system. This skill contains all shared utilities, contract definitions, pattern definitions, and state tracking mechanisms that other OmniResearch skills depend on.

## Invocation

```
/omr-core --init <workspace-path>
```

**Primary mode**: Infrastructure initialization (called by omr-bootstrap)

## What This Skill Provides

### 1. Contract System

**Location**: `contracts/*.json` (11 files)

Each contract defines:
- **Skill identifier**: Unique `omr-*` pattern name
- **Requires**: Artifact prerequisites (files, directories, metadata)
- **Produces**: Artifact outputs (with optional schema validation)
- **Gates**: Quality checkpoints (user-confirm, auto-pass, auto-fail)
- **Modes**: Configurable output variants (survey, report, manuscript, brief)

**Contract files**:
- `omr-bootstrap.json` - Workspace initialization contract
- `omr-collection.json` - Material collection contract
- `omr-evidence.json` - Evidence extraction contract
- `omr-research-plan.json` - Research planning contract
- `omr-decision.json` - Architecture decision contract
- `omr-evaluation.json` - Experiment execution contract
- `omr-synthesis.json` - Findings synthesis contract
- `omr-wiki.json` - Wiki generation contract
- `omr-idea-note.json` - Idea capture contract
- `omr-reconcile.json` - Reconciliation contract
- `omr-research-archive.json` - Archive snapshot contract

**Validation schema**: `schemas/contract.schema.json`

### 2. Dependency Resolver

**Script**: `scripts/dependency_resolver.py`

**Purpose**: Check skill prerequisites before invocation

**Features**:
- Load contract from JSON definition
- Verify required artifacts exist in workspace
- Determine if skill is unlocked/ready/locked
- Update downstream skills after artifact production
- Generate skill tree state transitions

**Usage**:
```python
from dependency_resolver import DependencyResolver

resolver = DependencyResolver(
    contracts_dir=Path('contracts/'),
    workspace_root=Path('/path/to/project'),
    tree_state_path=Path('tree/tree-state.json')
)

# Check if skill can be invoked
can_invoke, missing = resolver.can_invoke_skill('omr-evidence')

# Update skill tree after producing artifacts
resolver.update_downstream_skills(['evidence-map.md'])
```

### 3. Skill Tree Tracker

**Script**: `scripts/skill_tree.py`

**Purpose**: Track skill progression states

**States**:
- **unlocked**: Available but prerequisites not satisfied
- **ready**: Prerequisites satisfied, can be invoked
- **locked**: Hard dependencies not met
- **completed**: Skill executed successfully

**Visualization**:
```bash
python scripts/skill_tree.py            # Forward dependency view
python scripts/skill_tree.py --reverse  # Reverse producer view
```

**State file**: `tree/tree-state.json`

### 4. Pattern Definitions

**Location**: `patterns/*.json` (5 files)

**Purpose**: Define research workflow patterns that emerge from skill invocation sequences

**Patterns**:
- `evidence-first.json` - Start with literature collection → evidence → plan → decision → synthesis
- `idea-first.json` - Start with creative insight → collection → evidence → plan → decision → synthesis
- `decision-first.json` - Start with architectural stance → collection → evidence → plan → evaluation → synthesis
- `experiment-first.json` - Start by building/testing → collection → evidence → plan → evaluation → synthesis
- `rapid-prototype.json` - Fast iteration: idea → collection → evaluation → decision → synthesis

**Pattern detection**: `scripts/detect_pattern.py`

### 5. Contract Validation

**Script**: `scripts/validate_contract.py`

**Purpose**: Validate all contract JSON files against schema

**Usage**:
```bash
python scripts/validate_contract.py
```

**Output**: Reports valid contracts or schema violations

## Infrastructure Initialization

**Script**: `scripts/init_workspace.py`

**Purpose**: Set up workspace infrastructure structure

**What it creates**:
```
<workspace>/
├── skills/
│   ├── contracts/       # Copy of all 11 contract JSON files
│   ├── schemas/         # Copy of contract validation schema
│   ├── patterns/        # Copy of 5 pattern JSON files
│   ├── tree/
│   │   └── tree-state.json  # Initial skill tree state
│   └── shared/          # Scripts directory (symlink or copy)
│       ├── dependency_resolver.py
│       ├── skill_tree.py
│       ├── validate_contract.py
│       └── detect_pattern.py
└── docs/
    └── index/
        ├── .gitkeep
        ├── artifacts-index.json (empty)
        └── versions/
            └── .gitkeep
```

**Invocation**:
```python
python scripts/init_workspace.py /path/to/workspace
```

**Error handling**:
- If workspace exists: Ask user to confirm overwrite/merge/cancel
- If missing permissions: Report error with alternative suggestions
- If invalid path: Report validation error

## Installation Requirements

**For marketplace users**:
1. Install omr-core skill first (before any other OmniResearch skills)
2. omr-core provides infrastructure that other skills import at runtime
3. Skills check for omr-core presence and report errors if missing

**For skill developers**:
1. Domain skills must include `runtime_utils.py` to load infrastructure
2. Skills declare dependency via SKILL.md metadata: `requires_skills: [omr-core]`
3. Skills use `load_infrastructure()` utility to resolve paths

## Marketplace Distribution

**Package size**: ~104KB

**Contents**:
- 11 contract JSON files (~4KB each)
- 1 contract schema (~2KB)
- 5 pattern JSON files (~3KB each)
- 4 Python scripts (resolver, tree, validate, detect) ~15KB total
- 1 init_workspace.py script ~8KB
- 1 tree-state.json ~1KB

**Installation location**: `~/.claude/skills/omr-core/`

## What NOT to Do

- Do NOT invoke omr-core manually for routine research (it's infrastructure)
- Do NOT modify contracts directly in workspace (use skill contracts)
- Do NOT skip installing omr-core before domain skills
- Do NOT assume workspace infrastructure exists without initialization

## Dependencies

**This skill has NO dependencies** - it's the foundation layer.

All other OmniResearch skills depend on this skill.

## Success Criteria

- [ ] All 11 contracts valid against schema
- [ ] Dependency resolver functional
- [ ] Skill tree visualization working
- [ ] Pattern detection operational
- [ ] Workspace initialization successful
- [ ] Scripts executable without errors

## Version History

- **1.0.0** (2026-04-13): Initial marketplace release
  - Moved all shared infrastructure from skills/shared/
  - Added version, author, license metadata
  - Created init_workspace.py for setup
  - Packaged as standalone skill for marketplace