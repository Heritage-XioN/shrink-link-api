from pydantic_settings import BaseSettings

# sets up config for accessing env variables
class Settings(BaseSettings):
    DB_HOSTNAME: str = ""
    DB_PORT: str = ""
    DB_PASSWORD: str = ""
    DB_NAME: str = ""
    DB_DRIVER: str = ""
    DB_USERNAME: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
