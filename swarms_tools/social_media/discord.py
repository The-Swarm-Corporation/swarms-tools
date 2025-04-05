import asyncio
import discord
from discord.ext import commands
from discord import ui, Interaction
from loguru import logger
from typing import Optional
from swarms import Agent

# --------------------------
# Agent Initialization
# --------------------------
# default_agent: Agent = Agent(
#     agent_name="Stock-Analysis-Agent",
#     model_name="gpt-4o-mini",
#     max_loops="auto",
#     interactive=True,
#     streaming_on=True,
# )

# --------------------------
# Discord Bot Setup
# --------------------------
BOT_PREFIX = "!"
bot: commands.Bot = commands.Bot(command_prefix=BOT_PREFIX)


@bot.event
async def on_ready() -> None:
    """
    Event handler called when the bot is ready.
    Logs the bot's username and ID.
    """
    logger.info(f"Logged in as {bot.user.name} (ID: {bot.user.id})")


async def send_message(channel_id: int, message: str) -> None:
    """
    Sends a message to a Discord channel specified by channel_id.

    Args:
        channel_id (int): The target Discord channel ID.
        message (str): The message content to be sent.
    """
    channel: Optional[discord.TextChannel] = bot.get_channel(
        channel_id
    )
    if channel is None:
        logger.error(f"Channel with ID {channel_id} not found.")
        return

    try:
        await channel.send(message)
        logger.info(
            f"Sent message to channel {channel_id}: {message}"
        )
    except Exception as exc:
        logger.error(
            f"Failed to send message to channel {channel_id}: {exc}"
        )


@bot.command(name="send")
async def send(
    ctx: commands.Context, channel_id: int, *, message: str
) -> None:
    """
    Bot command to send a message to a specific channel.
    Usage:
        !send <channel_id> <message>

    Args:
        ctx (commands.Context): The command context.
        channel_id (int): The Discord channel ID.
        message (str): The message to be sent.
    """
    await send_message(channel_id, message)
    await ctx.send(f"Message sent to channel ID {channel_id}.")


# --------------------------
# Auto Reply Functionality
# --------------------------
@bot.event
async def on_message(message: discord.Message) -> None:
    """
    Auto-replies to messages containing specific keywords.
    Currently, if a message contains 'hello', the bot replies with 'Hi there!'.

    Args:
        message (discord.Message): The incoming message.
    """
    # Ignore messages sent by the bot itself.
    if message.author == bot.user:
        return

    # Example auto-response for "hello"
    if "hello" in message.content.lower():
        try:
            await message.channel.send("Hi there!")
            logger.info(
                f"Auto-responded to {message.author} for greeting: {message.content}"
            )
        except Exception as exc:
            logger.error(f"Error sending auto-response: {exc}")

    # Process other commands after auto-replying.
    await bot.process_commands(message)


# --------------------------
# Agent Button UI Component
# --------------------------
class AgentButtonView(ui.View):
    """
    A Discord UI View containing a button that triggers an agent query.
    """

    def __init__(
        self, agent: Agent, *, timeout: Optional[float] = 180
    ):
        """
        Initializes the view with a given agent instance.

        Args:
            agent (Agent): The agent instance to use for queries.
            timeout (Optional[float]): The timeout duration for the view.
        """
        super().__init__(timeout=timeout)
        self.agent = agent

    @ui.button(
        label="Run Agent Query",
        style=discord.ButtonStyle.primary,
        custom_id="agent_button",
    )
    async def run_agent(
        self, button: ui.Button, interaction: Interaction
    ) -> None:
        """
        Callback for the Agent Query button.
        Executes the agent's run method in a separate thread and sends the response.

        Args:
            button (ui.Button): The button that was clicked.
            interaction (Interaction): The interaction context.
        """
        await interaction.response.defer()  # Acknowledge the interaction

        query: str = (
            "What is the current market trend for tech stocks?"
        )
        logger.info(
            f"Received agent button click. Running query: {query}"
        )

        try:
            # Run the agent query in a separate thread to avoid blocking the event loop.
            response: str = await asyncio.to_thread(
                self.agent.run, query
            )
            logger.info("Agent query executed successfully.")
        except Exception as exc:
            response = f"Error running agent query: {exc}"
            logger.error(response)

        # Send the agent's response back to the user.
        await interaction.followup.send(response)


@bot.command(name="agent_button")
async def agent_button(
    ctx: commands.Context, agent: Optional[Agent] = None
) -> None:
    """
    Sends a message with an embedded button to run an agent query.
    Users can click the button to trigger the agent.

    Args:
        ctx (commands.Context): The command context.
        agent (Optional[Agent]): An optional agent instance to use. If not provided, defaults to the pre-defined agent.
    """
    # Use provided agent or default_agent if none is provided.
    view = AgentButtonView(agent)
    await ctx.send(
        "Click the button below to run the agent query:", view=view
    )


def run_discord_bot(token: str) -> None:
    """
    Starts the Discord bot with the provided token.

    Args:
        token (str): The Discord bot token.
    """
    logger.info("Starting Discord bot...")
    bot.run(token)


# if __name__ == "__main__":
#     # Retrieve the Discord bot token from the environment for security.
#     DISCORD_BOT_TOKEN: Optional[str] = os.getenv("DISCORD_BOT_TOKEN")
#     if not DISCORD_BOT_TOKEN:
#         logger.error(
#             "DISCORD_BOT_TOKEN environment variable not found."
#         )
#         exit(1)

#     run_discord_bot(DISCORD_BOT_TOKEN)
