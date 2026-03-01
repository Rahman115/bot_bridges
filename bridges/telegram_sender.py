from telegram import Bot
from telegram.error import TelegramError
import asyncio
from utils.logger import logger
from config import Config

class TelegramSender:
    """
    Telegram sender using python-telegram-bot
    Sends messages to specified Telegram group
    """
    
    def __init__(self):
        """Initialize Telegram sender bot"""
        self.token = Config.TELEGRAM_BOT_TOKEN
        self.chat_id = Config.TELEGRAM_SEND_CHAT_ID
        
        # Create bot instance
        self.bot = Bot(token=self.token)
        
        logger.info(f"TelegramSender initialized for chat ID: {self.chat_id}")
    
    async def send_message(self, text: str, source: str = None):
        """
        Send message to Telegram
        
        Args:
            text: Message text to send
            source: Source of the message (telegram/discord)
        """
        try:
            # Add source prefix if specified
            if source:
                if source == 'discord':
                    prefix = "📱 [Discord] "
                elif source == 'telegram':
                    prefix = "📱 [Telegram] "
                else:
                    prefix = "📱 "
                
                full_text = f"{prefix}{text}"
            else:
                full_text = text
            
            # Send message
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=full_text,
                disable_web_page_preview=True  # Prevent link previews
            )
            
            logger.info(f"Message forwarded to Telegram: {text[:50]}...")
            
        except TelegramError as e:
            logger.error(f"Error sending message to Telegram: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in Telegram sender: {e}")
    
    async def send_with_delay(self, text: str, source: str = None, delay: float = None):
        """
        Send message with delay (to avoid spam detection)
        
        Args:
            text: Message text
            source: Message source
            delay: Delay in seconds (default from config)
        """
        delay = delay or Config.MESSAGE_DELAY
        await asyncio.sleep(delay)
        await self.send_message(text, source)