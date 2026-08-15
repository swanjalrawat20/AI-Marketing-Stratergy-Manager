import os
import requests
from agents import function_tool
from dotenv import load_dotenv

load_dotenv()


@function_tool
def web_research(query: str) -> str:
    """
    Search the web using Tavily and return useful research results.
    """

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        return "ERROR: TAVILY_API_KEY is not configured."

    try:
        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": api_key,
                "query": query,
                "search_depth": "basic",
                "max_results": 5,
                "include_answer": True,
            },
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results", [])
        answer = data.get("answer")

        if not results:
            return f"No research results found for: {query}"

        output = []

        if answer:
            output.append("SUMMARY:")
            output.append(answer)

        output.append("\nSOURCES:")

        for index, result in enumerate(results, start=1):
            title = result.get("title", "Untitled")
            url = result.get("url", "")
            content = result.get("content", "")

            output.append(
                f"\n{index}. {title}\n"
                f"URL: {url}\n"
                f"{content[:1500]}"
            )

        return "\n".join(output)

    except requests.exceptions.RequestException as e:
        return f"Web research request failed: {e}"

    except Exception as e:
        return f"Unexpected web research error: {e}"