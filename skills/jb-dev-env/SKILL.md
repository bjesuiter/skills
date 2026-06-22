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
- Use SOPS/age only for committed encrypted secret blobs / multi-recipient GitOps secrets.

Repo modes:

- Shared/team repos: commit `.env.schema`; gitignore real env files. Each developer creates local env files using their own source.
- Solo/private repos: may commit env files containing non-secret resolver references (`keychain(...)`, Bitwarden/1Password/provider refs, `exec(...)`). Do not commit plaintext secrets.
- Avoid machine-local `varlock(local:...)` by default; it is device-bound and not portable across JB's Macs.
- Shared secret repos: commit SOPS/age encrypted blobs and wire Varlock to them via provider/plugin/`exec(...)`.

JB macOS default: prefer built-in Varlock `keychain()` for personal secrets, because Keychain can sync across Macs via iCloud Keychain when configured.

## Workflow

1. Inspect `.env.schema`, `.env*`, package scripts, CI, `.sops.yaml`, and `secrets*`.
2. Define/adjust `.env.schema`; mark sensitive vars explicitly.
3. Ensure real env files are gitignored.
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

5. For macOS secrets, start with `KEY=keychain(prompt)`; optionally replace with `keychain(service="...", account="...")`.
6. Prefer Varlock provider plugins before custom shell glue.
7. Document bootstrap/run commands.

## Monorepos

If the repo is a monorepo, read [references/varlock-monorepos.md](references/varlock-monorepos.md) before changing config.

Default: one `.env.schema` per app/service. Use `@import()` for shared root or sibling config.

## SOPS/age optional backend

Varlock = schema, validation, loading, redaction, local/provider resolution.

SOPS/age = shared encrypted files committed to git.

SOPS config is YAML by convention.

Use SOPS/age only when encrypted secrets must live in git. For CI, use a separate CI-only age key; never copy a developer private key into CI.

When recipients change:

```fish
sops updatekeys path/to/secrets.enc.yaml
```

## New-machine restore

Portability depends on the resolver:

- `keychain(...)`: preferred on JB's Macs; portable if matching Keychain items sync via iCloud Keychain, otherwise recreate via `keychain(prompt)`.
- `varlock(local:...)`: avoid by default; not portable, recreate on every machine.
- cloud provider refs: portable after logging into that provider.
- SOPS/age: portable for recipients that hold a valid private key.

## SSH / vault caveat

Do not assume `age` can decrypt through `SSH_AUTH_SOCK` or Bitwarden's SSH agent. Verify the installed SOPS/age/plugin path with a local encrypt/decrypt smoke test.

If verified, vault-gated local keys are highly recommended because they avoid loose plaintext key files and can make unexpected decrypt attempts visible.

## Deliverables

Report:

- Varlock strategy and whether SOPS/age is needed
- files changed
- run wrappers added
- local secret source
- CI secret names
- local load/run smoke-test result
- SOPS re-key/decrypt evidence if used
