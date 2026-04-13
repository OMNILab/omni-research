# OmniResearch Marketplace Installation Guide

## Overview

OmniResearch is a suite of AI agent skills for accelerating scientific innovation. This guide explains how to install skills from the Claude Code marketplace and set up a research project.

## Architecture

OmniResearch uses a **two-tier architecture**:

- **Tier 1**: `omr-core` - Foundation infrastructure (contracts, dependency resolver, skill tree)
- **Tier 2**: Domain skills - Research workflow skills that depend on omr-core

**Key concept**: All domain skills require `omr-core` to be installed first, as they depend on shared infrastructure for contract validation, dependency resolution, and skill tree tracking.

## Installation Order (REQUIRED)

Skills must be installed in dependency order:

### Step 1: Install Foundation

```
/find-skills omr-core
```

**omr-core** provides:
- Contract system (11 skill dependency definitions)
- Dependency resolver (prerequisite checking)
- Skill tree tracking (progression state)
- Pattern definitions (5 research workflow patterns)

**Size**: ~104KB

### Step 2: Install Project Initializer

```
/find-skills omr-bootstrap
```

**omr-bootstrap** initializes:
- Project directory structure (raw/, docs/, wiki/, src/)
- CLAUDE.md with research context
- Skill tree state
- Artifacts index

**Size**: ~24KB

**Dependencies**: omr-core

### Step 3: Install Domain Skills

Install based on your research pattern needs:

```
/find-skills omr-collection      # Phase 2.1 - Material collection (~112KB)
/find-skills omr-evidence        # Phase 2.2 - Evidence extraction (~28KB)
/find-skills omr-research-plan   # Phase 2.3 - Research planning (~28KB)
/find-skills omr-decision        # Phase 2.4 - Architecture decisions (~36KB)
/find-skills omr-evaluation      # Phase 2.5 - Experiment execution (~36KB)
/find-skills omr-synthesis       # Phase 3.1 - Findings synthesis (~36KB)
/find-skills omr-wiki            # Phase 3.2 - Wiki generation (~24KB)
/find-skills omr-idea-note       # Phase 3.3 - Idea capture (~16KB)
/find-skills omr-reconcile       # Phase 3.4 - Reconciliation (~24KB)
/find-skills omr-research-archive # Phase 3.5 - Archiving (~20KB)
```

**All domain skills depend on**: omr-core + initialized workspace

## Quick Start Workflow

### 1. Install Foundation Skills

```bash
# Install infrastructure
/find-skills omr-core

# Install project initializer
/find-skills omr-bootstrap
```

### 2. Initialize Research Project

```bash
# Create workspace
/omr-bootstrap "my-research-topic" "What research question are you investigating?"

# Example:
/omr-bootstrap "agent-memory-mechanisms" "How do AI agents manage long-term memory?"
```

**This creates**:
- `my-research-topic/` directory with full structure
- `CLAUDE.md` with project context and skill tree
- Infrastructure initialized by omr-core

### 3. Install Domain Skills

Install based on your research pattern:

**Evidence-First Pattern** (literature-driven):
```bash
/find-skills omr-collection  # Collect papers/materials
/find-skills omr-evidence    # Map evidence landscape
/find-skills omr-research-plan # Plan research
/find-skills omr-decision    # Make architecture decisions
/find-skills omr-synthesis   # Write findings
```

**Idea-First Pattern** (insight-driven):
```bash
/find-skills omr-idea-note   # Capture creative insight
/find-skills omr-collection  # Gather supporting materials
/find-skills omr-evidence    # Map evidence landscape
/find-skills omr-research-plan # Plan research
/find-skills omr-decision    # Make decisions based on idea
/find-skills omr-synthesis   # Document findings
```

**Decision-First Pattern** (architecture-driven):
```bash
/find-skills omr-decision    # Document architectural stance
/find-skills omr-collection  # Gather evidence for alternatives
/find-skills omr-evidence    # Map evidence landscape
/find-skills omr-evaluation  # Build and test prototype
/find-skills omr-synthesis   # Document results
```

**Experiment-First Pattern** (test-driven):
```bash
/find-skills omr-collection  # Gather materials
/find-skills omr-evidence    # Map evidence landscape
/find-skills omr-evaluation  # Build and test hypothesis
/find-skills omr-decision    # Make decision from results
/find-skills omr-synthesis   # Document findings
```

