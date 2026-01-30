#
# This code is a LangChain data-loading example.
# It shows how to turn a CSV file into LangChain Document objects
# so the data can later be used for search, embeddings, or RAG (Retrieval-Augmented Generation)
#########################
import pandas as pd
from langchain_community.document_loaders import DataFrameLoader

# 1. Load the CSV into a Pandas DataFrame
df = pd.read_csv("../machine-readable-business-employment-data-sep-2025-quarter.csv")

# 2. Use DataFrameLoader
# page_content_column is the column you want to use as the main text
# usually for CSVs, you can pick the main "Subject" or "Series_reference"
loader = DataFrameLoader(df, page_content_column="Series_reference")
data = loader.load()

print(f"Series Reference: {data[0]}")

# 3. Access your data
# The 'Series_reference' is now in page_content
print(f"Series Reference: {data[0].page_content}")

# All other columns are automatically placed in the metadata dictionary
print(f"Period: {data[0].metadata['Period']}")
print(f"Data Value: {data[0].metadata['Data_value']}")