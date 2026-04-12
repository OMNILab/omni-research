# Phase 2: Core Skills — Progress Summary

**Status**: 🚧 In Progress (Phase 2.1 started)

**Date**: 2026-04-12

**Current Task**: Implementing omr-collection skill (Phase 2.1)

---

## Phase 1 Recap ✅ Complete

All foundation components working:
- ✅ Contract System (11 contracts validated)
- ✅ Workspace Structure (bootstrap script tested)
- ✅ Skill Tree Visualization (forward + reverse views)
- ✅ Dependency Resolver (prerequisite checking functional)

**Phase 1 Files**: 17 files created (schemas, contracts, templates, scripts)

**Integration Tests**: All 4 tests passing

---

## Phase 2 Overview: Core Skills (5 Skills)

**Timeline**: Weeks 4-6 (per implementation plan)

**Skills to Implement**:
1. **omr-collection** (Phase 2.1) — Material collection with passive reception philosophy
2. **omr-evidence** (Phase 2.2) — Evidence extraction with minimal parsing boundary
3. **omr-research-plan** (Phase 2.3) — Merged skill: judgment + planning + Gate A
4. **omr-decision** (Phase 2.4) — Architecture decision with alternatives + Gate B
5. **omr-evaluation** (Phase 2.5) — Experiment execution + Gate C + pattern overrides

---

## Phase 2.1: omr-collection — Current Status

### SKILL.md Complete ✅

**Architecture from brainstorming session 2**:

**Key Philosophy**:
- **Passive Reception**: User decides sources → skill delivers materials
- **Minimal Parsing**: Format extraction only, NO semantic analysis
- **Pattern Neutrality**: Works for all 5 research patterns equally

**Components Designed**:

#### 1. Dual-Mode Input Model
- **Direct Input Mode**: URLs, DOIs, paths → Direct collection
- **Search Input Mode**: Research query → Search APIs → Hybrid confirmation UI → User approves → Collection

**Input Detection**:
```python
if matches_url_pattern(input):
    → Direct Input Mode
elif quoted_string(input) OR no_url_pattern(input):
    → Search Input Mode
```

#### 2. 4 Core Handlers (Minimal, Fixed)
- **Generic Web**: Chrome MCP → snapshot + markdown (`raw/web/url-hash.md`)
- **Paper**: PDF download → markdown parser (`raw/paper/doi-hash.md`)
- **GitHub**: README + release API (`raw/github/repo-name.md`)
- **HuggingFace**: README + card (`raw/dataset/hf-name.md`)

**Extensibility**: ✗ None (Generic Web covers edge cases)

**Fallback**: Primary handler fails → Generic Web fallback → Error artifact

#### 3. Configurable Retrieval Depth
**Default Mode** (Sensible Defaults):
- GitHub: README + latest release (no full clone)
- Papers: PDF only (no supplementary)
- HuggingFace: README + card (no download)
- Web: Snapshot + markdown (full page)

**Override Flags** (Pattern Compatibility):
- `--full-repo`: Clone full GitHub repo (shallow, depth=1)
- `--download-dataset`: Download HuggingFace dataset files
- `--download-model`: Download HuggingFace model weights
- `--with-supplementary`: Download paper supplementary materials

**Pattern Needs**:
- Evidence-First: Default sufficient
- Idea-First: Default sufficient
- Decision-First: Default sufficient
- Experiment-First: Needs `--download-dataset` flag

#### 4. AI-Optimized Output Structure
**Naming Philosophy**: Deterministic (DOI/hash) NOT Human-readable

**Why?**: Artifacts optimized for downstream AI skills, not human browsing

**Directory Layout**:
```
raw/
├── paper/           # DOI-based (doi-10-1234-abc.md)
├── web/             # URL-hash (url-a1b2c3d4.md)
├── github/          # Repo-name (github-user-project.md)
├── dataset/         # HF-name (hf-dataset-name.md)
├── search/          # query-hash-abc123/
│   ├── paper/
│   ├── github/
│   ├── dataset/
│   ├── query-metadata.json
│   └── results-list.json
└── failed/          # url-hash-error.md

docs/index/
├── papers-index.json
├── blogs-index.json
├── repos-index.json
├── datasets-index.json
├── search-queries-index.json
└── failed-index.json
```

#### 5. Minimal Metadata Scope
**Core Fields** (All Sources):
- id, title, url, source_type, collected_at, collected_by, file_path

**Source-Specific**:
- Paper: authors, date, DOI/arxiv_id, source_url
- GitHub: stars, language, license, release_tag, last_updated
- HuggingFace: downloads, likes, tags, task_type
- Web: captured_at, snapshot_path, markdown_length
- Search: query, sources_searched, results_found, results_collected, user_selection
- Failed: error_type, error_message, retry_attempts, fallback_attempted

**NO Semantic Fields**: ✗ Abstract, keywords, citations, references

#### 6. Balanced Error Handling
**Flow**:
```
1. Attempt primary handler
   ↓ (failure)
2. Retry 2x with 2s delay
   ↓ (still failing)
3. Try Generic Web fallback
   ↓ (still failing)
4. Create error artifact in raw/failed/
5. Continue collecting remaining sources
6. Report errors in console + error artifacts
```

