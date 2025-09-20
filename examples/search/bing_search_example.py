"""
Bing Search API Example

This example demonstrates how to use the Bing Search API tool to search for web articles
and retrieve relevant information from the web.

Requirements:
- BING_API_KEY environment variable must be set
- Install required dependencies: httpx, loguru

Usage:
    python bing_search_example.py
"""

import os
from dotenv import load_dotenv
from loguru import logger
from swarms_tools.search.bing import fetch_web_articles_bing_api

# Load environment variables
load_dotenv()


def main():
    """
    Main function demonstrating Bing Search API usage.
    """
    logger.info("Starting Bing Search API example...")
    
    # Check if API key is available
    api_key = os.getenv("BING_API_KEY")
    if not api_key:
        logger.error("BING_API_KEY not found in environment variables")
        logger.info("Please set your Bing Search API key in the .env file")
        logger.info("You can get an API key from: https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/")
        return
    
    try:
        # Example 1: Search for technology news
        logger.info("Example 1: Searching for technology news")
        tech_query = "latest artificial intelligence developments 2024"
        tech_results = fetch_web_articles_bing_api(tech_query)
        logger.info(f"Technology search results:\n{tech_results}")
        
        # Example 2: Search for financial information
        logger.info("Example 2: Searching for financial information")
        finance_query = "stock market trends today"
        finance_results = fetch_web_articles_bing_api(finance_query)
        logger.info(f"Finance search results:\n{finance_results}")
        
        # Example 3: Search for scientific research
        logger.info("Example 3: Searching for scientific research")
        science_query = "quantum computing breakthroughs"
        science_results = fetch_web_articles_bing_api(science_query)
        logger.info(f"Science search results:\n{science_results}")
        
        # Example 4: Search for programming documentation
        logger.info("Example 4: Searching for programming documentation")
        programming_query = "Python 3.12 new features documentation"
        programming_results = fetch_web_articles_bing_api(programming_query)
        logger.info(f"Programming search results:\n{programming_results}")
        
        # Example 5: Search for health and wellness
        logger.info("Example 5: Searching for health and wellness")
        health_query = "mental health awareness tips"
        health_results = fetch_web_articles_bing_api(health_query)
        logger.info(f"Health search results:\n{health_results}")
        
        # Example 6: Search for local information
        logger.info("Example 6: Searching for local information")
        local_query = "best restaurants in New York City"
        local_results = fetch_web_articles_bing_api(local_query)
        logger.info(f"Local search results:\n{local_results}")
        
        # Example 7: Search for educational content
        logger.info("Example 7: Searching for educational content")
        education_query = "machine learning tutorial for beginners"
        education_results = fetch_web_articles_bing_api(education_query)
        logger.info(f"Education search results:\n{education_results}")
        
        # Example 8: Search for news
        logger.info("Example 8: Searching for news")
        news_query = "breaking news technology"
        news_results = fetch_web_articles_bing_api(news_query)
        logger.info(f"News search results:\n{news_results}")
        
        logger.info("Bing Search API examples completed successfully!")
        logger.info("Note: The API returns formatted strings with article information")
        logger.info("Each search returns up to 4 articles with title, URL, and metadata")
        
    except Exception as e:
        logger.error(f"Error with Bing Search API: {e}")
        logger.info("Make sure your API key is valid and you have sufficient credits")
        logger.info("Check your Azure Cognitive Services subscription for usage limits")


if __name__ == "__main__":
    main()
