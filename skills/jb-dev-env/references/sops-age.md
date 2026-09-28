# SOPS/age with a Bitwarden SSH-agent identity

This is JB's default encrypted storage workflow on an **interactive desktop**. Varlock owns schema, profiles, validation, redaction, and process loading. SOPS holds committed ciphertext. `age-plugin-sshagent` asks Bitwarden's SSH agent to use JB's Ed25519 key. The local plugin identity contains a key selector and derivation salt, not a private key. Approval through Bitwarden is currently unavailable on JB's VMs.

## Recipient and desktop bootstrap

1. Install `sops`, `age`, Go, and `age-plugin-sshagent`; put the Go binary directory on `PATH`. On macOS, `brew install sops age` and `go install github.com/eszio/age-plugin-sshagent@v0.1.1` match the working Ornn Forge setup.
2. Unlock Bitwarden's SSH agent and ensure `SSH_AUTH_SOCK` reaches it. Use `age-plugin-sshagent list` to find the intended Ed25519 key fingerprint.
3. Create a local plugin identity, for example:

```sh
age-plugin-sshagent keygen -k '<Bitwarden key fingerprint>' -o "$HOME/Library/Application Support/sops/age/keys.txt"
chmod 600 "$HOME/Library/Application Support/sops/age/keys.txt"
```

4. Use `age-plugin-sshagent recipient -i "$HOME/Library/Application Support/sops/age/keys.txt"` to get the recipient. Put that plugin-derived `age1...` recipient in `.sops.yaml` under the relevant `creation_rules`; commit the configuration and encrypted files. When using a non-default identity path, set `SOPS_AGE_KEY_FILE` to it. SOPS can read the default identity path shown above on macOS.
5. Verify `sops decrypt <ciphertext> >/dev/null`, then load each affected Varlock profile with output redirected to `/dev/null`. Bitwarden may ask for approval.

Keep the identity file local even though it has no private key. Do not forward this SSH agent to untrusted hosts: a process that can request its signature may decrypt the ciphertext.

## No plaintext file workflow

Use a committed `.env.<profile>` file with `exec(...)` references to individual ciphertext values. A project helper can map allowed keys to `secrets/<profile>.env` and call `sops decrypt --extract '["KEY"]' <ciphertext>`. Varlock receives the value through the process pipe. Avoid whole-file decrypts to a path, `sops edit` with an editor that writes plaintext swap/backup files, and plaintext `.env` staging files.

For updates, send the value from a secure source to `sops set --value-stdin <ciphertext> '["KEY"]'`. `--value-stdin` avoids secret values in process arguments. Keep values out of shell history, logs, and terminal output. For a new ciphertext file, create a secret-free skeleton under the matching `.sops.yaml` creation rule, encrypt it, then add values through `sops set --value-stdin`. Verify decrypt and Varlock load with stdout redirected.

When recipients change, run `sops updatekeys <ciphertext>` for each affected file, then verify decryption. Adding a recipient for CI or a VM requires a separate authorization and a separately provisioned identity; the desktop SSH-agent identity is not an unattended credential.

## Other recipient modes

Native age uses an `age1...` recipient with `SOPS_AGE_KEY_FILE` or `SOPS_AGE_KEY`. A raw `ssh-ed25519 ...` recipient uses an SSH private key file or `SOPS_AGE_SSH_PRIVATE_KEY_FILE` / `SOPS_AGE_SSH_PRIVATE_KEY_CMD`; it does not use `SSH_AUTH_SOCK`. For Bitwarden or another vault SSH agent, use `age-plugin-sshagent` and its plugin-derived recipient. The plugin supports Ed25519 keys only. Verify the full SOPS/plugin/agent path locally before relying on it.
