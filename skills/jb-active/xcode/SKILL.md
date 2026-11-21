---
name: xcode
description: Build, test, run, inspect, or scaffold Xcode projects, Swift packages, Apple simulators, devices, and macOS apps. Use for Xcode, xcodebuild, Swift build/test, Apple-platform builds, device deployment, or UI testing.
---

# Xcode

Prefer Apple's built-in Xcode MCP for project inspection, builds, tests, previews, running, and debugging. Use the installed server's live tool schema; capabilities differ by Xcode version. Apple command-line tools are the fallback when MCP is unavailable or lacks the requested operation.

## Connect without opening the desktop app

Use the attached Apple Xcode MCP when available. For a CLI client, its stdio command is `xcrun mcpbridge`. Codex registration:

```bash
codex mcp add xcode -- xcrun mcpbridge
```

Prefer headless operation when supported by the installed Xcode:

```bash
xcodebuild -version
xcrun mcp-server --help
xcrun mcp-server status --format json
```

If headless mode needs initial setup, `sudo xcrun mcp-server enable` enables it. Retain normal agent and folder permissions; resolve any pending request identified by `status` for the intended agent or project. Reuse an enabled server. An older Xcode without headless support may require the project open in the desktop app; report that requirement before opening UI on a restricted host.

If the MCP is not attached to the agent, an installed `mcporter` can access the same Apple server:

```bash
bunx mcporter list --stdio "xcrun mcpbridge" --schema
bunx mcporter call --stdio "xcrun mcpbridge" XcodeOpenWorkspace path="/absolute/path/App.xcodeproj"
```

Opening a workspace through the headless server does not require launching Xcode's desktop UI. Use the returned workspace identifier explicitly on subsequent calls. Discover schemes and destinations, then select the requested scheme and exact destination before building or running. Do not inherit an unrelated workspace's defaults.

## Execute and verify

- Build with `BuildProject`; inspect `GetBuildLog` on failure.
- Run focused tests with `RunSomeTests`, or the applicable test plan with `RunAllTests`. Verify tests actually executed and report failures or skips.
- Use `RunProject` for build and launch. For debugging, request `attachDebugger: true`, read `GetConsoleOutput`, and use `InvokeDebuggerCommand`. Check `process status` before commands requiring a stopped process.
- Use `RenderPreview` when a SwiftUI preview answers the requested visual question.
- Inspect the live schema for workspace, scheme, destination, scaffolding, and device-interaction tools instead of copying tool catalogs between Xcode versions.

## Device UI

Follow repository host restrictions for UI tests and automation, including macOS apps. Headless builds do not authorize launching or automating the app on a restricted host.

When T3 Code exposes `device_*` tools, use its Device panel for simulator/emulator discovery, streaming, and screenshots, and the returned `agent-device` command for interaction. Otherwise use Apple's device-interaction tools when present in the live schema. Inspect the current accessibility hierarchy or device state before acting, prefer identifiers and labels, and refresh after layout changes. End interaction sessions and log captures when finished.

## Command-line fallback

Discover the local environment and destinations:

```bash
xcodebuild -list -project /path/App.xcodeproj
xcrun devicectl list devices
xcrun simctl list devices available
```

Use `-workspace` instead of `-project` when appropriate. For a physical iPhone, build the requested scheme with its discovered UDID, existing signing configuration, and an explicit derived-data directory:

```bash
xcodebuild -project /path/App.xcodeproj -scheme App -configuration Debug \
  -destination 'id=<device-udid>' -derivedDataPath /tmp/app-device build
xcrun devicectl device install app --device <device-udid> '/tmp/app-device/Build/Products/Debug-iphoneos/App.app'
xcrun devicectl device process launch --device <device-udid> <bundle-id>
```

Use the actual built product path and bundle identifier. Permit provisioning updates when required by the authorized signing workflow. For simulators, use `xcrun simctl` to install and launch; for Swift packages, use `swift build` or `swift test --package-path /path/to/package`. Preserve build/test output and verify installation and launch separately. Report which checks actually ran.
