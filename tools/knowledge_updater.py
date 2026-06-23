# -*- coding: utf-8 -*-
"""knowledge_updater.py ? self-improving crawler for the Content Creator Legal Risk Analyzer.

Pipeline:
  1. Fetch authoritative sources and arXiv cs.CY papers.
  2. Parse title, authors, date, DOI/URL, abstract.
  3. Score each entry: recency ? domain-keyword relevance.
  4. Deduplicate by URL/DOI SHA-256 hash.
  5. Append dated, cited blocks to SECOND-KNOWLEDGE-BRAIN.md.

Run weekly via cron or Task Scheduler.
"""
from __future__ import annotations

import argparse
import hashlib
import logging
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Iterable, List, Optional

logger = logging.getLogger("knowledge_updater")

DEFAULT_BRAIN = Path(__file__).resolve().parents[1] / "SECOND-KNOWLEDGE-BRAIN.md"

ARXIV_CATEGORIES = ["cs.CY"]
SEARCH_QUERIES = [
    "copyright fair use creator",
    "content id music licensing",
    "right of publicity likeness",
]
SOURCE_URLS = [
    "https://www.copyright.gov",
    "https://creativecommons.org",
    "https://www.wipo.int",
    "https://www.eff.org",
]
DOMAIN_KEYWORDS = [
    "copyright",
    "fair use",
    "creator",
    "content id",
    "music licensing",
    "publicity",
    "likeness",
    "trademark",
    "dmca",
    "creative commons",
]

SEED_ENTRIES = [
    {
        "title": "U.S. Copyright Office Fair Use Index",
        "url": "https://www.copyright.gov/fair-use/",
        "authors": "U.S. Copyright Office",
        "year": 2024,
        "abstract": (
            "Official fair-use case index and the four-factor test: purpose and character of use, "
            "nature of the copyrighted work, amount and substantiality used, and effect on the market."
        ),
    },
    {
        "title": "Creative Commons License Types",
        "url": "https://creativecommons.org/share-your-work/cclicenses/",
        "authors": "Creative Commons",
        "year": 2024,
        "abstract": (
            "Reference for CC0, BY, BY-SA, BY-NC, BY-ND, and BY-NC-SA license compatibility and reuse terms."
        ),
    },
    {
        "title": "WIPO Copyright",
        "url": "https://www.wipo.int/copyright/en/",
        "authors": "World Intellectual Property Organization",
        "year": 2024,
        "abstract": (
            "Global copyright overview, treaties (Berne, WCT), and cross-border enforcement guidance for creators."
        ),
    },
    {
        "title": "EFF Guide to YouTube Content ID",
        "url": "https://www.eff.org/issues/intellectual-property",
        "authors": "Electronic Frontier Foundation",
        "year": 2024,
        "abstract": (
            "Advocacy and analysis of DMCA takedowns, Content ID, and platform enforcement affecting creators."
        ),
    },
    {
        "title": "DMCA Section 512 Takedown Overview",
        "url": "https://www.copyright.gov/dmca/",
        "authors": "U.S. Copyright Office",
        "year": 2024,
        "abstract": (
            "Statutory framework for notice-and-takedown, counter-notice, and safe-harbor limits."
        ),
    },
]


@dataclass
class Config:
    brain: Path = DEFAULT_BRAIN
    dry_run: bool = False
    max_arxiv: int = 20
    queries: List[str] = field(default_factory=lambda: list(SEARCH_QUERIES))
    seed_only: bool = False


def _hash(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]


def _http_get(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
            )
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _crawl4ai_fetch(url: str) -> Optional[str]:
    try:
        from crawl4ai import AsyncWebCrawler
    except Exception as exc:
        logger.debug("crawl4ai not available: %s", exc)
        return None
    try:
        import asyncio

        async def _run() -> str:
            async with AsyncWebCrawler() as crawler:
                result = await crawler.arun(url=url)
                return getattr(result, "markdown", "") or getattr(result, "html", "")

        return asyncio.run(_run())
    except Exception as exc:
        logger.warning("crawl4ai fetch failed for %s: %s", url, exc)
        return None


def fetch_url(url: str) -> str:
    """Fetch a URL, preferring crawl4ai when installed, falling back to urllib."""
    text = _crawl4ai_fetch(url)
    if text:
        return text
    try:
        return _http_get(url)
    except urllib.error.URLError as exc:
        logger.warning("urllib fetch failed for %s: %s", url, exc)
        raise


