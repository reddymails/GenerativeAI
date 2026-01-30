
# A simple CSV Parser
import json
from langchain_community.document_loaders import CSVLoader

# Load the data
loader = CSVLoader("../machine-readable-business-employment-data-sep-2025-quarter.csv")
data = loader.load()

# Select the first record
first_record = data[0]

# 1. Combine content and metadata into a single dictionary
json_output = {
    "page_content": first_record.page_content,
    "metadata": first_record.metadata
}

# 2. Print as a formatted JSON string
print(json.dumps(json_output, indent=4))
