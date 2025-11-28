import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from bot.handlers import start, help_command, handle_message

app = Flask(__name__)

import os
import asyncio
import traceback
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from bot.handlers import start, help_command, handle_message

app = Flask(__name__)

@app.route("/api/telegram", methods=["POST"])
def telegram_webhook():
    """
    Webhook endpoint for Telegram updates.
    """
    if request.method == "POST":
        try:
            token = os.getenv("TELEGRAM_BOT_TOKEN")
            if not token:
                print("❌ Error: TELEGRAM_BOT_TOKEN not set!")
                return "Config Error", 500

            # Build the application FRESH for every request
            # This prevents issues with closed event loops in serverless environments
            telegram_app = ApplicationBuilder().token(token).build()
            
            # Register handlers
            telegram_app.add_handler(CommandHandler("start", start))
            telegram_app.add_handler(CommandHandler("help", help_command))
            telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
            
            # Process the update in a new event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Initialize the app FIRST (required for v20+)
            loop.run_until_complete(telegram_app.initialize())
            
            # Retrieve the JSON update object
            # We pass the bot object from the initialized app
            update_json = request.get_json(force=True)
            update = Update.de_json(update_json, telegram_app.bot)
            
            # Process update
            loop.run_until_complete(telegram_app.process_update(update))
            loop.run_until_complete(telegram_app.shutdown())
            
            loop.close()
            
            return "OK"
        except Exception as e:
            print(f"Error processing update: {e}")
            traceback.print_exc()
            return "Error", 500
    
    return "Invalid Method", 405
    
    return "Invalid Method", 405

@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"