def _extract_title(html: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    return re.sub(r"\s+", " ", m.group(1).strip()) if m else ""


def _extract_paragraph(html: str) -> str:
    m = re.search(r"<p[^>]*>(.*?)</p>", html, re.IGNORECASE | re.DOTALL)
    if not m:
        return html[:500]
    txt = re.sub(r"<[^>]+>", " ", m.group(1))
    return re.sub(r"\s+", " ", txt).strip()[:500]


def parse_arxiv_atom(xml_text: str) -> List[dict]:
    """Parse arXiv Atom API results into candidate entries."""
    entries: List[dict] = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        logger.warning("Failed to parse arXiv Atom: %s", exc)
        return entries
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    for entry in root.findall("atom:entry", ns):
        title_elem = entry.find("atom:title", ns)
        title = (title_elem.text or "").strip() if title_elem is not None else ""
        summary_elem = entry.find("atom:summary", ns)
        abstract = (summary_elem.text or "").strip() if summary_elem is not None else ""
        link_elem = entry.find("atom:link[@rel='alternate']", ns)
        href = link_elem.get("href", "") if link_elem is not None else ""
        authors = [
            name.text
            for name in entry.findall("atom:author/atom:name", ns)
            if name.text
        ]
        published_elem = entry.find("atom:published", ns)
        year = 0
        if published_elem is not None and published_elem.text:
            m = re.search(r"\d{4}", published_elem.text)
            year = int(m.group(0)) if m else 0
        if href:
            entries.append({
                "title": title or f"arXiv:{href.split('/')[-1]}",
                "url": href,
                "authors": ", ".join(authors),
                "year": year,
                "abstract": abstract,
            })
    return entries


def fetch_arxiv(config: Config) -> List[dict]:
    """Query the arXiv Atom API for recent cs.CY papers matching domain terms."""
    if not config.queries:
        return []
    terms = " OR ".join(config.queries)
    encoded = urllib.parse.quote(terms)
    url = (
        f"http://export.arxiv.org/api/query?search_query=cat:cs.CY+AND+({encoded})"
        f"&start=0&max_results={config.max_arxiv}&sortBy=submittedDate&sortOrder=descending"
    )
    try:
        xml = fetch_url(url)
    except urllib.error.URLError as exc:
        logger.warning("arXiv API unreachable: %s", exc)
        return []
    return parse_arxiv_atom(xml)


def fetch_sources() -> List[dict]:
    """Fetch landing pages from authoritative sources."""
    entries: List[dict] = []
    for url in SOURCE_URLS:
        try:
            text = fetch_url(url)
            title = _extract_title(text) or url
            abstract = _extract_paragraph(text)
            entries.append({
                "title": f"Source scan: {title}",
                "url": url,
                "authors": "",
                "year": date.today().year,
                "abstract": abstract,
            })
        except Exception as exc:
            logger.warning("Source scan failed for %s: %s", url, exc)
    return entries


def fetch_entries(config: Config) -> List[dict]:
    """Gather candidate entries from all configured sources."""
    entries: List[dict] = []
    try:
        entries.extend(fetch_arxiv(config))
    except Exception as exc:
        logger.warning("arXiv fetch failed gracefully: %s", exc)
    try:
        entries.extend(fetch_sources())
    except Exception as exc:
        logger.warning("Source scan failed gracefully: %s", exc)
    return entries


def relevance_score(entry: dict) -> float:
    """Score = recency (0-1) ? keyword relevance (0-1)."""
    try:
        year = int(entry.get("year", 0))
    except (TypeError, ValueError):
        year = 0
    now = date.today().year
    recency = max(0.0, 1.0 - (now - year) / 8.0) if year else 0.3
    text = (entry.get("title", "") + " " + entry.get("abstract", "")).lower()
    hits = sum(1 for kw in DOMAIN_KEYWORDS if kw in text)
    rel = min(1.0, hits / max(1, len(DOMAIN_KEYWORDS)))
    return round(recency * (0.4 + 0.6 * rel), 3)


def load_seen_hashes(brain: Path) -> set:
    if not brain.exists():
        return set()
    text = brain.read_text(encoding="utf-8")
    return set(re.findall(r"<!--hash:([0-9a-f]{16})--", text))


def append_entries(
    entries: Iterable[dict],
    brain: Path,
    dry_run: bool = False,
) -> int:
    """Append new, deduplicated, dated, cited entries to the knowledge base."""
    seen = load_seen_hashes(brain)
    scored = sorted(
        ((relevance_score(e), e) for e in entries),
        reverse=True,
        key=lambda x: x[0],
    )
    today = date.today().isoformat()
    new_blocks: List[str] = []
    for score, e in scored:
        url = e.get("url", "")
        if not url:
            continue
        h = _hash(url)
        if h in seen:
            continue
        seen.add(h)
        abstract = (e.get("abstract") or "(abstract pending)")[:280]
        title = e.get('title', 'Untitled')
        authors = e.get('authors', 'n/a')
        year = e.get('year', 'n/a')
        block = f"""### [{today}] {title}
- Authors: {authors}
- Year: {year}
- Link: {url}
- Relevance score: {score}
- Key findings: {abstract}
<!--hash:{h}-->
"""
        new_blocks.append(block)
    if not new_blocks:
        logger.info("No new entries to append.")
        return 0
    if dry_run:
        logger.info("Dry-run: would append %d entries.", len(new_blocks))
        return len(new_blocks)
    brain.parent.mkdir(parents=True, exist_ok=True)
    with brain.open("a", encoding="utf-8") as f:
        f.write(f"\n\n## Automated Crawl Batch ? {today}\n\n")
        f.write("\n".join(new_blocks))
    logger.info("Appended %d new entries.", len(new_blocks))
    return len(new_blocks)


def run(config: Config) -> int:
    if config.seed_only:
        return append_entries(SEED_ENTRIES, config.brain, dry_run=config.dry_run)
    entries = fetch_entries(config)
    return append_entries(entries, config.brain, dry_run=config.dry_run)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Refresh the SECOND-KNOWLEDGE-BRAIN.md knowledge base."
    )
    p.add_argument(
        "--brain",
        type=Path,
        default=DEFAULT_BRAIN,
        help="Path to SECOND-KNOWLEDGE-BRAIN.md",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Score and report without writing to the knowledge base.",
    )
    p.add_argument(
        "--seed",
        action="store_true",
        dest="seed_only",
        help="Append curated seed entries without crawling the network.",
    )
    p.add_argument(
        "--max-arxiv",
        type=int,
        default=20,
        help="Maximum arXiv entries to fetch per run.",
    )
    p.add_argument(
        "--queries",
        nargs="+",
        default=list(SEARCH_QUERIES),
        help="Search queries for scoring relevance.",
    )
    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
    )
    config = Config(
        brain=args.brain,
        dry_run=args.dry_run,
        max_arxiv=args.max_arxiv,
        queries=args.queries,
        seed_only=args.seed_only,
    )
    count = run(config)
    print(f"[knowledge_updater] appended {count} entries to {config.brain}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
