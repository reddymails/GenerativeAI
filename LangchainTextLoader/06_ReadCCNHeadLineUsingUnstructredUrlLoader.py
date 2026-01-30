# This Python program downloads CNN’s homepage and prints
# all headline-style text found inside HTML heading tags (h1, h2, h3).
#  In short: A basic web scraper to extract CNN headlines

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get("https://www.cnn.com", headers=headers, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")

print("CNN H1 Headers:\n")

count = 0
for tag in ["h1", "h2", "h3"]:
    for h in soup.find_all(tag):
        text = h.get_text(strip=True)
        if text:
            print(f"{tag.upper()}: {text}")

if count == 0:
    print("No H1 tags found (CNN may use H2/H3 instead)")
