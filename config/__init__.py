# config/__init__.py
"""
Configuration module for system environment variables and app-level settings.
"""

from .settings import (
    DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME,
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, DB_CONFIG
)

__all__ = [
    'DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASSWORD', 'DB_NAME',
    'TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID', 'DB_CONFIG'
]
