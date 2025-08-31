from swarms_tools.search.web_scraper import scrape_and_format_sync

# Scrape a news article with detailed information
url = "https://swarms.ai"
content = scrape_and_format_sync(
    url,
)

print(content)
