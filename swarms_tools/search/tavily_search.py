import os
from typing import Dict, Any

try:
    from tavily import TavilyClient
except ImportError:
    print("Installing tavily...")
    import subprocess
    import sys

    subprocess.run([sys.executable, "-m", "pip", "install", "tavily"])
    from tavily import TavilyClient


from dotenv import load_dotenv
from rich.console import Console

console = Console()
load_dotenv()


def format_query_results(json_data: Dict[str, Any]) -> str:
    """
    Formats Tavily search results into a structured text format.

    Args:
        json_data: Dictionary containing Tavily query results

    Returns:
        Formatted string with search results
    """
    formatted_text = []

    # Add the main query
    query = json_data.get("query", "No query provided.")
    formatted_text.append(f"### Query\n{query}\n\n---\n")

    # Add the results
    results = json_data.get("results", [])
    formatted_text.append("### Results\n")

    if not results:
        formatted_text.append("No results found.\n")
    else:
        for i, result in enumerate(results, 1):
            title = result.get("title", "No title")
            url = result.get("url", "No URL")
            content = result.get("content", "No content available.")
            score = result.get("score", "Not available")

            formatted_text.append(f"{i}. **Title**: {title}\n")
            formatted_text.append(f"   **URL**: {url}\n")
            formatted_text.append(f"   **Content**: {content}\n")
            formatted_text.append(f"   **Score**: {score}\n\n")

    return "".join(formatted_text)


def tavily_search(query: str) -> str:
    """
    Performs a web search using the Tavily API

    Args:
        query: Search query string

    Returns:
        Formatted search results string
    """
    # Initialize Tavily client
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    # Execute search query
    response = tavily_client.search(query)

    # Print raw JSON response
    console.print("\n[bold]Tavily Raw Response:[/bold]")
    console.print(response)

    # Format results
    formatted_text = format_query_results(response)

    # Save results to file
    with open("tavily_search_results.txt", "w") as file:
        file.write(formatted_text)

    return formatted_text


# # Example usage
# if __name__ == "__main__":
#     results = tavily_search("Deepseek news")
#     console.print("\n[bold]Formatted Tavily Results:[/bold]")
#     console.print(results)
