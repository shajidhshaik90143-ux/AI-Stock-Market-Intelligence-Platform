import feedparser
from urllib.parse import quote


def get_news(ticker, limit=15):
    """Fetch latest Google News RSS articles for a given stock ticker."""
    if not ticker:
        return []

    ticker = ticker.strip().upper()
    query = quote(f"{ticker} stock market")
    url = (
        "https://news.google.com/rss/search?"
        f"q={query}&hl=en-US&gl=US&ceid=US:en"
    )

    try:
        feed = feedparser.parse(url)
        articles = []

        for entry in feed.entries[:limit]:
            articles.append({
                "title": entry.get("title", "No title"),
                "link": entry.get("link", ""),
                "published": entry.get("published", "Unknown"),
                "summary": entry.get("summary", "")
            })

        return articles
    except Exception:
        return []


def search_news(query, limit=15):
    """Search Google News RSS articles by arbitrary query keyword."""
    if not query:
        return []

    query = query.strip()
    encoded_query = quote(query)
    url = (
        "https://news.google.com/rss/search?"
        f"q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    )

    try:
        feed = feedparser.parse(url)
        results = []

        for entry in feed.entries[:limit]:
            results.append({
                "title": entry.get("title", "No title"),
                "link": entry.get("link", ""),
                "published": entry.get("published", "Unknown"),
                "summary": entry.get("summary", "")
            })

        return results
    except Exception:
        return []


def format_news_for_ai(articles):
    """Formats a list of news dictionaries into clean text for AI prompts."""
    if not articles:
        return "No news available."

    output = []
    for article in articles:
        output.append(
            f"Title: {article.get('title')}\n"
            f"Published: {article.get('published')}\n"
            f"Summary: {article.get('summary')}\n"
        )

    return "\n---\n".join(output)