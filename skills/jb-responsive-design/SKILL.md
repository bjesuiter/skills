---
name: jb-responsive-design
description: Audit and fix responsive web UI across mobile and desktop with parallel browser evidence, GitHub issues, reviewed PRs, and an integration branch.
skill_author: bjesuiter@gmail.com
---

# JB responsive design

Audit and repair responsive web interfaces with reproducible browser evidence, issue-scoped fixes, and a reviewed integration branch.

## 1. Establish the target

1. Resolve the repository, app start command, test URL, default branch, and requested viewport range from local files and repository metadata.
2. Inspect existing scripts, contribution instructions, dirty worktrees, responsive-design issues, related pull requests, remote branches, prior evidence, and available browser tooling.
3. Reconcile prior work before creating artifacts. Map each verified issue, fix commit, and merged or open PR to the requested scope. Reuse completed work, continue incomplete work, and avoid duplicate issues or PRs.
4. Create a dedicated integration branch from the requested base or latest verified prior integration commit. Keep audit artifacts outside tracked source unless the repository explicitly owns them.

Complete when the base commit, integration branch, runnable URL, viewport matrix, and disposition of related prior work are recorded.

## 2. Build the viewport matrix

Choose a small matrix that covers:

- narrow mobile;
- wide mobile;
- tablet or compact laptop;
- common desktop;
- wide desktop.

Add issue-specific boundary widths when a layout changes near a breakpoint. Use separate named browser sessions so tests cannot share viewport or navigation state.

Complete when every requested device class has an exact width and height.

## 3. Audit in parallel

Use the installed `agent-browser` CLI and load its current core and dogfood instructions before commands. Start the app once, then assign independent viewport groups to parallel subagents when the user requests parallel testing.

For each viewport:

1. Open a fresh session and set the exact viewport.
2. Exercise the primary user path, not only the landing page.
3. Inspect vertical and horizontal scrolling, sticky or fixed elements, overflow, clipped controls, text wrapping, image intrinsic size, object fit, aspect ratio, loading shifts, and keyboard or focus behavior where relevant.
4. Capture a full-page screenshot and a focused screenshot for each reproducible defect.
5. Record the URL, viewport, steps, expected result, actual result, severity, likely ownership surface, and screenshot paths.
6. Re-run the steps once in a fresh session.

Treat multiple symptoms as one issue only when they share one ownership boundary and one fix can close them together.

Complete when every matrix entry has a result and every proposed defect reproduces twice with saved evidence.

## 4. File evidence-backed issues

Search for duplicates before filing. Create one GitHub issue per independent defect with:

- a concise title;
- affected URL and exact viewport;
- numbered reproduction steps;
- expected and actual behavior;
- impact;
- screenshots embedded as durable GitHub-hosted attachments or repository-approved artifact links;
- acceptance criteria covering the relevant viewport range.

Follow repository templates and the account's required provenance footer. Never publish local filesystem paths as evidence.

Complete when each confirmed defect has a non-duplicate issue URL whose images render for another GitHub user.

## 5. Fix one issue per branch

For every issue, create an issue branch from the responsive-design integration branch and give one Terra-high subagent ownership of that branch or worktree. Include the issue URL, acceptance criteria, reproduction evidence, allowed write scope, and required checks.

The fixer:

1. Reproduces the issue before editing.
2. Implements the smallest fix at the correct ownership boundary.
3. Runs focused tests and the repository's required checks.
4. Captures post-fix screenshots at the failing viewport plus adjacent breakpoint widths.
5. Confirms the primary user path and unrelated matrix entries still behave correctly.

Complete when acceptance criteria pass and before and after screenshots are paired at matching viewports.

## 6. Review, commit, and open the issue PR

Run `jb-autoreview` against the issue branch and its integration-branch base. Verify every actionable finding, fix accepted findings, rerun checks, and repeat until the helper exits cleanly or a remaining finding is explicitly justified.

Use `jb-committer` to inspect and commit only the issue's coherent changes, then push. Open a PR targeting the responsive-design integration branch. Include:

- the issue link and closing keyword where appropriate;
- root cause and fix summary;
- checks run;
- matched pre and post screenshots;
- the required provenance footer.

Complete when the remote PR targets the integration branch, CI is green, screenshots render, and review has no accepted actionable findings.

## 7. Integrate and verify

Merge each successful issue PR into the responsive-design integration branch in dependency-safe order. After every merge, rerun affected viewports. After the final merge:

1. Run the full viewport matrix in clean browser sessions.
2. Run repository-required tests and a final branch-level `jb-autoreview` against the original base.
3. Capture final verification screenshots.
4. Report issue and PR URLs, merge commits, commands and checks, tested viewports, remaining risks, and the integration branch name.

Keep the integration branch separate from the default branch unless the user explicitly asks to land it there.

Complete when all issue PRs are present in the integration branch and the final matrix, tests, and autoreview are clean.
