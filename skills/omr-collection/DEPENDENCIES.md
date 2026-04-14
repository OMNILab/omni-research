# Dependencies Guide for omr-collection Skill

This document explains the optional and required dependencies for the `omr-collection` skill, installation instructions, and fallback behaviors when optional dependencies are unavailable.

---

## Overview

**Philosophy**: Optional dependencies with graceful fallback

The skill is designed to work with **minimal core dependencies** and gracefully degrade when optional enhanced dependencies are unavailable. This ensures the skill remains functional even without all optional packages installed.

---

## Core Dependencies (Required)

These dependencies are **required** for basic functionality:

| Package | Version | Purpose |
|---------|---------|---------|
| `requests` | >=2.28.0 | HTTP client for API calls and web fetching |
| `pdfplumber` | >=0.7.0 | PDF text extraction (fallback parser) |
| `PyPDF2` | >=3.0.0 | PDF text extraction (last resort fallback) |
| `html2text` | >=2020.1.16 | HTML to markdown conversion |

**Installation**:
```bash
pip install requests pdfplumber PyPDF2 html2text
```

**What works with core only**:
- ✓ Basic paper downloads via HTTP
- ✓ GitHub repo README fetch
- ✓ HuggingFace README + metadata
- ✓ Webpage fetch (HTML → markdown)
- ✓ arxiv API search
- ✓ GitHub API search

**What doesn't work**:
- ✗ Rich paper metadata (title, authors, DOI, categories)
- ✗ Webpage screenshots
- ✗ Reliable arxiv downloads with retry logic
- ✗ Google Scholar search automation

---

## Optional Dependencies

### 1. arxiv Python SDK (Enhanced Paper Downloads)

**Package**: `arxiv>=3.0.0`

**Why install it?**
- Built-in retry logic (3 retries with 3s delay)
- Rich metadata: title, authors, DOI, categories, abstract
- Proper PDF download with progress tracking
- Better error handling for network issues
- Avoids XML parsing complexity

**Installation**:
```bash
pip install arxiv
```

**Fallback behavior (if not installed)**:
- Paper downloads use direct HTTP requests
- Minimal metadata (arxiv ID + source URL only)
- No retry logic beyond orchestrator defaults
- Works but less reliable and informative

**Feature comparison**:

| Feature | With arxiv SDK | Without SDK (HTTP fallback) |
|---------|---------------|----------------------------|
| Metadata | Title, authors, DOI, categories, abstract, published date | arxiv ID, source URL only |
| Retry logic | 3 retries with 3s delay (built-in) | 2 retries with 2s delay (orchestrator) |
| PDF download | Progress tracking, proper error handling | Simple HTTP stream download |
| Reliability | Higher (better error recovery) | Lower (network failures more likely) |

**Example output difference**:

With SDK:
```markdown
# Paper

**Title**: Agent Memory Survey
**Authors**: John Smith, Jane Doe
**Date**: 2026-02-15
**DOI**: 10.1234/paper
**arXiv**: 2402.12345
**Categories**: cs.AI, cs.CL
```

Without SDK:
```markdown
# Paper

**arXiv**: 2402.12345
**Source**: https://arxiv.org/abs/2402.12345
```

---

### 2. MCP Python SDK (Chrome MCP Integration)

**Package**: `mcp>=1.0.0`

**Why install it?**
- Webpage screenshot capture (PNG)
- Better markdown conversion from rendered pages
- Google Scholar search automation
- Handles JavaScript-rendered content properly

**Installation**:
```bash
pip install mcp
```

**Also requires**: Chrome MCP server (npm package)

```bash
npm install -g @anthropic/chrome-mcp-server
```

**Fallback behavior (if not installed)**:
- Webpage fetch uses simple HTTP requests
- No screenshot capture
- Markdown conversion from raw HTML (no JavaScript rendering)
- Search uses arxiv API only (no Google Scholar)

**Feature comparison**:

| Feature | With Chrome MCP | Without MCP (HTTP fallback) |
|---------|----------------|----------------------------|
| Screenshot | PNG snapshot of rendered page | Not available |
| Markdown | From rendered page (JavaScript executed) | From raw HTML (no JS) |
| Search | Google Scholar + arxiv | arxiv API only |
| JavaScript | Properly rendered | Not executed |
| Dynamic content | Captured correctly | Missing or incorrect |

**Chrome MCP server setup**:

The Chrome MCP server is a Node.js package that provides Chrome automation tools:

```bash
# Option 1: Install globally
npm install -g @anthropic/chrome-mcp-server

# Option 2: Use npx (no installation needed)
# The skill will automatically use npx -y @anthropic/chrome-mcp-server
# This works without global installation
```

**Server detection**:
- Skill checks for npm package availability
- If unavailable, falls back to HTTP fetch
- No configuration needed (stdio transport auto-start)

**Currently available MCP tools**:
- `navigate(url)` - Navigate to URL
- `screenshot()` - Capture PNG snapshot
- `read_page(format)` - Read page content (markdown/HTML)

**Future tools** (placeholder for search automation):
- `type(selector, text)` - Type text in input
- `click(selector)` - Click element
- `extract_results(selector, max_results)` - Extract search results

---

### 3. HuggingFace Hub Library (Dataset/Model Downloads)

**Package**: `huggingface_hub>=0.20.0`

**Why install it?**
- Download full datasets (not just README)
- Download model weights
- Proper handling of HF Hub structure
- Resume interrupted downloads

