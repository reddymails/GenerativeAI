# This script scrapes CNN content and prepares it as
# small LangChain document chunks, ready for embeddings and semantic search.
#     This program:
#     Downloads CNN’s homepage
#     Extracts readable text (headlines + paragraphs)
#     Converts it into a LangChain Document
#     Splits the text into small chunks using RecursiveCharacterTextSplitter
#     Prints a few chunks
#     👉 In short: Scrape → Clean → Document → Chunk
#

import requests
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# -----------------------------
# Step 1: Fetch CNN homepage
# -----------------------------
url = "https://www.cnn.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")

# -----------------------------
# Step 2: Extract readable text
# (headlines + paragraphs)
# -----------------------------
texts = []

for tag in soup.find_all(["h1", "h2", "p"]):
    text = tag.get_text(strip=True)
    if text:
        texts.append(text)

full_text = "\n".join(texts)

print(f"Total characters scraped: {len(full_text)}")

# -----------------------------
# Step 3: Create LangChain Document
# -----------------------------
doc = Document(
    page_content=full_text,
    metadata={"source": "cnn.com"}
)

# -----------------------------
# Step 4: RecursiveCharacterTextSplitter
# -----------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=0,
    separators=["\n\n", "\n", " ", ""]
)

chunks = splitter.split_documents([doc])

# -----------------------------
# Step 5: Print chunks We are printing top 5.
# -----------------------------
for i, chunk in enumerate(chunks[:5], 1):
    print(f"\n--- Chunk {i} ---")
    print(chunk.page_content)
