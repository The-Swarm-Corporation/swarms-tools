from swarms_tools.search.firecrawl import crawl_entire_site_firecrawl

content = crawl_entire_site_firecrawl(
    "https://swarms.ai",
    limit=1,
    formats=["markdown"],
    max_wait_time=600,
)

print(content)