### 4. Execute Skills in Workspace

Navigate to your project workspace and invoke skills:

```bash
cd my-research-topic

# Collect materials
/omr-collection "https://arxiv.org/abs/2402.12345"
/omr-collection "github:anthropics/anthropic-sdk-python"
/omr-collection "search:agent memory mechanisms"

# Map evidence
/omr-evidence

# Plan research
/omr-research-plan

# Make decisions
/omr-decision

# Document findings
/omr-synthesis --mode survey  # or --mode report, --mode manuscript, --mode brief
```

## Dependency Checking

Skills automatically check dependencies at runtime:

### Missing omr-core

```
❌ Error: OmniResearch infrastructure not found.
Install omr-core skill first, then initialize workspace with omr-bootstrap.

Installation:
  1. /find-skills omr-core
  2. /omr-bootstrap <project-name> <research-question>
```

### Missing Workspace

```
❌ Error: Workspace not initialized.
Run /omr-bootstrap first to create project structure.

Usage:
  /omr-bootstrap "project-name" "research question?"
```

### Missing Prerequisites

```
❌ Error: Skill prerequisites not satisfied.
Missing artifacts:
  - evidence-map.md (required by omr-research-plan)
  - research-brief.md (required by omr-research-plan)

Run prerequisite skills first:
  /omr-evidence
```

## Skill Package Contents

Each `.skill` file is a ZIP archive containing:

### omr-core Package

```
omr-core.skill (104KB)
├── SKILL.md            # Infrastructure skill specification
├── contracts/          # 11 JSON contract files
│   ├── omr-bootstrap.json
│   ├── omr-collection.json
│   ├── omr-evidence.json
│   ├── omr-research-plan.json
│   ├── omr-decision.json
│   ├── omr-evaluation.json
│   ├── omr-synthesis.json
│   ├── omr-wiki.json
│   ├── omr-idea-note.json
│   ├── omr-reconcile.json
│   └── omr-research-archive.json
├── schemas/
│   └── contract.schema.json
├── patterns/           # 5 research pattern definitions
│   ├── evidence-first.json
│   ├── idea-first.json
│   ├── decision-first.json
│   ├── experiment-first.json
│   └── rapid-prototype.json
├── scripts/
│   ├── dependency_resolver.py
│   ├── skill_tree.py
│   ├── validate_contract.py
│   ├── detect_pattern.py
│   └── init_workspace.py
└── tree/
    └── tree-state.json
```

### Domain Skill Packages (example: omr-collection)

```
omr-collection.skill (112KB)
├── SKILL.md            # Skill specification with marketplace metadata
├── runtime_utils.py    # Infrastructure loader
├── cli.py              # CLI entry point
├── orchestrator.py     # Orchestration logic
├── input_router.py     # Input detection
├── search.py           # Search functionality
└── handlers/
    ├── __init__.py
    ├── base_handler.py
    ├── generic_web_handler.py
    ├── paper_handler.py
    ├── github_handler.py
    └── huggingface_handler.py
```

## Skill Tree Progression

Skills unlock based on artifact production:

```
omr-bootstrap ✓ (completed)
    │
    ├── omr-collection ○ (ready)
    │       │
    │       ├── omr-evidence ● (locked: needs materials in raw/)
    │       │       │
    │       │       └── omr-research-plan ● (locked: needs evidence-map.md)
    │       │               │
    │       │               ├── omr-decision ● (locked: needs research-plan.md)
    │       │               │       │
    │       │               │       └── omr-evaluation ● (locked: needs decision.md)
    │       │               │
    │       │               └── omr-synthesis ● (locked: needs research-plan.md)
    │       │                       │
    │       │                       └── omr-wiki ● (locked: needs synthesis)
    │       │
    │       └── omr-idea-note ✓ (available anytime)
    │
    └── omr-reconcile ✓ (available anytime)
    └── omr-research-archive ✓ (available anytime)
```

**Legend**:
- ✓ = completed
- ○ = ready (prerequisites satisfied)
- ● = locked (missing prerequisites)

## Evidence Philosophy

