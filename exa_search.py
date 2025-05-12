import os
import json
import requests
from typing import Dict, Any
from dotenv import load_dotenv
from rich.console import Console
from datetime import datetime

console = Console()
load_dotenv()


def format_exa_results(json_data: Dict[str, Any]) -> str:
    """Formats Exa.ai search results into structured text"""
    formatted_text = []

    if "error" in json_data:
        return f"### Error\n{json_data['error']}\n"

    # Extract search metadata
    search_params = json_data.get("effectiveFilters", {})
    query = search_params.get("query", "General web search")
    formatted_text.append(
        f"### Exa Search Results for: '{query}'\n\n---\n"
    )

    # Process results
    results = json_data.get("results", [])

    if not results:
        formatted_text.append("No results found.\n")
    else:
        for i, result in enumerate(results, 1):
            title = result.get("title", "No title")
            url = result.get("url", result.get("id", "No URL"))
            published_date = result.get("publishedDate", "")

            # Handle highlights
            highlights = result.get("highlights", [])
            highlight_text = (
                "\n".join(
                    [
                        (
                            h.get("text", h)
                            if isinstance(h, dict)
                            else str(h)
                        )
                        for h in highlights[:3]
                    ]
                )
                if highlights
                else "No summary available"
            )

            formatted_text.extend(
                [
                    f"{i}. **{title}**\n",
                    f"   - URL: {url}\n",
                    f"   - Published: {published_date.split('T')[0] if published_date else 'Date unknown'}\n",
                    f"   - Key Points:\n      {highlight_text}\n\n",
                ]
            )

    return "".join(formatted_text)


def exa_search(query: str, **kwargs: Any) -> str:
    """Performs web search using Exa.ai API"""
    api_url = "https://api.exa.ai/search"
    headers = {
        "x-api-key": os.getenv("EXA_API_KEY"),
        "Content-Type": "application/json",
    }

    payload = {
        "query": query,
        "useAutoprompt": True,
        "numResults": kwargs.get("num_results", 10),
        "contents": {
            "text": True,
            "highlights": {"numSentences": 2},
        },
        **kwargs,
    }

    try:
        response = requests.post(
            api_url, json=payload, headers=headers
        )
        response.raise_for_status()
        response_json = response.json()

        console.print("\n[bold]Exa Raw Response:[/bold]")
        console.print(json.dumps(response_json, indent=2))

        formatted_text = format_exa_results(
            response_json
        )  # Correct function call

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"exa_search_results_{timestamp}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(formatted_text)

        return formatted_text

    except requests.exceptions.RequestException as e:
        error_msg = f"Exa search request failed: {str(e)}"
        console.print(f"[bold red]{error_msg}[/bold red]")
        return error_msg
    except json.JSONDecodeError as e:
        error_msg = f"Invalid Exa response: {str(e)}"
        console.print(f"[bold red]{error_msg}[/bold red]")
        return error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        console.print(f"[bold red]{error_msg}[/bold red]")
        return error_msg


if __name__ == "__main__":
    console.print("\n[bold]Example Exa.ai Search:[/bold]")
    results = exa_search("Deepseek news")
    console.print("\n[bold green]Formatted Exa Results:[/bold green]")
    console.print(results)
