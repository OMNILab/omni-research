# Skill Directory Structure: Final Organization

**Date**: 2026-04-18

**Status**: ✅ All 9 skills organized per agent skill specification (v1.0.0 baseline)

> **Update (v2.0.0, 2026-07-30)**: Skills consolidated from 12 → 9. `omr-evidence` + `omr-research-plan` merged into `omr-analyze` (§6); `omr-wiki` merged into `omr-synthesis` (§11); `omr-research-archive` merged into `omr-reconcile` (§8). Sections 9, 10, 12 below are deprecation notes for the merged-away skills. See `omr-skills-flowchart.md` for the current 9-skill structure.

---

## Specification Compliance

Per agent skill spec, skill directories can contain:

### Required
- `SKILL.md` - Metadata + instructions (in root)

### Optional
- `scripts/` - Executable code
- `references/` - Additional documentation (if SKILL.md >500 lines)
- `assets/` - Templates, images, data files

---

## Final Structure for All Skills

### 1. omr-bootstrap ✓
```
omr-bootstrap/
├── SKILL.md ✓ (required)
├── assets/ ✓ (renamed from templates/)
│   └── CLAUDE.md.template ✓
├── scripts/ ✓
│   ├── bootstrap_workspace.py ✓
│   └── runtime_utils.py ✓ (proxy stub)
```

### 2. omr-collection ✓
```
omr-collection/
├── SKILL.md ✓
├── scripts/ ✓ (already organized)
│   ├── cli.py ✓
│   ├── orchestrator.py ✓
│   ├── input_router.py ✓
│   ├── search.py ✓
│   └── mcp_client.py ✓
├── handlers/ ✓ (skill-specific)
│   ├── paper_handler.py ✓
│   ├── github_handler.py ✓
│   ├── huggingface_handler.py ✓
│   └── generic_web_handler.py ✓
├── tests/ ✓ (skill-specific)
├── utils/ ✓ (skill-specific)
```

### 3. omr-core ✓
```
omr-core/
├── SKILL.md ✓
├── scripts/ ✓
│   ├── dependency_resolver.py ✓
│   ├── skill_tree.py ✓
│   ├── detect_pattern.py ✓
│   ├── validate_contract.py ✓
│   ├── runtime_utils.py ✓ (canonical shared module)
│   ├── _runtime_utils_proxy.py ✓ (proxy template for domain skills)
│   └── init_workspace.py ✓
├── contracts/ ✓ (infrastructure)
├── patterns/ ✓ (infrastructure)
├── schemas/ ✓ (infrastructure)
├── tree/ ✓ (infrastructure)
```

### 4. omr-decision ✓
```
omr-decision/
├── SKILL.md ✓
├── scripts/ ✓
│   ├── make_decision.py ✓
│   └── runtime_utils.py ✓ (proxy stub)
```

### 5. omr-evaluation ✓
```
omr-evaluation/
├── SKILL.md ✓
├── scripts/ ✓
│   ├── run_evaluation.py ✓
│   └ runtime_utils.py ✓
```

### 6. omr-analyze ✓ (replaces deprecated omr-evidence + omr-research-plan)
```
omr-analyze/
├── SKILL.md ✓
├── scripts/ ✓
│   ├── extract_evidence.py ✓ (from omr-evidence)
│   ├── plan_research.py ✓ (from omr-research-plan)
│   └── runtime_utils.py ✓
```

### 7. omr-idea-note ✓
```
omr-idea-note/
├── SKILL.md ✓
├── scripts/ ✓
│   ├── capture_idea.py ✓
│   └ runtime_utils.py ✓
```

### 8. omr-reconcile ✓
```
omr-reconcile/
├── SKILL.md ✓
├── scripts/ ✓
│   ├── reconcile_evidence.py ✓
│   └ runtime_utils.py ✓
```

### 9. omr-research-archive ⚠️ DEPRECATED (v2.0.0) — merged into omr-reconcile (§8)

> Archive functionality now internal to `omr-reconcile` via `--archive`, `--rollback`, `--list`, `--review` modes.

### 10. omr-research-plan ⚠️ DEPRECATED (v2.0.0) — merged into omr-analyze (§6)

> Research planning is now an internal phase of `omr-analyze` (Gate A checkpoint at `after_judgment_before_plan`).

### 11. omr-synthesis ✓
```
omr-synthesis/
├── SKILL.md ✓
├── scripts/ ✓
│   ├── synthesize_findings.py ✓
│   └ runtime_utils.py ✓
```

### 12. omr-wiki ⚠️ DEPRECATED (v2.0.0) — merged into omr-synthesis (§11)

> Wiki generation is now an internal post-Gate-D step within `omr-synthesis`. Use `--no-wiki` to skip.

---

## Changes Made

### Python Files Relocated

**Before**: Python files in skill roots (make_decision.py, extract_evidence.py, etc.)
**After**: All .py files moved to scripts/ directories

**Skills affected**: 6 skills (omr-analyze through omr-synthesis; omr-evidence/omr-research-plan/omr-wiki/omr-research-archive deprecated & merged in v2.0.0)

### Templates Renamed

**Before**: `skills/omr-bootstrap/templates/`
**After**: `skills/omr-bootstrap/assets/`

Per spec recommendation, assets/ contains static resources like templates.

### Already Compliant

**Skills already organized**: omr-collection, omr-core
- omr-collection: Already had scripts/, handlers/, tests/, utils/
- omr-core: Already had scripts/, contracts/, patterns/, schemas/

---

## Verification

### Root Directory Contents

**Each skill root now contains**:
- ✓ SKILL.md (required)
- ✓ Optional: README files, requirements.txt, documentation
- ✓ NO Python files (moved to scripts/)

### Scripts Directory Contents

**Each scripts/ directory contains**:
- ✓ Main executable (skill_name.py)
- ✓ runtime_utils.py (proxy stub → omr-core/scripts/runtime_utils.py)
- ✓ Additional scripts (where applicable)

### Assets Directory

**omr-bootstrap/assets/**:
- ✓ CLAUDE.md.template (workspace template)

---

## Progressive Disclosure Compliance

Per spec recommendations:

### Level 1: Metadata (~100 tokens)
- SKILL.md frontmatter: name + description
- Loaded at startup for skill discovery
- ✓ All skills have correct frontmatter

### Level 2: Instructions (<5000 tokens)
- SKILL.md body content
- Loaded when skill activated
- ✓ All SKILL.md files <500 lines (no references/ needed)

### Level 3: Resources (as needed)
- Scripts in scripts/ directories
- Loaded only when executed
- ✓ All .py files properly located

---

## Summary

**All 9 active OmniResearch skills now fully comply with agent skill specification** (12 in v1.0.0; 4 merged/deprecated in v2.0.0):

1. ✓ Frontmatter fields per spec (name/description/license/compatibility/metadata)
2. ✓ SKILL.md in root directory (required)
3. ✓ scripts/ directory for all executable Python files
4. ✓ assets/ directory for templates (where applicable)
5. ✓ No Python files in skill root directories
6. ✓ Progressive disclosure structure maintained

**Ready for**:
- Agent skill harness integration
- Skill marketplace packaging
- External validation with skills-ref tool
- Skill distribution and installation

---

_Generated: 2026-04-18_
_Status: Directory Structure Organization Complete_