#!/usr/bin/env python3
"""
Telegram-Discord Bridge Application
Reads messages from Telegram and Discord, forwards to Telegram group
"""

import asyncio
import signal
import sys
from typing import Dict, Any

from config import Config
from utils.logger import logger
from bridges.telegram_reader import TelegramReader
from bridges.discord_reader import DiscordReader
from bridges.telegram_sender import TelegramSender

class BridgeApp:
    """
    Main application class that coordinates all bridges
    """
    
    def __init__(self):
        """Initialize the bridge application"""
        # Validate configuration
        try:
            Config.validate()
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            sys.exit(1)
        
        # Initialize components
        self.telegram_sender = TelegramSender()
        
        # Initialize readers with message handler
        self.telegram_reader = TelegramReader(self.handle_message)
        self.discord_reader = DiscordReader(self.handle_message)
        
        # Control flags
        self.is_running = False
        self.tasks = []
        
        logger.info("Bridge application initialized")
    
    async def handle_message(self, message_data: Dict[str, Any]):
        """
        Handle incoming messages from readers
        
        Args:
            message_data: Dictionary containing message information
        """
        try:
            source = message_data.get('source', 'unknown')
            text = message_data.get('text', '')
            
            if text:
                # Send to Telegram with delay
                await self.telegram_sender.send_with_delay(
                    text=text,
                    source=source
                )
            else:
                logger.warning(f"Received empty message from {source}")
                
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    async def setup_signal_handlers(self):
        """Setup graceful shutdown handlers"""
        loop = asyncio.get_running_loop()
        
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(
                sig,
                lambda s=sig: asyncio.create_task(self.shutdown(s))
            )
    
    async def shutdown(self, sig):
        """Gracefully shutdown the application"""
        logger.info(f"Received exit signal {sig.name}...")
        self.is_running = False
        
        # Stop all readers
        logger.info("Stopping readers...")
        await self.telegram_reader.stop()
        await self.discord_reader.stop()
        
        # Cancel all tasks
        for task in self.tasks:
            task.cancel()
        
        logger.info("Shutdown complete")
        sys.exit(0)
    
    async def run(self):
        """Main application loop"""
        logger.info("Starting Bridge Application...")
        
        try:
            # Setup signal handlers
            await self.setup_signal_handlers()
            
            self.is_running = True
            
            # Start all readers concurrently
            self.tasks = [
                asyncio.create_task(self.telegram_reader.start()),
                asyncio.create_task(self.discord_reader.start())
            ]
            
            logger.info("All readers started, waiting for messages...")
            
            # Wait for all tasks to complete (they shouldn't unless error)
            await asyncio.gather(*self.tasks)
            
        except asyncio.CancelledError:
            logger.info("Tasks cancelled")
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
        finally:
            await self.shutdown(signal.SIGTERM)

def main():
    """Entry point"""
    app = BridgeApp()
    
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()