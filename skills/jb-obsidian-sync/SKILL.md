---
name: "jb-obsidian-sync"
description: "Use `ob` to connect, sync, inspect, create, and edit Obsidian Sync vaults headlessly as Markdown."
---

# JB Obsidian Sync

Manage Obsidian vaults as synchronized Markdown repositories inside the agent workspace.

## Verified CLI

Use the headless Obsidian client `ob` from the `obsidian-headless` package.

```bash
command -v ob
ob --version
ob --help
```

The verified installation is `/home/igris/.bun/bin/ob`; its resolved package entrypoint is `obsidian-headless/cli.js`. Recheck `command -v ob`, the version, and relevant `--help` output before relying on syntax after upgrades.

Do not use an Obsidian CLI whose purpose is merely to remote-control Obsidian Desktop. Obsidian Desktop is not required.

## Operating model

- Use `ob` to connect and synchronize Obsidian Sync vaults into the workspace.
- After a vault is available locally, work directly on its Markdown files with normal filesystem tools.
- Treat `ob sync` as bidirectional by default.
- Do not assume a fixed vault path.
- Do not confuse an Obsidian Sync checkout with an ordinary Git repository unless the local checkout actually uses Git.
- Never put account passwords, MFA codes, vault passwords, recovery keys, encryption keys, or tokens in command arguments, logs, notes, tracked files, or chat.

## Inspect account and vaults

These commands are read-only:

```bash
ob login
ob sync-list-remote
ob sync-list-local
```

With no credentials passed, `ob login` shows the current login status or prompts interactively. Never pass `--password` or `--mfa` on the command line. If authentication is required, run `ob login` interactively so secrets are prompted.

Use `ob sync-list-remote` to resolve a remote vault by ID or unique name. Prefer the immutable vault ID when names are duplicated or when recording durable configuration.

Use `ob sync-list-local` to find already configured local checkouts and their paths before searching the filesystem.

## Resolve a local vault checkout

Use this order:

1. An absolute workspace path explicitly supplied by JB for the current task.
2. A matching entry from `ob sync-list-local`.
3. A vault checkout path recorded in `TOOLS.md`.
4. A bounded search inside the workspace for directories containing the configured Obsidian config directory, normally `.obsidian`.

Verify that the directory exists. For an already configured checkout, confirm it with:

```bash
ob sync-status --path "$VAULT_PATH"
```

- If exactly one matching vault exists, use it.
- If multiple vaults exist and the intended one is unclear, ask JB which vault to use.
- If none exists, report that no local checkout is connected. Do not invent a path.

`ob sync-status` reports the stored sync configuration; it is not a substitute for running `ob sync`.

## Connect a remote vault

When JB asks to clone, connect, or set up a remote vault:

1. Confirm authentication with `ob login`.
2. List remote vaults with `ob sync-list-remote`.
3. Choose a clear vault-specific directory under the workspace and create it only when the requested setup requires it.
4. Connect it interactively:

```bash
ob sync-setup \
  --vault "$REMOTE_VAULT_ID" \
  --path "$VAULT_PATH" \
  --device-name "Igris bj01-srv02"
```

5. Omit `--password`; allow `ob` to prompt for the E2E vault password.
6. Verify configuration with `ob sync-status --path "$VAULT_PATH"`.
7. Run the initial one-time synchronization:

```bash
ob sync --path "$VAULT_PATH"
```

8. Verify the checkout contents and record the stable path in `TOOLS.md` when it will be reused.

Use `--config-dir <name>` only when the vault deliberately uses a non-default Obsidian configuration directory.

## Safe editing and synchronization workflow

For every task that changes a synced vault:

1. Resolve the checkout and inspect its configuration:

```bash
ob sync-status --path "$VAULT_PATH"
```

2. Pull and reconcile current remote changes with a one-time bidirectional sync before editing:

```bash
ob sync --path "$VAULT_PATH"
```

3. Inspect the target notes, then make the requested Markdown changes.
4. Review the local files changed during the task. Do not alter unrelated notes or `.obsidian/` configuration.
5. Run another one-time bidirectional sync:

```bash
ob sync --path "$VAULT_PATH"
```

6. Run `ob sync-status --path "$VAULT_PATH"` again and inspect command output for failures or conflicts.
7. Report the vault path, changed notes, and whether the final sync succeeded.

Do not start `ob sync --continuous` for ordinary edits. Use continuous mode only when JB explicitly requests a long-running watcher; manage it as a background process and report how it can be stopped.

## Sync configuration

Inspect the current configuration without changing it:

```bash
ob sync-config --path "$VAULT_PATH"
```

Supported settings include:

- `--mode bidirectional|pull-only|mirror-remote`
- `--conflict-strategy merge|conflict`
- `--excluded-folders <comma-separated-folders>`
- `--file-types image,audio,video,pdf,unsupported`
- `--configs app,appearance,appearance-data,hotkey,core-plugin,core-plugin-data,community-plugin,community-plugin-data`
- `--device-name <name>`
- `--config-dir <name>`

Never switch to `mirror-remote`: it reverts local changes. Use it only with JB's explicit approval after showing the impact. Do not change sync mode, conflict strategy, exclusions, file types, or configuration categories merely to complete a note edit.

`ob sync-unlink --path "$VAULT_PATH"` removes the stored sync configuration and credentials. Treat unlinking as destructive and run it only when JB explicitly asks after confirming the exact path.

## Create a new remote vault

Create a remote vault only when JB explicitly asks.

1. Confirm authentication.
2. Determine the valid region identifier before creation. The CLI validates `--region`; do not guess the identifier.
3. Require end-to-end encryption and interactive password entry:

```bash
ob sync-create-remote \
  --name "$VAULT_NAME" \
  --encryption e2ee \
  --region "$REGION"
```

4. Omit `--password` so `ob` prompts securely.
5. Prefer Germany, specifically Frankfurt, when available; otherwise another German region, then an EU region.
6. If E2EE cannot be enabled, stop instead of creating the vault.
7. If the requested residency is unavailable, explain the available locations before choosing a materially different region.
8. After creation, connect it with `ob sync-setup` and verify with a one-time `ob sync`.

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

1. Complete the pre-edit sync workflow.
2. Search for an existing note with the same or overlapping purpose.
3. Follow the vault's existing naming, frontmatter, and organization patterns.
4. Use a Title Case filename when no stronger local convention exists.
5. Write the note as a coherent unit of learning.
6. Add relevant `[[wikilinks]]` and update an existing index note when appropriate.
7. Preserve unrelated content in existing notes.
8. Complete the post-edit sync and verification workflow.

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
- Stop on authentication, encryption, locking, synchronization, or conflict errors.
- Never resolve a conflict by discarding local or remote changes blindly.
- Never run more than one `ob sync` instance for the same vault; the CLI locks each checkout.
