import feedparser
from datetime import datetime, timezone
from dataclasses import dataclass

KEYWORDS = ["経済", "株価", "為替", "ビジネス", "金融"]
MAX_ARTICLES = 5

@dataclass
class Article:
    title: str
    summary: str
    url: str
    published: str


def _build_rss_url(keyword: str) -> str:
    return (
        f"https://news.google.com/rss/search"
        f"?q={keyword}&hl=ja&gl=JP&ceid=JP:ja"
    )


def _parse_entry(entry) -> Article:
    return Article(
        title=entry.get("title", ""),
        summary=entry.get("summary", ""),
        url=entry.get("link", ""),
        published=entry.get("published", ""),
    )


def fetch_articles() -> list[Article]:
    seen_titles: set[str] = set()
    articles: list[Article] = []

    for keyword in KEYWORDS:
        feed = feedparser.parse(_build_rss_url(keyword))
        for entry in feed.entries:
            title = entry.get("title", "")
            if title and title not in seen_titles:
                seen_titles.add(title)
                articles.append(_parse_entry(entry))
            if len(articles) >= MAX_ARTICLES * 3:
                break
        if len(articles) >= MAX_ARTICLES * 3:
            break

    return articles[:MAX_ARTICLES]
