"""
E-commerce Product Scraping Example

This example demonstrates scraping product pages and
extracting structured information for market research.
"""

from swarms_tools.search.web_scraper import (
    scrape_single_url_sync,
    format_scraped_content,
)

# Scrape product information from e-commerce sites
product_urls = [
    "https://www.amazon.com/dp/B08N5WRWNW",  # Example product
    "https://store.steampowered.com",  # Digital products
]

# Configure for e-commerce scraping
ecommerce_content = scrape_single_url_sync(
    url=product_urls[1],  # Use Steam store as example
    timeout=15,
    user_agent="Mozilla/5.0 (compatible; PriceBot/1.0)",
    remove_scripts=True,
    remove_styles=True,
)

# Extract product information
product_name = ecommerce_content.title
product_description = ecommerce_content.text
product_images = ecommerce_content.images
related_links = ecommerce_content.links

# Format for summary view
product_summary = format_scraped_content(
    ecommerce_content, format_type="summary", truncate=True
)

# Format for detailed analysis
product_details = format_scraped_content(
    ecommerce_content, format_type="detailed", truncate=False
)

# Use cases:
# - Price monitoring
# - Product research
# - Inventory tracking
# - Market analysis
# - Competitor monitoring
