"""
Exa Search API Example

This example demonstrates how to use the Exa Search API tool for advanced, natural language
web search capabilities. Exa provides structured, summarized results suitable for automated
research workflows.

Requirements:
- EXA_API_KEY environment variable must be set
- Install required dependencies: httpx, loguru, swarms

Usage:
    python exa_search_example.py
"""

import os
from dotenv import load_dotenv
from loguru import logger
from swarms_tools.search.exa_search import exa_search

# Load environment variables
load_dotenv()


def main():
    """
    Main function demonstrating Exa Search API usage.
    """
    logger.info("Starting Exa Search API example...")
    
    # Check if API key is available
    api_key = os.getenv("EXA_API_KEY")
    if not api_key:
        logger.error("EXA_API_KEY not found in environment variables")
        logger.info("Please set your Exa API key in the .env file")
        logger.info("You can get an API key from: https://exa.ai/")
        return
    
    try:
        # Example 1: Search for documentation
        logger.info("Example 1: Searching for Python documentation")
        doc_query = "Show me the latest Python 3.12 documentation on dataclasses"
        doc_results = exa_search(doc_query, characters=300, sources=3)
        logger.info(f"Documentation search results:\n{doc_results}")
        
        # Example 2: Search for research papers
        logger.info("Example 2: Searching for research papers")
        research_query = "Recent research on transformer architectures for vision tasks"
        research_results = exa_search(research_query, characters=400, sources=4)
        logger.info(f"Research search results:\n{research_results}")
        
        # Example 3: Search for technical articles
        logger.info("Example 3: Searching for technical articles")
        tech_query = "Best practices for microservices architecture in 2024"
        tech_results = exa_search(tech_query, characters=350, sources=3)
        logger.info(f"Technical search results:\n{tech_results}")
        
        # Example 4: Search for news and updates
        logger.info("Example 4: Searching for news and updates")
        news_query = "Latest developments in quantum computing hardware"
        news_results = exa_search(news_query, characters=300, sources=3)
        logger.info(f"News search results:\n{news_results}")
        
        # Example 5: Search for tutorials and guides
        logger.info("Example 5: Searching for tutorials and guides")
        tutorial_query = "Complete guide to machine learning model deployment with Docker"
        tutorial_results = exa_search(tutorial_query, characters=400, sources=3)
        logger.info(f"Tutorial search results:\n{tutorial_results}")
        
        # Example 6: Search for API documentation
        logger.info("Example 6: Searching for API documentation")
        api_query = "OpenAI API documentation for GPT-4 fine-tuning"
        api_results = exa_search(api_query, characters=350, sources=3)
        logger.info(f"API documentation search results:\n{api_results}")
        
        # Example 7: Search for regulatory information
        logger.info("Example 7: Searching for regulatory information")
        regulatory_query = "GDPR compliance requirements for AI systems in Europe"
        regulatory_results = exa_search(regulatory_query, characters=300, sources=3)
        logger.info(f"Regulatory search results:\n{regulatory_results}")
        
        # Example 8: Search for academic papers
        logger.info("Example 8: Searching for academic papers")
        academic_query = "arXiv papers on large language models and reasoning"
        academic_results = exa_search(academic_query, characters=400, sources=3)
        logger.info(f"Academic search results:\n{academic_results}")
        
        # Example 9: Search for industry reports
        logger.info("Example 9: Searching for industry reports")
        industry_query = "AI market trends and forecasts 2024"
        industry_results = exa_search(industry_query, characters=350, sources=3)
        logger.info(f"Industry search results:\n{industry_results}")
        
        # Example 10: Search for code examples
        logger.info("Example 10: Searching for code examples")
        code_query = "Python examples for async programming with asyncio"
        code_results = exa_search(code_query, characters=300, sources=3)
        logger.info(f"Code search results:\n{code_results}")
        
        logger.info("Exa Search API examples completed successfully!")
        logger.info("Note: Exa provides structured, summarized results with key insights")
        logger.info("The API is optimized for research workflows and documentation search")
        
    except Exception as e:
        logger.error(f"Error with Exa Search API: {e}")
        logger.info("Make sure your API key is valid and you have sufficient credits")
        logger.info("Check the Exa API documentation for usage limits and pricing")


if __name__ == "__main__":
    main()
