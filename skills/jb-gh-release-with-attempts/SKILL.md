---
name: jb-gh-release-with-attempts
description: "Use when setting up or running GitHub Actions releases with disposable release-attempt tags: release-attempt/patch|minor|major/from-VERSION/TIMESTAMP. Encodes JB's preference for explicit CLI-triggered release intent, matrix build verification before canonical v* tags, GitHub Release assets, and optional npm publish only after successful builds."
private: true
allowed-tools: Bash(git:*), Bash(gh:*), Bash(npm:*), Bash(pnpm:*), Bash(yarn:*), Bash(bun:*), Bash(deno:*)
skill_author: bjesuiter@gmail.com
---

# JB GitHub Release With Attempts

Author: bjesuiter

## Purpose

Use this skill to design, implement, or run a GitHub Actions release pipeline that starts from **non-semantic release-attempt tags** instead of canonical version tags.

JB's preference: releases should be explicit and easy to trigger from the CLI, but failed native/package builds must not leave broken `v*` tags or consumed semantic versions.

## Core model

Do **not** trigger release builds from canonical tags like `v0.8.2`.

Trigger from disposable intent tags:

```text
release-attempt/patch/from-0.8.1/20260620T093000Z
release-attempt/minor/from-0.8.1/20260620T093000Z
release-attempt/major/from-0.8.1/20260620T093000Z
```

The attempt tag points at the current `main` commit. If the pipeline succeeds, it creates a release commit and the canonical `vNEXT` tag only at the end:

```text
A --- B --- C  main
          \
           release-attempt/patch/from-0.8.1/...

# after success
A --- B --- C --- D  main
                    \
                     v0.8.2
```

`D` contains release file updates such as `package.json`, lockfile, and optionally `CHANGELOG.md`.

## When to use

Use this when the user wants to:

- set up GitHub Actions release automation
- release from local CLI without opening GitHub UI
- avoid broken semantic version tags after failed builds
- build matrix/native assets before creating a real release tag
- publish GitHub Release assets and optionally npm packages
- convert an existing local/manual release flow into CI-backed release attempts

If the task is only a fully local release, use `jb-local-release` instead.

## Repository preflight

Before editing, read repo-specific release docs and workflows:

- `AGENTS.md`, `CLAUDE.md`, `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`
- existing `.github/workflows/*release*`, `.github/workflows/*build*`, `.github/workflows/*prebuild*`
- package manager scripts in `package.json`
- existing release/publish scripts such as `scripts/publish.*`, `scripts/release.*`
- repo-local skills such as `.pi/skills/release/SKILL.md`

Repo-specific instructions win.

## Workflow shape

Create `.github/workflows/release.yml` or adapt the repo's release workflow with this trigger:

```yaml
on:
  push:
    tags:
      - "release-attempt/patch/from-*/*"
      - "release-attempt/minor/from-*/*"
      - "release-attempt/major/from-*/*"
```

The workflow should:

1. Parse `bump` from `GITHUB_REF_NAME`.
2. Parse optional expected current version from the `from-<version>` segment.
3. Checkout the commit pointed to by the attempt tag.
4. Fetch full history and tags.
5. Read current version from the package manifest or project-specific version source.
6. Fail early if `from-<version>` is present and does not match the current version.
7. Compute `NEXT` from `patch | minor | major`.
8. Assert canonical tag `vNEXT` does not already exist.
9. Update version files (`package.json`, lockfile, platform manifests) and optionally changelog.
10. Run all checks and matrix builds.
11. Package release assets and checksums.
12. Only after all required jobs succeed:
    - create release commit `chore(release): vNEXT`
    - push release commit to `main`
    - create canonical tag `vNEXT` on that release commit
    - create GitHub Release
    - upload assets/checksums
    - publish npm/package registry artifact only if requested or documented

If any required check/build/package step fails, the workflow must not create `vNEXT` or a GitHub Release.

## GitHub permissions

Set only the permissions needed by the workflow. A typical release workflow needs:

