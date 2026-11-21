# Verify the candidate

Use the repository's review workflow on the intended change. Resolve actionable
findings and record the reviewed commit and outcome. Follow the selected mode's
instructions for review after a rebase.

Record the final source and base SHAs. Select required suites and builds from
the diff and its affected behavior, using the repository's check planner when
available. For each result, record the command, tested state and outcome or log.
When either SHA changes, reconsider dependencies, configuration and conflict
resolutions. Reuse passing results with their original SHAs and a reason their
coverage still applies. Run missing or invalidated checks, or the full required
gate if impact is unclear. Report any failure, outstanding approval or unverified
requirement before declaring readiness.
