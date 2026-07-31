# OmniResearch Skill Installation Guide

Install the full OmniResearch skill suite so agents can run the complete research lifecycle — collection, analysis, decision, evaluation, synthesis, idea capture, and reconciliation.

**Recommendation:** install **all 9 skills in one batch**. Partial installs leave gaps (for example synthesis without analyze, or reconcile without core infrastructure).

| Skill | Role |
|-------|------|
| `omr-core` | Shared infrastructure (contracts, patterns, skill tree) — required by all others |
| `omr-bootstrap` | Initialize a research workspace |
| `omr-collection` | Collect papers, repos, pages, datasets |
| `omr-analyze` | Evidence map, judgment, research plan |
| `omr-decision` | Architecture decisions with alternatives |
| `omr-evaluation` | Experiment design and validation |
| `omr-synthesis` | Write findings to files (+ optional wiki) |
| `omr-idea-note` | Capture speculative ideas anytime |
| `omr-reconcile` | Update state when evidence changes |

Three install paths, in preferred order:

1. **[npx skills add](#1-npx-skills-add-recommended)** — works across Cursor, Claude Code, Codex, and many other agents
2. **[Claude Code marketplace](#2-claude-code-marketplace)** — native plugin flow inside Claude Code
3. **[Download and extract](#3-download-and-extract)** — manual copy into each agent's skill directory

---

## 1. `npx skills add` (recommended)

Uses the open [Agent Skills CLI](https://github.com/vercel-labs/skills). One command installs the whole suite to the agents you use.

### Install all skills (batch)

```bash
# Interactive: pick agents, then install every skill from this repo
npx skills add OMNILab/omni-research --skill '*'

# Global install (available in every project) + skip prompts
npx skills add OMNILab/omni-research --skill '*' -g -y

# Target specific agents
npx skills add OMNILab/omni-research --skill '*' -a cursor -a claude-code -g -y

# Install everything to every detected agent
npx skills add OMNILab/omni-research --all
```

### Useful variants

```bash
# List skills in the repo without installing
npx skills add OMNILab/omni-research --list

# Install only foundation + bootstrap (not recommended for full workflow)
npx skills add OMNILab/omni-research --skill omr-core --skill omr-bootstrap -g -y

# Update later
npx skills update
```

### Where skills land

| Scope | Flag | Typical location |
|-------|------|------------------|
| Project | (default) | `./.agents/skills/` or agent-specific project dir |
| Global | `-g` | Agent home dir (see [manual paths](#agent-skill-directories)) |

After install, restart the agent session or reload skills if needed.

---

## 2. Claude Code marketplace

Use this when you work primarily inside Claude Code and prefer the built-in plugin UI.

```text
/plugin marketplace add OMNILab/omni-research
```

Then install OmniResearch skills from the marketplace (Discover / Plugins UI), **or** install each skill you need:

```text
/plugin
```

Browse the **omniresearch** marketplace and enable the full set of `omr-*` skills.

Alternatively, discover by name:

```text
/find-skills omr-core
/find-skills omr-bootstrap
/find-skills omr-collection
/find-skills omr-analyze
/find-skills omr-decision
/find-skills omr-evaluation
/find-skills omr-synthesis
/find-skills omr-idea-note
/find-skills omr-reconcile
```

`omr-core` must be present before other domain skills can load shared infrastructure. Installing the full set still avoids missing later stages of the workflow.

Reload if skills do not appear:

```text
/reload-plugins
```

---

## 3. Download and extract

Use this for offline installs, custom agents, or when `npx` / marketplace is unavailable.

### Option A — clone the repo

```bash
git clone https://github.com/OMNILab/omni-research.git
cd omni-research
```

Copy every skill folder into your agent's global skills directory:

```bash
# Example: Cursor
mkdir -p ~/.cursor/skills
cp -R skills/omr-* ~/.cursor/skills/

# Example: Claude Code
mkdir -p ~/.claude/skills
cp -R skills/omr-* ~/.claude/skills/

# Example: Codex / universal agents path
mkdir -p ~/.agents/skills
cp -R skills/omr-* ~/.agents/skills/
```

### Option B — package `.skill` archives, then unzip

From a clone of this repo:

```bash
python scripts/package_all_skills.py ./dist
```

Each `dist/omr-*.skill` file is a ZIP. Extract into the agent skills directory:

```bash
# Claude Code example
for f in dist/omr-*.skill; do
  name=$(basename "$f" .skill)
  mkdir -p ~/.claude/skills/"$name"
  unzip -o "$f" -d ~/.claude/skills/"$name"
done
```

Repeat for Cursor (`~/.cursor/skills/`), Codex (`~/.codex/skills/` or `~/.agents/skills/`), or other agents below.

### Agent skill directories

| Agent | Global skills path | Project skills path |
|-------|--------------------|---------------------|
| Cursor | `~/.cursor/skills/` | `.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex | `~/.codex/skills/` | `.agents/skills/` |
| OpenCode | `~/.config/opencode/skills/` | `.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `.agents/skills/` |
| Windsurf | `~/.codeium/windsurf/skills/` | `.windsurf/skills/` |
| Cline / Warp / Zed | `~/.agents/skills/` | `.agents/skills/` |

Many other agents follow the same layout; `npx skills add` detects them automatically. See the [skills CLI agent table](https://github.com/vercel-labs/skills#supported-agents) for the full list.

Each skill directory must contain `SKILL.md` at its root, for example:

```text
~/.cursor/skills/omr-core/SKILL.md
~/.cursor/skills/omr-bootstrap/SKILL.md
...
```

---

## Verify installation

```bash
# Via skills CLI
npx skills list

# Or check filesystem (adjust path for your agent)
ls ~/.cursor/skills/omr-*
ls ~/.claude/skills/omr-*
ls ~/.agents/skills/omr-*
```

You should see all nine: `omr-core`, `omr-bootstrap`, `omr-collection`, `omr-analyze`, `omr-decision`, `omr-evaluation`, `omr-synthesis`, `omr-idea-note`, `omr-reconcile`.

---

## After install: quick start

```text
/omr-bootstrap "your research topic"
```

Creates only:

- `AGENTS.md` — project context for the agent
- `.omr/tree-state.json` — skill progress state

Content folders (`materials/`, `docs/`, `wiki/`, `src/`) are created **on demand** when a skill first writes.

Then run a research loop, for example Evidence-First:

```text
/omr-collection "https://arxiv.org/abs/2402.12345"
/omr-analyze
/omr-decision
/omr-evaluation
/omr-synthesis --mode survey
```

See the [README](../README.en.md) for patterns, gates, and day-to-day usage.

---

## Dependency notes

- **Runtime dependency:** domain skills resolve shared code from installed `omr-core` (contracts, patterns, `runtime_utils`).
- **Workspace dependency:** most skills expect an initialized workspace (`/omr-bootstrap` first).
- **Artifact dependency:** later skills unlock when earlier skills produce artifacts (skill tree). Install all skills up front; unlock order is about research progress, not install order.

### Common errors

| Symptom | Fix |
|---------|-----|
| Infrastructure not found | Install `omr-core` (or reinstall the full suite) |
| Workspace not initialized | Run `/omr-bootstrap "topic"` |
| Prerequisites missing | Run the skill that produces the missing artifact (see skill tree) |
| Skill not listed in agent | Restart session / reload plugins; confirm files under the agent skills path |

---

## For contributors (packaging)

```bash
# Package all skills as .skill ZIPs
python scripts/package_all_skills.py ./dist

# Package a subset
python scripts/package_all_skills.py ./dist --skills omr-core,omr-bootstrap

# Smoke-test packaged layout
python scripts/test_marketplace_install.py ./dist
```

Marketplace catalog: [`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json).

---

**Last updated:** 2026-07-31  
**OmniResearch version:** 2.0.0
