---
name: summarize
description: Use the summarize CLI when the user asks to summarize or extract content from URLs, local files, PDFs, images, audio, video, or YouTube.
---

# Summarize

Use `summarize` to extract or summarize web and local content.

## Workflow

1. Confirm the input is a URL or an accessible local path.
2. Run `summarize <input>` with the configured/default model.
3. Add only the controls needed for the requested output.
4. Return the summary or extracted content, noting any retrieval limitation.

```bash
summarize "https://example.com"
summarize "/path/to/document.pdf"
summarize "https://youtu.be/VIDEO_ID" --youtube auto
```

Do not select or recommend a specific model unless the user requests one. If they do, inspect the installed CLI for currently supported model syntax before passing `--model`.

## Output controls

- Use `--length short|medium|long|xl|xxl|<chars>` to control summary size.
- Use `--max-output-tokens <count>` for a hard output-token limit.
- Use `--extract-only` to retrieve URL content without summarizing it.
- Use `--json` when structured, machine-readable output is useful.

```bash
summarize "https://example.com" --length short
summarize "/path/to/document.pdf" --max-output-tokens 1200 --json
summarize "https://example.com" --extract-only
```

## Authentication and extraction

Ensure the API key required by the configured model provider is available in the environment. Do not print or expose keys.

For difficult or blocked pages, use the optional extraction service only when configured:

- Set `FIRECRAWL_API_KEY`, then use `--firecrawl auto|off|always`.
- Set `APIFY_API_TOKEN` when YouTube processing needs the Apify fallback.

## Live discovery

Treat installed CLI help as authoritative because flags, providers, and models can change:

```bash
summarize --help
summarize --help | rg -i 'model|provider|extract|youtube|firecrawl'
```
