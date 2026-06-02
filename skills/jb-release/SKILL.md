---
name: jb-release
description: Use when the user asks to cut, prepare, publish, tag, or verify a release, especially npm/package releases.
private: true
allowed-tools: Bash(git:*), Bash(gh:*), Bash(npm:*), Bash(pnpm:*), Bash(yarn:*), Bash(bun:*)
skill_author: bjesuiter@gmail.com
---

# JB Release

Author: bjesuiter

## Purpose

Use this as the **generic release skill** when preparing a release, cutting a package release, updating a changelog, tagging a version, or publishing artifacts.

## Precedence

Repo-specific instructions win. Before acting, check for release guidance in:

- `AGENTS.md`, `CLAUDE.md`, `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`
- package manager scripts in `package.json`
- project-specific skills or docs, such as `docs/release*`, `.github/*`, or maintainer notes

If specific instructions exist, follow them instead of this generic workflow. Use this skill only to fill gaps.

## Generic release workflow

1. **Identify release type and target**
   - Confirm the package/app to release if the repo has multiple packages.
   - Determine version bump: `patch`, `minor`, `major`, prerelease, or exact version.
   - If the user did not specify the bump/version, ask before changing files.

2. **Inspect current release state**
   - Check clean/dirty git state with `git status --short`.
   - Find latest tag: `git tag --sort=-version:refname | head`.
   - Review commits since the last release tag: `git log <last-tag>..HEAD --oneline`.
   - Check package metadata and publish scripts.

3. **Update release files**
   - Update the version in `package.json` and lockfiles using the repo's package manager when possible.
   - Add a concise `CHANGELOG.md` entry based on commits since the last release tag.
   - Keep changelog entries user-facing and grouped when useful: Added, Changed, Fixed, Removed.

4. **Verify**
   - Run the repo's normal checks before tagging:
     - lint
     - tests
     - build/typecheck
   - Prefer existing package scripts over inventing new commands.
   - If a check cannot be run, record why.

5. **Commit, tag, and push**
   - Commit release changes with a clear message, e.g. `chore: release v1.2.3`.
   - Tag the release commit with the version prefixed by `v`, e.g. `v1.2.3`.
   - Push code and tags.

6. **Publish only when requested or documented**
   - Do not publish to npm, app stores, or other registries unless the user explicitly asks or repo instructions require it.
   - If publishing, use the documented release script/CLI and verify the published version afterward.

## Guardrails

- Never create a branch unless the user asks.
- Do not overwrite project-specific release automation.
- Do not skip failing checks silently; stop and report the failure.
- Do not tag before release files are committed and checks have passed, unless repo-specific instructions say otherwise.
- Avoid changing unrelated files during a release.

## Deliverable

End with a short summary containing:

- released version
- changelog entry added/updated
- checks run and results
- commit hash and tag
- whether anything was published
