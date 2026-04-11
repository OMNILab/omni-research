---
name: omr-collection
description: Download, classify, and index raw research materials including papers, blogs, GitHub repos, models, datasets, and deep-research reports. Accepts URLs, file paths, or content. Organizes materials into evidence tiers (peer-reviewed papers as primary, technical blogs as supporting, AI-generated reports as leads only). Use when user provides research materials to collect, mentions "add papers", "download sources", or references URLs/repos to include in research.
---

# omr-collection: Collect and Classify Research Materials

## Purpose

Download, classify, and index raw research materials for evidence-bound research. This skill transforms scattered sources into an organized, traceable knowledge base with clear evidence hierarchies.

## Trigger

```
/omr-collection <materials>
```

**Required argument:** `<materials>` - URLs, file paths, or direct content (can be multiple)

**Examples:**
- `/omr-collection https://arxiv.org/abs/2401.12345`
- `/omr-collection ./papers/my-paper.pdf https://github.com/user/repo`
- `/omr-collection "Text content here..." --type blog`

## What This Skill Does

### 1. Material Classification

Classify each input by evidence tier:

| Tier | Type | Role | Storage | Weight |
|------|------|------|---------|--------|
| 1 | Peer-reviewed papers | Primary research evidence | `raw/paper/` | Anchor |
| 2 | Technical blogs | Engineering supplement | `raw/web/` | Supporting |
| 3 | Deep-research reports | Leads only, not anchor evidence | `raw/deep-research/` | Exploratory |
| 4 | GitHub/projects | Implementation reference | `raw/github/` | Practical |
| 5 | AI models | Implementation reference | `raw/models/` | Practical |
| 6 | Benchmarks/datasets | Evaluation reference | `raw/datasets/` | Validation |

**Classification rules:**
- arXiv URLs → `raw/paper/` (pending peer review)
- OpenReview URLs → `raw/paper/`
- Blog URLs → `raw/web/`
- GitHub URLs → `raw/github/`
- PDF files → Analyze metadata, classify as paper or report
- Direct text → Ask user for classification

### 2. Download and Store Materials

**For papers:**
- Download PDF from arXiv, OpenReview, or direct URL
- Extract metadata: title, authors, date, abstract, DOI
- Generate ID: `P-{sequence}` (e.g., P-001, P-002)
- Save to: `raw/paper/arxiv-{id}.pdf` or `raw/paper/{doi-slug}.pdf`

**For GitHub repos:**
- Clone repository to `raw/github/{repo-name}/`
- Extract: README, stars, language, last updated
- Generate ID: `GH-{sequence}`

**For web content:**
- Fetch and parse HTML
- Extract: title, author, date, content
- Save as markdown: `raw/web/{slug}.md`
- Generate ID: `B-{sequence}` for blogs, `W-{sequence}` for general web

**For models/datasets:**
- Download checkpoint files or dataset archives
- Extract metadata: model size, dataset size, format
- Generate ID: `M-{sequence}` for models, `D-{sequence}` for datasets

**For deep-research reports:**
- Accept AI-generated research reports
- Save as markdown: `raw/deep-research/{slug}.md`
- Generate ID: `DR-{sequence}`
- **Important:** Mark as "lead-only, not anchor evidence" in index

### 3. Extract Metadata

**Paper metadata (JSON):**
```json
{
  "id": "P-001",
  "type": "paper",
  "title": "Memory Systems for AI Agents",
  "authors": ["Author One", "Author Two"],
  "date": "2024-01-15",
  "abstract": "This paper explores...",
  "doi": "10.1234/arxiv.2401.12345",
  "arxiv_id": "2401.12345",
  "url": "https://arxiv.org/abs/2401.12345",
  "file": "raw/paper/arxiv-2401.12345.pdf",
  "keywords": ["memory", "agents", "long-term"],
  "evidence_tier": 1,
  "classification_timestamp": "2026-04-11T11:00:00Z"
}
```

**Blog metadata:**
```json
{
  "id": "B-001",
  "type": "blog",
  "title": "Building Production Memory Systems",
  "author": "Tech Company",
  "date": "2024-02-20",
  "url": "https://blog.example.com/memory-systems",
  "file": "raw/web/building-production-memory-systems.md",
  "keywords": ["production", "engineering"],
  "evidence_tier": 2
}
```

**GitHub metadata:**
```json
{
  "id": "GH-001",
  "type": "github",
  "repo": "user/agent-memory-framework",
  "url": "https://github.com/user/agent-memory-framework",
  "path": "raw/github/agent-memory-framework/",
  "description": "A framework for agent memory",
  "stars": 450,
  "language": "Python",
  "last_updated": "2024-03-01",
  "evidence_tier": 4
}
```

### 4. Generate Index Files

