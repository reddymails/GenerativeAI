# This Python program scrapes top headlines from multiple news websites by:
#     Sending HTTP requests to each site
#     Parsing the HTML with BeautifulSoup
#     Extracting text from heading tags (h1, h2, h3)
#     Printing a short list of unique headlines per site
#      In short: A lightweight multi-site news headline scraper

import requests
from bs4 import BeautifulSoup

news_channels = {
    "CNN": "https://www.cnn.com",
    "BBC": "https://www.bbc.com",
    "Reuters": "https://www.cricinfo.com",
    "Times of India": "https://www.timesofindia.com",
    "NDTV" : "https://www.ndtv.com"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

def fetch_headers(name, url, max_items=8):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        headlines = []
        for tag in ["h1", "h2", "h3"]:
            for h in soup.find_all(tag):
                text = h.get_text(strip=True)
                if text and text not in headlines:
                    headlines.append(text)
                if len(headlines) >= max_items:
                    return headlines

        return headlines

    except Exception as e:
        return [f"ERROR: {e}"]

print("\n=== NEWS HEADLINES ===\n")

for channel, url in news_channels.items():
    print(f"\n📰 {channel}" + " Url="+ url)
    print("-" * (len(channel) + 4))

    headlines = fetch_headers(channel, url)

    for i, headline in enumerate(headlines, 1):
        print(f"{i}. {headline}")
