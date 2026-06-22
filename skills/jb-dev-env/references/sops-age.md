# SOPS/age backend

Use this reference only when encrypted secrets must live in git or when reviewing an existing SOPS/age setup.

## Decision rule

Varlock handles schema, validation, loading, redaction, and local/provider resolution. SOPS/age handles shared encrypted files committed to git.

Do not add SOPS/age just because a project has secrets. Add it only when the encrypted secret blob itself belongs in the repo, usually for multi-recipient GitOps or shared operational config.

## Recipient modes

- Native age: `.sops.yaml` uses `age1...`; decrypt via `SOPS_AGE_KEY_FILE` / `SOPS_AGE_KEY`.
- Raw SSH recipient: `.sops.yaml` uses `ssh-ed25519 ...`; decrypt via SSH private key file / `SOPS_AGE_SSH_PRIVATE_KEY_FILE` / `SOPS_AGE_SSH_PRIVATE_KEY_CMD`, not `ssh-agent`.
- SSH-agent plugin: `.sops.yaml` uses plugin-derived `age1...`; decrypt via `age-plugin-sshagent`, local plugin identity file, `SSH_AUTH_SOCK`, and an `ssh-ed25519` key loaded in the agent.

If the user wants Bitwarden/1Password SSH-agent-backed SOPS, prefer `age-plugin-sshagent`; do not use raw `ssh-ed25519 ...` recipients for that flow.

## Re-key

When recipients change:

```fish
sops updatekeys path/to/secrets.enc.yaml
```

Verify without printing secrets:

```fish
sops --decrypt path/to/secrets.enc.yaml >/dev/null
```

## SSH / vault caveat

Do not assume stock `age` can decrypt through `SSH_AUTH_SOCK` or Bitwarden's SSH agent. Verify the installed SOPS/age/plugin path with a local encrypt/decrypt smoke test.

`age-plugin-sshagent` supports `ssh-ed25519` only. Its identity file is not secret, but keep it local by default. Anyone able to talk to the SSH agent can request the needed signature, so avoid agent forwarding to untrusted hosts.

If verified, vault-gated local keys are highly recommended because they avoid loose plaintext key files and can make unexpected decrypt attempts visible.

## New-machine restore for age-plugin-sshagent

1. Install `sops`, `age`, Go, and `age-plugin-sshagent`.
2. Put Go bin on `PATH`.
3. Unlock/load the SSH-agent key.
4. Run:

```fish
age-plugin-sshagent list
age-plugin-sshagent keygen -k "<selector>" -o ~/.config/sops/age/<project>-sshagent.txt
age-plugin-sshagent recipient -i ~/.config/sops/age/<project>-sshagent.txt
```

5. Set `SOPS_AGE_KEY_FILE` to that identity file.
6. Verify:

```fish
sops --decrypt <file> >/dev/null
varlock load >/dev/null
```
