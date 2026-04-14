---
name: omr-collection
description: Material collection with passive reception philosophy. User provides sources → skill delivers materials. Supports direct input (URLs, DOIs, arxiv IDs, GitHub repos, HuggingFace URLs) and keyword search queries. Minimal parsing (format extraction only, no semantic analysis). 4 handlers with configurable depth and graceful fallbacks. arxiv SDK integration for reliable paper downloads with rich metadata. Chrome MCP integration for webpage screenshots. Search automation with prioritized downloads. Use this skill whenever user wants to collect research materials, download papers, gather code repos, search for papers by keyword, capture webpage screenshots, or gather any web resources for research. Even if they don't explicitly mention 'collection' or 'download' - if they reference papers, repos, datasets, or web content, this skill should trigger.
version: 1.1.0
author: OmniResearch Team
license: MIT
metadata:
  requires_skills: [omr-core]
  requires_workspace: true
  category: research-logistics
  phase: 2.1
  enhancements: [arxiv-sdk, chrome-mcp, search-automation]
---

# omr-collection

**Purpose**: AI-logistics mechanism that delivers research-ready materials for downstream skills. NOT a research skill — pure logistics with minimal parsing.

**Philosophy**: Passive Reception (user expertise respected), Minimal Parsing (format access + metadata only), Pattern Neutrality (works for all 5 research patterns equally).

---

## Core Philosophy: Passive Reception

**User decides sources → Skill delivers materials**

- No active discovery (unless user provides search query)
- No filtering or curation
- No semantic analysis (that belongs in downstream skills)
- Logistics, not research

**Why Passive?**
- Users ARE domain experts
- Works equally for Evidence-First, Idea-First, Decision-First, Experiment-First patterns
- Minimal parsing boundary respected

---

## Minimal Parsing Boundary

**Format accessibility + metadata harvesting only**

- PDF → text extraction (format conversion)
- HTML → markdown (format conversion)
- Metadata: bibliographic + provenance info

**NO Semantic Extraction**:
- ✗ No abstract extraction
- ✗ No keyword classification
- ✗ No citation analysis
- ✗ No claim extraction

**Collection = preparation, Evidence = analysis**

Semantic extraction belongs in `omr-evidence` (downstream skill), not here.

---

## Input Model: Dual-Mode Reception

### Direct Input Mode (Passive)
- User provides: URLs, DOIs, Arxiv IDs, GitHub URLs, HuggingFace URLs, local paths
- Skill delivers: Materials as markdown artifacts with metadata
- No discovery, no filtering

**Examples**:
```
/omr-collection "https://arxiv.org/abs/2402.12345"
/omr-collection "10.1234/paper-doi"
/omr-collection "github.com/user/repo"
/omr-collection "huggingface.co/datasets/user/data"
```

### Search Input Mode (User-Driven)
- User provides: Research query (e.g., `"agent memory mechanisms"`)
- Skill executes: Search arxiv + GitHub + HuggingFace
- Skill proposes: Top-10 results per source (sensible defaults)
- User confirms: Accept defaults OR override
- Skill delivers: Approved materials

**Search Flow**:
```
User: /omr-collection "agent memory mechanisms"

Skill: Found 47 results:
       - arxiv: 23 papers
       - github: 18 repos
       - huggingface: 6 datasets

       Default: top-10 from each source (30 total)

       [Y] Accept default
       [custom] Override (e.g., 'top-5 arxiv, top-3 github')
       [n] Cancel

User: Y

Skill: ✓ Collecting 30 materials → raw/search/query-hash/
```

**Passive reception preserved**: User approves scope → Skill delivers within scope

**Input Detection**:
```python
if matches_url_pattern(input):
    → Direct Input Mode
elif quoted_string(input) OR no_url_pattern(input):
    → Search Input Mode
```

---

## Handler Architecture: 4 Core Handlers (Minimal, Fixed)

| Handler | Source Types | Retrieval Strategy | Output Format |
|---------|--------------|-------------------|---------------|
| **Generic Web** | HTTP/HTTPS URLs, unsupported sources | Chrome MCP → snapshot + markdown | `raw/web/url-hash.md` + `.png` |
| **Paper** | Paper URLs, DOIs, Arxiv IDs | PDF download → markdown parser | `raw/paper/doi-hash.md` |
| **GitHub** | GitHub URLs | README + release info (API) | `raw/github/repo-name.md` |
| **HuggingFace** | HF dataset/model URLs | README + card (browser + API) | `raw/dataset/hf-name.md` |

**Extensibility**: ✗ None

**Rationale**: First Principles minimalism + Generic Web covers 80% of edge cases (GitLab, Bitbucket, blogs, institutional repos)

**Fallback**: Primary handler fails → Try Generic Web snapshot → Error artifact if all fail

---

## Retrieval Depth: Configurable for Pattern Compatibility

**Default Mode (Sensible Defaults)**:
- GitHub: README + latest release (no full clone)
- Papers: PDF only (no supplementary materials)
- HuggingFace: README + card (no dataset/model download)
- Web: Snapshot + markdown (full page capture)

