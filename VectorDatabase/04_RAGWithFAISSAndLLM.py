"""
News RAG Pipeline

News Sites
   ↓ (BeautifulSoup: <a> tags)
Anchor Text + URL
   ↓
Sentence Transformer Embeddings
   ↓
FAISS Vector Index
   ↓
Retriever
   ↓
OpenAI LLM
   ↓
Grounded Answer
"""



# LangChain (1.2.6 compatible)
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from Method2FetchNewsByReadingHTMLAnchors import fetch_anchor_news


load_dotenv(r"C:\Rama\Learn\AI\.env")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not loaded")


# ============================================================
# HTTP HEADERS (USED BY SCRAPER)
# ============================================================
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}



# ============================================================
# NEWS SOURCES
# ============================================================
news_channels = {
    "CNN": "https://www.cnn.com",
    "Criciinof": "https://www.cricinfo.com",
    "Kansas" : "https://kusports.com",
    "BBC": "https://www.bbc.com",
    "NDTV": "https://www.ndtv.com",
    "Times of India": "https://www.timesofindia.com",
    "MoneyControl": "https://www.moneycontrol.com"
}


# ============================================================
# COLLECT NEWS
# ============================================================
all_articles = []

for name, url in news_channels.items():
    items = fetch_anchor_news(name, url)
    all_articles.extend(items)

if not all_articles:
    raise RuntimeError("❌ No news articles collected. Check scraping logic.")

print(f"📰 Collected {len(all_articles)} news snippets")


# ============================================================
# EMBEDDINGS
# ============================================================
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    encode_kwargs={"normalize_embeddings": True}
)

texts = [a["text"] for a in all_articles]
metadatas = [
    {"source": a["source"], "url": a["url"]}
    for a in all_articles
]


# ============================================================
# FAISS: LOAD OR CREATE
# ============================================================
INDEX_DIR = "news_faiss_index"

if os.path.exists(INDEX_DIR):
    faiss_db = FAISS.load_local(
        INDEX_DIR,
        embedding_model,
        allow_dangerous_deserialization=True
    )
    print("✅ FAISS index loaded")
else:
    faiss_db = FAISS.from_texts(
        texts=texts,
        embedding=embedding_model,
        metadatas=metadatas
    )
    faiss_db.save_local(INDEX_DIR)
    print("✅ FAISS index created and saved")


# ============================================================
# RETRIEVER
# ============================================================
retriever = faiss_db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)


# ============================================================
# LLM
# ============================================================
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# ============================================================
# PROMPT
# ============================================================
prompt = ChatPromptTemplate.from_template("""
You are a news assistant.
Answer the question using ONLY the provided news snippets.
If the answer is not present, say:
"I could not find this in the current news."

Context:
{context}

Question:
{question}

Answer in bullet points.
Mention the source name for each bullet.
""")


# ============================================================
# LCEL RAG PIPELINE (NO DEPRECATED APIs)
# ============================================================
def format_docs(docs):
    return "\n\n".join(
        f"[{d.metadata.get('source', 'Unknown')}] {d.page_content}"
        for d in docs
    )

rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)


# ============================================================
# QUERY
# ============================================================
#query = "What is happening with silver prices?"
#query = "Bangladesh Cricket news"
query = "Basketball news"
answer = rag_chain.invoke(query)

print("\n🧠 Answer:\n")
print(answer)


# ============================================================
# DEBUG: SHOW SOURCES
# ============================================================
print("\n📚 Retrieved Sources:\n")
docs = retriever.invoke(query)
for doc in docs:
    print(f"- {doc.metadata['source']} → {doc.metadata['url']}")
