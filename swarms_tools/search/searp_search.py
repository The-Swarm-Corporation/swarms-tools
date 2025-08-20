import os
from typing import Any, Dict

import httpx
from dotenv import load_dotenv
from rich.console import Console

console = Console()
load_dotenv()


def format_serpapi_results(json_data: Dict[str, Any]) -> str:
    """
    Formats SerpAPI search results into a structured text format.

    Args:
        json_data: Dictionary containing SerpAPI search results

    Returns:
        Formatted string with search results
    """
    formatted_text = []

    # Extract query information
    search_params = json_data.get("search_parameters", {})
    query = search_params.get("q", "No query provided.")
    formatted_text.append(f"### Query\n{query}\n\n---\n")

    # Process organic results
    results = json_data.get("organic_results", [])
    formatted_text.append("### Results\n")

    if not results:
        formatted_text.append("No results found.\n")
    else:
        for i, result in enumerate(results, 1):
            title = result.get("title", "No title")
            url = result.get("link", "No URL")
            content = result.get("snippet", "No content available.")

            formatted_text.append(f"{i}. **Title**: {title}\n")
            formatted_text.append(f"   **URL**: {url}\n")
            formatted_text.append(f"   **Content**: {content}\n\n")

    return "".join(formatted_text)


def serpapi_search(query: str) -> str:
    """
    Performs a web search using the SerpAPI Google Search API via HTTPX.

    Args:
        query: Search query string

    Returns:
        Formatted search results string
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError(
            "SERPAPI_API_KEY not found in environment variables."
        )

    params = {
        "api_key": api_key,
        "engine": "google",
        "q": query,
        "location": "Austin, Texas, United States",
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en",
    }

    url = "https://serpapi.com/search"

    with httpx.Client(timeout=30.0) as client:
        response = client.get(url, params=params)
        response.raise_for_status()
        results = response.json()

    # Print raw JSON response
    console.print("\n[bold]SerpAPI Raw Response:[/bold]")
    console.print(results)

    # Format results
    formatted_text = format_serpapi_results(results)

    # Save results to file
    with open("serpapi_search_results.txt", "w") as file:
        file.write(formatted_text)

    return formatted_text


# # Example usage
# if __name__ == "__main__":
#     results = serpapi_search("Deepseek news")
#     console.print("\n[bold]Formatted SerpAPI Results:[/bold]")
#     console.print(results)
