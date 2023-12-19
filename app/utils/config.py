from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    test_database_url: str = ''
    secret_key: str
    algorithm: str
    access_token_expire_seconds: int
    access_token_expire_minutes: int = 60
    cloudinary_name: str = ''
    cloudinary_api_key: str = ''
    cloudinary_api_secret: str = ''
    mail_username: str = ''
    mail_password: str = ''
    mail_port: int = 2525
    mail_server: str = ''

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
