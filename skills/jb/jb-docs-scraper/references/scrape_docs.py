#!/usr/bin/env python3
"""
Universal documentation scraper.

Scrapes documentation websites into local markdown files using crawl4ai.

Run with:
    uv run --with crawl4ai python scrape_docs.py <URL> [OPTIONS]

Examples:
    uv run --with crawl4ai python scrape_docs.py https://docs.example.com/api/v2/
    uv run --with crawl4ai python scrape_docs.py https://docs.example.com/api/v2/ --output ./my-docs
    uv run --with crawl4ai python scrape_docs.py https://docs.example.com/api/v2/ --max-pages 50 --max-depth 3

If Playwright browsers are missing:
    uv run --with crawl4ai playwright install
"""

import argparse
import asyncio
import re
import sys
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from crawl4ai import AsyncWebCrawler, CacheMode, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.deep_crawling.filters import DomainFilter, FilterChain, URLPatternFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape documentation websites into local markdown files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://mediasoup.org/documentation/v3/
  %(prog)s https://docs.rombo.co/tailwind --output ./tailwind-docs
  %(prog)s https://tanstack.com/start/latest/docs/ --max-pages 100
        """,
    )
    parser.add_argument(
        "url",
        help="Base URL of the documentation to scrape",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output directory (default: ./docs/<auto-detected-name>)",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=6,
        help="Maximum link depth to follow (default: 6)",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=500,
        help="Maximum pages to scrape (default: 500)",
    )
    parser.add_argument(
        "--url-pattern",
        type=str,
        default=None,
        help="URL pattern filter (glob style, e.g., '*docs/v2/*'). Auto-detected if not provided.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress verbose output",
    )
    return parser.parse_args()


def derive_config_from_url(url: str) -> dict:
    """
    Auto-detect configuration from the provided URL.

    Returns dict with: domain, url_pattern, path_prefix_regex, output_name
    """
    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path.rstrip("/")

    # Extract meaningful path segments for pattern matching
    # e.g., /documentation/v3/ -> *documentation/v3/*
    # e.g., /docs/api/v2/ -> *docs/api/v2/*
    if path:
        url_pattern = f"*{path}*"
        # Create regex to strip this prefix from file paths
        path_prefix_regex = rf"^{re.escape(path)}/?"
        # Use last meaningful segment for output name
        segments = [s for s in path.split("/") if s]
        output_name = (
            "_".join(segments[-2:])
            if len(segments) >= 2
            else (segments[-1] if segments else domain.replace(".", "_"))
        )
    else:
        url_pattern = f"*{domain}*"
        path_prefix_regex = r"^/?"
        output_name = domain.replace(".", "_")

    return {
        "domain": domain,
        "url_pattern": url_pattern,
        "path_prefix_regex": path_prefix_regex,
        "output_name": output_name,
    }


def normalize_file_name(source_url: str, path_prefix_regex: str) -> Path:
    """Convert a URL to a relative markdown file path."""
    parsed = urlparse(source_url)
    path = re.sub(path_prefix_regex, "", parsed.path)
    path = path.strip("/")
    if not path:
        path = "index"
    # Clean special characters, keep path structure
    cleaned = re.sub(r"[^a-zA-Z0-9/_-]", "_", path)
    return Path(f"{cleaned}.md")


def extract_markdown(result) -> Optional[str]:
    """Extract markdown content from a crawl result."""
    markdown = getattr(result, "markdown", None)
    if markdown is None:
        return None
    if isinstance(markdown, str):
        return markdown
    raw_markdown = getattr(markdown, "raw_markdown", None)
    if raw_markdown:
        return raw_markdown
    return getattr(markdown, "markdown", None)


async def run_scraper(
    base_url: str,
    output_dir: Path,
    max_depth: int,
    max_pages: int,
    domain: str,
    url_pattern: str,
    path_prefix_regex: str,
    verbose: bool,
) -> int:
    """Run the documentation scraper. Returns number of files written."""
    output_dir.mkdir(parents=True, exist_ok=True)
    base_prefix = base_url.rstrip("/")

    filter_chain = FilterChain(
        [
            DomainFilter(allowed_domains=[domain]),
            URLPatternFilter(patterns=[url_pattern]),
        ]
    )

    crawl_config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=max_depth,
            max_pages=max_pages,
            include_external=False,
            filter_chain=filter_chain,
        ),
        markdown_generator=DefaultMarkdownGenerator(content_source="cleaned_html"),
        cache_mode=CacheMode.BYPASS,
        stream=True,
        verbose=verbose,
    )

    written = set()

    try:
        async with AsyncWebCrawler() as crawler:
            async for result in await crawler.arun(url=base_url, config=crawl_config):
                url = getattr(result, "url", None)
                if not url:
                    continue
                if not url.startswith(base_prefix):
                    continue

                markdown = extract_markdown(result)
                if not markdown:
                    continue

                relative_path = normalize_file_name(url, path_prefix_regex)
                file_path = output_dir / relative_path
                if file_path in written:
                    continue

                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(markdown, encoding="utf-8")
                written.add(file_path)
                if verbose:
                    print(f"  -> {file_path}")
    except Exception as exc:
        message = str(exc)
        if "Playwright" in message or "playwright" in message:
            hint = (
                "Playwright browser binaries are missing. Run:\n"
                "  uv run --with crawl4ai playwright install"
            )
            print(f"ERROR: {hint}", file=sys.stderr)
            sys.exit(1)
        raise

    return len(written)


def main() -> None:
    args = parse_args()

    # Derive configuration from URL
    config = derive_config_from_url(args.url)

    # Use provided output or default to ./docs/<name>
    output_dir = args.output or Path("docs") / config["output_name"]

    # Use provided URL pattern or auto-detected one
    url_pattern = args.url_pattern or config["url_pattern"]

    verbose = not args.quiet

    if verbose:
        print(f"Scraping: {args.url}")
        print(f"Domain: {config['domain']}")
        print(f"URL Pattern: {url_pattern}")
        print(f"Output: {output_dir}")
        print(f"Max Depth: {args.max_depth}, Max Pages: {args.max_pages}")
        print("-" * 50)

    count = asyncio.run(
        run_scraper(
            base_url=args.url,
            output_dir=output_dir,
            max_depth=args.max_depth,
            max_pages=args.max_pages,
            domain=config["domain"],
            url_pattern=url_pattern,
            path_prefix_regex=config["path_prefix_regex"],
            verbose=verbose,
        )
    )

    if not args.quiet:
        print(f"\nWrote {count} markdown files to {output_dir}")


if __name__ == "__main__":
    main()
