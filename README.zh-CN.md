# LifeOS 知识管理

[English](README.md)

LifeOS 是一套由 AI 主导、在使用中不断生长的知识管理系统。AI 从日常工作中筛出值得留下的知识，在下一次任务里用上它，再根据真实的使用记录，把反复用到的做法整理成可调用的 Skill。

## LifeOS 怎样运转

```mermaid
flowchart TD
    A["日常积累 · 对话、资料、项目实践"] --> B["筛选、去重、整理"]
    B --> C["本地 Markdown 知识库"]
    C --> D["在 Obsidian 阅读正文、链接与反向链接"]
    C --> E["新任务 · AGENTS.md 引导 Codex 查索引和笔记"]
    E --> F["将知识用到任务中，留下读取记录"]
    F --> G["每日复盘 · 核对读取、更新索引与台账"]
    G --> H["每周复盘 · 从独立任务中找重复方法"]
    H --> I["你决定是否新建或补强 Skill"]
    I --> J["用下一项真实任务验证并复用"]
    J --> E
    J --> A
```

### 1. 从日常积累到本地知识库

把对话、资料和项目实践中的收获交给 Codex。你可以随手请它保存，也可以设置「每日知识沉淀」，让 AI 在你授权的范围内回看当天新增的对话内容。AI 先判断内容将来能不能帮助判断、创作或解决问题，再查索引和相关正文，优先给已有笔记补充新证据。原始材料、还在思考的问题、已经可以复用的方法分别存入 Sources、Notes 和 Wiki，并通过 `INDEX.md` 找到入口。

笔记是本地 Markdown 文件。用 Obsidian 打开同一个文件夹，就能阅读正文、沿链接找到相关笔记，也能从反向链接查看还有哪些笔记引用了它。

### 2. 从知识库到真实任务

在 Codex 全局或项目的 `AGENTS.md` 加入调用规则，填上知识库路径。新任务开始时，Codex 先判断库里的背景、方法或经验能不能帮上忙。有相关内容时，它先看 `INDEX.md`，再读笔记正文，必要时追溯来源。比如分析用户反馈时，AI 可以用库里的方法把已观察的现象、可能的解释和下一步核对分开，再结合当前证据给出判断。 [可复制的接入规则](plugins/lifeos-knowledge/skills/lifeos-knowledge-base/assets/vault/SETUP.md)

### 3. 从使用记录到可复用的 Skill

- **每天核对用过什么。** 每日复用统计回看前一个完整自然日，核对哪些 Wiki 真的读了正文、在什么任务里派上了什么用场。确认后把计数写入 `INDEX.md`，把用途和证据留在台账里。反复扫描同一条读取记录只记一次。
- **每周判断哪些做法值得留下。** 周回顾先看每日统计，再回查独立任务和实际输出。比如两个不同项目都在用「先列观察，再提出竞争解释，最后设计核对」，AI 会比较它们的步骤和验收，并查看现有 Skill 是否已覆盖。建议可能是新建 Skill、补强已有 Skill，或继续把方法保留为 Wiki。
- **用下一项任务检验。** 你决定采纳后，把触发条件、所需资料、步骤和验收标准写进 Skill。下一次遇到相似任务，就能按场景调用。实际使用留下的新证据，又能用于补充笔记或改进 Skill。

## 插件提供什么

| 入口 | 用途 |
| --- | --- |
| 知识库搭建与使用 | 初始化 Markdown 库、筛选入库、查重、查找和使用笔记 |
| 知识复用统计 | 核对读取证据、预览并更新索引与台账 |
| Skill 沉淀周回顾 | 比较真实任务和现有 Skill，形成供你决定的建议 |

三份定时任务指南分别是 [每日知识沉淀](plugins/lifeos-knowledge/guides/01-daily-knowledge-capture.md)、[每日复用统计](plugins/lifeos-knowledge/guides/02-daily-reuse-statistics.md)和[每周 Skill 回顾](plugins/lifeos-knowledge/guides/03-weekly-skill-review.md)。你可以先手动跑一轮，再按自己的时区、资料范围和库路径配置定时任务。当前自动统计覆盖选定 Codex 本地 JSONL 记录中能匹配到笔记正文的显式单文件 `cat` 读取。

## 安装到 Codex

需要 Codex CLI。建库和复用统计需要 Python 3.11 或更新版本。

```sh
codex plugin marketplace add gilbertwuu/lifeos-knowledge@v0.1.1
codex plugin add lifeos-knowledge@lifeos-knowledge
```

安装后在 Codex 桌面端打开 **LifeOS Knowledge** 并新开对话。可以先说「在我指定的空文件夹里初始化一个 LifeOS 知识库」，接着试着保存一条笔记，再从另一个任务验证主动调用。

[下载 ZIP](https://github.com/gilbertwuu/lifeos-knowledge/releases/download/v0.1.1/lifeos-knowledge-0.1.1.zip)后也可从本地安装。解压后，将第一条命令中的 GitHub 地址替换为解压目录路径。
