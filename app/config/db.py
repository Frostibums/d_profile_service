from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    db_url: str = "postgresql+asyncpg://user:password@localhost:5432/profile_db"


db_settings = DatabaseConfig()
