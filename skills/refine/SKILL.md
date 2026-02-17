# Refine Loop Skill

Autonomous research loop for enhancing openloop notes during the 00:00-04:00 window.

## Triggers

- `refine` — Start the autonomous refinement loop (runs for one Minimax cycle / 4 hours)
- `refine --note <slug>` — Refine a specific openloop note (default timeout: 20 min)
- `refine status` — Check current state without running
- `refine stop` — Gracefully halt any running loop

## Timing Window

**Allowed window:** 00:00 - 04:00 (one Minimax cycle)

- Outside this window: `refine` returns "Too early/late, come back between 00:00-04:00"
- Inside this window: Loop runs for 4 hours (until 04:00 max)
- **Single note refinement (`--note`):** Always allowed, no time gate

### Single Note Refinement

When targeting a specific note (`refine --note <slug>`):

1. **Load Note** — Fetch the specified openloop note
2. **Analyze** — Identify open questions and research needs
3. **Research** — Answer the primary question (one at a time)
4. **Update** — Add findings to the note
5. **Log** — Record action in `refinement-log.md`
6. **Complete** — Exit after one successful research cycle

**Default timeout:** 20 minutes (user can override)

## Loop Steps

1. **Select File** — Pick an openloop note needing refinement (skip if `last_refined` is today)
2. **Analyze** — Identify open questions not yet researched
3. **Research** — One question at a time (API search → search skill → browser fallback)
4. **Update** — Add findings to the note
5. **Mark Complete** — Set `last_refined: <ISO date>` in the note's frontmatter
6. **Log** — Record action in `refinement-log.md`
7. **Loop** — Return to step 1 or stop

## Rules

- **No duplicate refinement:** Skip notes with `last_refined` set to today's date
- **Track refinement:** Every refined note gets `last_refined: <ISO date>` in frontmatter

## Morning Summary

At the end of the loop (around 04:00), send JB a Telegram message with:

- **Which notes were refined** (list of note titles/slugs)
- **What new knowledge appeared** (summary of research findings added to each note)

---

**Anchor:** [[skill:refine]]
