# LinuxServer.io Image Basics

This reference summarizes how LSIO-style images are typically organized.

## Core model

LSIO images are conventionally built around:

1. LinuxServer baseimage (Alpine or Ubuntu)
2. `s6-overlay` process supervision
3. standard `/config` persistence
4. PUID/PGID permission model for host-safe file ownership

## Typical repository layout

```text
.
├── Dockerfile.alpine
├── Dockerfile.ubuntu
├── docker-bake.hcl
├── root/
│   └── etc/s6-overlay/s6-rc.d/
│       ├── init-<app>/
│       │   ├── run
│       │   └── type        # oneshot
│       ├── svc-<app>/
│       │   ├── run
│       │   └── type        # longrun
│       └── user/contents.d/
│           ├── init-<app>
│           └── svc-<app>
└── .github/workflows/build.yml
```

## Base image choices

- Alpine: `ghcr.io/linuxserver/baseimage-alpine:<tag>`
- Ubuntu: `ghcr.io/linuxserver/baseimage-ubuntu:<tag>`

Use both when maintainers want size + compatibility options.

## s6 pieces you usually define

- `init-<app>/run` (`oneshot`):
  - setup folders
  - migrate config
  - set ownership (`abc:abc`), if required
- `svc-<app>/run` (`longrun`):
  - executes the main app process with `exec ...`

## Build strategy

- Use `docker-bake.hcl` to define alpine + ubuntu targets.
- Build multi-arch (`linux/amd64`, `linux/arm64`) for general compatibility.
- Add CI workflow to run at least `docker buildx bake --print` or full build/push.

## Common maintainer decisions

- whether to support both bases or one
- how much app bootstrap happens in image build vs init script
- runtime env vars and exposed ports
- optional extras (mods, custom scripts, package install hooks)

## Official docs and references

- LSIO image formation blog: https://www.linuxserver.io/blog/how-is-container-formed
- Container customization: https://docs.linuxserver.io/general/container-customization/
- Container branding: https://docs.linuxserver.io/general/container-branding/
- Baseimage Alpine: https://github.com/linuxserver/docker-baseimage-alpine
- Baseimage Ubuntu: https://github.com/linuxserver/docker-baseimage-ubuntu
- Docker actions: https://github.com/linuxserver-labs/docker-actions
