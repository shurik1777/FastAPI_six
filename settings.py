from pydantic_settings import BaseSettings  # необходимо установить pip install pydantic-settings

from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
