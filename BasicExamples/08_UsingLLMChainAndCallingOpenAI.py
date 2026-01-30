#############################################################
# This script builds a two-step LangChain LCEL pipeline that automatically:
#     Generates a restaurant name from a cuisine
#     Uses that name to generate menu items
#     Combines both into a single formatted result
#############################################################
import os
from dotenv import load_dotenv
from openai import RateLimitError, AuthenticationError
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

#Save your open api key in .env file with OPENAI_API_KEY=ffdfdfafaf  (no quotes)
load_dotenv(r"C:\Rama\Learn\AI\.env")

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not loaded")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

prompt_restaurant = PromptTemplate(
    input_variables=["cuisine"],
    template="I want to open a restaurant for {cuisine}. Suggest a name."
)

prompt_menu = PromptTemplate(
    input_variables=["restaurant_name"],
    template="Suggest menu items for {restaurant_name}. Return a comma-separated list."
)

def extract_name(msg):
    return {"restaurant_name": msg.content.strip()}

def combine_outputs(data):
    return (
        f"Restaurant Name: {data['restaurant_name']}\n"
        f"Menu Items: {data['menu_items']}"
    )

chain = (
    prompt_restaurant
    | llm
    | RunnableLambda(extract_name)
    | {
        "restaurant_name": lambda x: x["restaurant_name"],
        "menu_items": prompt_menu | llm | (lambda m: m.content)
    }
    | RunnableLambda(combine_outputs)
)

try:
    result = chain.invoke({"cuisine": "Mexican"})
    print(result)
except AuthenticationError:
    print("Invalid OpenAI API key")
except RateLimitError:
    print("Rate limit exceeded")
