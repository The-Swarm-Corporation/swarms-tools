"""
Content Analysis Scraping Example

This example demonstrates scraping for content analysis,
SEO research, and text mining applications.
"""

from swarms_tools.search.web_scraper import SuperFastScraper

# Create analyzer-optimized scraper
content_analyzer = SuperFastScraper(
    timeout=12,
    max_workers=4,
    user_agent="ContentAnalyzer/1.0 (compatible)",
    strip_html=True,
    remove_scripts=True,
    remove_styles=True,
    remove_comments=True,
)

# Target URLs for content analysis
analysis_targets = [
    "https://blog.openai.com",
    "https://ai.googleblog.com",
    "https://research.facebook.com/blog",
]

# Scrape for detailed content analysis
analysis_results = content_analyzer.scrape_urls(analysis_targets)

# Process each result for analysis metrics
for content in analysis_results:
    page_url = content.url
    page_title = content.title
    content_text = content.text
    word_density = content.word_count
    link_count = len(content.links)
    image_count = len(content.images)

    # Calculate content metrics
    title_length = len(content.title)
    text_length = len(content.text)
    avg_word_length = text_length / max(content.word_count, 1)

    # SEO analysis data points
    has_title = len(content.title) > 0
    content_richness = content.word_count / max(link_count, 1)
    media_ratio = image_count / max(content.word_count, 1) * 100

# Applications:
# - SEO content audits
# - Competitive content analysis
# - Text mining and NLP preprocessing
# - Content quality assessment
# - Topic modeling preparation
