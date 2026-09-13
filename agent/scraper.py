"""Web scraping utilities: fetch a page and extract structured data."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

DEFAULT_TIMEOUT = 15
DEFAULT_USER_AGENT = "reconversion-agents-ia-scraper/1.0"


@dataclass
class PageData:
    url: str
    status_code: int
    title: str | None
    meta_description: str | None
    headings: list[str]
    links: list[str]
    word_count: int
    text: str

    def to_dict(self) -> dict:
        return asdict(self)


class ScraperError(RuntimeError):
    """Raised when a page cannot be fetched or parsed."""


def fetch_page(url: str, timeout: int = DEFAULT_TIMEOUT) -> PageData:
    """Fetch a URL and extract title, meta description, headings, links and text."""
    headers = {"User-Agent": DEFAULT_USER_AGENT}
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
    except requests.RequestException as exc:
        raise ScraperError(f"Failed to fetch {url}: {exc}") from exc

    # Use the raw bytes so BeautifulSoup can detect the encoding itself (via
    # <meta charset> or a BOM); trusting response.text here falls back to
    # ISO-8859-1 whenever the server omits a charset, mangling accents.
    soup = BeautifulSoup(response.content, "lxml")

    title = soup.title.string.strip() if soup.title and soup.title.string else None

    meta_tag = soup.find("meta", attrs={"name": "description"})
    meta_description = meta_tag["content"].strip() if meta_tag and meta_tag.get("content") else None

    headings = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"]) if h.get_text(strip=True)]

    parsed_base = urlparse(url)
    links: list[str] = []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href or href.startswith("#") or href.startswith("javascript:"):
            continue
        absolute = urljoin(f"{parsed_base.scheme}://{parsed_base.netloc}", href)
        if absolute not in links:
            links.append(absolute)

    text = " ".join(soup.get_text(separator=" ", strip=True).split())

    return PageData(
        url=url,
        status_code=response.status_code,
        title=title,
        meta_description=meta_description,
        headings=headings,
        links=links,
        word_count=len(text.split()),
        text=text,
    )


def fetch_many(urls: list[str], timeout: int = DEFAULT_TIMEOUT) -> list[dict]:
    """Fetch multiple URLs, skipping ones that fail and recording the error instead."""
    results = []
    for url in urls:
        try:
            results.append(fetch_page(url, timeout=timeout).to_dict())
        except ScraperError as exc:
            results.append({"url": url, "error": str(exc)})
    return results
