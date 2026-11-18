# Changesets

Install the release tooling with `bun install --frozen-lockfile`.

## Record a change

Run `bun run changeset` and commit the generated Markdown with the change. Describe the affected skills and any migration steps. Use patch for compatible fixes, minor for additions and compatible workflow changes, and major for removals or breaking changes to released skills.

For a non-interactive change record:

```sh
bun run changeset --patch jb-skills -m "Describe the change for skill users."
```

## Cut a release

1. Start from a clean checkout of `main` containing the changes to release.
2. Run `bun run release:version` to consume pending Changesets and update `package.json` and `CHANGELOG.md`. Run `bun install` to reconcile the lockfile.
3. Run `bun run check:skills` and review the diff and skill list.
4. Commit the version, changelog, lockfile if changed, and consumed Changesets. Run `bun run changeset git-tag` on the release commit. For this single-package repo, the tag has the form `v0.1.0`.
5. To make the release available remotely, push the release commit and its specific tag. A GitHub Release using the generated notes is optional. The private package serves as the version marker for Git releases.

## Install a fixed snapshot

Use a dedicated checkout so a release install cannot change the working branch of the skills repo. Replace `v0.1.0` with the release tag assigned to the implementer.

```sh
git clone --branch v0.1.0 --depth 1 https://github.com/bjesuiter/skills.git jb-skills-v0.1.0
cd /path/to/target-project
bunx skills add /absolute/path/to/jb-skills-v0.1.0 --skill jb-beans -a codex -y --copy
```
