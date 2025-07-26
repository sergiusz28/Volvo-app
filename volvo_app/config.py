import os
from typing import Optional
from pydantic_settings import BaseSettings


class VolvoConfig(BaseSettings):
    """Configuration settings for Volvo API integration."""
    
    # Volvo API settings
    VOLVO_CLIENT_ID: Optional[str] = 'dc-6gfrjpq4kuq16wc3m586nkiix'
    VOLVO_CLIENT_SECRET: Optional[str] = 'HhLMGiKAn5EHzQsaXFO5KO'
    VOLVO_API_KEY: Optional[str] = '294bd382cb284657b68071709c85e2c0'  # Dodaj API Key z Volvo Developer Portal
    VOLVO_VIN: Optional[str] = 'YV1ZWK8V4S2663123'      # Dodaj VIN Twojego pojazdu
    VOLVO_API_BASE_URL: str = "https://api.volvocars.com"
    VOLVO_REDIRECT_URI: str = "http://localhost:8000/callback"
    
    # Application settings
    APP_NAME: str = "Volvo Integration App"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Security
    SECRET_KEY: Optional[str] = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global configuration instance
config = VolvoConfig()
