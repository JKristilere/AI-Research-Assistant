import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Configuration settings for the AI Research Assistant."""

    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_BASE_URL = os.getenv("GROQ_BASE_URL")
    MODEL_NAME = "llama-3.3-70b-versatile"
    TEMPERATURE = 0.7
    MAX_TOKENS = 4096

    # OUTPUT CONFIGURATION
    OUTPUT_DIR = "outputs"
    REPORT_FORMAT = "markdown"

    # Research Configuration
    MAX_SEARCH_RESULTS = 10
    MAX_SOURCES = 5
    SCRAPING_TIMEOUT = 30

    # Validation
    @classmethod
    def validate(cls):
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set")
        return True
    
settings = Settings()
settings.validate()