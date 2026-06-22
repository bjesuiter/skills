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

- Shared/team repos: commit `.env.schema` and optional per-user/per-profile env files containing non-secret resolver references (`.env.jb`, `.env.alice`). Each developer keeps only their selector local.
- Solo/private repos: same pattern works well; commit resolver refs, not plaintext secrets.
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

5. For macOS secrets, choose a Keychain flow deliberately; default new repos to Varlock-native `keychain(prompt)`.
6. Prefer Varlock provider plugins before custom shell glue.
7. Document bootstrap/run commands.

## Local profile routing

Use Varlock environments to commit portable per-user/per-profile resolver refs while keeping the local profile selector gitignored. This is especially useful in multi-user repos because each person can commit/share their own non-secret references without sharing plaintext secrets.

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

Do not put the selector in the selected file. Fresh Mac restore: clone, create `.env.local` with `DEV_ENV=jb`, let iCloud Keychain/provider auth supply secrets.

## macOS Keychain flows

Preferred new-repo flow: use Varlock-native Keychain so VarlockEnclave gets compatible Keychain access.

```env
KEY=keychain(prompt)
# then optionally:
KEY=keychain(service="varlock", account="<project-slug>:<profile>:KEY")
```

Use project/profile-scoped accounts. Avoid one global item keyed only by env var name. Validate with `varlock load` and no `VarlockEnclave has access` errors.

Existing seeded-item migration flow: if secrets already exist via `/usr/bin/security` or prompt migration is too much friction, bridge through `exec(...)`:

```fish
security add-generic-password -U -s varlock -a "<project-slug>:<profile>:KEY" -w <value>
```

```env
KEY=exec("security find-generic-password -s varlock -a \"<project-slug>:<profile>:KEY\" -w")
```

This still keeps plaintext out of git and uses macOS Keychain, but bypasses VarlockEnclave. Verify item presence without values: `security find-generic-password -s varlock -a "<account>" >/dev/null`; verify resolution with `varlock load >/dev/null`.

## Monorepos

If the repo is a monorepo, read [references/varlock-monorepos.md](references/varlock-monorepos.md) before changing config.

Default: one `.env.schema` per app/service. Use `@import()` for shared root or sibling config.

## SOPS/age optional backend

Varlock = schema, validation, loading, redaction, local/provider resolution.

SOPS/age = shared encrypted files committed to git. SOPS config is YAML by convention.

Use SOPS/age only when encrypted secrets must live in git. For CI, use a separate CI-only age key; never copy a developer private key into CI.

Recipient modes:

- Native age: `.sops.yaml` uses `age1...`; decrypt via `SOPS_AGE_KEY_FILE` / `SOPS_AGE_KEY`.
- Raw SSH recipient: `.sops.yaml` uses `ssh-ed25519 ...`; decrypt via SSH private key file / `SOPS_AGE_SSH_PRIVATE_KEY_FILE` / `SOPS_AGE_SSH_PRIVATE_KEY_CMD`, not `ssh-agent`.
- SSH-agent plugin: `.sops.yaml` uses plugin-derived `age1...`; decrypt via `age-plugin-sshagent`, local plugin identity file, `SSH_AUTH_SOCK`, and an `ssh-ed25519` key loaded in the agent.

If the user wants Bitwarden/1Password SSH-agent-backed SOPS, prefer `age-plugin-sshagent`; do not use raw `ssh-ed25519 ...` recipients for that flow.

When recipients change:

```fish
sops updatekeys path/to/secrets.enc.yaml
```

## New-machine restore

Portability depends on the resolver:

- `keychain(...)`: preferred on JB's Macs; portable if matching Keychain items sync via iCloud Keychain, otherwise recreate via `keychain(prompt)`.
- `varlock(local:...)`: avoid by default; not portable, recreate on every machine.
- cloud provider refs: portable after logging into that provider.
- native SOPS/age: portable for recipients that hold a valid private key.
- `age-plugin-sshagent`: install `sops`, `age`, Go, and `age-plugin-sshagent`; put Go bin on `PATH`; unlock/load the SSH-agent key; run `age-plugin-sshagent list`; create identity with `age-plugin-sshagent keygen -k "<selector>" -o ~/.config/sops/age/<project>-sshagent.txt`; get recipient with `age-plugin-sshagent recipient -i ~/.config/sops/age/<project>-sshagent.txt`; set `SOPS_AGE_KEY_FILE` to that identity file; verify with `sops --decrypt <file> >/dev/null` and `varlock load`.

## SSH / vault caveat

Do not assume stock `age` can decrypt through `SSH_AUTH_SOCK` or Bitwarden's SSH agent. Verify the installed SOPS/age/plugin path with a local encrypt/decrypt smoke test.

`age-plugin-sshagent` supports `ssh-ed25519` only. Its identity file is not secret, but keep it local by default. Anyone able to talk to the SSH agent can request the needed signature, so avoid agent forwarding to untrusted hosts.

If verified, vault-gated local keys are highly recommended because they avoid loose plaintext key files and can make unexpected decrypt attempts visible.

## Deliverables

Report:

- Varlock strategy and whether SOPS/age is needed
- files changed
- run wrappers added
- local secret source and Keychain strategy (`keychain(...)` vs `exec(security)`)
- Keychain service/account naming convention
- CI secret names
- local load/run smoke-test result
- SOPS re-key/decrypt evidence if used
