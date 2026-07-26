---
name: "jb-obsidian-sync"
description: "Manage Obsidian Sync vault checkouts as Markdown repos without Obsidian Desktop."
---

# JB Obsidian Sync

Manage Obsidian vaults as synchronized Markdown repositories inside the agent workspace.

## Operating model

- Use the Obsidian Sync CLI to clone or synchronize vault repositories into the workspace.
- After a vault is available locally, work directly on its Markdown files with normal filesystem tools.
- Do not require Obsidian Desktop.
- Do not use an Obsidian CLI whose purpose is merely to remote-control Obsidian Desktop.
- Do not assume a fixed vault path.
- Do not confuse an Obsidian Sync repository with an ordinary Git repository unless the local checkout actually uses Git.

## Resolve a vault checkout

Use this order:

1. An absolute workspace path explicitly supplied by JB for the current task.
2. A vault checkout path recorded in `TOOLS.md`.
3. A bounded search inside the workspace for directories containing `.obsidian`.

Before reading or writing, verify that the directory exists and contains `.obsidian`.

- If exactly one matching vault exists, use it.
- If multiple vaults exist and the intended one is unclear, ask JB which vault to use.
- If none exists, report that no vault checkout is connected. Do not invent a path.

## Connect or synchronize a vault

When JB asks to connect, clone, pull, push, or synchronize a vault:

1. Identify the installed Obsidian Sync CLI executable and inspect its local help before constructing commands; do not guess its syntax.
2. Use that CLI directly, without starting Obsidian Desktop.
3. Keep the checkout under the workspace at a clear, vault-specific path.
4. Verify the resulting directory exists and contains `.obsidian` before editing notes.
5. Record a stable checkout path in `TOOLS.md` when it will be reused.
6. After edits, use the same Sync CLI when an explicit synchronization step is required by that tool or the requested workflow.

Never expose credentials, recovery keys, encryption keys, or tokens in commands, logs, notes, or chat output.

## Create a new vault

Create or initialize a new vault only when JB explicitly asks.

- Require end-to-end encryption.
- Prefer data residency in Germany, specifically Frankfurt, when the provider offers that choice.
- If Frankfurt is unavailable, prefer another German region, then an EU region.
- If end-to-end encryption cannot be enabled, stop and ask JB instead of creating the vault.
- If the requested residency is unavailable, explain the available locations before choosing a materially different region.
- Store or transmit encryption secrets only through the secure mechanism supported by the Sync CLI; never place them in Markdown, tracked files, shell history, or chat.

## Preserve Obsidian formatting

Prefer the vault's existing conventions when discoverable. Otherwise:

- Keep notes mostly flat at the vault root.
- Use **Title Case** for note filenames.
- Use index notes to aggregate related topics, for example `Skills Index.md` or `RAG Index.md`.
- Avoid new folders used only for categorization; prefer links and index notes.
- Use Obsidian `[[wikilinks]]`.
- Add links to dependencies and closely related notes near the bottom of a note.
- Keep index notes as simple, readable lists of `[[wikilinks]]`.
- Preserve existing YAML frontmatter, callouts, embeds, block references, tags, and other Obsidian syntax unless the task requires changing them.

## Search notes

Search filenames first, then content. Prefer `rg` and `rg --files`; fall back to `find` and `grep` if unavailable.

```bash
rg --files "$VAULT_PATH" -g '*.md' | rg -i 'keyword'
rg -il 'keyword' "$VAULT_PATH" -g '*.md'
```

## Create or update a note

1. Resolve and verify the local vault checkout.
2. Search for an existing note with the same or overlapping purpose.
3. Follow the vault's existing naming, frontmatter, and organization patterns.
4. Use a Title Case filename when no stronger local convention exists.
5. Write the note as a coherent unit of learning.
6. Add relevant `[[wikilinks]]` and update an existing index note when appropriate.
7. Preserve unrelated content in existing notes.
8. Synchronize through the Obsidian Sync CLI when the workflow requires it.

## Find backlinks

```bash
rg -l '\[\[Note Title\]\]' "$VAULT_PATH" -g '*.md'
```

## Find index notes

```bash
rg --files "$VAULT_PATH" -g '*Index*.md'
```

## Safety

- Never overwrite an existing note blindly.
- Never create or initialize a vault without explicit instruction.
- Treat `.obsidian/` as application configuration; do not edit it unless JB explicitly asks for an Obsidian configuration change.
- Keep edits scoped to the selected vault checkout.
- Inspect synchronization status before resolving conflicts; never discard remote or local changes blindly.
