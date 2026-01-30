# Creates a low-cost OpenAI chat model
# Registers two tools:
# Wikipedia search tool
# Custom math calculator
# Builds an agent that decides which tool to use
# Asks a compound question
# Agent:
#     Searches Wikipedia for India’s population
#     Calls calculator to compute 10%
#     Prints final answer
#      In short: An agent that can research and calculate

import os
import math
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.tools import tool

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# -----------------------------
# Load environment
# -----------------------------

load_dotenv(r"C:\Rama\Learn\AI\.env")
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not loaded")

# -----------------------------
# Model GPT-5 mini  or gpt-4o-mini
# gpt-4.1-nano Cheapest
# Input: $0.20 / 1M tokens
# -----------------------------
model = ChatOpenAI(
    model="gpt-4.1-nano",
    temperature=0
)

# -----------------------------
# Wikipedia Tool
# -----------------------------
wiki_tool = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(
        top_k_results=1,
        doc_content_chars_max=300
    )
)

# -----------------------------
# Math Tool (CUSTOM – RECOMMENDED)
# Custom built.
# -----------------------------
@tool
def calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression.
    Example: "1430000000 * 0.10"
    """
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

# -----------------------------
# Create Agent with BOTH tools
# debug=True
# -----------------------------
agent = create_agent(
    model=model,
    tools=[wiki_tool, calculate]

)

# -----------------------------
# Invoke Agent
# -----------------------------
query = (
    "According to Wikipedia, what is the population of India? "
    "Then calculate 10 percent of that population."
)

result = agent.invoke(
    {"messages": [("user", query)]}
)

print(result["messages"][-1].content)
