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

5. When migrating old repos, prefer Profile selector routing: commit `.env.<profile>` resolver refs and keep only `.env.local` as the gitignored profile selector.
6. Avoid adding new app-code dotenv loading by default. Remove or bypass double-loading where safe; let `varlock run -- ...` inject env for commands.
7. For macOS secrets, choose a Keychain flow deliberately; default new repos to Varlock-native `keychain(prompt)`.
8. Prefer Varlock provider plugins before custom shell glue.
9. Document bootstrap/run commands.

## Env loader migration

Prefer command wrappers over app-code env bootstrapping: `varlock run -- <command>` should be the default boundary where env enters the process. Avoid adding new `dotenv`/`@next/env`/custom preload code unless the framework genuinely requires it. When migrating, check for double-loading and remove or bypass old loaders only when behavior stays equivalent.

## Runtime env-loading conflicts

If the repo uses Bun, read [references/varlock-bun.md](references/varlock-bun.md) before changing env loading. Bun auto-loads `.env` files based on `NODE_ENV`/`BUN_ENV`, which can conflict with Varlock by injecting `.env.development` values before Varlock resolves config. Prefer disabling Bun automatic env loading with `env = false` in `bunfig.toml`, or use `--no-env-file` for `bun`/`bunx` invocations. For standalone `bun build` executables, consider `--no-compile-autoload-dotenv`.

Bun preload (`preload = ["varlock/auto-load"]`) is optional, but do not use it with framework integrations that watch `.env` files for live reload.

If the repo uses Deno, note there is no official Varlock Deno integration page yet. Do not invent a Deno policy; inspect how the repo loads env vars and ask JB for the current Deno rule when needed.

## Profile selector routing

Prefer this pattern when migrating old repos. Use Varlock environments to commit portable per-user/per-profile resolver refs while keeping the local profile selector gitignored. This is especially useful for fresh-machine clones and multi-user repos: secret references live in git, while each machine only needs a tiny `.env.local` selector and synced Keychain/provider auth.

Committed `.env.schema`:

```env
# @currentEnv=$DEV_ENV
# ---
# @type=enum(development, jb, test, production)
DEV_ENV=development
```

Gitignored `.env.local`:

```env
DEV_ENV=jb
```

Committed `.env.jb` or `.env.<user>`:

```env
API_KEY=keychain(service="my-app-api-key", account="jb")
```

Do not put the selector in the selected file. Fresh Mac restore: clone, create `.env.local` with `DEV_ENV=jb`, let iCloud Keychain/provider auth supply secrets from the committed refs.

## macOS Keychain flows

Preferred new-repo flow: use Varlock-native Keychain so VarlockEnclave gets compatible Keychain access.

```env
KEY=keychain(prompt)
# then optionally:
KEY=keychain(service="varlock", account="<project-slug>:<profile>:KEY")
```

Use project/profile-scoped accounts. Avoid one global item keyed only by env var name. Validate with `varlock load` and no `VarlockEnclave has access` errors.

Existing seeded-item fallback: if secrets already exist via `/usr/bin/security` or prompt migration is too much friction, bridge through `exec(...)` temporarily:

```fish
security add-generic-password -U -s varlock -a "<project-slug>:<profile>:KEY" -w <value>
```

```env
KEY=exec("security find-generic-password -s varlock -a \"<project-slug>:<profile>:KEY\" -w")
```

This keeps plaintext out of git, but it is a fallback: it bypasses VarlockEnclave and `security`-created items may be incompatible with Varlock-native `keychain(...)` ACLs. Prefer migrating to `keychain(prompt)` over time. Verify item presence without values: `security find-generic-password -s varlock -a "<account>" >/dev/null`; verify resolution with `varlock load >/dev/null`.

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

- `keychain(...)`: preferred on JB's Macs; portable if matching Keychain items sync via iCloud Keychain, otherwise recreate via `keychain(prompt)`.
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
- local secret source and Keychain strategy (`keychain(...)` preferred vs `exec(security)` fallback)
- Keychain service/account naming convention
- CI secret names
- local load/run smoke-test result
- SOPS re-key/decrypt evidence if used
