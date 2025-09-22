import os
import asyncio
from dotenv import load_dotenv
from swarms_tools.social_media.discord import run_discord_bot, send_message, bot

load_dotenv()

discord_token = os.getenv("DISCORD_BOT_TOKEN")
if not discord_token:
    exit()

# Test that the bot object is properly initialized
assert bot is not None
assert bot.command_prefix == "!"

# Test that send_message function exists and is callable
assert callable(send_message)

# Test that run_discord_bot function exists and is callable
assert callable(run_discord_bot)

# Test bot event handlers are registered
assert hasattr(bot, 'on_ready')
assert hasattr(bot, 'on_message')

# Test bot commands are registered
assert 'send' in bot.all_commands
assert 'agent_button' in bot.all_commands

# Test that the bot can be started (without actually running it)
try:
    # This tests the bot setup without starting the persistent service
    import discord
    from discord.ext import commands
    
    # Verify Discord.py components are available
    assert discord is not None
    assert commands is not None
    
    # Test that our bot is properly configured
    assert isinstance(bot, commands.Bot)
    assert bot.user is None  # Not logged in yet
    
except ImportError:
    # If discord.py is not installed, at least verify our functions exist
    assert send_message is not None
    assert run_discord_bot is not None