**Console Output**:
```
✓ Collected 6 artifacts (3 papers, 2 github, 1 dataset)
⚠ Failed: 2 sources
  - https://broken-link.com/paper.pdf (404)
  - https://timeout-server.com/blog.html (timeout)

See: raw/failed/ for error details
```

### Implementation Priorities (Phased)

**Phase 2.1a**: Core handlers (Generic Web, Paper, GitHub, HuggingFace)
**Phase 2.1b**: Search integration (APIs + hybrid confirmation UI)
**Phase 2.1c**: Reliability (retry + fallback + error artifacts)
**Phase 2.1d**: Pattern compatibility flags

---

## Next Steps: omr-collection Implementation

### Scripts to Create (Phase 2.1a)

**Priority**: Core Handlers (most critical)

1. **Input Router** (`skills/omr-collection/input_router.py`)
   - URL pattern matching
   - DOI/Arxiv ID detection
   - Search query detection
   - Handler selection logic

2. **Handlers Directory** (`skills/omr-collection/handlers/`)
   - `generic_web_handler.py` — Chrome MCP integration
   - `paper_handler.py` — PDF download + markdown conversion
   - `github_handler.py` — GitHub API for README + release
   - `huggingface_handler.py` — HF API for README + card

3. **Collection Orchestrator** (`skills/omr-collection/orchestrator.py`)
   - Coordinate handler execution
   - Retry logic (2x with 2s delay)
   - Fallback mechanism (Generic Web)
   - Error artifact creation
   - Index updates

4. **Search Integration** (`skills/omr-collection/search.py`)
   - arxiv API integration
   - GitHub search API integration
   - HuggingFace search integration
   - Hybrid confirmation UI (present results → user confirms)

5. **CLI Entry Point** (`skills/omr-collection/cli.py`)
   - Argument parsing (sources + override flags)
   - Direct input mode execution
   - Search mode execution
   - Progress reporting
   - Skill tree update integration

### Phase 2.1b: Search APIs

**APIs to Integrate**:
- **arxiv API**: `http://export.arxiv.org/api/query` (search papers)
- **GitHub Search API**: `https://api.github.com/search/repositories` (search repos)
- **HuggingFace Search**: HF Hub API (search datasets/models)

**Hybrid Confirmation UI**:
```
Skill: Found 47 results:
       - arxiv: 23 papers
       - github: 18 repos
       - huggingface: 6 datasets

       Default: top-10 from each source (30 total)

       [Y] Accept default
       [custom] Override (e.g., 'top-5 arxiv, top-3 github')
       [n] Cancel
```

### Phase 2.1c: Error Handling

**Error Handling Components**:
- Retry decorator (2x with 2s delay)
- Fallback router (Generic Web handler)
- Error artifact generator (markdown template)
- Console reporter (summary with failed sources)

### Phase 2.1d: Override Flags

**Flag Implementation**:
- `--full-repo`: Shallow clone (depth=1) using GitPython
- `--download-dataset`: HuggingFace dataset download (HF Hub API)
- `--download-model`: HuggingFace model download (HF Hub API)
- `--with-supplementary`: Paper supplementary materials (URL parsing + download)

---

## Phase 2.2-2.5: Remaining Core Skills

### omr-evidence (Phase 2.2)

**Purpose**: Extract research questions, claims, evidence, gaps from collected materials

**Minimal Parsing Boundary**: Read markdown artifacts → Extract evidence → Produce brief + evidence-map

**Output**:
- `research-brief.md` (question_id, scope, context)
- `evidence-map.md` (primary evidence, gaps, confidence)

**Dependencies**: Requires materials in `raw/` (from omr-collection)

### omr-research-plan (Phase 2.3)

**Purpose**: Merged skill — judge evidence + plan research

**Output**:
- `judgment-summary.md` (main conclusion, confidence)
- `research-plan.md` (priorities, timeline)

**Gate A**: Evidence sufficient for planning?
- Checks: Evidence coverage adequate, Research question clear, Scope defined
- Enforcement: user-confirm

**Dependencies**: Requires `evidence-map.md` (from omr-evidence)

### omr-decision (Phase 2.4)

**Purpose**: Architecture decision with alternatives + evidence refs

**Output**:
- `architecture-decision.md` (decision_id, alternatives, selected, evidence_refs, risks)

**Gate B**: Architecture decision sound?
- Checks: Alternatives documented, Risks stated, Evidence refs valid
- Enforcement: user-confirm

**Dependencies**: Requires `evidence-map.md` (mandatory), `judgment-summary.md` (optional)

### omr-evaluation (Phase 2.5)

**Purpose**: Experiment execution + evaluation

**Output**:
- `experiment-spec.md` (hypothesis, metrics, ground truth)
- `evaluation-report.md` (hypothesis support, decision validation, traceability)

**Gate C**: Experiment design valid?
- Checks: Metrics answer research question, Failure conditions explicit, Reproducible evaluation
- Enforcement: user-confirm

