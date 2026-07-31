# OmniResearch

**English** | [中文](#omniresearch-中文)

A suite of AI agent skills for evidence-bound scientific research — collect materials, analyze evidence, make decisions, evaluate ideas, and write findings with clear provenance.

Repository: [OMNILab/omni-research](https://github.com/OMNILab/omni-research)

---

## What you get

OmniResearch turns an AI coding agent into a research co-pilot with a structured workflow:

1. **Start a project** — create a minimal workspace and project context
2. **Collect materials** — papers, repos, web pages, datasets
3. **Analyze evidence** — map claims with strict evidence boundaries (`proven` / `suggested` / `inferred`)
4. **Decide & evaluate** — document architecture choices and validate them
5. **Write up** — save reports to files and get a short summary in chat

You do not need to understand the internal skill packaging model to use it. Install the skills, bootstrap a workspace, then invoke skills as you research.

---

## Quick start

### 1. Install skills

Install foundation first, then the skills you need. See the full guide:

- [Marketplace installation guide](docs/MARKETPLACE-INSTALL.md)

Typical order:

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

### 2. Bootstrap a research workspace

```text
/omr-bootstrap "your research topic"
```

This creates only:

- `AGENTS.md` — project instructions for the agent
- `.omr/tree-state.json` — skill progress state

Content folders such as `materials/`, `docs/`, `wiki/`, and `src/` are created **on demand** when a skill first writes into them.

### 3. Run a research loop

| Goal | Invoke |
|------|--------|
| Collect papers / repos / pages | `/omr-collection` |
| Capture a speculative idea | `/omr-idea-note` |
| Map evidence and plan next steps | `/omr-analyze` |
| Record an architecture decision | `/omr-decision` |
| Design and run an evaluation | `/omr-evaluation` |
| Write findings to files + summary | `/omr-synthesis` |
| Update when new evidence arrives | `/omr-reconcile` |

**Example — Evidence-First path**

```text
/omr-bootstrap "agent memory mechanisms"
/omr-collection "https://arxiv.org/abs/2402.12345"
/omr-analyze
/omr-decision
/omr-evaluation
/omr-synthesis --mode survey
```

Synthesis always writes the full report under `docs/<mode>/` and replies with a short summary only (paths, key findings, gate status).

---

## Skills

| Skill | What it does for you | Spec |
|-------|----------------------|------|
| **omr-core** | Shared infrastructure (contracts, patterns, skill tree) | [SKILL.md](skills/omr-core/SKILL.md) |
| **omr-bootstrap** | Start a research workspace | [SKILL.md](skills/omr-bootstrap/SKILL.md) |
| **omr-collection** | Collect papers, repos, web pages, datasets | [SKILL.md](skills/omr-collection/SKILL.md) |
| **omr-analyze** | Evidence map, judgment, research plan | [SKILL.md](skills/omr-analyze/SKILL.md) |
| **omr-decision** | Architecture decision with alternatives | [SKILL.md](skills/omr-decision/SKILL.md) |
| **omr-evaluation** | Experiment design and validation | [SKILL.md](skills/omr-evaluation/SKILL.md) |
| **omr-synthesis** | File-based report + chat summary (+ wiki) | [SKILL.md](skills/omr-synthesis/SKILL.md) |
| **omr-idea-note** | Capture speculative ideas anytime | [SKILL.md](skills/omr-idea-note/SKILL.md) |
| **omr-reconcile** | Update research when evidence changes | [SKILL.md](skills/omr-reconcile/SKILL.md) |

Flow overview: [OMR skills flowchart](docs/omr-skills-flowchart.md)

---

## Research patterns

Start wherever your work already is — you do not have to begin with literature review.

| Pattern | Start with | Best when |
|---------|------------|-----------|
| Evidence-First | `/omr-collection` | Systematic survey from papers |
| Idea-First | `/omr-idea-note` | You have a hypothesis to explore |
| Decision-First | `/omr-decision` | Architecture choice comes first |
| Experiment-First | `/omr-evaluation` | You want to prototype/test early |
| Rapid-Prototype | collect → synthesize | Fast draft from available material |

Details: [Research patterns](docs/design/patterns.md) · [Workflow examples](docs/design/workflows.md)

---

## Quality gates

Gates keep claims honest and decisions reviewable:

| Gate | When | Ensures |
|------|------|---------|
| **A** | Inside `omr-analyze` | Evidence boundaries and confidence before planning |
| **B** | Before committing a decision | Alternatives and risks are documented |
| **C** | Before trusting evaluation | Metrics and reproducibility are explicit |
| **D** | Before publishing synthesis | Traceability and no over-claiming |

Details: [Quality gates](docs/design/gates.md)

---

## Workspace layout (created as needed)

```text
my-project/
├── AGENTS.md              # created by bootstrap
├── .omr/
│   └── tree-state.json    # created by bootstrap
├── materials/                   # on demand — collected materials
├── docs/                  # on demand — plans, reports, indexes
├── wiki/                  # on demand — living concept pages
└── src/                   # on demand — prototypes / experiments
```

Static skill specs stay in the installed skills (for example under `~/.agents/skills/` or `~/.claude/skills/`). Research projects keep only mutable state in `.omr/`.

Architecture notes: [Workspace architecture](docs/design/architecture.md) · [Outputs model](docs/design/outputs.md)

---

## Documentation

| Audience | Links |
|----------|-------|
| Install & setup | [Marketplace install](docs/MARKETPLACE-INSTALL.md) |
| Design overview | [Design docs index](docs/design/README.md) · [Overview](docs/design/overview.md) · [Principles](docs/design/principles.md) |
| Skills & contracts | [Skills reference](docs/design/skills-reference.md) · [Agent skill spec](docs/agent-skill-spec.md) |
| Day-to-day workflow | [Workflows](docs/design/workflows.md) · [Patterns](docs/design/patterns.md) · [Gates](docs/design/gates.md) |
| Visual map | [Skills flowchart](docs/omr-skills-flowchart.md) |

---

## For contributors

Developer-oriented layout and packaging live under [`skills/`](skills/) and [`scripts/`](scripts/). Prefer the design docs above for system internals; end users should not need them for normal research work.

---

# OmniResearch 中文

[English](#omniresearch) | **中文**

面向科研场景的 AI Agent 技能套件：采集材料、分析证据、做架构决策、实验验证，并以可追溯方式把研究结果写入文件。

仓库：[OMNILab/omni-research](https://github.com/OMNILab/omni-research)

---

## 你能得到什么

OmniResearch 把 AI 编程助手变成有流程约束的研究搭档：

1. **启动项目** — 创建最小工作区与项目上下文
2. **采集材料** — 论文、代码仓库、网页、数据集
3. **分析证据** — 用严格证据边界标注主张（`proven` / `suggested` / `inferred`）
4. **决策与评估** — 记录架构选择并做验证
5. **撰写产出** — 报告落盘，聊天中只返回摘要

日常使用不必了解技能打包细节：安装技能 → bootstrap 工作区 → 按研究需要调用即可。

---

## 快速开始

### 1. 安装技能

先装基础设施，再装你需要的领域技能。完整说明见：

- [Marketplace 安装指南](docs/MARKETPLACE-INSTALL.md)

常用安装顺序：

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

### 2. 初始化研究工作区

```text
/omr-bootstrap "你的研究主题"
```

只会创建：

- `AGENTS.md` — 给 Agent 的项目说明
- `.omr/tree-state.json` — 技能进度状态

`materials/`、`docs/`、`wiki/`、`src/` 等目录会在对应技能**首次写入时**按需创建。

### 3. 进入研究循环

| 目标 | 调用 |
|------|------|
| 采集论文 / 仓库 / 网页 | `/omr-collection` |
| 记录灵感或假设 | `/omr-idea-note` |
| 梳理证据并规划下一步 | `/omr-analyze` |
| 记录架构决策 | `/omr-decision` |
| 设计并运行评估 | `/omr-evaluation` |
| 写报告到文件 + 聊天摘要 | `/omr-synthesis` |
| 新证据到来后更新状态 | `/omr-reconcile` |

**示例 — 证据优先路径**

```text
/omr-bootstrap "agent memory mechanisms"
/omr-collection "https://arxiv.org/abs/2402.12345"
/omr-analyze
/omr-decision
/omr-evaluation
/omr-synthesis --mode survey
```

`omr-synthesis` 始终把完整报告写入 `docs/<mode>/`，聊天中只返回路径、关键发现与门禁状态摘要。

---

## 技能一览

| 技能 | 对你的作用 | 说明 |
|------|------------|------|
| **omr-core** | 共享基础设施（契约、模式、技能树） | [SKILL.md](skills/omr-core/SKILL.md) |
| **omr-bootstrap** | 启动研究工作区 | [SKILL.md](skills/omr-bootstrap/SKILL.md) |
| **omr-collection** | 采集论文、仓库、网页、数据集 | [SKILL.md](skills/omr-collection/SKILL.md) |
| **omr-analyze** | 证据图、判断与研究计划 | [SKILL.md](skills/omr-analyze/SKILL.md) |
| **omr-decision** | 带备选方案的架构决策 | [SKILL.md](skills/omr-decision/SKILL.md) |
| **omr-evaluation** | 实验设计与验证 | [SKILL.md](skills/omr-evaluation/SKILL.md) |
| **omr-synthesis** | 报告落盘 + 聊天摘要（可选 wiki） | [SKILL.md](skills/omr-synthesis/SKILL.md) |
| **omr-idea-note** | 随时记录灵感 | [SKILL.md](skills/omr-idea-note/SKILL.md) |
| **omr-reconcile** | 证据变化时更新研究状态 | [SKILL.md](skills/omr-reconcile/SKILL.md) |

流程总览：[技能流程图](docs/omr-skills-flowchart.md)

---

## 研究模式

可以从你当前所处阶段切入，不必总从文献综述开始。

| 模式 | 入口 | 适合场景 |
|------|------|----------|
| Evidence-First | `/omr-collection` | 从文献系统调研 |
| Idea-First | `/omr-idea-note` | 先有假设再验证 |
| Decision-First | `/omr-decision` | 先有架构立场 |
| Experiment-First | `/omr-evaluation` | 先做原型/实验 |
| Rapid-Prototype | 采集 → 综合 | 快速形成初稿 |

详见：[研究模式](docs/design/patterns.md) · [工作流示例](docs/design/workflows.md)

---

## 质量门禁

| 门禁 | 时机 | 保证 |
|------|------|------|
| **A** | `omr-analyze` 内部 | 规划前证据边界与置信度清楚 |
| **B** | 固化决策前 | 备选方案与风险已记录 |
| **C** | 采信评估前 | 指标与可复现性明确 |
| **D** | 发布综合报告前 | 可追溯，且无过度宣称 |

详见：[质量门禁](docs/design/gates.md)

---

## 工作区结构（按需创建）

```text
my-project/
├── AGENTS.md              # bootstrap 创建
├── .omr/
│   └── tree-state.json    # bootstrap 创建
├── materials/                   # 按需 — 原始材料
├── docs/                  # 按需 — 计划、报告、索引
├── wiki/                  # 按需 — 概念页面
└── src/                   # 按需 — 原型 / 实验
```

静态技能规范保留在已安装技能目录（如 `~/.agents/skills/` 或 `~/.claude/skills/`）。研究项目只在 `.omr/` 保存可变状态。

结构说明：[工作区架构](docs/design/architecture.md) · [产出模型](docs/design/outputs.md)

---

## 文档导航

| 用途 | 链接 |
|------|------|
| 安装与配置 | [Marketplace 安装](docs/MARKETPLACE-INSTALL.md) |
| 设计总览 | [设计文档索引](docs/design/README.md) · [概述](docs/design/overview.md) · [原则](docs/design/principles.md) |
| 技能与契约 | [技能参考](docs/design/skills-reference.md) · [Agent Skill 规范](docs/agent-skill-spec.md) |
| 日常流程 | [工作流](docs/design/workflows.md) · [模式](docs/design/patterns.md) · [门禁](docs/design/gates.md) |
| 可视化 | [技能流程图](docs/omr-skills-flowchart.md) |

---

## 贡献者说明

面向开发的目录布局与打包脚本见 [`skills/`](skills/) 与 [`scripts/`](scripts/)。普通研究使用请优先阅读上文；深入实现细节可进入设计文档。
