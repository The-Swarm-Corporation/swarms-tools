"""
Markdown Format Scraping Example

This example demonstrates scraping content and formatting it
as markdown for documentation or note-taking purposes.
"""

from swarms_tools.search.web_scraper import scrape_and_format_sync

# Scrape a documentation site and format as markdown
documentation_url = (
    "https://docs.python.org/3/tutorial/introduction.html"
)
markdown_content = scrape_and_format_sync(
    url=documentation_url,
    format_type="markdown",
    truncate=False,  # Keep full content for documentation
    remove_scripts=True,
    remove_styles=True,
    remove_comments=True,
)

# The markdown_content contains:
# # Page Title
#
# Full content text...
#
# **Links:** X found
# **Images:** Y found
# **Word Count:** Z

formatted_doc = markdown_content

# Perfect for saving to .md files or including in documentation
# The markdown format makes it easy to read and process further
