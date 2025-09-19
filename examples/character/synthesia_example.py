"""
Synthesia API Example

This example demonstrates how to use the Synthesia API tool to create AI-generated videos.
The Synthesia tool allows you to create synthetic videos with AI avatars and text-to-speech.

Requirements:
- SYNTHESIA_API_KEY environment variable must be set
- Install required dependencies: httpx, loguru, python-dotenv

Usage:
    python synthesia_example.py
"""

import os
from dotenv import load_dotenv
from loguru import logger
from swarms_tools.character.synthesia_tool import SynthesiaAPI, synthesia_api

# Load environment variables
load_dotenv()


def main():
    """
    Main function demonstrating Synthesia API usage.
    """
    logger.info("Starting Synthesia API example...")
    
    # Check if API key is available
    api_key = os.getenv("SYNTHESIA_API_KEY")
    if not api_key:
        logger.error("SYNTHESIA_API_KEY not found in environment variables")
        logger.info("Please set your Synthesia API key in the .env file")
        logger.info("You can get an API key from: https://www.synthesia.io/")
        return
    
    try:
        # Example 1: Using the SynthesiaAPI class directly
        logger.info("Example 1: Using SynthesiaAPI class")
        synthesia_client = SynthesiaAPI(bearer_key=api_key)
        
        # Example payload for video creation (based on actual Synthesia API)
        video_payload = {
            "test": True,
            "title": "My AI Generated Video",
            "visibility": "private",
            "aspectRatio": "16:9",
            "script": "Hello! This is an AI-generated video using Synthesia. Welcome to the future of video creation!",
            "avatar": "anna_costume1_cameraA",
            "background": "office_background"
        }
        
        # Create video
        response = synthesia_client.create_video(video_payload)
        logger.info(f"Video creation response: {response}")
        
        # Example 2: Using the simplified function (note: this function has hardcoded payload)
        logger.info("Example 2: Using simplified synthesia_api function")
        logger.info("Note: This function uses a hardcoded payload from the tool implementation")
        simple_response = synthesia_api({})  # Payload is ignored, uses hardcoded values
        logger.info(f"Simple API response: {simple_response}")
        
        # Example 3: Different video configurations
        logger.info("Example 3: Different video configurations")
        
        # Educational video
        educational_payload = {
            "test": True,
            "title": "Educational Video - Python Basics",
            "visibility": "private", 
            "aspectRatio": "16:9",
            "script": "Welcome to Python programming! Today we'll learn about variables, functions, and loops.",
            "avatar": "anna_costume1_cameraA",
            "background": "classroom_background"
        }
        
        edu_response = synthesia_client.create_video(educational_payload)
        logger.info(f"Educational video response: {edu_response}")
        
        # Marketing video
        marketing_payload = {
            "test": True,
            "title": "Product Demo Video",
            "visibility": "private",
            "aspectRatio": "16:9", 
            "script": "Introducing our revolutionary new product! It will change the way you work forever.",
            "avatar": "anna_costume1_cameraA",
            "background": "modern_office"
        }
        
        marketing_response = synthesia_client.create_video(marketing_payload)
        logger.info(f"Marketing video response: {marketing_response}")
        
        logger.info("Synthesia API examples completed successfully!")
        logger.info("Note: Videos are created in test mode. Check your Synthesia dashboard for results.")
        
    except Exception as e:
        logger.error(f"Error creating video: {e}")
        logger.info("Make sure your API key is valid and you have sufficient credits")
        logger.info("Check the Synthesia API documentation for proper payload format")


if __name__ == "__main__":
    main()
