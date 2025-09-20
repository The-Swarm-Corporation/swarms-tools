import os
from dotenv import load_dotenv
from swarms_tools.social_media.discord import send_message, run_discord_bot

load_dotenv()

discord_token = os.getenv("DISCORD_BOT_TOKEN")
if not discord_token:
    print("DISCORD_BOT_TOKEN not found in environment variables")
    print("Please set your Discord bot token in the .env file")
    print("To create a Discord bot:")
    print("1. Go to https://discord.com/developers/applications")
    print("2. Create a new application")
    print("3. Go to the 'Bot' section and create a bot")
    print("4. Copy the bot token and add it to your .env file")
    exit()

# Demonstrate Discord bot functionality
print("Discord bot functionality available:")
print("- send_message function for sending messages to channels")
print("- run_discord_bot function for starting the bot")
print("- Auto-reply functionality for specific keywords")
print("- Interactive buttons for agent queries")

# Show bot configuration
print(f"\nBot configuration:")
print(f"Bot Token: {'Set' if discord_token else 'Not set'}")
print("Prefix: !")
print("Auto-reply Keywords: ['hello']")
print("Agent Query: 'What is the current market trend for tech stocks?'")
print("Button Timeout: 180 seconds")

# Show required permissions
permissions = [
    "Send Messages",
    "Read Message History", 
    "Use Slash Commands",
    "Add Reactions",
    "Embed Links"
]

print(f"\nRequired bot permissions:")
for permission in permissions:
    print(f"  - {permission}")

print(f"\nNote: The actual bot running is commented out to avoid starting a persistent service")
print("To start the bot, uncomment: run_discord_bot(discord_token)")
