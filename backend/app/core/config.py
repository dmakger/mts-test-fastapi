from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    LOG_LEVEL: str

    class Config:
        env_file = "backend/.env"
        env_file_encoding = "utf-8"


settings = Settings()
