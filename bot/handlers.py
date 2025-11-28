from telegram import Update
from telegram.ext import ContextTypes
from bot.ai_service import get_ai_response

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when the command /start is issued."""
    user_first_name = update.effective_user.first_name
    welcome_message = (
        f"Yo, {user_first_name}. I'm your new DevOps mentor.\n\n"
        "I'm here to help you level up your hacking and engineering skills. "
        "No BS, just straight talk and technical facts.\n\n"
        "Ask me anything about Linux, security, coding, or whatever you're breaking today."
    )
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = (
        "Look, it's simple:\n"
        "1. You ask a question.\n"
        "2. I give you the answer.\n\n"
        "I can help with:\n"
        "- Python, JS, Go, Rust\n"
        "- Linux administration\n"
        "- Network security\n"
        "- Docker/K8s\n\n"
        "Just type your message."
    )
    await update.message.reply_text(help_text)

from bot.memory import MemoryStore

# Initialize Memory Store (handles both local and Redis)
memory_store = MemoryStore()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming text messages by sending them to the AI."""
    user_message = update.message.text
    chat_id = update.effective_chat.id
    
    # Show a "typing" action so the user knows we're thinking
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    
    # Retrieve history for this chat
    history = memory_store.get_history(chat_id)
    
    # Get response from AI
    ai_reply = get_ai_response(user_message, chat_history=history)
    
    # Update history
    # We manually append the interaction to our local store
    # Gemini expects: role='user'|'model', parts=['text']
    history.append({'role': 'user', 'parts': [user_message]})
    history.append({'role': 'model', 'parts': [ai_reply]})
    
    # Save back to store
    memory_store.save_history(chat_id, history)
    
    await update.message.reply_text(ai_reply)
