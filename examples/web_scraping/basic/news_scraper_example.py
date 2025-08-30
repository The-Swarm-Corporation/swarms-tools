"""
News Website Scraping Example

This example demonstrates scraping news articles and blogs
using the detailed format to get comprehensive information.
"""

from swarms_tools.search.web_scraper import scrape_single_url_sync

# Scrape a news article with detailed information
url = "https://techcrunch.com"
content = scrape_single_url_sync(
    url,
    timeout=15,
    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
)

# The content object contains:
# - content.url: Original URL
# - content.title: Page title
# - content.text: Clean extracted text
# - content.links: List of all links found
# - content.images: List of all image URLs
# - content.word_count: Number of words in content
# - content.timestamp: When it was scraped
# - content.status_code: HTTP response code

# Access different parts of the scraped content
title = content.title
main_text = content.text
num_links = len(content.links)
num_images = len(content.images)
words = content.word_count
