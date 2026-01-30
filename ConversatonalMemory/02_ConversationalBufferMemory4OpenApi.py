#
# This code builds a session-based chatbot that remembers the entire
# conversation history and automatically passes it to the LLM for every response.
#

import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Load env
load_dotenv("C:/Rama/Learn/AI/.env")

# LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5
)

# Prompt with history
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm

# Store histories by session
store = {}

def get_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Add memory
conversation = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="input",
    history_messages_key="history",
)

# ---- Conversation ----
config = {"configurable": {"session_id": "rama-session"}}

response1 = conversation.invoke(
    {"input": "What is LangChain?"},
    config=config
)
print(response1.content)

response2 = conversation.invoke(
    {"input": "How is it different from using OpenAI directly?"},
    config=config
)
print(response2.content)

response3 = conversation.invoke(
    {"input": "Give me a real-world enterprise use case"},
    config=config
)
print(response3.content)

