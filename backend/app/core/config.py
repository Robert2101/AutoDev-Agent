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
            # This is the most stable way to run on Render Free Tier!
            self.CELERY_BROKER_URL = db_url.replace("postgresql://", "sqla+postgresql://", 1)
            self.CELERY_RESULT_BACKEND = "db+" + db_url
        else:
            # Upstash FIX: Upstash REQUIRES rediss:// (SSL) - we force it here.
            redis_url = self.REDIS_URL.strip()
            if "upstash.io" in redis_url.lower() and redis_url.startswith("redis://"):
                redis_url = redis_url.replace("redis://", "rediss://", 1)
                # Upstash/Render require ssl_cert_reqs to be specified for rediss://
                if "?" not in redis_url:
                    redis_url += "?ssl_cert_reqs=none"
                elif "ssl_cert_reqs" not in redis_url:
                    redis_url += "&ssl_cert_reqs=none"
            
            self.REDIS_URL = redis_url
            self.CELERY_BROKER_URL = redis_url
            self.CELERY_RESULT_BACKEND = redis_url
            
        return self

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a global settings instance
settings = Settings()
