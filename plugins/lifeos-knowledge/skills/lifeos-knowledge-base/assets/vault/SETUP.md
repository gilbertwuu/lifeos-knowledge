# Connect your knowledge base to your Agent

Add the rule below to the instruction file or persistent project settings your Agent reads. Use global instructions to apply the rule across projects or project instructions for one project. If your tool reads `AGENTS.md`, the vault's own file guides work started in that folder. Follow your tool's instruction discovery rules for work started elsewhere. Keep existing instructions.

Give the Agent read access to the vault and write access for saves you want it to perform. If it can only read uploaded files, attach the relevant notes for each task and save returned changes locally.

Replace the placeholder with your vault's absolute path.

```markdown
## My knowledge base

My knowledge base is at `<absolute path to my vault>`.
Before starting a task, consider whether the vault can provide relevant context, methods, or experience. When it can, check INDEX.md first and read the relevant note bodies. Apply what fits the task and briefly say which note helped and how. Continue if nothing applies.
When I ask to save or capture knowledge, read the vault's AGENTS.md and MEMORY.md, then check INDEX.md and follow the capture workflow.
If a relevant lookup is blocked by a missing path or permission, explain the specific gap.
```

## Test the connection

Start a fresh chat from the project. Give Codex a normal task related to one of your saved notes. For a note about evidence and assumptions, try “What conclusions does this feedback support?” Check that the Agent reads the index and note, then applies the method in its answer. If no lookup happens, ask which instruction file is active and which vault path it found.

## Open the same folder in Obsidian

Select **Open folder as vault**, choose the vault root, and open [Separate observations from explanations](examples/Separate-observations-from-explanations.md). Use internal links and Obsidian's Backlinks panel to inspect note relationships. Attachments can be placed in an `attachments/` folder beside a note and embedded using a relative Markdown path, such as `![Explanation](attachments/example.png)`.

[Obsidian vault documentation](https://obsidian.md/help/vault)
