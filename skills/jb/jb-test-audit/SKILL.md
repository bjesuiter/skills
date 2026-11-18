---
name: jb-test-audit
description: Audit tests, remove useless or tautological tests, improve test value, or review implementation-coupled tests; also gate newly authored or changed tests for independent behavioral value.
---

# JB Test Audit

**Matt Pocock’s durable minimum rule: “Tautological tests considered harmful.”**

Apply one value gate in every mode: each test must protect observable behavior, a credible regression, or an independently meaningful contract. Favor outside-in proof at the owner boundary. Optimize for confidence, not test count or deletion count.

## Choose a Mode

- **Authoring:** gate every proposed or changed test before writing it.
- **Audit:** inspect a focused test surface read-only, report candidates, then edit only authorized outcomes.
- **Campaign:** when asked to audit a whole subsystem, inventory its complete test surface, split it into coherent owner-boundary batches, and run the audit procedure on one batch at a time.

State the selected mode and bounded scope. Completion means the mode and ownership boundary are explicit.

## Inspect Before Judging

Read repository instructions, the complete tests, their production owners, entry points, callers, callees, sibling implementations, overlapping tests, CI routing, and relevant test commands. Inspect dependency source or types when a claim depends on them. Use history when it can explain the contract or seam.

Keep discovery read-only and report evidence before editing. Completion means each candidate is understood in its real call and coverage context.

## Apply the Value Gate

For each new, changed, or audited test, answer:

1. What observable behavior or independently meaningful contract does it protect?
2. What credible regression would make it fail for the intended reason?
3. Why would stronger existing proof not catch that regression?
4. Is this the strongest practical owner boundary, tested outside-in where feasible?
5. Does it demand a production export, flag, wrapper, injection hook, or path with no non-test caller?

In authoring mode, do not add the test until every answer supports its independent value. A bug regression must demonstrably fail against the pre-fix behavior for the intended reason and pass after the fix.

Flag candidates that:

- cannot meaningfully fail or contain no meaningful assertion;
- self-compare, reassert copied input, or derive expected values from the implementation under test;
- duplicate implementation logic in assertions;
- verify mocks, call shapes, private helpers, source text, or fixture behavior instead of observable behavior;
- fail under behavior-preserving refactors;
- duplicate stronger proof at an owner boundary;
- replay one shared contract at every layer or implementation without a distinct risk;
- require test-only production seams or keep dead production paths alive; or
- claim behavior their inputs and execution path cannot exercise.

Do not reject a test merely because it is static, slow, or source-based. Retain independent public API, protocol, configuration, migration, persistence, security, platform, generated artifact, packaging, release, architecture, or observable ordering contracts when their failure signal is meaningful.

Completion means every test passes the value gate or becomes an evidence-backed candidate.

## Record Candidate Evidence

Before recommending or making any deletion, record:

- exact test name and file/line reference;
- detectable failure: what it can actually catch and whether that failure is credible;
- non-test callers of any production or support seam;
- stronger remaining proof at the owner boundary, or why no proof is needed;
- relevant history when useful and the likely reason the test or seam exists;
- maintenance and confidence risk of changing it;
- recommended **retain**, **rewrite**, **replace**, or **delete** outcome and why;
- production or test-support cleanup unlocked; and
- exact focused validation command selected from repository conventions.

**Never delete without evidence.** Missing evidence changes the outcome to retain or investigate, not delete. Completion means every candidate has a complete, reviewable evidence record.

## Edit a Coherent Boundary

After findings are reviewed or edits are authorized, apply the smallest coherent outcome:

- rewrite implementation-coupled tests around observable owner behavior;
- replace weaker duplicates only when the replacement supplies stronger independent proof;
- consolidate repeated cases when each does not protect a distinct risk; and
- remove obsolete test-only seams and newly dead code together with proven low-value tests.

Do not add a replacement that restates the same implementation. Do not broaden a focused audit to inflate cleanup totals. Completion means the diff stays within one declared ownership boundary and preserves or improves independent proof.

## Validate

Run the smallest relevant owner and sibling tests first, then the repository-required formatter, linter, type checks, broader tests, and diff checks in the documented order. Use the repository’s own commands and test runner; never invent a runner. If deleting a static assertion, run the executable or generated-artifact check that now owns the contract. Inspect the final diff and distinguish production/tooling changes from test/test-support changes.

Completion means every planned command has a recorded result, or a named blocker and residual risk.

## Report Findings First

Lead with findings, even when there are none. For each finding provide:

1. severity and value impact;
2. file/line reference and exact test;
3. evidence and detectable failure;
4. recommended retain/rewrite/replace/delete action; and
5. validation command.

Use severity for test-value impact: **high** for false confidence or test-driven production distortion around important behavior, **medium** for fragile or duplicative maintenance with stronger proof, and **low** for localized redundancy.

After findings, report edits made, retained candidates and why, validation commands/results, remaining risks, and follow-up boundaries. Completion means the reader can evaluate every recommendation without reconstructing the audit.
