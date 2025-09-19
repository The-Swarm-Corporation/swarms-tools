"""
Discord Bot Example

This example demonstrates how to use the Discord integration tools to create a Discord bot
with auto-reply functionality, agent integration, and interactive UI components.

Requirements:
- DISCORD_BOT_TOKEN environment variable must be set
- Install required dependencies: discord.py, loguru, swarms, asyncio

Usage:
    python discord_example.py
"""

import os
import asyncio
from dotenv import load_dotenv
from loguru import logger
from swarms_tools.social_media.discord import run_discord_bot, send_message

# Load environment variables
load_dotenv()


def main():
    """
    Main function demonstrating Discord bot usage.
    """
    logger.info("Starting Discord Bot example...")
    
    # Check if Discord bot token is available
    discord_token = os.getenv("DISCORD_BOT_TOKEN")
    if not discord_token:
        logger.error("DISCORD_BOT_TOKEN not found in environment variables")
        logger.info("Please set your Discord bot token in the .env file")
        logger.info("To create a Discord bot:")
        logger.info("1. Go to https://discord.com/developers/applications")
        logger.info("2. Create a new application")
        logger.info("3. Go to the 'Bot' section and create a bot")
        logger.info("4. Copy the bot token and add it to your .env file")
        logger.info("5. Set the required permissions and invite the bot to your server")
        return
    
    try:
        # Example 1: Basic Discord bot functionality
        logger.info("Example 1: Discord bot features")
        
        features = [
            "Auto-reply to messages containing specific keywords",
            "Send messages to specific channels",
            "Interactive buttons for agent queries",
            "Command-based interactions",
            "Event handling for message processing"
        ]
        
        for feature in features:
            logger.info(f"  - {feature}")
        
        # Example 2: Bot commands available
        logger.info("Example 2: Available bot commands")
        
        commands = [
            "!send <channel_id> <message> - Send a message to a specific channel",
            "!agent_button - Create an interactive button for agent queries",
            "Auto-reply to 'hello' messages with 'Hi there!'"
        ]
        
        for command in commands:
            logger.info(f"  - {command}")
        
        # Example 3: Agent integration
        logger.info("Example 3: Agent integration features")
        
        agent_features = [
            "Button-based agent query execution",
            "Asynchronous agent processing",
            "Error handling for agent responses",
            "Customizable agent queries"
        ]
        
        for feature in agent_features:
            logger.info(f"  - {feature}")
        
        # Example 4: Usage instructions
        logger.info("Example 4: Usage instructions")
        
        instructions = [
            "1. Set DISCORD_BOT_TOKEN in your .env file",
            "2. Invite the bot to your Discord server with appropriate permissions",
            "3. Use !send command to send messages to channels",
            "4. Use !agent_button to create interactive agent queries",
            "5. The bot will auto-reply to messages containing 'hello'"
        ]
        
        for instruction in instructions:
            logger.info(f"  {instruction}")
        
        # Example 5: Bot permissions needed
        logger.info("Example 5: Required bot permissions")
        
        permissions = [
            "Send Messages",
            "Read Message History", 
            "Use Slash Commands",
            "Add Reactions",
            "Embed Links"
        ]
        
        for permission in permissions:
            logger.info(f"  - {permission}")
        
        # Example 6: Bot configuration
        logger.info("Example 6: Bot configuration")
        
        config_info = [
            f"Bot Token: {'Set' if discord_token else 'Not set'}",
            "Prefix: !",
            "Auto-reply Keywords: ['hello']",
            "Agent Query: 'What is the current market trend for tech stocks?'",
            "Button Timeout: 180 seconds"
        ]
        
        for info in config_info:
            logger.info(f"  - {info}")
        
        # Example 7: Error handling
        logger.info("Example 7: Error handling features")
        
        error_features = [
            "Graceful handling of network errors",
            "Logging of all bot activities",
            "Exception handling for agent queries",
            "Channel validation before sending messages"
        ]
        
        for feature in error_features:
            logger.info(f"  - {feature}")
        
        # Example 8: Bot lifecycle
        logger.info("Example 8: Bot lifecycle")
        
        lifecycle_steps = [
            "1. Bot initialization and login",
            "2. Event listener setup",
            "3. Command registration",
            "4. Auto-reply system activation",
            "5. Agent integration setup",
            "6. Ready for user interactions"
        ]
        
        for step in lifecycle_steps:
            logger.info(f"  {step}")
        
        # Note: The actual bot running is commented out to avoid starting a persistent service
        logger.info("Example 9: Starting Discord bot (commented out)")
        logger.info("To start the bot, uncomment the following line:")
        logger.info("# run_discord_bot(discord_token)")
        
        # Uncomment the line below to actually start the bot
        # run_discord_bot(discord_token)
        
        logger.info("Discord Bot examples completed successfully!")
        logger.info("Note: The bot is designed to run continuously and handle real-time interactions")
        logger.info("Make sure to properly configure your Discord application and bot permissions")
        
    except Exception as e:
        logger.error(f"Error with Discord bot: {e}")
        logger.info("Make sure your bot token is valid and the bot has proper permissions")
        logger.info("Check the Discord Developer Portal for bot configuration")


if __name__ == "__main__":
    main()
