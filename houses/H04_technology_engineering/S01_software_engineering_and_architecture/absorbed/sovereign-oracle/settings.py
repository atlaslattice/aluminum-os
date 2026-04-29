"""
Configuration for Manus 2.0 Self-Improvement Toolkit
Loads API keys from environment variables for multi-LLM routing.
"""
import os

# Multi-LLM API Configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
XAI_API_KEY = os.environ.get("XAI_API_KEY", "")

# Model routing tiers
CHEAP_MODELS = {
    "gemini": "gemini-2.5-flash",
    "deepseek": "deepseek-chat",
    "openai": "gpt-4o-mini",
}
POWER_MODELS = {
    "anthropic": "claude-sonnet-4-20250514",
    "openai": "gpt-5",
    "gemini": "gemini-2.5-pro",
}
REASONING_MODELS = {
    "openai": "o3",
    "anthropic": "claude-opus-4-20250514",
    "xai": "grok-3",
}

# Task complexity thresholds
COMPLEXITY_THRESHOLDS = {
    "simple": 0.3,    # Route to cheap models
    "moderate": 0.6,  # Route to power models
    "complex": 1.0,   # Route to reasoning models
}

# Notion System RAM
NOTION_DATABASE_ID = "add65d86-00d0-46c6-b97b-c0924a94512f"

# Cache settings
CACHE_DIR = "/home/ubuntu/manus_wishlist/cache"
CACHE_TTL_SECONDS = 3600  # 1 hour default

# Log settings
LOG_DIR = "/home/ubuntu/manus_wishlist/logs"
