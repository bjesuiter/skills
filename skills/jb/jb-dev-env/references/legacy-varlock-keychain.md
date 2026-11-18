# Legacy Varlock and macOS Keychain workflow

Use this reference only when maintaining or migrating a repo that already uses Varlock `keychain(...)` references. New JB desktop setups use the [SOPS/Bitwarden workflow](sops-age.md).

Varlock >= 1.9.0 has native `varlock keychain` commands. These create Keychain items with Varlock-compatible helper access. Use project/profile-scoped accounts and let Varlock write the reference:

```sh
varlock keychain set API_KEY --project <project-slug> --profile jb --write-to .env.jb
```

The reference has this shape:

```env
API_KEY=keychain(service="varlock", account="<project-slug>:jb:API_KEY")
```

For an existing plaintext env file, `varlock keychain import .env --project <project-slug> --profile jb --write-to .env.jb` imports values and writes resolver references. Use `--force` only for intentional overwrites. Remove plaintext secret files from git and history as needed. Keychain items may sync through iCloud Keychain when configured; otherwise recreate them on each Mac. Verify with `varlock load >/dev/null` and use `varlock keychain list <project-slug>` for metadata-only inspection.

Items created through `/usr/bin/security` may lack Varlock helper access. First try `varlock load`. If it reports a helper/access error, use `varlock keychain fix-access --account "<project-slug>:<profile>:KEY"` or `varlock keychain fix-access --path .env.jb`, then retry. A non-default Keychain may require `--keychain Login` or its actual name. Recreate through Varlock-native `set` or `import` when possible.

A temporary `exec("security find-generic-password -s varlock -a \"<project-slug>:<profile>:KEY\" -w")` bridge bypasses VarlockEnclave and invokes the shell. Replace it with a Varlock-native reference or migrate the repo to SOPS when feasible.
