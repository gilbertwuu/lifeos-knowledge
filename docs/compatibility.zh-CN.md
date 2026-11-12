# 兼容性说明

[English](compatibility.md) · [LifeOS 完整流程](../README.zh-CN.md)

知识库是一组本地 Markdown 文件。只要 Agent 能访问这些文件并遵循长期指令，就可以沿用入库和调用流程。如果希望它直接更新知识库，还需要写入权限。只能上传附件的聊天工具可以在每次任务中读取你提供的相关笔记，更新由你自己保存。

## 定时任务、复用记录与 Skill

- 如果工具的定时功能可以读取所需资料并写到授权位置，就可以使用仓库里的定时任务提示词。也可以手动运行。
- 工具记录无法读取或格式不同时，先手工记录日期、任务、笔记路径和实际用途。周回顾结合这些记录和任务产出判断重复方法。包内的自动采集脚本识别选定 Codex 本地 JSONL 记录中能匹配正文的单文件 `cat` 读取。
- 支持 Skill 的工具可以用自己的方式接入这些步骤。也可以把相关步骤作为任务指令交给 Agent。安装或改用前，核对工具要求的包结构和指令格式。

## 已验证的插件安装方式

当前英文插件包已在 Codex 验证。建库和复用统计脚本需要 Python 3.11 或更新版本。

```sh
codex plugin marketplace add gilbertwuu/lifeos-knowledge@v0.1.1
codex plugin add lifeos-knowledge@lifeos-knowledge
```

安装后在 Codex 桌面端打开 **LifeOS Knowledge** 并新开对话。也可以[下载 ZIP](https://github.com/gilbertwuu/lifeos-knowledge/releases/download/v0.1.1/lifeos-knowledge-0.1.1.zip)，解压后把第一条命令里的 GitHub 地址替换成解压目录。

如果添加过 GitHub 上的 0.1.0 试用版，先运行 `codex plugin marketplace remove lifeos-knowledge`，再执行安装命令。知识库仍在原来选定的文件夹。
