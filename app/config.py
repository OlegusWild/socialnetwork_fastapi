from pydantic import BaseSettings


class Settings(BaseSettings):
    database_username: str
    database_password: str
    database_hostname: str
    database_port: str
    database_name: str

    secret_key: str
    token_expire_time_minutes: int
    algorithm: str

    # makes it to search in our .env 
    # but the environment vars can be also set on a local machine instead
    class Config:
        env_file='.env'

settings = Settings()