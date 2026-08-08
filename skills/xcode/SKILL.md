---
name: xcode
description: Build, test, run, inspect, or scaffold Xcode projects, Swift packages, Apple simulators, devices, and macOS apps through XcodeBuildMCP. Use when the user mentions Xcode, xcodebuild, Swift build/test, Apple-platform builds, simulators, devices, or UI testing.
---

# XcodeBuildMCP

Use XcodeBuildMCP through `mcporter` for Xcode and Swift work:

```bash
bunx mcporter call --stdio "xcodebuildmcp" <tool_name> [args...]
```

Assume `mcporter` and `xcodebuildmcp` are installed globally. Here `bunx` runs installed binaries; it must not fetch untrusted replacements.

## Discover the environment

Identify the target before building:

```bash
bunx mcporter call --stdio "xcodebuildmcp" doctor
bunx mcporter call --stdio "xcodebuildmcp" discover_projs workspaceRoot="$(pwd)"
bunx mcporter call --stdio "xcodebuildmcp" list_schemes
bunx mcporter call --stdio "xcodebuildmcp" list_sims
```

For physical-device work, discover connected devices instead of assuming an identifier. Distinguish among an Xcode project, workspace, Swift package, simulator target, physical device, and macOS app; choose tools for that target family.

## Set session defaults

Set project/workspace, scheme, and destination defaults before most build and test calls:

```bash
bunx mcporter call --stdio "xcodebuildmcp" session-set-defaults \
  projectPath="/path/to/App.xcodeproj" \
  scheme="App" \
  simulatorName="<discovered simulator>"
```

For a workspace, use `workspacePath`; for an exact simulator or device, use its discovered identifier. Inspect defaults when behavior is surprising:

```bash
bunx mcporter call --stdio "xcodebuildmcp" session-show-defaults
```

Do not reuse stale defaults across unrelated repositories or targets.

## Execute the requested workflow

After setting the target:

1. Select the matching simulator, device, macOS, or Swift-package tools.
2. Build before attempting installation or launch unless a combined build-and-run tool applies.
3. Run focused tests first, then broader tests when warranted.
4. Preserve build output and surface actionable compiler/test failures.
5. Use log-capture tools around reproductions when runtime evidence is needed, and stop the capture afterward.

For scaffolding, confirm the destination, project name, platform, and bundle identifier. Do not overwrite an existing project implicitly.

## Simulator UI interaction

Build and launch the app, then inspect the current accessibility hierarchy before every interaction sequence:

```bash
bunx mcporter call --stdio "xcodebuildmcp" describe_ui
```

Prefer accessibility identifiers or labels. Use coordinates only from the latest hierarchy, never guessed from a screenshot or reused after the UI changes. Take screenshots when visual proof is material. Re-run `describe_ui` after navigation, dialogs, rotation, or other layout changes.

## Use the live tool schema

Tool names and arguments can change with XcodeBuildMCP versions. Do not rely on a copied catalog. Inspect the installed `mcporter` help and XcodeBuildMCP schema before using an unfamiliar operation:

```bash
bunx mcporter --help
bunx mcporter list --stdio "xcodebuildmcp" --schema
```

Use the live schema for gestures, simulator settings, recording, logs, device operations, Swift packages, scaffolding, and utilities.

## Diagnose failures

- Missing project/workspace: inspect and set session defaults.
- Unknown simulator/device: rediscover available destinations.
- Environment or integration failure: run `doctor` and inspect the exact error.
- Incremental-build issue: try the server's standard-xcodebuild preference only when supported by the live schema.
- Build or test failure: diagnose the emitted compiler/test evidence rather than treating it as an MCP failure.
