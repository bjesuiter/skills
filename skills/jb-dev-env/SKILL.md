---
name: jb-dev-env
description: Use when setting up or reviewing a development environment, especially Varlock env schemas, gitignored env files, macOS Keychain/local secret storage, SOPS/age optional GitOps secrets, CI secret access, dotenv bootstrapping, or secure local dev onboarding.
---

# JB Dev Env

Build secure, reproducible dev envs without putting secrets in git or app code.

## Default model

Use **Varlock first**:

- Commit `.env.schema`: required vars, types, sensitivity, AI-safe config context.
- Keep app code Varlock-agnostic. Wrap commands with `varlock run -- ...`.
- Detect the package manager/toolchain and use its native style: dev dependency for JS package repos; `npx`/`bunx`/`pnpm dlx`/`uvx`/direct CLI only when that fits the repo better.
- Use SOPS/age only for committed encrypted secret blobs / multi-recipient GitOps secrets.
- Never print secret values. Validate with redacted/presence checks, not echoing resolved secrets.

Repo modes:

- Shared/team repos: commit `.env.schema` and optional per-user/per-profile env files containing non-secret resolver references (`.env.jb`, `.env.alice`). Each developer keeps only their selector local.
- Solo/private repos: same pattern works well; commit resolver refs, not plaintext secrets.
- Avoid machine-local `varlock(local:...)` by default; it is device-bound and not portable across JB's Macs.
- Shared secret repos: commit SOPS/age encrypted blobs and wire Varlock to them via provider/plugin/`exec(...)`.

JB macOS default: prefer built-in Varlock `keychain()` for personal secrets, because Keychain can sync across Macs via iCloud Keychain when configured.

## Workflow

1. Inspect files that decide how env vars enter the app:
   - `.env.schema`, `.env*`, `.gitignore`, package scripts, `turbo.json`
   - CI/workflow files such as `.github/workflows/*`
   - Dockerfiles, compose files, and deployment config for Vercel/Cloudflare/Netlify/etc.
   - runtime config such as `bunfig.toml`, `deno.json`, `deno.jsonc`
   - existing env loaders: `dotenv`, `@next/env`, `cross-env`, `env-cmd`, `direnv`, custom bootstrap code
   - `.sops.yaml`, `secrets*`, encrypted secret blobs
2. Define/adjust `.env.schema`; mark sensitive vars explicitly.
3. Ensure real env files are gitignored and not already tracked.
4. Add run wrappers, e.g.:

```json
{
  "scripts": {
    "dev": "varlock run -- vite",
    "build": "varlock run -- vite build",
    "test": "varlock run -- vitest"
  }
}
```

5. When migrating old repos, prefer Profile selector routing: commit `.env.<profile>` resolver refs and, when possible, inline the `DEV_ENV` selector directly into `package.json` commands so fresh clones do not need a local `.env.local` selector. Keep `.env.local` only when scripts cannot safely encode the profile.
6. Avoid adding new app-code dotenv loading by default. Remove or bypass double-loading where safe; let `varlock run -- ...` inject env for commands.
7. For macOS secrets, choose a Keychain flow deliberately; default new repos to Varlock-native `keychain(...)` refs created by `varlock keychain import` or `varlock keychain set` (Varlock >= 1.9.0).
8. Prefer Varlock provider plugins before custom shell glue.
9. Document bootstrap/run commands.

## Env loader migration

Prefer command wrappers over app-code env bootstrapping: `varlock run -- <command>` should be the default boundary where env enters the process, as long as not defined otherwise inside a repo. Avoid adding new `dotenv`/`@next/env`/custom preload code unless the framework genuinely requires it. When migrating, check for double-loading and remove or bypass old loaders only when behavior stays equivalent.

## Runtime env-loading conflicts

If the repo uses Bun, read [references/varlock-bun.md](references/varlock-bun.md) before changing env loading. Bun auto-loads `.env` files based on `NODE_ENV`/`BUN_ENV`, which can conflict with Varlock by injecting `.env.development` values before Varlock resolves config. Prefer disabling Bun automatic env loading with `env = false` in `bunfig.toml`, or use `--no-env-file` for `bun`/`bunx` invocations. For standalone `bun build` executables, consider `--no-compile-autoload-dotenv`.

Bun preload (`preload = ["varlock/auto-load"]`) is optional, but do not use it with framework integrations that watch `.env` files for live reload.

If the repo uses Deno, note there is no official Varlock Deno integration page yet. Do not invent a Deno policy; inspect how the repo loads env vars and ask JB for the current Deno rule when needed.

## Profile selector routing

Prefer this pattern when migrating old repos. Use Varlock environments to commit portable per-user/per-profile resolver refs. Secret references live in git, while the selected profile comes from either inline command env vars or a tiny gitignored `.env.local` selector.

Prefer inline selectors in `package.json` when the repo's scripts are profile-specific. This avoids requiring a freshly cloned repo to create `.env.local` before common commands work:

```json
{
  "scripts": {
    "dev": "DEV_ENV=jb varlock run -- vite",
    "build": "DEV_ENV=jb varlock run -- vite build",
    "test": "DEV_ENV=test varlock run -- vitest"
  }
}
```

