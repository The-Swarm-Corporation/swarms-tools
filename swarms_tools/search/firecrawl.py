"""
Firecrawl API integration for crawling entire websites.

This module provides a synchronous function to crawl websites using the Firecrawl API,
returning all accessible content as a formatted string.
"""

import os
import time
from typing import Dict, List, Optional, Any

import httpx
import orjson
from loguru import logger


def crawl_entire_site_firecrawl(
    url: str,
    limit: int = 20,
    formats: Optional[List[str]] = None,
    max_wait_time: int = 300,
    poll_interval: int = 5,
    include_metadata: bool = True,
) -> str:
    """
    Crawl an entire website and return all content as a formatted string.

    This function initiates a crawl job with the Firecrawl API, polls for completion,
    and returns all scraped content formatted as a single string. The function is
    synchronous and will block until the crawl is complete or times out.

    Args:
        url: The base URL to crawl (e.g., "https://docs.firecrawl.dev")
        limit: Maximum number of pages to crawl (default: 100)
        formats: List of content formats to retrieve. Options: ["markdown", "html"]
                (default: ["markdown"])
        max_wait_time: Maximum time to wait for crawl completion in seconds (default: 300)
        poll_interval: Time between status checks in seconds (default: 5)
        include_metadata: Whether to include page metadata in the output (default: True)
        api_key: Firecrawl API key. If None, reads from FIRECRAWL_API_KEY env var
        timeout: HTTP request timeout in seconds (default: 30)

    Returns:
        str: Formatted string containing all crawled content from the website

    Raises:
        ValueError: If API key is missing or invalid parameters are provided
        httpx.HTTPError: If HTTP requests fail
        TimeoutError: If crawl job doesn't complete within max_wait_time
        RuntimeError: If crawl job fails or returns unexpected response

    Example:
        >>> content = crawl_entire_site(
        ...     "https://docs.firecrawl.dev",
        ...     limit=50,
        ...     formats=["markdown"],
        ...     max_wait_time=600
        ... )
        >>> print(f"Crawled {len(content)} characters of content")
    """
    timeout = 30

    # Validate inputs
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")

    if limit <= 0:
        raise ValueError("Limit must be positive")

    if max_wait_time <= 0:
        raise ValueError("Max wait time must be positive")

    if poll_interval <= 0:
        raise ValueError("Poll interval must be positive")

    # Set default formats
    if formats is None:
        formats = ["markdown"]

    # Validate formats
    valid_formats = {"markdown", "html"}
    invalid_formats = set(formats) - valid_formats
    if invalid_formats:
        raise ValueError(
            f"Invalid formats: {invalid_formats}. Must be one of: {valid_formats}"
        )

    # Get API key
    api_key = os.getenv("FIRECRAWL_API_KEY")

    if not api_key:
        raise ValueError(
            "API key is required. Provide it as parameter or set FIRECRAWL_API_KEY environment variable"
        )

    logger.info(f"Starting crawl for URL: {url} with limit: {limit}")

    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # Prepare crawl request payload
    crawl_payload = {
        "url": url,
        "limit": limit,
        "scrapeOptions": {"formats": formats},
    }

    try:
        with httpx.Client(timeout=timeout) as client:
            # Submit crawl job
            logger.info("Submitting crawl job to Firecrawl API")
            response = client.post(
                "https://api.firecrawl.dev/v2/crawl",
                headers=headers,
                content=orjson.dumps(crawl_payload),
            )
            response.raise_for_status()

            crawl_data = orjson.loads(response.content)

            if not crawl_data.get("success"):
                raise RuntimeError(
                    f"Crawl job submission failed: {crawl_data}"
                )

            job_id = crawl_data.get("id")
            if not job_id:
                raise RuntimeError(
                    "No job ID returned from crawl submission"
                )

            logger.info(
                f"Crawl job submitted successfully. Job ID: {job_id}"
            )

            # Poll for completion
            start_time = time.time()
            status_url = (
                f"https://api.firecrawl.dev/v2/crawl/{job_id}"
            )

            while True:
                elapsed_time = time.time() - start_time
                if elapsed_time > max_wait_time:
                    raise TimeoutError(
                        f"Crawl job did not complete within {max_wait_time} seconds"
                    )

                logger.debug(
                    f"Checking crawl status (elapsed: {elapsed_time:.1f}s)"
                )

                status_response = client.get(
                    status_url, headers=headers
                )
                status_response.raise_for_status()

                status_data = orjson.loads(status_response.content)
                status = status_data.get("status")

                logger.debug(f"Crawl status: {status}")

                if status == "completed":
                    logger.info("Crawl completed successfully")
                    break
                elif status == "failed":
                    error_msg = status_data.get(
                        "error", "Unknown error"
                    )
                    raise RuntimeError(
                        f"Crawl job failed: {error_msg}"
                    )
                elif status in ["scraping", "waiting"]:
                    # Job still in progress
                    total = status_data.get("total", 0)
                    credits_used = status_data.get("creditsUsed", 0)
                    logger.info(
                        f"Crawl in progress: {credits_used}/{total} pages processed"
                    )
                    time.sleep(poll_interval)
                else:
                    logger.warning(f"Unknown crawl status: {status}")
                    time.sleep(poll_interval)

            # Extract and format the crawled data
            crawled_data = status_data.get("data", [])
            if not crawled_data:
                logger.warning("No data returned from crawl")
                return ""

            logger.info(
                f"Processing {len(crawled_data)} crawled pages"
            )

            # Format the content into a single string
            formatted_content = _format_crawled_content(
                crawled_data, formats, include_metadata
            )

            logger.success(
                f"Successfully crawled {len(crawled_data)} pages, "
                f"returning {len(formatted_content)} characters"
            )

        return formatted_content

    except httpx.HTTPError as e:
        logger.error(f"HTTP error during crawl: {e}")
        raise
    except orjson.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        raise RuntimeError(f"Failed to parse API response: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during crawl: {e}")
        raise


def _format_crawled_content(
    crawled_data: List[Dict[str, Any]],
    formats: List[str],
    include_metadata: bool,
) -> str:
    """
    Format crawled data into a single string.

    Args:
        crawled_data: List of crawled page data from API
        formats: List of content formats to include
        include_metadata: Whether to include metadata

    Returns:
        str: Formatted content string
    """
    content_parts = []

    for i, page in enumerate(crawled_data, 1):
        page_content = []

        # Add page header
        source_url = page.get("metadata", {}).get(
            "sourceURL", "Unknown URL"
        )
        title = page.get("metadata", {}).get("title", "Untitled")

        page_content.append(f"\n{'='*80}")
        page_content.append(f"PAGE {i}: {title}")
        page_content.append(f"URL: {source_url}")
        page_content.append(f"{'='*80}\n")

        # Add metadata if requested
        if include_metadata:
            metadata = page.get("metadata", {})
            if metadata:
                page_content.append("METADATA:")
                for key, value in metadata.items():
                    if key != "sourceURL":  # Already shown above
                        page_content.append(f"  {key}: {value}")
                page_content.append("")

        # Add content in requested formats
        for format_type in formats:
            content = page.get(format_type)
            if content:
                page_content.append(f"{format_type.upper()} CONTENT:")
                page_content.append("-" * 40)
                page_content.append(content)
                page_content.append("")

        content_parts.append("\n".join(page_content))

    return "\n".join(content_parts)


# if __name__ == "__main__":
#     content = crawl_entire_site_firecrawl(
#         "https://swarms.ai",
#         limit=100,
#         formats=["markdown"],
#         max_wait_time=600,
#     )
#     print(content)
