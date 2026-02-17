# OpenClaw LinuxServer Findings (from `openclaw-linuxserver/docs`)

Source document used: `docs/Creating a LinuxServer.io Image for Openclaw.md`

## Intent

- Build an LSIO-style image for OpenClaw to simplify self-hosted deployment.
- Keep compatibility high while supporting Raspberry Pi and standard x86 hosts.
- Prefer maintainable structure over one-off Dockerfiles.

## Recommended direction from research

- Use LinuxServer base images (`ghcr.io/linuxserver/baseimage-alpine` and/or `...-ubuntu`).
- Support both variants:
  - Alpine for small footprint.
  - Ubuntu for wider package/runtime compatibility.
- Use LSIO-style init/service flow with `s6-overlay`.

## Structure suggested in the notes

- `root/etc/s6-overlay/s6-rc.d/init-<app>/run` for pre-start setup (`/config`, ownership, prep).
- `root/etc/s6-overlay/s6-rc.d/svc-<app>/run` for long-running service command.
- Keep scaffold reusable for both alpine + ubuntu via shared `root/` and separate Dockerfiles.
- Use `docker-bake.hcl` for dual-base, multi-arch builds.

## Links captured in the notes

- LSIO blog: https://www.linuxserver.io/blog/how-is-container-formed
- LSIO base Alpine: https://github.com/linuxserver/docker-baseimage-alpine
- LSIO base Ubuntu: https://github.com/linuxserver/docker-baseimage-ubuntu
- LSIO docker actions: https://github.com/linuxserver-labs/docker-actions
- LSIO CI reference: https://github.com/linuxserver/docker-ci
- Node service reference image: https://github.com/linuxserver/docker-node-red
- Browser dependency reference image: https://github.com/linuxserver/docker-browserless
- LSIO branding: https://docs.linuxserver.io/general/container-branding/
- Container customization: https://docs.linuxserver.io/general/container-customization/

## Practical guidance for this skill

- Scaffold both Dockerfiles by default unless user explicitly requests one base.
- Keep all app-specific logic as TODO placeholders so the scaffold is generic.
- Always include `/config` volume and PUID/PGID ownership prep pattern.
