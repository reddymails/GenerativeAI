#########################################################################################
#The program:
#    Loads your SerpAPI key
#    Calls Google Autocomplete for the word "coffee"
#    Extracts suggested search phrases
#    Prints them in a readable format
#    Filters suggestions containing "near me"
#    👉 In short: A real-time Google autocomplete suggestion fetcher
#########################################################################################
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
# -----------------------------
# Load environment  we have both keys here
# -----------------------------
load_dotenv("C:\Rama\Learn\AI\.env")
if not os.getenv("SERPAPI_API_KEY"):
    raise RuntimeError("SERPAPI_API_KEY not loaded")

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
######
# Simple function to parse results.
######
def parse_and_print_autocomplete(results):
    parsed = []

    for r in results:
        parsed.append({
            "query": r.get("value"),
            "relevance": r.get("relevance"),
            "type": r.get("type"),
            "serpapi_link": r.get("serpapi_link")
        })

    # Pretty print
    print("\nGoogle Autocomplete Suggestions:\n" + "-" * 40)
    for i, p in enumerate(parsed, start=1):
        print(
            f"{i:02d}. {p['query']}\n"
            f"    Relevance : {p['relevance']}\n"
            f"    Type      : {p['type']}\n"
        )

    return parsed




params = {
  "engine": "google_autocomplete",
  "q": "coffee",
  "hl": "en",
  "gl": "us",
  "api_key":SERPAPI_API_KEY
}

search = GoogleSearch(params)
results = search.get_dict()
print(results)
suggestions = results["suggestions"]
parsed = parse_and_print_autocomplete (suggestions)


near_me = [r for r in parsed  if "near me" in r["query"].lower()]

print(' Near me =', near_me)




