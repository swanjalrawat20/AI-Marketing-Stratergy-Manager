import os
import requests
from agents import function_tool


@function_tool
def competitor_research(product: str, target_audience: str) -> str:
    """
    Research competitors for a product using the Tavily Search API.

    Returns competitor names, descriptions, strengths, weaknesses,
    and source URLs based on web search results.
    """

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        return "ERROR: TAVILY_API_KEY is not configured in the .env file."

    query = (
        f"competitors of {product} for {target_audience} "
        f"AI education platforms study apps"
    )

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
        answer = data.get("answer", "")

        if not results:
            return (
                f"No competitor research results found for "
                f"{product}."
            )

        output = []

        output.append("COMPETITOR RESEARCH")
        output.append("=" * 50)

        output.append(f"Product: {product}")
        output.append(f"Target Audience: {target_audience}")

        if answer:
            output.append("\nTavily Summary:")
            output.append(answer)

        output.append("\nResearch Sources:")

        for i, result in enumerate(results, start=1):

            title = result.get(
                "title",
                "Untitled"
            )

            url = result.get(
                "url",
                ""
            )

            content = result.get(
                "content",
                ""
            )

            output.append(
                f"\n{i}. {title}\n"
                f"URL: {url}\n"
                f"Evidence:\n{content[:1200]}"
            )

        output.append("\n")
        output.append(
            "IMPORTANT: The search results are evidence "
            "for competitor research. Competitor strengths "
            "and weaknesses should be verified before being "
            "treated as definitive facts."
        )

        return "\n".join(output)

    except requests.exceptions.RequestException as error:

        return (
            "Competitor research request failed: "
            f"{str(error)}"
        )

    except Exception as error:

        return (
            "Unexpected competitor research error: "
            f"{str(error)}"
        )