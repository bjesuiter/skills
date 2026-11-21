# Repository tooling preferences

Confirmed by JB on 2026-10-09 in the `jb-stack-prefs` discussion.

## Linting and formatting

- Preferred linting for projects controlled by JB: oxlint.
- For projects outside JB's control: ESLint, respecting the repository's tooling.
- Legacy linting in JB's own projects: ESLint, superseded by oxlint as the current preference.
- Preferred formatting: oxfmt.
- Legacy formatting: Prettier, superseded by oxfmt as the current preference.
- These legacy labels describe JB's preferences. Apply the skill's existing-repository guidance before changing tooling.

## Build tooling

- Preferred TypeScript build tool for npm libraries and CLI apps: tsdown.
- Preferred frontend build tooling: Vite.

## Testing

- For pure Bun repositories, such as TypeScript CLI projects, prefer `bun test` for unit, integration, and even end-to-end tests where appropriate. JB values its fast test runner.
- For Vite repositories that make little use of Bun, Vitest is an accepted choice.
- When using Vitest Browser Mode for component integration tests, use Vitest for unit tests too, keeping the number of testing frameworks to what the project needs.
- For browser end-to-end tests, use Playwright and follow JB's `jb-testing` skill. This browser-specific preference applies even when other tests use Bun or Vitest.
