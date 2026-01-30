# Convert one document into multiple smaller documents based on line breaks
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document

docs = [
    Document(page_content="""Headline one
Headline two
Headline three
Headline four""",
             metadata={"source": "cnn"})
]

splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=200,
    chunk_overlap=0
)

split_docs = splitter.split_documents(docs)

for i, doc in enumerate(split_docs, 1):
    print(f"\n--- Chunk {i} ---")
    print(doc.page_content)
    print("Metadata:", doc.metadata)
