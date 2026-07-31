# OmniResearch

**中文** | [English](README.en.md)

把严谨科研方法做成可复用的 AI Agent 技能：采集材料、界定证据、做判断与决策、实验验证，并以可追溯方式把结论写入文件。

仓库：[OMNILab/omni-research](https://github.com/OMNILab/omni-research)

---

## 愿景

**研究 ≠ 堆材料。** OmniResearch（OMR）把「深研」拆成可组合的技能生命周期：

```text
采集 → 分析（界定 · 证据 · 判断 · 规划）→ 决策 → 验证 → 落盘写回
```

目标不是替你「搜一堆链接」，而是让 Agent 在明确证据边界下推进研究，并留下可检查、可复现、可回滚的产物。

---

## 适用场景

| 场景 | 你会怎么用 |
|------|------------|
| **文献调研 / Survey** | 批量收论文与仓库 → 画证据图 → 写成 survey |
| **从想法起步** | 先记假设 → 再决策 / 实验 → 回填证据 |
| **架构选型** | 先写下备选与取舍 → 用证据与评估约束决策 |
| **快速验证假设** | 先做原型与评估 → 再补分析与综合 |
| **持续迭代课题** | 新证据到来时 reconcile，保留版本与影响范围 |
| **多人 / 多 Agent 协作** | 状态都在文件里（`.omr/`、`docs/`、`materials/`），可审查、可交接 |

安装后，在 Cursor、Claude Code、Codex 等支持 Agent Skills 的环境中，用斜杠命令按需调用即可。

---

## 设计哲学

一句话：**Skills + Tree + Gates + Patterns + Reconciliation**。

| 原则 | 含义 |
|------|------|
| **证据边界** | 主张必须标成 `proven` / `suggested` / `inferred`，禁止过度宣称 |
| **技能可组合** | 技能是原料，不是固定流水线；模式是可保存的配方 |
| **产物即状态** | 进度与结论都在文件中，无隐藏内存状态 |
| **质量门禁** | Gate A–D 约束推进；Gate L 支持「再挖一层 vs 往前走」 |
| **可追溯写回** | 综合报告落盘；聊天只给摘要与路径 |
| **迭代是常态** | 新证据触发 reconcile，而非推倒重来 |

与「一键总结网页」类工具的差别：OMR 强调**边界、门禁、模式与可复现产物**，适合需要严肃论证的科研与工程研究。

更多：[概述](docs/design/overview.md) · [原则](docs/design/principles.md)

---

## 安装技能

**建议一次性装齐全部 9 个技能**，才能走完采集 → 分析 → 决策 → 评估 → 综合（以及灵感记录、证据调和）的完整能力。只装一部分会导致后续阶段不可用。

完整说明（三种方式、各 Agent 路径、排错）：**[技能安装指南](docs/INSTALL.md)**

### 方式 1 — `npx skills add`（推荐）

跨 Cursor / Claude Code / Codex 等 Agent，一条命令批量安装：

```bash
npx skills add OMNILab/omni-research --skill '*' -g -y
```

### 方式 2 — Claude Code Marketplace

```text
/plugin marketplace add OMNILab/omni-research
```

在插件界面安装 **omniresearch** 下的全部 `omr-*` 技能。

### 方式 3 — 下载解压

```bash
git clone https://github.com/OMNILab/omni-research.git
cp -R omni-research/skills/omr-* ~/.cursor/skills/   # Cursor 示例
# 或 ~/.claude/skills/、~/.agents/skills/ 等，见安装指南
```

也可打包为 `.skill` 后再解压到对应目录（见安装指南）。

---

## 快速开始

### 1. 初始化研究工作区

```text
/omr-bootstrap "你的研究主题"
```

只会创建：

- `AGENTS.md` — 给 Agent 的项目说明
- `.omr/tree-state.json` — 技能进度状态

`materials/`、`docs/`、`wiki/`、`src/` 等目录在对应技能**首次写入时**按需创建。

### 2. 进入研究循环

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

静态技能规范保留在已安装技能目录（如 `~/.cursor/skills/`、`~/.claude/skills/`、`~/.agents/skills/`）。研究项目只在 `.omr/` 保存可变状态。

结构说明：[工作区架构](docs/design/architecture.md) · [产出模型](docs/design/outputs.md)

---

## 文档导航

| 用途 | 链接 |
|------|------|
| 安装与配置 | [技能安装指南](docs/INSTALL.md) |
| 设计总览 | [设计文档索引](docs/design/README.md) · [概述](docs/design/overview.md) · [原则](docs/design/principles.md) |
| 技能与契约 | [技能参考](docs/design/skills-reference.md) · [Agent Skill 规范](docs/agent-skill-spec.md) |
| 日常流程 | [工作流](docs/design/workflows.md) · [模式](docs/design/patterns.md) · [门禁](docs/design/gates.md) |
| 可视化 | [技能流程图](docs/omr-skills-flowchart.md) |

---

## 贡献者说明

面向开发的目录布局与打包脚本见 [`skills/`](skills/) 与 [`scripts/`](scripts/)。普通研究使用请优先阅读上文与 [安装指南](docs/INSTALL.md)；深入实现细节可进入设计文档。