```yaml
permissions:
  contents: write
  actions: read
  id-token: write # only when publishing npm with provenance or similar OIDC flows
```

Use `GITHUB_TOKEN` for commits, tags, and GitHub Releases unless the repo's branch protection requires a PAT or GitHub App token.

## Release attempt helper script

Prefer adding a small CLI script so JB can trigger releases locally:

```fish
npm run release:attempt -- patch
npm run release:attempt -- minor
npm run release:attempt -- major
```

The helper should:

1. Require a clean working tree.
2. Require current branch to be `main` unless repo instructions allow otherwise.
3. Pull/fetch latest `main` and tags.
4. Read current version.
5. Build tag name: `release-attempt/<bump>/from-<current-version>/<UTC timestamp>`.
6. Create an annotated or lightweight tag at `HEAD`.
7. Push the tag.
8. Print the GitHub Actions URL and the expected next version.

Example shell equivalent:

```fish
set bump patch
set version (node -p "require('./package.json').version")
set ts (date -u +%Y%m%dT%H%M%SZ)
set tag release-attempt/$bump/from-$version/$ts
git tag $tag
git push origin $tag
gh run list --workflow release.yml --limit 5
```

Validate bump input strictly: only `patch`, `minor`, and `major` unless the user explicitly asks for prerelease support.

## Version and changelog policy

Prefer explicit release intent over commit-message-derived versioning. Do not default to `semantic-release` unless the user asks.

For changelogs, choose one based on repo preference:

- existing manual `CHANGELOG.md` format
- generated notes from commits since last canonical `v*` tag
- no changelog update if the repo does not maintain one

If ambiguous, ask whether changelog updates should be automatic and what source to use.

## Matrix/native assets

For native/prebuild repos, package assets after successful matrix builds. Common names:

```text
<package>-darwin-arm64.tar.gz
<package>-linux-x64.tar.gz
<package>-linux-arm64.tar.gz
<package>-win32-x64.zip
checksums.txt
```

Use artifact upload/download between matrix and finalize jobs. The finalize job must depend on all required matrix jobs.

## NPM/package publishing

Publishing is optional and must happen only after successful build verification.

- Do not publish unless the user explicitly asks or repo docs require it.
- If publishing npm, prefer `npm publish --provenance` when the package supports it.
- Use `npm_tag` only when needed (`latest`, `next`, etc.).
- Verify the published version after publish.

## Attempt tag cleanup

Default: keep failed `release-attempt/*` tags for debugging/audit unless the user requests cleanup.

For successful attempts, ask or follow repo policy:

- keep as audit trail, or
- delete after the canonical `vNEXT` release is created

Never delete attempt tags silently.

## Manual fallback

If the repo strongly prefers GitHub UI triggering, use `workflow_dispatch` with static inputs:

```yaml
workflow_dispatch:
  inputs:
    bump:
      type: choice
      options: [patch, minor, major]
    mode:
      type: choice
      options: [dry-run, release]
    expected_current_version:
      required: false
    npm_tag:
      type: choice
      options: [latest, next]
```

But note: JB generally prefers CLI-pushed `release-attempt/*` tags because GitHub cannot dynamically show the computed future version in the dispatch form before a run starts.

## Verification checklist

Before finishing implementation:

- `release-attempt/*` trigger patterns match the actual tag format.
- Helper script creates tags in exactly that format.
- Workflow checks expected current version before doing expensive work.
- Workflow fails if `vNEXT` already exists.
- Canonical `vNEXT` tag is created only in the final success path.
- Release commit is pushed before canonical tag creation.
- Matrix/finalize dependencies prevent partial releases.
- Assets and checksums are attached to the GitHub Release.
- Publishing is gated and documented.
- Local docs explain how to start a release attempt and where to inspect the run.

## Deliverable

End with:

- files changed
- how to trigger a patch/minor/major attempt
- what the workflow creates on success
- what remains after failure
- checks run and results
