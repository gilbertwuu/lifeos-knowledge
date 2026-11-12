# 安装与兼容性说明

[English](compatibility.md) · [LifeOS 完整流程](../README.md#简体中文)

## 用同一个下载包接入你的 Agent

1. 解压 [LifeOS ZIP](https://github.com/gilbertwuu/lifeos-knowledge/releases/download/v0.2.0/lifeos-knowledge-0.2.0.zip)。[plugins/lifeos-knowledge/skills](../plugins/lifeos-knowledge/skills) 下有三个独立目录，遵循 [Agent Skills 格式](https://agentskills.io/specification)。复制时保留目录名和里面的全部文件。
2. 将这三个目录放进你的工具会读取的 Skill 目录，或逐个用导入功能接入。例如，会扫描 `.agents/skills/` 的工具可以使用项目下这个目录。Claude Code 支持项目下的 `.claude/skills/`。如果导入器要求每个 Skill 一个 ZIP，可以把同一下载包中的对应目录单独压缩。如果工具不支持加载 Skill，可把 `SKILL.md` 和引用的材料作为任务指令。[Claude Code 项目 Skill 说明](https://code.claude.com/docs/en/skills)
3. 新开对话，调用 `lifeos-knowledge-base` 初始化测试库。按[接入规则](../plugins/lifeos-knowledge/skills/lifeos-knowledge-base/assets/vault/SETUP.md)配置工具的长期指令。给 Agent 读库权限，需要直接存入库时再给写入权限。如果只能上传附件，就随任务提供文件，自己保存返回的结果。

## 配置定时任务和复用证据

| 任务 | 输入与产出 | 自动或手动 |
| --- | --- | --- |
| [每日知识沉淀](../plugins/lifeos-knowledge/skills/lifeos-knowledge-base/references/daily-capture.md) | 指定对话或导出 → 笔记、索引和检查点 | 定时环境能读原材料并写库时可自动跑。也可手工提供材料运行。 |
| [每日复用统计](../plugins/lifeos-knowledge/skills/lifeos-wiki-reuse/references/daily-reuse.md) | 原任务的读取和使用证据 → 日台账或经核对的采集结果 | 定时 Agent 能读取证据时可自动核对。没有日志时，从实际工作中记下证据，或手工提供原任务摘录。 |
| [每周 Skill 回顾](../plugins/lifeos-knowledge/skills/lifeos-skill-review/references/weekly-review.md) | 日台账或统计导出、实际任务、现有 Skill → 建议报告 | 等日统计落盘后定时运行，也可以手工提供材料。具体 Skill 改造由你决定。 |

每个提示词都要填时区、授权范围、知识库路径和输出位置。先手动跑通一次，再把同一份提示词放进工具的定时设置。第一次到点执行时，核对触发时间和文件权限。安装 Skill 本身不会创建定时任务。

Markdown 台账无需运行脚本。可选的自动采集器需要 POSIX 环境和 Python 3.11 或更新版本，读取指定 Codex 本地 JSONL 中能匹配笔记正文的单文件 `cat` 记录。确认实际用途后再写入统计。

## 可选的 Codex 插件安装

```sh
codex plugin marketplace add gilbertwuu/lifeos-knowledge@v0.2.0
codex plugin add lifeos-knowledge@lifeos-knowledge
```

从本地安装时，将第一条命令中的 GitHub 地址替换为解压目录。已登记旧版 GitHub 发布源时，先运行 `codex plugin marketplace remove lifeos-knowledge`，再执行安装命令。这会移除旧发布源登记，知识库仍在原来选定的文件夹。
