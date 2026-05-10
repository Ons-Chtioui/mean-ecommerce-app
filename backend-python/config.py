from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "ecommerce"
    EXCHANGE_RATE_API_URL: str = "https://open.er-api.com/v6/latest"
    UPLOAD_DIR: str = "uploads/products"
    PORT: int = 8000

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