OmniResearch enforces strict evidence boundaries:

- **Proven**: Directly supported by source material (explicit claim in paper)
- **Suggested**: Indirect support (paper implies but doesn't explicitly state)
- **Inferred**: Logical conclusion from multiple sources (requires multiple papers)

**Rule**: Never claim "paper proves X" when it only suggests X. This prevents over-claiming and maintains research integrity.

## Research Patterns

OmniResearch recognizes 5 workflow patterns:

### 1. Evidence-First

Literature-driven research:
```
collection → evidence → plan → decision → synthesis
```

Use when: Starting with papers to analyze

### 2. Idea-First

Insight-driven research:
```
idea → collection → evidence → plan → decision → synthesis
```

Use when: Starting with creative hypothesis

### 3. Decision-First

Architecture-driven research:
```
decision → collection → evidence → plan → evaluation → synthesis
```

Use when: Starting with architectural stance to validate

### 4. Experiment-First

Test-driven research:
```
collection → evidence → evaluation → decision → synthesis
```

Use when: Starting with hypothesis to test

### 5. Rapid-Prototype

Fast iteration:
```
idea → collection → evaluation → decision → synthesis
```

Use when: Quick prototype cycle

**Pattern detection**: After 3+ skill invocations, OmniResearch identifies your pattern and optimizes skill recommendations.

## Troubleshooting

### Skill Not Found

```
/find-skills omr-core
❌ Skill not found in marketplace
```

**Solution**: Skills may not be published yet. Package manually:

```bash
cd skills/
python scripts/package_all_skills.py ./dist
```

Then install manually:

```bash
unzip dist/omr-core.skill -d ~/.claude/skills/
```

### Infrastructure Missing

```
❌ ImportError: OmniResearch infrastructure not found
```

**Solution**: Install omr-core:

```bash
/find-skills omr-core
```

Or verify global installation:

```bash
ls ~/.claude/skills/omr-core/
```

### Workspace Not Initialized

```
❌ Error: Workspace not found
```

**Solution**: Run bootstrap:

```bash
/omr-bootstrap "project-name" "research question?"
```

### Dependency Resolver Fails

```
❌ Error: dependency_resolver.py not found
```

**Solution**: Verify runtime_utils.py in skill package:

```bash
ls ~/.claude/skills/omr-collection/runtime_utils.py
```

If missing, skill package incomplete. Re-package:

```bash
python scripts/package_all_skills.py ./dist --skills omr-collection
```

## Advanced Usage

### Package Skills Manually

```bash
# Package all skills
cd skills/
python scripts/package_all_skills.py ./dist

# Package specific skills
python scripts/package_all_skills.py ./dist --skills omr-core,omr-bootstrap
```

### Test Marketplace Installation

```bash
# Test packaged skills
python scripts/test_marketplace_install.py ./dist
```

### Install from Local Files

```bash
# Unzip to Claude skills directory
unzip dist/omr-core.skill -d ~/.claude/skills/
unzip dist/omr-bootstrap.skill -d ~/.claude/skills/
```

## Marketplace Metadata

Each skill includes marketplace-standard metadata in SKILL.md:

```yaml
---
name: omr-collection
description: Material collection with passive reception philosophy...
version: 1.0.0
author: OmniResearch Team
license: MIT
metadata:
  requires_skills: [omr-core]
  requires_workspace: true
  category: research-logistics
  phase: 2.1
---
```

**Fields**:
- `name`: Skill identifier (kebab-case)
- `description`: When to trigger + what it does
- `version`: Semantic versioning (1.0.0)
- `author`: Team/individual name
- `license`: MIT, Apache-2.0, etc.
- `metadata.requires_skills`: Skill dependencies
- `metadata.requires_workspace`: Boolean
- `metadata.category`: Skill classification
- `metadata.phase`: OmniResearch workflow phase

## Version History

- **1.0.0** (2026-04-13): Initial marketplace release
  - Hybrid architecture with omr-core foundation
  - 11 skills packaged individually
  - runtime_utils.py for infrastructure loading
  - Marketplace metadata in SKILL.md frontmatter

---

**Last updated**: 2026-04-13
**OmniResearch version**: 1.0.0
**Compatibility**: Claude Code 1.0+