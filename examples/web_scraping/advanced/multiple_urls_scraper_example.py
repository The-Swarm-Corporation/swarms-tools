"""
Multiple URLs Concurrent Scraping Example

This example demonstrates scraping multiple websites concurrently
for maximum performance and efficiency.
"""

from swarms_tools.search.web_scraper import scrape_multiple_urls_sync

# List of URLs to scrape concurrently
urls_to_scrape = [
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://example.com",
    "https://www.python.org",
    "https://github.com",
]

# Scrape all URLs concurrently with custom settings
formatted_results = scrape_multiple_urls_sync(
    urls=urls_to_scrape,
    format_type="detailed",
    truncate=True,
    max_workers=5,  # Number of concurrent threads
    timeout=12,  # Timeout per request
    max_retries=2,  # Retry failed requests
)

# The formatted_results string contains all scraped content
# formatted and separated by dividers for easy reading
all_content = formatted_results

# Each URL result includes:
# - URL and title
# - Full extracted text content
# - Number of links and images found
# - Word count and timestamp
# - Status information
