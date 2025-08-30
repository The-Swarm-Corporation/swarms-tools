"""
Custom Configuration Scraping Example

This example demonstrates advanced scraper configuration
for specific use cases and website requirements.
"""

from swarms_tools.search.web_scraper import SuperFastScraper

# Create scraper with custom configuration for research sites
research_scraper = SuperFastScraper(
    timeout=20,  # Longer timeout for academic sites
    max_retries=5,  # More retries for reliability
    user_agent="Mozilla/5.0 (compatible; ResearchBot/1.0; +http://example.com/bot)",
    max_workers=2,  # Conservative threading for respectful scraping
    strip_html=True,
    remove_scripts=True,
    remove_styles=True,
    remove_comments=True,
)

# Scrape academic/research content
research_url = "https://arxiv.org/abs/2301.00001"
research_content = research_scraper.scrape_single_url(research_url)

# Access structured data
paper_title = research_content.title
paper_abstract = research_content.text
paper_links = research_content.links
citation_count = research_content.word_count

# Format for academic use
academic_summary = research_scraper.format_content(
    research_content,
    format_type="full",  # Complete content for research
    truncate=False,  # Never truncate academic content
)

# Configuration optimized for:
# - Academic papers and journals
# - Respectful scraping practices
# - Maximum content retention
# - Reliability over speed
