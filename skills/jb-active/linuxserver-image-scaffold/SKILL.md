---
name: linuxserver-image-scaffold
description: Scaffold a new LinuxServer.io-style Docker image project in a new or existing folder. Use when asked to create/bootstrap a linuxserver.io image repo (Alpine, Ubuntu, or both), including LSIO-style root/ s6-overlay service structure, Dockerfiles, docker-bake.hcl, and starter CI files.
---

# LinuxServer.io Image Scaffold

Scaffold LinuxServer.io-style image repositories with repeatable structure.

## Use this skill by default workflow

1. Confirm target path and whether folder is new or existing.
2. Confirm base variant: `alpine`, `ubuntu`, or `both`.
3. Run scaffold script:
   - `bash scripts/scaffold-linuxserver-image.sh --name <image-name> --path <target-path> --base <alpine|ubuntu|both>`
4. Verify generated files and show next steps.
5. If repo already contains files, scaffold into that folder without deleting existing content.

## Command

```bash
bash scripts/scaffold-linuxserver-image.sh \
  --name <image-name> \
  --path <target-path> \
  --base <alpine|ubuntu|both>
```

### Behavior

- Create folder if missing.
- Reuse existing folder if present.
- Generate LSIO-style `root/` + s6 service stubs.
- Generate Dockerfiles for selected base(s).
- Generate `docker-bake.hcl` and starter GitHub Actions workflow.
- Keep existing files unless they conflict with generated scaffold paths.

## After scaffolding

1. Replace placeholder labels and maintainer fields.
2. Fill app-specific install/runtime in Dockerfile(s).
3. Edit `root/etc/s6-overlay/s6-rc.d/svc-<name>/run` start command.
4. Add project-specific ports/env vars in compose examples.
5. Build test:
   - `docker build -f Dockerfile.alpine .` (or ubuntu)

## References

Read these when making decisions:

- `references/openclaw-linuxserver-findings.md` (project context from JB's OpenClaw LSIO research)
- `references/linuxserver-image-basics.md` (LSIO image model, structure, and links)
