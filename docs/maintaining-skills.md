# Maintaining skills

## Repository layout

- [`skills/jb/`](../skills/jb/) contains JB's existing skills.
- `skills/<owner>-<repo>/` holds skills from one upstream repository.
- [`skills/in-progress/`](../skills/in-progress/) holds drafts. The CLI includes drafts in `--list` and `--all` unless their frontmatter sets `metadata.internal: true`.

### Upstream skills

Use [update-vendored](../.agents/skills/update-vendored/SKILL.md) to review or refresh an existing import. For a first import, see its [import reference](../.agents/skills/update-vendored/references/importing.md).

## Validate changes

From the repository root, run `bun run check:skills` and check that the expected skills are listed. When testing an actual installation, use a disposable project and one of the agents specified in [AGENTS.md](../AGENTS.md).

```bash
npx skills add /absolute/path/to/skills --skill jb-beans -a codex -y
```

## Releases and decisions

- [Record changes and cut a release](../.changeset/README.md).
- [Read the repository's decision records](adr/README.md).
