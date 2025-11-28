import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from bot.handlers import start, help_command, handle_message

app = Flask(__name__)

# Initialize the Telegram Application
# We use a global variable to cache the application instance across requests if possible
telegram_app = None

def get_telegram_app():
    global telegram_app
    if telegram_app is None:
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            raise ValueError("TELEGRAM_BOT_TOKEN not set!")
        
        telegram_app = ApplicationBuilder().token(token).build()
        
        # Register handlers
        telegram_app.add_handler(CommandHandler("start", start))
        telegram_app.add_handler(CommandHandler("help", help_command))
        telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
    return telegram_app

@app.route("/api/telegram", methods=["POST"])
def telegram_webhook():
    """
    Webhook endpoint for Telegram updates.
    """
    if request.method == "POST":
        try:
            telegram_app = get_telegram_app()
            
            # Retrieve the JSON update object
            update_json = request.get_json(force=True)
            update = Update.de_json(update_json, telegram_app.bot)
            
            # Process the update
            # Since we are in a serverless environment, we need to await the process_update call
            # We create a new event loop for this request if needed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(telegram_app.process_update(update))
            loop.close()
            
            return "OK"
        except Exception as e:
            print(f"Error processing update: {e}")
            return "Error", 500
    
    return "Invalid Method", 405

@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"
