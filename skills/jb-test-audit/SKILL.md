---
name: jb-test-audit
description: Use when writing, changing, reviewing, or pruning tests. Gate new tests for independent behavioral value and audit low-value, implementation-coupled, duplicative tests and test-only production seams.
---

# JB Test Audit

Keep tests that independently protect meaningful behavior; remove or rewrite tests that merely preserve an implementation. Optimize for confidence, not deletion count.

This is JB’s portable adaptation of OpenClaw’s `test-audit` skill. It retains the value bar and audit discipline while removing OpenClaw-specific commands, infrastructure, and release flow.

- Original: https://github.com/openclaw/openclaw/blob/main/.agents/skills/test-audit/SKILL.md
- Fork intent: generic use in any repository and with any test runner.

## Authoring Gate

Before adding or changing a test, answer all four questions:

1. What observable behavior, invariant, or independent contract does it protect?
2. What credible regression would make it fail?
3. Why does existing coverage not already catch that regression? Assign each contract one primary owner at the strongest practical boundary. Add another layer only for a distinct risk, such as transport, lifecycle, persistence, or integration failure.
4. Does it require a production-only-for-tests seam—an export, flag, wrapper, or injection hook—that production callers do not need? If so, test at a real boundary instead.

If an answer is missing, do not add the test yet. Prefer extending a table-driven case or shared fixture over a near-duplicate test. A test that breaks under behavior-preserving refactoring is asserting implementation, not behavior; rewrite it at the owning boundary.

A bug regression must fail against the pre-fix behavior for the intended reason and pass after the repair. One owner-boundary regression is normally enough; do not replay the same scenario at every layer it crosses.

## Low-Value Patterns

Reject new tests and investigate existing tests that:

- have no meaningful assertion, self-compare, or reassert input copying;
- grep source, imports, private call shapes, or incidental strings rather than an independent contract;
- duplicate a stronger owner-boundary test or replay a shared helper at every provider;
- use expected values produced by the implementation under test;
- make a mock implement the very behavior being asserted;
- preserve test-only exports, globals, wrappers, or dead production paths;
- rely on fixtures that already provide the receipt, ordering, persistence, or callback they claim to verify;
- exercise declared capability flags rather than the delivered behavior they promise;
- pass negative controls for an unrelated guard or path; or
- promise more in their name or fixture than their input can exercise.

## Retention Bar

Keep tests when they independently enforce a public API, protocol, config, migration, persistence, security, platform, default, generated artifact, package, release, prompt/output byte, or architecture contract. Also keep credible regressions and observable ordering guarantees.

Static or slow is not a deletion reason. Source inspection can be valid when it is the cheapest independent guard for a user-visible key, byte, path, or generated artifact and survives identifier-only refactors. Treat a retained baseline failure as a possible product defect: reproduce and repair the owner before considering removal.

## Audit Workflow

1. **Discover read-only.** Read repository guidance, the complete test and production owner, entry points, callers, callees, sibling implementations, overlapping tests, CI routing, and relevant history. Inspect dependency source or types when a claim depends on it.
2. **Record evidence.** For every candidate, capture the exact test, the failure it can detect, non-test callers of any seam, stronger remaining proof, why it exists, deletion unlocked, risk, and focused validation command. Missing evidence means no deletion.
3. **Change one coherent boundary.** Remove obsolete test-only seams and dead paths rather than preserving aliases. Move retained regressions to canonical owners and consolidate repeated assertions into a generic contract. Do not create replacement tests that repeat the same implementation.
4. **Validate proportionately.** Run the narrow owner and sibling tests first; then run required repository checks, formatting, and `git diff --check`. Inspect the final diff and distinguish production/tooling changes from test and test-support changes.
5. **Close out honestly.** Report what was removed or retained, why, proof actually run, remaining risks, and any follow-up batch. Do not commit, push, open a PR, or land changes without authorization.

## Guardrails

- Prefer a few high-confidence candidates to a speculative mass cleanup.
- Do not edit code or tests while the relevant test runner is actively watching the checkout.
- Never delete a test merely because it looks coupled; prove that stronger independent proof remains or that no meaningful contract exists.
- Stop at a coherent ownership boundary. Broader sweeps become separate follow-up changes.