**Override Flags**:
- `--full-repo`: Clone full GitHub repository (shallow clone, depth=1)
- `--download-dataset`: Download full HuggingFace dataset files
- `--download-model`: Download full HuggingFace model weights
- `--with-supplementary`: Download paper supplementary materials

**Pattern Compatibility**:
- Evidence-First: Default sufficient (papers for reading)
- Idea-First: Default sufficient (inspiration sources)
- Decision-First: Default sufficient (validation materials)
- Experiment-First: `--download-dataset` flag needed (actual dataset for evaluation)

---

## Skill Structure

```
omr-collection/
├── SKILL.md           # Skill instructions (this file)
├── README.md          # Quick reference guide
├── requirements.txt   # Optional dependencies
├── DEPENDENCIES.md    # Dependency management guide
│
├── scripts/           # Executable entry points
│   ├── cli.py         # Main CLI interface
│   ├── orchestrator.py # Collection coordination
│   ├── search.py      # Search automation
│   ├── mcp_client.py  # Chrome MCP utility
│   ├── input_router.py # Input classification
│   └── verify_enhancements.py # Setup verification
│
├── handlers/          # Domain-specific handlers
│   ├── paper_handler.py     # arxiv/DOI papers (SDK + HTTP)
│   ├── github_handler.py    # GitHub repositories
│   ├── generic_web_handler.py # Webpages (Chrome MCP + HTTP)
│   ├── huggingface_handler.py # HF datasets/models
│   └── base_handler.py      # Abstract base class
│
├── utils/             # Shared utilities
│   └── runtime_utils.py # Infrastructure loader
│
└── tests/             # Test suite (future)
```

