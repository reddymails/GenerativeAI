import pandas as pd
from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import SentenceTransformersTokenTextSplitter
from langchain_community.vectorstores import FAISS

# -------------------------------
# Load CSV
# -------------------------------
df = pd.read_csv("../sample_text_category.csv").dropna(subset=["text"])

# -------------------------------
# Embedding model (FAISS-optimized)
# -------------------------------
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    encode_kwargs={"normalize_embeddings": True}
)

# -------------------------------
# Token-aware text splitter
# -------------------------------
splitter = SentenceTransformersTokenTextSplitter(
    chunk_size=200,
    chunk_overlap=20
)

# -------------------------------
# Prepare texts & metadata
# -------------------------------
texts = []
metadata = []

for idx, row in df.iterrows():
    chunks = splitter.split_text(row["text"])
    for chunk in chunks:
        texts.append(chunk)
        metadata.append({
            "row_id": idx,
            "category": row.get("category", "unknown")
        })

print(f"✂️ Chunks created: {len(texts):,}")

# -------------------------------
# Create FAISS vector store
# -------------------------------
faiss_db = FAISS.from_texts(
    texts=texts,
    embedding=embedding_model,
    metadatas=metadata
)

print("✅ FAISS index created")

# -------------------------------
# Persist FAISS index
# -------------------------------
FAISS_DIR = "faiss_index"

faiss_db.save_local(FAISS_DIR)

print(f"💾 FAISS index saved to: {FAISS_DIR}")