**Pattern Override**: Experiment-First allows evaluation without prior decision
```yaml
Experiment-First:
  contract_overrides:
    omr-evaluation:
      requires: []  # Allow without architecture-decision.md
```

**Dependencies**: Requires `architecture-decision.md` (mandatory, can be overridden)

---

## Implementation Strategy

**Approach**: Implement skills sequentially (2.1 → 2.2 → 2.3 → 2.4 → 2.5)

**Reason**: Each skill depends on outputs from previous skills, so testing requires working upstream skills

**Testing**: For each skill:
1. Unit tests (handler logic, error handling, metadata extraction)
2. Integration tests (workspace creation → collection → evidence → ... → evaluation)
3. End-to-end tests (complete research workflow following a pattern)

**Integration**: Each skill completion triggers:
- Skill tree state update (unlock downstream skills)
- Dependency resolver update (prerequisite checking)
- Index updates (metadata persistence)

---

## Success Metrics for Phase 2

| Metric | Target |
|--------|--------|
| Skills implemented | 5/5 |
| Handlers working | 4/4 (omr-collection) |
| Gates enforced | 3/3 (A, B, C) |
| Pattern overrides supported | 1/1 (Experiment-First) |
| Search integration working | ✓ (hybrid confirmation) |
| Error handling tested | ✓ (retry + fallback + error artifacts) |
| Integration tests passing | 5/5 skills |

---

## Dependencies Between Phase 2 Skills

```
omr-collection → produces raw/* + docs/index/*
  ↓
omr-evidence → requires raw/* → produces research-brief.md + evidence-map.md
  ↓
omr-research-plan → requires evidence-map.md → produces judgment-summary.md + research-plan.md + Gate A
  ↓
omr-decision → requires evidence-map.md (mandatory) + judgment-summary.md (optional) → produces architecture-decision.md + Gate B
  ↓
omr-evaluation → requires architecture-decision.md (mandatory, can be overridden) → produces experiment-spec.md + evaluation-report.md + Gate C
```

**Pattern Override Example**: Experiment-First
```
omr-evaluation (no decision) → produces experiment-spec.md + evaluation-report.md
  ↓
omr-evidence → produces evidence-map.md
  ↓
omr-decision → produces architecture-decision.md (retroactive)
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| **Search API limits** | Use sensible defaults (top-10 per source), user override available |
| **PDF parsing failures** | Try multiple parsers (marker, pdfplumber), fallback to Generic Web |
| **GitHub API rate limits** | Use unauthenticated search (limited rate), user can provide auth token |
| **Chrome MCP not available** | Generic Web handler fallback to simple HTML fetcher |
| **Pattern override complexity** | Clear contract override schema, validate before execution |
| **Skill tree update race conditions** | Atomic tree state updates, dependency resolver locks |

---

## Known Limitations (Phase 2)

1. **Pattern definitions not yet created**: Contract overrides mechanism exists, but pattern JSON files not yet defined (Phase 4 will create)

2. **Artifact schemas not yet defined**: Output schemas referenced in contracts, but JSON schema files not yet created (Phase 2 will create artifact schemas as skills are implemented)

3. **Skill-to-skill invocation**: Skills implemented as CLI tools, but skill-to-skill calling mechanism not yet built (Phase 3 will implement orchestration)

4. **Reverse tree incomplete**: Goal-first planning shows goals, but doesn't trace full prerequisite chain (Phase 4 will implement)

5. **Gate enforcement**: Gates defined, but enforcement logic (user confirm prompts) not yet implemented (Phase 2 will implement with each skill)

---

## Files Created (Phase 2 so far)

1. `skills/omr-collection/SKILL.md` — Skill definition following Phase 2.1 architecture

**Next Files** (Phase 2.1a implementation):
- `skills/omr-collection/input_router.py`
- `skills/omr-collection/handlers/generic_web_handler.py`
- `skills/omr-collection/handlers/paper_handler.py`
- `skills/omr-collection/handlers/github_handler.py`
- `skills/omr-collection/handlers/huggingface_handler.py`
- `skills/omr-collection/orchestrator.py`
- `skills/omr-collection/cli.py`

---

## Timeline Estimate

**Phase 2.1 (omr-collection)**: 2-3 days
- Phase 2.1a (Core handlers): 1 day
- Phase 2.1b (Search integration): 0.5 day
- Phase 2.1c (Error handling): 0.5 day
- Phase 2.1d (Override flags): 0.5 day

**Phase 2.2-2.5 (Remaining skills)**: 3-4 days each (total 12-16 days)

**Phase 2 Total**: 14-19 days (2-3 weeks)

---

## Next Action

**Immediate**: Implement omr-collection Phase 2.1a (Core Handlers)

**Files to Create**:
1. Input router
2. 4 handlers (Generic Web, Paper, GitHub, HuggingFace)
3. Collection orchestrator
4. CLI entry point

**Testing**: Create test workspace → Test each handler → Test fallback → Test error handling

---

_Generated: 2026-04-12_
_Status: Phase 2.1 SKILL.md complete, implementation scripts next_