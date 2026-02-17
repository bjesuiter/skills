---
name: openhue
description: Control JB's Philips Hue lights via OpenHue CLI
private: true
---

# OpenHue CLI - JB's Setup

**Bridge:** 192.168.204.47

## Rooms & Lights

| Room | Lights |
|------|--------|
| **Bad** | Bad Decke (Daylo), Spiegellicht |
| **Bennys Zimmer** | Benny Lightstrip, Filament Warm & Cold, Stecker Gelb - Piano, Strahler 1600 |
| **Benny Streaming** | GreenScreen LED Stripe (plug) |
| **Flur** | Flur vorne, Flur hinten (both color) |
| **Küche** | Lightstrip Küche, Strahler |
| **Schlafzimmer** | Edison Wohnzimmer, Color 1600 #2, Filament Edison Warm |
| **Wohnzimmer** | Wohnzimmer White 1600 |
| **Zimmer komplett** | Stecker Rot - Stern (plug) |

## Common Scenes
Each room has: Aktivieren, Konzentration, Entspannen, Gedimmt, Nachtlicht, Hell/Lesen

## Quick Commands
```bash
openhue get room --json              # List all rooms
openhue get light --json             # List all lights
openhue set light "Flur vorne" --on  # Turn on specific light
openhue set scene <scene-id>         # Activate scene
openhue set light <id> --off         # Turn off
openhue set light <id> --brightness 50 --on
```

See bundled openhue skill for full CLI reference.
