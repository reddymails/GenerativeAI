import requests
from bs4 import BeautifulSoup

# ✅ DEFINE HEADERS HERE
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

# ============================================================
# SCRAPER: READ <a> TAGS (HEADLINES)
# ============================================================
def fetch_anchor_news(source, url, max_items=20):
    articles = []

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        for a in soup.find_all("a", href=True):
            text = a.get_text(strip=True)
            link = a["href"]

            if not text or len(text) < 40:
                continue

            if link.startswith("/"):
                link = url.rstrip("/") + link

            articles.append({
                "text": text,
                "url": link,
                "source": source
            })

            if len(articles) >= max_items:
                break

    except Exception as e:
        print(f"❌ {source}: {e}")

    return articles