**Installation**:
```bash
pip install huggingface_hub
```

**Fallback behavior (if not installed)**:
- README + card metadata only
- No dataset/model file downloads
- Works for research planning but not evaluation

**Usage flags**:
```bash
# Download full dataset
/omr-collection "huggingface.co/datasets/user/data" --download-dataset

# Download model weights
/omr-collection "huggingface.co/models/user/model" --download-model
```

**Error if flag used without library**:
```
RuntimeError: huggingface_hub library required for dataset download.
Install: pip install huggingface_hub
```

---

## Installation Strategies

### Strategy 1: Minimal (Core Only)

**Command**:
```bash
pip install requests pdfplumber PyPDF2 html2text
```

**What you get**:
- Basic functionality
- HTTP-based paper downloads
- Simple webpage markdown conversion
- API-based search (arxiv, GitHub, HF)

**Use case**:
- Quick setup for basic material collection
- Testing and development
- Environments with limited package access

---

### Strategy 2: Enhanced Paper Handling

**Command**:
```bash
pip install requests pdfplumber PyPDF2 html2text arxiv
```

**What you get**:
- Reliable paper downloads with rich metadata
- Better error recovery
- Progress tracking for large PDFs

**Use case**:
- Research projects focused on academic papers
- Need reliable downloads and metadata
- Most common setup for paper collection

---

### Strategy 3: Full Web Features

**Command**:
```bash
pip install -r requirements.txt
npm install -g @anthropic/chrome-mcp-server
```

**What you get**:
- Everything from Strategy 2
- Webpage screenshots
- Rendered page markdown
- Google Scholar search (when implemented)

**Use case**:
- Comprehensive web content collection
- Need screenshots for documentation
- Research involving blogs, documentation sites

---

### Strategy 4: Maximum Features

**Command**:
```bash
pip install -r requirements.txt
npm install -g @anthropic/chrome-mcp-server
```

**What you get**:
- All optional dependencies
- Full dataset/model downloads
- Maximum search coverage

**Use case**:
- Full research workflow
- Experiment-First pattern (needs actual datasets)
- Maximum feature availability

---

## Checking Dependency Status

Use the built-in checker:

```bash
# Check MCP SDK and Chrome server
python skills/omr-collection/mcp_client.py

# Test arxiv SDK
python skills/omr-collection/handlers/paper_handler.py /tmp/test 2402.12345

# Test full collection
python skills/omr-collection/orchestrator.py /tmp/test 2402.12345
```

**Output will show**:
```
MCP Python SDK: ✓ Installed
Chrome MCP Server: ✗ Not installed
arxiv SDK: ✓ Installed
```

---

## Troubleshooting

### Issue: "ImportError: No module named 'arxiv'"

**Solution**:
```bash
pip install arxiv
```

**Impact**: Paper downloads will work but with HTTP fallback (minimal metadata)

---

### Issue: "RuntimeError: Chrome MCP server not installed"

**Solution**:
```bash
npm install -g @anthropic/chrome-mcp-server
```

**Alternative**: Use npx (no installation):
```bash
# Skill will auto-use npx -y @anthropic/chrome-mcp-server
# This works without global install
```

**Impact**: Webpage fetch will use HTTP fallback (no screenshots)

---

### Issue: "RuntimeError: huggingface_hub required for dataset download"

**Solution**:
```bash
pip install huggingface_hub
```

**Alternative**: Remove `--download-dataset` flag (README-only mode)

---

### Issue: npm/npx not found

**Solution**:
```bash
# Install Node.js and npm
# macOS: brew install node
# Linux: apt-get install nodejs npm
# Windows: Download from nodejs.org
```

**Impact**: Chrome MCP unavailable, use HTTP fallback for webpages

---

## Dependency Philosophy

**Why optional dependencies?**

1. **Portability**: Skill works in minimal environments
2. **Flexibility**: Users choose features they need
3. **Graceful degradation**: No hard failures, always functional
4. **Testing**: Can test fallback behavior easily

**Pattern used**:

```python
try:
    import arxiv
    # Use enhanced method
    result = fetch_with_sdk()
except ImportError:
    # Use fallback method
    result = fetch_with_http()
```

This pattern ensures:
- Skill never crashes due to missing optional package
- Always has functional fallback
- Logs which method used for transparency

---

## Future Dependencies

**Potential additions** (not yet implemented):

| Package | Feature | Status |
|---------|---------|--------|
| `semanticscholar` | Semantic Scholar API search | Not planned |
| `crossrefapi` | DOI metadata lookup | Not planned |
| `pypaperbot` | Alternative paper fetcher | Not planned |

---

## Summary

| Setup | Install Time | Features | Reliability |
|-------|--------------|----------|-------------|
| Minimal (core) | ~1 min | Basic downloads, API search | Medium |
| Enhanced (+arxiv) | ~2 min | Rich metadata, reliable papers | High (papers) |
| Full (+MCP) | ~5 min | Screenshots, rendered pages | High (all) |
| Maximum (+HF) | ~7 min | Datasets, models, everything | Maximum |

**Recommendation**:
- Start with **Enhanced** (Strategy 2) for most research
- Add **MCP** (Strategy 3) if you need screenshots
- Add **HF Hub** only if downloading datasets/models

**All fallbacks tested**: ✓ Verified to work when optional deps unavailable