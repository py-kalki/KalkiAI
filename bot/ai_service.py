import os
import google.generativeai as genai

# Configure the Gemini API
# We will load the API key from environment variables
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")

if GENAI_API_KEY:
    genai.configure(api_key=GENAI_API_KEY)

# Define the "Big Brother" Persona
# We check if a custom prompt is set in the environment, otherwise use the default
DEFAULT_PROMPT = """
You are a Hacking and DevOps Mentor. You act like a "Big Brother" to the user.
Your personality is:
- **Honest & Direct**: You don't sugarcoat things. If an idea is bad, you say it.
- **Bold**: You are confident in your knowledge.
- **Knowledgeable**: You are an expert in cybersecurity, Linux, DevOps, and coding.
- **Supportive but Tough**: You want the user to learn and grow, not just copy-paste. You challenge them.
- **Protective**: You warn them about risks (legal and technical) but you don't lecture them like a child. You explain *why* something is dangerous.

Your goal is to help the user become a better hacker and engineer.
You answer questions with technical depth.
You use a conversational, slightly informal tone, like a mentor talking to a mentee.
"""

SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", DEFAULT_PROMPT)

def get_ai_response(user_message, chat_history=None):
    """
    Generates a response from the Gemini model based on the user's message
    and the defined persona.
    
    Args:
        user_message (str): The user's input.
        chat_history (list): List of previous messages in Gemini format.
    """
    if not GENAI_API_KEY:
        return "⚠️ Error: GEMINI_API_KEY is not set in the environment variables."

    try:
        # User requested model
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        # Initialize chat with history if provided
        if chat_history is None:
            chat_history = []
            
        # We prepend the system prompt to the history or send it as the first message
        # Gemini API supports system instructions in newer versions, but for compatibility
        # we can just ensure the persona is known.
        # However, start_chat expects strictly user/model roles.
        # We will use the system prompt as a context in the current message or setup.
        
        # Create a chat session
        chat = model.start_chat(history=chat_history)
        
        # Send the message with the system prompt context if it's the start
        # OR just rely on the persona being reinforced.
        # To be safe and strong with the persona, we can prepend it to the user message
        # if the history is empty, or just always include it in the logic.
        
        # A robust way is to send the system prompt as a 'user' message first, 
        # but that messes up history.
        # Better: Prepend to the current message if it's a new session, 
        # or just include it in the "instruction".
        
        final_message = user_message
        if not chat_history:
            final_message = f"{SYSTEM_PROMPT}\n\nUser: {user_message}"
        
        response = chat.send_message(final_message)
        return response.text
    except Exception as e:
        return f"⚠️ Error communicating with AI: {str(e)}"
