
# In short: Convert a .txt file into a LangChain Document

import pprint
from langchain_community.document_loaders import TextLoader

loader  = TextLoader("../Debug_Ouput_CallingWikipediaAgentWithMathInPython.txt")
data =   loader.load()
#print(data[0])

#print(data[0].page_content)

#Prints file name. 
print(data[0].metadata)