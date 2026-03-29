---
name: jb-markit
description: Convert files, URLs, stdin, images, audio, and archives to markdown with the markit CLI. Use when the user wants PDFs, Office docs, webpages, feeds, spreadsheets, JSON/YAML, or media turned into markdown, or needs raw/JSON extraction for agents.
homepage: https://github.com/Michaelliv/markit
metadata: {"clawdbot":{"emoji":"📝","requires":{"bins":["markit"]},"install":[{"id":"bun","kind":"bun","package":"markit-ai","bins":["markit"],"label":"Install markit (bun)"}]}}
---

# jb-markit

Use `markit` to convert almost anything into markdown.

## Install

```bash
bun add -g markit-ai
```

## Best modes for agents

- `markit <source> -q` → raw markdown only
- `markit <source> --json` → structured output for parsing
- `markit <source> -o output.md` → write markdown to a file
- `cat file.pdf | markit -` → read from stdin

## Quick start

```bash
# Documents
markit report.pdf
markit document.docx
markit slides.pptx
markit data.xlsx

# Web
markit https://example.com/article
markit https://en.wikipedia.org/wiki/Markdown

# Data / config
markit data.csv
markit config.json
markit schema.yaml

# Raw markdown or JSON
markit report.pdf -q
markit report.pdf --json

# Save output
markit report.pdf -o report.md
```

## Media + AI

Images and audio include metadata extraction by default. AI descriptions/transcriptions require an API key.

```bash
# OpenAI (default)
export OPENAI_API_KEY=sk-...
markit photo.jpg
markit recording.mp3

# Anthropic
markit config set llm.provider anthropic
export ANTHROPIC_API_KEY=sk-ant-...
markit photo.jpg

# Focus the extraction
markit receipt.jpg -p "List all line items with prices as a table"
markit whiteboard.jpg -p "Extract all text verbatim"
markit diagram.png -p "Describe the architecture and data flow"
```

## Common formats

`markit` supports PDFs, DOCX, PPTX, XLSX, HTML, EPUB, Jupyter notebooks, RSS/Atom, CSV/TSV, JSON, YAML, XML/SVG, plain text, many code files, images, audio, ZIP archives, and URLs.

Use `markit formats` to see what the installed version supports.

## Config

```bash
markit init
markit config show
markit config get llm.model
markit config set llm.provider anthropic
markit config set llm.apiBase http://localhost:11434/v1
```

Config file: `.markit/config.json`

Env vars override config. Common keys:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `MARKIT_API_KEY`

## Plugins

```bash
markit plugin install npm:markit-plugin-dwg
markit plugin install git:github.com/user/markit-plugin-ocr
markit plugin install ./my-plugin.ts
markit plugin list
markit plugin remove dwg
```

Plugin converters run before built-ins, so plugins can add new formats or override existing converters.

## Good defaults

- Prefer `-q` when you want clean markdown in pipelines.
- Prefer `--json` when another tool or agent will parse the result.
- Use `-p` to constrain image/audio extraction to the exact task.
- Use `-o` when the conversion should become a durable artifact in the repo.
