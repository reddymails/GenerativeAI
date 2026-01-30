#     This code builds a chatbot with sliding window memory:
#     The assistant remembers only the last N messages
#     Older messages are automatically discarded
#     Conversation is tied to a session ID
#     Uses LangChain’s RunnableWithMessageHistory
# In short:
#     Stateful chatbot with windowed conversation memory

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

# ---- WINDOW MEMORY IMPLEMENTATION ----
WINDOW_SIZE = 4   # last 4 messages (2 user + 2 AI)

store = {}

def get_windowed_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    history = store[session_id]

    # Enforce window size
    if len(history.messages) > WINDOW_SIZE:
        history.messages = history.messages[-WINDOW_SIZE:]

    return history

conversation = RunnableWithMessageHistory(
    chain,
    get_windowed_history,
    input_messages_key="input",
    history_messages_key="history",
)

config = {"configurable": {"session_id": "rama-session"}}

# ---- Conversation ----
conversation.invoke({"input": "What is LangChain?"}, config=config)
conversation.invoke({"input": "How does memory work?"}, config=config)
conversation.invoke({"input": "Explain window memory"}, config=config)
conversation.invoke({"input": "Why is it useful?"}, config=config)
response5 = conversation.invoke({"input": "What happens to old messages?"}, config=config)

print(response5.content)