**Papers index (`docs/index/papers-index.json`):**
```json
{
  "papers": [
    {
      "id": "P-001",
      "title": "Memory Systems for AI Agents",
      "authors": ["Author One", "Author Two"],
      "date": "2024-01-15",
      "arxiv_id": "2401.12345",
      "file": "raw/paper/arxiv-2401.12345.pdf",
      "keywords": ["memory", "agents"],
      "evidence_tier": 1
    }
  ],
  "last_updated": "2026-04-11T11:00:00Z"
}
```

**Papers index markdown (`docs/index/papers-index.md`):**
```markdown
# Papers Index

Last updated: 2026-04-11

## P-001: Memory Systems for AI Agents
- **Authors:** Author One, Author Two
- **Date:** 2024-01-15
- **arXiv:** [2401.12345](https://arxiv.org/abs/2401.12345)
- **File:** `raw/paper/arxiv-2401.12345.pdf`
- **Keywords:** memory, agents, long-term
- **Evidence Tier:** 1 (Primary)
```

**Similar indexes for:**
- `docs/index/blogs-index.json` + `.md`
- `docs/index/github-index.json` + `.md`
- `docs/index/models-index.json` (if models present)
- `docs/index/datasets-index.json` (if datasets present)

### 5. Update Skill Tree

After successful collection:
- Unlock `omr-evidence` if ≥1 paper collected
- Prompt pattern detection after 3+ sources

**Pattern detection logic:**
- If this is the 3rd+ skill invocation, analyze sequence
- If sequence matches Evidence-First pattern, suggest saving pattern
- Ask user: "Pattern emerging: Evidence-First. Save pattern? [y/N]"

### 6. Trigger Reconciliation Check

If new materials contradict existing evidence:
- Detect contradictions by comparing abstracts/conclusions with existing decisions
- Call `omr-reconcile` automatically if contradiction found

## Metadata

**Collection state:**
```yaml
---
id: COL-001
type: collection
sources_count: 15
papers: 10
blogs: 3
github: 2
models: 0
datasets: 0
deep_research: 0
classification_timestamp: 2026-04-11T11:00:00Z
status: complete
dependencies: []
---
```

## Implementation Details

### URL Handling

**arXiv URLs:**
```
https://arxiv.org/abs/2401.12345 → arxiv-2401.12345.pdf
https://arxiv.org/pdf/2401.12345.pdf → arxiv-2401.12345.pdf
```

**OpenReview URLs:**
```
https://openreview.net/forum?id=XXXXX → openreview-XXXXX.pdf
```

**GitHub URLs:**
```
https://github.com/user/repo → raw/github/repo/
https://github.com/user/repo.git → raw/github/repo/
```

**Generic URLs:**
- Fetch HTML
- Parse title, author, date
- Convert to markdown
- Save as `raw/web/{slug}.md`

### Classification Algorithm

```
For each material:
  1. Detect type from URL/file extension
     - arxiv.org → paper
     - openreview.net → paper
     - github.com → github
     - .pdf → analyze metadata
     - .md/.html → ask user

  2. Extract metadata
     - Paper: title, authors, date, abstract, DOI/arXiv ID
     - Blog: title, author, date, content
     - GitHub: repo name, description, stars, language

  3. Assign evidence tier
     - Peer-reviewed paper → Tier 1
     - arXiv preprint → Tier 1 (pending peer review)
     - Technical blog → Tier 2
     - Deep-research report → Tier 3
     - GitHub repo → Tier 4

  4. Generate ID
     - Papers: P-{sequence}
     - Blogs: B-{sequence}
     - GitHub: GH-{sequence}
     - Models: M-{sequence}
     - Datasets: D-{sequence}
     - Deep-research: DR-{sequence}

  5. Store in appropriate directory
  6. Update index files
```

### Duplicate Detection

Before downloading:
1. Check if URL already in index
2. Check if file already in `raw/`
3. If duplicate detected:
   - Skip download
   - Warn user: "Material already indexed as {ID}"
   - Do not increment sequence counter

### Batch Processing

If multiple materials provided:
- Process in parallel (download, extract metadata)
- Update indexes once after all complete
- Show summary: "✓ 5 papers, 2 blogs, 1 GitHub repo indexed"

### Error Handling

**URL inaccessible:**
- Warn user: "⚠️  Failed to fetch {URL}: {error}"
- Skip and continue with remaining materials
- Do not fail entire batch

**Classification ambiguous:**
- Ask user: "Is this a [1] Paper, [2] Blog, [3] GitHub repo, [4] Other?"
- Proceed with user choice

**Duplicate material:**
- Skip download
- Warn: "Material already indexed as {ID}"
- Continue

**Insufficient metadata:**
- Paper without title: Use filename as placeholder, warn user
- Blog without author: Use "Unknown Author"
- GitHub without description: Use "No description"

## Gates

None (collection can happen anytime)

## Can Call

- `omr-reconcile` (if new material contradicts existing evidence)

## Prerequisites

- Workspace must exist (created by `omr-bootstrap`)
- If no workspace: Error message "Run `/omr-bootstrap` first."

## Examples

