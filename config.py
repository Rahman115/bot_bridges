import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Centralized configuration management"""
    
    # Telegram Reader (user account)
    TELEGRAM_API_ID = int(os.getenv('TELEGRAM_API_ID', 0))
    TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH', '')
    TELEGRAM_PHONE = os.getenv('TELEGRAM_PHONE', '')
    TELEGRAM_READ_CHAT_ID = int(os.getenv('TELEGRAM_READ_CHAT_ID', 0))
    
    # Telegram Sender (bot)
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_SEND_CHAT_ID = int(os.getenv('TELEGRAM_SEND_CHAT_ID', 0))
    
    # Discord
    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN', '')
    DISCORD_READ_CHANNEL_ID = int(os.getenv('DISCORD_READ_CHANNEL_ID', 0))
    
    # Settings
    MESSAGE_DELAY = float(os.getenv('MESSAGE_DELAY', 2.0))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls):
        """Validate that all required configs are present"""
        required = [
            ('TELEGRAM_API_ID', cls.TELEGRAM_API_ID),
            ('TELEGRAM_API_HASH', cls.TELEGRAM_API_HASH),
            ('TELEGRAM_PHONE', cls.TELEGRAM_PHONE),
            ('TELEGRAM_READ_CHAT_ID', cls.TELEGRAM_READ_CHAT_ID),
            ('TELEGRAM_BOT_TOKEN', cls.TELEGRAM_BOT_TOKEN),
            ('TELEGRAM_SEND_CHAT_ID', cls.TELEGRAM_SEND_CHAT_ID),
            ('DISCORD_BOT_TOKEN', cls.DISCORD_BOT_TOKEN),
            ('DISCORD_READ_CHANNEL_ID', cls.DISCORD_READ_CHANNEL_ID),
        ]
        
        missing = [name for name, value in required if not value]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")