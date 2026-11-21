---
name: jb-dev-env
description: "Use for Varlock development env setup or review: schemas, profiles, SOPS/age secrets via Bitwarden's SSH agent on an interactive desktop, and CI secret access."
---

# JB dev env

Use Varlock for schema, validation, redaction, profiles, and process injection. Store desktop secrets as committed SOPS ciphertext encrypted to an `age-plugin-sshagent` recipient from JB's Bitwarden Ed25519 key. Resolve individual values through Varlock `exec(...)` without writing decrypted files. This flow is **interactive desktop**; Bitwarden SSH-agent approval is not yet available on JB's VMs.

Read [the SOPS/Bitwarden workflow](references/sops-age.md) when creating, changing, or restoring secrets. For existing `keychain(...)` repos, use [the legacy Keychain reference](references/legacy-varlock-keychain.md) when maintaining or migrating them.

## Workflow

1. Inspect `.env*`, `.sops.yaml`, ciphertext, `.gitignore`, scripts, CI/deploy config, runtime config, and existing env loaders.
2. Commit `.env.schema` with required fields, types, sensitivity, AI-safe context, and `@currentEnv` for profiles. Keep app code Varlock-agnostic; wrap commands with `varlock run -- ...`. Use a JS dev dependency or the repo's fitting CLI runner.
3. Commit `.env.<profile>` files with public values and SOPS resolver references, plus `.sops.yaml` and ciphertext. Keep decrypted secrets off disk and local identity files out of git; inspect tracked files, not only ignore rules. Avoid `varlock(local:...)` because it binds secrets to one machine.
4. Select clear profiles inline in scripts (`DEV_ENV=development varlock run -- ...`); use a gitignored `.env.local` selector only for machine-specific choice. Keep privileged `ops` references out of everyday profiles. Prefer a suitable Varlock provider plugin; otherwise use a small project helper that maps approved keys to ciphertext and returns one decrypted value to `exec(...)` through a pipe.
5. Remove duplicate app-level dotenv loading when behavior stays equivalent. For Bun, read [its Varlock conflict guide](references/varlock-bun.md). For monorepos, read [the schema layout guide](references/varlock-monorepos.md). For Deno, inspect actual loading and ask JB for a rule when needed.
6. Verify each affected SOPS file and Varlock profile with output redirected to `/dev/null`. Check tracked env files for plaintext, and document desktop bootstrap, run commands, and any host limitations without printing secrets.

For CI or VMs that must decrypt, arrange a separately authorized recipient and platform-provisioned identity. Confirm recipient policy before changing `.sops.yaml` or re-keying; the desktop SSH-agent identity is not an unattended credential. Preserve existing cloud-provider resolvers where used and judge portability by their actual provider.
