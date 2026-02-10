import os
from dotenv import load_dotenv
from google import genai

load_dotenv(r"C:\Rama\Learn\AI\.env")

api_key_value = os.getenv("AI_STUDIO_GOOGLE_COM_API_KEY")
if not api_key_value:
    raise RuntimeError("AI_STUDIO_GOOGLE_COM_API_KEY not found in .env file")

client = genai.Client(api_key=api_key_value)

for m in client.models.list():
    print(m.name)

