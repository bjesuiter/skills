---
name: jb-verifiable-modules
description: Make modules independently verifiable, audit agent-readiness, or design verification boundaries for agent-driven code changes. Produces runnable behavioral evidence and a bounded improvement plan or validated implementation, including readability/performance tradeoffs.
---

# Independently Verifiable Modules

1. Set the boundary and mode.
   Read repository instructions and select one module or subsystem. Record its requested behavior, human domain terms, dependency constraints, and relevant risks. Choose audit (no edits), design (proposed boundary and checks), or improve (authorized implementation). Ask only for missing decisions that block the work. Read [source and scope](references/source.md) before applying the framing.
   Done when the target, mode, constraints, and expected deliverable are explicit.

2. Find the executable contract.
   Inspect the public entry point, callers, dependency boundaries, existing tests, and repository test commands. Identify observable outputs, state changes, errors, and important interactions. Use requirements or known examples as an independent oracle; do not derive expected results by copying the implementation. Retain the names people use to describe the domain.
   Done when each important behavior has an expected result and a concrete check, or a named evidence gap.

3. Establish a safe baseline.
   For existing code, run the smallest existing check that exercises the owner boundary without starting the whole application. If no isolated check exists, record that gap and use the nearest safe check only as partial evidence. For a new design with no implementation, specify the proposed command and fixtures without claiming a baseline run. Record the command, setup, fixtures, outcome, and dependency requirements. Use disposable local state; do not probe production or trigger external side effects without explicit authorization. Keep interactions under test real where practical; replace only dependencies outside the boundary and retain integration proof for those interactions. Inspect at least one credible failure case and how the check detects it. In improve mode, demonstrate a new regression check failing before the fix when applicable; audit mode does not modify code to manufacture a failure.
   Done when another agent can reproduce the baseline, or the exact execution blocker is recorded. Coverage percentages alone do not establish verification.

4. Choose the smallest useful boundary change.
   Rank gaps by the behavior they leave unverified: hidden global state, inseparable startup, uncontrolled time or I/O, missing observations, or unavailable fixtures. Prefer an existing public contract and controlled dependencies. In audit mode, report evidence-backed changes without editing. In design mode, specify the boundary, checks, and adoption cost without claiming execution. In improve mode, implement only the authorized change and its behavioral checks. Avoid new production exports used only by tests, speculative adapters, and cosmetic function splitting.
   Done when each proposed or implemented change closes a named verification gap; explain why an already independently verifiable module needs no change.

5. Preserve human intervention and justify complexity.
   Keep a clear entry point, domain names, and an observable path for a human spot-check or incident investigation. Judge function size and complexity by concrete verification or maintenance risks rather than using them as automatic refactoring triggers; obey repository lint and complexity rules. Before accepting a readability sacrifice for performance, compare a representative benchmark against the baseline, record conditions and results, and rerun correctness checks. Label unavailable or inconclusive performance evidence as unproven; do not justify added complexity with an assumed speedup.
   Done when the human inspection path is identified and each performance tradeoff has evidence or remains explicitly unaccepted.

6. Verify and hand off.
   In improve mode, rerun isolated checks, relevant integration checks, and repository-required validation; inspect the final diff for unrelated changes. For all modes, report the target and verdict (independently verifiable, gaps found, or blocked), behavioral evidence with exact commands and actual outcomes, remaining integration risks, and the next bounded action. Separate executed checks from proposed checks. An unavailable environment is a blocker, not a pass.
   Done when the recipient can reproduce the evidence and see what remains unverified.

Use jb-test-audit for detailed test-value judgments and jb-autoreview for second-model diff review when available. This workflow owns the module's independent execution and observation boundary; it does not replace either review.