**Progressive disclosure**:
- **SKILL.md** (352 lines) - Loaded when skill triggers
- **scripts/** - Executed as needed (unlimited)
- **DEPENDENCIES.md** - Reference for dependency setup

## Output Structure: AI-Optimized Artifacts

**Directory Layout**:
```
raw/
├── paper/           # DOI-based naming (doi-10-1234-abc.md)
│                   # arxiv-based naming (arxiv-2402-12345.md)
├── web/             # URL-hash naming (url-a1b2c3d4.md)
│                   # Screenshots: url-a1b2c3d4-snapshot.png
├── github/          # Repo-name naming (github-user-project.md)
├── dataset/         # HF-name naming (hf-dataset-name.md)
├── search/          # Search-specific
│   └── query-hash-abc123/
│       ├── query-metadata.json
│       └── (collected papers in raw/paper/)
└── failed/          # Error artifacts (url-hash-error.md)

docs/index/
├── papers-index.json
├── blogs-index.json
├── repos-index.json
├── datasets-index.json
├── search-queries-index.json
└── failed-index.json
```

**Naming Philosophy**: Deterministic (DOI/hash-based) NOT Human-readable

**Why?**: Artifacts optimized for downstream AI skills, not human browsing. Index provides human-readable metadata for lookup.

**Human Access**: Query index → Find title → Get file_path → Read artifact

---

## Metadata Scope: Minimal (Core + Source-Specific)

**Core Fields (All Sources)**:
```json
{
  "id": "unique-identifier",
  "title": "human-readable-name",
  "url": "source-location",
  "source_type": "paper/web/github/dataset/search/failed",
  "collected_at": "ISO-8601",
  "collected_by": "omr-collection",
  "file_path": "raw/source-type/artifact-name.md"
}
```

**Paper-Specific**: authors, date, DOI/arxiv_id, source_url

**GitHub-Specific**: stars, language, license, release_tag, last_updated

**HuggingFace-Specific**: downloads, likes, tags, task_type

**Web-Specific**: captured_at, snapshot_path, markdown_length

**Search-Specific**: query, sources_searched, results_found, results_collected, user_selection

**Failed-Specific**: error_type, error_message, retry_attempts, fallback_attempted

**NO Semantic Fields**: ✗ Abstract, keywords, citations, references (downstream skills extract)

---

## Error Handling: Balanced Reliability

**Flow**:
```
1. Attempt primary handler
   ↓ (failure)
2. Retry 2x with 2s delay
   ↓ (still failing)
3. Try Generic Web fallback (Chrome MCP snapshot)
   ↓ (still failing)
4. Create error artifact in raw/failed/
5. Continue collecting remaining sources (fail gracefully)
6. Report errors in console + error artifacts + failed-index.json
```

**Error Artifact**:
```markdown
# Collection Failure

**URL**: https://broken-link.com/paper.pdf
**Source Type**: paper
**Status**: failed
**Error**: HTTP 404: Not Found
**Retry Attempts**: 2
**Fallback Attempted**: Yes (generic_web)
**Collected At**: 2026-04-12T11:27:00Z
```

**Console Output**:
```
✓ Collected 6 artifacts (3 papers, 2 github, 1 dataset)
⚠ Failed: 2 sources
  - https://broken-link.com/paper.pdf (404)
  - https://timeout-server.com/blog.html (timeout)

See: raw/failed/ for error details
```

---

## Implementation Priorities (Phased)

**Phase 2.1a**: Core handlers (Generic Web, Paper, GitHub, HuggingFace)
**Phase 2.1b**: Search integration (APIs + hybrid confirmation UI)
**Phase 2.1c**: Reliability (retry + fallback + error artifacts)
**Phase 2.1d**: Pattern compatibility flags

---

## Implementation Notes

### Enhanced Features (v1.1.0)

**arxiv SDK Integration**:
- Official arxiv Python SDK for reliable downloads
- Rich metadata: title, authors, DOI, categories, abstract
- Built-in retry logic (3 retries, 3s delay)
- HTTP fallback when SDK unavailable
- See: handlers/paper_handler.py

**Chrome MCP Integration**:
- Webpage screenshot capture (PNG snapshots)
- Rendered page markdown (JavaScript executed)
- Server detection via npm package
- HTTP fallback when MCP unavailable
- See: handlers/generic_web_handler.py, scripts/mcp_client.py

**Search Automation**:
- arxiv SDK search (richer results)
- Google Scholar via Chrome MCP (placeholder)
- Prioritization: arxiv results preferred
- Top-N papers downloaded automatically
- See: scripts/search.py

### Handler Implementation
- Each handler: fetch → convert → store → index
- Retry logic: max_retries=2, retry_delay=2s (orchestrator)
- Fallback chain: primary → retry → Generic Web → error artifact
- Deterministic naming: DOI/hash-based

### Input Router
- Pattern matching for URLs, DOIs, arxiv IDs
- Quoted string detection for search queries
- URL parsing attempt: if fails, treat as search

### Metadata Extraction
- Minimal bibliographic info (no semantic analysis)
- Provenance tracking (source, timestamp, method)
- arxiv SDK: rich metadata vs HTTP: minimal metadata

### Index Updates
- Append to existing indexes
- Maintain determinism (hash/DOI naming)
- Update timestamps

---

## Dependencies & Fallbacks

**Optional dependencies with graceful fallback**:

| Dependency | With it | Without it |
|-----------|---------|-----------|
| `arxiv` SDK | Rich metadata, reliable downloads | HTTP downloads, basic metadata |
| `mcp` SDK + Chrome server | Screenshots, rendered pages | HTTP fetch, markdown only |
| `huggingface_hub` | Full dataset/model downloads | README + metadata only |

**Installation**:
```bash
# Minimal (core deps)
pip install requests pdfplumber PyPDF2 html2text

# Enhanced (recommended)
pip install -r requirements.txt

# Full features
pip install -r requirements.txt
npm install -g @anthropic/chrome-mcp-server
```

See DEPENDENCIES.md for comprehensive setup guide.

---

## Success Criteria

- ✓ Materials stored in correct directories
- ✓ Minimal metadata extracted (no semantic analysis)
- ✓ Indexes updated (JSON only, no markdown index)
- ✓ Deterministic naming (DOI/hash-based)
- ✓ Error handling (retry + fallback + error artifacts)
- ✓ Skill tree updated (unlock downstream skills)
- ✓ Search confirmation UI working (hybrid model)
- ✓ Configurable depth flags functional
- ✓ Fail gracefully (partial success allowed)
- ✓ arxiv SDK integration (rich metadata)
- ✓ Chrome MCP integration (screenshots)
- ✓ Search automation (prioritized downloads)
- ✓ Optional dependencies documented
- ✓ Graceful fallbacks tested

---

## What NOT to Do

- ✗ Do NOT extract abstract, keywords, citations (belongs in omr-evidence)
- ✗ Do NOT filter or curate materials (user decides)
- ✗ Do NOT fail entire batch if one source fails
- ✗ Do NOT use human-readable filenames (use DOI/hash)
- ✗ Do NOT create markdown indexes (only JSON indexes)
- ✗ Do NOT auto-classify beyond source type (paper/web/github/dataset)
- ✗ Do NOT skip error handling (always retry + fallback + error artifact)

---

## Downstream Skill Integration

| Downstream Skill | omr-collection Outputs Used |
|------------------|----------------------------|
| **omr-evidence** | `raw/paper/*.md`, `docs/index/papers-index.json` |
| **omr-research-plan** | `raw/paper/*.md`, `raw/web/*.md` |
| **omr-decision** | `raw/github/*.md`, `raw/dataset/*.md` |
| **omr-evaluation** | `raw/dataset/*` (if `--download-dataset`) |
| **omr-synthesis** | All `raw/` artifacts |

---

## Prerequisites

- Workspace must exist (created by `omr-bootstrap`)
- If no workspace: Error "Run `/omr-bootstrap` first"

---

## Gates

None (collection can happen anytime)

---

## Can Call

- None (pure logistics, no downstream calls)

---

_Generated from brainstorming-session-2026-04-12-1124.md_