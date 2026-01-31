"""
Core configuration settings for the AutoDev Agent backend.
"""
from pydantic import model_validator
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str = "postgresql://autodev:autodev_password@db:5432/autodev_db"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"
    
    # API Keys
    GEMINI_API_KEY: str
    GITHUB_TOKEN: str
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Worker Configuration
    CLONE_DIR: str = "/tmp/autodev-clones"
    MAX_FILE_SIZE: int = 1048576  # 1MB
    MAX_FILES_PER_REPO: int = 100
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    @model_validator(mode='after')
    def sync_redis_urls(self) -> 'Settings':
        """Sync Celery URLs. Use Database if Redis is unavailable (Perfect for Render Free Tier)."""
        db_url = self.DATABASE_URL
        
        # If REDIS_URL is default/localhost, it won't work in the cloud.
        # Fallback to PostgreSQL as the task broker.
        is_redis_missing = (
            not self.REDIS_URL or 
            "redis:6379" in self.REDIS_URL or 
            "localhost" in self.REDIS_URL
        )

        if is_redis_missing:
            # Use Database for tasks
            self.CELERY_BROKER_URL = db_url.replace("postgresql://", "sqla+postgresql://", 1)
            self.CELERY_RESULT_BACKEND = "db+" + db_url
        else:
            # Redis is explicitly set. If it's Upstash, ensure we use SSL (rediss://)
            if "upstash.io" in self.REDIS_URL.lower() and self.REDIS_URL.startswith("redis://"):
                self.REDIS_URL = self.REDIS_URL.replace("redis://", "rediss://", 1)
            
            self.CELERY_BROKER_URL = self.REDIS_URL
            self.CELERY_RESULT_BACKEND = self.REDIS_URL
            
        return self

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a global settings instance
settings = Settings()
