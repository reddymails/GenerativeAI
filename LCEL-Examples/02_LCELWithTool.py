# This script builds a stateful conversational assistant using:
# LCEL (LangChain Expression Language)
# OpenAI chat model
# Sliding window memory
# Automatic string output parsing
# In short:
#     An enterprise-ready chatbot that remembers only the last few messages

from dotenv import load_dotenv
load_dotenv("C:/Rama/Learn/AI/.env")

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools([add])

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}")
])

# Step 1: LLM decides to call tool
ai_msg = (prompt | llm_with_tools).invoke(
    {"input": "What is 12 plus 30?"}
)

# Step 2: Execute tool
tool_call = ai_msg.tool_calls[0]
tool_result = add.invoke(tool_call["args"])

# Step 3: Give result back to LLM
final_msg = llm.invoke([
    ai_msg,
    {
        "role": "tool",
        "tool_call_id": tool_call["id"],
        "content": str(tool_result)
    }
])

print(final_msg.content)
