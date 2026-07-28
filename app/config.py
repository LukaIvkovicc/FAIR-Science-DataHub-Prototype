from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./fair_data_hub.db"
    app_env: str = "local"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

