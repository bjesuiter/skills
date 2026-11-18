# TypeScript CLI preferences

Confirmed by JB on 2026-10-09 in the `jb-stack-prefs` discussion, describing his modern TypeScript CLI stack for 2026.

## CLI framework

- Established default: Commander for projects where JB wants to avoid experimentation. Commander is not legacy.
- Experimental choice: Gunshi when the project permits experimentation. Use it until concrete roadblocks justify switching back to Commander.
- Evaluation rationale: composable, modular subcommands with context sharing and lazy loading are attractive for organization and performance.
- Open question: whether Gunshi is better than Commander for those needs. Evaluate that in real use rather than assuming superiority.

## Prompts, hooks, builds, and tests

- Strong preference for quick interactive CLI paths: `@clack/prompts`. Combine it with Commander or Gunshi to enter an interactive mode depending on the invoked command.
- Preferred when git hooks are needed: Lefthook. Hooks remain optional; JB rarely uses them. Confirmed by JB on 2026-11-18, replacing the earlier evaluation status.
- Apply the build and test choices in [repository tooling](repository-tooling.md), including the TypeScript build tool and Bun test preference for pure Bun CLI repositories.

## Release tooling

- Evaluating: Bumpy for changelog generation and publishing. JB's initial impression is positive, but he considers it quite new and wants to evaluate it before treating it as an established default.
- Interested in trying: Fledgling for the initial npm package claim and OIDC setup. JB has heard good reports; this is a trial candidate, not a proven preference.
- Preferred use case for `@changesets/cli`: let each feature branch contribute release intent toward the next version when that change-management workflow is the main need.
- Pending comparison: assess Changesets against Bumpy for that workflow. Bumpy may eventually replace Changesets in JB's preferences; no replacement has been decided.

The scope distinction above describes JB's intended use. Changesets itself also supports version updates, changelogs, and publishing, as described in its [official repository](https://github.com/changesets/changesets). Compare the tools against the required workflow rather than assuming Changesets only manages change records.

JB's supplied package reference: [@changesets/cli on npmx](https://npmx.dev/package/@changesets/cli).
