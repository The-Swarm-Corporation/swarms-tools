import os
import sys
import subprocess

from loguru import logger

try:
    from telegram import Update
    from telegram.ext import (
        ApplicationBuilder,
        CommandHandler,
        ContextTypes,
        MessageHandler,
        filters,
    )
except ImportError as error:
    logger.error(
        f"Telegram API not installed {error}. Attempting to install..."
    )
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "python-telegram-bot",
        ],
        check=True,
    )
    logger.info("Telegram API installed successfully.")


def telegram_check_mention(update: Update) -> bool:
    """Check if the bot was mentioned in the message"""
    message = update.message
    bot_username = update.get_bot().username

    # Check for @mentions
    if message.entities:
        for entity in message.entities:
            if entity.type == "mention":
                mention = message.text[
                    entity.offset : entity.offset + entity.length
                ]
                if mention.lower() == f"@{bot_username.lower()}":
                    return True

    # Check for text_mentions
    if message.entities:
        for entity in message.entities:
            if entity.type == "text_mention" and entity.user.is_bot:
                if (
                    entity.user.username.lower()
                    == bot_username.lower()
                ):
                    return True

    return False


async def telegram_process_message(update: Update) -> str:
    """Clean up message by removing bot mention"""
    message = update.message.text
    bot_username = update.get_bot().username

    # Remove @username
    cleaned_message = message.replace(f"@{bot_username}", "").strip()

    # If the message starts with the bot's username without @, remove it too
    if cleaned_message.lower().startswith(bot_username.lower()):
        cleaned_message = cleaned_message[len(bot_username) :].strip()

    return cleaned_message


async def telegram_start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Handle /start command - only works in DMs"""
    if update.message.chat.type != "private":
        return

    welcome_message = "👋 Hello! I am your medical coding assistant bot. Send me any medical coding question!"
    await update.message.reply_text(welcome_message)
    logger.info(f"Start command from user {update.effective_user.id}")


async def telegram_help(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Handle /help command - only works in DMs"""
    if update.message.chat.type != "private":
        return

    help_message = (
        "Just send me any medical coding question and I'll help you!\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n\n"
        "In groups, tag me with @botname to get my attention!"
    )
    await update.message.reply_text(help_message)
    logger.info(f"Help command from user {update.effective_user.id}")


async def telegram_handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    response: str = None,
):
    """Handle incoming messages - works in DMs and when mentioned in groups"""
    # Check if it's a DM or mention
    if (
        update.message.chat.type != "private"
        and not telegram_check_mention(update)
    ):
        return

    user_id = update.effective_user.id
    logger.info(
        f"Message received from {user_id} in {update.message.chat.type} chat"
    )

    try:
        # Clean up the message
        cleaned_message = await telegram_process_message(update)
        if not cleaned_message:
            return

        # Send response
        await update.message.reply_text(response)
        logger.info(f"Sent response to user {user_id}")

    except Exception as e:
        logger.error(
            f"Error processing message: {str(e)}", exc_info=True
        )
        await update.message.reply_text(
            "Sorry, I encountered an error while processing your request. Please try again."
        )


def telegram_dm_or_tag_api(response: str):
    # Get token from environment variable
    token = os.getenv("TELEGRAM_KEY")
    if not token:
        logger.error(
            "TELEGRAM_KEY not found in environment variables"
        )
        sys.exit(1)

    try:
        # Create application
        application = ApplicationBuilder().token(token).build()

        # Add handlers
        application.add_handler(
            CommandHandler("start", telegram_start)
        )
        application.add_handler(CommandHandler("help", telegram_help))
        application.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                response,
                telegram_handle_message,
            )
        )

        # Run the bot
        logger.info("Bot started successfully")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        logger.error(f"Critical error: {str(e)}", exc_info=True)
        sys.exit(1)
