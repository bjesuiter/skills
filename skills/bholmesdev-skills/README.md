# bholmesdev skills

[`jb-simplify`](jb-simplify/SKILL.md) comes from [bholmesdev/skills](https://github.com/bholmesdev/skills). The pinned revision is recorded in [vendor.json5](vendor.json5). The upstream MIT license is retained in [LICENSE](LICENSE).

The import includes only `skills/simplify`, renamed to `jb-simplify` through `upstreamNames` in the manifest. It has no sibling skill dependencies. Omit `alt-text`, `done`, `free-disk-space`, `taste-review`, and `transcribe` because this import selects only `simplify`. Revisit that selection only when explicitly requested.

## Local changes

- The rename keeps Claude Code's built-in `/simplify` available. A skill with the same name replaces it.
- `jb-simplify` narrows its trigger to a finished, checked code diff before commit or hand-off, and excludes pre-coding loads and docs, prose, or config-only changes. Its procedure now requires reading the diff and reporting each edit or "no change" with the reason. A skill-doctor run on 2026-11-22 found that agents read the skill before writing code in 59 of 71 sessions, and that 15 of 20 scored sessions claimed a simplify pass with no diff read or edit. It also adds Efficiency and Altitude sections, adapted from Claude Code's built-in `/simplify`, so Codex gets those checks too. Reapply these changes after each refresh.
