#
# Build a prompt → send it to an LLM → print the response → handle errors.
#
################################################################
import os
from dotenv import load_dotenv
from openai import RateLimitError, AuthenticationError

load_dotenv(r"C:\Rama\Learn\AI\.env")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not loaded")

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.6
)

# This will just format and correct the string you still need to Call LLM.
prompt = PromptTemplate(
    input_variables=["cuisine"],
    template="I want to open a restaurant for {cuisine} food. Suggest a fancy name."
)
chain_input = prompt.format(cuisine="Indian")
print(chain_input)

try:
    response = llm.invoke(chain_input)
    print(response)

    
except RateLimitError as e:
    print("❌ RATE LIMIT ERROR")
    print(e)

except AuthenticationError as e:
    print("❌ AUTH ERROR")
    print(e)

except Exception as e:
    print("❌ OTHER ERROR")
    print(type(e))
    print(e)
