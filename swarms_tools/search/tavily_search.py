import os
from typing import Dict, Any
import httpx

from dotenv import load_dotenv

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
    Performs a web search using the Tavily API with raw httpx calls

    Args:
        query: Search query string

    Returns:
        Formatted search results string
    """
    # Get API key from environment
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError(
            "TAVILY_API_KEY environment variable is required"
        )

    # Set up headers and endpoint
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    base_url = "https://api.tavily.com"
    endpoint = f"{base_url}/search"

    # Prepare request payload
    payload = {"query": query}

    # Make the API request using httpx
    with httpx.Client() as client:
        try:
            response = client.post(
                endpoint, headers=headers, json=payload, timeout=30.0
            )

            # Check if the request was successful
            if response.status_code == 200:
                response_data = response.json()

                # Print raw JSON response
                print("\nTavily Raw Response:")
                print(response_data)

                # Format results
                formatted_text = format_query_results(response_data)

                # Save results to file
                with open("tavily_search_results.txt", "w") as file:
                    file.write(formatted_text)

                return formatted_text
            else:
                error_msg = f"API request failed with status {response.status_code}: {response.text}"
                print(f"Error: {error_msg}")
                return error_msg

        except httpx.RequestError as e:
            error_msg = f"Request error: {str(e)}"
            print(f"Error: {error_msg}")
            return error_msg
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP error: {e.response.status_code} - {e.response.text}"
            print(f"Error: {error_msg}")
            return error_msg


# # Example usage
# if __name__ == "__main__":
#     results = tavily_search("Deepseek news")
#     print("\nFormatted Tavily Results:")
#     print(results)
