# Maintaining skills

## Repository layout

- [`skills/jb/`](../skills/jb/) contains JB's existing skills.
- `skills/<owner>-<repo>/` holds skills from one upstream repository.
- [`skills/in-progress/`](../skills/in-progress/) holds drafts. The CLI includes drafts in `--list` and `--all` unless their frontmatter sets `metadata.internal: true`.

### Upstream skills

Each upstream folder has a `vendor.json5` with the GitHub repository, its HTTPS URL, and the revision to track. See [the tstack manifest](../skills/t3dotgg-tstack/vendor.json5).

Keep the selection and reasons for omissions in the upstream folder's `README.md`. Check that file before choosing what to export for an update.

- Fetch the pinned revision into a temporary Git repository. Use `git archive` to export the selected skill directories and upstream license and notices. Copy whole skill directories so bundled files and executable modes carry over.
- Inspect cross-skill references before selecting directories. Include required sibling skills and document them in the catalog when a user might install skills individually.
- Use `track: { type: "commit", branch: "main" }` to check a branch tip, or `track: { type: "release" }` to check the latest GitHub release using `gh`.
- Set `snapshot` to `null` until the first import. After importing, record `snapshot: { revision: "...", vendoredAt: "YYYY-MM-DD" }` with the full commit SHA or exact release tag that was imported.
- Use one snapshot per upstream folder. When refreshing a folder, bring all its imported skills to the recorded revision and reapply local changes.

Run `bun scripts/vendor-updates.ts` to compare each snapshot with its upstream. The check reports differing revisions for review.

## Validate changes

From the repository root, run `bun run check:skills` and check that the expected skills are listed. When testing an actual installation, use a disposable project and one of the agents specified in [AGENTS.md](../AGENTS.md).

```bash
npx skills add /absolute/path/to/skills --skill jb-beans -a codex -y
```

## Releases and decisions

- [Record changes and cut a release](../.changeset/README.md).
- [Read the repository's decision records](adr/README.md).
