# This script builds a stateful conversational assistant using:
# LCEL (LangChain Expression Language)
# OpenAI chat model
# Sliding window memory
# Automatic string output parsing
# In short:
#     An enterprise-ready chatbot that remembers only the last few messages

import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser

# Load env
load_dotenv("C:/Rama/Learn/AI/.env")

# LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3
)

# Prompt (LCEL-friendly)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful enterprise AI assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# LCEL chain: Prompt → LLM → String output
chain = prompt | llm | StrOutputParser()

# ---- Window Memory ----
WINDOW_SIZE = 4
store = {}

def get_windowed_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    history = store[session_id]

    # Keep only last N messages
    if len(history.messages) > WINDOW_SIZE:
        history.messages = history.messages[-WINDOW_SIZE:]

    return history

conversation = RunnableWithMessageHistory(
    chain,
    get_windowed_history,
    input_messages_key="input",
    history_messages_key="history",
)

# ---- Run Conversation ----
config = {"configurable": {"session_id": "lcel-demo"}}

print(conversation.invoke(
    {"input": "What is LangChain?"},
    config=config
))

print(conversation.invoke(
    {"input": "How is LCEL different from chains?"},
    config=config
))

print(conversation.invoke(
    {"input": "Give me an enterprise use case"},
    config=config
))
