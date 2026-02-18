import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Application settings using standard os.getenv to avoid extra dependencies.
    """
    APP_NAME: str = os.getenv("APP_NAME", "restrict-llm")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Default timeouts
    DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", "30"))

settings = Settings()
