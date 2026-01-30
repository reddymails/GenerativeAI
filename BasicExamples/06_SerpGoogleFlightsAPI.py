############################################################################################
# This script queries Google Flights via SerpAPI for flights
# between two cities on a given date and prints the best options in a simplified format.
############################################################################################
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
from ParseFilghtsResponse import parse_best_flights
# -----------------------------
# Load environment  we have both keys here
# -----------------------------
load_dotenv("C:\Rama\Learn\AI\.env")

if not os.getenv("SERPAPI_API_KEY"):
    raise RuntimeError("SERPAPI_API_KEY not loaded")

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

params = {
    "engine": "google_flights",
    "departure_id": "BLR",
    "arrival_id": "COK",
    "currency": "INR",
    "type": "2",
    "outbound_date": "2026-02-20",
    "api_key": SERPAPI_API_KEY
}

search = GoogleSearch(params)
results = search.get_dict()

best_flights = results.get("best_flights", [])
parsed_flights = parse_best_flights(best_flights)

for f in parsed_flights:
    print(f)





