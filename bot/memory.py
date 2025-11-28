import os
import json
import logging

# Try to import redis, but don't fail if it's not installed (fallback to local)
try:
    import redis
except ImportError:
    redis = None

logger = logging.getLogger(__name__)

class MemoryStore:
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL")
        self.redis_client = None
        self.local_store = {}
        
        if self.redis_url and redis:
            try:
                self.redis_client = redis.from_url(self.redis_url)
                # Test connection
                self.redis_client.ping()
                logger.info("✅ Connected to Redis for memory storage.")
            except Exception as e:
                logger.error(f"⚠️ Failed to connect to Redis: {e}. Falling back to local memory.")
                self.redis_client = None
        else:
            if self.redis_url and not redis:
                logger.warning("⚠️ REDIS_URL found but 'redis' package not installed. Using local memory.")
            else:
                logger.info("ℹ️ No REDIS_URL set. Using in-memory storage (data will be lost on restart).")

    def get_history(self, chat_id):
        """Retrieve chat history for a given chat_id."""
        if self.redis_client:
            try:
                data = self.redis_client.get(str(chat_id))
                if data:
                    return json.loads(data)
                return []
            except Exception as e:
                logger.error(f"Redis get error: {e}")
                return []
        else:
            return self.local_store.get(chat_id, [])

    def save_history(self, chat_id, history):
        """Save chat history for a given chat_id."""
        # Limit history size to prevent infinite growth (e.g., last 20 messages)
        # Each interaction is 2 parts (user + model), so 20 messages = 10 turns
        trimmed_history = history[-20:]
        
        if self.redis_client:
            try:
                # Expire data after 24 hours (86400 seconds) to save space
                self.redis_client.setex(str(chat_id), 86400, json.dumps(trimmed_history))
            except Exception as e:
                logger.error(f"Redis set error: {e}")
        else:
            self.local_store[chat_id] = trimmed_history

    def clear_history(self, chat_id):
        """Clear history for a chat."""
        if self.redis_client:
            self.redis_client.delete(str(chat_id))
        elif chat_id in self.local_store:
            del self.local_store[chat_id]
