---
name: "obsidian-vault"
description: "Manage JB's Obsidian vault using verified paths, Title Case notes, wikilinks, and index notes."
---

# Obsidian Vault

> Forked from `mattpocock/skills` (`skills/personal/obsidian-vault`). This JB-owned fork replaces the upstream author's machine-specific vault path with verified, portable path resolution.

## Resolve the vault path

Never assume a fixed vault path.

Use this order:

1. An absolute vault path explicitly supplied by JB for the current task.
2. A non-empty `OBSIDIAN_VAULT_PATH` environment variable.
3. An environment-specific Obsidian vault path recorded in `TOOLS.md`.
4. A bounded filesystem search of likely user or mounted-data roots for directories containing `.obsidian`.

Before reading or writing, verify that the resolved directory exists and contains `.obsidian`.

- If exactly one vault is found, use it.
- If multiple vaults are found and the intended vault is unclear, ask JB which one to use.
- If none is found, report that no vault is connected. Do not create a vault or invent a path unless JB explicitly asks.
- Obsidian does not need to be running for direct Markdown file operations.

## Organization

Prefer the existing vault's conventions when they are discoverable. Otherwise use these defaults:

- Keep notes mostly flat at the vault root.
- Use **Title Case** for note filenames.
- Use index notes to aggregate related topics, for example `Skills Index.md` or `RAG Index.md`.
- Avoid creating new folders merely for categorization; prefer links and index notes.

## Linking

- Use Obsidian `[[wikilinks]]`.
- Add links to dependencies and closely related notes near the bottom of a note.
- Index notes should be simple, readable lists of `[[wikilinks]]`.

## Search notes

Search filenames first, then content. Prefer `rg`/`rg --files`; fall back to `find` and `grep` if unavailable.

Examples, with `$OBSIDIAN_VAULT_PATH` already verified:

```bash
rg --files "$OBSIDIAN_VAULT_PATH" -g '*.md' | rg -i 'keyword'
rg -il 'keyword' "$OBSIDIAN_VAULT_PATH" -g '*.md'
```

## Create or update a note

1. Resolve and verify the vault path.
2. Search for an existing note with the same or overlapping purpose.
3. Follow the vault's existing naming and organization patterns.
4. Use a Title Case filename when no stronger local convention exists.
5. Write the note as a coherent unit of learning.
6. Add relevant `[[wikilinks]]` and update an existing index note when appropriate.
7. Preserve unrelated content in existing notes.

## Find backlinks

Search for the exact wikilink:

```bash
rg -l '\[\[Note Title\]\]' "$OBSIDIAN_VAULT_PATH" -g '*.md'
```

## Find index notes

```bash
rg --files "$OBSIDIAN_VAULT_PATH" -g '*Index*.md'
```

## Safety

- Never overwrite an existing note blindly.
- Never create or initialize a new vault without explicit instruction.
- Do not require the Obsidian GUI or CLI when direct Markdown operations are sufficient.
- Treat `.obsidian/` as application configuration; do not edit it unless JB explicitly asks for an Obsidian configuration change.
