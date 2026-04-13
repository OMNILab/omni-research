# Overview and Research Philosophy

## Overall Rules

- Follow agent skill spec strictly
- Leverage `skill-creator` skill primarily to manage skills
- Follow Claude skill marketplace patterns
- **Evidence-bound research**: All claims traceable to sources with explicit boundaries
- **Gate-driven quality**: Stages separated by review gates; no skipping ahead
- **Pattern-based composition**: Skills are composable ingredients; patterns are templates

## Project Overview

Omni-Research is a skill set for general-purpose deep research, adapted from Prof. Jin's `agent-memory-survey` architecture. It transforms rigorous research methodology into reusable agent skills applicable to any topic.

### Core Capabilities

- **Broad input acceptance**: Web links, text snippets, GitHub projects, papers, videos, and more — all classified as raw materials
- **Full research lifecycle**: Not just information gathering — explore, develop, validate, and writeback
- **Dual output model**: Static documents (authoritative, evidence-bound) + living wiki (continuously updated)
- **Pattern flexibility**: Multiple research patterns (Evidence-First, Idea-First, Decision-First, Experiment-First, Rapid-Prototype)
- **Configurable synthesis**: Survey, report, manuscript, or brief — output type defined by pattern

## Research Philosophy

### Core Stance: `research ≠ information-gathering`

True deep research requires a complete lifecycle:

```
Collection → Definition → Evidence → Judgment → Decision → Validation → Writeback
```

Research outputs must be:

- **Traceable**: Every claim links to source, decision, or experiment
- **Evidence-bound**: Clear boundaries between "proven", "suggested", "inferred"
- **Reproducible**: Artifacts (code, data, configs) versioned alongside conclusions

### Evidence Hierarchy

Materials are classified by evidence strength:

| Tier | Type | Role | Storage |
|------|------|------|---------|
| 1 | Peer-reviewed papers | Primary research evidence | `raw/paper/` |
| 2 | Technical blogs | Engineering supplement | `raw/web/` |
| 3 | Deep-research reports | Leads only, not anchor evidence | `raw/deep-research/` |
| 4 | GitHub/projects | Implementation reference | `raw/github/` |
| 5 | AI models | Implementation reference | `raw/models/` |
| 6 | Benchmarks/datasets | Evaluation reference | `raw/datasets/` |

**Non-negotiable**: Never claim "paper proves X" when it only suggests.

### Evidence-Bound Argumentation

**Three levels of evidence strength:**

| Level | Label | Meaning |
|-------|-------|---------|
| **Proven** | "Paper X validates..." | Experimental validation, strong evidence |
| **Suggested** | "Paper X suggests..." | Indirect evidence, reasonable inference |
| **Inferred** | "Based on X, we infer..." | Multi-source synthesis, explicit boundary |

**Example in synthesis:**
```markdown
Evidence: Paper A validates importance threshold scoring (experimental, n=1000).
          Paper B suggests graph memory improves retrieval (limited evaluation, n=50).
          We infer that hybrid approach combines validated threshold with promising graph structure.

Note: Paper B provides supporting evidence only — not proven.
```