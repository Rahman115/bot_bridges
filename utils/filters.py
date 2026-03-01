import re
from typing import Optional

class MessageFilter:
    """Filter messages based on criteria"""
    
    def __init__(self, allowed_types=None, keywords=None, min_length=1):
        """
        Initialize filter
        
        Args:
            allowed_types: List of allowed message types (e.g., ['text', 'photo'])
            keywords: List of keywords to filter (if any, only messages containing these)
            min_length: Minimum message length
        """
        self.allowed_types = allowed_types or ['text']
        self.keywords = [k.lower() for k in (keywords or [])]
        self.min_length = min_length
    
    def should_forward(self, message) -> bool:
        """
        Determine if message should be forwarded
        
        Args:
            message: Message object from Telegram or Discord
            
        Returns:
            bool: True if message should be forwarded
        """
        # Check message type
        if not self._check_type(message):
            return False
        
        # Get message text
        text = self._get_text(message)
        if not text:
            return False
        
        # Check minimum length
        if len(text) < self.min_length:
            return False
        
        # Check keywords (if specified)
        if self.keywords:
            text_lower = text.lower()
            if not any(keyword in text_lower for keyword in self.keywords):
                return False
        
        return True
    
    def _check_type(self, message) -> bool:
        """Check if message type is allowed"""
        # Implementation depends on message object structure
        # Will be overridden in specific implementations
        return True
    
    def _get_text(self, message) -> Optional[str]:
        """Extract text from message"""
        # Implementation depends on message object structure
        return str(message) if message else None


class TelegramFilter(MessageFilter):
    """Filter for Telegram messages"""
    
    def _check_type(self, message):
        """Check Telegram message type"""
        # Check if it's a text message
        return hasattr(message, 'message') and message.message
    
    def _get_text(self, message):
        """Get text from Telegram message"""
        return message.message if hasattr(message, 'message') else None


class DiscordFilter(MessageFilter):
    """Filter for Discord messages"""
    
    def _check_type(self, message):
        """Check Discord message type"""
        # Check if it's a text message (not system message)
        return not message.author.bot and message.content
    
    def _get_text(self, message):
        """Get text from Discord message"""
        return message.content