import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import Message
from utils.logger import logger
from utils.filters import TelegramFilter
from config import Config

class TelegramReader:
    """
    Telegram reader using Telethon (user account)
    Reads messages from specified group/channel
    """
    
    def __init__(self, message_handler):
        """
        Initialize Telegram reader
        
        Args:
            message_handler: Async callback function to handle received messages
        """
        self.api_id = Config.TELEGRAM_API_ID
        self.api_hash = Config.TELEGRAM_API_HASH
        self.phone = Config.TELEGRAM_PHONE
        self.chat_id = Config.TELEGRAM_READ_CHAT_ID
        
        # Create Telegram client
        self.client = TelegramClient('reader_session', self.api_id, self.api_hash)
        
        # Store message handler
        self.message_handler = message_handler
        
        # Initialize filter
        self.filter = TelegramFilter(
            allowed_types=['text'],
            min_length=1
        )
        
        logger.info(f"TelegramReader initialized for chat ID: {self.chat_id}")
    
    async def start(self):
        """Start the Telegram reader client"""
        try:
            # Start client and authenticate
            await self.client.start(phone=self.phone)
            logger.info("Telegram reader client started successfully")
            
            # Get entity info for logging
            entity = await self.client.get_entity(self.chat_id)
            logger.info(f"Monitoring Telegram chat: {entity.title if hasattr(entity, 'title') else entity.id}")
            
            # Register message handler
            @self.client.on(events.NewMessage(chats=[self.chat_id]))
            async def handle_new_message(event):
                """Handle new messages from monitored chat"""
                try:
                    message = event.message
                    
                    # Apply filter
                    if self.filter.should_forward(message):
                        logger.info(f"Received message from Telegram: {message.message[:50]}...")
                        
                        # Call the message handler
                        await self.message_handler({
                            'source': 'telegram',
                            'text': message.message,
                            'raw': message,
                            'sender': message.sender_id,
                            'timestamp': message.date
                        })
                    else:
                        logger.debug(f"Message filtered out: {message.message[:30]}...")
                        
                except Exception as e:
                    logger.error(f"Error handling Telegram message: {e}")
            
            # Keep the client running
            await self.client.run_until_disconnected()
            
        except Exception as e:
            logger.error(f"Error in Telegram reader: {e}")
            raise
    
    async def stop(self):
        """Stop the Telegram reader client"""
        await self.client.disconnect()
        logger.info("Telegram reader stopped")