### Example 1: Single paper
```
User: /omr-collection https://arxiv.org/abs/2401.12345

System: ✓ Downloading paper...
        ✓ Classified as: Paper (Tier 1)
        ✓ ID: P-001
        ✓ Saved to: raw/paper/arxiv-2401.12345.pdf
        ✓ Indexed: docs/index/papers-index.json

        Title: Memory Systems for AI Agents
        Authors: Author One, Author Two
        Date: 2024-01-15

        Papers indexed: 1
        📊 Skill tree: omr-evidence [READY]
```

### Example 2: Multiple materials
```
User: /omr-collection https://arxiv.org/abs/2401.12345 https://blog.example.com/memory https://github.com/user/repo

System: ✓ Processing 3 materials...

        [1/3] arXiv paper
        ✓ Downloaded: arxiv-2401.12345.pdf → raw/paper/
        ✓ ID: P-001

        [2/3] Blog
        ✓ Fetched: building-production-memory-systems.md → raw/web/
        ✓ ID: B-001

        [3/3] GitHub repo
        ✓ Cloned: agent-memory-framework → raw/github/
        ✓ ID: GH-001

        Summary:
        - Papers: 1 (Tier 1)
        - Blogs: 1 (Tier 2)
        - GitHub: 1 (Tier 4)

        ✓ Updated indexes: papers, blogs, github

        Total materials indexed: 3
        📊 Skill tree: omr-evidence [READY]

        Pattern emerging: Evidence-First (detected)
        Save pattern? [y/N]
```

### Example 3: Duplicate detection
```
User: /omr-collection https://arxiv.org/abs/2401.12345

System: ⚠️  Material already indexed as P-001
        Skipping duplicate.

        Papers indexed: 1 (no change)
```

### Example 4: Ambiguous classification
```
User: /omr-collection https://example.com/unknown-content

System: ⚠️  Could not auto-classify: https://example.com/unknown-content

        Is this a:
        [1] Paper
        [2] Blog
        [3] GitHub repo
        [4] Deep-research report
        [5] Other

User: 2

System: ✓ Classified as: Blog (Tier 2)
        ✓ ID: B-002
        ✓ Saved to: raw/web/unknown-content.md
```

### Example 5: Error handling
```
User: /omr-collection https://arxiv.org/abs/9999.99999 https://valid-url.com

System: Processing 2 materials...

        [1/2] arXiv paper
        ⚠️  Failed to fetch arXiv 9999.99999: Not found
        Skipping...

        [2/2] Web content
        ✓ Fetched: valid-content.md → raw/web/
        ✓ ID: B-003

        Summary:
        - Failed: 1
        - Indexed: 1 (Blogs)

        Total materials indexed: 1
```

## What NOT to Do

- Do NOT claim AI-generated deep-research reports as primary evidence (always mark as Tier 3)
- Do NOT fail entire batch if one material fails (skip and continue)
- Do NOT overwrite existing materials without warning
- Do NOT auto-classify ambiguous materials (ask user)
- Do NOT proceed without workspace (require `omr-bootstrap` first)
- Do NOT skip duplicate detection (always check for existing materials)

## Success Criteria

- [ ] Materials downloaded/cloned to correct directories
- [ ] Metadata extracted and stored
- [ ] Index files updated (JSON + markdown)
- [ ] IDs assigned sequentially
- [ ] Evidence tiers correctly assigned
- [ ] Skill tree updated (unlock `omr-evidence`)
- [ ] Pattern detection triggered if 3+ sources
- [ ] Duplicates detected and skipped
- [ ] Errors handled gracefully (skip and warn)

## Edge Cases

### Deep-research reports

AI-generated research reports (e.g., from deep research tools) should be:
- Classified as Tier 3 (lead-only)
- Stored in `raw/deep-research/`
- Marked in index: `"lead_only": true, "not_anchor_evidence": true`
- Never used as primary evidence for claims

### Private GitHub repos

If GitHub URL requires authentication:
- Warn user: "⚠️  Private repo: {URL}"
- Ask: "Provide authentication token or clone manually?"
- If manual: "Please clone to `raw/github/{repo-name}/` and re-run with path"

### Large files

If file > 50MB:
- Warn: "Large file detected: {size}MB"
- Ask: "Download anyway? [y/N]"
- If yes: Download with progress indicator

### PDFs without metadata

If PDF lacks title/author:
- Extract from filename: `my-paper.pdf` → Title: "My Paper"
- Set author: "Unknown"
- Warn: "Missing metadata, using placeholders"

### Non-English content

If content not in English:
- Detect language
- Store as-is
- Add metadata: `"language": "zh"`
- Note in index: "Non-English content"

## Integration with Other Skills

**After collection:**
- Unlock `omr-evidence` for evidence mapping
- Enable pattern detection (if 3+ invocations)
- Trigger `omr-reconcile` if contradictions detected

**Before collection:**
- Requires `omr-bootstrap` for workspace structure

**Concurrent collection:**
- Multiple `/omr-collection` calls add to existing index
- Sequence IDs increment globally (P-001, P-002, P-003...)