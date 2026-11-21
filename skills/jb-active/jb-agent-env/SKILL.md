---
name: jb-agent-env
description: Manage JB's preferred agent environment from the shared Gist registry, including Markdown skills, Pi extensions, CLIs, and MCP servers. Use when adding, tagging, installing, updating, removing, or inspecting those resources, or when JB says "update from skill registry".
private: true
skill_author: bjesuiter@gmail.com
---

# JB Agent Environment

The Gist setup document holds every workflow for this registry: installing, updating, validating, and editing entries. This skill only finds it. Do not keep a second copy of those rules here.

## Canonical resources

- Gist: `https://gist.github.com/bjesuiter/98d5768dc360093affb8d8fdb064e45f`
- Registry: `jb-skill-preferences.json5`
- Setup document: `jb-skill-preferences-setup.md`
- Gist description: `JB shared preferred AI skill registry`

## Steps

1. Read the setup document:

   ```bash
   gh gist view https://gist.github.com/bjesuiter/98d5768dc360093affb8d8fdb064e45f \
     --filename jb-skill-preferences-setup.md \
     --raw
   ```

2. Follow the section that matches the request:
   - Install or update the machine: ensure mode, or the selection JB names.
   - Install one entry JB just added: the new-entry workflow.
   - Add, change, tag, or remove an entry: updating the registry.
   - Check what is installed or available: validate availability and local state.
3. If the pinned Gist cannot be read, find it by filename or description:

   ```bash
   gh gist list --limit 100 --filter 'jb-skill-preferences\.json5|JB shared preferred AI skill registry'
   ```