Use gitignored `.env.local` only when the profile must stay machine/user-selectable outside committed scripts:

```env
DEV_ENV=jb
```

Committed `.env.schema`:

```env
# @currentEnv=$DEV_ENV
# ---
# @type=enum(development, jb, test, production)
DEV_ENV=development
```

Committed `.env.jb` or `.env.<user>`:

```env
API_KEY=keychain(service="my-app-api-key", account="jb")
```

Do not put the selector in the selected file. Fresh Mac restore with inline scripts: clone and run the script; iCloud Keychain/provider auth supplies secrets from the committed refs. Fresh Mac restore with `.env.local`: clone, create `.env.local` with `DEV_ENV=jb`, then run commands.

## macOS Keychain flows

Varlock >= 1.9.0 has native `varlock keychain` subcommands. Prefer them over `/usr/bin/security` for creating/importing secrets because they create Keychain items with Varlock-compatible helper access.

Preferred new-repo flow: use Varlock-native Keychain refs with project/profile-scoped accounts.

```fish
varlock keychain set API_KEY --project <project-slug> --profile jb --write-to .env.jb
```

This stores the secret in macOS Keychain and writes a resolver ref like:

```env
API_KEY=keychain(service="varlock", account="<project-slug>:jb:API_KEY")
```

Use project/profile-scoped accounts. Avoid one global item keyed only by env var name. Validate with `varlock load` and no `VarlockEnclave has access` errors.

### Import plaintext env files into Keychain

When migrating a plaintext env file, use `varlock keychain import` instead of `security add-generic-password` plus manual ref fixes.

Import in place:

```fish
varlock keychain import .env --project <project-slug> --profile jb
```

Import from a plaintext source and write resolver refs to a committed per-profile file:

```fish
varlock keychain import .env --project <project-slug> --profile jb --write-to .env.jb
```

Use `--force` only when intentionally overwriting existing Keychain items or refs. After importing, remove plaintext secret files from git/history as needed and keep only resolver refs committed.

Useful metadata-only checks:

```fish
varlock keychain list varlock
varlock keychain list <project-slug>
```

Do not print resolved secret values. Verify resolution with `varlock load >/dev/null`.

### Fix permissions for older `security`-created items

If secrets already exist because they were created with `/usr/bin/security`, do not bridge through `exec(security ...)` unless absolutely necessary. Prefer converting refs to `keychain(...)` and granting Varlock helper access:

```fish
varlock keychain fix-access --account "<project-slug>:<profile>:KEY"
```

Or fix every explicit `keychain(...)` ref in an env file:

```fish
varlock keychain fix-access --path .env.jb
```

If the item is in a non-default Keychain, add `--keychain Login` or the appropriate Keychain name. Then validate with `varlock load >/dev/null`.

Temporary fallback only: if permission fixing or migration is blocked, bridge through `exec(...)` for the shortest possible time:

```env
KEY=exec("security find-generic-password -s varlock -a \"<project-slug>:<profile>:KEY\" -w")
```

This keeps plaintext out of git, but it bypasses VarlockEnclave and can expose values through shell execution. Replace it with `keychain(...)` plus `varlock keychain fix-access` or re-import via `varlock keychain import` as soon as possible.

## Monorepos

If the repo is a monorepo, read [references/varlock-monorepos.md](references/varlock-monorepos.md) before changing config.

Default: one `.env.schema` per app/service. Use `@import()` for shared root or sibling config.

## SOPS/age optional backend

Varlock = schema, validation, loading, redaction, local/provider resolution.

SOPS/age = shared encrypted files committed to git. SOPS config is YAML by convention.

Use SOPS/age only when encrypted secrets must live in git. For CI, use a separate CI-only age key; never copy a developer private key into CI.

For recipient modes, SSH-agent-backed vault flows, and re-key commands, read [references/sops-age.md](references/sops-age.md).

## New-machine restore

Portability depends on the resolver:

- `keychain(...)`: preferred on JB's Macs; portable if matching Keychain items sync via iCloud Keychain, otherwise recreate via `varlock keychain set` or `varlock keychain import`.
- `varlock(local:...)`: avoid by default; not portable, recreate on every machine.
- cloud provider refs: portable after logging into that provider.
- native SOPS/age: portable for recipients that hold a valid private key.
- `age-plugin-sshagent`: portable after plugin install, local identity-file setup, vault/agent unlock, and decrypt/load verification; read [references/sops-age.md](references/sops-age.md) for the exact flow.

## Validation

Use fish syntax for local checks. Do not print secret values.

```fish
varlock load >/dev/null
git check-ignore .env.local
git ls-files '.env*'
```

If `git ls-files '.env*'` shows tracked files, verify each is schema or resolver-only before proceeding. Plaintext secret files must not be tracked.

If SOPS/age is used:

```fish
sops --decrypt path/to/secrets.enc.yaml >/dev/null
```

## Deliverables

Report:

- Varlock strategy and whether SOPS/age is needed
- files changed
- run wrappers added
- local secret source and Keychain strategy (`varlock keychain` + `keychain(...)` preferred vs temporary `exec(security)` fallback)
- Keychain service/account naming convention
- CI secret names
- local load/run smoke-test result
- SOPS re-key/decrypt evidence if used
