# LifeOS 知识管理

[English](README.md)

LifeOS 是一套由 AI 主导、在使用中不断生长的知识管理系统。把值得保留的内容沉淀到本地 Markdown 知识库，让 Codex 在真实任务中参考它，再从反复用到的方法里找出适合做成 Skill 的候选。

## 安装到 Codex

选择一个语言版本。在终端执行以下命令，然后在 Codex 桌面端打开已安装的插件并新开对话。建库和统计脚本需要 Python 3.11 或更新版本。

```sh
codex plugin marketplace add gilbertwuu/lifeos-knowledge@v0.1.0
codex plugin add lifeos-knowledge-zh@lifeos-knowledge
```

[中文版插件指南](plugins/lifeos-knowledge-zh/README.md)列出三个 Skill 和三份定时任务配置指南。[发布页](https://github.com/gilbertwuu/lifeos-knowledge/releases)提供下载包。

如果下载了 ZIP，解压后把上面第一条命令中的 GitHub 仓库地址换成解压目录的路径。

## 跑一遍完整流程

1. **入库**。请 Codex 在你选的空文件夹建库，再给它一条有来源、值得保留的材料。AI 查重、整理并更新索引。用 Obsidian 打开同一个目录，可以看正文、链接和反向链接。
2. **调用**。[把调用规则加到 `AGENTS.md`](plugins/lifeos-knowledge-zh/skills/lifeos-knowledge-base/assets/vault/接入说明.md)，填入自己的知识库路径。新开对话，给 Codex 一件与库内笔记相关的普通任务，检查它有没有主动找到笔记并用上其中的方法。
3. **复盘**。每日统计核对指定 Codex 记录里的实际读取。周回顾从独立任务里找重复方法，对照已有 Skill，给出新建或补强的建议，由你决定是否采纳。

三份指南分别对应每日知识沉淀、每日复用统计和每周 Skill 建议。定时安排、输入范围和知识库由你选择。0.1.0 的自动统计识别指定 Codex 本地 JSONL 记录中的显式单文件 `cat` 读取。
