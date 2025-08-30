import asyncio

from swarms_tools.search.web_scraper import (
    scrape_single_url,
    format_scraped_content,
)


async def _run():
    url = "https://httpbin.org/html"
    content = await scrape_single_url(url)
    formatted = format_scraped_content(content, "summary")
    print(formatted)


if __name__ == "__main__":
    asyncio.run(_run())
