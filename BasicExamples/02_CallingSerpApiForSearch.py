# Loads OpenAI and SerpAPI credentials
# Creates an OpenAI chat model
# Registers a Google Search tool
# Builds an AI agent that can call Google Search
# Asks a real-time question
# Agent searches Google and returns an answer
#  In short: An AI agent that can browse Google and answer current-events questions

import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.tools import tool

from langchain_community.utilities import SerpAPIWrapper

# -----------------------------
# Load environment  we have both keys here
# -----------------------------
load_dotenv("C:\Rama\Learn\AI\.env")

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not loaded")

if not os.getenv("SERPAPI_API_KEY"):
    raise RuntimeError("SERPAPI_API_KEY not loaded")

# -----------------------------
# Model (GPT-4.1 Nano)
# -----------------------------
model = ChatOpenAI(
    model="gpt-4.1-nano",
    temperature=0
)

# -----------------------------
# Google Search Tool (SerpAPI)
# -----------------------------
search = SerpAPIWrapper()

@tool
def google_search(query: str) -> str:
    """Search Google for recent information"""
    return search.run(query)

# -----------------------------
# Create Agent (debug enabled)
# debug=True
# -----------------------------
agent = create_agent(
    model=model,
    tools=[google_search]
)

# -----------------------------
# Invoke Agent
# -----------------------------
query = "What is the current RBI repo rate in India?"

result = agent.invoke(
    {"messages": [("user", query)]}
)

print(result["messages"][-1].content)

