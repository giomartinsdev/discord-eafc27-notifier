from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://fc:fc@localhost:5432/fc27"


settings = Settings()
