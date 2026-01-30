from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    encode_kwargs={"normalize_embeddings": True}
)

faiss_db = FAISS.load_local(
    "faiss_index",
    embedding_model,
    allow_dangerous_deserialization=True
)

print("✅ FAISS index loaded")
print(faiss_db)

#query = "How do I store embeddings efficiently?"
query = "I want to buy a polo t-shirt"
#query ="How about some vacation"

results = faiss_db.similarity_search_with_score(
    query,
    k=3
)

for doc, score in results:
    print(f"\nScore: {score:.4f}")
    print(f"Category: {doc.metadata.get('category')}")
    print(doc.page_content[:200])