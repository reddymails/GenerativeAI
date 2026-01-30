#########################################################################
# Run with:
# streamlit run C:\Rama\Learn\GenerativeAI\Z_FinalProject\StocksNewsAnalyzer.py
# Once launched  type in questions like
#  "Print top 10 stocks"
#  what's the price of Jubilant Pharma
#  TOP gainers.
#########################################################################

import os
import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_classic.chains.qa_with_sources.retrieval import (
    RetrievalQAWithSourcesChain
)

# --------------------------------------------------------
# Load Environment Variables
# --------------------------------------------------------

load_dotenv(r"C:\Rama\Learn\AI\.env")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not found in .env file")

# --------------------------------------------------------
# Streamlit UI
# --------------------------------------------------------

st.set_page_config(page_title="News Research Tool", layout="wide")
st.title("📰 News Research Tool (RAG App)")

st.sidebar.title("Enter News Article URLs")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    if url:
        urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")

main_placeholder = st.empty()

FAISS_INDEX_PATH = "faiss_index"

# --------------------------------------------------------
# Create LLM
# --------------------------------------------------------

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# --------------------------------------------------------
# Process URLs -> Build Vector Store
# --------------------------------------------------------

if process_url_clicked and urls:

    main_placeholder.text("Loading data...")
    loader = UnstructuredURLLoader(urls=urls)
    data = loader.load()
    main_placeholder.text("Loading data... ☑ Completed")

    # Split text
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", ","],
        chunk_size=1000,
        chunk_overlap=200
    )

    main_placeholder.text("Splitting text...")
    docs = splitter.split_documents(data)
    main_placeholder.text("Splitting text... ☑ Completed")

    # Create embeddings & FAISS
    main_placeholder.text("Creating embeddings & building vector store...")
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(FAISS_INDEX_PATH)
    main_placeholder.text("Vector store saved ☑ Completed")

    st.success("URLs processed and indexed successfully!")

# --------------------------------------------------------
# Ask Questions
# --------------------------------------------------------

st.markdown("### Ask a Question")

query = st.text_input("Question:")

if query:

    if not os.path.exists(FAISS_INDEX_PATH):
        st.error("Vector database not found. Please process URLs first.")
    else:
        embeddings = OpenAIEmbeddings()

        vectorstore = FAISS.load_local(
            FAISS_INDEX_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

        chain = RetrievalQAWithSourcesChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever()
        )
        # Will return a dictionary of
        result = chain({"question": query}, return_only_outputs=True)

        st.header("Answer")
        st.write(result["answer"])

        # Print the link or source from which we pulled the data.
        if "sources" in result:
            st.subheader("Sources")
            st.write(result["sources"])

# --------------------------------------------------------
# Footer
# --------------------------------------------------------

st.markdown("---")
st.caption("Built with Streamlit + LangChain + FAISS + OpenAI")
