# This script creates a LangChain LCEL chatbot with sliding window memory and
# a callable math tool, allowing the assistant to both converse and perform calculations.

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool

load_dotenv("C:/Rama/Learn/AI/.env")

@tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful enterprise assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

llm_with_tools = llm.bind_tools([add])

chain = prompt | llm_with_tools | StrOutputParser()

# ---- Window Memory ----
WINDOW_SIZE = 2
store = {}

def get_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    history = store[session_id]
    if len(history.messages) > WINDOW_SIZE:
        history.messages = history.messages[-WINDOW_SIZE:]

    return history

conversation = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="input",
    history_messages_key="history",
)

config = {"configurable": {"session_id": "enterprise-demo"}}

print(conversation.invoke({"input": "What is LangChain?"}, config))
print(conversation.invoke({"input": "What is 15 plus 27?"}, config))
print(conversation.invoke({"input": "Why is window memory useful?"}, config))
