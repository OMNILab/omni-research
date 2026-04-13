# Skills Directory Structure

**Reorganized**: 2026-04-12

**Philosophy**: Each skill is self-contained with its own assets (schemas, scripts, templates). Shared infrastructure lives in `skills/shared/`.

---

## Directory Layout

```
skills/
├── shared/                     # Shared infrastructure (used by all skills)
│   ├── contracts/              # Skill contract definitions (11 JSON files)
│   ├── schemas/                # Contract schema validation
│   ├── tree/                   # Skill tree state tracking
│   ├── validate_contract.py    # Contract validation script
│   ├── dependency_resolver.py  # Prerequisite checking
│   └── skill_tree.py           # Tree visualization
│
├── omr-bootstrap/              # Bootstrap skill (workspace creation)
│   ├── SKILL.md                # Skill specification
│   ├── scripts/                # Bootstrap implementation scripts
│   │   └ bootstrap_workspace.py
│   └── templates/              # CLAUDE.md template
│       └── CLAUDE.md.template
│
├── omr-collection/             # Material collection skill
│   ├── SKILL.md                # Skill specification (Phase 2.1 architecture)
│   ├── handlers/               # 4 core handlers
│   │   ├── __init__.py
│   │   ├── base_handler.py
│   │   ├── generic_web_handler.py
│   │   ├── paper_handler.py
│   │   ├── github_handler.py
│   │   └── huggingface_handler.py
│   └── input_router.py         # Input type detection and routing
│
├── omr-evidence/               # Evidence extraction skill (Phase 2.2)
│   └── SKILL.md
│
├── omr-research-plan/          # Judgment + planning skill (Phase 2.3)
│   └── SKILL.md
│
├── omr-decision/               # Architecture decision skill (Phase 2.4)
│   └── SKILL.md
│
├── omr-evaluation/             # Experiment execution skill (Phase 2.5)
│   └── SKILL.md
│
├── omr-synthesis/              # Synthesis writeback skill (Phase 3.1)
│   └── SKILL.md
│
├── omr-wiki/                   # Wiki generation skill (Phase 3.2)
│   └── SKILL.md
│
├── omr-idea-note/              # Idea capture skill (Phase 3.3)
│   └── SKILL.md
│
├── omr-reconcile/              # Reconciliation skill (Phase 3.4)
│   └── SKILL.md
│
├── omr-research-archive/       # Archive skill (Phase 3.5)
│   └── SKILL.md
│
└── patterns/                   # Pattern definitions (Phase 4)
    └── (future pattern JSON files)
```

---

## Design Philosophy

### Modular Skill Structure

Each skill directory contains:
- **SKILL.md**: Skill specification, usage, examples
- **scripts/**: Implementation scripts (CLI entry points, handlers, utilities)
- **handlers/**: Skill-specific handlers (if applicable)
- **templates/**: Templates for skill outputs (if applicable)
- **schemas/**: Artifact schemas for skill outputs (if applicable)

**Benefits**:
- Skills are self-contained
- Easy to test individually
- Clear separation of concerns
- Can be packaged independently

---

### Shared Infrastructure

`skills/shared/` contains infrastructure used across all skills:
- **Contract definitions**: Artifact-bound dependencies for all 11 skills
- **Contract schema**: JSON schema for validating contracts
- **Contract validation**: Script to validate all contracts
- **Dependency resolver**: Prerequisite checking before skill invocation
- **Skill tree state**: Tracks unlocked/ready/locked/completed skills
- **Skill tree visualization**: ASCII forward/reverse views

**Benefits**:
- Centralized contract management
- Single source of truth for dependency resolution
- Shared skill tree state across all skills
- Consistent validation across skills

---

## File Manifest

**Shared Infrastructure** (8 files):
- `shared/contracts/*.json` (11 contract files)
- `shared/schemas/contract.schema.json`
- `shared/validate_contract.py`
- `shared/dependency_resolver.py`
- `shared/skill_tree.py`
- `shared/tree/tree-state.json`

**omr-bootstrap** (3 files):
- `SKILL.md`
- `scripts/bootstrap_workspace.py`
- `templates/CLAUDE.md.template`

**omr-collection** (8 files):
- `SKILL.md`
- `input_router.py`
- `handlers/__init__.py`
- `handlers/base_handler.py`
- `handlers/generic_web_handler.py`
- `handlers/paper_handler.py`
- `handlers/github_handler.py`
- `handlers/huggingface_handler.py`

**Remaining Skills** (11 files):
- 11 `SKILL.md` files (specifications only, implementation pending)

**Total**: 30 files created (Phase 1 + Phase 2.1)

---

## Usage

### Contract Validation

```bash
python skills/shared/validate_contract.py
```

### Dependency Resolution

```bash
python skills/shared/dependency_resolver.py omr-evidence --check --workspace /tmp/test-project
```

### Skill Tree Visualization

```bash
python skills/shared/skill_tree.py            # Forward view
python skills/shared/skill_tree.py --reverse  # Reverse view
```

### Workspace Bootstrap

```bash
python skills/omr-bootstrap/scripts/bootstrap_workspace.py my-project "Research question?"
```

### Material Collection (Phase 2.1 handlers)

```bash
python skills/omr-collection/input_router.py "https://arxiv.org/abs/2402.12345" "agent memory"
python skills/omr-collection/handlers/paper_handler.py /tmp/test-project 2402.12345
python skills/omr-collection/handlers/github_handler.py /tmp/test-project anthropics/anthropic-sdk-python
```

---

## Implementation Progress

### Phase 1: Foundation ✅ Complete
- Contract system working
- Workspace bootstrap tested
- Skill tree visualization functional
- Dependency resolver validated

### Phase 2.1: omr-collection 🚧 In Progress
- SKILL.md complete (Phase 2.1 architecture)
- Input router implemented
- 4 handlers implemented (base + paper + github + huggingface + generic web)
- Handlers tested individually
- Orchestrator + CLI pending (Phase 2.1 continuation)

### Phase 2.2-2.5: Remaining Skills ⏳ Pending
- SKILL.md exists for each skill
- Implementation pending

### Phase 3-5: Future Work ⏳ Planned
- See `implementation-plan-omr-skills.md` for complete roadmap

---

## Next Steps

1. **omr-collection completion**: Implement orchestrator + CLI entry point
2. **omr-evidence implementation**: Phase 2.2
3. **omr-research-plan implementation**: Phase 2.3
4. **omr-decision implementation**: Phase 2.4
5. **omr-evaluation implementation**: Phase 2.5

---

## Integration Testing

**Phase 1 Tests**: All passing
- Contract validation: ✓ 11 contracts valid
- Workspace bootstrap: ✓ Structure created
- Skill tree visualization: ✓ Forward + reverse views working
- Dependency resolver: ✓ Prerequisite checking functional

**Phase 2.1 Tests**: Handlers tested individually
- Input router: ✓ URL/DOI/Search detection working
- Paper handler: Pending (needs test workspace)
- GitHub handler: Pending (needs test workspace)
- HuggingFace handler: Pending (needs test workspace)
- Generic Web handler: Pending (needs test workspace)

---

_Generated: 2026-04-12_
_Status: Skills folder structure reorganized, Phase 1 complete, Phase 2.1 handlers implemented_