# Uses LangChain’s WikipediaLoader
# Searches Wikipedia for a query
# Downloads the top matching pages
# Converts them into LangChain Document objects
# Prints metadata and partial text
#  In short: Pull Wikipedia articles into LangChain for RAG or analysis

from langchain_community.document_loaders import WikipediaLoader
docs = WikipediaLoader(query="Kantara Kannada movie Collections", load_max_docs=2).load()
len(docs)
print(docs[0].metadata) # metadata of the first document
print(docs[0].page_content[:400])  # a part of the page content

# Test 2.
docs = WikipediaLoader(query="Whats elon musk current age ?", load_max_docs=10).load()
print(docs[0].page_content[:400])  # a part of the page content
