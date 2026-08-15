import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

print("Tavily API key loaded:", bool(api_key))

if not api_key:
    print("ERROR: TAVILY_API_KEY is missing from .env")
    exit()

response = requests.post(
    "https://api.tavily.com/search",
    json={
        "api_key": api_key,
        "query": "AI-powered education market trends for college students",
        "search_depth": "basic",
        "max_results": 5,
        "include_answer": True,
    },
    timeout=30,
)

print("Status code:", response.status_code)
print("\nResponse:")
print(response.text)