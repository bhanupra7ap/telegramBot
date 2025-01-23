from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging

# Replace with your bot token
BOT_TOKEN = "6227369198:AAHgS6-0A8tJaSRLrgE1gaq4z93AEbB-SMw"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)

# Telegram Bot Application
#application = Application.builder().token(BOT_TOKEN).build()

# Command handler function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        logger.info(f"Received /start command from user {update.effective_user.id}")
        await update.message.reply_text("Hello! I am your Telegram bot. How can I help you?")
    except Exception as e:
        logger.error(f"Error in /start handler: {e}")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    await update.message.reply_text(f"You said: {user_message}")


# Add handler to application
#application.add_handler(CommandHandler("start", start))

@app.route("/webhook", methods=["POST"])
def webhook():
    """Handle incoming Telegram updates."""
    if request.method == "POST":
        try:
            # Get the incoming update
            json_update = request.get_json()
            logger.info(f"Incoming update: {json_update}")

            # Convert JSON to Update object
            update = Update.de_json(json_update, application.bot)

            # Process the update
            application.update_queue.put_nowait(update)
        except Exception as e:
            logger.error(f"Error processing update: {e}")
        return "OK", 200

def main():
    application = Application.builder().token(token).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Register a message handler to echo all text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the bot
    print("Bot is running... Press Ctrl+C to stop.")
    application.run_polling()

if __name__ == "__main__":
    try:
        # Set the webhook URL
        webhook_url = "https://telegrambot-dvnr.onrender.com/webhook"
        application.bot.set_webhook(url=webhook_url)
        logger.info(f"Webhook successfully set to {webhook_url}")

        # Run the Flask app
        app.run(host="0.0.0.0", port=5000)
        
        main()
    except Exception as e:
        logger.error(f"Failed to start the bot: {e}")
