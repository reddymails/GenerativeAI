# Author: rreddy
# This script creates a simple LangGraph-powered chatbot that sends user messages
# to an OpenAI model, stores the conversation history, and allows multi-turn conversations.
# This code builds a very small conversational workflow using LangGraph and LangChain where:
#    A user asks a question
#    The question is sent to an OpenAI chat model
#    The model responds
#    The conversation history is preserved
# You can keep asking follow-up questions in the same context

from langgraph.graph import StateGraph, MessagesState
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
# Load env
load_dotenv("C:/Rama/Learn/AI/.env")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def chat_node(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

graph = StateGraph(MessagesState)
graph.add_node("chat", chat_node)
graph.set_entry_point("chat")
graph.set_finish_point("chat")

app = graph.compile()

# ---- Run ----
state = {"messages": []}

state = app.invoke({
    "messages": [("human", "What is LangChain?")]
})
print(state["messages"][-1].content)

state = app.invoke({
    "messages": state["messages"] + [("human", "Give me an enterprise use case")]
})
print(state["messages"][-1].content)
