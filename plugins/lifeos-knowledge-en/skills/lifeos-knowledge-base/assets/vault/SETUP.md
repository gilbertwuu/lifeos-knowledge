# Connect your knowledge base to Codex

The vault's `AGENTS.md` guides chats started in that folder. To make Codex consult the vault from another project, append the rule below to the instruction file active in that project.

- **All projects.** Add it to the global Codex file, normally `~/.codex/AGENTS.md`. If you use a custom Codex home, use that directory.
- **One project.** Add it to `AGENTS.md` in that project's root.
- If an `AGENTS.override.md` is active at the chosen location, append the rule there. Keep existing instructions. If there is no instruction file, create `AGENTS.md`.

Replace the placeholder with your vault's absolute path.

```markdown
## My knowledge base

My knowledge base is at `<absolute path to my vault>`.
Before starting a task, consider whether the vault can provide relevant context, methods, or experience. When it can, check INDEX.md first and read the relevant note bodies. Apply what fits the task and briefly say which note helped and how. Continue if nothing applies.
When I ask to save or capture knowledge, read the vault's AGENTS.md and MEMORY.md, then check INDEX.md and follow the capture workflow.
If a relevant lookup is blocked by a missing path or permission, explain the specific gap.
```

## Test the connection

Start a fresh Codex chat from the project. Give Codex a normal task related to one of your saved notes. For a note about evidence and assumptions, try “What conclusions does this feedback support?” Check that Codex reads the index and note, then applies the method in its answer. If no lookup happens, ask which instruction file is active and which vault path it found.

## Open the same folder in Obsidian

Select **Open folder as vault**, choose the vault root, and open [Separate observations from explanations](examples/Separate-observations-from-explanations.md). Use internal links and Obsidian's Backlinks panel to inspect note relationships. Attachments can be placed in an `attachments/` folder beside a note and embedded using a relative Markdown path, such as `![Explanation](attachments/example.png)`.

[Codex AGENTS.md documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md) · [Obsidian vault documentation](https://obsidian.md/help/vault)
