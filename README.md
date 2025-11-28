# HackGPT - The "Big Brother" DevOps Mentor

A personalized, intelligent Telegram bot powered by Google Gemini.
It acts as a bold, honest, and knowledgeable mentor for hacking, DevOps, and engineering.

## 🌟 Features

-   **Custom Persona**: "Big Brother" personality that gives honest, no-nonsense technical advice.
-   **AI-Powered**: Uses Google's **Gemini 1.5 Flash** (or 2.5 Lite) for high-speed, intelligent responses.
-   **Memory**: Remembers your conversation context (Short-term & Long-term).
-   **Persistance**: Supports **Redis** for saving chat history across server restarts.
-   **Serverless**: Designed to run for free on **Vercel**.

## 🛠️ Configuration

The bot is configured via environment variables (in `.env` locally or Vercel Settings).

| Variable | Description | Required |
| :--- | :--- | :--- |
| `TELEGRAM_BOT_TOKEN` | Your Bot Token from @BotFather | ✅ Yes |
| `GEMINI_API_KEY` | API Key from Google AI Studio | ✅ Yes |
| `SYSTEM_PROMPT` | Custom persona/instructions for the AI | ❌ No (Default provided) |
| `REDIS_URL` | Connection string for Redis database | ❌ No (Defaults to local memory) |
| `WEBHOOK_URL` | Your Vercel project URL (for production) | ❌ No (Only for Vercel) |

## 🚀 Quick Start (Local)

1.  **Clone the repository**.
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up secrets**:
    - Rename `.env.example` to `.env`.
    - Add your keys.
4.  **Run the bot**:
    ```bash
    python dev_runner.py
    ```

## ☁️ Deployment (Vercel)

1.  **Install Vercel CLI**: `npm i -g vercel`
2.  **Deploy**: Run `vercel` in the project folder.
3.  **Set Environment Variables**: In Vercel Dashboard, add your keys.
4.  **Set Webhook**:
    ```bash
    curl "https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=<YOUR_VERCEL_URL>/api/telegram"
    ```

## 🧠 Memory & Database

-   **Local Mode**: Uses in-memory storage (RAM). History is lost when you stop the script.
-   **Production Mode**: Add a `REDIS_URL` (e.g., from [Upstash](https://upstash.com/)) to enable persistent memory. The bot will automatically switch to Redis if the variable is present.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
