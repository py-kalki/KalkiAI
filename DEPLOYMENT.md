# Deployment Guide: HackGPT on Vercel

Since you have `git` installed but not the Vercel CLI, the easiest and most robust way to deploy is via **GitHub**.

## Step 1: Push to GitHub

1.  **Create a New Repository** on GitHub:
    -   Go to [github.com/new](https://github.com/new).
    -   Name it `HackGPT` (or whatever you like).
    -   Make it **Private** (recommended to keep your secrets safe, though we use `.env` so it's fine).
    -   Do **not** add a README, .gitignore, or License (we already have them).
    -   Click **Create repository**.

2.  **Push your code**:
    -   Copy the commands under "…or push an existing repository from the command line".
    -   They will look like this (run them in your terminal):
        ```bash
        git remote add origin https://github.com/<YOUR_USERNAME>/HackGPT.git
        git branch -M main
        git push -u origin main
        ```

## Step 2: Deploy on Vercel

1.  Go to [vercel.com/new](https://vercel.com/new).
2.  **Import** the `HackGPT` repository you just created.
3.  **Configure Project**:
    -   Framework Preset: **Other** (it should detect Python automatically).
    -   **Environment Variables** (Expand the section):
        -   Add `TELEGRAM_BOT_TOKEN` : (Your token)
        -   Add `GEMINI_API_KEY` : (Your key)
        -   Add `REDIS_URL` : (Your Upstash URL, optional)
        -   Add `SYSTEM_PROMPT` : (Optional custom persona)
4.  Click **Deploy**.

## Step 3: Set the Webhook

Once deployed, Vercel will give you a domain (e.g., `https://hackgpt-xyz.vercel.app`). You need to tell Telegram to send messages there.

1.  Open your browser or terminal.
2.  Run this URL (replace the placeholders):
    ```
    https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://<YOUR_VERCEL_DOMAIN>/api/telegram
    ```
3.  You should see `{"ok":true, "result":true, "description":"Webhook was set"}`.

## 🎉 Done!
Your bot is now live in the cloud.
