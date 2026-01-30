# Test your Environment With OpenAPI

import os
from dotenv import load_dotenv
from openai import OpenAI
from openai import RateLimitError, AuthenticationError

load_dotenv(r"C:\Rama\Learn\AI\.env")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not loaded")

client = OpenAI()

try:
    response = client.responses.create(
        model="gpt-5-nano",
        input="Write a one-sentence bedtime story about a unicorn."
    )
    print(response.output_text)


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
