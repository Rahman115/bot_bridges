import discord
from discord.ext import commands
import asyncio
from utils.logger import logger
from utils.filters import DiscordFilter
from config import Config

class DiscordReader(commands.Bot):
    """
    Discord reader using discord.py
    Reads messages from specified channel
    """
    
    def __init__(self, message_handler):
        """
        Initialize Discord reader
        
        Args:
            message_handler: Async callback function to handle received messages
        """
        intents = discord.Intents.default()
        intents.message_content = True  # Required for reading message content
        intents.guilds = True
        
        super().__init__(command_prefix='!', intents=intents)
        
        self.token = Config.DISCORD_BOT_TOKEN
        self.channel_id = Config.DISCORD_READ_CHANNEL_ID
        self.message_handler = message_handler
        
        # Initialize filter
        self.filter = DiscordFilter(
            allowed_types=['text'],
            min_length=1
        )
        
        logger.info(f"DiscordReader initialized for channel ID: {self.channel_id}")
        
        # Setup event handlers
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup Discord event handlers"""
        
        @self.event
        async def on_ready():
            """Called when bot is ready"""
            logger.info(f'Discord bot logged in as {self.user}')
            for guild in self.guilds:
                logger.info(f"Guild: {guild.name}")
                for channel in guild.text_channels:
                    logger.info(f" - {channel.name} | {channel.id}")
               
            # Get channel info
            channel = self.get_channel(self.channel_id)
            if channel:
                logger.info(f"Monitoring Discord channel: #{channel.name} in {channel.guild.name}")
            else:
                logger.error(f"Could not find Discord channel with ID: {self.channel_id}")
        
        @self.event
        async def on_message(message):
            """Handle new messages"""
            # Ignore messages from self
            if message.author == self.user:
                return
            
            # Check if it's the monitored channel
            if message.channel.id != self.channel_id:
                return
            
            try:
                # Apply filter
                if self.filter.should_forward(message):
                    logger.info(f"Received message from Discord: {message.content[:50]}...")
                    
                    # Call the message handler
                    await self.message_handler({
                        'source': 'discord',
                        'text': message.content,
                        'raw': message,
                        'sender': str(message.author),
                        'channel': message.channel.name,
                        'timestamp': message.created_at
                    })
                else:
                    logger.debug(f"Discord message filtered out: {message.content[:30]}...")
                    
            except Exception as e:
                logger.error(f"Error handling Discord message: {e}")
    
    async def run_bot(self):
        """Start the Discord bot"""
        # await self.start(self.token)
        await super().start(self.token)
    
    async def stop(self):
        """Stop the Discord bot"""
        await self.close()
        logger.info("Discord reader stopped")