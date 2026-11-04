# Source and scope

Matt Pocock, 4 November 2026, 12:12:35 UTC:
https://x.com/mattpocockuk/status/2117953152376799498

The complete long-form post was retrieved directly from X on 4 November 2026 and cross-checked against https://api.fxtwitter.com/status/2117953152376799498. The retrieved post has no outbound primary-content links or parent post. No follow-up thread is relied on here.

## Author's argument

Pocock argues that agents learn how code works by executing and probing it, so agent-facing readability should emphasize verifiability. He recommends independently testable modules and permits some readability sacrifice for performance. He retains human spot-checks, observability, and domain language shared between the human request and code.

His illustration pairs a complex module with 100% test coverage and says an agent needs "zero time" to become comfortable. His conclusion says function size and cyclomatic complexity do not matter to agents. These are the author's claims, not measured guarantees supplied by this skill.

## Procedure designed from that argument

The skill turns independent verification into a reproducible owner-boundary check with explicit inputs, expected behavior, observations, and dependency setup. It prioritizes missing verification boundaries over cosmetic refactoring while preserving human intervention.

Independent oracles, meaningful failure cases, safe local probes, integration checks, measured performance comparisons, and explicit blockers are safeguards added by this workflow. The post does not establish that coverage proves correctness, that agents need no investigation, or that repository standards can be ignored. The skill makes none of those assumptions.
