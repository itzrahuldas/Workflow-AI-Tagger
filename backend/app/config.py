"""
Configuration module — loads settings from environment variables.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Groq API (OpenAI-compatible)
    groq_api_key: str
    groq_base_url: str = "https://api.groq.com/openai/v1"

    # Model config
    model_name: str = "llama-3.3-70b-versatile"
    max_tokens: int = 500

    # Server config
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
