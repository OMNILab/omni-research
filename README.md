# OmniResearch

**中文** | [English](README.en.md)

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
| Loop | `/omr-idea-note` 或 `/omr-collection` | 用 Gate L 循环深化想法或证据 |

详见：[研究模式](docs/design/patterns.md) · [工作流示例](docs/design/workflows.md)

---

## 质量门禁

| 门禁 | 时机 | 保证 |
|------|------|------|
| **A** | `omr-analyze` 内部 | 规划前证据边界与置信度清楚 |
| **B** | 固化决策前 | 备选方案与风险已记录 |
| **C** | 采信评估前 | 指标与可复现性明确 |
| **D** | 发布综合报告前 | 可追溯，且无过度宣称 |
| **L** | Loop 模式（analyze / idea-note） | 继续深化，或推进到下一阶段 |

详见：[质量门禁](docs/design/gates.md)

---

## 工作区结构（按需创建）

```text
my-project/
├── AGENTS.md              # bootstrap 创建
├── .omr/
│   ├── tree-state.json    # bootstrap 创建
│   └── loop-state.json    # Loop / Gate L 激活时
├── materials/             # 按需 — 采集材料
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
