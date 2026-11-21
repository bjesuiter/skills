# Cursor pstack

[`unslop`](unslop/SKILL.md) comes from [pstack in cursor/plugins](https://github.com/cursor/plugins/tree/main/pstack). The pinned revision is recorded in [vendor.json5](vendor.json5). The upstream MIT license is retained in [LICENSE](LICENSE).

The import includes only `pstack/skills/unslop`. It has no sibling skill dependencies. The remaining pstack skills and plugin files are outside the scope of this import.

## Local changes

- `unslop` adds rule 34: explain a new term or internal component in plain words the first time it appears. A skill-doctor run on 2026-11-21 found that users asked what an agent meant in 5 of 7 sessions. Reapply this rule after each refresh.
