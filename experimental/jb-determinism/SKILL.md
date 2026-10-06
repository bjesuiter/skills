---
name: jb-determinism
description: Use when an ad-hoc helper script, repeating mechanical agent step, or deterministic prompt/skill prose should be analyzed and made reproducible; also use for a retrospective of recurring agent or coding work.
---

# JB Determinism (Experimental)

Replace reliably mechanical work with a reproducible command, schema, test, or helper. Keep judgment, context gathering, prioritization, and tradeoffs as agent work. This source lives in `experimental/` and is not installable through this repository's `skills/` discovery.

## Automatic immediate workflow analysis

Run this branch immediately after noticing a repeated mechanical step, a one-off helper script, or deterministic prose in the current task.

1. Capture the exact repeated inputs, outputs, side effects, failure modes, and invocation context. **Done:** a concrete before/after behavior is written down.
2. Classify the work: make stable transformations, validation, lookup, or formatting deterministic; retain ambiguous intent, incomplete context, prioritization, and tradeoffs as agent steps. For repeated structured code discovery or transformation, prefer a reviewable AST query or codemod over free-form edits or semantics-blind regex; decide the transformation once as agent judgment, then automate execution and verification. **Done:** every step is assigned to a deterministic mechanism or to agent judgment, with a reason.
3. Check the repository's current authorization. If implementation is authorized, create or improve the smallest compatible repo-owned code, test, schema, CLI, AST query, or codemod; otherwise produce a ranked proposal with a focused diff plan and validation command. **Done:** either the authorized change exists or the ranked plan names files, rationale, and proof.
4. Run the narrowest relevant validation and inspect the resulting diff or output. **Done:** recorded evidence shows the deterministic path behaves as intended, or the limitation is explicit.

## Manual retrospective

Run this branch only when asked to review past agent or coding work for determinism opportunities. Its purpose is **meta verification**: observe where agents fail, then improve the environment, constraints, skills, scripts, architecture, or verification harness so future agents avoid or detect that failure.

1. Select the latest up to 20 current-repo-relevant sessions. Prefer sessions whose title, metadata, messages, changed paths, or stated task mention this repository, its worktree, branch, or files; exclude unrelated personal/chat sessions. Use `sessions_list` to find candidates, `sessions_search` to confirm relevance, and `sessions_history` to inspect only the candidates needed. **Done:** no more than 20 sessions are listed with a one-line relevance reason.
2. When local CLI evidence is useful, inspect the supported families `openclaw sessions` and `openclaw transcripts`; use their built-in help before choosing a subcommand. **Done:** every CLI command used is supported by its help output.
3. Treat unavailable, redacted, compacted, or incomplete histories as a limitation, not negative evidence. Do not infer that a workflow never occurred from missing transcripts. **Done:** each incomplete source is marked skipped or partial with its reason.
4. Identify repeated mechanical patterns and separate them from context-dependent judgment and tradeoffs. Rank candidates by repetition, error risk, effort saved, and implementation cost. **Done:** each candidate has its retained-agent boundary and a ranking rationale.
5. Check implementation authorization. If code changes are currently authorized, implement the highest-value bounded candidate and validate it; otherwise give the ranked proposal/diff plan only. Do not add transcript-collection scripts. **Done:** the result is either a validated authorized change or a ranked, file-specific plan with validation commands.
