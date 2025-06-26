from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    database_url: str
    ollama_model: str
    ollama_address: str
    ollama_timeout: str

settings = Settings()