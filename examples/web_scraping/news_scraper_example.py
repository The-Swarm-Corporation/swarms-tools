"""
News Website Scraping Example

This example demonstrates scraping news articles and blogs
using the detailed format to get comprehensive information.
"""

from swarms_tools.search.web_scraper import scrape_and_format_sync

# Scrape a news article with detailed information
url = "https://x.com"
content = scrape_and_format_sync(
    url,
)

print(content)
