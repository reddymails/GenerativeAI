#######################################################################################################
# A two-stage LLM workflow wrapped in a function
# This code defines a LangChain-powered function that generates a restaurant name
# and menu items for a given cuisine using a two-step LLM pipeline.
########################################################################################################
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

#Save your open ai key in .env file with OPENAI_API_KEY=ffdfdfafaf  (no quotes)
load_dotenv(r"C:\Rama\Learn\AI\.env")

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not loaded")


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

def generate_restaurant_name_and_menu_items(cuisine):
    cuisine = cuisine.lower()
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


    result = chain.invoke({"cuisine": cuisine})
    return result


if __name__ == "__main__":
    print (generate_restaurant_name_and_menu_items("Mexican"))
#
#def generate_restaurant_name_and_menu_items( cuisine):
#    return {
#        'restaurant_name':'Curry Delight',
#        'menu_items' : 'samosa, paneer, mushroom masala'
#    }

