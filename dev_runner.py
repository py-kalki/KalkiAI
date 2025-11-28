import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file BEFORE importing other modules
load_dotenv()

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from bot.handlers import start, help_command, handle_message

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found in .env file.")
        return

    print("🚀 Starting Big Brother Bot in POLLING mode...")
    
    application = ApplicationBuilder().token(token).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Bot is running. Press Ctrl+C to stop.")
    application.run_polling()

if __name__ == '__main__':
    main()
