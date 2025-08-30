"""
Minimal Format Scraping Example

This example demonstrates quick content extraction using
the minimal format for fast processing and overview.
"""

from swarms_tools.search.web_scraper import SuperFastScraper

# Create scraper instance with optimized settings for speed
scraper = SuperFastScraper(
    timeout=8,
    max_workers=3,
    user_agent="FastBot/1.0",
    strip_html=True,
    remove_scripts=True,
    remove_styles=True,
)

# URLs for quick content overview
quick_urls = [
    "https://news.ycombinator.com",
    "https://reddit.com/r/technology",
    "https://stackoverflow.com",
]

# Get minimal formatted results for rapid scanning
minimal_results = scraper.scrape_urls_formatted(
    urls=quick_urls,
    format_type="minimal",
    truncate=True,  # Truncate to 200 characters per result
)

# minimal_results contains compact summaries like:
# "Page Title: First 200 characters of content..."
# Perfect for quick scanning and overview

compact_summaries = minimal_results

# Ideal for:
# - Content previews
# - Quick scanning
# - Feed generation
# - Summary dashboards
