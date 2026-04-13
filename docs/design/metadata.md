# Artifact Metadata System

## Standard Metadata Header

Every artifact includes standardized YAML frontmatter:

```yaml
---
# Identity
id: Q-001                          # Unique artifact ID
type: research-brief               # Artifact type
version: 1.0.0                     # Semantic versioning

# Provenance
created_at: 2026-04-11T10:30:00Z
updated_at: 2026-04-11T10:30:00Z
created_by: user                   # user | agent-name
status: draft                      # draft | reviewed | published | archived

# Lineage
pattern: evidence-first            # Pattern name (if any)
stage: definition                  # Research stage
dependencies: []                   # IDs of artifacts this depends on
dependents: []                     # IDs of artifacts that depend on this

# Quality
gates_passed: []                   # List of gates passed
review_notes: []                   # Review comments

# Traceability
traceability_refs: []              # Cross-references to other artifacts
---
```

## File Naming Convention

**Pattern:** `{type}-{id}-v{major}.{minor}.{patch}.md`

| Artifact Type | Filename | Example |
|---------------|----------|---------|
| research-brief | `brief-{id}-v{version}.md` | `brief-Q-001-v1.0.0.md` |
| evidence-map | `evidence-{id}-v{version}.md` | `evidence-Q-001-v1.0.0.md` |
| judgment-summary | `judgment-{id}-v{version}.md` | `judgment-Q-001-v1.0.0.md` |
| research-plan | `plan-{id}-v{version}.md` | `plan-Q-001-v1.0.0.md` |
| architecture-decision | `decision-{id}-v{version}.md` | `decision-DEC-001-v1.0.0.md` |
| experiment-spec | `spec-{id}-v{version}.md` | `spec-EXP-001-v1.0.0.md` |
| evaluation-report | `report-{id}-v{version}.md` | `report-EXP-001-v1.0.0.md` |
| synthesis | `synthesis-{id}-v{version}.md` | `synthesis-Q-001-v1.0.0.md` |
| idea-note | `idea-{timestamp}-{slug}.md` | `idea-20260411T103000-quantum-memory.md` |

**Version suffix optional for current version:**
- `decision-DEC-001.md` = current version (symlink/copy)
- `decision-DEC-001-v1.0.0.md` = specific version (archived)

## Semantic Versioning

| Change Type | Increment | Example |
|-------------|-----------|---------|
| Breaking change (invalidates downstream) | MAJOR | 1.0.0 → 2.0.0 |
| Additive change (new fields) | MINOR | 1.0.0 → 1.1.0 |
| Bug fix, typo, formatting | PATCH | 1.0.0 → 1.0.1 |

**Version lifecycle:**
```
draft (v0.1.0) → reviewed (v1.0.0) → published (v1.0.0) → superseded (v1.0.0 archived, v2.0.0 created)
```

## Status Workflow

```
draft → reviewed → published → archived
  ↓        ↓          ↓
  └────────┴──────────┴→ superseded
```

| Status | Meaning | Can Edit? |
|--------|---------|-----------|
| `draft` | Work in progress | Yes |
| `reviewed` | Passed gate review | No (fork to edit) |
| `published` | Final, traceable | No (only supersede) |
| `archived` | Historical record | No (read-only) |
| `superseded` | Replaced by newer version | No (pointer to current) |

## Dependency Tracking

**Automatic dependency recording:**

When `omr-decision` produces `decision-DEC-001.md`:
```yaml
dependencies:
  - id: Q-001
    type: research-brief
    file: docs/plans/brief-Q-001.md
  - id: Q-001
    type: evidence-map
    file: docs/plans/evidence-Q-001.md
```

**Reverse dependency (dependents) updated automatically:**

In `brief-Q-001.md`:
```yaml
dependents:
  - id: DEC-001
    type: architecture-decision
    file: docs/plans/decision-DEC-001.md
```

## Index Files

**Artifact Index:** `docs/index/artifacts-index.json`
- Lists all artifacts with metadata
- Machine-readable for tooling
- Updated on every artifact creation/update

**Version History:** `docs/index/versions/{id}-history.json`
- Tracks all versions of an artifact
- Records reasons for changes
- Links to archived files

## Schema Validation

JSON schemas in `docs/schemas/{type}.schema.json`

Skills validate output against schema before writing artifacts.
